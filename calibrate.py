"""単体の事前トリム調整: 同じ設定で10回測定 → 小幅補正 → 10回検証。"""

import configparser
import csv
from datetime import datetime
import json
import math
from pathlib import Path
import statistics
import tempfile
import time

from codrone_edu.drone import Drone
from codrone_edu.system import ModeFlight


class SetTrim:
    def __init__(self, config_file=None):
        self.config_file = Path(config_file) if config_file else Path(__file__).with_name('config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file, encoding='utf-8')
        self.roll_trim = self.config.getint('TRIM', 'roll_trim', fallback=0)
        self.pitch_trim = self.config.getint('TRIM', 'pitch_trim', fallback=0)
        if not all(-100 <= value <= 100 for value in self.load_trim_config()):
            raise ValueError('config.ini のトリム値は -100～100 で指定してください')

    def load_trim_config(self):
        return self.roll_trim, self.pitch_trim

    def save_trim_config(self):
        if not self.config.has_section('TRIM'):
            self.config.add_section('TRIM')
        self.config['TRIM']['roll_trim'] = str(self.roll_trim)
        self.config['TRIM']['pitch_trim'] = str(self.pitch_trim)
        # 書き込み途中で失敗しても、保存済みのファイルを壊さない。
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode='w', encoding='utf-8', dir=self.config_file.parent,
                prefix=self.config_file.name + '.', suffix='.tmp', delete=False,
            ) as configfile:
                temporary = Path(configfile.name)
                self.config.write(configfile)
            temporary.replace(self.config_file)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        print(f'トリム値を {self.config_file} に保存しました')

    def measure_flights(self, drone, phase, log_dir):
        """同一トリムで10回。位置の回帰直線の傾きを各飛行の流れとする。"""
        results = []
        attempts = {}
        while len(results) < 10:
            trial = len(results) + 1
            attempts[trial] = attempts.get(trial, 0) + 1
            print(f'\n{phase}: {trial}/10 回目 / roll={self.roll_trim}, pitch={self.pitch_trim}')
            while True:
                command = input('同じ開始位置・向きに戻し、飛行範囲を確認してEnter（qで中止）: ')
                if command.strip().lower() == 'q':
                    raise InterruptedError('ユーザーが測定を中止しました')
                if not command.strip():
                    break
                print('開始する場合は何も入力せずEnter、中止する場合はqを入力してください。')

            state = list(drone.get_state_data(delay=0.1))
            age = time.time() - drone.timeStartProgram - state[0]
            if state[0] <= 0 or not 0 <= age <= 1:
                raise TimeoutError('離陸前の機体状態を受信できません')
            if state[2] is not ModeFlight.Ready:
                raise RuntimeError(f'離陸可能な状態ではありません: {state[2]}')
            if state[6] < 30:
                print('A\n「ドローン、完全に沈黙！ 予備電源、作動しません！」')
                print('B\n「そんな……！ 回路が焼き切れたの！？ それとも拒絶しているというの、せいじ君が……！」')
                raise RuntimeError('バッテリーが30%未満です。測定を中止します')

            samples = []
            status = 'incomplete'
            reason = ''
            airborne = False
            retry_measurement = False
            try:
                drone.set_trim(self.roll_trim, self.pitch_trim)
                time.sleep(1)
                for _ in range(3):
                    if tuple(drone.get_trim()) == self.load_trim_config():
                        break
                    time.sleep(0.1)
                else:
                    raise RuntimeError('機体に設定したトリム値を確認できません')
                airborne = True  # takeoff内部の中断時も着陸を試みる。
                drone.takeoff()
                started = time.monotonic()
                last_position = -1
                while time.monotonic() - started < 4:
                    tick = time.monotonic()
                    # 最初の1秒は安定待ち。下降や位置補正をせず無操作を測る。
                    drone.hover(0.01)
                    position = list(drone.get_position_data())
                    # 2.10の取得関数はキャッシュを返すため、受信時刻も読む。
                    flow = list(drone.get_flow_data())
                    distance = list(drone.get_range_data())
                    state = list(drone.get_state_data())
                    elapsed = time.monotonic() - started
                    received = time.time() - drone.timeStartProgram
                    values = position + flow + distance + [state[0], state[6]]
                    if not all(math.isfinite(value) for value in values):
                        raise ValueError('センサーが有限値以外を返しました')
                    samples.append({
                        'phase': phase, 'trial': trial, 'elapsed_s': elapsed,
                        'stage': 'settling' if elapsed < 1 else 'measuring',
                        'roll_trim': self.roll_trim, 'pitch_trim': self.pitch_trim,
                        'position_time_s': position[0],
                        'x_m': position[1], 'y_m': position[2], 'z_m': position[3],
                        'flow_time_s': flow[0], 'flow_x_raw': flow[1], 'flow_y_raw': flow[2],
                        'range_time_s': distance[0], 'height_m': distance[2] / 1000,
                        'state_time_s': state[0], 'flight_state': state[2].name,
                        'battery_percent': state[6],
                        'fresh_position': position[0] > last_position,
                    })
                    if any(packet[0] <= 0 or not 0 <= received - packet[0] <= 1
                        for packet in (position, flow, distance, state)):
                        retry_measurement = True
                        stale = [name for name, packet in (
                            ('position', position), ('flow', flow),
                            ('range', distance), ('state', state),
                        ) if packet[0] <= 0 or not 0 <= received - packet[0] <= 1]
                        raise TimeoutError(f'センサーデータが未受信または1秒以上更新されていません: {stale}')
                    if state[2] is not ModeFlight.Flight:
                        raise RuntimeError(f'通常の飛行状態ではありません: {state[2]}')
                    if state[6] < 20:
                        print('A\n「ドローン、完全に沈黙！ 予備電源、作動しません！」')
                        print('B\n「そんな……！ 回路が焼き切れたの！？ それとも拒絶しているというの、せいじ君が……！」')
                        raise RuntimeError('飛行中にバッテリーが20%未満になりました')
                    if not 0.3 <= distance[2] / 1000 <= 1.5:
                        retry_measurement = True
                        raise RuntimeError(f'測定高度が0.3～1.5mの範囲外です: {distance[2] / 1000:.3f}m')
                    if math.hypot(position[1], position[2]) > 0.75:
                        raise RuntimeError('離陸地点からの水平ずれが0.75mを超えました')
                    last_position = max(last_position, position[0])
                    time.sleep(max(0, 0.1 - (time.monotonic() - tick)))

                measured = [row for row in samples
                            if row['stage'] == 'measuring' and row['fresh_position']]
                if len(measured) < 10:
                    raise RuntimeError('更新済みの位置データが10点未満です')
                timestamps = [row['position_time_s'] for row in measured]
                if timestamps[-1] - timestamps[0] < 2:
                    raise RuntimeError('有効な測定時間が2秒未満です')
                heights = [row['height_m'] for row in measured]
                if max(heights) - min(heights) > 0.15:
                    raise RuntimeError('測定中の高度変動が0.15mを超えました')
                vx = statistics.linear_regression(timestamps, [row['x_m'] for row in measured]).slope
                vy = statistics.linear_regression(timestamps, [row['y_m'] for row in measured]).slope
                speeds = []
                for previous, current in zip(measured, measured[1:]):
                    dt = current['position_time_s'] - previous['position_time_s']
                    speeds.append(((current['x_m'] - previous['x_m']) / dt) ** 2
                                  + ((current['y_m'] - previous['y_m']) / dt) ** 2)
                results.append({
                    'trial': trial, 'vx_m_s': vx, 'vy_m_s': vy,
                    'rms_speed_m_s': math.sqrt(statistics.mean(speeds)),
                    'battery_percent': measured[0]['battery_percent'],
                })
                status = 'complete'
                print(f'平均的な流れ: 前後={vx:+.4f} m/s、左右={vy:+.4f} m/s')
            except BaseException as error:
                status = 'failed'
                reason = f'{type(error).__name__}: {error}'
                if not retry_measurement or attempts[trial] >= 3:
                    raise
            finally:
                try:
                    if airborne:
                        drone.land()
                        landed = False
                        deadline = time.monotonic() + 5
                        while time.monotonic() < deadline:
                            state = list(drone.get_state_data(delay=0.1))
                            age = time.time() - drone.timeStartProgram - state[0]
                            if state[0] > 0 and 0 <= age <= 1 and state[2] is ModeFlight.Ready:
                                landed = True
                                break
                        if not landed:
                            raise TimeoutError('着陸完了を確認できません。以降の飛行を中止します')
                except BaseException as error:
                    status = 'failed'
                    reason += f' / landing: {type(error).__name__}: {error}'
                    raise
                finally:
                    # 中断や着陸失敗でも、それまでの測定を残す。
                    suffix = '' if attempts[trial] == 1 else f'_retry{attempts[trial] - 1}'
                    with (log_dir / f'{phase}_{trial:02d}{suffix}.csv').open(
                        'x', newline='', encoding='utf-8-sig',
                    ) as logfile:
                        fields = list(samples[0]) if samples else ['phase', 'trial']
                        writer = csv.DictWriter(logfile, fieldnames=fields + ['status', 'reason'])
                        writer.writeheader()
                        for row in samples or [{'phase': phase, 'trial': trial}]:
                            writer.writerow(dict(row, status=status, reason=reason))
            if status == 'failed':
                print(f'測定を中断して着陸しました: {reason}')
                print(f'完了済みの{len(results)}回は保持しています。この回は集計しません。')
                print('床面・機体・センサーと飛行範囲を確認してください。次のEnterで再試行、qで中止します。')
        return results

    def summarize_measurements(self, results):
        if len(results) != 10:
            raise ValueError('集計には完了した10回分の測定が必要です')
        summary = {}
        for key in ('vx_m_s', 'vy_m_s', 'rms_speed_m_s'):
            ordered = sorted(results, key=lambda row: (row[key], row['trial']))
            if not all(math.isfinite(row[key]) for row in ordered):
                raise ValueError('集計値に有限値以外が含まれています')
            # 最大・最小を1回ずつ除外して8回を平均。除外番号も残す。
            retained = ordered[1:-1]
            values = [row[key] for row in retained]
            summary[key] = {
                'mean': statistics.mean(values), 'stdev': statistics.stdev(values),
                'excluded_trials': [ordered[0]['trial'], ordered[-1]['trial']],
                'retained_trials': [row['trial'] for row in retained],
            }
        summary['flights'] = results
        return summary

    def calculate_trim(self, summary):
        """暫定の小幅補正。流速をそのままトリム値へ換算しない。"""
        values = []
        # 位置は前(+)、左(+)。トリムは前(+)、右(+)。
        for current, key, direction in (
            (self.roll_trim, 'vy_m_s', 1), (self.pitch_trim, 'vx_m_s', -1),
        ):
            mean = summary[key]['mean']
            # 2cm/s以下、または飛行間のばらつきに対して不明瞭なら変更しない。
            threshold = max(0.02, 2 * summary[key]['stdev'] / math.sqrt(8))
            step = direction * (2 if mean > 0 else -2) if abs(mean) > threshold else 0
            values.append(max(-100, min(100, current + step)))
        return tuple(values)

    def set_trim_start(self, drone):
        original = self.load_trim_config()
        log_dir = Path(__file__).with_name('calibration_logs') / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        log_dir.mkdir(parents=True, exist_ok=False)
        report = {'original_trim': original, 'status': 'started'}
        saved = False
        print('補正前10回 → トリムを最大2ずつ補正 → 補正後10回を実施します')
        print(f'測定ログ: {log_dir}')
        try:
            before = self.summarize_measurements(self.measure_flights(drone, 'before', log_dir))
            report['before'] = before
            self.roll_trim, self.pitch_trim = self.calculate_trim(before)
            report['candidate_trim'] = self.load_trim_config()
            print(f'候補トリム: roll={self.roll_trim}, pitch={self.pitch_trim}')
            after = self.summarize_measurements(self.measure_flights(drone, 'after', log_dir))
            report['after'] = after
            # 符号付き平均の相殺だけで「改善」としない。
            uncertainty = 2 * math.sqrt((before['rms_speed_m_s']['stdev'] ** 2
                                         + after['rms_speed_m_s']['stdev'] ** 2) / 8)
            improved = (before['rms_speed_m_s']['mean'] - after['rms_speed_m_s']['mean']
                        > max(0.005, uncertainty))
            for key, index in (('vx_m_s', 1), ('vy_m_s', 0)):
                old = abs(before[key]['mean'])
                new = abs(after[key]['mean'])
                improved = improved and new <= max(0.02, old)
                if self.load_trim_config()[index] != original[index]:
                    improved = improved and new < old
            if self.load_trim_config() == original:
                report['status'] = 'unchanged'
                print('明確な補正方向がないため、設定を変更しません')
            elif improved:
                self.save_trim_config()
                saved = True
                report['status'] = 'saved'
            else:
                report['status'] = 'not_improved'
                print('改善を確認できなかったため元のトリムへ戻します。設定は保存しません')
            print(f"流れのRMS（8回平均）: {before['rms_speed_m_s']['mean']:.4f}"
                  f" → {after['rms_speed_m_s']['mean']:.4f} m/s")
        except BaseException as error:
            report['status'] = 'aborted'
            report['reason'] = f'{type(error).__name__}: {error}'
            raise
        finally:
            try:
                if not saved:
                    self.roll_trim, self.pitch_trim = original
                    drone.set_trim(*original)
                    time.sleep(1)
                    for _ in range(3):
                        if tuple(drone.get_trim()) == original:
                            break
                        time.sleep(0.1)
                    else:
                        raise RuntimeError('元の機体トリムへの復元を確認できません')
            except BaseException as error:
                report['restore_error'] = f'{type(error).__name__}: {error}'
                print('元の機体トリムへの復元に失敗しました。summary.jsonを確認してください')
                raise
            finally:
                with (log_dir / 'summary.json').open('x', encoding='utf-8') as logfile:
                    json.dump(report, logfile, ensure_ascii=False, indent=2, allow_nan=False)


if __name__ == '__main__':
    set_trim = SetTrim()
    drone = Drone()
    try:
        drone.pair()
        set_trim.set_trim_start(drone)
    except (KeyboardInterrupt, InterruptedError):
        print('調整を中止しました。保存済みの設定は変更していません')
        raise SystemExit(1)
    finally:
        drone.close()




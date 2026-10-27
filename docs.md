# CoDrone EDU Python 関数ガイド

CoDrone EDU を Python から操作するときに使う関数を、用途別にまとめています。まず基本例を読み、必要な関数を表から探してください。表の関数は `drone.関数名(...)` の形で呼び出します。

- 参照：[Robolink 公式ドキュメント（version 2.10）](https://docs.robolink.com/docs/CoDroneEDU/Python/Drone-Function-Documentation/#pair)
- 確認日：2026年10月20日
- 対象：このプロジェクトの `codrone-edu==2.10`。引数・戻り値はローカルの `.venv/Lib/site-packages/codrone_edu/drone.py` でも確認しています。公式資料と実装の差は末尾に記載しています。
- 主要機能の要約です。全引数や機種ごとの対応状況は公式資料を参照してください。実機での動作確認は行っていません。

## 最初に読む：基本の流れ

コントローラーと機体をペアリングし、コントローラーを USB で PC に接続してから実行します。`pair()` は、プログラムからコントローラーへの接続を開く関数です。

```python
from codrone_edu.drone import Drone

drone = Drone()
drone.pair()  # USB ポートを自動検出する
# 自動検出できない場合は、上の行を drone.pair("COM3") などに変更する

try:
    drone.takeoff()
    drone.hover(2)  # 2秒間、その場にとどまる
finally:
    try:
        drone.land()
    finally:
        drone.close()
```

`finally` は処理の途中で例外が発生した場合も、着陸と接続終了を試みるための書き方です。通信が切れた場合など、着陸の成功を保証するものではありません。

### 目的に合う移動方法を選ぶ

| やりたいこと | 使う関数 | 指定例 |
| --- | --- | --- |
| 方向・パワー・時間で動かす | `go()` | `drone.go("forward", 30, 1)` |
| 距離を指定して動かす | `move_forward()` など | `drone.move_forward(50, "cm", 0.5)` |
| 複数の方向へ同時に動かす | `move_distance()` | `drone.move_distance(0.5, 0.5, 0, 0.5)` |
| 離陸地点を基準に目的地へ向かう | `send_absolute_position()` | 下の位置指定の表を参照 |
| 複数の操縦量を組み合わせる | `set_*()` と `move()` | 下の飛行変数の節を参照 |

## 1. 接続・離着陸

| 関数 | 動作・用途 | 注意事項 |
| --- | --- | --- |
| `pair(portname=None)` | プログラムとコントローラーの接続を開く。 | 省略時は自動検出。例：`pair("COM3")`。 |
| `takeoff()` | 自動で高度約80 cmまで上昇してホバリングし、約1秒間姿勢を安定させる。 | 離陸高度や設定は変更できない。 |
| `hover(秒数)` | 指定した秒数、ホバリングする。 | — |
| `land()` | 他の操縦コマンドを停止し、ホバリングを経て着陸する。 | 飛行終了時に使用する。 |
| `close()` | プログラムとコントローラーの接続を閉じる。 | 操作終了時に呼ぶ。着陸の代わりにはならない。 |
| `emergency_stop()` | モーターを即座に停止する。 | 空中では落下する。通常の終了には `land()` を使う。 |

**基本的な実行順序：** `pair()` → `takeoff()` → 飛行操作 → `land()` → `close()`

離陸直後に着陸させる場合も、間に `hover(1)` などを入れてください。公式資料では、直後の着陸指示が取りこぼされる場合があると説明されています。

## 2. 移動・位置指定

| 関数 | 動作・用途 | 引数・補足 |
| --- | --- | --- |
| `go(direction, power=50, duration=1)` | 方向・パワー・秒数で移動する。 | 方向は `"forward"`、`"backward"`、`"left"`、`"right"`、`"up"`、`"down"`。パワーは0～100。 |
| `avoid_wall(timeout=2, distance=70)` | 前方センサーを使って目標距離に近づくよう前後に調整する。 | 秒数と距離（cm）を指定。実装では目標付近で安定すると早期終了する。 |
| `keep_distance(timeout=2, distance=50)` | 前方の対象物との距離を指定時間保つ。 | 秒数と距離（cm）を指定。 |
| `move_forward(distance, units="cm", speed=0.5)` | 指定距離だけ前進する。 | 第2引数は時間ではなく単位。速度は m/s。 |
| `move_backward(distance, units="cm", speed=0.5)` | 指定距離だけ後退する。 | 引数は前進と共通。 |
| `move_left(distance, units="cm", speed=0.5)` | 指定距離だけ左へ動く。 | 同上。 |
| `move_right(distance, units="cm", speed=0.5)` | 指定距離だけ右へ動く。 | 同上。 |
| `move_upward(distance, units="cm", speed=0.5)` | 指定距離だけ上昇する。 | 同上。 |
| `move_downward(distance, units="cm", speed=0.5)` | 指定距離だけ下降する。 | 同上。 |
| `move_distance(positionX, positionY, positionZ, velocity)` | 現在位置と機体の向きを基準に相対移動する。 | 距離は m、速度は m/s。Xの正＝前、Yの正＝左、Zの正＝上。複数軸を同時に指定できる。 |
| `send_absolute_position(positionX, positionY, positionZ, velocity, heading, rotationalVelocity)` | 最初の離陸地点を基準に絶対位置への移動指示を送る。 | XYZは m、速度は m/s、方位は度、旋回速度は度/秒。6引数。 |

`move_forward()` など6方向の関数では、単位に `"cm"`、`"m"`、`"ft"`、`"in"` を指定でき、最大速度は2 m/sです。位置を使う移動は、明るく模様のある床面で精度が出やすく、高度1.5 mを超えると下方センサーの精度が低下する場合があります。

例えば `move_distance(0.5, 0, 0, 0.5)` は「今いる場所から前へ0.5 m」です。`send_absolute_position(0.5, 0, 1, 0.5, 0, 0)` は「離陸地点基準の座標 (0.5, 0, 1) m へ」という指定です。同じ相対移動を繰り返すと目的地が変わり、同じ絶対位置を指定すると目的地は変わりません。

## 3. 旋回・特殊飛行

| 関数 | 動作・用途 | 注意事項 |
| --- | --- | --- |
| `turn(power=50, seconds=None)` | パワーと時間で旋回する。 | 正＝左、負＝右。例：`turn(-30, 1)`。 |
| `turn_degree(degree=90, timeout=3, p_value=10)` | 離陸直後の初期方位を基準に指定角度へ向く。 | 最短方向へ旋回する。450°は90°相当で、1回転以上回る指定ではない。 |
| `turn_left(degree=90)` | 現在の向きから左旋回する。 | 角度は0～360°。 |
| `turn_right(degree=90)` | 現在の向きから右旋回する。 | 角度は0～360°。 |
| `circle(speed=75, direction=1)` | 円軌道を飛行する。 | `direction` は1＝右、-1＝左。 |
| `flip(direction="back")` | 指定方向に機体を反転させる。 | `"front"`、`"back"`、`"left"`、`"right"`。バッテリー残量50％未満では実行されない。 |
| `spiral(speed=50, seconds=5, direction=1)` | 下降する螺旋状の軌道で飛行する。 | 高度が下がる動作。 |
| `square(speed=60, seconds=1, direction=1)` | 四角形の軌道で飛行する。 | 引数はパワー・時間・方向。 |
| `sway(speed=30, seconds=2, direction=1)` | 機体を揺らしながら飛行する。 | 同上。 |
| `triangle(speed=60, seconds=1, direction=1)` | 三角形の軌道で飛行する。 | 同上。 |

## 4. 飛行変数の設定とトリム

### 4.1 飛行変数

| 関数 | 動作・用途 | 値の意味・注意事項 |
| --- | --- | --- |
| `get_move_values()` | 現在のロール・ピッチ・ヨー・スロットルの値を取得する。 | — |
| `set_pitch(power)` | ピッチ値を設定する。 | -100～100。正：前進、負：後退。 |
| `set_roll(power)` | ロール値を設定する。 | -100～100。正：右移動、負：左移動。 |
| `set_throttle(値)` | スロットル値を設定する。 | 範囲：-100～100。正：上昇、負：下降。値は保持される。 |
| `set_yaw(power)` | ヨー値を設定する。 | -100～100。正：左旋回、負：右旋回。 |
| `move(duration=None)` | 設定済みの飛行変数を送信する。 | 秒数指定時はその間送信を続ける。省略時は1回送信して戻る。事前に離陸する。 |
| `reset_move_values()` | ロール・ピッチ・ヨー・スロットルをすべて0に戻す。 | 意図しない次の動作を防ぐために使用する。 |

`set_pitch()`・`set_roll()`・`set_throttle()`・`set_yaw()` は値を設定するだけで、実際の飛行には `move()` の呼び出しが必要です。設定値は変更・リセットされるまで保持されるため、不要になった値は0に戻してください。`get_move_values()` の戻り値は `[roll, pitch, yaw, throttle]` です。

```python
# 接続・離陸後に実行する操作部分
drone.reset_move_values()
drone.set_pitch(30)
drone.set_roll(20)
drone.move(1)  # 前進と右移動を同時に1秒間行う
drone.reset_move_values()
drone.hover(1)
```

### 4.2 トリム・ジャイロのリセット

| 関数 | 動作・用途 | 引数・補足 |
| --- | --- | --- |
| `get_trim()` | 現在のトリム値を取得する。 | — |
| `set_trim(roll, pitch)` | ロール・ピッチのトリム値を設定する。 | 値の範囲：-100～100。 |
| `reset_trim()` | ロール・ピッチのトリムをリセットする。 | — |
| `reset_gyro()` | ロール・ピッチ・ヨーの角度を0にリセットする。 | 旧関数名：`reset_sensor()`。 |

トリムは意図しない横流れを補正する設定です。電源を切っても保存されます。離陸直前に `set_trim()` を呼ぶ場合は、続けて `time.sleep(1)` を入れてから離陸します。

## 5. 距離・高度・位置・速度センサー

| 関数 | 取得する情報・動作 | 補足 |
| --- | --- | --- |
| `detect_wall(distance=50)` | 前方の距離が閾値未満なら `True`、それ以外なら `False`。 | 閾値は cm。下方センサーではない。 |
| `get_bottom_range()` | 機体下部から地面までの距離を取得する。 | 単位：cm。着陸時は0。着陸時は下方距離センサーがオフ、カラーセンサーがオンになる。 |
| `get_front_range()` | 機体前方の距離センサーの測定値を取得する。 | 単位：cm。光の散乱・干渉により、センサーを覆っても最小約0.9 cmとなることがある。 |
| `get_height()` | 現在の高度（地面との距離）を取得する。 | 単位：cm。着陸中は0として扱える。 |
| `get_pos_x(unit="cm")` | X軸の位置（前後）を取得する。 | 既定の単位は cm。 |
| `get_pos_y()` | Y軸の位置（左右）を取得する。 | 同上。 |
| `get_pos_z()` | Z軸の位置（上下）を取得する。 | 同上。 |
| `get_position_data()` | `[経過秒数, x, y, z]` をリストで取得する。 | 個別取得と異なり、XYZの単位は m。 |
| `get_flow_velocity_x()` | 光学フローセンサーで測定したX軸方向（前後）の速度に対応する生データを取得する。 | 生データの単位・換算方法は元資料に記載なし。 |
| `get_flow_velocity_y()` | 光学フローセンサーで測定したY軸方向（左右）の速度に対応する生データを取得する。 | 生データの単位・換算方法は元資料に記載なし。 |

距離センサー・高度・個別の位置取得では `unit="cm"` が既定です。`"m"`、`"mm"`、`"in"` も選べます。下方距離は着地中に0となりますが、公式資料にはエラーでも0や-100、範囲外・タイムアウト時には999.9となる旨が記載されています。距離の値だけで着陸成功を判定しないでください。

## 6. 加速度・角度・角速度センサー

| 関数 | 取得する情報 | 単位・補足 |
| --- | --- | --- |
| `get_accel_x()` | X軸方向の加速度 | 元資料に単位の記載なし。 |
| `get_accel_y()` | Y軸方向の加速度 | 同上。 |
| `get_accel_z()` | Z軸方向の加速度 | 同上。 |
| `get_angle_x()` | X軸の角度（ロール角） | 離陸時またはバッテリー再挿入時に0へリセット。 |
| `get_angle_y()` | Y軸の角度（ピッチ角） | 同上。 |
| `get_angle_z()` | Z軸の角度（ヨー角） | 同上。 |
| `get_angular_speed_x()` | X軸（ロール軸）周りの角速度 | °/秒。 |
| `get_angular_speed_y()` | Y軸（ピッチ軸）周りの角速度 | °/秒。 |
| `get_angular_speed_z()` | Z軸（ヨー軸）周りの角速度 | °/秒。 |

## 7. 機体状態・エラー・LED

| 関数 | 動作・用途 | 補足 |
| --- | --- | --- |
| `get_battery()` | バッテリー残量を取得する。 | 戻り値：％。 |
| `get_flight_state()` | 現在の飛行状態を取得する。 | — |
| `get_movement_state()` | 飛行可能か、ホバリング中かなどの移動状態を取得する。 | — |
| `get_sensor_data()` | 高度・姿勢・位置・距離・状態のデータをまとめて取得する。 | 実装では5種類を順番に要求して結合する。同一時刻の測定値とは限らない。 |
| `get_error_data()` | 機体がエラー状態かを確認し、該当する英語名のエラーをコンソールに表示する。 | エラー名の一覧は下記参照。 |
| `drone_LED_off()` | 機体のLEDを消灯する。 | — |

### `get_error_data()` で表示される主なエラー

| 分類 | エラー名 | 意味・補足 |
| --- | --- | --- |
| Motion | `Motion_Calibrating` / `Motion_NoAnswer` / `Motion_WrongValue` / `Motion_NotCalibrated` | モーションセンサーの較正中・応答なし・値異常・未較正。 |
| Pressure | `Pressure_NoAnswer` / `Pressure_WrongValue` | 気圧センサーの応答なし・値異常。 |
| RangeGround | `RangeGround_NoAnswer` / `RangeGround_WrongValue` | 下方距離センサーの応答なし・値異常。 |
| Flow | `Flow_NoAnswer` / `Flow_CannotRecognizeGroundImage` | 光学フローセンサーの応答なし・地面画像の認識不可。 |
| デバイス | `NotRegistered` | デバイス未登録。 |
| 書き込み保護 | `FlashReadLock_UnLocked` / `BootloaderWriteLock_UnLocked` | 対応するロックが解除されている。 |
| 電源 | `LowBattery` | バッテリー残量低下。 |
| 離陸 | `TakeoffFailure_CheckPropellerAndMotor` | 離陸失敗。プロペラ・モーターの確認が必要。 |
| 振動 | `CheckPropellerVibration` | プロペラの振動に関する異常。 |
| 姿勢 | `Attitude_NotStable` | 機体姿勢が不安定。 |
| 反転 | `CanNotFlip_LowBattery` / `CanNotFlip_TooHeavy` | バッテリー不足・重量超過によって反転できない。 |

## 8. LED・音

| 関数 | 用途 |
| --- | --- |
| `set_drone_LED(r, g, b, brightness)` / `set_controller_LED(r, g, b, brightness)` | 機体／コントローラーの色と明るさを設定する。RGBは0～255、明るさは0～100。 |
| `set_drone_LED_mode(r, g, b, mode, speed)` / `set_controller_LED_mode(r, g, b, mode, speed)` | 点滅などのパターンを設定する。モードの一覧は公式資料を参照。 |
| `drone_LED_off()` / `controller_LED_off()` | 対象のLEDを消灯する。 |
| `drone_buzzer(note, duration)` / `controller_buzzer(note, duration)` | 音を鳴らす。`note` は周波数または音符、`duration` はミリ秒。 |
| `start_drone_buzzer(note)` / `start_controller_buzzer(note)` | 音を鳴らし始める。 |
| `stop_drone_buzzer()` / `stop_controller_buzzer()` | 音を止める。 |
| `drone_buzzer_sequence(kind)` / `controller_buzzer_sequence(kind)` | 用意された音のパターンを鳴らす。 |
| `ping()` | 音とLEDで機体を識別する。 |

飛行の時間は秒ですが、`*_buzzer()` の発音時間はミリ秒です。例えば `drone.drone_buzzer(440, 500)` は440 Hzを0.5秒鳴らします。

## 9. 気圧・色・コントローラー・画面

| 分類 | 主な関数 | 用途・使い方 |
| --- | --- | --- |
| 気圧・温度 | `get_pressure()`、`get_elevation()`、`get_drone_temperature()` | 気圧・標高・温度を取得する。地面からの高さを知りたい場合は `get_height()` を使う。 |
| 気圧による高度 | `set_initial_pressure()`、`height_from_pressure()` | 基準気圧を設定し、気圧から高度を求める。 |
| 色の取得 | `get_colors()`、`get_front_color()`、`get_back_color()`、`get_color_data()` | 前後のカラーセンサーの色名やデータを取得する。 |
| 色の学習・分類 | `new_color_data()`、`append_color_data()`、`load_color_data()`、`predict_colors()` | 学習データを用意し、色を分類する。詳細な引数と手順は公式資料を参照。 |
| ボタン | `get_button_data()`、`up_arrow_pressed()`、`l1_pressed()` など | ボタンの状態を取得する。個別の `*_pressed()` で押下を判定できる。 |
| スティック | `get_joystick_data()`、`get_left_joystick_x()` など | 左右のスティックのX・Y入力を取得する。 |
| 画面 | `controller_create_canvas()`、`controller_draw_string()`、`controller_draw_canvas()` など | キャンバスを作成し、文字や図形を描いてから画面へ送信する。 |

画面関連の機能には、JROTC版や Python for Robolink では使えないものがあります。対応状況は[公式資料の Screen 節](https://docs.robolink.com/docs/CoDroneEDU/Python/Drone-Function-Documentation/#screen)を確認してください。

## 10. 資料と実装の差・未確認事項

- **接続ポートの引数：** 公式の例には `port_name` とありますが、ローカル実装の引数名は `portname` です。このガイドでは `pair("COM3")` のように位置引数を使います。
- **距離移動の既定速度：** 公式資料は1.0 m/s、ローカルの2.10実装は0.5 m/sです。このガイドの表はローカル実装に合わせています。キーワード引数は `unit` ではなく `units` です。
- **`move()` の時間省略：** 公式資料の「無期限」は呼び出しが待ち続ける意味ではありません。ローカル実装は1回送信して戻ります。次の停止指示までの実機の挙動は未確認です。
- **位置データの構造：** `get_position_data()` はローカル実装では時刻を含む4要素です。Xは `[1]`、Yは `[2]`、Zは `[3]` で取り出します。
- **戻り値の記述：** 公式の Returns 欄には、説明や例で値を返す関数にも `None` とある箇所があります。`detect_wall()` や `get_move_values()` はローカル実装の戻り値を記載しました。
- **センサーの単位：** 加速度と光学フロー速度は、物理単位や換算の説明が十分でないため、このガイドでは推測で確定していません。
- **古い関数名：** `get_flow_x/y()`、`get_x/y/z_accel()`、`get_x/y/z_angle()`、`reset_sensor()`、`print_move_values()`、`reset_move()` などは旧名です。新規コードでは表に掲載した名前を使ってください。
- **検証範囲：** 公式資料とローカルソースの照合のみです。通信・飛行・センサー精度・機種別の動作は未確認です。


import time
from codrone_edu.drone import Drone
import configparser

def move_test(drone: Drone):
    try:
        poll_down = -0.55  # カードドロップの時に下げる値
        move_card = 0.8 # !!!!////

        drone.set_controller_LED(0, 0, 255, 100)
        drone.set_drone_LED(0, 0, 255, 100)

        drone.move_distance(0, 0, 0.15, 1)
        drone.hover(2)
        # 開始地点：中央ラインより縦0.3m, 横1.5m地点を中心とする

        # ドロップ
        drone.move_distance(1.8, 0, 0, 0.75)  # ...distance(前後/m, 左右/m, 上下/m, 距離m/s)
        drone.hover(0.5)
        drone.move_distance(0, -0.3, 0, 0.75)

        # z：35cm

        # 半円超してボール初期位置
        drone.move_distance(0.3, -0.5, -0.1, 0.8)  # ...distance(前後/m, 左右/m, 上下/m, 距離m/s)
        drone.hover(0.5)

        # z：25cm

        # ボール移動一回目
        drone.move_distance(0.1, 0, 0, 1)
        drone.hover(0.5)
        drone.move_distance(0, 0, -0.5, 0.5)
        drone.hover(3)

        # z：80cm
        drone.move_distance(0, 0, 0.35, 1)
        drone.hover(0.5)
        drone.move_distance(1.4, 0, 0, 1)
        drone.hover(1)
        drone.move_distance(0.3, 0,0.2,1)
        drone.hover(0.5)

        # ドロップ
        drone.move_distance(0, move_card, 0, 1)
        drone.hover(0.5)

        drone.move_distance(0, 0, poll_down, 1)
        drone.hover(3)

        # z：35cm
        drone.move_distance(0, -(move_card + 0.05), 0, 1)
        drone.hover(0.5)

        drone.move_distance(0, 0, -0.1, 1)
        drone.hover(0.5)

        drone.move_distance(0, 0, 0.55, 1)
        # z：25cm

        # ボール移動二回目
        drone.move_distance(1.5, 0, 0, 1)
        drone.hover(1)

        # 円手前に移動
        drone.move_distance(0, 0, 1.28, 1)
        drone.hover(0.5)

        drone.move_distance(-1.722, 0, 0, 1)
        drone.hover(0.5)

        drone.move_distance(0, 1.95, 0, 1)
        drone.hover(0.5)


        # 円貫通
        drone.move_distance(1.285, 0, 0, 1)
        drone.hover(0.5)

        # ランディングポイント上空
        drone.move_distance(0, -0.415, 0, 1)
        drone.hover(1)

    except KeyboardInterrupt:
        print("動作が中断されました")
        return


drone = Drone()

# config.iniファイルのトリム値を代入
config_file = 'config.ini'
config = configparser.ConfigParser()  # オブジェクトの生成
config.read(config_file)  # config.iniファイルの全体読み込み
try:
    roll_trim = int(config['TRIM']['roll_trim'])  # roll_trimの読み込み
    pitch_trim = int(config['TRIM']['pitch_trim'])  # pitch_trimの読み込み
except (KeyError, ValueError):  # 読み込めなかった場合0 0を返す
    roll_trim = 0
    pitch_trim = 0

try:
    # ドローンとPCを接続する
    drone.pair()
    # トリム値を設定
    drone.set_trim(roll_trim, pitch_trim)  # トリム値を設定
    time.sleep(1)
    # 離陸する
    drone.takeoff()
    # 実行する関数
    move_test(drone)
except TimeoutError:
    print("ドローンとの接続が失敗しました")
finally:
    print("プログラムを終了します")
    drone.land()
    drone.close()
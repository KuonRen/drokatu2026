import time
from codrone_edu.drone import Drone

def move_test():
    drone = Drone()
    # ドローンとPCを接続する
    drone.pair()
    # トリム値を設定
    drone.set_trim(-38, 34)  # トリム値を設定
    time.sleep(1)
    # 離陸する
    drone.takeoff()
    poll_down = -0.55  # カードドロップの時に下げる値
    move_card = 0.8 # !!!!////
    drone.set_controller_LED(255, 0, 0, 100)
    drone.set_drone_LED(255, 0, 0, 100)
    drone.move_distance(0, 0, 0.15, 1)
    drone.hover(1)
    # 開始地点：中央ラインより縦0.3m, 横1.5m地点を中心とする

    # ドロップ
    drone.move_distance(1.8, 0, 0, 0.75)  # ...distance(前後/m, 左右/m, 上下/m, 距離m/s)
    drone.hover(0.5)
    drone.move_distance(0, 0.3, 0, 0.75)
    drone.hover(0.5)
    # z：35cm

    # 半円超してボール初期位置
    drone.move_distance(0.3, 0.5, -0.1, 0.8)  # ...distance(前後/m, 左右/m, 上下/m, 距離m/s)
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
    drone.move_distance(0, -move_card, 0, 1)
    drone.hover(0.5)

    drone.move_distance(0, 0, poll_down, 1)
    drone.hover(3)

    # z：35cm
    drone.move_distance(0, (move_card + 0.05), 0, 1)
    drone.hover(0.5)

    drone.move_distance(0, 0, -0.1, 1)
    drone.hover(0.5)

    drone.move_distance(0, 0, 0.55, 1)
    drone.hover(1)
    # z：25cm

    # ボール移動二回目
    drone.move_distance(1.5, 0, 0, 1)
    drone.hover(1)

    # 円手前に移動
    drone.move_distance(0, 0, 1.28, 1)
    drone.hover(0.5)

    drone.move_distance(-1.722, 0, 0, 1)
    drone.hover(0.5)

    drone.move_distance(0, -1.95, 0, 1)
    drone.hover(0.5)


    # 円貫通
    drone.move_distance(1.285, 0, 0, 1)
    drone.hover(0.5)

    # ランディングポイント上空
    drone.move_distance(0, 0.415, 0, 1)
    drone.hover(1)

    drone.land()
    drone.close()

# 実行する関数
move_test()
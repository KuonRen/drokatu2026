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
    print("スーパー宮本せいじ号発進！！！")
    # poll_down = -0.55  # カードドロップの時に下げる値
    # move_card = 0.8
    drone.set_controller_LED(255, 0, 0, 100)
    drone.set_drone_LED(255, 0, 0, 100)
    drone.hover(1)

    # 実際に飛行するコード

    # Ⅰ．ドリブルチャレンジ（10 / 20 / 40）
    drone.move_distance(0.7, -0.1, 0, 1)        # 前へ70cm、右へ10cm（↕70～80cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, 0, -0.4, 1)          # 40cm下降（↕30cm）
    drone.hover(2)                              # 1sホバリング
    drone.move_distance(0.7, 0, 0, 1)           # 前に70cm（↕30cm）
    drone.hover(1)                              # 1sホバリング

# 実行する関数
move_test()
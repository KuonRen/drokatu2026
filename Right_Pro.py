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
    drone.takeoff()                             # 離陸（↕70～80cm）
    print("スーパー宮本せいじ号発進！！！")
    # poll_down = -0.55  # カードドロップの時に下げる値
    # move_card = 0.8
    drone.set_controller_LED(255, 0, 0, 100)    # コントローラーLED：赤
    drone.set_drone_LED(255, 0, 0, 100)         # ドローンLED：赤
    drone.hover(1)

    # 実際に飛行するコード

    # Ⅰ．ドリブルチャレンジ（点数配分：10 / 20 / 40）
    drone.move_distance(0.7, -0.1, 0, 1)        # 開始ポジション：前へ70cm、右へ10cm（↕70～80cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, 0, -0.4, 1)          # 風の当たる高さへ：40cm下降（↕30cm）
    drone.hover(2)                              # 1sホバリング
    drone.move_distance(0.7, 0, 0, 1)           # 第一回前進：前に70cm（↕30cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0.7, 0.1, 0, 1)         # 第二回前進：前に70cm、左へ10cm（↕30cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, -0.9, 0, 1)          # 右に押し込む：右に90cm（↕30cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, -0.1, 0, 1)          # 左に動かすために右へ：右に10cm（↕30cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, 0.4, 0, 1)           # 左上へ押し込む：左に40cm（↕30cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, 0, 0.3, 1)           # 上へ上げる：上30cm（↕60cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0, 1, 0, 1)             # 左へ移動：左に100cm（↕60cm）
    drone.hover(1)                              # 1sホバリング

    # Ⅱ．半円通過
    drone.move_distance(2.5, 0, 0, 1)           # 半円通過：前に110cm（↕60cm）
    drone.hover(1)                              # 1sホバリング

    # Ⅲ．ブラインド～ゴール
    drone.move_distance(0, 1.4, 0, 1)           # 上へ上昇：上に140cm（↕200cm）
    drone.hover(1)                              # 1sホバリング
    drone.move_distance(0., 1.4, 0, 1)           # 上へ上昇：上に140cm（↕200cm）
    drone.hover(1)

# 実行する関数
move_test()
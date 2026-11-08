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
    drone.set_controller_LED(0, 0, 255, 100)
    drone.set_drone_LED(0, 0, 255, 100)
    drone.hover(1)
    # 開始地点：中央ラインより縦0.3m, 横1.5m地点を中心とする

    # L字-1
    # 開始ポジション
    drone.move_distance(0.5, 0, 0, 0.75)  # ...distance(前後/m, 左右/m, 上下/m, 距離m/s)
    drone.hover(0.5)
    # 少し下がってボールに風あてる
    drone.move_distance(0, 0, -0.4, 0.5)
    drone.hover(4)
    # ドロップコイン横までせいじ君が進む
    drone.move_distance(0.55, 0, 0, 1)
    drone.hover(2)

    # ドロップコイン
    drone.move_distance(0, 0, 0.3, 1)
    drone.hover(1)
    drone.move_distance(0, 1, 0, 1)
    drone.hover(2)
    # せいじ君がL字に帰宅
    drone.move_distance(0, -1, 0, 1)
    drone.hover(3)
    drone.move_distance(0, 0, -0.3, 1)
    drone.hover(2)

    # L字の角まで進む
    drone.move_distance(0.77, 0, 0, 1)
    drone.hover(1)
    # 右にあるであろうボールに風を当てるため
    drone.move_distance(0, -0.1, 0, 1)
    drone.hover(1)
    # L字横移動
    drone.move_distance(0, 0.962, 0, 0.7)
    drone.hover(1)
    # 最後の穴入れチャレンジ
    drone.move_distance(0, -0.25, 0, 1)
    drone.hover(1)
    drone.move_distance(0.1, 0, 0, 1)
    drone.hover(1)
    # 押し込み & 縦位置戻し
    drone.move_distance(-0.1, 0, 0, 1)
    drone.hover(1)

    # マット初期位置650 高さは後日設定
    drone.move_distance(0, -0.4, 0, 1)
    drone.hover(1)
    drone.move_distance(2.516, 0, 0, 1)
    drone.hover(1)
    drone.move_distance(0, 0.75, 0, 1)
    drone.hover(1)

    # ボーナスタワー落とし
    drone.move_distance(0, 0.4, 0, 1)
    drone.hover(1)
    drone.move_distance(0.4, 0, 0, 1)
    drone.hover(1)
    drone.move_distance(0, -0.4, 0, 1)
    drone.hover(1)

    # ブラインド
    drone.move_distance(0, -1.8, 0, 1)
    drone.hover(1)

    drone.move_distance(0.95, 0, 0, 1)
    drone.hover(1)
    # ランディング
    drone.land()
    drone.close()

# 実行する関数
move_test()
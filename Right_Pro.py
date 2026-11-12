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

    # Ⅰ．ドリブルチャレンジ
    # スタート中心は200＋250÷2。縦レーン入口1000mmの150mm手前へ。
    print("[Ⅰ-01] ボールの後方へ：前525mm", flush=True)
    drone.move_distance((850 - 325) / 1000, 0, 0, 0.6)
    print("[Ⅰ-02] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 離陸750mmは既存値の中間。風を当てる高さ350mmは練習で調整。
    print("[Ⅰ-03] ドリブル高度へ：下400mm", flush=True)
    drone.move_distance(0, 0, (350 - 750) / 1000, 0.4)
    print("[Ⅰ-04] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 0点区画の奥端は入口1000＋300。縦レーン中心は右900＋200÷2。
    print("[Ⅰ-05] 初期区画の境界へ：前450mm", flush=True)
    drone.move_distance((1000 + 300 - 850) / 1000, 0, 0, 0.4)
    print("[Ⅰ-06] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 横レーンの中心は奥行1000＋1524＋200÷2＝2624mm。
    print("[Ⅰ-07] 横レーンの中心へ：前1324mm", flush=True)
    drone.move_distance((1524 + 200 / 2 - 300) / 1000, 0, 0, 0.4)
    print("[Ⅰ-08] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 奥の区画の中心は右900＋200＋475÷2＝1337.5mm。
    print("[Ⅰ-09] 40点区画の入口に合わせる：右337.5mm", flush=True)
    drone.move_distance(0, -(200 / 2 + 475 / 2) / 1000, 0, 0.4)
    print("[Ⅰ-10] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 奥の区画の中心は奥行2624＋200÷2＋380÷2＝2914mm。
    print("[Ⅰ-11] 40点区画の中心へ：前290mm", flush=True)
    drone.move_distance((200 / 2 + 380 / 2) / 1000, 0, 0, 0.4)
    print("[Ⅰ-12] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 通過高度650mmは右600mmのラインで実測確認する。
    print("[Ⅰ-13] ゲート通過高度へ：上300mm", flush=True)
    drone.move_distance(0, 0, (650 - 350) / 1000, 0.5)
    print("[Ⅰ-14] ホバリング：1秒", flush=True)
    drone.hover(1)

    # Right側の通過ラインは中央線から右600mmを練習目標とする。
    print("[Ⅰ-15] 半円ゲートの通過ラインへ：左737.5mm", flush=True)
    drone.move_distance(0, (1337.5 - 600) / 1000, 0, 0.6)
    print("[Ⅰ-16] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[DIAG Ⅰ→Ⅱ] 機体のエラー状態を照会", flush=True)
    print("[DIAG Ⅰ→Ⅱ] SDK応答:", repr(drone.get_error_data()), flush=True)

    # Ⅱ．半円通過
    # 奥行4000mmのゲート面から300mm先まで進んでから上昇する。
    print("[Ⅱ-01] ゲート通過：前1386mm", flush=True)
    drone.move_distance((4000 + 300 - 2914) / 1000, 0, 0, 0.5)
    print("[Ⅱ-02] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[DIAG Ⅱ→Ⅲ] 機体のエラー状態を照会", flush=True)
    print("[DIAG Ⅱ→Ⅲ] SDK応答:", repr(drone.get_error_data()), flush=True)

    # Ⅲ．ブラインド～ゴール
    # 暗幕上端1650mmに対して400mm上の高度を目標にする。
    print("[Ⅲ-01] 暗幕を越える高さへ：上1400mm", flush=True)
    drone.move_distance(0, 0, (1650 + 400 - 650) / 1000, 0.5)
    print("[Ⅲ-02] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 箱の中心は奥行7350mm、中央線から右550mm。
    print("[Ⅲ-03] 箱の中心へ：前3050mm、左50mm", flush=True)
    drone.move_distance((8000 - 500 - 300 / 2 - 4300) / 1000,
                        (600 - (400 + 300 / 2)) / 1000, 0, 0.7)
    print("[Ⅲ-04] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 箱の上面300mmの上で位置を安定させ、着陸指令を出す。
    print("[Ⅲ-05] 箱の上面350mm上まで下降：下1400mm", flush=True)
    drone.move_distance(0, 0, (300 + 350 - 2050) / 1000, 0.4)
    print("[Ⅲ-06] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅲ-07] 着陸指令", flush=True)
    drone.land()
    print("[Ⅲ-08] 接続を閉じる", flush=True)
    drone.close()
    print("[END] 飛行プログラム終了", flush=True)


# 接続準備から着陸まで、例外が出た箇所をターミナルに残す。
try:
    print("[START] 接続準備・離陸処理を開始", flush=True)
    move_test()
except Exception:
    print("[ERROR] 処理中断。最後の操作ログと下の例外を確認してください。", flush=True)
    raise

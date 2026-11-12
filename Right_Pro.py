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
    print("[Ⅰ-01] ボール手前へ：前70cm、右10cm", flush=True)
    drone.move_distance(0.7, -0.1, 0, 1)
    print("[Ⅰ-02] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅰ-03] ドリブルの高さへ：下40cm", flush=True)
    drone.move_distance(0, 0, -0.4, 1)
    print("[Ⅰ-04] ホバリング：2秒", flush=True)
    drone.hover(2)

    print("[Ⅰ-05] 直線区間：前70cm", flush=True)
    drone.move_distance(0.7, 0, 0, 1)
    print("[Ⅰ-06] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅰ-07] 曲がり角へ：前70cm、左10cm", flush=True)
    drone.move_distance(0.7, 0.1, 0, 1)
    print("[Ⅰ-08] ホバリング：1秒", flush=True)
    drone.hover(1)

    # 横パイプの端は、右900mm＋パイプ長762mmと仮定。
    # 右1000mmから右1500mmまでを練習時の上限目標にする。
    print("[Ⅰ-09] ボールを横へ押す：右45cm", flush=True)
    drone.move_distance(0, -0.45, 0, 1)
    print("[Ⅰ-10] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅰ-11] 折り返し位置へ：右5cm", flush=True)
    drone.move_distance(0, -0.05, 0, 1)
    print("[Ⅰ-12] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅰ-13] ボールを押し戻す：左40cm", flush=True)
    drone.move_distance(0, 0.4, 0, 1)
    print("[Ⅰ-14] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅰ-15] ゲート通過の高さへ：上30cm", flush=True)
    drone.move_distance(0, 0, 0.3, 1)
    print("[Ⅰ-16] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅰ-17] ゲート通過ラインへ：左50cm", flush=True)
    drone.move_distance(0, 0.5, 0, 1)
    print("[Ⅰ-18] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[DIAG Ⅰ→Ⅱ] 機体のエラー状態を照会", flush=True)
    print("[DIAG Ⅰ→Ⅱ] SDK応答:", repr(drone.get_error_data()), flush=True)

    # Ⅱ．半円通過
    print("[Ⅱ-01] 半円ゲートを通過：前187.5cm", flush=True)
    drone.move_distance(1.875, 0, 0, 0.5)
    print("[Ⅱ-02] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[DIAG Ⅱ→Ⅲ] 機体のエラー状態を照会", flush=True)
    print("[DIAG Ⅱ→Ⅲ] SDK応答:", repr(drone.get_error_data()), flush=True)

    # Ⅲ．ブラインド～ゴール
    print("[Ⅲ-01] 暗幕を越える高さへ：上140cm", flush=True)
    drone.move_distance(0, 0, 1.4, 0.5)
    print("[Ⅲ-02] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅲ-03] ゾーンボックスの真上へ：前305cm、左5cm", flush=True)
    drone.move_distance(3.05, 0.05, 0, 0.7)
    print("[Ⅲ-04] ホバリング：1秒", flush=True)
    drone.hover(1)

    print("[Ⅲ-05] 着陸前の高さへ：下140cm", flush=True)
    drone.move_distance(0, 0, -1.4, 0.4)
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

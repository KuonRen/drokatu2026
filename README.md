# drokatu2026

CoDrone EDUをPythonで操作するチーム開発用プロジェクトです。
依存管理には [uv](https://docs.astral.sh/uv/) を使用します。

- `pyproject.toml`：プロジェクト情報と依存ライブラリ（`package.json` 相当）
- `uv.lock`：間接依存を含むバージョン固定（`package-lock.json` 相当）
- `.python-version`：使用するPythonのバージョン（3.14）
- `.venv`：各メンバーのローカルPython環境（Git管理対象外）

## 初期セットアップ（Windows / VSCode）

1. [Python公式サイト](https://www.python.org/downloads/windows/) からPythonをインストールします。
   インストール済みなら追加のインストールは不要です。
   VSCodeの新しいPowerShellターミナルで確認します。

   ```powershell
   py --version
   ```

2. uvをインストールします。

   ```powershell
   py -m pip install uv
   py -m uv --version
   ```

3. リポジトリを取得し、VSCodeの「フォルダーを開く」でプロジェクトフォルダーを開きます。
   「ターミナル → 新しいターミナル」を選び、`pyproject.toml` があるフォルダーで実行します。

   ```powershell
   py -m uv sync --locked
   ```

   Python 3.14の仮想環境 `.venv` が作成され、`uv.lock` のバージョンで依存ライブラリがインストールされます。
   必要なPythonが見つからない場合はuvがダウンロードします。初回はインターネット接続が必要です。

4. VSCodeにMicrosoftの **Python** と **Pylance** 拡張機能を入れます。
   F5で実行するため、Microsoftの **Python Debugger** 拡張機能も有効になっていることを確認します（通常はPython拡張機能と一緒にインストールされます）。
   `Ctrl+Shift+P` → `Python: Select Interpreter` で `.venv\Scripts\python.exe` を選びます。

5. 機体を動かさず、ライブラリのインポートを確認します。

   ```powershell
   .\.venv\Scripts\python.exe -c "from codrone_edu.drone import Drone; print('import OK')"
   ```

   `import OK` が表示されれば、Pythonとライブラリの準備は完了です。

## コードの実行

VSCodeでプロジェクトフォルダーを開き、初期セットアップで選択した
`.venv\Scripts\python.exe` を使用します。

### test.pyを実行する

1. コントローラーをデータ通信対応USBケーブルでPCにつなぎます。
2. ドローンとコントローラーの電源を入れ、ペアリングします。
3. 同じコントローラーを使用するブラウザーや別のプログラムの接続を終了します。
4. VSCodeで `test.py` を開き、保存します。
5. 飛行スペースを確保し、**F5** を押します。
   または、上部の **「実行」→「デバッグの開始」** を選びます。
   左側の **「実行とデバッグ」** タブから **「実行とデバッグ」** ボタンを押しても実行できます。
6. 初回に選択画面が表示されたら **「Python Debugger」→「Python File（Pythonファイル）」** を選びます。
   現在開いているPythonファイルを実行する構成を選択してください。

`test.py` は離陸 → 1秒ホバリング → 着陸 → 接続終了を行います。
各PCのUSB接続・ポート使用状況・権限によって接続できない場合は、下記を確認してください。
F5はデバッグ実行のため、ブレークポイントがあるとその行で処理が停止します。
飛行テスト前に不要なブレークポイントを解除してください。

### 別のファイルを実行する

実行したい `.py` ファイルをVSCodeで開き、保存してから **F5**、
または **「実行」→「デバッグの開始」** を選びます。
現在開いているPythonファイルを実行する構成を使用してください。

実行操作の詳細は [VSCode公式ドキュメント](https://code.visualstudio.com/docs/python/debugging) を参照してください。

## 事前の自動トリム調整（calibrate.py）

コース実行前に `calibrate.py` を単体で実行します。

```powershell
.\.venv\Scripts\python.exe calibrate.py
```

1. 保存済みのトリム値で「離陸 → 安定待ち → 約3秒測定 → 着陸」を10回行います。
2. 各飛行の位置データから前後・左右の流れを求め、各方向で最大・最小の1回ずつを除いた8回を平均します。
3. 明確な流れがある方向のトリムを最大2だけ変更します。
4. 補正後の同じ設定で10回飛行し、改善を確認できた場合だけ `config.ini` を更新します。

各飛行の前に、機体を同じ開始位置・向きへ戻してEnterを押します。
`q` で次の飛行を中止、飛行中は `Ctrl+C` で着陸を試みて中止します。
下降・離陸地点への復帰・コース走行は行いません。

測定は約0.1秒間隔を目標とし、更新された位置データを使用します。
位置の時間変化を回帰直線で集計し、光学フローの生データも併せて記録します。
無操作時の揺れも評価するため、位置変化から求めた速度のRMSを補正前後で比較します。
改善量が0.005m/sと飛行間のばらつきから求めた判定幅の両方を超え、補正した各方向も改善した場合に保存します。
この初版は実機で補正量を確定する前の小幅な1段階調整です。20回だけで最適値へ収束する保証はありません。
補正方向の判定は、流れが0.02m/sとばらつきから求めた判定幅の両方を超える場合に行います。
これらの閾値は初期値であり、実機ログで妥当性を確認してください。

`calibration_logs/日時/` に各飛行のCSVと `summary.json`（除外した回、補正前後の集計、採否・中断理由）を残します。
CSVには安定待ち区間も記録しますが、補正計算には含めません。
中断・悪化時は設定ファイルを更新せず、機体のトリムも元の値へ戻します。
測定中のセンサー更新停止・高度範囲外では、着陸を確認した後に失敗した回を再試行できます。
原因と飛行範囲を確認してEnterを押すと再試行、`q`で全体を中止します。完了した回は保持し、失敗した回は集計しません。
各回は初回を含め最大3回までとし、着陸確認失敗やその他のエラーでは全体を中止します。
再試行のCSVには`_retry1`、`_retry2`を付け、失敗した測定のログも残します。
センサー更新の停止、離陸地点から0.75mを超える水平ずれ、高度範囲外（0.3～1.5m）、測定中0.15mを超える高度変動などは中止条件です。
バッテリーは離陸前30%以上、測定中20%以上を必要とします。
`takeoff()` 内部の待機中はこのプログラム側の監視が動かないため、離陸直後も目視で確認してください。

関数の用途は [Robolink公式の2.10ドキュメント](https://docs.robolink.com/docs/CoDroneEDU/Python/Drone-Function-Documentation/) を参照しています。
更新時刻・飛行状態の確認には、導入済み2.10の `get_flow_data()`・`get_range_data()`・`get_state_data()` の実装も参照しています。

## 実行できない場合

- `py` が見つからない：Pythonをインストールし、VSCodeとターミナルを開き直します。
- `No module named uv`：`py -m pip install uv` を実行します。
- `.venv\Scripts\python.exe` が見つからない：現在のフォルダーを確認し、`py -m uv sync --locked` を実行します。
- `No module named codrone_edu`：`py -m uv sync --locked` を実行し、`Python: Select Interpreter` で `.venv\Scripts\python.exe` を選び直します。
- F5でPythonを実行できない：PythonとPython Debugger拡張機能が有効か確認し、対象の `.py` ファイルを開いて実行します。
- コントローラーが検出されない：USBケーブルがデータ通信対応か、電源と接続状態を確認します。
- `Could not connect to CoDrone EDU controller` / アクセス拒否：ブラウザーなどが同じポートを使用していないか確認し、USBを接続し直します。組織のPCではUSB・シリアル通信の制限も管理者に確認してください。

接続エラーはライブラリ側で終了コード0になる場合があります。
終了コードだけでなく、`Connected to CoDrone EDU.` の表示と、その後のエラーの有無を確認してください。

## 依存ライブラリの変更

チームで変更するライブラリとバージョンを決めてから更新します。

```powershell
py -m uv add ライブラリ名
```

CoDrone EDUのバージョン変更は `py -m uv add "codrone-edu==新しいバージョン"` で行います。
`pyproject.toml` と `uv.lock` はセットでGit管理し、`uv.lock` は手で編集しません。
変更を受け取ったメンバーは `py -m uv sync --locked` を再実行します。

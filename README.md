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

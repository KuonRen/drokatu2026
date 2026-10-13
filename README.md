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
   `Ctrl+Shift+P` → `Python: Select Interpreter` で `.venv\Scripts\python.exe` を選びます。
   以下の直接実行コマンドは、この選択にかかわらず `.venv` のPythonを使用します。

5. 機体を動かさず、ライブラリのインポートを確認します。

   ```powershell
   .\.venv\Scripts\python.exe -c "from codrone_edu.drone import Drone; print('import OK')"
   ```

   `import OK` が表示されれば、Pythonとライブラリの準備は完了です。

## コードの実行

すべてのコマンドは、`pyproject.toml` があるプロジェクトフォルダーで実行します。
仮想環境の有効化やPowerShellスクリプトの読み込みは不要です。

### test.pyを実行する

1. コントローラーをデータ通信対応USBケーブルでPCにつなぎます。
2. ドローンとコントローラーの電源を入れ、ペアリングします。
3. 同じコントローラーを使用するブラウザーや別のプログラムの接続を終了します。
4. 飛行スペースを確保し、次を実行します。

   ```powershell
   .\.venv\Scripts\python.exe .\test.py
   ```

`test.py` は離陸 → 1秒ホバリング → 着陸 → 接続終了を行います。
このコマンドは開発時にCOM6のCoDrone EDUへ接続し、正常終了した方法です。
各PCのUSB接続・ポート使用状況・権限によって接続できない場合は、下記を確認してください。

### 別のファイルを指定する

次のパスを、実行したいPythonファイルのパスに置き換えます。

```powershell
.\.venv\Scripts\python.exe "実行するファイルのパス.py"
```

相対パスは現在のターミナルのフォルダーを基準にします。絶対パスも指定できます。
スペースを含むパスはダブルクォートで囲みます。
ファイルに渡す引数は、ファイルパスの後に続けて指定できます。

## 実行できない場合

- `py` が見つからない：Pythonをインストールし、VSCodeとターミナルを開き直します。
- `No module named uv`：`py -m pip install uv` を実行します。
- `.venv\Scripts\python.exe` が見つからない：現在のフォルダーを確認し、`py -m uv sync --locked` を実行します。
- `No module named codrone_edu`：`py -m uv sync --locked` を実行し、上記の `.venv` のPythonでインポートを再確認します。
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

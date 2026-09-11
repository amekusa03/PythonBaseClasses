# Python GUI File Manager Base & Application

<p align="center">
  <a href="#english">English</a> | <a href="#japanese">日本語</a>
</p>

---

<a name="english"></a>
## English

A clean set of **data model and repository pattern base classes** along with a **rich desktop GUI sample application** built with Python and PySide6.

### 🌟 Features

- **Object-Oriented Data Model**: Polymorphic node objects (`BaseNodeObject`, `FileNodeObject`, `DirectoryNodeObject`) encapsulating icons, localized file type labels, sizes, and timestamp metadata.
- **Repository Pattern**: Decoupled filesystem operations (`FilerRepository`) keeping GUI logic separate from OS-level operations.
- **Modern Desktop GUI**: Sleek Tokyo Night dark-themed UI built with PySide6.
- **Bilingual Support (EN / JA)**: Dynamic language switching without restarting the application.
- **Rich Navigation**: Back/Forward history, parent directory navigation, path entry, search filter, and quick shortcuts.
- **File Management**: Create files/folders, rename, delete, and open items via context menu or details panel.

### 📂 Project Structure

```
PythonBaseClasses/
├── BaseNodeObject.py   # Data models (Node information, icon, type, metadata)
├── FilerRepository.py  # Repository (Filesystem CRUD operations wrapper)
├── i18n.py             # Localization module (English & Japanese support)
├── main.py             # Desktop GUI Application (PySide6 / Tokyo Night theme)
└── README.md           # Documentation
```

### 🛠️ Architecture & Components

1. **Data Model Layer (`BaseNodeObject.py`)**
   - Encapsulates file and directory attributes into object instances.
   - `BaseNodeObject`: Base class with path, name, selection state (`updated` Signal), timestamps, and status checks.
   - `FileNodeObject`: File representation with extension icons, formatted size, and type names.
   - `DirectoryNodeObject`: Directory representation holding child node lists.

2. **Data Access & Operation Layer (`FilerRepository.py`)**
   - Encapsulates filesystem read/write operations without direct OS module coupling from the GUI layer.
   - Methods: `get_directory_node()`, `create_directory()`, `create_file()`, `rename_node()`, `delete_node()`.

3. **Internationalization Layer (`i18n.py`)**
   - Manages language state (`en` / `ja`) and translation lookup.
   - Provides observer callbacks to update UI components seamlessly upon language change.

4. **UI & Presentation Layer (`main.py`)**
   - Built with PySide6 desktop widgets.
   - Features navigation controls, breadcrumb path bar, quick filter, table view with numeric/time sorting, sidebar shortcuts, details metadata panel, context menu, and a language toggle button.

### 🚀 Setup & Execution

#### Requirements
- Python 3.12+
- PySide6

#### Instructions

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   ```

2. **Install dependencies**
   ```bash
   ./venv/bin/pip install PySide6
   ```

3. **Run application**
   ```bash
   ./venv/bin/python main.py
   ```

---

<a name="japanese"></a>
## 日本語

Python (PySide6) でファイルやディレクトリを操作するGUIアプリケーションを開発するためのクリーンな**データモデルおよびリポジトリパターンのベースクラス群**と、それを利用して構築された**モダンなGUIアプリケーション**の実装サンプルです。

### 🌟 主な特徴

- **オブジェクト指向データモデル**: `BaseNodeObject`、`FileNodeObject`、`DirectoryNodeObject` によるポリモーフィズム設計。アイコン、多言語ファイル種別、サイズ、タイムスタンプをカプセル化。
- **リポジトリパターン**: GUI表示とファイル操作実処理を `FilerRepository` で疎結合化。
- **モダンなデスクトップGUI**: PySide6による Tokyo Night ダークテーマの洗練されたUI。
- **多言語対応 (日本語 / 英語)**: アプリを再起動せずにツールバーから即座に言語を切り替え可能。
- **快適なナビゲーション**: 戻る/進む履歴、上の階層移動、パス直接入力、リアルタイム検索フィルタ、サイドバーショートカット。
- **ファイル操作**: コンテキストメニューや詳細パネルからの新規ファイル/フォルダ作成、名前変更、削除、ファイルオープン。

### 📂 プロジェクト構成

```
PythonBaseClasses/
├── BaseNodeObject.py   # データモデル（ノード情報・アイコン・メタデータの保持）
├── FilerRepository.py  # リポジトリ（ファイルシステムの読み書き操作のカプセル化）
├── i18n.py             # 多言語化モジュール（日本語・英語対応）
├── main.py             # GUIアプリケーション (PySide6 / Tokyo Nightダークテーマ)
└── README.md           # 本書
```

### 🛠️ アーキテクチャと役割

1. **データモデル層 (`BaseNodeObject.py`)**
   - ファイル・ディレクトリ要素をオブジェクトとして表現し、UI用プロパティやメタデータをカプセル化。
   - `BaseNodeObject`: 基底クラス。パス・名前・選択状態（`updated` シグナル）、更新・作成日時。
   - `FileNodeObject`: ファイル表現。拡張子アイコン、ファイルサイズ、多言語ファイル種別名。
   - `DirectoryNodeObject`: ディレクトリ表現。配下の子ノードリスト（`children`）を保持。

2. **データアクセス・操作層 (`FilerRepository.py`)**
   - ファイルシステムの読み書き操作をカプセル化するリポジトリ。GUI層からOS標準モジュールへの直接依存を排除。
   - メソッド: `get_directory_node()`, `create_directory()`, `create_file()`, `rename_node()`, `delete_node()`。

3. **多言語化層 (`i18n.py`)**
   - 日本語（`ja`）および英語（`en`）のテキスト辞書と言語状態を管理。
   - 言語切替時のリスナー登録により、画面のリロード・再描画をシームレスに実施。

4. **UI・プレゼンテーション層 (`main.py`)**
   - PySide6を用いて構築されたデスクトップ向けGUI。
   - 履歴ナビゲーション、パスバー、インクリメンタル検索、型安全なソート対応テーブル、サイドバー、詳細メタデータパネル、コンテキストメニュー、言語切替ボタンを搭載。

### 🚀 セットアップと実行

#### 動作環境
- Python 3.12 以上
- PySide6

#### インストール手順

1. **仮想環境の作成**
   ```bash
   python3 -m venv venv
   ```

2. **依存関係のインストール**
   ```bash
   ./venv/bin/pip install PySide6
   ```

3. **アプリケーションの実行**
   ```bash
   ./venv/bin/python main.py
   ```

---

## 💡 本ベースクラス群を応用した開発

このリポジトリは、独自のファイル管理ツールや、画像ビューア、メディア管理ライブラリ、クラウド同期型ファイルマネージャー等の開発ベースとして利用できます。

- **ファイルプレビュー機能の追加**: `FileNodeObject` にプレビューデータ読み込み処理を拡張し、GUI側の詳細パネルで拡張子に応じて画像やテキストのプレビューを描画することが容易です。

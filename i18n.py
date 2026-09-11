"""
i18n module for PythonBaseClasses providing English and Japanese localization.
"""

from typing import Dict, Any, Callable, List

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # App & Window
        "app_title": "Antigravity Filer",
        "lang_name": "日本語",
        "ready": "Ready",
        
        # Navigation Tooltips & Placeholders
        "nav_back": "Back",
        "nav_forward": "Forward",
        "nav_up": "Up to parent folder",
        "nav_refresh": "Refresh current folder",
        "btn_new_folder": "Create New Folder",
        "btn_new_file": "Create New File",
        "path_placeholder": "Enter folder path...",
        "search_placeholder": "🔍 Filter files...",
        "toggle_language": "Switch language to Japanese",
        
        # Table Headers
        "col_select": "",
        "col_name": "Name",
        "col_type": "Type",
        "col_size": "Size",
        "col_modified": "Date Modified",
        
        # Sidebar Shortcuts
        "shortcut_home": "🏠 Home",
        "shortcut_documents": "📄 Documents",
        "shortcut_downloads": "📥 Downloads",
        "shortcut_desktop": "🖥️ Desktop",
        "shortcut_root": "💾 Root (/)",
        
        # Details Panel
        "details_title": "Item Details",
        "lbl_name": "Name",
        "lbl_type": "Type",
        "lbl_size": "Size",
        "lbl_path": "Path",
        "lbl_created": "Created",
        "lbl_modified": "Modified",
        "mark_selected": "Mark as Selected",
        "btn_open_file_or_folder": "Open File / Folder",
        "btn_open_folder": "Open Folder",
        "btn_open_file": "Open File",
        "btn_delete_item": "Delete Item",
        
        # Status Bar
        "status_total": "Total: {total} items",
        "status_total_selected": "Total: {total} items | Selected: {selected} items ({size})",
        
        # Context Menu
        "menu_open": "Open",
        "menu_rename": "Rename...",
        "menu_delete": "Delete",
        "menu_new_folder": "New Folder...",
        "menu_new_file": "New File...",
        "menu_refresh": "Refresh",
        
        # Dialogs & Prompts
        "dialog_rename_title": "Rename",
        "dialog_rename_prompt": "Enter new name for '{name}':",
        "dialog_confirm_delete_title": "Confirm Delete",
        "dialog_confirm_delete_msg": "Are you sure you want to delete '{name}'?\nThis action cannot be undone.",
        "dialog_new_folder_title": "New Folder",
        "dialog_new_folder_prompt": "Enter folder name:",
        "dialog_new_file_title": "New File",
        "dialog_new_file_prompt": "Enter file name:",
        "error_title": "Error",
        "error_rename": "Failed to rename '{name}'.",
        "error_delete": "Failed to delete '{name}'.",
        "error_create_folder": "Failed to create folder '{name}'.",
        "error_create_file": "Failed to create file '{name}'.",
        "error_nav_title": "Navigation Error",
        "error_nav_msg": "The directory does not exist:\n{path}",
        "error_open_title": "Error Opening File",
        "error_open_msg": "Could not open file:\n{path}\n\nError: {error}",
        
        # File Types
        "type_folder": "Folder",
        "type_file": "File",
        "type_unknown": "{ext} File",
        "type_archive": "{ext} Archive",
        "type_image": "{ext} Image",
        "type_audio": "{ext} Audio",
        "type_video": "{ext} Video",
        "type_code": "{ext} Script/Code",
        "type_text": "Text Document",
        "type_pdf": "PDF Document",
        "type_word": "Word Document",
        "type_spreadsheet": "Spreadsheet",
    },
    "ja": {
        # App & Window
        "app_title": "Antigravity ファイラー",
        "lang_name": "English",
        "ready": "準備完了",
        
        # Navigation Tooltips & Placeholders
        "nav_back": "戻る",
        "nav_forward": "進む",
        "nav_up": "上の階層へ",
        "nav_refresh": "現在のフォルダを更新",
        "btn_new_folder": "新規フォルダ作成",
        "btn_new_file": "新規ファイル作成",
        "path_placeholder": "フォルダパスを入力...",
        "search_placeholder": "🔍 ファイルを検索...",
        "toggle_language": "言語を英語に切り替える",
        
        # Table Headers
        "col_select": "",
        "col_name": "名前",
        "col_type": "種類",
        "col_size": "サイズ",
        "col_modified": "更新日時",
        
        # Sidebar Shortcuts
        "shortcut_home": "🏠 ホーム",
        "shortcut_documents": "📄 ドキュメント",
        "shortcut_downloads": "📥 ダウンロード",
        "shortcut_desktop": "🖥️ デスクトップ",
        "shortcut_root": "💾 ルート (/)",
        
        # Details Panel
        "details_title": "アイテム詳細",
        "lbl_name": "名前",
        "lbl_type": "種類",
        "lbl_size": "サイズ",
        "lbl_path": "パス",
        "lbl_created": "作成日時",
        "lbl_modified": "更新日時",
        "mark_selected": "選択中に設定",
        "btn_open_file_or_folder": "開く",
        "btn_open_folder": "フォルダを開く",
        "btn_open_file": "ファイルを開く",
        "btn_delete_item": "削除",
        
        # Status Bar
        "status_total": "合計: {total} 個の項目",
        "status_total_selected": "合計: {total} 個の項目 | 選択中: {selected} 個 ({size})",
        
        # Context Menu
        "menu_open": "開く",
        "menu_rename": "名前の変更...",
        "menu_delete": "削除",
        "menu_new_folder": "新規フォルダ作成...",
        "menu_new_file": "新規ファイル作成...",
        "menu_refresh": "更新",
        
        # Dialogs & Prompts
        "dialog_rename_title": "名前の変更",
        "dialog_rename_prompt": "'{name}' の新しい名前を入力してください:",
        "dialog_confirm_delete_title": "削除の確認",
        "dialog_confirm_delete_msg": "'{name}' を削除してもよろしいですか？\nこの操作は取り消せません。",
        "dialog_new_folder_title": "新規フォルダ",
        "dialog_new_folder_prompt": "フォルダ名を入力してください:",
        "dialog_new_file_title": "新規ファイル",
        "dialog_new_file_prompt": "ファイル名を入力してください:",
        "error_title": "エラー",
        "error_rename": "'{name}' の名前変更に失敗しました。",
        "error_delete": "'{name}' の削除に失敗しました。",
        "error_create_folder": "フォルダ '{name}' の作成に失敗しました。",
        "error_create_file": "ファイル '{name}' の作成に失敗しました。",
        "error_nav_title": "移動エラー",
        "error_nav_msg": "指定されたディレクトリが存在しません:\n{path}",
        "error_open_title": "ファイル読み込みエラー",
        "error_open_msg": "ファイルを開けませんでした:\n{path}\n\nエラー: {error}",
        
        # File Types
        "type_folder": "フォルダ",
        "type_file": "ファイル",
        "type_unknown": "{ext} ファイル",
        "type_archive": "{ext} アーカイブ",
        "type_image": "{ext} 画像",
        "type_audio": "{ext} 音声",
        "type_video": "{ext} 動画",
        "type_code": "{ext} スクリプト/コード",
        "type_text": "テキストドキュメント",
        "type_pdf": "PDFドキュメント",
        "type_word": "Wordドキュメント",
        "type_spreadsheet": "スプレッドシート",
    }
}

class I18nManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
            cls._instance._current_lang = "ja" # Default to Japanese
            cls._instance._listeners: List[Callable[[], None]] = []
        return cls._instance

    @property
    def current_language(self) -> str:
        return self._current_lang

    def set_language(self, lang: str):
        if lang in TRANSLATIONS and self._current_lang != lang:
            self._current_lang = lang
            self._notify_listeners()

    def toggle_language(self):
        new_lang = "en" if self._current_lang == "ja" else "ja"
        self.set_language(new_lang)

    def add_listener(self, callback: Callable[[], None]):
        if callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[], None]):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify_listeners(self):
        for listener in list(self._listeners):
            try:
                listener()
            except Exception:
                pass

    def t(self, key: str, **kwargs: Any) -> str:
        lang_dict = TRANSLATIONS.get(self._current_lang, TRANSLATIONS["en"])
        template = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
        if kwargs:
            try:
                return template.format(**kwargs)
            except Exception:
                return template
        return template

# Global singleton helper
i18n = I18nManager()

def t(key: str, **kwargs: Any) -> str:
    return i18n.t(key, **kwargs)

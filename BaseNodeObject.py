from PySide6.QtCore import QObject, Signal
import os
from i18n import t

def format_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 Bytes"
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

class BaseNodeObject(QObject):
    """ファイルやディレクトリのベースとなるデータオブジェクト"""
    updated = Signal(object) # 状態が変わったらGUIに通知する信号

    def __init__(self, path: str):
        super().__init__()
        self.path = os.path.abspath(path)
        self.name = os.path.basename(path)
        self._is_selected = False
        self.size = 0

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        if self._is_selected != value:
            self._is_selected = value
            self.updated.emit(self) # 選択状態が変わったら再描画を促す

    @property
    def exists(self) -> bool:
        return os.path.exists(self.path)

    @property
    def modified_time(self) -> float:
        try:
            return os.path.getmtime(self.path) if self.exists else 0.0
        except Exception:
            return 0.0

    @property
    def created_time(self) -> float:
        try:
            return os.path.getctime(self.path) if self.exists else 0.0
        except Exception:
            return 0.0

    @property
    def icon(self) -> str:
        return "📄"

    @property
    def type_name(self) -> str:
        return t("type_file")

    @property
    def size_str(self) -> str:
        return "-"


class FileNodeObject(BaseNodeObject):
    """ファイルを表すオブジェクト（サイズや拡張子などの情報を持つ）"""
    def __init__(self, path: str):
        super().__init__(path)
        self.size = os.path.getsize(path) if os.path.exists(path) else 0
        self.extension = os.path.splitext(self.name)[1]

    @property
    def size_str(self) -> str:
        return format_size(self.size)

    @property
    def icon(self) -> str:
        ext = self.extension.lower()
        if ext in ['.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z']:
            return "📦"
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']:
            return "🖼️"
        elif ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
            return "🎵"
        elif ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv']:
            return "🎥"
        elif ext in ['.py', '.js', '.ts', '.html', '.css', '.cpp', '.c', '.h', '.go', '.rs', '.java', '.sh', '.bat']:
            return "⚙️"
        elif ext in ['.txt', '.md', '.ini', '.cfg', '.json', '.yaml', '.yml', '.xml']:
            return "📄"
        elif ext in ['.pdf']:
            return "📕"
        elif ext in ['.doc', '.docx', '.odt']:
            return "📘"
        elif ext in ['.xls', '.xlsx', '.ods']:
            return "📗"
        else:
            return "📄"

    @property
    def type_name(self) -> str:
        ext = self.extension.lower()
        ext_label = ext[1:].upper() if ext else ""
        if ext in ['.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z']:
            return t("type_archive", ext=ext_label)
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']:
            return t("type_image", ext=ext_label)
        elif ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
            return t("type_audio", ext=ext_label)
        elif ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv']:
            return t("type_video", ext=ext_label)
        elif ext in ['.py', '.js', '.ts', '.html', '.css', '.cpp', '.c', '.h', '.go', '.rs', '.java', '.sh', '.bat']:
            return t("type_code", ext=ext_label)
        elif ext in ['.txt', '.md', '.ini', '.cfg', '.json', '.yaml', '.yml', '.xml']:
            return t("type_text")
        elif ext in ['.pdf']:
            return t("type_pdf")
        elif ext in ['.doc', '.docx', '.odt']:
            return t("type_word")
        elif ext in ['.xls', '.xlsx', '.ods']:
            return t("type_spreadsheet")
        else:
            return t("type_unknown", ext=ext_label) if ext_label else t("type_file")


class DirectoryNodeObject(BaseNodeObject):
    """ディレクトリを表すオブジェクト（配下の子オブジェクトリストを持つ）"""
    def __init__(self, path: str):
        super().__init__(path)
        self.size = -1
        self.children: list[BaseNodeObject] = []

    @property
    def icon(self) -> str:
        return "📁"

    @property
    def type_name(self) -> str:
        return t("type_folder")

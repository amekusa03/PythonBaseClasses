import os
import shutil
from BaseNodeObject import DirectoryNodeObject, FileNodeObject

class FilerRepository:
    """ローカルのファイルシステムからノード（オブジェクト）を取得し、操作するラッパー"""
    
    def get_directory_node(self, dir_path: str) -> DirectoryNodeObject:
        """指定されたパスのディレクトリノードを作成し、中身のノード群を詰めて返す"""
        dir_node = DirectoryNodeObject(dir_path)
        
        if not os.path.isdir(dir_path):
            return dir_node

        try:
            for entry in os.scandir(dir_path):
                if entry.is_dir():
                    dir_node.children.append(DirectoryNodeObject(entry.path))
                else:
                    dir_node.children.append(FileNodeObject(entry.path))
        except PermissionError:
            pass # アクセス権限がない場合は空のまま返す
            
        return dir_node

    def create_directory(self, parent_path: str, name: str) -> bool:
        """指定された親ディレクトリ配下に新しいディレクトリを作成する"""
        target_path = os.path.join(parent_path, name)
        try:
            os.makedirs(target_path, exist_ok=False)
            return True
        except Exception:
            return False

    def create_file(self, parent_path: str, name: str) -> bool:
        """指定された親ディレクトリ配下に新しい空ファイルを作成する"""
        target_path = os.path.join(parent_path, name)
        try:
            # ファイルが既に存在する場合はエラーになるように 'x' モードを使用
            with open(target_path, 'x'):
                pass
            return True
        except Exception:
            return False

    def rename_node(self, node_path: str, new_name: str) -> bool:
        """ノードの名前を変更する"""
        if not os.path.exists(node_path):
            return False
        parent_dir = os.path.dirname(node_path)
        new_path = os.path.join(parent_dir, new_name)
        try:
            os.rename(node_path, new_path)
            return True
        except Exception:
            return False

    def delete_node(self, node_path: str) -> bool:
        """ノード（ファイルまたはディレクトリ）を削除する"""
        if not os.path.exists(node_path):
            return False
        try:
            if os.path.isdir(node_path):
                shutil.rmtree(node_path)
            else:
                os.remove(node_path)
            return True
        except Exception:
            return False
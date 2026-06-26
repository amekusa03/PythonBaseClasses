import sys
import os
import datetime
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem,
    QPushButton, QLineEdit, QLabel, QSplitter, QStatusBar, QHeaderView,
    QCheckBox, QFrame, QMessageBox, QMenu, QInputDialog
)
from BaseNodeObject import BaseNodeObject, FileNodeObject, DirectoryNodeObject, format_size
from FilerRepository import FilerRepository

def format_datetime(timestamp):
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "-"

class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, text, sort_value):
        super().__init__(text)
        self.sort_value = sort_value

    def __lt__(self, other):
        if isinstance(other, NumericTableWidgetItem):
            return self.sort_value < other.sort_value
        return super().__lt__(other)

class FilerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antigravity Filer")
        self.resize(1150, 720)
        
        self.repository = FilerRepository()
        self.current_directory_path = ""
        self.current_nodes = []
        self.selected_node = None
        
        # Navigation History
        self.history_back = []
        self.history_forward = []
        
        self.init_ui()
        self.apply_styles()
        
        # Navigate to home directory by default
        home_path = os.path.expanduser("~")
        if os.path.exists(home_path):
            self.navigate_to(home_path)
        else:
            self.navigate_to("/")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # --- Top Navigation Bar ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        
        self.btn_back = QPushButton("◀")
        self.btn_back.setToolTip("Back")
        self.btn_back.setFixedWidth(40)
        self.btn_back.clicked.connect(self.navigate_back)
        
        self.btn_forward = QPushButton("▶")
        self.btn_forward.setToolTip("Forward")
        self.btn_forward.setFixedWidth(40)
        self.btn_forward.clicked.connect(self.navigate_forward)
        
        self.btn_up = QPushButton("▲")
        self.btn_up.setToolTip("Up to parent folder")
        self.btn_up.setFixedWidth(40)
        self.btn_up.clicked.connect(self.navigate_up)
        
        self.btn_refresh = QPushButton("🔄")
        self.btn_refresh.setToolTip("Refresh current folder")
        self.btn_refresh.setFixedWidth(40)
        self.btn_refresh.clicked.connect(self.refresh_directory)

        self.btn_new_folder = QPushButton("📁+")
        self.btn_new_folder.setToolTip("Create New Folder")
        self.btn_new_folder.setFixedWidth(40)
        self.btn_new_folder.clicked.connect(self.create_folder)

        self.btn_new_file = QPushButton("📄+")
        self.btn_new_file.setToolTip("Create New File")
        self.btn_new_file.setFixedWidth(40)
        self.btn_new_file.clicked.connect(self.create_file_item)
        
        self.path_bar = QLineEdit()
        self.path_bar.setPlaceholderText("Enter folder path...")
        self.path_bar.returnPressed.connect(self.on_path_bar_entered)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Filter files...")
        self.search_bar.setFixedWidth(180)
        self.search_bar.textChanged.connect(self.filter_table)
        
        top_bar.addWidget(self.btn_back)
        top_bar.addWidget(self.btn_forward)
        top_bar.addWidget(self.btn_up)
        top_bar.addWidget(self.btn_refresh)
        top_bar.addWidget(self.btn_new_folder)
        top_bar.addWidget(self.btn_new_file)
        top_bar.addWidget(self.path_bar, stretch=1)
        top_bar.addWidget(self.search_bar)
        
        main_layout.addLayout(top_bar)
        
        # --- Splitter for Workspace Division ---
        self.splitter = QSplitter(Qt.Horizontal)
        
        # 1. Left Sidebar (Shortcuts)
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.setup_sidebar_shortcuts()
        self.sidebar.itemClicked.connect(self.on_sidebar_clicked)
        self.splitter.addWidget(self.sidebar)
        
        # 2. Central Files Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["", "Name", "Type", "Size", "Date Modified"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Interactive)
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        # Context Menu Trigger
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        self.table.itemChanged.connect(self.on_item_changed)
        
        self.splitter.addWidget(self.table)
        
        # 3. Right Details Panel
        self.details_panel = QFrame()
        self.details_panel.setObjectName("detailsPanel")
        self.setup_details_panel()
        self.splitter.addWidget(self.details_panel)
        
        # Set initial splitter proportions (Sidebar: 15%, Table: 60%, Details: 25%)
        self.splitter.setSizes([160, 640, 260])
        
        main_layout.addWidget(self.splitter)
        
        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def setup_sidebar_shortcuts(self):
        shortcuts = [
            ("🏠 Home", os.path.expanduser("~")),
            ("📄 Documents", os.path.expanduser("~/Documents")),
            ("📥 Downloads", os.path.expanduser("~/Downloads")),
            ("🖥️ Desktop", os.path.expanduser("~/Desktop")),
            ("💾 Root (/) ", "/"),
        ]
        
        for name, path in shortcuts:
            if os.path.exists(path):
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, path)
                self.sidebar.addItem(item)

    def setup_details_panel(self):
        layout = QVBoxLayout(self.details_panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)
        
        # Title Label
        title_label = QLabel("Item Details")
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #7aa2f7; margin-bottom: 4px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Large Icon Display
        self.detail_icon = QLabel("📁")
        icon_font = QFont()
        icon_font.setPointSize(48)
        self.detail_icon.setFont(icon_font)
        self.detail_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.detail_icon)
        
        # Meta info
        self.detail_name = QLabel("Name: -")
        self.detail_name.setWordWrap(True)
        self.detail_type = QLabel("Type: -")
        self.detail_size = QLabel("Size: -")
        self.detail_path = QLabel("Path: -")
        self.detail_path.setWordWrap(True)
        self.detail_created = QLabel("Created: -")
        self.detail_modified = QLabel("Modified: -")
        
        layout.addWidget(self.detail_name)
        layout.addWidget(self.detail_type)
        layout.addWidget(self.detail_size)
        layout.addWidget(self.detail_path)
        layout.addWidget(self.detail_created)
        layout.addWidget(self.detail_modified)
        
        # Selection checkbox
        self.detail_select_checkbox = QCheckBox("Mark as Selected")
        self.detail_select_checkbox.setEnabled(False)
        self.detail_select_checkbox.toggled.connect(self.on_detail_select_toggled)
        layout.addWidget(self.detail_select_checkbox)
        
        layout.addStretch()
        
        # Action buttons
        self.btn_open_item = QPushButton("Open File / Folder")
        self.btn_open_item.setEnabled(False)
        self.btn_open_item.clicked.connect(self.on_open_clicked_from_details)
        layout.addWidget(self.btn_open_item)

        self.btn_delete_item = QPushButton("Delete Item")
        self.btn_delete_item.setEnabled(False)
        self.btn_delete_item.setObjectName("deleteBtn")
        self.btn_delete_item.clicked.connect(self.on_delete_clicked_from_details)
        layout.addWidget(self.btn_delete_item)

    def apply_styles(self):
        qss = """
        QMainWindow {
            background-color: #1a1b26;
        }
        
        QWidget {
            color: #c0caf5;
            font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
            font-size: 13px;
        }
        
        /* Left Sidebar List Widget */
        QListWidget#sidebar {
            background-color: #16161e;
            border: 1px solid #24283b;
            border-radius: 8px;
            padding: 6px;
        }
        QListWidget#sidebar::item {
            padding: 8px 12px;
            border-radius: 6px;
            margin: 2px 0px;
            color: #a9b1d6;
        }
        QListWidget#sidebar::item:hover {
            background-color: #24283b;
            color: #c0caf5;
        }
        QListWidget#sidebar::item:selected {
            background-color: #3b4261;
            color: #7aa2f7;
            font-weight: bold;
        }
        
        /* Central Table */
        QTableWidget {
            background-color: #1a1b26;
            border: 1px solid #24283b;
            border-radius: 8px;
            gridline-color: #1f2335;
        }
        QTableWidget::item {
            padding: 6px 8px;
            color: #c0caf5;
        }
        QTableWidget::item:hover {
            background-color: #24283b;
        }
        QTableWidget::item:selected {
            background-color: #2e3c64;
            color: #c0caf5;
        }
        QHeaderView::section {
            background-color: #16161e;
            color: #787c99;
            padding: 8px;
            border: none;
            border-bottom: 2px solid #24283b;
            font-weight: bold;
        }
        
        /* Top bar & General Buttons */
        QPushButton {
            background-color: #16161e;
            color: #c0caf5;
            border: 1px solid #3b4261;
            border-radius: 6px;
            padding: 6px 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #24283b;
            border-color: #7aa2f7;
            color: #7aa2f7;
        }
        QPushButton:pressed {
            background-color: #1f2335;
        }
        QPushButton:disabled {
            background-color: #16161e;
            color: #444b6a;
            border-color: #24283b;
        }
        
        /* Specific Red Delete Button */
        QPushButton#deleteBtn {
            background-color: #382530;
            color: #f7768e;
            border: 1px solid #f7768e;
        }
        QPushButton#deleteBtn:hover {
            background-color: #f7768e;
            color: #1a1b26;
        }
        QPushButton#deleteBtn:disabled {
            background-color: #16161e;
            color: #444b6a;
            border-color: #24283b;
        }
        
        /* Input Line Edits */
        QLineEdit {
            background-color: #16161e;
            color: #c0caf5;
            border: 1px solid #3b4261;
            border-radius: 6px;
            padding: 6px 10px;
        }
        QLineEdit:focus {
            border-color: #7aa2f7;
        }
        
        /* Details Sidebar Panel */
        QFrame#detailsPanel {
            background-color: #16161e;
            border: 1px solid #24283b;
            border-radius: 8px;
        }
        QFrame#detailsPanel QLabel {
            color: #a9b1d6;
            font-size: 13px;
        }
        
        /* Checkboxes */
        QCheckBox {
            spacing: 8px;
            color: #a9b1d6;
        }
        
        /* Scrollbar aesthetics */
        QScrollBar:vertical {
            border: none;
            background: #16161e;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #3b4261;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: #7aa2f7;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            border: none;
            background: #16161e;
            height: 10px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background: #3b4261;
            min-width: 20px;
            border-radius: 5px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #7aa2f7;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        
        /* Splitter handle */
        QSplitter::handle {
            background-color: #24283b;
        }
        QSplitter::handle:horizontal {
            width: 3px;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #16161e;
            color: #787c99;
            border-top: 1px solid #24283b;
        }
        QStatusBar QLabel {
            color: #787c99;
        }
        """
        self.setStyleSheet(qss)

    def navigate_to(self, path, push_history=True):
        path = os.path.abspath(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            QMessageBox.warning(self, "Navigation Error", f"The directory does not exist:\n{path}")
            return
        
        # Save history
        if push_history and self.current_directory_path:
            self.history_back.append(self.current_directory_path)
            self.history_forward.clear()
            
        self.current_directory_path = path
        self.path_bar.setText(path)
        
        self.update_nav_buttons()
        
        # Load directory contents using our FilerRepository
        dir_node = self.repository.get_directory_node(path)
        self.current_nodes = dir_node.children
        
        # Sort current nodes: Directories first, then Files alphabetically
        def sort_key(node):
            is_dir = isinstance(node, DirectoryNodeObject)
            return (0 if is_dir else 1, node.name.lower())
        self.current_nodes.sort(key=sort_key)
        
        # Setup updated Signal connections
        for node in self.current_nodes:
            node.updated.connect(self.on_node_updated)
            
        # Draw table
        self.populate_table()
        self.clear_details_panel()
        self.highlight_sidebar_item(path)
        self.update_status_bar()

    def populate_table(self):
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.current_nodes))
        
        for row, node in enumerate(self.current_nodes):
            # Checkbox item
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
            chk_item.setCheckState(Qt.Checked if node.is_selected else Qt.Unchecked)
            # Store the node object reference in data
            chk_item.setData(Qt.UserRole + 1, node)
            self.table.setItem(row, 0, chk_item)
            
            # Name (Icon is now a property on node)
            name_item = QTableWidgetItem(f"{node.icon}  {node.name}")
            self.table.setItem(row, 1, name_item)
            
            # Type (Type description is now a property on node)
            type_item = QTableWidgetItem(node.type_name)
            self.table.setItem(row, 2, type_item)
            
            # Size (Size string and numeric size are properties on node)
            size_item = NumericTableWidgetItem(node.size_str, node.size)
            self.table.setItem(row, 3, size_item)
            
            # Date Modified (Timestamp is now a property on node)
            mtime = node.modified_time
            mtime_str = format_datetime(mtime)
            mtime_item = NumericTableWidgetItem(mtime_str, mtime)
            self.table.setItem(row, 4, mtime_item)
            
        self.table.setSortingEnabled(True)
        self.table.blockSignals(False)

    def on_item_changed(self, item):
        if item.column() == 0:
            node = item.data(Qt.UserRole + 1)
            if node:
                is_checked = (item.checkState() == Qt.Checked)
                if node.is_selected != is_checked:
                    node.is_selected = is_checked

    def on_node_updated(self, node):
        # Synchronize table view checkbox
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.data(Qt.UserRole + 1) == node:
                item.setCheckState(Qt.Checked if node.is_selected else Qt.Unchecked)
                break
        self.table.blockSignals(False)
        
        # Synchronize details panel checkbox
        if self.selected_node == node:
            self.detail_select_checkbox.blockSignals(True)
            self.detail_select_checkbox.setChecked(node.is_selected)
            self.detail_select_checkbox.blockSignals(False)
            
        self.update_status_bar()

    def on_table_selection_changed(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            self.clear_details_panel()
            return
            
        row = selected_ranges[0].topRow()
        item = self.table.item(row, 0)
        if item:
            node = item.data(Qt.UserRole + 1)
            if node:
                self.show_details(node)

    def on_cell_double_clicked(self, row, column):
        item = self.table.item(row, 0)
        if item:
            node = item.data(Qt.UserRole + 1)
            if isinstance(node, DirectoryNodeObject):
                self.navigate_to(node.path)
            elif isinstance(node, FileNodeObject):
                self.open_file(node.path)

    def show_details(self, node):
        self.selected_node = node
        
        self.detail_icon.setText(node.icon)
        self.detail_name.setText(f"<b>Name:</b> {node.name}")
        self.detail_type.setText(f"<b>Type:</b> {node.type_name}")
        self.detail_size.setText(f"<b>Size:</b> {node.size_str}")
        self.detail_path.setText(f"<b>Path:</b> {node.path}")
        
        self.detail_created.setText(f"<b>Created:</b> {format_datetime(node.created_time)}")
        self.detail_modified.setText(f"<b>Modified:</b> {format_datetime(node.modified_time)}")
        
        self.detail_select_checkbox.setEnabled(True)
        self.detail_select_checkbox.blockSignals(True)
        self.detail_select_checkbox.setChecked(node.is_selected)
        self.detail_select_checkbox.blockSignals(False)
        
        self.btn_open_item.setEnabled(True)
        if isinstance(node, DirectoryNodeObject):
            self.btn_open_item.setText("Open Folder")
        else:
            self.btn_open_item.setText("Open File")

        self.btn_delete_item.setEnabled(True)

    def clear_details_panel(self):
        self.selected_node = None
        self.detail_icon.setText("📁")
        self.detail_name.setText("Name: -")
        self.detail_type.setText("Type: -")
        self.detail_size.setText("Size: -")
        self.detail_path.setText("Path: -")
        self.detail_created.setText("Created: -")
        self.detail_modified.setText("Modified: -")
        
        self.detail_select_checkbox.blockSignals(True)
        self.detail_select_checkbox.setChecked(False)
        self.detail_select_checkbox.setEnabled(False)
        self.detail_select_checkbox.blockSignals(False)
        
        self.btn_open_item.setText("Open File / Folder")
        self.btn_open_item.setEnabled(False)

        self.btn_delete_item.setEnabled(False)

    def on_detail_select_toggled(self, checked):
        if self.selected_node:
            self.selected_node.is_selected = checked

    def on_open_clicked_from_details(self):
        if self.selected_node:
            if isinstance(self.selected_node, DirectoryNodeObject):
                self.navigate_to(self.selected_node.path)
            elif isinstance(self.selected_node, FileNodeObject):
                self.open_file(self.selected_node.path)

    def on_delete_clicked_from_details(self):
        if self.selected_node:
            self.delete_node(self.selected_node)

    def open_file(self, path):
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        except Exception as e:
            QMessageBox.warning(self, "Error Opening File", f"Could not open file:\n{path}\n\nError: {str(e)}")

    def navigate_back(self):
        if self.history_back:
            path = self.history_back.pop()
            self.history_forward.append(self.current_directory_path)
            self.navigate_to(path, push_history=False)

    def navigate_forward(self):
        if self.history_forward:
            path = self.history_forward.pop()
            self.history_back.append(self.current_directory_path)
            self.navigate_to(path, push_history=False)

    def navigate_up(self):
        parent_dir = os.path.dirname(self.current_directory_path)
        if parent_dir != self.current_directory_path:
            self.navigate_to(parent_dir)

    def refresh_directory(self):
        if self.current_directory_path:
            self.navigate_to(self.current_directory_path, push_history=False)

    def on_path_bar_entered(self):
        target_path = self.path_bar.text().strip()
        if target_path.startswith("~"):
            target_path = os.path.expanduser(target_path)
        self.navigate_to(target_path)

    def update_nav_buttons(self):
        self.btn_back.setEnabled(len(self.history_back) > 0)
        self.btn_forward.setEnabled(len(self.history_forward) > 0)
        
        parent_dir = os.path.dirname(self.current_directory_path)
        self.btn_up.setEnabled(self.current_directory_path != "/" and parent_dir != self.current_directory_path)

    def filter_table(self):
        filter_text = self.search_bar.text().strip().lower()
        for row in range(self.table.rowCount()):
            chk_item = self.table.item(row, 0)
            node = chk_item.data(Qt.UserRole + 1) if chk_item else None
            name_to_check = node.name.lower() if node else ""
            should_show = filter_text in name_to_check
            self.table.setRowHidden(row, not should_show)

    def highlight_sidebar_item(self, path):
        self.sidebar.blockSignals(True)
        self.sidebar.clearSelection()
        for i in range(self.sidebar.count()):
            item = self.sidebar.item(i)
            item_path = item.data(Qt.UserRole)
            if item_path == path:
                item.setSelected(True)
                break
        self.sidebar.blockSignals(False)

    def update_status_bar(self):
        total_items = len(self.current_nodes)
        selected_nodes = [node for node in self.current_nodes if node.is_selected]
        selected_count = len(selected_nodes)
        
        if selected_count > 0:
            selected_size = sum(node.size for node in selected_nodes if isinstance(node, FileNodeObject))
            size_str = format_size(selected_size)
            self.status_bar.showMessage(
                f"Total: {total_items} items | Selected: {selected_count} items ({size_str})"
            )
        else:
            self.status_bar.showMessage(f"Total: {total_items} items")

    def on_sidebar_clicked(self, item):
        path = item.data(Qt.UserRole)
        if path:
            self.navigate_to(path)

    def show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #16161e;
                color: #c0caf5;
                border: 1px solid #24283b;
                border-radius: 6px;
                padding: 4px 0px;
            }
            QMenu::item {
                padding: 6px 22px;
            }
            QMenu::item:selected {
                background-color: #2e3c64;
                color: #7aa2f7;
            }
            QMenu::separator {
                height: 1px;
                background-color: #24283b;
                margin: 4px 0px;
            }
        """)
        
        node = None
        if item:
            row = item.row()
            chk_item = self.table.item(row, 0)
            if chk_item:
                node = chk_item.data(Qt.UserRole + 1)
                
        if node:
            action_open = menu.addAction("Open")
            action_rename = menu.addAction("Rename...")
            action_delete = menu.addAction("Delete")
            menu.addSeparator()
            
            action_new_folder = menu.addAction("New Folder...")
            action_new_file = menu.addAction("New File...")
            menu.addSeparator()
            action_refresh = menu.addAction("Refresh")
            
            selected_action = menu.exec(self.table.mapToGlobal(pos))
            
            if selected_action == action_open:
                if isinstance(node, DirectoryNodeObject):
                    self.navigate_to(node.path)
                else:
                    self.open_file(node.path)
            elif selected_action == action_rename:
                self.rename_node(node)
            elif selected_action == action_delete:
                self.delete_node(node)
            elif selected_action == action_new_folder:
                self.create_folder()
            elif selected_action == action_new_file:
                self.create_file_item()
            elif selected_action == action_refresh:
                self.refresh_directory()
        else:
            action_new_folder = menu.addAction("New Folder...")
            action_new_file = menu.addAction("New File...")
            menu.addSeparator()
            action_refresh = menu.addAction("Refresh")
            
            selected_action = menu.exec(self.table.mapToGlobal(pos))
            
            if selected_action == action_new_folder:
                self.create_folder()
            elif selected_action == action_new_file:
                self.create_file_item()
            elif selected_action == action_refresh:
                self.refresh_directory()

    def rename_node(self, node):
        new_name, ok = QInputDialog.getText(
            self, "Rename", f"Enter new name for '{node.name}':", text=node.name
        )
        if ok and new_name.strip() and new_name.strip() != node.name:
            success = self.repository.rename_node(node.path, new_name.strip())
            if success:
                self.refresh_directory()
            else:
                QMessageBox.critical(self, "Error", f"Failed to rename '{node.name}'.")

    def delete_node(self, node):
        reply = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete '{node.name}'?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.repository.delete_node(node.path)
            if success:
                # If deleted node was selected, clear details panel
                if self.selected_node == node:
                    self.clear_details_panel()
                self.refresh_directory()
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete '{node.name}'.")

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(
            self, "New Folder", "Enter folder name:"
        )
        if ok and folder_name.strip():
            success = self.repository.create_directory(self.current_directory_path, folder_name.strip())
            if success:
                self.refresh_directory()
            else:
                QMessageBox.critical(self, "Error", f"Failed to create folder '{folder_name}'.")

    def create_file_item(self):
        file_name, ok = QInputDialog.getText(
            self, "New File", "Enter file name:"
        )
        if ok and file_name.strip():
            success = self.repository.create_file(self.current_directory_path, file_name.strip())
            if success:
                self.refresh_directory()
            else:
                QMessageBox.critical(self, "Error", f"Failed to create file '{file_name}'.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilerMainWindow()
    window.show()
    sys.exit(app.exec())

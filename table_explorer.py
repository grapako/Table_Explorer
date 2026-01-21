import sys
import os
import pandas as pd
from typing import List, Optional, Union
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, 
                             QWidget, QLineEdit, QLabel, QHeaderView, QMessageBox)
from PyQt5.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel

# =============================================================================
# GUI CLASSES (Model & View)
# =============================================================================

class PandasModel(QAbstractTableModel):
    """
    A model to interface a pandas.DataFrame with a QTableView.
    Enables sorting and fast data display.
    """
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        col_name = self._data.columns[column]
        ascending = (order == Qt.AscendingOrder)
        self._data.sort_values(by=col_name, ascending=ascending, inplace=True)
        self.layoutChanged.emit()

class TableViewer(QMainWindow):
    """
    The main window that displays the data, allows filtering and sorting.
    """
    def __init__(self, df: pd.DataFrame, title: str = "Table Viewer", info: str = ""):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(1000, 600) # Slightly larger default

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 1. Info Label (shows separator info etc)
        if info:
            self.info_label = QLabel(f"Info: {info}")
            self.info_label.setStyleSheet("color: gray; font-style: italic;")
            self.layout.addWidget(self.info_label)

        # 2. Filter Input
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Type to filter rows (RegEx supported)...")
        self.filter_input.textChanged.connect(self.apply_filter)
        self.layout.addWidget(self.filter_input)

        # 3. Status Label
        self.status_label = QLabel(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
        self.layout.addWidget(self.status_label)

        # 4. Table View setup
        self.table_view = QTableView()
        self.model = PandasModel(df)
        
        # Proxy Model for Filtering and Sorting
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1) # Filter all columns

        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setAlternatingRowColors(True)
        
        self.layout.addWidget(self.table_view)

    def apply_filter(self, text):
        """Updates the proxy model regex to filter rows."""
        self.proxy_model.setFilterFixedString(text)

# =============================================================================
# HELPER FUNCTIONS (File Listing & Selection)
# =============================================================================

def get_files_multiext(path: str = '.', extensions: list = ['.csv', '.dat', '.txt']) -> pd.DataFrame:
    """
    Lists files matching multiple extensions. Returns a DataFrame for the selector.
    """
    search_path = os.path.abspath(os.path.expanduser(path))
    
    if not os.path.exists(search_path):
        print(f"Error: Path not found: {search_path}")
        return pd.DataFrame()

    all_files = os.listdir(search_path)
    matching_files = [
        f for f in all_files 
        if os.path.isfile(os.path.join(search_path, f)) and 
        any(f.lower().endswith(ext.lower()) for ext in extensions)
    ]
    
    matching_files.sort()
    
    if not matching_files:
        return pd.DataFrame()

    df = pd.DataFrame(matching_files, columns=['Options'])
    df.index += 1
    return df

def list_selector(list_or_pandas, message='Select files to open (e.g., "1,3" or Enter for all):'):
    """
    Allows user to select files from the list.
    """
    if isinstance(list_or_pandas, list):
        listanumerada = pd.DataFrame(list_or_pandas, columns=['Options'])
        listanumerada.index += 1
    else:
        listanumerada = list_or_pandas

    if listanumerada.empty:
        print("No files found with the specified extensions.")
        return []

    print("\n" + "="*60)
    print(listanumerada)
    print("="*60 + "\n")
    
    while True:
        try:
            print(message)
            seleccion = str.casefold(input("[Enter] for all, [s] to skip/exit: ")).strip()
            
            if seleccion == '':
                return listanumerada['Options'].to_list()
            elif seleccion == 's':
                return []
            elif "," in seleccion:
                indices = [int(num.strip()) for num in seleccion.split(',') if num.strip().isdigit()]
                return listanumerada['Options'].loc[indices].to_list()
            else:
                if seleccion.isdigit():
                    return [listanumerada['Options'].loc[int(seleccion)]]
                # Allow selecting 0 or out of bounds to loop back? No, just catch error.
        except KeyError:
            print("Error: Invalid number selected.")
            continue
        except ValueError:
            print("Error: Please enter numbers separated by commas.")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

def load_data(filepath):
    """
    Attempts to load data intelligently using pandas by trying multiple strategies.
    Returns: (DataFrame, info_string) or (None, error_message)
    """
    strategies = [
        # Strategy 1: Whitespace (High priority for scientific data, even if .csv)
        {'sep': r'\s+', 'engine': 'python', 'desc': 'Whitespace Separated'},
        
        # Strategy 2: Auto-detect (Good for standard CSVs)
        {'sep': None, 'engine': 'python', 'desc': 'Auto-Detected'},
        
        # Strategy 3: Standard CSV (comma) - Fast engine
        {'sep': ',', 'engine': 'c', 'desc': 'Comma Separated'},
        
        # Strategy 4: Semicolon (common in Europe)
        {'sep': ';', 'engine': 'c', 'desc': 'Semicolon Separated'},
        
        # Strategy 5: Tab
        {'sep': '\t', 'engine': 'c', 'desc': 'Tab Separated'},
    ]

    print(f"   Reading {os.path.basename(filepath)}...")
    
    last_error = ""

    for strat in strategies:
        try:
            # Construct kwargs, removing 'desc'
            kwargs = {k: v for k, v in strat.items() if k != 'desc'}
            
            # Try reading
            df = pd.read_csv(filepath, **kwargs)
            
            # Basic validation: If we read 1 column but file is large, maybe it failed to split?
            if df.shape[1] < 2 and df.shape[0] > 0:
                # If we only found 1 column, it might be a failure to split, 
                # but valid for 1-col files. We'll accept it but keep trying if we haven't tried all.
                # Actually, for safety, let's assume success if no exception, 
                # but maybe prioritize strategies that yield more columns?
                # For now, let's just return the first success.
                pass
            
            msg = f"Loaded successfully using {strat['desc']}"
            print(f"     -> {msg}")
            return df, msg
            
        except Exception as e:
            last_error = str(e)
            # print(f"     -> Failed with {strat['desc']}: {e}") # Debug only
            continue
            
    print(f"     -> Error: Failed to parse. Last error: {last_error}")
    return None, last_error

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    # 1. Define extensions to look for
    extensions = ['.csv', '.dat', '.txt']
    
    # 2. Get file list
    current_dir = os.getcwd()
    print(f"Scanning {current_dir} for {extensions}...")
    df_files = get_files_multiext(path=current_dir, extensions=extensions)
    
    # 3. User Selection (CLI)
    selected_files = list_selector(df_files)
    
    if not selected_files:
        print("No files selected. Exiting.")
        return

    # 4. GUI Initialization
    app = QApplication(sys.argv)
    
    windows = [] # Keep references to windows
    
    print("\nProcessing files...")
    for filename in selected_files:
        filepath = os.path.join(current_dir, filename)
        
        df, info_msg = load_data(filepath)
        
        if df is not None:
            # Create a window for this file
            viewer = TableViewer(df, title=f"Viewer: {filename}", info=info_msg)
            viewer.show()
            windows.append(viewer) 
        else:
            print(f"     -> Skipping {filename} due to errors.")

    if windows:
        print(f"\n{len(windows)} windows open. Check your taskbar.")
        sys.exit(app.exec_())
    else:
        print("\nNo valid files could be loaded.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
import sys
import os

def resource_path(relative_path):
    """獲取打包後與開發時一樣的資源路徑"""
    try:
        # PyInstaller 建立的臨時資料夾 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

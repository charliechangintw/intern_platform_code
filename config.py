import os

# os.path.dirname(__file__) 獲取當前文件(config.py)的目錄
# os.path.abspath() 將該目錄轉換為絕對路徑， BASE_DIR 變數儲存了您應用程式的根目錄絕對路徑
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 將 BASE_DIR 和 'uploads' 字串組合，創建一個指向應用程式中 uploads 目錄的路徑
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

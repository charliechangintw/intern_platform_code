
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response, session
import os
import logging
import pandas as pd
from preprocessing import Preprocessing
from counter import count_words, process_subject
from wordCloud import generate_wordcloud
from structured_csv import structure_csv
# render_template: 渲染 HTML 模板。request: 處理 HTTP 請求。jonify: 將 Python 列表轉換為 JSON 格式。os: 與作業系統互動

# 初始化 Flask
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# 設定上傳文件資料夾的路徑
from config import UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 全域變數
selected_columns_global = []
current_progress = 0
app.secret_key = 'your_secret_key'

# Flask 使用裝飾器來定義路由，告訴 Flask，當用戶訪問 '/' 路徑時，執行下面的函數
# 顯示主畫面 (index.html)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """
    處理檔案上傳
    1. 檢查是否有文件被上傳
    2. 儲存上傳的文件到指定目錄
    3. 回傳上傳文件的檔名
    """
    if 'file' not in request.files:
        # HTML 中用 <input type="file"> 上傳文件，可以透過 request.files 訪問
        return jsonify({"error": "No file part"})
        # jonify: 將 Python 列表轉換為 JSON 格式。 web 開發中，JSON 是一種常見的資料交換格式
    file = request.files['file']
    # 檢查是否選擇了檔案
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    filename = file.filename
    # 檢查指定路徑是否存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    # 儲存上傳的檔案
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Structure the uploaded CSV
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    structured_df = structure_csv(file_path)
    structured_df.to_csv('structured.csv', index=False)

    # app.config['UPLOAD_FOLDER']代表檔案上傳的目錄。
    return jsonify({'filename': filename})

# @app.route('/columns', methods=['POST'])
# def columns():
#     """
#     得到上傳 CSV 文件的所有cloumn名
#     1. 從請求中獲取檔名
#     2. 使用 pandas 讀取 CSV 文件
#     3. 回傳文件中的所有cloumn名
#     """
#     # 從請求中獲取檔名
#     filename = request.json.get('filename')
#     # 檢查 filename 是否存在，如果沒有檔名，回傳錯誤
#     if not filename:
#         return jsonify({"error": "No filename provided"})
#     # 組合完整的文件路徑，將上傳文件夾的路徑app.config['UPLOAD_FOLDER']和上傳的文件名filename組合
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     # 檢查文件是否存在
#     if not os.path.exists(file_path):
#         return jsonify({"error": "File not found"})
#     # 用 pandas 讀取 CSV 
#     df = pd.read_csv(file_path)
#     # 回傳文件中的所有cloumn名，一個包含所有列名的list
#     return jsonify({"columns": df.columns.tolist()})

@app.route('/columns', methods=['POST'])
def columns():
    try:
        df = pd.read_csv('structured.csv')
        columns = df.columns.tolist()
        # print(df)
        return jsonify({"columns": df.columns.tolist()})
    except Exception as e:
        return jsonify(error=str(e))
    
@app.route('/process-data', methods=['POST'])
def process_data():
    """
    處理上傳的 CSV 文件的數據
    1. 從請求中獲取檔名和用戶選擇的cloumn
    2. 依據用戶選擇的操作，對數據進行預處理
    3. 保存處理後的數據到新的 CSV 文件
    4. 回傳處理後的數據
    """
    global current_progress
    global selected_columns_global
    # 從請求中獲取選擇的cloumn，getlist()
    # 當通過表單船送數據時，這些數據可以通過 request.form 訪問
    selected_columns_global = request.form.getlist('columns')
    try:
        # 從請求中獲取檔名
        filename = request.form.get('filename')
        # 檢查 filename 是否存在，如果沒有檔名，回傳錯誤
        if not filename:
            print("Filename not provided.")
            return jsonify({"error": "Filename not provided"})
        print(f"Processing file: {filename}")
        # 組合完整的文件路徑
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'structured.csv')
        # 檢查文件是否存在
        if not os.path.exists(file_path):
            print("File not found.")
            return jsonify({"error": "File not found"})
        # 從請求中獲取使用者選擇的cloumn
        selected_columns = request.form.getlist('columns')
        print(f"Selected columns: {selected_columns}")
        # 從請求中獲取使用者選擇的操作
        operations = request.form.getlist('operations')
        print(f"Selected operations: {operations}")
        # 初始化Preprocessing class
        # 使用class功能時，要創建class的實例。這個過程稱為初始化
        preprocessing = Preprocessing(file_path, selected_columns)
        # 獲取操作的順序
        # 字典生成式(dict comprehension)，會產生一個新的字典***
        # request.form[f'order_{op}'] 從請求的表單獲取以 order_ 開頭，後接 op 名稱的值
        operations_order = {op: int(request.form[f'order_{op}']) for op in operations}
        sorted_operations = sorted(operations_order, key=operations_order.get)
        print(f"Operations order: {sorted_operations}")
        # 設定進度條
        num_operations = len(sorted_operations)
        progress_increment = 100.0 / num_operations if num_operations else 0
        # 根據選擇的操作進行預處理
        for operation in sorted_operations:
            print(f"Applying operation: {operation}")
            if operation == 'remove_punctuation':
                preprocessing.punctuation()
                current_progress += progress_increment
            elif operation == 'convert_lowercase':
                preprocessing.lowercase()
                current_progress += progress_increment
            elif operation == 'remove_stopwords':
                preprocessing.stopwords()
                current_progress += progress_increment
            elif operation == 'remove_spaces':
                preprocessing.spaces()
                current_progress += progress_increment
        # 保存處理後的數據
        # 使用 pandas 的 to_csv() 函數將處理後的數據存文件中
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "preprocessed.csv")
        preprocessing.df_input.to_csv(processed_file_path, index=False)
        print("Data processed successfully.")
        # 限制進度條的最大值
        current_progress = min(100, current_progress)
        # 返回處理後的數據
        # to_html() 是 pandas DataFrame 的方法，將 DataFrame 轉換為 HTML 表格
        return preprocessing.df_input[selected_columns].to_html()
    # Python 的異常處理機制，try-except 語句用於捕獲和處理錯誤
    # 如果在 try 的代碼出現錯誤，則執行會跳到相應的 except 塊
    # as e 是將捕獲的異常賦值給變數 e，jsonify() 函數建立 JSON 格式的回應，其中包含錯誤訊息
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)})

@app.route('/download-processed-csv')
def download_processed():
    """
    讓使用者下載前處理後的文件
    1. 使用 Flask 的 send_from_directory 函數將 'preprocessed.csv' 文件發送給使用者
    """
    # send_from_directory(檔案路徑, 檔案名稱, as_attachment=True)
    # as_attachment=True會作為附件傳送，當使用者訪問路由時，瀏覽器會下載文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'preprocessed.csv', as_attachment=True)

@app.route('/get-progress', methods=['GET'])
def get_progress():
    """
    獲取當前數據處理的進度
    1. 使用全域變數 current_progress 獲取當前的進度
    2. 返回進度值
    """
    global current_progress
    return jsonify({"progress": current_progress})

@app.route('/compute-word-frequency', methods=['POST'])
def compute_word_frequency():
    """
    計算每個subject_id的字頻
    1. 讀取已經預處理的數據
    2. 對每個'subject_id' 進行處理
    3. 使用 `process_subject` 函數計算字頻
    4. 返回成功或錯誤消息
    """
    output_path = os.path.join(UPLOAD_FOLDER, 'frequency.csv')
    try:
        df = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'preprocessed.csv'))
        # Python 中，想在一個函數內修改一個全域變數的值，需要函數中使用 global 關鍵字來聲明該變數
        global selected_columns_global
        selected_columns = selected_columns_global
        # unique() 函數的return包含column中所有不重複的值，能夠對每個單獨的 subject_id 進行操作
        for subject_id in df['subject_id'].unique():
            process_subject(df, subject_id, UPLOAD_FOLDER, selected_columns)  # Pass selected columns to the function
        return jsonify(success=True)
    except Exception as e:
        # 在字串前加上 f 或 F 並使用 {} 包裹變數，可直接將變數或表達式的值插入到字串中
        # f"Error: {str(e)}" 會創建一個新的字串，其中 str(e) 的結果會插入到 Error: 之後
        # 假設 e 的值是 ValueError ，內容是 "Invalid value"，則 f"Error: {str(e)}" 是 "Error: Invalid value
        error_message = f"Error: {str(e)}"
        print(error_message)
        return jsonify(success=False, error=error_message)


@app.route('/download-word-frequency-result')
def download_word_frequency_result():
    """
    讓使用者下載字頻結果的CSV
    1. 使用 Flask 的 send_from_directory 函數將 'word_frequency_result.csv' 文件發送給使用者。
    """
    # send_from_directory(檔案路徑, 檔案名稱, as_attachment=True)
    # as_attachment=True會作為附件傳送，當使用者訪問路由時，瀏覽器會下載文件
    return send_from_directory(UPLOAD_FOLDER, 'word_frequency_result.csv', as_attachment=True)

@app.route('/generate_wordcloud', methods=['GET'])
def generate_wordcloud_route():
    """
    產生文字雲圖片並返回其路徑
    1. 獲取全域變數 selected_columns_global
    2. 調用 generate_wordcloud 函數產生文字雲圖片
    3. 將產生的圖片路徑保存到 session 中
    4. 返回成功或錯誤消息
    """
    try:
        global selected_columns_global
        selected_columns = selected_columns_global
        wordcloud_paths = generate_wordcloud(selected_columns)

        # 檢查 wordcloud_paths 是否為 None 或不是列表
        if not isinstance(wordcloud_paths, list):
            return jsonify({"status": "error", "message": "Failed to generate wordclouds"})

        # 列表解析(list comprehension)，允許用表達式產生列表***
        # [expression for item in iterable]，遍歷 iterable 中的每一個元素，並對每個元素執行 expression，然後將結果放入新的列表中
        relative_urls = ["/uploads/" + os.path.basename(path) for path in wordcloud_paths]
        # 將 wordcloud_paths 儲存到 Flask 的 session 
        session["wordcloud_paths"] = wordcloud_paths
        return jsonify({
            "status": "success",
            "wordcloud_paths": relative_urls
        })
    except Exception as e:
        # "status" 的值為 "error"，而 "message" 的值為異常的文字描述
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download_wordcloud', methods=['GET'])
def download_wordcloud():
    """讓使用者下載指定的文字雲圖片
    1. 從請求參數中獲取文字雲圖片的路徑
    2. 檢查文字雲圖片是否存在
    3. 使用 Flask 的 send_from_directory 函數將文字雲圖片發送給使用者
    """
    # request.args.get()從請求參數中獲取文字雲的圖片路徑
    wordcloud_path = request.args.get("path")
    # 檢查是否指定文字雲圖片路徑，如果沒有，返回 400 錯誤
    # HTTP 400 錯誤是一個標準的 HTTP 錯誤碼，表示請求無效或格式不正確
    if wordcloud_path is None:
        return "No wordcloud specified", 400
    # Extracting the filename from the path.
    wordcloud_name = os.path.basename(wordcloud_path)
    # 使用 Flask 的 send_from_directory 函數將文字雲圖片發送給使用者
    # 當as_attachment=True會作為附件傳送，當使用者訪問路由時，瀏覽器會下載文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], wordcloud_name, as_attachment=True)

# @app.route('/upload', methods=['POST']) 是用於處理上傳操作的，只在使用者上傳文件時觸發
# @app.route('/uploads/<filename>') 是用於直接訪問某個特定文件，可能在多個地方被使用
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    讓使用者訪問上傳的文件。
    1. 使用 Flask 的 send_from_directory 函數將指定的文件發送給使用者
    """
    # 第一個參數是文件路徑(取自 app.config['UPLOAD_FOLDER'])，第二個參數是文件名(從函數參數 filename 獲取)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # 啟動 Flask 
    # debug=True，當程式碼更改時，伺服器會自動重新啟動
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
    # 將 Flask 應用的運行端口更改為 8080
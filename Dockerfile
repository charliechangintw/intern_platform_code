# text_processing_app
# 使用官方的 Python Images作為基礎Images，不需從頭開始安裝和配置 Python
FROM python:3.8

# 設定後續命令的工作目錄
# 在 Dockerfile 中運行其他命令(如 COPY 或 RUN)，將在這個目錄中執行
WORKDIR /app

# 安裝依賴項，通常指應用程式需要運行的其他軟件或程式庫
# pip freeze > requirements.txt，透過指令自動產生requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# 複製應用程式到容器中
# 第一個 . 表示當前目錄(Dockerfile 的目錄)，第二個 . 表示複製到容器的目的地(WORKDIR)
COPY . .

# 啟動應用程式
CMD ["python", "app.py"]


import pandas as pd
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
# re: 正則表達式的相關功能。string: 提供常見的字串操作功能

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')

class Preprocessing:
    # Preprocessing class的初始化函數
    def __init__(self, filename, processColumns):
        self.filename = filename
        self.processColumns = processColumns
        self.df_input = pd.read_csv(self.filename)
        # 用 pandas 的 read_csv 函數讀取 CSV 文件並將其存儲為一個 DataFrame
    
    def lowercase(self):
        # 遍歷所有需要進行處理的column
        for column in self.processColumns:
            # astype()將column中的元素轉換為指定的類型，這裡換成字串
            # .str.lower()將字串轉換為小寫
            self.df_input[column] = self.df_input[column].astype(str).str.lower()  

    def punctuation(self):
        # 建一個translator翻譯表，定義如何替換字串中的字，將所有標點符號轉換為空字符串
        # string.punctuation 為包含所有標點符號的字串，如：!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`
        translator = str.maketrans('', '', string.punctuation)
        for column in self.processColumns:
            # translate() 是Python中字串的方法，使用提供的翻譯表來替換字串中的字
            self.df_input[column] = self.df_input[column].astype(str).str.translate(translator)

    def spaces(self):
        for column in self.processColumns:
            # 正則表達式 r'\s+'，找到文本中的一個或重複的空白，替換成單個空格
            # str.replace(old, new)，用於替換字串中的一部分內容
            self.df_input[column] = self.df_input[column].astype(str).str.replace(r'\s+', ' ')
            
    def stopwords(self):
        # NLP中，"token" 通常指的是文本中的單個單詞或標點符號，tokenization有助於進一步分析每個單詞的意義
        def remove_stopwords(text): # text代表要處理的文本
            text = str(text) # 確保 text 是字串格式
            # 使用 spacy 的 nlp 函數將文本轉換為一系列的 tokens，doc 是一個包含這些 tokens 的列表
            doc = nlp(text)
            # 一個過濾機制，將文本中的所有停用詞過濾掉，只保留其他詞
            # 對於每個 token，檢查 token.is_stop，如果 token.is_stop 為 True，則該詞是一個停用詞，不會被加入到最終的列表中
            # 使用 join 方法將這個列表中的所有詞連接起來，詞之間用空格隔開
            return " ".join([token.text for token in doc if not token.is_stop])
        for processColumn in self.processColumns:
            # fillna 方法替換 DataFrame 中的缺失值，如 NaN 或 None，這邊是替換成空字串 ('')
            self.df_input[processColumn] = self.df_input[processColumn].fillna('')
            # lambda 是 Python 中用於創建匿名函數的關鍵字，匿名函數是指沒有名稱的函數
            # apply 方法對 DataFrame 指定的column(processColumn)中的每一行應用一個函數
            # 對於該column中的每一個值(也就是每一個文本)，都會執行 remove_stopwords 函數，將文本中的停用詞刪除
            self.df_input[processColumn] = self.df_input[processColumn].apply(lambda x: remove_stopwords(x))
        

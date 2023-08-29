import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import imageio
import matplotlib.gridspec as gridspec
from collections import Counter
from wordcloud import WordCloud
import os
from config import UPLOAD_FOLDER
# matplotlib：Python 2D 繪圖庫。imageio：圖像讀取和寫入

def generate_wordcloud(selected_columns):
    """
    Generate word clouds for the given columns from the frequency.csv file.
    
    Parameters:
    - selected_columns (list): A list of column names from the frequency.csv for which word clouds need to be generated.
    
    Returns:
    - list: A list of paths where the generated word cloud images are saved.
    """
    freq_csv_path = os.path.join(UPLOAD_FOLDER, 'frequency.csv')
    df = pd.read_csv(freq_csv_path)
    # 初始化一個空列表 存文字雲圖的路徑
    wordcloud_image_paths = []
    # 遍歷每一個選擇的column
    for column in selected_columns:
        # 為每一column創建一個獨特的圖片文件名
        image_path = os.path.join(UPLOAD_FOLDER, f"wordcloud_{column}.png")
        # df['word']從 DataFrame df 中取出一列名為 'word' 的資料
        # zip 函數將兩列資料組合在一起，zip([1, 2, 3], ['a', 'b', 'c']) 會產生配對 (1, 'a'), (2, 'b') 和 (3, 'c')
        # dict 函數將這些配對資料轉換成一個字典
        word_freq = dict(zip(df['word'], df[column]))

        # Removing words with a frequency of zero
        word_freq = {key: value for key, value in word_freq.items() if value != 0}  

        # 用 WordCloud 的 generate_from_frequencies 方法產生文字雲
        wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
        # 將產生的文字雲存為圖片
        wc.to_file(image_path)
        # 在列表中添加新產生的圖片路徑
        wordcloud_image_paths.append(image_path)
    return wordcloud_image_paths


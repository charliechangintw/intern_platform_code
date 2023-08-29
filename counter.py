import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

def count_words(text):
    # text.split() 將字串 text 按空白字符分割成一個列表，列表中的每一項都是一個詞
    # Counter()：從 collections 導入，計算列表中每個詞的出現次數
    return Counter(text.split())

def process_subject(df, subject_id, output_path, selected_columns):
    print("Starting process_subject function...")
    try:
        # 初始化一個空的 DataFrame
        result_df = pd.DataFrame()
        print(f"Processing for columns: {selected_columns}")

        for column in selected_columns:
            # .dropna() 會刪除中column的所有 NaN(不是數字)值
            # 對於每一個選定的column，組合該column的所有文本
            combined_text = " ".join(df[column].dropna())
            word_freq = count_words(combined_text)
            # pd.DataFrame(...) 將列表轉換為 DataFrame，columns=['word', column] 定義 DataFrame 的column名稱
            column_df = pd.DataFrame(word_freq.items(), columns=['word', column])
            # 檢查 result_df 是否為空
            if result_df.empty:
                result_df = column_df
            else:
                # pd.merge(...) 合併 result_df 和 column_df
                # result_df 包含先前column的字頻數據，而 column_df 包含當前column的數據
                # on='word'：merge 函數按照 'word' 列來合併兩個 DataFrame
                # how='outer'：外部合併
                result_df = pd.merge(result_df, column_df, on='word', how='outer')
        
        # 將所有 NaN 值替換為 0，因為某些詞可能只在某些column中出現
        result_df = result_df.fillna(0)
        # 把最終的詞頻結果存為 frequency.csv
        result_df.to_csv(os.path.join(output_path, 'frequency.csv'), index=False)
        # print result_df 的前五行幫助檢查
        # head() 返回 DataFrame 的前 n 行，預設 5 行
        print('Final result DataFrame:', result_df.head())
    except Exception as e:
        print(f"Error occurred in process_subject: {str(e)}")
        raise e  

def save_results_to_csv(result_df, output_path):
    """
    Save the provided DataFrame to a CSV file.
    
    Parameters:
    - result_df (pd.DataFrame): The DataFrame to save.
    - output_path (str): The path where the CSV file should be saved.
    
    Returns:
    None
    """
    result_df.to_csv(output_path, index=False)


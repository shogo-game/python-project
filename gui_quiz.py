# 1. 必要な道具箱を全部インポートするニャ
import tkinter as tk
import pandas as pd

# --- 設定はここニャ！ ---
EXCEL_FILE_NAME = "理論練習テキスト1.xlsx" 
QUESTION_COLUMN = "問題"
ANSWER_COLUMN = "解答＆ポイント"
HINT_COLUMN = "ヒント"
# --------------------

# --- Excelを読み込む専門の呪文（関数）を作るニャ ---
def load_questions_from_excel():
    """Excelファイルを読み込んで、データ表（df）を返すニャ"""
    try:
        df = pd.read_excel(EXCEL_FILE_NAME)
        # 成功したら、読み込んだデータ表を返すニャ
        return df
    except FileNotFoundError:
        # もし失敗したら、エラーメッセージを出して終了するニャ
        question_label.config(text=f"エラー: {EXCEL_FILE_NAME} が見つからないニャ！")
        return None

# --- ボタンが押された時の呪文（関数）ニャ ---
def show_next_question():
    """新しい問題を表示するための関数ニャ"""
    if question_df is not None:
        # データ表からランダムに1行選ぶニャ
        random_row = question_df.sample(n=1)
        
        # その行から問題テキストを取り出すニャ
        question_text = random_row[QUESTION_COLUMN].iloc[0]
        
        # ラベルの文字を、選ばれた問題に書き換えるニャ
        question_label.config(text=question_text)


# --- ここからがアプリ本体の組み立てだニャ ---

# まずはExcelを読み込むニャ
question_df = load_questions_from_excel()

# アプリのメインとなる「ウィンドウ」を作るニャ
window = tk.Tk()
window.title("財務諸表論 - ランダム問題マシーン 🐾")
window.geometry("700x500")

# ウィンドウに表示するラベル部品を作るニャ
question_label = tk.Label(window, text="下のボタンを押してニャ！", font=("Helvetica", 14), wraplength=680)
question_label.pack(pady=20)

# ウィンドウに表示するボタン部品を作るニャ
next_button = tk.Button(window, text="次の問題へ", command=show_next_question)
next_button.pack()

# ウィンドウを表示し続けるニャ！
window.mainloop()
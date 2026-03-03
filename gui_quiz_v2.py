import tkinter as tk
from tkinter import ttk
import pandas as pd

# --- 設定はここニャ！ ---
EXCEL_FILE_NAME = "理論練習テキスト1.xlsx" 
QUESTION_COLUMN = "問題"
ANSWER_COLUMN = "解答＆ポイント"
HINT_COLUMN = "ヒント"
# --------------------

# グローバル変数として、選ばれた行を保存する箱を用意するニャ
current_question_row = None

def open_quiz_window(sheet_name):
    """クイズ画面（新しいウィンドウ）を開くための呪文ニャ"""
    
    # --- まずはExcelから、選ばれたシートのデータを読み込むニャ ---
    try:
        question_df = pd.read_excel(EXCEL_FILE_NAME, sheet_name=sheet_name)
    except Exception as e:
        # もしエラーが出たら、クイズ画面にエラーメッセージを出すニャ
        quiz_window = tk.Toplevel(start_window)
        quiz_window.title("エラーニャ！")
        error_label = tk.Label(quiz_window, text=f"エラー: {e}")
        error_label.pack(pady=20, padx=20)
        return

    # --- ここからがクイズ画面の組み立てだニャ ---
    quiz_window = tk.Toplevel(start_window)
    quiz_window.title(f"{sheet_name} - ランダム問題マシーン 🐾")
    quiz_window.geometry("700x500")

    # --- 部品（ウィジェット）を定義するニャ ---
    question_label = tk.Label(quiz_window, text="下のボタンを押してニャ！", font=("Helvetica", 14), wraplength=680, justify="left")
    answer_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=680, justify="left", fg="blue")
    
    # --- ボタンが押された時の呪文（内部関数）を定義するニャ ---
    def show_next_question():
        global current_question_row
        random_row = question_df.sample(n=1)
        current_question_row = random_row
        question_text = random_row[QUESTION_COLUMN].iloc[0]
        question_label.config(text=question_text)
        answer_label.config(text="") # 答えを隠すニャ

    def show_answer():
        if current_question_row is not None:
            answer_text = current_question_row[ANSWER_COLUMN].iloc[0]
            answer_label.config(text=f"【解答】\n{answer_text}")

    # --- 部品を配置するニャ ---
    question_label.pack(pady=20, padx=10, fill="x")
    
    # ボタンを横に並べるためのフレームを作るニャ
    button_frame = tk.Frame(quiz_window)
    button_frame.pack(pady=10)

    answer_button = tk.Button(button_frame, text="答えを見る", command=show_answer)
    answer_button.pack(side="left", padx=10)

    next_button = tk.Button(button_frame, text="次の問題へ", command=show_next_question)
    next_button.pack(side="left", padx=10)
    
    answer_label.pack(pady=20, padx=10, fill="x")


def start_quiz():
    """スタートボタンが押された時に実行される呪文ニャ"""
    selected_sheet = sheet_selector.get()
    if not selected_sheet or "見つからない" in selected_sheet:
        return
        
    # 科目選択ウィンドウを隠すニャ
    start_window.withdraw()
    # 新しいクイズウィンドウを開くニャ
    open_quiz_window(selected_sheet)


# --- ここからがアプリ本体の組み立てだニャ ---
start_window = tk.Tk()
start_window.title("クイズの科目を選んでニャ！ 🐾")
start_window.geometry("400x200")

try:
    excel_file = pd.ExcelFile(EXCEL_FILE_NAME)
    sheet_names = excel_file.sheet_names
except FileNotFoundError:
    sheet_names = [f"{EXCEL_FILE_NAME} が見つからないニャ！"]

info_label = tk.Label(start_window, text="どの科目に挑戦するニャ？", font=("Helvetica", 14))
info_label.pack(pady=20)

sheet_selector = ttk.Combobox(start_window, values=sheet_names, state="readonly", font=("Helvetica", 12))
if sheet_names:
    sheet_selector.current(0)
sheet_selector.pack(pady=10)

start_button = tk.Button(start_window, text="この科目でスタート！", font=("Helvetica", 12), command=start_quiz)
start_button.pack(pady=20)

start_window.mainloop()
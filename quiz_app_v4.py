import tkinter as tk
from tkinter import ttk
import pandas as pd
import random # シャッフルするために新しい仲間を呼ぶニャ！

# --- 設定はここニャ！ ---
EXCEL_FILE_NAME = "理論練習テキスト1.xlsx" # 君のファイル名に合わせたニャ！
QUESTION_COLUMN = "問題"
ANSWER_COLUMN = "解答＆ポイント"
HINT_COLUMN = "ヒント"
# --------------------

# グローバル変数（共有の箱）をいくつか用意するニャ
current_question_row = None
shuffled_indices = []
current_position = -1

def open_quiz_window(sheet_name):
    """クイズ画面（新しいウィンドウ）を開くための呪文ニャ"""
    
    global shuffled_indices, current_position
    
    try:
        question_df = pd.read_excel(EXCEL_FILE_NAME, sheet_name=sheet_name)
        # ★★★ ここで問題の順番をシャッフルするニャ！ ★★★
        shuffled_indices = list(question_df.index)
        random.shuffle(shuffled_indices)
        current_position = -1 # 位置をリセット
    except Exception as e:
        quiz_window = tk.Toplevel(start_window)
        quiz_window.title("エラーニャ！")
        error_label = tk.Label(quiz_window, text=f"エラー: {e}")
        error_label.pack(pady=20, padx=20)
        return

    quiz_window = tk.Toplevel(start_window)
    quiz_window.title(f"{sheet_name} - ランダム問題マシーン 🐾")
    quiz_window.geometry("700x600")

    # --- 部品（ウィジェット）を定義するニャ ---
    question_label = tk.Label(quiz_window, text="下のボタンを押してニャ！", font=("Helvetica", 14), wraplength=680, justify="left")
    your_answer_label = tk.Label(quiz_window, text="【君の答え】", font=("Helvetica", 12, "bold"))
    your_answer_text = tk.Text(quiz_window, height=5, font=("Helvetica", 12))
    
    # ★★★ ヒント用と答え用のラベルを２つに分けるニャ！ ★★★
    hint_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=680, justify="left", fg="green")
    answer_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=680, justify="left", fg="blue")
    
    # --- ボタンが押された時の呪文（内部関数）を定義するニャ ---
    def show_next_question():
        global current_question_row, current_position
        
        # ★★★ シャッフルしたリストの次の問題に進むニャ ★★★
        current_position += 1
        if current_position >= len(shuffled_indices):
            # 全部見終わったら、もう一度シャッフルするニャ！
            random.shuffle(shuffled_indices)
            current_position = 0
            question_label.config(text="全問終了！お疲れ様でした！")
            hint_label.config(text="")
            answer_label.config(text="")
            your_answer_text.delete("1.0", "end")
            return

        question_index = shuffled_indices[current_position]
        random_row = question_df.loc[[question_index]]
        current_question_row = random_row
        
        question_text = random_row[QUESTION_COLUMN].iloc[0]
        question_label.config(text=question_text)
        
        # ★★★ ヒントと答えの両方を隠すニャ ★★★
        hint_label.config(text="")
        answer_label.config(text="")
        your_answer_text.delete("1.0", "end")

    def show_hint():
        if current_question_row is not None:
            # iloc[0]の前に.valuesをつけると、より安全になることがあるニャ
            hint_text = current_question_row[HINT_COLUMN].values[0]
            # ★★★ ヒント専用ラベルに表示ニャ！ ★★★
            hint_label.config(text=f"【ヒント】\n{hint_text}")

    def show_answer():
        if current_question_row is not None:
            answer_text = current_question_row[ANSWER_COLUMN].values[0]
            # ★★★ 答え専用ラベルに表示ニャ！ ★★★
            answer_label.config(text=f"【解答】\n{answer_text}")

    # --- 部品を配置するニャ ---
    question_label.pack(pady=10, padx=10, fill="x")
    your_answer_label.pack(pady=(10, 0))
    your_answer_text.pack(pady=5, padx=10, fill="x")
    button_frame = tk.Frame(quiz_window)
    button_frame.pack(pady=10)
    hint_button = tk.Button(button_frame, text="ヒントを見る", command=show_hint)
    hint_button.pack(side="left", padx=10)
    answer_button = tk.Button(button_frame, text="答えを見る", command=show_answer)
    answer_button.pack(side="left", padx=10)
    next_button = tk.Button(button_frame, text="次の問題へ", command=show_next_question)
    next_button.pack(side="left", padx=10)
    
    # ★★★ ２つのラベルを配置ニャ！ ★★★
    hint_label.pack(pady=10, padx=10, fill="x")
    answer_label.pack(pady=10, padx=10, fill="x")


def start_quiz():
    """スタートボタンが押された時に実行される呪文ニャ"""
    selected_sheet = sheet_selector.get()
    if not selected_sheet or "見つからない" in selected_sheet:
        return
        
    start_window.withdraw()
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
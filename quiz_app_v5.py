import tkinter as tk
from tkinter import ttk
import pandas as pd
import random

# --- 設定はここニャ！ ---
EXCEL_FILE_NAME = "理論練習テキスト1.xlsx"
QUESTION_COLUMN = "問題"
ANSWER_COLUMN = "解答＆ポイント"
HINT_COLUMN = "ヒント"
# --------------------

# --- グローバル変数 ---
current_question_row = None
shuffled_indices = []
current_position = -1
question_df = None

def open_quiz_window(sheet_name, mode):
    """クイズ画面を開く呪文ニャ。モードも受け取るニャ！"""
    
    global shuffled_indices, current_position, question_df
    
    try:
        question_df = pd.read_excel(EXCEL_FILE_NAME, sheet_name=sheet_name)
        if mode == "random":
            # ランダムモードなら、順番をシャッフルするニャ！
            shuffled_indices = list(question_df.index)
            random.shuffle(shuffled_indices)
        current_position = -1
    except Exception as e:
        # (エラー処理は省略ニャ)
        return

    quiz_window = tk.Toplevel(start_window)
    quiz_window.title(f"{sheet_name} - {mode}モード 🐾")
    quiz_window.geometry("700x600")

    question_label = tk.Label(quiz_window, text="下のボタンを押してニャ！", font=("Helvetica", 14), wraplength=680, justify="left")
    your_answer_label = tk.Label(quiz_window, text="【君の答え】", font=("Helvetica", 12, "bold"))
    your_answer_text = tk.Text(quiz_window, height=5, font=("Helvetica", 12))
    hint_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=680, justify="left", fg="green")
    answer_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=680, justify="left", fg="blue")
    
    def show_next_question():
        global current_question_row, current_position
        
        current_position += 1
        
        # ★★★ モードによって動きを変えるニャ！ ★★★
        if mode == "random":
            if current_position >= len(shuffled_indices):
                random.shuffle(shuffled_indices)
                current_position = 0
                question_label.config(text="全問終了！お疲れ様でした！")
                # (ラベルをクリアする処理は省略ニャ)
                return
            question_index = shuffled_indices[current_position]
        else: # "sequential"モードの場合
            if current_position >= len(question_df):
                #current_position = 0 修正済！
                current_position = -1 # ← ここを-1に変えるニャ！
                question_label.config(text="全問終了！最初の問題に戻るニャ！")
                # (ラベルをクリアする処理は省略ニャ)
                return
            question_index = current_position
        
        # .locじゃないとエラーになることがあるので修正ニャ
        random_row = question_df.iloc[[question_index]]
        current_question_row = random_row
        
        question_text = random_row[QUESTION_COLUMN].values[0]
        question_label.config(text=question_text)
        
        hint_label.config(text="")
        answer_label.config(text="")
        your_answer_text.delete("1.0", "end")

    def show_hint():
        if current_question_row is not None:
            hint_text = current_question_row[HINT_COLUMN].values[0]
            hint_label.config(text=f"【ヒント】\n{hint_text}")

    def show_answer():
        if current_question_row is not None:
            answer_text = current_question_row[ANSWER_COLUMN].values[0]
            answer_label.config(text=f"【解答】\n{answer_text}")

    # (部品の配置部分は省略ニャ)
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
    hint_label.pack(pady=10, padx=10, fill="x")
    answer_label.pack(pady=10, padx=10, fill="x")


def start_quiz():
    selected_sheet = sheet_selector.get()
    # ★★★ 選ばれたモードを取得するニャ！ ★★★
    selected_mode = mode_var.get()
    
    if not selected_sheet or "見つからない" in selected_sheet:
        return
        
    start_window.withdraw()
    open_quiz_window(selected_sheet, selected_mode)

# --- ここからが科目選択ウィンドウの組み立てだニャ ---
start_window = tk.Tk()
start_window.title("クイズの科目を選んでニャ！ 🐾")
# ★★★ この一行を追加するニャ！ ★★★
start_window.state('zoomed')

try:
    excel_file = pd.ExcelFile(EXCEL_FILE_NAME)
    sheet_names = excel_file.sheet_names
except FileNotFoundError:
    sheet_names = [f"{EXCEL_FILE_NAME} が見つからないニャ！"]

info_label = tk.Label(start_window, text="どの科目に挑戦するニャ？", font=("Helvetica", 14))
info_label.pack(pady=10)
sheet_selector = ttk.Combobox(start_window, values=sheet_names, state="readonly", font=("Helvetica", 12))
if sheet_names:
    sheet_selector.current(0)
sheet_selector.pack(pady=5)

# ★★★ ここからがモード選択の新しい部品だニャ！ ★★★
mode_frame = tk.Frame(start_window)
mode_frame.pack(pady=10)

# モードを保存するための特別な変数ニャ
mode_var = tk.StringVar(value="random") 

random_button = tk.Radiobutton(mode_frame, text="ランダム出題", variable=mode_var, value="random", font=("Helvetica", 10))
random_button.pack(side="left", padx=10)

sequential_button = tk.Radiobutton(mode_frame, text="順番通り出題", variable=mode_var, value="sequential", font=("Helvetica", 10))
sequential_button.pack(side="left", padx=10)
# ★★★ ここまで ★★★

start_button = tk.Button(start_window, text="この科目でスタート！", font=("Helvetica", 12), command=start_quiz)
start_button.pack(pady=10)

start_window.mainloop()
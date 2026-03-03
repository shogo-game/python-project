import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
import re

# --- 設定はここニャ！ ---
EXCEL_FILE_NAME = r"C:\Users\shogo\OneDrive\資格の大原税理士試験デスクトップpc用\理論練習テキスト1.xlsx"

# ★★★ 新しいExcelの列名に合わせて設定を変えたニャ！ ★★★
DAI_COLUMN = "大項目"
CHU_COLUMN = "中項目"
QUESTION_COLUMN = "問題"
ANSWER_COLUMN = "解答"     # ← 「解答＆ポイント」から「解答」だけにしたニャ
POINT_COLUMN = "ポイント"   # ← 新しく追加する「ポイント」列だニャ
# --------------------

# --- グローバル変数 ---
current_question_row = None
shuffled_indices = []
current_position = -1
question_df = None

def open_quiz_window(sheet_name, mode):
    global shuffled_indices, current_position, question_df
    
    try:
        # Excelを読み込むニャ
        question_df = pd.read_excel(EXCEL_FILE_NAME, sheet_name=sheet_name)
        # ★★★ 魔法の1行！ 空っぽのセル(NaN)を、ただの空文字("")に変えておくニャ！ ★★★
        question_df = question_df.fillna("") 
        
        if mode == "random":
            shuffled_indices = list(question_df.index)
            random.shuffle(shuffled_indices)
        current_position = -1
    except Exception as e:
        print(f"エラーだニャ: {e}") 
        return

    quiz_window = tk.Toplevel(start_window)
    quiz_window.title(f"{sheet_name} - {mode}モード 🐾")
    quiz_window.state('zoomed')

    # --- 部品（ウィジェット）を定義するニャ ---
    question_label = tk.Label(quiz_window, text="下のボタンを押してニャ！", font=("Helvetica", 16, "bold"), wraplength=1200, justify="left")
    your_answer_label = tk.Label(quiz_window, text="【君の答え】", font=("Helvetica", 12, "bold"))
    your_answer_text = tk.Text(quiz_window, height=5, font=("Helvetica", 12))
    hint_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=1200, justify="left", fg="green")
    answer_label = tk.Label(quiz_window, text="", font=("Helvetica", 12), wraplength=1200, justify="left", fg="blue")
    
    # --- ボタンが押された時の呪文（内部関数） ---
    def show_next_question():
        global current_question_row, current_position
        current_position += 1
        
        if mode == "random":
            if current_position >= len(shuffled_indices):
                random.shuffle(shuffled_indices); current_position = 0
                question_label.config(text="全問終了！もう一度シャッフルしたニャ！")
                hint_label.config(text=""); answer_label.config(text="")
                return
            question_index = shuffled_indices[current_position]
        else:
            if current_position >= len(question_df):
                current_position = -1; 
                question_label.config(text="全問終了！最初の問題に戻るニャ！")
                hint_label.config(text=""); answer_label.config(text="")
                return
            question_index = current_position
            
        random_row = question_df.iloc[[question_index]]
        current_question_row = random_row
        
        # ★★★ 改良ポイント！大項目・中項目・問題を合体させるニャ！ ★★★
        dai_text = str(random_row[DAI_COLUMN].values[0])
        chu_text = str(random_row[CHU_COLUMN].values[0])
        q_text = str(random_row[QUESTION_COLUMN].values[0])
        
        # f-stringの魔法で合体ニャ！（\n は改行という意味だニャ）
        full_question_text = f"{dai_text}、{chu_text}\n\n{q_text}"
        
        question_label.config(text=full_question_text)
        hint_label.config(text="")
        answer_label.config(text="")
        your_answer_text.delete("1.0", "end")
        
    def show_hint():
        """ヒントを自動生成して表示するニャ！"""
        if current_question_row is not None:
            answer_text = str(current_question_row[ANSWER_COLUMN].values[0])
            
            # ★★★ ここが一番の改良ポイントニャ！ ★★★
            # 半角の [ ] の前に \ を置いて、ただの文字として認識させているニャ！
            hint_text = re.sub(r'\[.*?\]', '（　　　）', answer_text)
            
            hint_label.config(text=f"【ヒント】\n{hint_text}")

    def show_answer():
        """解答とポイントを表示するニャ！"""
        if current_question_row is not None:
            answer_text = str(current_question_row[ANSWER_COLUMN].values[0])
            point_text = str(current_question_row[POINT_COLUMN].values[0])
            
            # ▼▼▼ 新しく追加したお掃除魔法ニャ！ ▼▼▼
            # '[' を何もなし('')に置き換え、さらに ']' も何もなし('')に置き換えるニャ！
            answer_text = answer_text.replace('[', '').replace(']', '')
            # ▲▲▲ これでジャマなカッコが消え去るニャン！ ▲▲▲
            
            # 解答とポイントをきれいに並べるニャ
            display_text = f"【解答】\n{answer_text}"
            
            # ポイントが空っぽじゃない時だけ、下にポイントを付け足すニャ
            if point_text != "":
                display_text += f"\n\n【ポイント】\n{point_text}"
                
            answer_label.config(text=display_text)
    
    def go_back_to_start():
        quiz_window.destroy()
        start_window.deiconify()
        start_window.state('zoomed')

    # --- 部品を配置するニャ ---
    question_label.pack(pady=20, padx=10, fill="x") 
    your_answer_label.pack(pady=(10, 0))
    your_answer_text.pack(pady=5, padx=10, fill="x")
    button_frame = tk.Frame(quiz_window); button_frame.pack(pady=10)
    hint_button = tk.Button(button_frame, text="ヒントを見る", command=show_hint); hint_button.pack(side="left", padx=10)
    answer_button = tk.Button(button_frame, text="答えを見る", command=show_answer); answer_button.pack(side="left", padx=10)
    next_button = tk.Button(button_frame, text="次の問題へ", command=show_next_question); next_button.pack(side="left", padx=10)
    hint_label.pack(pady=10, padx=10, fill="x")
    answer_label.pack(pady=10, padx=10, fill="x")
    back_button = tk.Button(quiz_window, text="科目選択に戻る", command=go_back_to_start); back_button.pack(pady=20)


def start_quiz():
    selected_sheet = sheet_selector.get()
    selected_mode = mode_var.get()
    if not selected_sheet or "見つからない" in selected_sheet: return
    start_window.withdraw()
    open_quiz_window(selected_sheet, selected_mode)

# --- 科目選択ウィンドウ ---
start_window = tk.Tk()
start_window.title("クイズの科目を選んでニャ！ 🐾")
start_window.state('zoomed')
info_label = tk.Label(start_window, text="どの科目に挑戦するニャ？", font=("Helvetica", 14)); info_label.pack(pady=10)
try: excel_file = pd.ExcelFile(EXCEL_FILE_NAME); sheet_names = excel_file.sheet_names
except FileNotFoundError: sheet_names = [f"{EXCEL_FILE_NAME} が見つからないニャ！"]
sheet_selector = ttk.Combobox(start_window, values=sheet_names, state="readonly", font=("Helvetica", 12)); sheet_selector.pack(pady=5)
if sheet_names: sheet_selector.current(0)
mode_frame = tk.Frame(start_window); mode_frame.pack(pady=10)

# 1. 最初の状態(デフォルト)を "sequential" (順番通り) に変更するニャ！
mode_var = tk.StringVar(value="sequential") 

# 2. 先に「順番通り出題」のボタンを作って配置するニャ！(これで左側にくるニャ)
sequential_button = tk.Radiobutton(mode_frame, text="順番通り出題", variable=mode_var, value="sequential", font=("Helvetica", 10))
sequential_button.pack(side="left", padx=10)

# 3. 後から「ランダム出題」のボタンを作って配置するニャ！(これで右側にくるニャ)
random_button = tk.Radiobutton(mode_frame, text="ランダム出題", variable=mode_var, value="random", font=("Helvetica", 10))
random_button.pack(side="left", padx=10)

start_button = tk.Button(start_window, text="この科目でスタート！", font=("Helvetica", 12), command=start_quiz); start_button.pack(pady=10)
start_window.mainloop()
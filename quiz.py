# 必要な道具箱をインポートするニャ
import pandas as pd
import time

# --- ここから設定ニャ！ ---
# 君のExcelファイルの名前に書き換えてニャ
EXCEL_FILE_NAME = "理論練習テキスト1.xlsx" 
# Excelの列名をここに書くニャ（君のファイルに合わせてニャ！）
QUESTION_COLUMN = "問題"
ANSWER_COLUMN = "解答＆ポイント"
# --- 設定はここまでニャ！ ---


print("--- 資格試験☆ランダム一問一答マシーン ---")
print(f"'{EXCEL_FILE_NAME}'を読み込んでいるニャ…")

# Excelファイルを読み込むニャ
# もしエラーが出たら、ファイル名や列名が合っているか確認するニャン
try:
    df = pd.read_excel(EXCEL_FILE_NAME)
except FileNotFoundError:
    print(f"エラー: '{EXCEL_FILE_NAME}'が見つからないニャ！同じフォルダにあるか確認してニャ。")
    exit() # プログラムを終了するニャ

print("準備完了ニャ！いつでも始められるニャン！")
time.sleep(1) # 1秒待つニャ

# 「q」が入力されるまで、無限に問題を出し続けるニャ
while True:
    # ランダムに1行だけ選ぶ、pandasの魔法ニャ！
    question_row = df.sample(n=1)
    
    # 選ばれた行から、問題と答えのテキストを取り出すニャ
    question = question_row[QUESTION_COLUMN].iloc[0]
    answer = question_row[ANSWER_COLUMN].iloc[0]
    
    print("\n----------------------------------------")
    print(f"【問題】\n{question}")
    print("----------------------------------------")
    
    input("答えがわかったら、Enterキーを押してニャ…")
    
    print("\n↓")
    print("↓")
    print("↓")
    
    print(f"\n【解答＆ポイント】\n{answer}")
    
    # 続けるか、やめるか聞くニャ
    user_input = input("\nもう一問挑戦するニャ？ (やめる場合は'q'を入力): ")
    if user_input == "q":
        break # whileループから脱出するニャ

print("\nおつかれさまニャ！よく頑張ったニャン！")
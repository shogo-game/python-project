# 必要な道具箱をインポートするニャ
import shutil
import datetime
import os

# --- ★★★ 設定はここだけニャ！ ★★★ ---

# 1. バックアップしたい、元のExcelファイルの「絶対パス」をここに書くニャ
#    Shift + 右クリックで「パスのコピー」したものを貼り付けてニャ！
SOURCE_FILE_PATH = r"C:\Users\shogo\OneDrive\資格の大原税理士試験デスクトップpc用\理論練習テキスト1.xlsx"

# 2. バックアップを保存するための、新しいフォルダの「絶対パス」をここに書くニャ
#    デスクトップに「ExcelBackup」というフォルダを作って、そのパスを貼るのがおすすめニャ！
BACKUP_FOLDER_PATH = r"C:\Users\shogo\OneDrive\資格の大原税理士試験デスクトップpc用\ExcelBackup"

# --- 設定はここまでニャ！ ---


# --- ここからが、バックアップ処理の本体だニャ ---

# バックアップ用のフォルダがもし無かったら、自動で作るニャ
if not os.path.exists(BACKUP_FOLDER_PATH):
    os.makedirs(BACKUP_FOLDER_PATH)
    print(f"'{BACKUP_FOLDER_PATH}' フォルダを作ったニャ！")

# 今日の日付と時間から、ファイル名を作るニャ (例: 20251013_170000)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
original_filename = os.path.basename(SOURCE_FILE_PATH)
backup_filename = f"{timestamp}_{original_filename}"

# 新しいバックアップファイルの、最終的な保存場所を作るニャ
destination_path = os.path.join(BACKUP_FOLDER_PATH, backup_filename)

# shutilの魔法で、ファイルをコピーしてバックアップを作るニャ！
try:
    shutil.copy2(SOURCE_FILE_PATH, destination_path)
    print(f"バックアップ成功ニャ！ -> {destination_path}")
except Exception as e:
    print(f"エラーニャ！バックアップに失敗したニャン…。: {e}")
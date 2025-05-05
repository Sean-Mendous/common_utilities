import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("shared_logger")
    logger.setLevel(logging.INFO)

    # すでにハンドラがある場合は追加しない（多重出力防止）
    if not logger.handlers:
        # ファイル用ハンドラ
        file_handler = logging.FileHandler("logs/execution.log", encoding="utf-8")
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # コンソール用ハンドラ（＝ターミナル出力）
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

# 共通で使う用のインスタンス
logger = setup_logger()
"""
Модуль для описания модальных окон
"""
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QErrorMessage, QFileDialog


def error_message(text: str) -> None:
    "Вызов окна с сообщением об ошибке"
    err_msg = QErrorMessage()
    err_msg.showMessage(f"Ошибка!\n {text}")
    err_msg.exec()


def file_dialog() -> Any:
    "Вызов диалогового окна для выбора файла с СУБД"
    path = Path(__file__).parent.parent.parent.absolute()
    return QFileDialog.getOpenFileName(
        None, "Открыть",
        f"/{path}/databases/", "DB File (*.db)")[0]

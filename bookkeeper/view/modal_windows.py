"""
Модуль для описания дополнительных модальных окон
для взаимодействия с пользователем:
окна с сообщениями об ошибках
информационные окна
окна выбора файла с СУБД
"""
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (QErrorMessage, QFileDialog,
                               QMessageBox)


def error_message(text: str) -> None:
    "Вызов окна с сообщением об ошибке"
    err_msg = QErrorMessage()
    err_msg.showMessage(f"Ошибка!\n {text}")
    err_msg.exec()


def message_send(text: str) -> None:
    "Вызов информационного окна с сообщением"
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.exec()


def file_dialog() -> Any:
    "Вызов диалогового окна для выбора файла с СУБД"
    path = Path(__file__).parent.parent.parent.absolute()
    return QFileDialog.getOpenFileName(
        None, "Открыть",
        f"/{path}/databases/", "DB File (*.db)")[0]

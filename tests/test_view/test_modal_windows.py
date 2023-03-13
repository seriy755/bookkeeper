"""
Тесты GUI для модуля с модальными окнами
"""
from PySide6.QtWidgets import (QErrorMessage, QFileDialog,
                               QMessageBox)

from bookkeeper.view.modal_windows import (error_message, message_send,
                                           file_dialog)


def test_error_message(qtbot, monkeypatch):
    monkeypatch.setattr(QErrorMessage, 'exec',
                        lambda *args: QErrorMessage.done)
    assert error_message("") is None


def test_message_send(qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, 'exec',
                        lambda *args: QMessageBox.Ok)
    assert message_send("") is None


def test_open_file_dialog(qtbot, monkeypatch):
    monkeypatch.setattr(QFileDialog, 'parent',
                        lambda *args: QFileDialog.Cancel)
    file_dialog()
    assert True

from PyQt5.QtWidgets import QMessageBox

def TetrisAboutWindow():
    msgBox = QMessageBox(
                QMessageBox.Information,
                "About",
                "ABOUT ME \n-------------------------",
                QMessageBox.Ok
                )
    return msgBox


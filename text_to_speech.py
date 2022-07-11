#!/usr/bin/env python
"""
Text-2-Speech
By Gabriel Riley
"""
import os
import sys
import pyttsx3 as tts
from PySide6 import QtCore, QtWidgets, QtGui


class TextToSpeech(QtWidgets.QWidget):
    """
    A basic text to speech converter
    """
    def __init__(self):
        """
        Uses pyttsx3 to convert given text to speech and save it to a given directory.
        Various parameters can be adjusted using gui, including tone, rate and save format.
        """
        super().__init__()
        self.setWindowTitle("Text-2-Speech")
        self.icon = QtGui.QIcon()
        self.icon.addFile('Logo.ico')
        self.setWindowIcon(self.icon)

        # ----------Text2Speech----------
        self.text_to_speech = tts.init()
        self.voices = self.text_to_speech.getProperty('voices')
        self.rate = self.text_to_speech.getProperty('rate')

        # ----------Labels----------
        self.label_text = QtWidgets.QLabel("Text to Speech")
        self.label_tone = QtWidgets.QLabel("Tone")
        self.label_rate = QtWidgets.QLabel("Rate")
        self.label_dir = QtWidgets.QLabel(f"Directory: {os.getcwd()}")

        # ----------Dialog----------
        self.dialog_text = QtWidgets.QLineEdit()

        # ----------ComboBoxes----------
        self.combo_tone = QtWidgets.QComboBox()
        self.combo_tone.addItems(["Masculine", "Feminine"])

        self.combo_format = QtWidgets.QComboBox()
        self.combo_format.addItems(["mp3", "WAV", "FLAC"])

        # ----------Sliders----------
        self.slider_rate = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)
        self.slider_rate.setMinimum(50)
        self.slider_rate.setMaximum(400)
        self.slider_rate.setValue(200)

        # ----------Buttons----------
        self.button_convert = QtWidgets.QPushButton("Convert")
        self.button_dir = QtWidgets.QPushButton("Select")

        # ----------Layout----------
        self.grid = QtWidgets.QGridLayout(self)

        self.grid.addWidget(self.label_tone, 0, 0, 1, 3)
        self.grid.addWidget(self.label_rate, 0, 3, 1, 1)
        self.grid.addWidget(self.combo_tone, 1, 0, 1, 1)
        self.grid.addWidget(self.slider_rate, 1, 1, 1, 4)
        self.grid.addWidget(self.label_text, 2, 0, 1, 1)
        self.grid.addWidget(self.dialog_text, 2, 1, 1, 3)
        self.grid.addWidget(self.combo_format, 2, 4, 1, 1)
        self.grid.addWidget(self.button_dir, 3, 0, 1, 1)
        self.grid.addWidget(self.label_dir, 3, 1, 1, 4)
        self.grid.addWidget(self.button_convert, 4, 0, 1, 5)

        # ----------Functionality----------
        self.slider_rate.valueChanged.connect(self.set_rate)

        self.button_dir.clicked.connect(self.get_directory)
        self.button_convert.clicked.connect(self.convert_text)

    def convert_text(self):
        """
        Converts given text to speech.
        Takes in parameters from QtWidgets for tone, rate and format.
        """
        text = self.dialog_text.text()
        self.dialog_text.setText("")
        tts_format = self.combo_format.currentText()
        directory = self.label_dir.text().split(" ")

        if self.combo_tone.currentIndex() == 0:
            self.text_to_speech.setProperty('voice', self.voices[0].id)
        else:
            self.text_to_speech.setProperty('voice', self.voices[1].id)

        self.text_to_speech.say(text)
        self.text_to_speech.save_to_file(text, f"{directory[1]}/{text}.{tts_format}")
        self.text_to_speech.runAndWait()

    def get_directory(self):
        """
        Sets label and save path to a user defined directory.
        """
        dialog_directory = QtWidgets.QFileDialog.getExistingDirectory()
        if dialog_directory:
            self.label_dir.setText(f"Directory: {dialog_directory}")

    def set_rate(self):
        """
        Sets the rate of speech
        """
        rate = self.slider_rate.value()
        self.text_to_speech.setProperty('rate', rate)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widgets = TextToSpeech()
    widgets.setFixedSize(500, 150)
    widgets.show()

    # Style
    with open('style.qss', 'r', encoding="utf-8") as f:
        style = f.read()
        app.setStyleSheet(style)

    sys.exit(app.exec())

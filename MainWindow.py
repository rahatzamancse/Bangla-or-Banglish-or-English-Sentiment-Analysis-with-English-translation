from enum import Enum

from PyQt5.QtWidgets import QMainWindow, QStatusBar
from PyQt5.uic import loadUi

from pyavrophonetic import avro
from textblob import TextBlob

from models.TextBlob import TextBlobClass
from models.VaderSentiment import VaderSentiment


class PHASE(Enum):
    BANGLISH = 0
    BANGLA = 1
    ENGLISH = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./UI/MainWindow.ui", self)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Welcome")

        self.reset_button.clicked.connect(self.resetAll)
        self.go_button.clicked.connect(self.go)

        self.banglish_radio.setChecked(True)

    def resetAll(self):
        self.banglish_radio.setChecked(True)
        self.input_textedit.clear()
        self.textBrowser1.clear()
        self.textBrowser2.clear()
        self.result1.setText("Press Analyse")
        self.result2.setText("Press Analyse")
        self.statusBar.showMessage("Cleared")

    def go(self):
        self.statusBar.showMessage("Calculating")
        input = ("", PHASE.BANGLISH)
        models = [TextBlobClass, VaderSentiment]

        if self.banglish_radio.isChecked():
            input = (self.input_textedit.toPlainText(), PHASE.BANGLISH)
        elif self.bangla_radio.isChecked():
            input = (self.input_textedit.toPlainText(), PHASE.BANGLA)
        elif self.english_radio.isChecked():
            input = (self.input_textedit.toPlainText(), PHASE.ENGLISH)

        # input = ("i am", phase.bengla)

        results = MainWindow.getSenti(input, models)

        # results= [ {'name': extlob , 'resut': " ", 'conclusion':Neutral },
        #             {'name':nvadertext , 'resut': " ", 'conclusion':Neutral }
        #           ]

        self.textBrowser1.setText(results[0]["result"])
        self.textBrowser2.setText(results[1]["result"])
        self.result1.setText(results[0]["conclusion"])
        self.result2.setText(results[1]["conclusion"])

        self.statusBar.showMessage("Done")

    def getSenti(input, models):
        sentence, phase = input

        if phase is PHASE.BANGLISH:
            print("Banglish is :", sentence)
            sentence = avro.parse(sentence)
            phase = PHASE.BANGLA
            print("Bangla is :", sentence)

        if phase is PHASE.BANGLA:
            # sentence = str(TextBlob(sentence).translate(to='en'))
            from googletrans import Translator
            translator = Translator()
            sentence = translator.translate(sentence)
            phase = PHASE.ENGLISH
            print("English is :", sentence)

        results = []

        for uniModel in models:
            model = uniModel(sentence)
            result = {
                'name': model.name,
                'result': model.result(),
                'conclusion': model.conclusion()
            }
            results.append(result)


        return results

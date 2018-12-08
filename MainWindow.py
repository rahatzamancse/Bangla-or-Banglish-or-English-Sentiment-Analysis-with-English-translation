from enum import Enum

from

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
        self.language.clear()
        self.language.addItems(["translate", "googletrans", "TextBlob"])
        self.language.setCurrentIndex(0)

        self.parse_button.clicked.connect(self.parse_start)

    def resetAll(self):
        self.banglish_radio.setChecked(True)
        self.input_textedit.clear()
        self.textBrowser1.clear()
        self.textBrowser2.clear()
        self.result1.setText("Press Analyse")
        self.result2.setText("Press Analyse")
        self.statusBar.showMessage("Cleared")

    def parse_start(self):
        from scrapy.crawler import CrawlerProcess
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(ProthomSpider)
        self.statusBar.showMessage("Scraping from prothom alo")
        process.start()

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

        results = self.getSenti(input, models)

        # results= [ {'name': extlob , 'resut': " ", 'conclusion':Neutral },
        #             {'name':nvadertext , 'resut': " ", 'conclusion':Neutral }
        #           ]

        self.textBrowser1.setText(results[0]["result"])
        self.textBrowser2.setText(results[1]["result"])
        self.result1.setText(results[0]["conclusion"])
        self.result2.setText(results[1]["conclusion"])

        self.statusBar.showMessage("Done")

    def getSenti(self, input, models):
        sentence, phase = input

        if phase is PHASE.BANGLISH:
            print("Banglish is :", sentence)
            sentence = avro.parse(sentence)
            phase = PHASE.BANGLA
            print("Bangla is :", sentence)

        if phase is PHASE.BANGLA:
            # 1 : TextBlob
            # 2 : googletrans
            # 3 : translate


            use_api = self.language.currentIndex()
            if use_api == 2:
                print("Using Textblob translator")
                sentence = str(TextBlob(sentence).translate(to='en'))

            elif use_api == 1:
                print("Using googletrans translator")
                from googletrans import Translator
                translator = Translator()
                sentence = str(translator.translate(sentence))

            elif use_api == 0:
                print("Using translate translator")
                from translate import Translator
                translator = Translator(to_lang="en", from_lang="bn")
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

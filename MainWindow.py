import json
import textwrap
from enum import Enum

import qdarkstyle
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QTreeWidgetItem, QFileDialog, QAction, QMenu, \
    qApp
from PyQt5.uic import loadUi
from scrapy.crawler import CrawlerProcess
from textblob import TextBlob

from models.TextBlob import TextBlobClass
from models.VaderSentiment import VaderSentiment
from prothomaloscraping.converttoutf import JSONUtf
from prothomaloscraping.prothomalo.spiders.archive_getter import ProthomSpider
from prothomaloscraping.prothomalo.spiders.article_comments_getter import ArticleCommentsSpider
from pyavrophonetic import avro


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
        self.send_from_tree_button.clicked.connect(self.moveItemToEdit)
        self.itemSelected = None
        self.text_clear_button.clicked.connect(self.clearText)
        self.browse_button.clicked.connect(self.browser_file)
        self.json_tree.setColumnCount(2)
        self.json_tree.setHeaderLabels(["Title", "Content"])
        self.json_tree.setColumnWidth(0, 100)
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': 'prothomaloscraping/prothom.json'
        })
        self.initMenu()

    def initMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        # File menu

        act = QAction('Load from json', self)
        act.setStatusTip('Load from saved JSON file')
        # act.triggered.connect(self.addCar)
        fileMenu.addAction(act)

        act = QAction('About', self)
        act.setStatusTip('Show Gulu')
        # act.triggered.connect(self.showArch)
        fileMenu.addAction(act)

        settingsMenu = menubar.addMenu('&Settings')
        themeMenu = QMenu("Themes", self)
        settingsMenu.addMenu(themeMenu)

        act = QAction('Dark', self)
        act.setStatusTip('Dark Theme')
        act.triggered.connect(lambda: qApp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()))
        themeMenu.addAction(act)

        act = QAction('White', self)
        act.setStatusTip('White Theme')
        act.triggered.connect(lambda: qApp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()))
        themeMenu.addAction(act)

        ## Add Exit
        fileMenu.addSeparator()
        act = QAction('&Exit', self)
        act.setShortcut('Ctrl+Q')
        act.setStatusTip('Exit application')
        act.triggered.connect(qApp.quit)
        fileMenu.addAction(act)

    def browser_file(self):
        file = QFileDialog.getOpenFileName()[0]


    def clearText(self):
        self.input_textedit.clear()

    def moveItemToEdit(self):
        getSelected = self.json_tree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            text = baseNode.text(1)
            self.input_textedit.setText(self.input_textedit.toPlainText() + "\n" + text)


    def resetAll(self):
        self.banglish_radio.setChecked(True)
        self.input_textedit.clear()
        self.textBrowser1.clear()
        self.textBrowser2.clear()
        self.result1.setText("Press Analyse")
        self.result2.setText("Press Analyse")
        self.statusBar.showMessage("Cleared")

    def parse_start(self):

        with open("prothomaloscraping/prothom.json", 'w') as file:
            file.write("")

        data = str(self.prothom_date_lineedit.text())

        if self.date_radio.isChecked():
            self.process.crawl(ProthomSpider, data)
        else:
            self.process.crawl(ArticleCommentsSpider, data)

        self.statusBar.showMessage("Scraping from prothom alo")
        self.process.start()
        JSONUtf().start()

        json_data = {}
        with open('results.json') as file:
            json_data = json.load(file)

        data = []
        for item in json_data:
            if 'comment' in item:
                tree = {}
                if 'title-page' in item:
                    tree['title'] = item['title-page'].strip()
                    tree['content'] = []

                    for content in item['content']:
                        content = content.strip()
                        if content != "":
                            tree['content'].append(content)

                    tree['comments'] = []
                    for c in item['comment']:
                        c = c.strip()
                        if c != "":
                            tree['comments'].append(c)
                data.append(tree)

        print(data)
        self.updateTree(data)

        self.statusBar.showMessage("Scraping DONE")

    def updateTree(self, data):
        for tree in data:
            item = QTreeWidgetItem(['Title', '\n'.join(textwrap.wrap(tree['title'], 50))])
            full_con = ""
            for con in tree['content']:
                full_con = full_con + con
            full_con = textwrap.wrap(full_con, 50)
            full_con = '\n'.join(full_con)
            con_child = QTreeWidgetItem(['Content', full_con])
            # con_child.setSizeHint(1, QSize(100, 100))
            com_child = QTreeWidgetItem(['Comments', ""])
            for i, comment in enumerate(tree['comments']):
                com_item = QTreeWidgetItem([str(i), '\n'.join(textwrap.wrap(comment, 40))])
                com_child.addChild(com_item)
            item.addChild(con_child)
            item.addChild(com_child)
            self.json_tree.addTopLevelItem(item)

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

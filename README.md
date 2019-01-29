# Bangla or Banglish Sentiment Analysis with English Translation
> Primary version

![white interface](images/white.png) ![dark interface](images/dark.png)

## Description
A Sentiment analysis with graphical user interface of bangla or phonetic bangla(banglish) language project. This uses rule based sentiment analysis API of [TextBlob](https://textblob.readthedocs.io/en/dev/) and [VaderSentiment](https://github.com/cjhutto/vaderSentiment).

## Motivation
This is my third semester System Development project. I was trying to improve my skill with [PyQt](https://wiki.python.org/moin/PyQt) and usage of python APIs.

## Python Package Dependencies
1. Scrapy
2. QDarkstyle
3. Pyqt
4. Vadersentiment
5. Textblob

N.B. geckodriver must be installed in your system for website automation.

## Getting started
1. `git clone --recursive https://github.com/rahatzamancse/Bangla-or-Banglish-or-English-Sentiment-Analysis-with-English-translation.git`
2. Install the required dependencies to your python virtual environment.
3. `python3 main.py`

Thats it! As the project is just for learning purposes, please look into how the project is structured and how the control of the project flows.

## Features
What's all the bells and whistles this project can perform?
* Scrape the title and content of the webpage of prothom alo.
* Scrape all the comments of that webpage of prothom alo.
* Scrape above two of all the webpages of prothom alo date of a specific date.
* Translate the content from phonetic bangla(banglish) to bangla and from bangla to english.
* Display results of two sentiment analysis APIs(Textblob and VaderSentiment).

## Usage
1. Run main.py
2. Provide a link of a post from [prothom alo](https://www.prothomalo.com/) or a date in the first text field.
3. Select the appropriate data provided in the textfield(Link or Date).
4. Click Parse. This will parse the title, content and comments on that page.
5. Select some items of the parsed list.
6. Select appropriate translation api to use from the drop down and the appropriate use of radio button for the source language.
7. Click on the Analyze button. This will analyse the contents selected and show the results.

N.B. You can also use your own text in the input text field for sentiment analysis.

## Contributing
The main reason to publish something open source, is that anyone can just jump in and start contributing to my project.
So If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links and References
- Project homepage: https://github.com/rahatzamancse/Bangla-or-Banglish-or-English-Sentiment-Analysis-with-English-translation
- Repository: https://github.com/rahatzamancse/Bangla-or-Banglish-or-English-Sentiment-Analysis-with-English-translation.git
- Issue tracker: https://github.com/rahatzamancse/Bangla-or-Banglish-or-English-Sentiment-Analysis-with-English-translation/issues
- In case of any help you may need from me, please contact rahatzamancse@gmail.com directly without any hesitation! I will be glad to help you.

## Author
Rahat Zaman

rahatzamancse@gmail.com

Student at Department of Computer Science and Engineering

Khulna University of Engineering & Technology, Khulna

Bangladesh

## Licensing
The code in this project is licensed under GNU GPLv3 license.

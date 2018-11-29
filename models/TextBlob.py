from textblob import TextBlob

from models.Model import Model


class TextBlobClass(Model):
    def __init__(self, english_input):
        super().__init__(english_input)
        self.name = "TextBlob"

    def result(self):
        blob = TextBlob(self.english_input)
        self.res = blob.sentiment
        dicti = {
            'polarity': self.res.polarity,
            'subjectivity': self.res.subjectivity
        }
        ret = ""
        for i, v in dicti.items():
            ret = ret + str(i) + " : " + str(v) + "\n"
        return ret

    def conclusion(self):
        # print(self.res.polarity)
        if -0.1 <= self.res.polarity <= 0.1:
            self.conc = "Neutral"
        elif self.res.polarity > 0.1:
            self.conc = "Positive!"
        elif self.res.polarity < -0.1:
            self.conc = "Negative!"
        return self.conc

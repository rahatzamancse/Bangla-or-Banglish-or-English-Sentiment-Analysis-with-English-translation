from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from models.Model import Model


class VaderSentiment(Model):
    def __init__(self, english_input):
        super().__init__(english_input)
        self.name = "VaderSentiment"

    def result(self):
        self.res = SentimentIntensityAnalyzer().polarity_scores(self.english_input)
        ret = ""
        for i, v in self.res.items():
            ret = ret + str(i) + " : " + str(v) + "\n"
        return ret

    def conclusion(self):
        # self.res = {
        #           'neg' : <float>
        #           'neu': <float>,
        #           'pos':<float>
        #            }


        m = self.res['neu']
        self.conc = "Neutral"
        if m < self.res['pos']:
            self.conc = "Positive"
            m = self.res['pos']
        if m < self.res['neg']:
            self.conc = "Negative"

        return self.conc

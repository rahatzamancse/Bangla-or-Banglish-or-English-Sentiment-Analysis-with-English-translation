class Model:
    def __init__(self, english_input):
        self.name = "Model"
        self.english_input = str(english_input)
        self.res = None
        self.conc = None

    def result(self):
        return self.res

    def conclusion(self):
        return self.conc

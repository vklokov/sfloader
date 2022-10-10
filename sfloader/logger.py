class Logger:
    def __init__(self, silent):
        self.silent = silent

    def log(self, message):
        print(message)

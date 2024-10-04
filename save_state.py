import pickle


class SaveState:
    def __init__(self, config) -> None:
        self.games = []
        self.neilers = []
        self.config = config

    def save(self):
        with open(self.config["save_path"], "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)

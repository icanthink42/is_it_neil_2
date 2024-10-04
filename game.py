class Game:
    def __init__(self, guesser_id, neiler_id) -> None:
        self.guesser_id = guesser_id
        self.neiler_id = neiler_id

    def is_neil(self, config):
        return self.neiler_id == config["neil"]

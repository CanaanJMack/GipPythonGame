class Player:
    def __init__(self):
        self._score = 0
        self._name = ""

    def __str__(self):
        return f"{self._name}"

    def reset_score(self):
        self.set_score(0)

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_score(self, score):
        self._score = score

    def get_score(self):
        return self._score

    def add_score(self, score):
        self._score += score

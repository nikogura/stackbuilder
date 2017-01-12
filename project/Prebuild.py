import util

class Prebuild:
    def __init__(self, project, data=[]):
        self.steps = []

        if data is not None:
            for stepstring in data:
                self.steps.append(util.replaceTokens(project, stepstring))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__




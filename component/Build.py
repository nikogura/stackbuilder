import util

class Build:
    def __init__(self, component, data={}):
        self.component = component
        self.project = component.project
        self.steps = []

        if data.get('steps') is not None:
            for stepstring in data.get('steps'):
                self.steps.append(util.replaceTokens(component.project, component, stepstring))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



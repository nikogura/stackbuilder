import util

class Check:
    def __init__(self, component, data={}):
        self.component = component
        self.project = component.project
        self.type = data.get('type')
        self.key = data.get('key')
        self.url = util.replaceTokens(component.project, component, data.get('url'))

        self.filename = self.url.split('/')[-1] if self.url is not None else ""

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


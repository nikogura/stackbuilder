class Project:
    def __init__(self, name=None, version=None, locations={}, components=[]):
        self.name = name
        self.version = version
        self.locations = locations
        self.components = components

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

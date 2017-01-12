import re
from Source import Source
from Check import Check
from Build import Build


class Component:
    def __init__(self, data={}):
        self.name = data.get('name')
        self.version = data.get('version')
        self.project = data.get('project')
        self.src = Source(self, data.get('src'))
        self.chk = Check(self, data.get('chk'))
        self.build = Build(self, data.get('build'))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__




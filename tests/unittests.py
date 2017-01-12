import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

from Stackbuilder import Stackbuilder
from project.Project import Project
from component.Component import Component

import fixtures


class stackbuilderTest(unittest.TestCase):
    def testDirs(self):
        sb = Stackbuilder("../resources/stack.yml")

        tempDir = sb.tempDir

        self.assertTrue(os.path.isdir(tempDir + "/src" ), "Src Dir Created")
        self.assertTrue(os.path.isdir(tempDir + "/work" ), "Work Dir Created")
        self.assertTrue(os.path.isdir(tempDir + "/gpg" ), "Gpg Dir Created")

'''
    def testProject(self):
        sb = Stackbuilder("../resources/stack.yml")
        testSb = fixtures.fargle()
        print "Generated: "
        print sb

        print "Fixture:"
        print testSb

        self.assertEqual(1, 1, "Basic law of identity")
        self.assertEqual(sb, testSb, "Generated Project equals Test Project")
'''

if __name__ == '__main__':
    unittest.main()

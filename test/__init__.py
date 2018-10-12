# The following lines are important as they enable the project to be tested
# without requiring a third party library and to be seamlessly integrated into
# a third party library.

import sys
import os

# Get path to current file
filePath = os.path.dirname(__file__)
# Abitrary path to the root of the project root
rootPath = "/../../"
# Obtaintion of the absolute path to the root of the project root
projectRootPath = os.path.abspath(os.path.join(filePath+rootPath))
# Addition of the root of the project root path to the set of python libraries
sys.path.append(projectRootPath)

from test.src import *

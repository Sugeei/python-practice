from packA import a1  # "import packA.a1" will work just the same
import sys
# sysfrom abc import nnn
from packB import a1 as a
sys.path.append('/path/to/2014_07_13_test')

a1.a1_func()

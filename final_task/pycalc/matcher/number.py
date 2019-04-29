""""""

import re

from .helpers import regex_matcher

NUMBER = r'''
(           # integers or numbers with a fractional part: 13, 154., 3.44, ...
\d+         #   an integer part: 10, 2, 432, ...
(\.\d*)*    #   a fractional part: .2, .43, .1245, ... or dot: .
)
|
(           # numbers that begin with a dot: .12, .59, ...
\.\d+       #   a fractional part: .2, .43, .1245, ...
)      
'''

NUMBER_REGEX = re.compile(NUMBER, re.VERBOSE)

NUMBER_MATCHER = regex_matcher(NUMBER_REGEX)

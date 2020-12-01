
from .__version__ import version

from .exceptions import *


__doc__ = """
A way to efficiently do a c++ style switch case in Python 3.7+. Should work for Python 3.6. Haven't tested for older versions of Python.

I would like feedback, however, if there any ways to improve it. Please see the docstring for the SwitchCase classes for usage examples. I do plan on making a package for it soon.

    Works on any class or variable type that contains a definition for __eq__.
    the nested BreakCase exception is the only exception suppressed. All others are passed on.

    ------------- Usage Examples -------------

        # example 1
        test = 10
        with SwitchCase(test) as sc:
            sc(2, on_true=print, on_true_args=('test 1',) )
            print('sub 1')
            sc(10, on_true=print, on_true_args=('test 2',) )  # will break here due to match found.
            print('sub 2')
            sc(12, on_true=print, on_true_args=('test 3',) )

        # example 2
        test = '10'
        with SwitchCase(test, catch_value_to_check=True) as sc:
            on_true = lambda x: print(f'testing... {x}')

            sc(2, on_true=on_true)
            print('sub 1')
            sc('1', on_true=on_true)
            print('sub 2')
            sc('10', on_true=on_true)  # will break here due to match found.

        # example 3
        def run_test(*args, **kwargs):
            return {
                    'args': args,
                    'kwargs': kwargs
                    }
        test = '10'
        switcher = SwitchCase(test, catch_value_to_check=True)
        with switcher as sc:
            on_true = lambda x: run_test(x, test=True)

            sc(2, on_true=on_true)
            print('sub 1')
            sc('1', on_true=on_true)  # will break here.
            print('sub 2')
            sc('10', on_true=on_true)
        print(switcher.result)
"""

__name__ = 'PySwitchCase'
__author__ = "Tyler Stegmaier"
__email__ = "tyler.stegmaier.510@gmail.com"
__copyright__ = "Copyright 2020"
__credits__ = [
        "Copyright (c) 2020 Tyler Stegmaier",
        ]
__license__ = "GPL 3.0"
__version__ = version
__maintainer__ = __author__

# How mature is this project? Common values are
#   3 - Alpha
#   4 - Beta
#   5 - Production/Stable
__status__ = 'Development Status :: 3 - Alpha'

__url__ = fr'https://github.com/Jakar510/{__name__}'
# download_url=f'https://github.com/Jakar510/PyDebug/TkinterExtensions/releases/tag/{version}'
__classifiers__ = [
        __status__,

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: MIT -- Free To Use But Restricted',

        # Support platforms
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        'Programming Language :: Python :: 3',
        ]

__short_description__ = 'A pure python way to efficiently do a c++ style switch case in Python 3.6+.'

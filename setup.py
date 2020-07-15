from setuptools import setup
from src.PySwitchCase.__version__ import version




data_files = [
        'PySwitchCase/*.py'
        ]
setup(
        name='PySwitchCase',
        version=version,
        packages=['PySwitchCase'],
        url='https://github.com/Jakar510/PySwitchCase',
        download_url='https://github.com/Jakar510/PySwitchCase/releases/tag/v1.0.2',
        license='GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
        author='Tyler Stegmaier',
        author_email='tyler.stegmaier.510@gmail.com',
        description='A pure python way to efficiently do a c++ style switch case in Python 3.6+.',
        install_requires=[],
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish
            'License :: Free To Use But Restricted',

            # Support platforms
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',

            'Programming Language :: Python :: 3',
        ],
        keywords='switch switch-case case',
        package_dir={'PySwitchCase': 'src/PySwitchCase'},
        package_data={
                'PySwitchCase': data_files,
            },
        )


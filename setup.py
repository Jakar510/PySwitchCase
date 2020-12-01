from setuptools import setup

from src.PySwitchCase import __version__, __classifiers__, __author__, __name__, __license__, __url__, __email__, __short_description__


data_files = [
        'PySwitchCase/*.py'
        ]
setup(
        name=__name__,
        version=__version__,
        packages=[__name__],
        url=__url__ or 'https://github.com/Jakar510/PySwitchCase',
        license=__license__ or 'GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
        author=__author__,
        author_email=__email__,
        description=__short_description__,
        install_requires=[],
        classifiers=__classifiers__,
        keywords='switch switch-case case',
        package_dir={ 'PySwitchCase': 'src/PySwitchCase' },
        package_data={
                'PySwitchCase': data_files,
                },
        )

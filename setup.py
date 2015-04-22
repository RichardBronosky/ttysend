from setuptools import setup

setup(
    name='ttysend',
    version='0.1',
    py_modules=['ttysend', 'ttyscripter'],
    entry_points={
        'console_scripts': [
            'ttysend=ttysend:cli',
            'ttyscripter=ttyscripter:cli',
        ],
    },
)

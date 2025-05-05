from setuptools import setup, find_packages

setup(
    name='common_utils',
    version='0.1.0',
    py_modules=['google_spreadsheet'],
    packages=find_packages(where="."),
    install_requires=[
        'gspread>=5.0.0',
        'google-auth',
        'google-auth-oauthlib',
    ],
)
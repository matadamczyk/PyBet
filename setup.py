from setuptools import setup, find_packages

setup(
    name="pybet",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'django',
        'requests',
        'beautifulsoup4',
        'numpy',
        'scikit-learn',
        'joblib',
    ],
)

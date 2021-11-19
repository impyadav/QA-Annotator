from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='QA-Annotator',
    version='1.0.0',
    packages=['annotator'],
    url='https://github.com/impyadav/QA-Annotator',
    license='GPLv3',
    author='Prateek Yadav',
    author_email='impyadav.tech@gmail.com',
    description='Question-Answering Annotation Tool',
    long_description=long_description
)

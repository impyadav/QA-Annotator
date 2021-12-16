from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='QA-Annotator',
    version='1.0.0',
    packages=['annotator'],
    url='https://github.com/impyadav/QA-Annotator',
    license='MIT',
    author='Praveen Singh, Shubham Modi, Prateek Yadav',
    author_email='impyadav.tech@gmail.com',
    description='Data Annotation Tool for NLP-based Question-Answering systems',
    long_description=long_description
)

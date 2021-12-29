from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='QA-Annotator',
    version='1.0.0',
    packages=['annotator'],
    url='https://github.com/impyadav/QA-Annotator',
    download_url='https://github.com/impyadav/QA-Annotator/archive/refs/tags/v_1.0.0.tar.gz',
    install_requires=required,
    license='MIT',
    author='Praveen Singh, Shubham Modi, Prateek Yadav',
    author_email='impyadav.tech@gmail.com',
    description='Data Annotation Tool for NLP-based Question-Answering systems',
    long_description='Making the mammoth task of data annotation for an NLP-based Question-Answering system hassle-free. Just jump right in and start annotating! 🤞'

)

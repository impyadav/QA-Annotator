from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    README = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='qa_annotator',
    version='1.0.0.dev9',
    packages=find_packages(),
    # include_package_data=True,
    package_data={
        'annotator': ['.env', '*.sqlite3', 'templates/*', 'static/**/*', '*.txt', '*.md', '.flaskenv'],
        'static': ['**/*.css', '**/*.map', '**/*.gif', '**/*.js'],
        'templates': ['*.html'],
    },
    entry_points={
        'console_scripts': [
            'annotator=annotator.app:main'
        ]},
    url='https://github.com/impyadav/QA-Annotator',
    download_url='https://github.com/impyadav/QA-Annotator/archive/refs/tags/v_1.1.0.tar.gz',
    install_requires=required,
    license='MIT',
    author='Praveen Singh, Shubham Modi, Prateek Yadav',
    author_email='impyadav.tech@gmail.com',
    description='Data Annotation Tool for NLP-based Question-Answering systems.',
    long_description_content_type='text/markdown',
    long_description=README
)

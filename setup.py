from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='watch2gether',
    version='0.1b2',
    description='一起看电影',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steve R. Sun',
    author_email='s1638650145@gmail.com',
    url='https://github.com/sun1638650145/bunnyburrow',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    license='GNU General Public License v2 (GPLv2)',
    entry_points={
        'console_scripts': [
            'w2g-cli = watch2gether.cli:run'
        ]
    },
    install_requires=[
        'fastapi>=0.110.1, <=0.111.0',
        'uvicorn>=0.26.0, <=0.30.1',
        'websockets>=11.0, <=12.0',
    ],
    python_requires='>=3.9',
)

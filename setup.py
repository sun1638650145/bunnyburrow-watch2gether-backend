from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='watch2gether',
    version='0.1a4',
    description='一起看电影',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steve R. Sun',
    author_email='s1638650145@gmail.com',
    url='https://github.com/sun1638650145/bunnyburrow',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
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
        'fastapi>=0.89.1, <=0.97.0',
        'uvicorn==0.22.0',
        'websockets>=10.4, <=11.0.3',
    ],
    python_requires='>=3.8',
)

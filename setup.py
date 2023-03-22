from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='watch2gether',
    version='0.1a3',
    description='一起看电影',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steve R. Sun',
    author_email='s1638650145@gmail.com',
    url='https://www.sunruiqi.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    license='Non-free Software',
    install_requires=[
        'fastapi>=0.89.1, <=0.95.0',
        'websockets==10.4',
    ],
    python_requires='>=3.8',
)

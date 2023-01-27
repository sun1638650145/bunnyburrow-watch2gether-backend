from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='watch2gether',
    version='0.1a0',
    description='一起看电影',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steve R. Sun',
    author_email='s1638650145@gmail.com',
    url='www.sunruiqi.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    license='Non-free Software',
    install_requires=[
        'fastapi==0.89.1',
        'uvicorn==0.20.0',
    ],
    python_requires='>=3.8',
)

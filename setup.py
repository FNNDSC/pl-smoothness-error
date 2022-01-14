from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name='smoothness_error',
    version='1.0.0',
    description='Calculate vertex-wise smoothness error of a .obj surface mesh',
    long_description=readme,
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-smoothness-error',
    packages=['smoothness_error'],
    install_requires=['chrisapp', 'pybicpl'],
    license='MIT',
    zip_safe=False,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'smoothness_error = smoothness_error.__main__:main'
        ]
    }
)

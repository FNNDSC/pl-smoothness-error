from setuptools import setup

setup(
    name='smtherr',
    version='2.0.1',
    description='Calculate smoothness error (difference in curvature between neighbor vertices) for surfaces.',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-smoothness-error',
    py_modules=['smtherr'],
    install_requires=['chris_plugin'],
    license='MIT',
    python_requires='>=3.10.4',
    entry_points={
        'console_scripts': [
            'smtherr = smtherr:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)

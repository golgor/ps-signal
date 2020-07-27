from setuptools import setup, find_packages
import pathlib
import ps_signal

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

description = "Module for parsing and analysing data from a picoscope."

setup(
    name='ps_signal',
    version=ps_signal.__version__,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/golgor/ps-signal',
    author='Robert Nyström',
    author_email='golgafrincham@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='analysis, picoscope',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'matplotlib>=3.1.3',
        'scipy>=1.4.1',
        'numpy>=1.18.1',
        'xlrd>=1.2.0',
        'seaborn>=0.10.0',
        'pandas>=1.0.1'
    ],
    # extras_require={},
    # package_data={},
    # data_files=[],
    entry_points={
        'console_scripts': ['ps-signal = ps_signal.__main__:main']
    },
)

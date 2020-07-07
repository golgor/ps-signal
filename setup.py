from setuptools import setup

setup(
    name='ps_signal',
    version='0.1b1',
    packages=['ps_signal', 'cli', 'signal_processing'],
    entry_points={
        'console_scripts': ['ps_signal = ps_signal.__main__:main']
    },
)

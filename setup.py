from setuptools import setup

setup(name='ps_signal',
      version='0.1',
      packages=['ps_signal'],
      entry_points={
          'console_scripts': [
              'ps_signal = ps_signal.__main__:main'
          ]
      },
)

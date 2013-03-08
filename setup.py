from distutils.core import setup

setup(
    name='FilenameSort',
    version='0.1.3',
    author='David N. Mashburn',
    author_email='david.n.mashburn@gmail.com',
    packages=['FilenameSort'],
    scripts=[],
    url='http://pypi.python.org/pypi/FilenameSort/',
    license='LICENSE.txt',
    description='utility to aid in natural or "human-like" sorting of file names',
    long_description=open('README.rst').read(),
    install_requires=[
                      'cmpGen>=0.1'
                     ],
)

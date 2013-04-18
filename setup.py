from distutils.core import setup

# Read the version number
with open("FilenameSort/_version.py") as f:
    exec(f.read())

setup(
    name='FilenameSort',
    version=__version__, # use the same version that's in _version.py
    author='David N. Mashburn',
    author_email='david.n.mashburn@gmail.com',
    packages=['FilenameSort'],
    scripts=[],
    url='http://pypi.python.org/pypi/FilenameSort/',
    license='LICENSE.txt',
    description='utility to aid in natural or "human-like" sorting of file names',
    long_description=open('README.rst').read(),
    install_requires=[], # No dependencies!
)

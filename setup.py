from setuptools import setup

setup(
    name='LeanSim',
    version='0.1',
    packages=['leansim'],
    url='https://github.com/nickdelgrosso/LeanSim',
    license='MIT',
    author='Nicholas A. Del Grosso',
    author_email='delgrosso.nick@gmail.com',
    description='A simple Lean production simulation, meant for exploring lean management concepts and sharing in a lecture setting.',
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    entry_points="""
        [console_scripts]
        leansim=leansim.main:main
    """,
)

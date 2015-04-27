from distutils.core import setup

setup(
    name='pjViz',
    version='1.0.0',
    packages=['pjViz/Graph', 'pjViz/Utils', 'pjViz/Parser', 'pjViz/Visual'],
    install_requires=['ply', 'pyglet'],
    url='https://github.com/Twoods01/programVisualization',
    license='MIT',
    author='twoods',
    author_email='twoods01@calpoly.edu',
    description='This program generates a visualization of an input java program',
    entry_points={
        'console_scripts': [
            'pjViz=pjViz:main',
        ],
    }
)

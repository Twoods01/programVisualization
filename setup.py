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
    classifiers=[
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Instructors :: Students',
    'Topic :: Program Visualization',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7'
    ],
    entry_points={
        'console_scripts': [
            'pjViz=pjViz:main',
        ],
    }
)

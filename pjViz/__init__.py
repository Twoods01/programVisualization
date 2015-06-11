__author__ = 'twoods'
import main as m
import sys, os


def main():
    sys.path.insert(0, os.getcwd())
    m.main(sys.argv[1:])

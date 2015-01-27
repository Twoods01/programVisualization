__author__ = 'twoods0129'
import math
import operator as op

#Normalizes a 2D vector
def normalize(direction):
    magnitude = math.sqrt(math.pow(direction[0], 2) + math.pow(direction[1], 2))
    if magnitude == 0:
        return direction
    else:
        return map(lambda x: x / magnitude, direction)

#Returns the angle between 2 vectors
def angle(vector1, vector2):
    return math.acos(sum(map(op.mul, vector1, vector2)))

def add_vectors(vector1, vector2):
    return map(op.add, vector1, vector2)

__author__ = 'twoods0129'

def print_nested(nested_array):
        print(build_simple_array(nested_array))

def build_simple_array(nested_array):
    result = []
    for el in nested_array:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.append(build_simple_array(el))
        else:
            result.append(el.name)
    return result

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def is_nested(x):
    for el in x:
        if hasattr(el, "__iter__"):
            return True

    return False

def all_nested(x):
    for el in x:
        if not hasattr(el, "__iter__"):
            return False

    return True

#Place the elements of new into arr preserving proper nesting
def add_to_array_preserve_nesting(arr, new):
    #Check if there were any method calls this statement
    if len(new) > 0:

        #If method calls were nested, preserve nesting
        if is_nested(new):

            if all_nested(new):
                arr.append(new)

            else:
                for el in new:
                    if hasattr(el, "__iter__"):
                        arr.append(el)
                    else:
                        arr.extend([el])
        #No nesting, flatten everything and extend
        else:
            arr.extend(flatten(new))
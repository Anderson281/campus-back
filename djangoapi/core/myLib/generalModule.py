
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def stringListToString(l:list):#devuelve una cadena 'grupo1, grupo2, ...'
    s=""
    for g in l:
        s = s + g + ", "
    s=s[:-2]
    return s

class AnyInt:
    def __eq__(self, other):
        return isinstance(other, int)

class AnyStr:
    def __eq__(self, other):
        return isinstance(other, str)

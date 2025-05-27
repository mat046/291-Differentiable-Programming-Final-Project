import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(os.path.dirname(current))
parent = os.path.dirname(current)
sys.path.append(parent)
import compiler
import ctypes
import error
import math
import unittest

epsilon = 1e-4

def adj_equals_one(ret):
    ret.contents.dval = 1

class FlomaTest(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    def test_builtins(self):
        with open('floma_code/builtins.py') as f:
            _dfloat, lib, func_name_to_symbols = compiler.compile(f.read(),
                                                    target = 'c++',
                                                    output_filename = '_code/builtins',
                                                    output_cpp_filename='_code/builtins.cpp')
        x = _dfloat(-3.0, 0.0)
        y = _dfloat(5.0, 0.0)

        set_adj_to_one = ctypes.CFUNCTYPE(None, ctypes.POINTER(_dfloat))
        k = set_adj_to_one(adj_equals_one)

        symbol = func_name_to_symbols["d_func"]
        f = getattr(lib, symbol)
        f(ctypes.byref(x), ctypes.byref(y), k)

        expected_dx = 5.0 + 1/5.0
        expected_dy = (-3.0) - (-3.0)/(5.0**2)

        print(f"expected dx: {expected_dx},  actual dx: {x.dval}")
        print(f"expected dy: {expected_dy},  actual dy: {y.dval}")

        assert abs(x.dval - expected_dx) < epsilon and \
            abs(y.dval - expected_dy) < epsilon
        
if __name__ == '__main__':
    unittest.main()
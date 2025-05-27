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
import importlib

epsilon = 1e-4

def k(ret):
    ret.dval = 1

class FlomaTest(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # def test_builtins(self):
    #     with open('floma_code/builtins.py') as f:
    #        compiler.compile(f.read(),
    #             target = 'c++',
    #             output_filename = '_code/builtins',
    #             output_cpp_filename='_code/builtins.cpp')
        
    #     module_path = "_code/builtins.so"
    #     module_name = "builtins" 

    #     spec = importlib.util.spec_from_file_location(module_name, module_path)
    #     m = importlib.util.module_from_spec(spec)
    #     sys.modules[module_name] = m
    #     spec.loader.exec_module(m)

    #     x = m.make__dfloat(-3.0, 0.0)
    #     y = m.make__dfloat(5.0, 0.0)

    #     m.d_func(x,y,k)
        
    #     expected_dx = 5.0 + 1/5.0
    #     expected_dy = (-3.0) - (-3.0)/(5.0**2)

    #     print(f"expected dx: {expected_dx},  actual dx: {x.dval}")
    #     print(f"expected dy: {expected_dy},  actual dy: {y.dval}")

    #     assert abs(x.dval - expected_dx) < epsilon and \
    #         abs(y.dval - expected_dy) < epsilon
        
    def test_float_constant(self):
        with open('floma_code/float_constant.py') as f:
           compiler.compile(f.read(),
                target = 'c++',
                output_filename = '_code/float_constant',
                output_cpp_filename='_code/float_constant.cpp')
        
        module_path = "_code/float_constant.so"
        module_name = "float_constant"

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = m
        spec.loader.exec_module(m)

        x = m.make__dfloat(2.0, 0.0)

        m.d_func(x,k)
        
        expected_dx = 2.0 + 1/2.0

        print(f"expected dx: {expected_dx},  actual dx: {x.dval}")

        assert abs(x.dval - expected_dx) < epsilon
        
if __name__ == '__main__':
    unittest.main()
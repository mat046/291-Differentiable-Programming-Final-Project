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

        
    # def test_float_constant(self):
    #     with open('floma_code/float_constant.py') as f:
    #        compiler.compile(f.read(),
    #             target = 'c++',
    #             output_filename = '_code/float_constant',
    #             output_cpp_filename='_code/float_constant.cpp')
        
    #     module_path = "_code/float_constant.so"
    #     module_name = "float_constant"

    #     spec = importlib.util.spec_from_file_location(module_name, module_path)
    #     m = importlib.util.module_from_spec(spec)
    #     sys.modules[module_name] = m
    #     spec.loader.exec_module(m)

    #     x = m.make__dfloat(2.0, 0.0)

    #     m.d_func(x,k)
        
    #     expected_dx = 2.0 + 1/2.0

    #     print(f"expected dx: {expected_dx},  actual dx: {x.dval}")

    #     assert abs(x.dval - expected_dx) < epsilon


    # def test_nested_funcs(self):
    #     with open('floma_code/nested_funcs.py') as f:
    #        compiler.compile(f.read(),
    #             target = 'c++',
    #             output_filename = '_code/nested_funcs',
    #             output_cpp_filename='_code/nested_funcs.cpp')
        
    #     module_path = "_code/nested_funcs.so"
    #     module_name = "nested_funcs"

    #     spec = importlib.util.spec_from_file_location(module_name, module_path)
    #     m = importlib.util.module_from_spec(spec)
    #     sys.modules[module_name] = m
    #     spec.loader.exec_module(m)

    #     x = -7.3
    #     xdfloat = m.make__dfloat(x, 0.0)

    #     m.d_func(xdfloat,k)
        
    #     dx = 16.0 * (x ** 3)
        
    #     print(f"dx : {xdfloat.dval} ; expected dx : {dx}")
    #     assert abs(xdfloat.dval - dx) < epsilon
    
    def test_nested_funcs(self):
        with open('floma_code/polynomial.py') as f:
           compiler.compile(f.read(),
                target = 'c++',
                output_filename = '_code/polynomial',
                output_cpp_filename='_code/polynomial.cpp')
        
        module_path = "_code/polynomial.so"
        module_name = "polynomial"

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        m = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = m
        spec.loader.exec_module(m)

        x = 22.7
        xdfloat = m.make__dfloat(x, 0.0)

        y = 2.718
        ydfloat = m.make__dfloat(y, 0.0)

        z = -41.67
        zdfloat = m.make__dfloat(z, 0.0)

        m.d_poly(xdfloat, ydfloat, zdfloat, k)
        actual_result = m.poly(x, y, z)

        expected_result = x**2 + 2*x*y + 2*y**2 + 2*y*z + z**2
        dx = 2.0*x + 2.0*y
        dy = 2.0*x + 4.0*y + 2.0*z
        dz = 2.0*y + 2.0*z

        print(f"expected result {expected_result} ; actual result {actual_result}")
        print(f"expected dx: {dx} ; actual dx: {xdfloat.dval}")
        print(f"expected dx: {dy} ; actual dx: {ydfloat.dval}")
        print(f"expected dx: {dz} ; actual dx: {zdfloat.dval}")
        assert abs(expected_result - actual_result) < epsilon
        assert abs(dx - xdfloat.dval) < epsilon
        assert abs(dy - ydfloat.dval) < epsilon
        assert abs(dz - zdfloat.dval) < epsilon

        
if __name__ == '__main__':
    unittest.main()
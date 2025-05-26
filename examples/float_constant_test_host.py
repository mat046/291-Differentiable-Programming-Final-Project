import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import compiler
import ctypes

if __name__ == '__main__':
    with open('float_constant_test.py') as f:
        compiler.compile(f.read(),
                            target = 'c',
                            output_cpp_filename = '_code/float_constant_test.cpp')
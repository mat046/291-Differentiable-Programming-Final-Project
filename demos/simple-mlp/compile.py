import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
import compiler

def compile():
    with open('mlp.py') as f:
        compiler.compile(f.read(),
                target = 'c++',
                output_filename = 'mlp',
                output_cpp_filename='mlp.cpp')
    

if __name__ == "__main__":
    compile()
        
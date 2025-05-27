import attrs
import autodiff
import ctypes
from ctypes import CDLL
import check
import codegen_c
# import codegen_ispc
# import codegen_opencl
import inspect
import os
import parser
import shutil
from subprocess import run
import ir
ir.generate_asdl_file()
import _asdl.floma_diff as floma_diff_ir
import numpy as np
# import cl_utils
import pathlib
import error
import platform
import distutils.ccompiler
import subprocess
import copy


def define_interface(funcs : list[floma_diff_ir.FunctionDef]) -> str:
    code = ""
    for f in funcs:
        code += f"\n    m.def(\"{f.id}\", &{f.id},"
        arg_list = [f"py::arg(\"{a.id}\")" for a in f.args]
        args = ",".join(arg_list)
        code += args + ");"
    return code


def compile(loma_code : str,
            target : str = 'c++',
            output_filename : str = None,
            output_cpp_filename : str = None,
            print_error = True):
    """ Given loma frontend code represented as a string,
        compiles C++.
        It then generates a shared library from the compiled code
        which can be imported as a python module.

        Parameters:
        loma_code - a string representing loma code to be compiled
        target - 'c++' only for now
        output_filename - where to store the generated library 
            Don't need the suffix (like '.so').
        output_cpp_filename - where to store the c++ 'intermediate' file
            This is entirely optional - use for debugging purposes.
    """

    interfaces : set[str]

    # The compiler passes
    # first parse the frontend code
    try:
        funcs = parser.parse(loma_code)
        interfaces = {f.id for f in funcs.values() if isinstance(f, floma_diff_ir.ReverseDiff)}

        # next figure out the types related to differentiation
        dfloat, funcs = autodiff.make_builtins(funcs)

        # next check if the resulting code is valid, barring from the derivative code
        check.check_ir(funcs, check_diff = False)

    except error.UserError as e:
        if print_error:
            print('[Error] error found before automatic differentiation:')
            print(e.to_string())
        raise e
    
    # next actually differentiate the functions
    funcs = autodiff.differentiate(dfloat, funcs)
    try:
        # next check if the derivative code is valid
        check.check_ir(funcs, check_diff = True)
    except error.UserError as e:
        if print_error:
            print('[Error] error found after automatic differentiation:')
            print(e.to_string())
        raise e
    
    module_name : str
    if output_filename is not None:
        module_name = copy.deepcopy(output_filename).split("/")[-1]
        # + .dll or + .so
        output_filename = output_filename + distutils.ccompiler.new_compiler().shared_lib_extension
        pathlib.Path(os.path.dirname(output_filename)).mkdir(parents=True, exist_ok=True)
    else:
        assert False, "Need to specify an output file"
    
    

    # Generate and compile the code
    if target == 'c++':
        code = codegen_c.codegen_c(dfloat, funcs)
        
        # add standard headers
        code = """
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <memory>
        \n""" + code

        # add pybind11 module; used to turn cpp file into an importable python module
        code += """
namespace py = pybind11;
\n
"""

        code += f"PYBIND11_MODULE({module_name}, m) " + "{"

        code += """
    py::class_<_dfloat, std::shared_ptr<_dfloat>>(m, "_dfloat")
        .def(py::init<>())
        .def_readwrite("val", &_dfloat::val)
        .def_readwrite("dval", &_dfloat::dval);

    m.def("make__dfloat", &make__dfloat,
          py::arg("val"), py::arg("dval"),
          "Create a _dfloat with specified value and derivative.");

    m.def("make__const__dfloat", &make__const__dfloat,
          py::arg("val"),
          "Create a constant _dfloat (zero derivative).");
"""
        to_be_interfaces = [f for f in funcs.values() if f.id in interfaces]
        code += define_interface(to_be_interfaces)

        code += """
}
"""


        print('Generated C code:')
        print(code)

        if platform.system() == 'Windows':
            assert False, "Windows is currently not a supported platform"
        else:
            includes = subprocess.check_output(["python3", "-m", "pybind11", "--includes"], text=True).strip()
            includes_list = includes.split()

            cmd = [
                "g++", "-O3", "-shared", "-std=c++17", "-fPIC",
                *includes_list,
                "-x", "c++", "-",
                "-o", output_filename
            ]

            log = subprocess.run(cmd, input=code, text=True, check=True)
            if log.returncode != 0:
                print(log.stderr)
            
            if output_cpp_filename != None:
                pathlib.Path(os.path.dirname(output_cpp_filename)).mkdir(parents=True, exist_ok=True)
                with open(output_cpp_filename, 'w') as f:
                    f.write(code)
    else:
        assert False, f'unrecognized compilation target {target}'


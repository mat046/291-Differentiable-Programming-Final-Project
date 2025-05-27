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

# def loma_to_ctypes_type(t : floma_diff_ir.type | floma_diff_ir.arg, \
#                         _dfloat : ctypes.Structure) -> ctypes.Structure:
#     """ Given a loma type, maps to the corresponding ctypes type by
#         looking up ctypes_structs
#     """

#     match t:
#         case floma_diff_ir.Arg():
#             return loma_to_ctypes_type(t.t, _dfloat)
#         # case floma_diff_ir.Int():
#         #     return ctypes.c_int
#         case floma_diff_ir.Float():
#             return ctypes.c_float
#         case floma_diff_ir.Struct():
#             return _dfloat
#         case floma_diff_ir.Cont():
#             return ctypes.CFUNCTYPE(None, ctypes.POINTER(_dfloat))
#         case None:
#             return None
#         case _:
#             assert False


# def get_function_symbols(so_file : str) -> list[str]:
#     symbol_output = subprocess.run(
#             ['nm', '-D', '--defined-only', so_file],
#             stdout=subprocess.PIPE,
#             text=True
#         ).stdout
#     symbols_table = [line for line in symbol_output.splitlines()]
#     split_cols = [line.split(" ") for line in symbols_table]
#     symbols_list = [line[2] for line in split_cols]
#     return symbols_list

# def find_function_symbol(so_file_path : str, func_names : list[str]) -> dict[str, str]:
#     symbols_list = get_function_symbols(so_file_path)
    
#     func_name_to_symbol = {}
#     for n in func_names:
#         matches = [smbl for smbl in symbols_list if n in smbl]
#         match = min(matches, key=len)
#         func_name_to_symbol[n] = match

#     return func_name_to_symbol


def define_interface(funcs : list[floma_diff_ir.FunctionDef]) -> str:
    code = ""
    for f in funcs:
        code += f"m.def(\"{f.id}\", &{f.id},"
        arg_list = [f"py::arg(\"{a.id}\")" for a in f.args]
        args = ",".join(arg_list)
        code += args + ");\n\n"
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

    # 
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
\n\n
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
            # log = run(['g++', '-shared', '-fPIC', '-o', output_filename, '-O2', '-x', 'c++', '-'],
            #     input = code,
            #     encoding='utf-8',
            #     capture_output=True)
            # if log.returncode != 0:
            #     print(log.stderr)

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

    # # build ctypes structs/classes
    # ctypes_structs = {}
    # for s in sorted_structs_list:
    #     ctypes_structs[s.id] = type(s.id, (ctypes.Structure, ), {
    #         '_fields_': [(m.id, loma_to_ctypes_type(m.t, ctypes_structs)) for m in s.members]
    #     })
    
    # ctype_dfloat = type(
    #     dfloat.id,
    #     (ctypes.Structure,),
    #     {
    #         '_fields_': [(m.id, loma_to_ctypes_type(m.t)) for m in dfloat]
    #     }
    # )
    # class _dfloat(ctypes.Structure):
    #     _fields_ = [
    #         ('val', ctypes.c_float),
    #         ('dval', ctypes.c_float)
    #     ]

    # # load the dynamic library
    # lib = CDLL(os.path.join(os.getcwd(), output_filename))
    # func_name_to_symbol = find_function_symbol(output_filename, [f.id for f in funcs.values()])
    # for f in funcs.values():
    #     symbol = func_name_to_symbol[f.id]
    #     c_func = getattr(lib, symbol)
    #     argtypes = [ctypes.POINTER(loma_to_ctypes_type(arg, _dfloat)) for arg in f.args]
    #     c_func.argtypes = argtypes
    #     restype = loma_to_ctypes_type(f.ret_type, _dfloat)
    #     if f.id == "make__const__dfloat":
    #         restype = ctypes.POINTER(restype)
    #     c_func.restype = restype

    # return _dfloat, lib, func_name_to_symbol

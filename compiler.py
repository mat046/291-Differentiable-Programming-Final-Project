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

def loma_to_ctypes_type(t : floma_diff_ir.type | floma_diff_ir.arg) -> ctypes.Structure:
                        # ctypes_structs : dict[str, ctypes.Structure]) -> ctypes.Structure:
    """ Given a loma type, maps to the corresponding ctypes type by
        looking up ctypes_structs
    """

    match t:
        case floma_diff_ir.Arg():
            return loma_to_ctypes_type(t.t)
        # case floma_diff_ir.Int():
        #     return ctypes.c_int
        case floma_diff_ir.Float():
            return ctypes.c_float
        # case floma_diff_ir.Struct():
        #     return ctypes_structs[t.id]
        case None:
            return None
        case _:
            assert False


def compile(loma_code : str,
            target : str = 'c++',
            output_filename : str = None,
            output_cpp_filename : str = None,
            print_error = True):
    """ Given loma frontend code represented as a string,
        compiles it to either C, ISPC, or OpenCL code.
        Furthermore, generates a library from the compiled code,
        and dynamically links the generated library.

        Parameters:
        loma_code - a string representing loma code to be compiled
        target - 'c', 'ispc', or 'opencl'
        output_filename - where to store the generated library for C and ISPC backends. 
            Don't need the suffix (like '.so').
            when target == 'opencl', this argument is ignored.
        opencl_context, opencl_device, opencl_command_queue - see cl_utils.create_context()
                    only used by the opencl backend
        print_error - whether it prints compile errors or not
    """

    # The compiler passes
    # first parse the frontend code
    try:
        funcs = parser.parse(loma_code)

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

    if output_filename is not None:
        # + .dll or + .so
        output_filename = output_filename + distutils.ccompiler.new_compiler().shared_lib_extension
        pathlib.Path(os.path.dirname(output_filename)).mkdir(parents=True, exist_ok=True)

    # Generate and compile the code
    if target == 'c++':
        code = codegen_c.codegen_c(dfloat, funcs)
        # add standard headers
        code = """
#include <functional>
        \n""" + code

        print('Generated C code:')
        print(code)

        if platform.system() == 'Windows':
            assert False, "Windows is currently not a supported platform"
        else:
            log = run(['g++', '-shared', '-fPIC', '-o', output_filename, '-O2', '-x', 'c', '-'],
                input = code,
                encoding='utf-8',
                capture_output=True)
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
    class _dfloat(ctypes.Structure):
        _fields_ = [
            ('val', ctypes.c_float),
            ('dval', ctypes.c_float)
        ]

    # load the dynamic library
    lib = CDLL(os.path.join(os.getcwd(), output_filename))
    for f in funcs.values():
        c_func = getattr(lib, f.id)
        argtypes = [loma_to_ctypes_type(arg) for arg in f.args]
        c_func.argtypes = argtypes
        c_func.restype = loma_to_ctypes_type(f.ret_type)

    return ctype_dfloat, lib

"""
This is the main parsing and class metaprogramming module in ASDL-ADT.

Code written by Gilbert Bernstein, Jonathan Ragan-Kelley, and Alex Reinking.
Available under MIT open source-license.  Please see ASDL-ADT project
on Github for more info.
"""
import asdl
import textwrap
import inspect
import os
from typing import Any, Mapping, Optional, Collection, List
from collections import ChainMap

from yapf.yapflib.yapf_api import FormatCode

# --------------------------------------------------------------------------- #
#   Main Interface API

def ADT(
    asdl_str    : str,
    *,
    header      : Optional[str] = None,
    ext_types   : Optional[Mapping[str, str]] = None,
    checks      : Optional[Mapping[str, str]] = None,
    no_checks   : bool = False,
    memoize     : Optional[Collection[str]] = None,
    filename    : Optional[str] = None
):
    """
    Function that converts an ASDL grammar into a Python Module.
    The generated module will contain one class for every ASDL type
    declared in the input grammar, and one (sub-)class for every
    constructor in each of those types.  These constructors will
    type-check objects on __new__ to ensure conformity with the
    given grammar.

    You should `import module_name` after running the ADT command.

    Some additional features are:
    - The new module will be written to a file -- either `filename.py` or
      by default `module_name.py`

    Arguments:
    =================
    - `header` is a string that will get pre-pended to the generated file
    - `ext_types` is a mapping from undefined ASDL type names to Python
      types used to back those types. Note that the following types are
      built in: 'bool', 'float', 'int', 'object' (i.e. any),
                'string' (i.e. str)
    - `checks` is a mapping from (undefined) ASDL type names to Python
      functions used to type check those types instead of a default
      `isinstance(...)` check
    - `no_checks` will turn off the dynamic type-checking feature, which
      may improve performance.  We recommend against using this option.
    - `memoize` is a collection of ASDL class names for which you would
      like to generate a memoized constructor
    - `filename` allows for specifying an alternate filename (see above)

    ASDL Syntax
    =================
    The grammar of ASDL follows this BNF::
        module      ::= "module" Id "{" [definitions] "}"
        definitions ::= { TypeId "=" type }+
        type        ::= product | sum
        product     ::= fields
        fields      ::= "()" | "(" { field, "," }* field ")"
        field       ::= TypeId ["?" | "*"]? Id
        sum         ::= constructor { "|" constructor }*
                        ["attributes" fields]?
        constructor ::= ConstructorId [fields]
        note: *Id is a valid posix name string

    Example
    =================
    ::
        ADT(\"\"\" module PolyMod {
            expr = Var   ( id    name  )
                 | Const ( float val   )
                 | Sum   ( expr* terms )
                 | Prod  ( float coeff, expr* terms )
                 attributes( string? tag )
        }\"\"\",
        header=\"\"\"
        from my_library import is_valid_id
        \"\"\",
        ext_types = { 'id' : 'str' },
        checks = { 'id' : 'is_valid_id' },
        memoize=['Var'])

        import PolyMod
    """
    asdl_ast = asdl.ASDLParser().parse(asdl_str)
    assert isinstance(asdl_ast, asdl.Module)

    header      = header or ""
    ext_types   = ext_types or dict()
    checks      = checks or dict()
    memoize     = memoize or set()

    mod_str = _BuildClasses(asdl_ast, header,
                                      ext_types,
                                      checks,
                                      not no_checks,
                                      memoize).file()
    mod_str = ("\"\"\"\n"+textwrap.dedent(
                """\
                ASDL Module generated by asdl_adt
                Original ASDL description:
                """)
                + textwrap.dedent(asdl_str)
                + "\n\"\"\"\n"
                + textwrap.dedent(mod_str))

    # determine the filename to dump to
    caller_frame = inspect.stack()[1]
    if not filename:
        caller_dir  = os.path.dirname(caller_frame.filename)
        try:
            os.mkdir(os.path.join(caller_dir, '_asdl'))
        except FileExistsError:
            pass
        filename    = os.path.join(caller_dir, '_asdl',
                                   f"{asdl_ast.name}.py")

    with open(filename, "w") as new_file:
        new_file.write(mod_str)

# --------------------------------------------------------------------------- #
#   Implementation

class _BuildClasses:
    """ Constructs an output file to dump """
    _builtin_types = {
        "bool": "bool",
        "float": "float",
        "int": "int",
        "object": "object",
        "string": "str",
    }
    _builtin_checks = {
        "object": "(lambda x: x is not None)",
    }
    _default_header = """
    from __future__ import annotations
    import attrs as _attrs
    from typing import Tuple as _Tuple
    from typing import Optional as _Optional

    def _list_to_tuple(xs):
        return tuple(xs) if isinstance(xs, list) else xs

    """

    def __init__(self, mod       : asdl.Module,
                       header    : str,
                       ext_types : Mapping[str, str],
                       checks    : Mapping[str, str],
                       do_checks : bool,
                       memoize   : Collection[str]):
        self._header    = textwrap.dedent(self._default_header)
        if header:
            self._header += textwrap.dedent(header) + "\n\n"

        self._types     = ChainMap({}, ext_types, self._builtin_types)
        self._checks    = ChainMap({}, checks, self._builtin_checks)
        self._do_checks = do_checks
        self._memoize   = memoize

        self._classes   = []
        self._mod_name  = None

        self.register_module(mod)
        self.build_module(mod)
    
    def file(self):
        """ Return the results of building """
        final_str = FormatCode(self._header +
                               "\n\n".join(self._classes) +
                               "\n",
                               style_config="pep8")[0]
        return final_str

    def register_module(self, mod : asdl.Module):
        """ This is the first pass over the definition.  It sets up
            anything that might be needed by the second pass """
        self._mod_name = mod.name

        # register all classes
        for dfn in mod.dfns:
            if isinstance(dfn.value, asdl.Product):
                self.register_class(dfn.name)
            elif isinstance(dfn.value, asdl.Sum):
                self.register_sum(dfn.value, dfn.name)
            else:
                assert False, f"bad case: {type(dfn)}"

    def register_class(self, name : str):
        self._types[name] = name

    def register_sum(self, sum_node : asdl.Sum, name : str):
        self.register_class(name)
        for t in sum_node.types:
            self.register_class(t.name)

    def build_module(self, mod : asdl.Module):
        """ Go through all the top-level type definitions and
            dispatch to the product or sum builders """
        for dfn in mod.dfns:
            if isinstance(dfn.value, asdl.Product):
                self.build_product(dfn.value, dfn.name)
            elif isinstance(dfn.value, asdl.Sum):
                self.build_sum(dfn.value, dfn.name)
            else:
                assert False, f"bad case: {type(dfn)}"

    def build_product(self, prod : asdl.Product, name : str):
        """ Create a full-featured class for each Product """
        self.build_class(name, prod.fields)

    def build_sum(self, sum_node : asdl.Sum, name : str):
        """ Create an abstract base class for each Sum type.
            Then create sub-classes for each Constructor """
        self._classes.append(
            f"class {name}:\n"
            f"    def __init__(self, *args, **kwargs):\n"
            f"        assert False,\"Cannot instantiate {name}\"")

        attributes = sum_node.attributes
        for t in sum_node.types:
            self.build_class(t.name, t.fields + attributes, super_cls = name)

    def build_class(self, name : str, fields : List[asdl.Field],
                          super_cls : Optional[str] = None):
        """ Build a fully-featured class """
        # optional inheritance from a super-class
        super_str = f"({super_cls})" if super_cls else ""
        # Define the class name and set up `lines` as an accumulator
        lines = [f"@_attrs.define", #(frozen=True)",
                 f"class {name}{super_str}:"]
        if len(fields) == 0:
            #lines.append("    pass")
            pass
        else:
            lines += self.build_field_decls(fields)

        lines.append("    ")

        if name in self._memoize:
            lines += ["    _memo_cache = dict()",
                      "    "]

        # lines += self.build_new_fn(fields, name)
        # lines += ["    "]
        lines += self.build_init_fn(fields, name)

        self._classes.append("\n".join(lines))

    def build_field_decls(self, fields : List[asdl.Field]):
        lines = []
        for f in fields:
            if f.name in self._types:
                raise TypeError(f"Cannot use '{f.name}' as a field name; "
                                f"it is already being used as a type name")

            seq = ""
            # if f.seq:
            #     seq = " = _attrs.field(converter=_list_to_tuple)"
            l = f"    {f.name} : {self.field_type(f)}{seq}"
            if f.opt:
                l += f" = None"
            lines.append(l)
        return lines

    def build_new_fn(self, fields : List[asdl.Field], clsname):
        fnames = []
        fnames_init = []
        for f in fields:
            n = f.name
            fnames.append(n)
            if f.opt:
                n += ' = None'
            fnames_init.append(n)
        argstr = ', '.join(['cls']+fnames_init)
        fargs  = ', '.join(fnames)

        lines = [f"    def __new__({argstr}):"]
        # do conversion from list to tuple as needed for key
        if clsname in self._memoize:
            for f in fields:
                lines += self.build_seq_coercion(f.name, f, pre="        ")
        if len(lines) > 1:
            lines += ["        "]

        if clsname in self._memoize:
            lines += [f"        _key_ = tuple([{fargs}])",
                      f"        if _key_ in cls._memo_cache:",
                      f"            result = cls._memo_cache[_key_]",
                      f"        else:",
                      f"            result = super().__new__(cls)",
                      f"            cls._memo_cache[_key_] = result",
                      f"        return result"]
        else:
            lines += [f"        return super().__new__(cls)"]

        return lines

    def build_init_fn(self, fields : List[asdl.Field], clsname):
        if self._do_checks:
            lines = [f"    def __attrs_post_init__(self):"]
            for k,f in enumerate(fields):
                lines += self.build_field_check(clsname, f, k, pre="        ")
            if len(lines) == 1:
                lines += ["        pass"]
        else:
            lines = []

        return lines
    
    def build_seq_coercion(self, val : str, field : asdl.Field, pre=""):
        if not field.seq:
            return []
        else:
            return [f"{pre}if isinstance({val}, list):",
                    f"{pre}    {val} = tuple({val})"]

    def build_field_check(self, clsname : str,
                                field : asdl.Field, k : int, pre=""):
        fname   = f"self.{field.name}"
        ftype   = field.type + ("*" if field.seq else
                                "?" if field.opt else "")
        errmsg  = (f"\"{clsname}(...) argument {k+1}: \" + \"invalid instance "
                   f"of '{ftype} {field.name}'\"")

        def check(x):
            if field.type in self._checks:
                return f"{self._checks[field.type]}({x})"
            else:
                btyp = self.field_type(field,base=True)
                return f"isinstance({x}, {btyp})"
        if field.seq:
            check_expr = (f"not (isinstance({fname}, (tuple,list)) and "
                          f"all({check('x')} for x in {fname}))")
        elif field.opt:
            check_expr = f"not ({fname} is None or {check(fname)})"
        else:
            check_expr = f"not {check(fname)}"
        return [f"{pre}if {check_expr}:",
                f"{pre}    raise TypeError({errmsg})"]

    def field_type(self, field : asdl.Field, base=False):
        # safely look up the concrete type name for the annotation
        if field.type not in self._types:
            raise TypeError(f"Unrecognized type '{field.type}'; did you "
                            f"mean to include it in ext_types?")
        typ = self._types[field.type]
        if base:
            return typ

        # handle sequence and optional qualifiers
        assert not (field.seq and field.opt), "cannot qualify as both * and ?"
        if field.seq:
            # typ = f"_Tuple[{typ}]"
            typ = f"list[{typ}]"
        elif field.opt:
            typ = f"_Optional[{typ}]"
        return typ
       
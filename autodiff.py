import ir
ir.generate_asdl_file()
import _asdl.floma_diff as floma_diff_ir
# import irmutator
# import forward_diff
# import reverse_diff
import irvisitor

# def type_to_diff_type(diff_structs : dict[str, floma_diff_ir.Struct],
#                       t : floma_diff_ir.type) -> floma_diff_ir.type:
#     """ Given a loma type t, look up diff_structs for the differential type.
#     For example, for float, we will generate a class "_dfloat" to represent
#     both the primal value and the differential:
#     class _dfloat:
#         val : float
#         dval : float
    
#     Calling type_to_diff_type(diff_structs, floma_diff_ir.Float())
#     would then return the loma type representing _dfloat.

#     diff_structs is a map that goes from the ID of the type to the differential
#     struct. For example, diff_structs['float'] will return the _dfloat type.
#     """

#     match t:
#         case floma_diff_ir.Int():
#             return diff_structs['int']
#         case floma_diff_ir.Float():
#             return diff_structs['float']
#         case floma_diff_ir.Array():
#             return floma_diff_ir.Array(\
#                 type_to_diff_type(diff_structs, t.t),
#                 t.static_size)
#         case floma_diff_ir.Struct():
#             return diff_structs[t.id]
#         case None:
#             return None
#         case _:
#             assert False, f'Unhandled type {t}'

def replace_diff_types(func : floma_diff_ir.FunctionDef) -> floma_diff_ir.FunctionDef:
    """ Given a loma function func, find all function arguments and
        declarations with type Diff[...] and turn them into the 
        corresponding differential type by looking up diff_structs.

        For example, the following loma code
        x : Diff[float]
        will be turned into
        x : _dfloat

        where _dfloat is
        class _dfloat:
            val : float
            dval : float

        diff_structs is a map that goes from the ID of the type to the 
        differential struct. For example, diff_structs['float'] will 
        return the _dfloat type.

        Currently, we do not allow repeated applications of Diff[]
        (like Diff[Diff[float]]).
    """

    def _replace_diff_type(t):
        match t:
            case floma_diff_ir.Int():
                return floma_diff_ir.Int()
            case floma_diff_ir.Float():
                return floma_diff_ir.Float()
            case floma_diff_ir.Array():
                return floma_diff_ir.Array(\
                    _replace_diff_type(t.t),
                    t.static_size)
            case floma_diff_ir.Struct():
                return t
            case floma_diff_ir.Diff():
                t = _replace_diff_type(t.t)
                if isinstance(t, floma_diff_ir.Int):
                    return diff_structs['int']
                elif isinstance(t, floma_diff_ir.Float):
                    return diff_structs['float']
                elif isinstance(t, floma_diff_ir.Struct):
                    return diff_structs[t.id]
                else:
                    # TODO: throw an user error
                    assert False, "No Diff[Array]"

    class DiffTypeMutator(irmutator.IRMutator):
        def mutate_function_def(self, node):
            new_args = [\
                floma_diff_ir.Arg(arg.id, _replace_diff_type(arg.t), arg.i) \
                for arg in node.args]
            new_body = [self.mutate_stmt(stmt) for stmt in node.body]
            new_body = irmutator.flatten(new_body)
            return floma_diff_ir.FunctionDef(\
                node.id,
                new_args,
                new_body,
                node.is_simd,
                _replace_diff_type(node.ret_type),
                lineno = node.lineno)

        def mutate_declare(self, node):
            return floma_diff_ir.Declare(\
                node.target,
                _replace_diff_type(node.t),
                self.mutate_expr(node.val) if node.val is not None else None,
                lineno = node.lineno)

    return DiffTypeMutator().mutate_function(func)

def make_builtins(funcs : dict[str, floma_diff_ir.func]) -> \
        tuple[floma_diff_ir.Struct, dict[str, floma_diff_ir.func]]:
    """ Convert floma_diff_ir to floma_diff_ir in preparation for
        automatic differentiation
    
        Return a list of funcs and their (not yet differentiated)
        counterparts.

        Return the _dfloat struct:
        class _dfloat:
            val : float
            dval : float
        _dfloats are used when differentiating float variables
        The differential struct for an int is still an int.
    """

    # funcs_to_be_diffed = False
    # for f in funcs.values():
    #     if isinstance(f, floma_diff_ir.ReverseDiff):
    #         funcs_to_be_diffed = True

    # if not funcs_to_be_diffed:
    #     return None, funcs

    # diff_structs['float'] = dfloat
    # diff_structs['int'] = floma_diff_ir.Int()


    # --------------------------------------dfloat stuff-----------------------------------------------
    dfloat = floma_diff_ir.Struct('_dfloat',
                            [floma_diff_ir.MemberDef('val', floma_diff_ir.Float()),
                             floma_diff_ir.MemberDef('dval', floma_diff_ir.Float())])
    funcs['make__dfloat'] = floma_diff_ir.FunctionDef(
            'make__dfloat',
            args = [floma_diff_ir.Arg('val', floma_diff_ir.Float()),
                    floma_diff_ir.Arg('dval', floma_diff_ir.Float())],
            body = [floma_diff_ir.Declare('ret', dfloat),
                    floma_diff_ir.Assign(floma_diff_ir.StructAccess(floma_diff_ir.Var('ret'), 'val'), floma_diff_ir.Var('val')),
                    floma_diff_ir.Assign(floma_diff_ir.StructAccess(floma_diff_ir.Var('ret'), 'dval'), floma_diff_ir.Var('dval')),
                    floma_diff_ir.Return(floma_diff_ir.Var('ret'))],
            ret_type = dfloat)
    

    # --------------------------- built in functions and derivatives ---------------------------------------------

    def declare_ret(operation : floma_diff_ir.bin_op) -> floma_diff_ir.Declare:
        decl = floma_diff_ir.Declare(
            target='ret',
            t=dfloat,
            val=floma_diff_ir.Call(
                'make__dfloat',
                args=[
                    floma_diff_ir.BinaryOp(
                        op=operation,
                        left=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='x', t=dfloat),
                            member_id='val',
                            t=floma_diff_ir.Float()
                        ),
                        right=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='y', t=dfloat),
                            member_id='val',
                            t=floma_diff_ir.Float()
                        )
                    ),
                    floma_diff_ir.ConstFloat(0.0)
                ]
            )
        )
        return decl
    
    def adj_plus_equals(df : str, rhs : floma_diff_ir.expr) -> floma_diff_ir.Assign:
        adj = floma_diff_ir.StructAccess(
            struct=floma_diff_ir.Var(id=df, t=dfloat),
            member_id='dval',
            t=floma_diff_ir.Float()
        )
        plus_equls = floma_diff_ir.Assign(
            target=adj,
            val=floma_diff_ir.BinaryOp(
                op=floma_diff_ir.Add(),
                left=adj,
                right=rhs
            )
        )
        return plus_equls
    
    call_continuation = floma_diff_ir.CallStmt(
                            floma_diff_ir.Call(
                                id='k',
                                args=[floma_diff_ir.Var('ret', t=dfloat)]
                            )
                        )
    
    bin_op_args = [
        floma_diff_ir.Arg('x', floma_diff_ir.Float()),
        floma_diff_ir.Arg('y', floma_diff_ir.Float())
    ]

    diff_bin_op_args = [
        floma_diff_ir.Arg('x', dfloat),
        floma_diff_ir.Arg('y', dfloat),
        floma_diff_ir.Arg('k', floma_diff_ir.Cont(dfloat))
    ]
    
    # ADD FLOATS
    funcs['addf'] = floma_diff_ir.FunctionDef(
        id='addf',
        args=bin_op_args,
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    floma_diff_ir.Add(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Float()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Float())
                ),
            )
        ],
        ret_type=floma_diff_ir.Float()
    )
    funcs['d_addf'] = floma_diff_ir.FunctionDef(
        id='d_addf',
        args=diff_bin_op_args,
        body=[
            # ret = make__dfloat(x.val + y.val, 0)
            declare_ret(floma_diff_ir.Add()),

            # k(ret)
            call_continuation,

            # x.dval += ret.dval
            adj_plus_equals(
                df='x',
                rhs=floma_diff_ir.StructAccess(
                        struct=floma_diff_ir.Var(id='ret', t=dfloat),
                        member_id='dval',
                        t=floma_diff_ir.Float()
                    )
            ),

            # y.dval += ret.dval
            adj_plus_equals(
                df='y',
                rhs=floma_diff_ir.StructAccess(
                        struct=floma_diff_ir.Var(id='ret', t=dfloat),
                        member_id='dval',
                        t=floma_diff_ir.Float()
                    )
            )
        ],
        ret_type=None
    )

    # SUB FLOATS
    funcs['subf'] = floma_diff_ir.FunctionDef(
        id='subf',
        args=bin_op_args,
        body=[
            floma_diff_ir.Return(
                floma_diff_ir.BinaryOp(
                    floma_diff_ir.Sub(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Float()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Float()
    )
    funcs['d_subf'] = floma_diff_ir.FunctionDef(
        id='d_subf',
        args=bin_op_args,
        body=[
            # ret = make__dfloat(x.val - y.val, 0)
            declare_ret(floma_diff_ir.Sub()),

            # k(ret)
            call_continuation,

            # x.dval += ret.dval
            adj_plus_equals(
                df='x',
                rhs=floma_diff_ir.StructAccess(
                        struct=floma_diff_ir.Var(id='ret', t=dfloat),
                        member_id='dval',
                        t=floma_diff_ir.Float()
                    )
            ),

            # y.dval -= ret.dval
            adj_plus_equals(
                df='y',
                rhs=floma_diff_ir.BinaryOp(
                        op=floma_diff_ir.Mul(),
                        left=floma_diff_ir.ConstFloat(-1.0),
                        right=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='ret', t=dfloat),
                            member_id='dval',
                            t=floma_diff_ir.Float()
                        )
                    )
            )
        ],
        ret_type=None
    )

    # MUL FLOATS
    funcs['mulf'] = floma_diff_ir.FunctionDef(
        id='mulf',
        args=bin_op_args,
        body=[
            floma_diff_ir.Return(
                floma_diff_ir.BinaryOp(
                    floma_diff_ir.Mul(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Float()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Float()
    )
    funcs['d_mulf'] = floma_diff_ir.FunctionDef(
        id='d_mulf',
        args=diff_bin_op_args,
        body=[
            # ret = make__dfloat(x.val * y.val, 0)
            declare_ret(floma_diff_ir.Mul()),

            # k(ret)
            call_continuation,

            # x.dval += y.val * ret.dval
            adj_plus_equals(
                df='x',
                rhs=floma_diff_ir.BinaryOp(
                        op=floma_diff_ir.Mul(),
                        left=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var('y', t=dfloat),
                            member_id='val',
                            t=floma_diff_ir.Float()
                        ),
                        right=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='ret', t=dfloat),
                            member_id='dval',
                            t=floma_diff_ir.Float()
                        )
                    )
            ),

            # y.dval += x.val * ret.dval
            adj_plus_equals(
                df='y',
                rhs=floma_diff_ir.BinaryOp(
                        op=floma_diff_ir.Mul(),
                        left=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var('x', t=dfloat),
                            member_id='val',
                            t=floma_diff_ir.Float()
                        ),
                        right=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='ret', t=dfloat),
                            member_id='dval',
                            t=floma_diff_ir.Float()
                        )
                    )
            )
        ],
        ret_type=None
    )

    # DIV FLOATS
    funcs['divf'] = floma_diff_ir.FunctionDef(
        id='divf',
        args=bin_op_args,
        body=[
            floma_diff_ir.Return(
                floma_diff_ir.BinaryOp(
                    floma_diff_ir.Div(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Float()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Float()
    )
    funcs['d_divf'] = floma_diff_ir.FunctionDef(
        id='d_divf',
        args=diff_bin_op_args,
        body=[
            # ret = make__dfloat(x.val / y.val, 0)
            declare_ret(floma_diff_ir.Div()),

            # k(ret)
            call_continuation,

            # x.dval += ret.dval / y.val
            adj_plus_equals(
                df='x',
                rhs=floma_diff_ir.BinaryOp(
                        op=floma_diff_ir.Div(),
                        left=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='ret', t=dfloat),
                            member_id='dval',
                            t=floma_diff_ir.Float()
                        ),
                        right=floma_diff_ir.StructAccess(
                            struct=floma_diff_ir.Var(id='y', t=dfloat),
                            member_id='val',
                            t=floma_diff_ir.Float()
                        )
                    )
            ),

            # y.dval -= ret.dval * x.val / ((y.val)^2)
            adj_plus_equals(
                df='y',
                rhs=floma_diff_ir.BinaryOp(
                    floma_diff_ir.Mul(),
                    left=floma_diff_ir.ConstFloat(-1.0),
                    right=floma_diff_ir.BinaryOp(
                        # /
                        op=floma_diff_ir.Div(),
                        # ret.dval * x.val
                        left=floma_diff_ir.BinaryOp(
                            op=floma_diff_ir.Mul(),
                            left=floma_diff_ir.StructAccess(
                                struct=floma_diff_ir.Var(id='ret', t=dfloat),
                                member_id='dval',
                                t=floma_diff_ir.Float()
                            ),
                            right=floma_diff_ir.StructAccess(
                                struct=floma_diff_ir.Var(id='x', t=dfloat),
                                member_id='val',
                                t=floma_diff_ir.Float()
                            ),
                        ),
                        # ((y.val)^2)
                        right=floma_diff_ir.BinaryOp(
                            floma_diff_ir.Mul(),
                            left=floma_diff_ir.StructAccess(
                                struct=floma_diff_ir.Var(id='y', t=dfloat),
                                member_id='val',
                                t=floma_diff_ir.Float()
                            ),
                            right=floma_diff_ir.StructAccess(
                                struct=floma_diff_ir.Var(id='y', t=dfloat),
                                member_id='val',
                                t=floma_diff_ir.Float()
                            )
                        )
                    )
                )
            )
        ],
        ret_type=None
    )

    return dfloat, funcs

class CallFuncVisitor(irvisitor.IRVisitor):
    def __init__(self):
        self.called_func_ids = set()

    def visit_call(self, node):
        for arg in node.args:
            self.visit_expr(arg)

        # do nothing if it's built-in func
        if node.id == 'sin' or \
            node.id == 'cos' or \
            node.id == 'sqrt' or \
            node.id == 'pow' or \
            node.id == 'exp' or \
            node.id == 'log' or \
            node.id == 'int2float' or \
            node.id == 'float2int' or \
            node.id == 'thread_id' or \
            node.id == 'atomic_add':
            return

        self.called_func_ids.add(node.id)

def differentiate(structs : dict[str, floma_diff_ir.Struct],
                  diff_structs : dict[str, floma_diff_ir.Struct],
                  funcs : dict[str, floma_diff_ir.func]) -> dict[str, floma_diff_ir.func]:
    """ Given a list loma functions (funcs), replace all functions 
        that are marked as ForwardDiff and ReverseDiff with 
        FunctionDef and the actual implementations.

        Parameters:
        structs - a dictionary that maps the ID of a Struct to 
                the corresponding Struct
        diff_structs - a dictionary that maps the ID of the primal
                Struct to the corresponding differential Struct
                e.g., diff_structs['float'] returns _dfloat
        funcs - a dictionary that maps the ID of a function to 
                the corresponding func

        Returns:
        funcs - now all functions that are ForwardDiff and ReverseDiff
                are replaced by the actual FunctionDef
    """

    # Map functions to their forward/reverse versions
    func_to_fwd = dict()
    func_to_rev = dict()
    for f in funcs.values():
        if isinstance(f, floma_diff_ir.ForwardDiff):
            func_to_fwd[f.primal_func] = f.id
        elif isinstance(f, floma_diff_ir.ReverseDiff):
            func_to_rev[f.primal_func] = f.id

    # Traverse: for each function that requires forward diff
    # recursively having all called functions to require forward diff
    # as well
    visited_func = set(func_to_fwd.keys())
    func_stack = list(func_to_fwd.keys())
    while len(func_stack) > 0:
        primal_func_id = func_stack.pop()
        primal_func = funcs[primal_func_id]
        if primal_func_id not in func_to_fwd:
            fwd_func_id = '_d_fwd_' + primal_func_id
            func_to_fwd[primal_func_id] = fwd_func_id
            funcs[fwd_func_id] = floma_diff_ir.ForwardDiff(fwd_func_id, primal_func_id)
        cfv = CallFuncVisitor()
        cfv.visit_function(primal_func)
        for f in cfv.called_func_ids:
            if f not in visited_func:
                visited_func.add(f)
                func_stack.append(f)
    # Do the same for reverse diff
    visited_func = set(func_to_rev.keys())
    func_stack = list(func_to_rev.keys())
    while len(func_stack) > 0:
        primal_func_id = func_stack.pop()
        primal_func = funcs[primal_func_id]
        if primal_func_id not in func_to_rev:
            rev_func_id = '_d_rev_' + primal_func_id
            func_to_rev[primal_func_id] = rev_func_id
            funcs[rev_func_id] = floma_diff_ir.ReverseDiff(rev_func_id, primal_func_id)
        cfv = CallFuncVisitor()
        cfv.visit_function(primal_func)
        for f in cfv.called_func_ids:
            if f not in visited_func:
                visited_func.add(f)
                func_stack.append(f)

    for f in funcs.values():
        if isinstance(f, floma_diff_ir.ForwardDiff):
            fwd_diff_func = forward_diff.forward_diff(\
                f.id, structs, funcs, diff_structs,
                funcs[f.primal_func], func_to_fwd)
            funcs[f.id] = fwd_diff_func
            import pretty_print
            print(f'\nForward differentiation of function {f.id}:')
            print(pretty_print.loma_to_str(fwd_diff_func))
        elif isinstance(f, floma_diff_ir.ReverseDiff):
            rev_diff_func = reverse_diff.reverse_diff(\
                f.id, structs, funcs, diff_structs,
                funcs[f.primal_func], func_to_rev)
            funcs[f.id] = rev_diff_func
            import pretty_print
            print(f'\nReverse differentiation of function {f.id}:')
            print(pretty_print.loma_to_str(rev_diff_func))

    return funcs

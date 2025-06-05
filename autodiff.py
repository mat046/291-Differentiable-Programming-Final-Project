import ir
ir.generate_asdl_file()
import _asdl.floma_diff as floma_diff_ir
import irmutator
# import forward_diff
import reverse_diff
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
                # self.mutate_expr(node.val) if node.val is not None else None,
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
        builtin=True,
        id='make__dfloat',
        args = [floma_diff_ir.Arg('val', floma_diff_ir.Float()),
                floma_diff_ir.Arg('dval', floma_diff_ir.Float())],
        body = [floma_diff_ir.Declare(target='ret', t=dfloat, dyn_alloc=True),
                floma_diff_ir.Assign(floma_diff_ir.StructAccess(floma_diff_ir.Var('ret'), 'val'), floma_diff_ir.Var('val')),
                floma_diff_ir.Assign(floma_diff_ir.StructAccess(floma_diff_ir.Var('ret'), 'dval'), floma_diff_ir.Var('dval')),
                floma_diff_ir.Return(floma_diff_ir.Var('ret'))],
        ret_type = dfloat)
    
    funcs['make__const__dfloat'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='make__const__dfloat',
        args=[floma_diff_ir.Arg('val', floma_diff_ir.Float())],
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.Call(
                    id='make__dfloat',
                    args=[floma_diff_ir.Var(id='val'), floma_diff_ir.ConstFloat(0.0)],
                    t=dfloat
                )
            )
        ],
        ret_type=dfloat
    )

    # --------------------------- built in float binary operations and derivatives ---------------------------------------------

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
    
    bin_op_float_args = [
        floma_diff_ir.Arg('x', floma_diff_ir.Float()),
        floma_diff_ir.Arg('y', floma_diff_ir.Float())
    ]

    diff_bin_op_float_args = [
        floma_diff_ir.Arg('x', dfloat),
        floma_diff_ir.Arg('y', dfloat),
        floma_diff_ir.Arg('k', floma_diff_ir.Cont(dfloat))
    ]
    
    # ADD FLOATS
    funcs['addf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='addf',
        args=bin_op_float_args,
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
        builtin=True,
        id='d_addf',
        args=diff_bin_op_float_args,
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
        builtin=True,
        id='subf',
        args=bin_op_float_args,
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
        builtin=True,
        id='d_subf',
        args=diff_bin_op_float_args,
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
        builtin=True,
        id='mulf',
        args=bin_op_float_args,
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
        builtin=True,
        id='d_mulf',
        args=diff_bin_op_float_args,
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
        builtin=True,
        id='divf',
        args=bin_op_float_args,
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
        builtin=True,
        id='d_divf',
        args=diff_bin_op_float_args,
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



    # --------------------------- built in integer binary operations (which don't have derivatives) ---------------------------------------------

    bin_op_int_args = [
        floma_diff_ir.Arg('x', floma_diff_ir.Int()),
        floma_diff_ir.Arg('y', floma_diff_ir.Int())
    ]

    # ADD INTS
    funcs['addi'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='addi',
        args=bin_op_int_args,
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    floma_diff_ir.Add(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Int()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Int())
                ),
            )
        ],
        ret_type=floma_diff_ir.Int()
    )

    # SUB INTS
    funcs['subi'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='subi',
        args=bin_op_int_args,
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    floma_diff_ir.Sub(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Int()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Int())
                ),
            )
        ],
        ret_type=floma_diff_ir.Int()
    )

    # MUL INTS
    funcs['muli'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='muli',
        args=bin_op_int_args,
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    floma_diff_ir.Sub(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Int()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Int())
                ),
            )
        ],
        ret_type=floma_diff_ir.Int()
    )

    # DIV INTS
    funcs['divi'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='divi',
        args=bin_op_int_args,
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    floma_diff_ir.Sub(),
                    floma_diff_ir.Var('x', t=floma_diff_ir.Int()),
                    floma_diff_ir.Var('y', t=floma_diff_ir.Int())
                ),
            )
        ],
        ret_type=floma_diff_ir.Int()
    )

 

    #-------------------------------------- control flow -----------------------------------------------

    # FLOAT IFELSE
    funcs['ifelsef'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='ifelsef',
        args=[
            floma_diff_ir.Arg(id='cond', t=floma_diff_ir.Bool()),
            floma_diff_ir.Arg(id='_then', t=floma_diff_ir.Float()),
            floma_diff_ir.Arg(id='_else', t=floma_diff_ir.Float())
        ],
        body=[
            floma_diff_ir.IfElse(
                cond=floma_diff_ir.Var(id='cond', t=floma_diff_ir.Bool()),
                then_call=floma_diff_ir.Return(val=floma_diff_ir.Var(id='_then', t=floma_diff_ir.Float())),
                else_call=floma_diff_ir.Return(val=floma_diff_ir.Var(id='_else', t=floma_diff_ir.Float()))
            )
        ],
        ret_type=floma_diff_ir.Float()
    )
    funcs['d_ifelsef'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='d_ifelsef',
        args=[
            floma_diff_ir.Arg(id='cond', t=floma_diff_ir.Bool()),
            floma_diff_ir.Arg(id='_then', t=dfloat),
            floma_diff_ir.Arg(id='_else', t=dfloat),
            floma_diff_ir.Arg(id='k', t=floma_diff_ir.Cont(arg_type=dfloat))
        ],
        body=[
            floma_diff_ir.IfElse(
                cond=floma_diff_ir.Var(id='cond', t=floma_diff_ir.Bool()),
                then_call=floma_diff_ir.CallStmt(
                    call=floma_diff_ir.Call(id='k', args=[floma_diff_ir.Var(id='_then', t=dfloat)], t=None)
                ),
                else_call=floma_diff_ir.CallStmt(
                    call=floma_diff_ir.Call(id='k', args=[floma_diff_ir.Var(id='_else', t=dfloat)], t=None)
                )
            )
        ],
        ret_type=None
    )

    # INTEGER IFELSE
    funcs['ifelsei'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='ifelsei',
        args=[
            floma_diff_ir.Arg(id='cond', t=floma_diff_ir.Bool()),
            floma_diff_ir.Arg(id='_then', t=floma_diff_ir.Int()),
            floma_diff_ir.Arg(id='_else', t=floma_diff_ir.Int())
        ],
        body=[
            floma_diff_ir.IfElse(
                cond=floma_diff_ir.Var(id='cond', t=floma_diff_ir.Bool()),
                then_call=floma_diff_ir.Return(val=floma_diff_ir.Var(id='_then', t=floma_diff_ir.Int())),
                else_call=floma_diff_ir.Return(val=floma_diff_ir.Var(id='_else', t=floma_diff_ir.Int()))
            )
        ],
        ret_type=floma_diff_ir.Int()
    )



    # ---- comparison operators; these don't have derivatives because they output booleans - however we need to define them for dfloats -------

    # LESS
    funcs['lessi'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='lessi',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Int()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Int())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Less(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Int()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Int())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )

    funcs['lessf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='lessf',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Float()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Float())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Less(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Float()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )
    funcs['d_lessf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='d_lessf',
        args=[
            floma_diff_ir.Arg(id='x', t=dfloat),
            floma_diff_ir.Arg(id='y', t=dfloat)
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Less(),
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
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )


    # LESS-EQUAL

    funcs['less_equali'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='less_equali',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Int()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Int())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.LessEqual(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Int()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Int())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )

    funcs['less_equalf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='less_equalf',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Float()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Float())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.LessEqual(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Float()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )
    funcs['d_less_equalf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='d_less_equalf',
        args=[
            floma_diff_ir.Arg(id='x', t=dfloat),
            floma_diff_ir.Arg(id='y', t=dfloat)
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.LessEqual(),
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
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )


    # GREATER

    funcs['greater'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='greater',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Int()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Int())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Greater(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Int()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Int())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )

    funcs['greaterf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='greaterf',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Float()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Float())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Greater(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Float()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )
    funcs['d_greaterf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='d_greaterf',
        args=[
            floma_diff_ir.Arg(id='x', t=dfloat),
            floma_diff_ir.Arg(id='y', t=dfloat)
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Greater(),
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
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )


    # GREATER-EQUAL

    funcs['greater_equali'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='greater_equali',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Int()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Int())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.GreaterEqual(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Int()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Int())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )

    funcs['greater_equalf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='greater_equalf',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Float()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Float())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.GreaterEqual(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Float()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )
    funcs['d_greater_equalf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='d_greater_equalf',
        args=[
            floma_diff_ir.Arg(id='x', t=dfloat),
            floma_diff_ir.Arg(id='y', t=dfloat)
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.GreaterEqual(),
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
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )


    # EQUAL

    funcs['equali'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='equali',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Int()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Int())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Equal(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Int()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Int())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )

    funcs['equalf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='equalf',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Float()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Float())
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Equal(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Float()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Float())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )
    funcs['d_equalf'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='d_equalf',
        args=[
            floma_diff_ir.Arg(id='x', t=dfloat),
            floma_diff_ir.Arg(id='y', t=dfloat)
        ],
        body = [
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Equal(),
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
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )



    # ------------------------------------------ logical operators -----------------------------------------------

    # AND

    funcs['and'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='and',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Bool()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Bool())
        ],
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.And(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Bool()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Bool())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )

    # OR

    funcs['or'] = floma_diff_ir.FunctionDef(
        builtin=True,
        id='or',
        args=[
            floma_diff_ir.Arg(id='x', t=floma_diff_ir.Bool()),
            floma_diff_ir.Arg(id='y', t=floma_diff_ir.Bool())
        ],
        body=[
            floma_diff_ir.Return(
                val=floma_diff_ir.BinaryOp(
                    op=floma_diff_ir.Or(),
                    left=floma_diff_ir.Var(id='x', t=floma_diff_ir.Bool()),
                    right=floma_diff_ir.Var(id='y', t=floma_diff_ir.Bool())
                )
            )
        ],
        ret_type=floma_diff_ir.Bool()
    )


    return dfloat, funcs

class CallFuncVisitor(irvisitor.IRVisitor):
    def __init__(self, builtins):
        self.called_func_ids = set()
        self.builtins : set[str] = builtins

    def visit_call(self, node):
        for arg in node.args:
            self.visit_expr(arg)

        # do nothing if it's built-in func
        # if node.id == 'sin' or \
        #     node.id == 'cos' or \
        #     node.id == 'sqrt' or \
        #     node.id == 'pow' or \
        #     node.id == 'exp' or \
        #     node.id == 'log' or \
        #     node.id == 'int2float' or \
        #     node.id == 'float2int' or \
        #     node.id == 'thread_id' or \
        #     node.id == 'atomic_add':
        #     return
        if node.id in self.builtins:
            return

        self.called_func_ids.add(node.id)

def differentiate(dfloat : floma_diff_ir.Struct,
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
    # set of builtin functions
    builtins : set[str] = {f.id for f in funcs.values() if isinstance(f, floma_diff_ir.FunctionDef) and f.builtin}

    # Map functions to their differentiated versions
    func_to_rev = dict()
    for f in funcs.values():
        if isinstance(f, floma_diff_ir.ReverseDiff):
            func_to_rev[f.primal_func] = f.id
    
    # Define derivatives for built-in functions as well
    func_to_rev['addf'] = 'd_addf'
    func_to_rev['subf'] = 'd_subf'
    func_to_rev['mulf'] = 'd_mulf'
    func_to_rev['divf'] = 'd_divf'
    func_to_rev['ifelsef'] = 'd_ifelsef'
    # Aswell as the dfloat counterparts of comparison operators
    func_to_rev['lessf'] = 'd_lessf'
    func_to_rev['less_equalf'] = 'd_less_equalf'
    func_to_rev['greaterf'] = 'd_greaterf'
    func_to_rev['greater_equalf'] = 'd_greater_equalf'
    func_to_rev['equalf'] = 'd_equalf'
    # Unless defined in autodiff.make_builtins, the 'derivative' of a builtin is itself
    for f_name in builtins:
        if f_name not in func_to_rev.keys() and f_name not in func_to_rev.values():
            func_to_rev[f_name] = f_name

    # Traverse: for each function that requires reverse diff
    # recursively having all called functions to require reverse diff
    # as well
    visited_func = set(func_to_rev.keys())
    func_stack = list(func_to_rev.keys())
    while len(func_stack) > 0:
        primal_func_id = func_stack.pop()
        primal_func = funcs[primal_func_id]
        if primal_func_id not in func_to_rev:
            rev_func_id = 'd_' + primal_func_id
            func_to_rev[primal_func_id] = rev_func_id
            funcs[rev_func_id] = floma_diff_ir.ReverseDiff(rev_func_id, primal_func_id)
        cfv = CallFuncVisitor(builtins=builtins)
        cfv.visit_function(primal_func)
        for f in cfv.called_func_ids:
            if f not in visited_func:
                visited_func.add(f)
                func_stack.append(f)

    for f in funcs.values():
        if isinstance(f, floma_diff_ir.ReverseDiff):
            rev_diff_func = reverse_diff.reverse_diff(dfloat, funcs[f.primal_func], funcs, func_to_rev)
            funcs[f.id] = rev_diff_func
            import pretty_print
            print(f'\nReverse differentiation of function {f.id}:')
            print(pretty_print.loma_to_str(rev_diff_func))

    return funcs

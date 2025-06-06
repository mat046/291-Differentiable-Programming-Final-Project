import attrs
import ir
ir.generate_asdl_file()
import _asdl.floma_diff as floma_diff_ir
import irvisitor
import compiler

def type_to_string(node : floma_diff_ir.type | floma_diff_ir.arg) -> str:
    """ Given a loma type, return a string that represents
        the type in C.
    """

    match node:
        case floma_diff_ir.Arg():
            # if isinstance(node.t, floma_diff_ir.Struct): # dfloat
            #     return type_to_string(node.t) + '*'
            return type_to_string(node.t)
        case floma_diff_ir.Int():
            return 'int'
        case floma_diff_ir.Float():
            return 'double'
        case floma_diff_ir.Bool():
            return 'bool'
        # case floma_diff_ir.Array():
        #     return type_to_string(node.t) + '*'
        case floma_diff_ir.Struct():
            return "std::shared_ptr<" + node.id + ">"
        case floma_diff_ir.Cont():
            return "const std::function<void(std::shared_ptr<_dfloat>)>&"
        case None:
            return 'void'
        case _:
            assert False

@attrs.define()
class CCodegenVisitor(irvisitor.IRVisitor):
    """ Generates C code from loma IR.
    """

    code = ''
    tab_count = 0
    funcs_defs = None

    def __init__(self, func_defs):
        self.func_defs = func_defs
        self.ret_type = None

    def emit_tabs(self):
        self.code += '\t' * self.tab_count

    def visit_function_def(self, node):
        ret_type = type_to_string(node.ret_type)
        # if node.id == 'make__const__dfloat': # make__const__dfloat needs to return an lvalue ref
        #     ret_type += '&'
        self.code += f'{ret_type} {node.id}('
        
        for i, arg in enumerate(node.args):
            if i > 0:
                self.code += ', '
            self.code += f'{type_to_string(arg)} {arg.id}'
        self.code += ') {\n'

        self.ret_type = node.ret_type
        self.tab_count += 1
        for stmt in node.body:
            self.visit_stmt(stmt)
        self.tab_count -= 1
        self.code += '}\n'

    def visit_return(self, node):
        self.emit_tabs()
        self.code += f'return {self.visit_expr(node.val)};\n'

    # def init_zero(self, id, t, depth = 0):
    #     # Initiailize the declared variable to zero
    #     if isinstance(t, floma_diff_ir.Int) or isinstance(t, floma_diff_ir.Float):
    #         self.emit_tabs()
    #         self.code += f'{id} = 0;\n'
    #     elif isinstance(t, floma_diff_ir.Struct):
    #         for m in t.members:
    #             self.init_zero(id + '.' + m.id, m.t, depth)
    #     elif isinstance(t, floma_diff_ir.Array):
    #         self.emit_tabs()
    #         iter_var_name = 'i'
    #         self.code += f'for (int _{iter_var_name * (depth + 1)} = 0;' + \
    #                      f' _{iter_var_name * (depth + 1)} < {t.static_size};' + \
    #                      f'_{iter_var_name * (depth + 1)}++) {{\n'

    #         self.tab_count += 1
    #         self.init_zero(id + f'[_{iter_var_name * (depth + 1)}]', t.t, depth + 1)
    #         self.tab_count -= 1
            
    #         self.emit_tabs()
    #         self.code += '}\n'

    def visit_declare(self, node):
        self.emit_tabs()
        # if not isinstance(node.t, floma_diff_ir.Array):
        #     self.code += f'{type_to_string(node.t)} {node.target}'
        # else:
        #     # Special rule for arrays
        #     assert node.t.static_size != None
        #     self.code += f'{type_to_string(node.t.t)} {node.target}[{node.t.static_size}]'

        # if node.is_static_var:
        #     self.code += 'thread_local '
        self.code += f'{type_to_string(node.t)} {node.target}'
        # currently, cant dyn alloc and initialize variables
        if node.dyn_alloc: # specifally for dfloats
            self.code += f' = std::make_shared<{node.t.id}>()'
        elif node.val is not None:
            self.code += f' = {self.visit_expr(node.val)}'#\n'
        self.code += ';\n'

        # else:
        #     # self.code += ';\n'
        #     # self.init_zero(node.target, node.t)
        #     assert False, "Declaration statements should initialize objects"
        

    def visit_assign(self, node):
        self.emit_tabs()
        self.code += self.visit_expr(node.target)
        expr_str = self.visit_expr(node.val)
        if expr_str != '':
            self.code += f' = {expr_str}'
        self.code += ';\n'

    def visit_ifelse(self, node):
        self.emit_tabs()
        self.code += f'if ({self.visit_expr(node.cond)}) {{\n'
        
        self.tab_count += 1
        self.visit_stmt(node.then_call)
        self.tab_count -= 1

        self.emit_tabs()
        self.code += f'}} else {{\n'

        self.tab_count += 1
        self.visit_stmt(node.else_call)
        self.tab_count -= 1

        self.emit_tabs()
        self.code += '}\n'

    # def visit_while(self, node):
    #     self.emit_tabs()
    #     self.code += f'while ({self.visit_expr(node.cond)}) {{\n'
    #     self.tab_count += 1
    #     for stmt in node.body:
    #         self.visit_stmt(stmt)
    #     self.tab_count -= 1
    #     self.emit_tabs()
    #     self.code += '}\n'

    def visit_call_stmt(self, node):
        self.emit_tabs()
        if (self.ret_type != None):
            self.code += "return "
        self.code += self.visit_expr(node.call) + ';\n'

    def visit_expr(self, node):
        match node:
            case floma_diff_ir.Var():
                # if node.id in self.byref_args:
                #     return '(*' + node.id + ')'
                # else:
                #     return node.id
                return node.id
            case floma_diff_ir.StructAccess():
                return f'({self.visit_expr(node.struct)})->{node.member_id}'
            case floma_diff_ir.ConstFloat():
                return f'(float)({node.val})'
            case floma_diff_ir.ConstInt():
                return f'(int)({node.val})'
            case floma_diff_ir.ConstBool():
                return f'(bool)({node.val})'
            case floma_diff_ir.BinaryOp():
                match node.op:
                    case floma_diff_ir.Add():
                        return f'({self.visit_expr(node.left)}) + ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Sub():
                        return f'({self.visit_expr(node.left)}) - ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Mul():
                        return f'({self.visit_expr(node.left)}) * ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Div():
                        return f'({self.visit_expr(node.left)}) / ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Less():
                        return f'({self.visit_expr(node.left)}) < ({self.visit_expr(node.right)})'
                    case floma_diff_ir.LessEqual():
                        return f'({self.visit_expr(node.left)}) <= ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Greater():
                        return f'({self.visit_expr(node.left)}) > ({self.visit_expr(node.right)})'
                    case floma_diff_ir.GreaterEqual():
                        return f'({self.visit_expr(node.left)}) >= ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Equal():
                        return f'({self.visit_expr(node.left)}) == ({self.visit_expr(node.right)})'
                    case floma_diff_ir.And():
                        return f'({self.visit_expr(node.left)}) && ({self.visit_expr(node.right)})'
                    case floma_diff_ir.Or():
                        return f'({self.visit_expr(node.left)}) || ({self.visit_expr(node.right)})'
                    case _:
                        assert False
            case floma_diff_ir.Call():
                # if node.id == 'thread_id':
                #     return '__work_id'
                # elif node.id == 'atomic_add':
                #     arg0_str = self.visit_expr(node.args[0])
                #     arg1_str = self.visit_expr(node.args[1])
                #     return f'{arg0_str} += {arg1_str}'
                func_id = node.id
                # # call the single precision versions of the intrinsic functions
                # if func_id == 'sin':
                #     func_id = 'sinf'
                # elif func_id == 'cos':
                #     func_id = 'cosf'
                # elif func_id == 'sqrt':
                #     func_id = 'sqrtf'
                # elif func_id == 'pow':
                #     func_id = 'powf'
                # elif func_id == 'exp':
                #     func_id = 'expf'
                # elif func_id == 'log':
                #     func_id = 'logf'
                # elif func_id == 'int2float':
                #     func_id = '(float)'
                # elif func_id == 'float2int':
                #     func_id = '(int)'

                ret = f'{func_id}('
                ret += ','.join([self.visit_expr(arg) for arg in node.args])
                ret += ')'
                return ret
            case floma_diff_ir.ContExpr():
                captures = '[' + ','.join([c for c in node.captures]) + ']'
                parameter = '(' + type_to_string(node.argument.t) + node.argument.id + ')'
                
                self.tab_count += 1
                tabs = '\t' * self.tab_count
                body = '\n' + tabs + "-> void{" + self.visit_expr(node.body) + ";}"
                self.tab_count -= 1

                ret = captures + parameter + body
                return ret
            case None:
                return ''
            case _:
                assert False, f'Visitor error: unhandled expression {expr}'

def codegen_c(dfloat : floma_diff_ir.Struct,
              funcs : dict[str, floma_diff_ir.func]) -> str:
    """ Given loma Structs (structs) and loma functions (funcs),
        return a string that represents the equivalent C code.

        Parameters:
        structs - a dictionary that maps the ID of a Struct to 
                the corresponding Struct
        funcs - a dictionary that maps the ID of a function to 
                the corresponding func
    """

    # sorted_structs_list = compiler.topo_sort_structs(structs)

    # Definition of structs
    code = ''
    # for s in sorted_structs_list:
    #     code += f'typedef struct {{\n'
    #     for m in s.members:
    #         # Special rule for arrays
    #         if isinstance(m.t, floma_diff_ir.Array) and m.t.static_size is not None:
    #             code += f'\t{type_to_string(m.t.t)} {m.id}[{m.t.static_size}];\n'
    #         else:
    #             code += f'\t{type_to_string(m.t)} {m.id};\n'
    #     code += f'}} {s.id};\n'

    code += f'typedef struct {{\n'
    for m in dfloat.members:
        code += f'\t{type_to_string(m.t)} {m.id};\n'
    code += f'}} {dfloat.id};\n\n'

    # Forward declaration of functions
    for f in funcs.values():
        ret_type = type_to_string(f.ret_type)
        # if f.id == 'make__const__dfloat': # make__const__dfloat needs to return an lvalue ref
        #     ret_type += '&'
        code += f'{ret_type} {f.id}('
        for i, arg in enumerate(f.args):
            if i > 0:
                code += ', '
            code += f'{type_to_string(arg)} {arg.id}'
        code += ');\n'
    code += '\n'

    for f in funcs.values():
        cg = CCodegenVisitor(funcs)
        cg.visit_function(f)
        code += cg.code
        code += '\n'

    return code

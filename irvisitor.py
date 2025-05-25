import ir
ir.generate_asdl_file()
import _asdl.floma_diff as floma_diff_ir

class IRVisitor:
    """ Visitor pattern: we use IRVisitor to traverse loma IR code,
        and visit its children.
        To use this class, you should inherit IRVisitor, and define
        your own visit functions to decide what to do.
        By default the class does nothing to the IR code.
    """

    def visit_function(self, node):
        match node:
            case floma_diff_ir.FunctionDef():
                self.visit_function_def(node)
            # case floma_diff_ir.ForwardDiff():
            #     self.visit_forward_diff(node)
            case floma_diff_ir.ReverseDiff():
                self.visit_reverse_diff(node)
            case _:
                assert False, f'Visitor error: unhandled func {node}'

    def visit_function_def(self, node):
        for stmt in node.body:
            self.visit_stmt(stmt)

    def visit_forward_diff(self, node):
        pass

    def visit_reverse_diff(self, node):
        pass

    def visit_stmt(self, node):
        match node:
            case floma_diff_ir.Return():
                self.visit_return(node)
            case floma_diff_ir.Declare():
                self.visit_declare(node)
            case floma_diff_ir.Assign():
                self.visit_assign(node)
            # case floma_diff_ir.IfElse():
            #     self.visit_ifelse(node)
            # case floma_diff_ir.While():
            #     self.visit_while(node)
            case floma_diff_ir.CallStmt():
                self.visit_call_stmt(node)
            case _:
                assert False, f'Visitor error: unhandled statement {node}'

    def visit_return(self, node):
        self.visit_expr(node.val)

    def visit_declare(self, node):
        if node.val is not None:
            self.visit_expr(node.val)

    def visit_assign(self, node):
        self.visit_expr(node.val)

    def visit_ifelse(self, node):
        self.visit_expr(node.cond)
        for stmt in node.then_stmts:
            self.visit_stmt(stmt)
        for stmt in node.else_stmts:
            self.visit_stmt(stmt)

    def visit_while(self, node):
        self.visit_expr(node.cond)
        for stmt in node.body:
            self.visit_stmt(stmt)

    def visit_call_stmt(self, node):
        self.visit_expr(node.call)

    def visit_expr(self, node):
        match node:
            case floma_diff_ir.Var():
                self.visit_var(node)
            # case floma_diff_ir.ArrayAccess():
            #     self.visit_array_access(node)
            case floma_diff_ir.StructAccess():
                self.visit_struct_access(node)
            case floma_diff_ir.ConstFloat():
                self.visit_const_float(node)
            # case floma_diff_ir.ConstInt():
            #     self.visit_const_int(node)
            case floma_diff_ir.BinaryOp():
                self.visit_binary_op(node)
            case floma_diff_ir.Call():
                self.visit_call(node)
            case floma_diff_ir.ContExpr():
                self.visit_cont_expr(node)
            case _:
                assert False, f'Visitor error: unhandled expression {node}'

    def visit_var(self, node):
        pass

    def visit_array_access(self, node):
        self.visit_expr(node.array)
        self.visit_expr(node.index)

    def visit_struct_access(self, node):
        self.visit_expr(node.struct)
        pass

    def visit_cont_expr(self, node):
        self.visit_expr(node.argument)
        self.visit_expr(node.body)

    def visit_const_float(self, node):
        pass

    def visit_const_int(self, node):
        pass

    def visit_binary_op(self, node):
        match node.op:
            case floma_diff_ir.Add():
                self.visit_add(node)
            case floma_diff_ir.Sub():
                self.visit_sub(node)
            case floma_diff_ir.Mul():
                self.visit_mul(node)
            case floma_diff_ir.Div():
                self.visit_div(node)
            case floma_diff_ir.Less():
                self.visit_less(node)
            case floma_diff_ir.LessEqual():
                self.visit_less_equal(node)
            case floma_diff_ir.Greater():
                self.visit_greater(node)
            case floma_diff_ir.GreaterEqual():
                self.visit_greater_equal(node)
            case floma_diff_ir.Equal():
                self.visit_equal(node)
            case floma_diff_ir.And():
                self.visit_and(node)
            case floma_diff_ir.Or():
                self.visit_or(node)

    def visit_add(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_sub(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_mul(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_div(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_less(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_less_equal(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_greater(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_greater_equal(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_equal(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_and(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_or(self, node):
        self.visit_expr(node.left)
        self.visit_expr(node.right)

    def visit_call(self, node):
        for arg in node.args:
            self.visit_expr(arg)

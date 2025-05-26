from __future__ import annotations 

import ir
ir.generate_asdl_file()
import _asdl.floma_diff as floma_diff_ir
import irmutator
import autodiff
import string
import random
import copy

# From https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def random_id_generator(size=6, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def reverse_diff(#diff_func_id : str,
                #  structs : dict[str, floma_diff_ir.Struct],
                #  funcs : dict[str, floma_diff_ir.func],
                #  diff_structs : dict[str, floma_diff_ir.Struct],
                 dfloat : floma_diff_ir.Struct,
                 func : floma_diff_ir.FunctionDef,
                 funcs_dict : dict[str, floma_diff_ir.func],
                 func_to_rev : dict[str, str]) -> floma_diff_ir.FunctionDef:
    """ Given a primal loma function func, apply reverse differentiation
        and return a function that computes the total derivative of func.

        For example, given the following function:
        def square(x : In[float]) -> float:
            return x * x
        and let diff_func_id = 'd_square', reverse_diff() should return
        def d_square(x : In[float], _dx : Out[float], _dreturn : float):
            _dx = _dx + _dreturn * x + _dreturn * x

        Parameters:
        diff_func_id - the ID of the returned function
        structs - a dictionary that maps the ID of a Struct to 
                the corresponding Struct
        funcs - a dictionary that maps the ID of a function to 
                the corresponding func
        diff_structs - a dictionary that maps the ID of the primal
                Struct to the corresponding differential Struct
                e.g., diff_structs['float'] returns _dfloat
        func - the function to be differentiated
        func_to_rev - mapping from primal function ID to its reverse differentiation
    """

    # Some utility functions you can use for your homework.
    def type_to_string(t):
        match t:
            # case floma_diff_ir.Int():
            #     return 'int'
            case floma_diff_ir.Float():
                return 'float'
            # case floma_diff_ir.Array():
            #     return 'array_' + type_to_string(t.t)
            case floma_diff_ir.Struct():
                return t.id
            case _:
                assert False

    # def assign_zero(target):
    #     match target.t:
    #         case floma_diff_ir.Int():
    #             return []
    #         case floma_diff_ir.Float():
    #             return [floma_diff_ir.Assign(target, floma_diff_ir.ConstFloat(0.0))]
    #         case floma_diff_ir.Struct():
    #             s = target.t
    #             stmts = []
    #             for m in s.members:
    #                 target_m = floma_diff_ir.StructAccess(
    #                     target, m.id, t = m.t)
    #                 if isinstance(m.t, floma_diff_ir.Float):
    #                     stmts += assign_zero(target_m)
    #                 elif isinstance(m.t, floma_diff_ir.Int):
    #                     pass
    #                 elif isinstance(m.t, floma_diff_ir.Struct):
    #                     stmts += assign_zero(target_m)
    #                 else:
    #                     assert isinstance(m.t, floma_diff_ir.Array)
    #                     assert m.t.static_size is not None
    #                     for i in range(m.t.static_size):
    #                         target_m = floma_diff_ir.ArrayAccess(
    #                             target_m, floma_diff_ir.ConstInt(i), t = m.t.t)
    #                         stmts += assign_zero(target_m)
    #             return stmts
    #         case _:
    #             assert False

    # def accum_deriv(target, deriv, overwrite):
    #     match target.t:
    #         case floma_diff_ir.Int():
    #             return []
    #         case floma_diff_ir.Float():
    #             if overwrite:
    #                 return [floma_diff_ir.Assign(target, deriv)]
    #             else:
    #                 return [floma_diff_ir.Assign(target,
    #                     floma_diff_ir.BinaryOp(floma_diff_ir.Add(), target, deriv))]
    #         case floma_diff_ir.Struct():
    #             s = target.t
    #             stmts = []
    #             for m in s.members:
    #                 target_m = floma_diff_ir.StructAccess(
    #                     target, m.id, t = m.t)
    #                 deriv_m = floma_diff_ir.StructAccess(
    #                     deriv, m.id, t = m.t)
    #                 if isinstance(m.t, floma_diff_ir.Float):
    #                     stmts += accum_deriv(target_m, deriv_m, overwrite)
    #                 elif isinstance(m.t, floma_diff_ir.Int):
    #                     pass
    #                 elif isinstance(m.t, floma_diff_ir.Struct):
    #                     stmts += accum_deriv(target_m, deriv_m, overwrite)
    #                 else:
    #                     assert isinstance(m.t, floma_diff_ir.Array)
    #                     assert m.t.static_size is not None
    #                     for i in range(m.t.static_size):
    #                         target_m = floma_diff_ir.ArrayAccess(
    #                             target_m, floma_diff_ir.ConstInt(i), t = m.t.t)
    #                         deriv_m = floma_diff_ir.ArrayAccess(
    #                             deriv_m, floma_diff_ir.ConstInt(i), t = m.t.t)
    #                         stmts += accum_deriv(target_m, deriv_m, overwrite)
    #             return stmts
    #         case _:
    #             assert False

    # # A utility class that you can use for HW3.
    # # This mutator normalizes each call expression into
    # # f(x0, x1, ...)
    # # where x0, x1, ... are all floma_diff_ir.Var or 
    # # floma_diff_ir.ArrayAccess or floma_diff_ir.StructAccess
    # # Furthermore, it normalizes all Assign statements
    # # with a function call
    # # z = f(...)
    # # into a declaration followed by an assignment
    # # _tmp : [z's type]
    # # _tmp = f(...)
    # # z = _tmp
    # class CallNormalizeMutator(irmutator.IRMutator):
    #     def mutate_function_def(self, node):
    #         self.tmp_count = 0
    #         self.tmp_declare_stmts = []
    #         new_body = [self.mutate_stmt(stmt) for stmt in node.body]
    #         new_body = irmutator.flatten(new_body)

    #         new_body = self.tmp_declare_stmts + new_body

    #         return floma_diff_ir.FunctionDef(\
    #             node.id, node.args, new_body, node.is_simd, node.ret_type, lineno = node.lineno)

    #     def mutate_return(self, node):
    #         self.tmp_assign_stmts = []
    #         val = self.mutate_expr(node.val)
    #         return self.tmp_assign_stmts + [floma_diff_ir.Return(\
    #             val,
    #             lineno = node.lineno)]

    #     def mutate_declare(self, node):
    #         self.tmp_assign_stmts = []
    #         val = None
    #         if node.val is not None:
    #             val = self.mutate_expr(node.val)
    #         return self.tmp_assign_stmts + [floma_diff_ir.Declare(\
    #             node.target,
    #             node.t,
    #             val,
    #             lineno = node.lineno)]

    #     def mutate_assign(self, node):
    #         self.tmp_assign_stmts = []
    #         target = self.mutate_expr(node.target)
    #         self.has_call_expr = False
    #         val = self.mutate_expr(node.val)
    #         if self.has_call_expr:
    #             # turn the assignment into a declaration plus
    #             # an assignment
    #             self.tmp_count += 1
    #             tmp_name = f'_call_t_{self.tmp_count}_{random_id_generator()}'
    #             self.tmp_count += 1
    #             self.tmp_declare_stmts.append(floma_diff_ir.Declare(\
    #                 tmp_name,
    #                 target.t,
    #                 lineno = node.lineno))
    #             tmp_var = floma_diff_ir.Var(tmp_name, t = target.t)
    #             assign_tmp = floma_diff_ir.Assign(\
    #                 tmp_var,
    #                 val,
    #                 lineno = node.lineno)
    #             assign_target = floma_diff_ir.Assign(\
    #                 target,
    #                 tmp_var,
    #                 lineno = node.lineno)
    #             return self.tmp_assign_stmts + [assign_tmp, assign_target]
    #         else:
    #             return self.tmp_assign_stmts + [floma_diff_ir.Assign(\
    #                 target,
    #                 val,
    #                 lineno = node.lineno)]

    #     def mutate_call_stmt(self, node):
    #         self.tmp_assign_stmts = []
    #         call = self.mutate_expr(node.call)
    #         return self.tmp_assign_stmts + [floma_diff_ir.CallStmt(\
    #             call,
    #             lineno = node.lineno)]

    #     def mutate_call(self, node):
    #         self.has_call_expr = True
    #         new_args = []
    #         for arg in node.args:
    #             if not isinstance(arg, floma_diff_ir.Var) and \
    #                     not isinstance(arg, floma_diff_ir.ArrayAccess) and \
    #                     not isinstance(arg, floma_diff_ir.StructAccess):
    #                 arg = self.mutate_expr(arg)
    #                 tmp_name = f'_call_t_{self.tmp_count}_{random_id_generator()}'
    #                 self.tmp_count += 1
    #                 tmp_var = floma_diff_ir.Var(tmp_name, t = arg.t)
    #                 self.tmp_declare_stmts.append(floma_diff_ir.Declare(\
    #                     tmp_name, arg.t))
    #                 self.tmp_assign_stmts.append(floma_diff_ir.Assign(\
    #                     tmp_var, arg))
    #                 new_args.append(tmp_var)
    #             else:
    #                 new_args.append(arg)
    #         return floma_diff_ir.Call(node.id, new_args, t = node.t)

    # HW2 happens here. Modify the following IR mutators to perform
    # reverse differentiation.

    class ParentChildCallPair:
        """
        Keeps track of which function-call instances call other function-call instances

        Example:
        add(sub(x,y),mul(x,y))
        ->
        (call pair for the add and sub function calls)
        {
            child=<sub call instance>
            parent=<add call instance>
            arg_idx=0  # sub is the 0th index in the add call
        }
        """
        def __init__(self, child, parent, arg_idx):
            self.child_ : floma_diff_ir.Call = child
            self.parent_ : floma_diff_ir.Call = parent
            self.arg_idx_ : int = arg_idx

        @staticmethod
        def get_call_pairs_and_mutate_signatures(parent : floma_diff_ir.Call) -> tuple[list[ParentChildCallPair], floma_diff_ir.Call]:
            """
            The body of the function to be differentiated is a bunch of nested function calls.
            We need to traverse these functions in a particular order while differentiating.
            The returned list denotes this order.

            We also mutate the name of the functions to their differentiated counterpart
            and add the continuation argument to them.
            """
            
            if not isinstance(parent, floma_diff_ir.Call):
                new_node = copy.deepcopy(parent)
                return [], new_node
            
            pccp_list = []
            new_args = []

            # get list of call pairs from nested function calls, as well as mutated arguments
            for arg in parent.args:
                new_list, new_arg = ParentChildCallPair.get_call_pairs_and_mutate_signatures(arg)
                pccp_list += new_list
                new_args.append(new_arg)
            
            # add continuation lambda to arguments
            t = funcs_dict[parent.id].ret_type
            if isinstance(t, floma_diff_ir.Float):
                continuation = floma_diff_ir.Var(
                    id='k', 
                    t=floma_diff_ir.Cont(arg_type=dfloat)
                )
                new_args.append(continuation)

            # get new parent function call
            new_parent = floma_diff_ir.Call(
                id=func_to_rev[parent.id],
                args=new_args,
                lineno=parent.lineno,
                t=None
            )
            
            # create new parent child call pair
            for idx, arg in enumerate(new_parent.args):
                if not isinstance(arg, floma_diff_ir.Call):
                    continue

                pccp = ParentChildCallPair(child=arg, parent=new_parent, arg_idx=idx)
                pccp_list = [pccp] + pccp_list

            
            return pccp_list, new_parent


    # Apply the differentiation.
    class RevDiffMutator(irmutator.IRMutator):
        def __init__(self):
            # The mutated function body will turn into a series of nested functions (lambdas)
            # self.head is the 'front', or outer-most function call
            self.head_ : floma_diff_ir.Call

            self.call_pairs_ : list[ParentChildCallPair]

            # The nested lambda functions will need to close on variables from outer scopes
            # Inner lambdas will have to close on the parameters from outer lambdas
            # This helps us keep track of the order in which lambdas are nested
            self.conts_ : list[floma_diff_ir.ContExpr] = []

            self.lambda_count_ : int = 0

            self.params_ : list[str] = []

        def mutate_args(self, node):
            new_args = []
            for arg in node.args:
                new_arg : floma_diff_ir.Arg
                match arg.t:
                    case floma_diff_ir.Float():
                        new_arg = floma_diff_ir.Arg(id=arg.id, t=dfloat)
                    case _:
                        assert False, f"Unrecognized type for arg {arg}"
                new_args.append(new_arg)
                self.params_.append(new_arg.id)
            
            assert node.ret_type != None # should be caught in parser.py, but just in case
            new_arg : floma_diff_ir.Arg
            match node.ret_type:
                case floma_diff_ir.Float():
                    new_arg = floma_diff_ir.Arg(
                        id='k',
                        t=floma_diff_ir.Cont(arg_type=dfloat)
                    )
                case _:
                    assert False, f'Unsupported return type for function {node.id}'
            new_args.append(new_arg)
            self.params_.append(new_arg.id)
            node.ret_type = None

            return new_args

        def mutate_function_def(self, node):
            # Mutate arguments
            new_args = self.mutate_args(node)
            
            # Mutate body
            assert len(node.body) == 1, f'Malformed function body in {node.id}. Functions should just be an expression'
            new_body = self.mutate_stmt(node.body[0])

            # Return differentiated function
            new_func = floma_diff_ir.FunctionDef(
                id=func_to_rev[func.id],
                args=new_args,
                body=[new_body],
                ret_type=None,
                lineno=node.lineno
            )
            return new_func

        # def mutate_ifelse(self, node):
        #     # HW3: TODO
        #     return super().mutate_ifelse(node)

        def mutate_call_stmt(self, node):
            self.call_pairs_, self.head_ = ParentChildCallPair.get_call_pairs_and_mutate_signatures(node.call)
            self.conts_ = []
            self.lambda_count_ = 0

            new_call = self.mutate_expr(node.call)
            new_call_stmt = floma_diff_ir.CallStmt(
                call=new_call
            )
            return new_call_stmt

        # def mutate_const_float(self, node):
        #     # TODO:
        #     assert False, "Need to implement mutate_const_float"

        # def mutate_const_int(self, node):
        #     # HW2: TODO
        #     return super().mutate_const_int(node)

        # def mutate_var(self, node):
        #     # HW2: TODO
        #     return super().mutate_var(node)

        def mutate_call(self, node):
            for pccp in self.call_pairs_:
                new_head = pccp.child_
                old_parent = pccp.parent_
                arg_idx = pccp.arg_idx_

                lambda_param_name = f"t{self.lambda_count_}"
                self.lambda_count_ += 1
                lambda_param = floma_diff_ir.Var(
                    id=lambda_param_name,
                    t=dfloat
                )

                # Pull redex out of the expression
                old_parent.args[arg_idx] = lambda_param

                # turn continuation into a lambda
                new_cont = floma_diff_ir.ContExpr(
                    argument=lambda_param,
                    captures=[],
                    body=self.head_,
                    t=None
                )

                # plug continuation lambda into (new) redex function
                self.head_ = new_head
                self.head_.args[-1] = new_cont
                

                # propogate captures
                new_cont.captures = copy.deepcopy(self.params_)
                for c in self.conts_:
                    c.captures.append(lambda_param_name)
                self.conts_ = [new_cont] + self.conts_
            
            return self.head_

    return RevDiffMutator().mutate_function_def(func)

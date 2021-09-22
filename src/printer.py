from expr import (
    ExprVisitor,
    Expr,
    Assign,
    Binary,
    Unary,
    Call,
    Get,
    Grouping,
    Literal,
    Logical,
    Set,
    Super,
    This,
    Variable,
)


class ASTPrinter(ExprVisitor):
    def make_str(self, expr: "Expr") -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, *exprs: "Expr") -> str:
        str_exprs = " ".join([str(x.accept(self)) for x in exprs])
        return f"({name} {str_exprs})"

    def visit_assign_expr(self, expr: "Assign") -> str:
        print("Implement me please!")

    def visit_binary_expr(self, expr: "Binary") -> str:
        return self._parenthesize(expr.operator.token_type.value, expr.left, expr.right)

    def visit_call_expr(self, expr: "Call") -> str:
        print("Implement me please!")

    def visit_get_expr(self, expr: "Get") -> str:
        print("Implement me please!")

    def visit_grouping_expr(self, expr: "Grouping") -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: "Literal") -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_logical_expr(self, expr: "Logical") -> str:
        print("Implement me please!")

    def visit_set_expr(self, expr: "Set") -> str:
        print("Implement me please!")

    def visit_super_expr(self, expr: "Super") -> str:
        print("Implement me please!")

    def visit_this_expr(self, expr: "This") -> str:
        print("Implement me please!")

    def visit_unary_expr(self, expr: "Unary") -> str:
        return self._parenthesize(expr.operator.token_type.value, expr.right)

    def visit_variable_expr(self, expr: "Variable") -> str:
        print("Implement me please!")

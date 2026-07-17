from sympy import (
    symbols, diff, integrate, limit, series, Symbol,
    solve, Function, Eq, dsolve, sympify, pi, E, oo,
    sin, cos, tan, log, ln, exp, sqrt, Abs,
    factorial, binomial, simplify, trigsimp,
    apart, together, factor, expand,
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

LOCAL_DICT = {
    "pi": pi,
    "e": E,
    "E": E,
    "oo": oo,
    "inf": oo,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "log": log,
    "ln": ln,
    "exp": exp,
    "sqrt": sqrt,
    "abs": Abs,
    "factorial": factorial,
    "binomial": binomial,
}


def safe_parse(expr_str: str):
    expr_str = expr_str.strip()
    return parse_expr(
        expr_str,
        local_dict=LOCAL_DICT,
        transformations=TRANSFORMATIONS,
    )


class CalculusSolver:

    def differentiate(self, expr_str: str, var_str: str = "x", order: int = 1):
        expr = safe_parse(expr_str)
        var = Symbol(var_str)
        result = diff(expr, var, order)
        return {
            "operation": "differentiation",
            "input": expr_str,
            "variable": var_str,
            "order": order,
            "result": result,
            "result_str": str(result),
        }

    def integrate_def(self, expr_str: str, var_str: str = "x", lower=None, upper=None):
        expr = safe_parse(expr_str)
        var = Symbol(var_str)
        if lower is not None and upper is not None:
            lower = safe_parse(str(lower))
            upper = safe_parse(str(upper))
            result = integrate(expr, (var, lower, upper))
        else:
            result = integrate(expr, var)
        return {
            "operation": "integration",
            "input": expr_str,
            "variable": var_str,
            "lower": str(lower) if lower is not None else None,
            "upper": str(upper) if upper is not None else None,
            "definite": lower is not None and upper is not None,
            "result": result,
            "result_str": str(result),
        }

    def compute_limit(self, expr_str: str, var_str: str = "x", point="0", direction="+"):
        expr = safe_parse(expr_str)
        var = Symbol(var_str)
        pt = safe_parse(point)
        if direction == "+":
            result = limit(expr, var, pt, "+")
        elif direction == "-":
            result = limit(expr, var, pt, "-")
        else:
            result = limit(expr, var, pt)
        return {
            "operation": "limit",
            "input": expr_str,
            "variable": var_str,
            "point": point,
            "direction": direction,
            "result": result,
            "result_str": str(result),
        }

    def taylor_expand(self, expr_str: str, var_str: str = "x", point="0", order: int = 6):
        expr = safe_parse(expr_str)
        var = Symbol(var_str)
        pt = safe_parse(point)
        result = series(expr, var, pt, order)
        result_simplified = result.removeO()
        return {
            "operation": "taylor_series",
            "input": expr_str,
            "variable": var_str,
            "point": point,
            "order": order,
            "result": result,
            "result_simplified": result_simplified,
            "result_str": str(result),
        }

    def solve_ode(self, eq_str: str, func_name: str = "y", var_str: str = "x"):
        var = Symbol(var_str)
        func = Function(func_name)(var)

        ode_local = dict(LOCAL_DICT)
        ode_local[func_name] = Function(func_name)

        eq_str_clean = eq_str.strip()
        if "=" in eq_str_clean:
            lhs_str, rhs_str = eq_str_clean.split("=", 1)
            lhs = parse_expr(lhs_str, local_dict=ode_local, transformations=TRANSFORMATIONS)
            rhs = parse_expr(rhs_str, local_dict=ode_local, transformations=TRANSFORMATIONS)
            eq = Eq(lhs, rhs)
        else:
            eq = Eq(parse_expr(eq_str_clean, local_dict=ode_local, transformations=TRANSFORMATIONS), 0)

        hints_to_try = [
            "nth_linear_constant_coeff_homogeneous",
            "nth_linear_constant_coeff_undetermined_coefficients",
            "nth_linear_euler_eq_homogeneous",
            "separable",
            "linear",
            "1st_homogeneous_coeff_best",
            "default",
        ]

        solution = None
        last_error = None
        for hint in hints_to_try:
            try:
                solution = dsolve(eq, func, hint=hint)
                break
            except Exception:
                last_error = hint
                continue

        if solution is None:
            try:
                solution = dsolve(eq, func)
            except Exception as e:
                raise RuntimeError(f"Could not solve ODE (tried hints: {hints_to_try}). Error: {e}")

        return {
            "operation": "ode",
            "input": eq_str,
            "function": func_name,
            "variable": var_str,
            "result": solution,
            "result_str": str(solution),
        }

    def simplify_expr(self, expr_str: str):
        expr = safe_parse(expr_str)
        result = simplify(expr)
        return {
            "operation": "simplify",
            "input": expr_str,
            "result": result,
            "result_str": str(result),
        }

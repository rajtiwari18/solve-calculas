from sympy import latex as sympy_latex


class LatexRenderer:

    @staticmethod
    def to_latex(expr, **kwargs):
        return sympy_latex(expr, **kwargs)

    @staticmethod
    def render_diff(result: dict) -> dict:
        inp = result["input"]
        var = result["variable"]
        order = result.get("order", 1)
        res = result["result"]

        if order > 1:
            numerator = f"d^{{{order}}}"
            denominator = f"d{var}^{{{order}}}"
        else:
            numerator = "d"
            denominator = f"d{var}"

        latex_input = f"\\frac{{{numerator}}}{{{denominator}}} \\left({inp}\\right)"
        latex_result = sympy_latex(res)

        return {
            "latex_input": latex_input,
            "latex_result": latex_result,
            "latex_full": f"{latex_input} = {latex_result}",
        }

    @staticmethod
    def render_integral(result: dict) -> dict:
        inp = result["input"]
        var = result["variable"]
        res = result["result"]

        if result.get("definite"):
            lower = result["lower"]
            upper = result["upper"]
            latex_input = f"\\int_{{{lower}}}^{{{upper}}} {inp} \\, d{var}"
        else:
            latex_input = f"\\int {inp} \\, d{var}"

        latex_result = sympy_latex(res)

        return {
            "latex_input": latex_input,
            "latex_result": latex_result,
            "latex_full": f"{latex_input} = {latex_result}",
        }

    @staticmethod
    def render_limit(result: dict) -> dict:
        inp = result["input"]
        var = result["variable"]
        point = result["point"]
        direction = result["direction"]
        res = result["result"]

        dir_symbol = ""
        if direction == "+":
            dir_symbol = "^{+}"
        elif direction == "-":
            dir_symbol = "^{-}"

        latex_input = f"\\lim_{{{var} \\to {point}{dir_symbol}}} {inp}"
        latex_result = sympy_latex(res)

        return {
            "latex_input": latex_input,
            "latex_result": latex_result,
            "latex_full": f"{latex_input} = {latex_result}",
        }

    @staticmethod
    def render_taylor(result: dict) -> dict:
        inp = result["input"]
        var = result["variable"]
        point = result["point"]
        order = result["order"]
        res = result["result"]

        latex_input = f"\\text{{Taylor}}\\left({inp}, {var}, {point}, {order}\\right)"
        latex_result = sympy_latex(res)

        return {
            "latex_input": latex_input,
            "latex_result": latex_result,
            "latex_full": f"{latex_input} = {latex_result}",
        }

    @staticmethod
    def render_ode(result: dict) -> dict:
        inp = result["input"]
        res = result["result"]

        latex_input = f"\\text{{ODE: }} {inp}"
        latex_result = sympy_latex(res)

        return {
            "latex_input": latex_input,
            "latex_result": latex_result,
            "latex_full": f"{latex_input} \\implies {latex_result}",
        }

    @classmethod
    def render(cls, result: dict) -> dict:
        op = result["operation"]
        renderers = {
            "differentiation": cls.render_diff,
            "integration": cls.render_integral,
            "limit": cls.render_limit,
            "taylor_series": cls.render_taylor,
            "ode": cls.render_ode,
            "simplify": lambda r: {
                "latex_input": sympy_latex(r["result"].free_symbols.pop()) if r["result"].free_symbols else r["input"],
                "latex_result": sympy_latex(r["result"]),
                "latex_full": sympy_latex(r["result"]),
            },
        }

        renderer = renderers.get(op)
        if renderer:
            latex_info = renderer(result)
            result.update(latex_info)
        else:
            result["latex_result"] = sympy_latex(result["result"])
            result["latex_full"] = result["latex_result"]

        return result

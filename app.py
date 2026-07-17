#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from solver import CalculusSolver, LatexRenderer

app = Flask(__name__)
solver = CalculusSolver()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/solve", methods=["POST"])
def solve():
    data = request.get_json()
    operation = data.get("operation", "")
    expression = data.get("expression", "")
    variable = data.get("variable", "x")

    try:
        if operation == "diff":
            order = int(data.get("order", 1))
            result = solver.differentiate(expression, variable, order)

        elif operation == "integ":
            lower = data.get("lower")
            upper = data.get("upper")
            if lower and upper:
                result = solver.integrate_def(expression, variable, lower, upper)
            else:
                result = solver.integrate_def(expression, variable)

        elif operation == "limit":
            point = data.get("point", "0")
            direction = data.get("direction", "=")
            result = solver.compute_limit(expression, variable, point, direction)

        elif operation == "taylor":
            point = data.get("point", "0")
            order = int(data.get("order", 6))
            result = solver.taylor_expand(expression, variable, point, order)

        elif operation == "ode":
            result = solver.solve_ode(expression, data.get("func", "y"), variable)

        elif operation == "simplify":
            result = solver.simplify_expr(expression)

        else:
            return jsonify({"error": f"Unknown operation: {operation}"}), 400

        latex = LatexRenderer.render(result)
        return jsonify({
            "success": True,
            "result": result["result_str"],
            "latex_input": latex.get("latex_input", ""),
            "latex_result": latex.get("latex_result", ""),
            "latex_full": latex.get("latex_full", ""),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)

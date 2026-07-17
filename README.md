# Calculus Solver — LaTeX Edition

A powerful calculus equation solver with LaTeX rendering, available in both terminal and web interfaces.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![SymPy](https://img.shields.io/badge/SymPy-1.12+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Differentiation** — Compute derivatives of any order
- **Integration** — Both definite and indefinite integrals
- **Limits** — One-sided and two-sided limits
- **Taylor Series** — Expand functions around any point
- **ODE Solving** — Solve ordinary differential equations
- **Simplify** — Simplify mathematical expressions
- **LaTeX Output** — Beautiful mathematical notation in terminal and web

## Demo

### Terminal

```bash
$ python cli.py "diff sin(x)*x**2 w.r.t x"

╭───────────────────────────────── Derivative ─────────────────────────────────╮
│ LaTeX:  \frac{d}{dx} \left(sin(x)*x**2\right) = x^{2} \cos(x) + 2x \sin(x) │
│ Result:  x**2*cos(x) + 2*x*sin(x)                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### Web

```bash
$ python app.py
# Open http://localhost:5000
```

Beautiful dark-themed web interface with live LaTeX rendering powered by KaTeX.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/rajtiwari18/solve-calculas.git
cd solve-calculas
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Terminal (CLI)

Start the interactive REPL:
```bash
python cli.py
```

Or run a single command:
```bash
python cli.py "diff sin(x)*x**2 w.r.t x"
```

#### CLI Commands

| Command | Syntax | Example |
|---------|--------|---------|
| `diff` | `diff <expr> w.r.t <var> [order N]` | `diff x**3 w.r.t x order 2` |
| `integ` | `integ <expr> w.r.t <var> [from A to B]` | `integ sin(x) w.r.t x from 0 to pi` |
| `limit` | `limit <expr> w.r.t <var> at <point> [from +/-]` | `limit sin(x)/x w.r.t x at 0` |
| `taylor` | `taylor <expr> w.r.t <var> at <point> order N` | `taylor exp(x) w.r.t x at 0 order 6` |
| `ode` | `ode <equation>` | `ode diff(y(x),x) = y(x)` |
| `simpl` | `simpl <expr>` | `simpl sin(x)**2 + cos(x)**2` |
| `help` | `help` | Show all commands |
| `quit` | `quit` | Exit the REPL |

### Web Interface

Start the Flask server:
```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000`.

Features:
- Tabbed interface for different operations
- Live expression preview
- Beautiful dark theme
- One-click LaTeX copy button
- Responsive design

## API

The web interface uses a REST API. You can also call it directly:

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"operation": "diff", "expression": "sin(x)*x**2", "variable": "x", "order": 1}'
```

### API Endpoints

**POST /api/solve**

Request body:
```json
{
  "operation": "diff|integ|limit|taylor|ode|simplify",
  "expression": "sin(x) * x**2",
  "variable": "x",
  "order": 1,
  "lower": "0",
  "upper": "pi",
  "point": "0",
  "direction": "="
}
```

Response:
```json
{
  "success": true,
  "result": "x**2*cos(x) + 2*x*sin(x)",
  "latex_input": "\\frac{d}{dx} \\left(sin(x) * x**2\\right)",
  "latex_result": "x^{2} \\cos{\\left(x \\right)} + 2 x \\sin{\\left(x \\right)}",
  "latex_full": "\\frac{d}{dx} \\left(sin(x) * x**2\\right) = x^{2} \\cos{\\left(x \\right)} + 2 x \\sin{\\left(x \\right)}"
}
```

## Examples

### Differentiation
```bash
# First derivative
python cli.py "diff sin(x)*x**2 w.r.t x"

# Second derivative
python cli.py "diff exp(x)*cos(x) w.r.t x order 2"
```

### Integration
```bash
# Indefinite integral
python cli.py "integ x**2 w.r.t x"

# Definite integral
python cli.py "integ sin(x) w.r.t x from 0 to pi"
```

### Limits
```bash
# Basic limit
python cli.py "limit sin(x)/x w.r.t x at 0"

# One-sided limit
python cli.py "limit 1/x w.r.t x at 0 from +"
```

### Taylor Series
```bash
# Taylor expansion around 0
python cli.py "taylor exp(x) w.r.t x at 0 order 6"

# Taylor expansion around different point
python cli.py "taylor sin(x) w.r.t x at pi/4 order 4"
```

### ODE Solving
```bash
# First-order ODE
python cli.py "ode diff(y(x),x) = y(x)"

# Second-order ODE
python cli.py "ode Derivative(y(x),(x,2)) + y(x) = 0"
```

## Project Structure

```
calculas-solver/
├── app.py                  # Flask web server + API
├── cli.py                  # Terminal REPL with Rich
├── solver/
│   ├── __init__.py         # Package exports
│   ├── core.py             # SymPy calculus engine
│   └── latex_renderer.py   # LaTeX rendering utilities
├── templates/
│   └── index.html          # Web UI template
├── static/
│   ├── css/
│   │   └── style.css       # Dark theme styling
│   └── js/
│       └── app.js          # Frontend logic
└── requirements.txt        # Python dependencies
```

## Technologies Used

- **Python** — Core language
- **SymPy** — Symbolic mathematics library
- **Flask** — Web framework
- **Rich** — Beautiful terminal formatting
- **KaTeX** — Fast LaTeX rendering in browser

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SymPy](https://www.sympy.org/) for the powerful symbolic mathematics engine
- [KaTeX](https://katex.org/) for beautiful LaTeX rendering
- [Rich](https://github.com/Textualize/rich) for terminal formatting

## Author

**Raj Tiwari** - [GitHub](https://github.com/rajtiwari18)

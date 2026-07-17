#!/usr/bin/env python3
import sys
import shlex
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.text import Text

from solver import CalculusSolver, LatexRenderer

console = Console()
solver = CalculusSolver()

HELP_TEXT = """
## Calculus Solver — Commands

| Command | Example |
|---------|---------|
| `diff`  | `diff sin(x)*x**2 w.r.t x` |
| `diff`  | `diff x**3 w.r.t x order 2` |
| `integ` | `integ x**2 w.r.t x` |
| `integ` | `integ sin(x) w.r.t x from 0 to pi` |
| `limit` | `limit sin(x)/x w.r.t x at 0` |
| `limit` | `limit 1/x w.r.t x at 0 from +` |
| `taylor`| `taylor exp(x) w.r.t x at 0 order 6` |
| `ode`   | `ode Derivative(y(x),(x,2)) + y(x) = 0` |
| `ode`   | `ode diff(y(x),x) = y(x)` |
| `simpl` | `simpl sin(x)**2 + cos(x)**2` |
| `help`  | Show this help |
| `quit`  | Exit |
"""


def format_latex_terminal(latex_str: str) -> str:
    return latex_str


def cmd_diff(args: str):
    parts = args.split("w.r.t")
    if len(parts) < 2:
        console.print("[red]Usage: diff <expr> w.r.t <var> [order N][/red]")
        return
    expr_str = parts[0].strip()
    rest = parts[1].strip()
    rest_parts = rest.split("order")
    var_str = rest_parts[0].strip()
    order = int(rest_parts[1].strip()) if len(rest_parts) > 1 else 1

    result = solver.differentiate(expr_str, var_str, order)
    latex = LatexRenderer.render(result)
    console.print(Panel(
        f"[bold cyan]LaTeX:[/bold cyan]  {latex['latex_full']}\n\n"
        f"[bold green]Result:[/bold green]  {result['result_str']}",
        title="[bold]Derivative[/bold]",
        border_style="blue",
    ))


def cmd_integ(args: str):
    parts = args.split("w.r.t")
    if len(parts) < 2:
        console.print("[red]Usage: integ <expr> w.r.t <var> [from A to B][/red]")
        return
    expr_str = parts[0].strip()
    rest = parts[1].strip()

    lower, upper = None, None
    if "from" in rest:
        var_and_range = rest.split("from")
        var_str = var_and_range[0].strip()
        range_parts = var_and_range[1].strip().split("to")
        lower = range_parts[0].strip()
        upper = range_parts[1].strip() if len(range_parts) > 1 else None
    else:
        var_str = rest.strip()

    result = solver.integrate_def(expr_str, var_str, lower, upper)
    latex = LatexRenderer.render(result)
    console.print(Panel(
        f"[bold cyan]LaTeX:[/bold cyan]  {latex['latex_full']}\n\n"
        f"[bold green]Result:[/bold green]  {result['result_str']}",
        title="[bold]Integral[/bold]",
        border_style="blue",
    ))


def cmd_limit(args: str):
    parts = args.split("w.r.t")
    if len(parts) < 2:
        console.print("[red]Usage: limit <expr> w.r.t <var> at <point> [from +/-][/red]")
        return
    expr_str = parts[0].strip()
    rest = parts[1].strip()

    direction = "="
    if "from" in rest:
        rest, dir_part = rest.split("from")
        direction = dir_part.strip()

    var_and_point = rest.split("at")
    var_str = var_and_point[0].strip()
    point = var_and_point[1].strip() if len(var_and_point) > 1 else "0"

    result = solver.compute_limit(expr_str, var_str, point, direction)
    latex = LatexRenderer.render(result)
    console.print(Panel(
        f"[bold cyan]LaTeX:[/bold cyan]  {latex['latex_full']}\n\n"
        f"[bold green]Result:[/bold green]  {result['result_str']}",
        title="[bold]Limit[/bold]",
        border_style="blue",
    ))


def cmd_taylor(args: str):
    parts = args.split("w.r.t")
    if len(parts) < 2:
        console.print("[red]Usage: taylor <expr> w.r.t <var> at <point> order N[/red]")
        return
    expr_str = parts[0].strip()
    rest = parts[1].strip()

    order = 6
    if "order" in rest:
        rest, order_part = rest.split("order")
        order = int(order_part.strip())

    var_and_point = rest.split("at")
    var_str = var_and_point[0].strip()
    point = var_and_point[1].strip() if len(var_and_point) > 1 else "0"

    result = solver.taylor_expand(expr_str, var_str, point, order)
    latex = LatexRenderer.render(result)
    console.print(Panel(
        f"[bold cyan]LaTeX:[/bold cyan]  {latex['latex_full']}\n\n"
        f"[bold green]Result:[/bold green]  {result['result_str']}",
        title="[bold]Taylor Series[/bold]",
        border_style="blue",
    ))


def cmd_ode(args: str):
    result = solver.solve_ode(args.strip())
    latex = LatexRenderer.render(result)
    console.print(Panel(
        f"[bold cyan]LaTeX:[/bold cyan]  {latex['latex_full']}\n\n"
        f"[bold green]Result:[/bold green]  {result['result_str']}",
        title="[bold]ODE Solution[/bold]",
        border_style="blue",
    ))


def cmd_simpl(args: str):
    result = solver.simplify_expr(args.strip())
    latex = LatexRenderer.render(result)
    console.print(Panel(
        f"[bold cyan]LaTeX:[/bold cyan]  {latex['latex_full']}\n\n"
        f"[bold green]Result:[/bold green]  {result['result_str']}",
        title="[bold]Simplified[/bold]",
        border_style="blue",
    ))


COMMANDS = {
    "diff": cmd_diff,
    "integ": cmd_integ,
    "limit": cmd_limit,
    "taylor": cmd_taylor,
    "ode": cmd_ode,
    "simpl": cmd_simpl,
}


def print_banner():
    banner = """
[bold blue]╔══════════════════════════════════════════╗
║       Calculus Solver — LaTeX Edition     ║
╚══════════════════════════════════════════╝[/bold blue]

[dim]Type [bold]help[/bold] for commands, [bold]quit[/bold] to exit.[/dim]
"""
    console.print(banner)


def repl():
    print_banner()
    while True:
        try:
            user_input = Prompt.ask("[bold magenta]calc>[/bold magenta]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        user_input = user_input.strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            console.print("[dim]Goodbye![/dim]")
            break
        if user_input.lower() == "help":
            console.print(Markdown(HELP_TEXT))
            continue

        cmd_name = user_input.split()[0].lower()
        cmd_args = user_input[len(cmd_name):].strip()

        if cmd_name in COMMANDS:
            try:
                COMMANDS[cmd_name](cmd_args)
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")
        else:
            console.print(f"[red]Unknown command:[/red] {cmd_name}. Type [bold]help[/bold] for available commands.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        cmd_name = user_input.split()[0].lower()
        cmd_args = user_input[len(cmd_name):].strip()
        if cmd_name in COMMANDS:
            try:
                COMMANDS[cmd_name](cmd_args)
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")
                sys.exit(1)
        else:
            console.print(f"[red]Unknown command:[/red] {cmd_name}")
            sys.exit(1)
    else:
        repl()

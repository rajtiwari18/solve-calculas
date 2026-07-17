document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const expressionInput = document.getElementById("expression");
    const exprPreview = document.getElementById("expr-preview");
    const solveBtn = document.getElementById("solve-btn");
    const resultSection = document.getElementById("result-section");
    const errorSection = document.getElementById("error-section");
    const copyBtn = document.getElementById("copy-btn");

    let currentOp = "diff";

    // Tab switching
    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            tabs.forEach((t) => t.classList.remove("active"));
            tab.classList.add("active");
            currentOp = tab.dataset.op;

            document.querySelectorAll(".params").forEach((p) => p.classList.add("hidden"));
            const paramEl = document.getElementById(`params-${currentOp}`);
            if (paramEl) paramEl.classList.remove("hidden");
        });
    });

    // Live preview
    expressionInput.addEventListener("input", () => {
        const val = expressionInput.value.trim();
        if (val) {
            exprPreview.textContent = `f(${getVariable()}) = ${val}`;
        } else {
            exprPreview.textContent = "";
        }
    });

    function getVariable() {
        const varInputs = {
            diff: "diff-var",
            integ: "integ-var",
            limit: "limit-var",
            taylor: "taylor-var",
            ode: "ode-var",
        };
        const el = document.getElementById(varInputs[currentOp]);
        return el ? el.value : "x";
    }

    // Definite integral toggle
    const integDefCheck = document.getElementById("integ-definite");
    const integBounds = document.getElementById("integ-bounds");
    if (integDefCheck) {
        integDefCheck.addEventListener("change", () => {
            integBounds.style.display = integDefCheck.checked ? "grid" : "none";
        });
    }

    // Solve
    solveBtn.addEventListener("click", solve);
    expressionInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") solve();
    });

    async function solve() {
        const expression = expressionInput.value.trim();
        if (!expression) {
            showError("Please enter an expression.");
            return;
        }

        solveBtn.disabled = true;
        solveBtn.textContent = "Solving...";

        const body = { operation: currentOp, expression, variable: getVariable() };

        if (currentOp === "diff") {
            body.order = document.getElementById("diff-order").value;
        } else if (currentOp === "integ") {
            if (integDefCheck.checked) {
                body.lower = document.getElementById("integ-lower").value;
                body.upper = document.getElementById("integ-upper").value;
            }
        } else if (currentOp === "limit") {
            body.point = document.getElementById("limit-point").value;
            body.direction = document.getElementById("limit-dir").value;
        } else if (currentOp === "taylor") {
            body.point = document.getElementById("taylor-point").value;
            body.order = document.getElementById("taylor-order").value;
        } else if (currentOp === "ode") {
            body.func = document.getElementById("ode-func").value;
        }

        try {
            const res = await fetch("/api/solve", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });
            const data = await res.json();

            if (!res.ok || !data.success) {
                showError(data.error || "Unknown error");
                return;
            }

            hideError();

            const inputEl = document.getElementById("result-input");
            const outputEl = document.getElementById("result-output");
            const latexSource = document.getElementById("latex-source");

            inputEl.textContent = "";
            outputEl.textContent = "";
            latexSource.textContent = data.latex_full;

            katex.render(data.latex_input || data.result, inputEl, {
                throwOnError: false,
                displayMode: true,
            });

            katex.render(data.latex_full, outputEl, {
                throwOnError: false,
                displayMode: true,
            });

            resultSection.style.display = "block";
            resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
        } catch (err) {
            showError(err.message);
        } finally {
            solveBtn.disabled = false;
            solveBtn.textContent = "Solve";
        }
    }

    function showError(msg) {
        document.getElementById("error-msg").textContent = msg;
        errorSection.style.display = "block";
        resultSection.style.display = "none";
    }

    function hideError() {
        errorSection.style.display = "none";
    }

    // Copy LaTeX
    copyBtn.addEventListener("click", () => {
        const source = document.getElementById("latex-source").textContent;
        navigator.clipboard.writeText(source).then(() => {
            copyBtn.textContent = "Copied!";
            setTimeout(() => (copyBtn.textContent = "Copy LaTeX"), 1500);
        });
    });
});

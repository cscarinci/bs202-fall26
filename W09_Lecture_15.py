import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 15 · Covariance and correlation", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys
    from fractions import Fraction

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, Fraction, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(15, "Covariance and correlation")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    d_x = lk.slider(-0.75, 0.75, step=0.05, value=0.5, label="$x$")
    v_sx = lk.slider(1, 2, step=0.1, value=2, label=r"$\sigma_X$")
    v_sy = lk.slider(1, 2, step=0.1, value=1.5, label=r"$\sigma_Y$")
    v_rho = lk.slider(-1, 1, step=0.05, value=0.5, label=r"$\rho_{X,Y}$")
    g_a = lk.slider(-2, 2, step=0.1, value=1, label="$a$")
    g_b = lk.slider(0, 2, step=0.1, value=1, label="$b$")
    # one fixed sample of (X, Y), X, Y ~ N(0, 1) independent (fixed seed); moving a or b keeps it
    g_xy = np.random.default_rng(1515).standard_normal((2, 400))
    return d_x, g_a, g_b, g_xy, v_rho, v_sx, v_sy


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Joint distributions &nbsp; $f_{X,Y}(x, y)$

        Marginal distributions &nbsp; $f_X(x)$, $f_Y(y)$

        Conditional distributions &nbsp; $f_{Y|X}(y \mid x) = \dfrac{f_{X,Y}(x, y)}{f_X(x)}$

        > $\leadsto$ &nbsp; independence: &nbsp; $f_{X,Y}(x, y) = f_X(x) \, f_Y(y)$

        > $\leadsto$ &nbsp; conditional expectation
        """,
        lk.aside(
            r"> > $E[u(Y) \mid X = x] = \displaystyle\sum_y u(y) \, f_{Y|X}(y \mid x)$",
            r"expected value of $u(Y)$ given<br>the measured value of $X = x$",
        ),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"How strongly are $X$ and $Y$ related?", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 5.5–5.8")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # section
    lk.section("Expectations of functions of two random variables")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # definition: expectation of u(X, Y)
    lk.definition(
        [
            r"Given $u : \mathbb{R}^2 \longrightarrow \mathbb{R}$ bivariate function",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \mk{E[u(X, Y)]} &= \sum_x \sum_y u(x, y) \, f_{X,Y}(x, y)\\[4pt]
                \text{or} \quad &= \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} u(x, y) \, f_{X,Y}(x, y) \, dx \, dy
                \end{aligned}
                $$
                """,
                [(1, r"$E[u(X, Y)]$ = expectation of $u(X, Y)$")],
                rows=2,
            ),
        ],
        label="def-expectation",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # theorem: properties of expectations
    lk.theorem(
        r"""
        > • &nbsp; $E[a \, u(X, Y) + b \, v(X, Y)] = a \, E[u(X, Y)] + b \, E[v(X, Y)]$

        > • &nbsp; $E[u(X) \, v(Y)] = E[u(X)] \, E[v(Y)]$ &nbsp; if $X, Y$ independent
        """,
        title="properties of expectations",
        label="thm-expectations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # proof: second property
    lk.proof(
        [
            lk.aside(
                r"""
                $$
                \begin{aligned}
                E[u(X) \, v(Y)] &= \sum_x \sum_y u(x) \, v(y) \, f_{X,Y}(x, y)\\
                &\mathrel{\mk{=}} \sum_x \sum_y u(x) \, v(y) \, f_X(x) \, f_Y(y)\\
                &= \sum_x u(x) \, f_X(x) \sum_y v(y) \, f_Y(y) = E[u(X)] \, E[v(Y)]
                \end{aligned}
                $$
                """,
                "independence",
                rows=3,
                at=2,
            ),
        ],
        title="of the second property",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariance
    # section
    lk.section("Covariance")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariance
    # definition: covariance
    lk.definition(
        r"""
        Given $X, Y$ random variables on $(S, \mathcal{E}, P)$

        $$
        \sigma_{X,Y} = \mathrm{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)]
        $$

        is called the **covariance** of $X$ and $Y$

        > $\leadsto$ &nbsp; $\mu_X = E[X]$, $\mu_Y = E[Y]$ means of $X$, $Y$
        """,
        label="def-covariance",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: covariance
    # prose: the four quadrants
    # the quadrants about (mu_X, mu_Y)
    _fig = Figure(figsize=(3.0, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(1.5, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.axhline(1.2, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    for _q, _xy, _color in (("Q1", (2.3, 1.95), lk.BLUE), ("Q2", (0.75, 1.95), lk.RED), ("Q3", (0.75, 0.55), lk.BLUE), ("Q4", (2.3, 0.55), lk.RED)):
        _ax.text(*_xy, _q, color=_color, fontsize=13, ha="center", va="center")
    _ax.set_xlim(0, 3)
    _ax.set_ylim(0, 2.5)
    _ax.set_xticks([1.5], [r"$\mu_X$"])
    _ax.set_yticks([1.2], [r"$\mu_Y$"])
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$y$", rotation=0, labelpad=10)
    _ax.tick_params(labelsize=12)
    lk.prose(
        lk.side(
            lk.figure(_fig),
            r"""
            Q1: &nbsp; $(x - \mu_X)(y - \mu_Y) > 0$

            Q2: &nbsp; $(x - \mu_X)(y - \mu_Y) < 0$

            Q3: &nbsp; $(x - \mu_X)(y - \mu_Y) > 0$

            Q4: &nbsp; $(x - \mu_X)(y - \mu_Y) < 0$
            """,
        ),
        r"""
        $\leadsto$ &nbsp; if $\mathrm{Cov}(X, Y) > 0$ we expect to see values of $(X, Y)$ in Q1 and Q3

        > $\leadsto$ &nbsp; $X$ and $Y$ get large or small together!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariance
    # theorem: properties of covariance
    lk.theorem(
        [
            r"""
            $$
            \mathrm{Cov}(X, Y) = E[XY] - \mu_X \mu_Y
            $$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \mathrm{Cov}(X, X) &= \mathrm{Var}(X) = \mk{\sigma_X^2}\\
                \mathrm{Cov}(Y, Y) &= \mathrm{Var}(Y) = \mk{\sigma_Y^2}
                \end{aligned}
                $$
                """,
                "maybe this makes the<br>squares more natural",
            ),
            "Also:",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \mathrm{Cov}(X, Y) &= \mathrm{Cov}(Y, X)\\
                \mathrm{Cov}(aX + bY, Z) &= a \, \mathrm{Cov}(X, Z) + b \, \mathrm{Cov}(Y, Z)\\
                \mathrm{Cov}(X, Y) &= 0 \quad \text{if } X, Y \text{ are independent}
                \end{aligned}
                $$
                """,
                [(1, "symmetric"), (2, "bilinear")],
                rows=3,
            ),
        ],
        label="thm-covariance",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariance
    # prose: inner product
    lk.prose(
        r"""
        $\leadsto$ &nbsp; $\mathrm{Cov}$ is like an inner product and independent random variables are orthogonal!

        <span class="lk-ghost">$\leadsto$ &nbsp;</span>$\mathrm{Var}$ is like length squared! &nbsp; (However, some non-zero random variables have zero variance!)
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariance
    # remark: zero covariance
    lk.remark(r"Not every pair $(X, Y)$ of random variables with $\mathrm{Cov}(X, Y) = 0$ is independent!")
    return


@app.cell(hide_code=True)
def _(Figure, d_x, lk, np):
    # module: covariance
    # example: uniform on a square
    # left: S_{X,Y} with its slice X = x; right: the conditional pdf of Y given X = x, uniform on the slice, against
    # the marginal pdf of Y
    _x = d_x.value
    _h = 1 - abs(_x)
    _top = 2.0
    _fig = Figure(figsize=(5.8, 2.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, gridspec_kw={"width_ratios": [1, 1.4]})
    _left.fill([1, 0, -1, 0], [0, 1, 0, -1], facecolor=lk.LIGHT, edgecolor=lk.GREY, lw=1.0)
    _left.axhline(0, color="black", lw=0.8)
    _left.axvline(0, color="black", lw=0.8)
    _left.plot([_x, _x], [-_h, _h], color=lk.BLUE, lw=2.4, solid_capstyle="butt")
    _left.annotate("$x$", (_x, -_h), textcoords="offset points", xytext=(4, -6), color=lk.BLUE, fontsize=12, ha="left", va="top")
    _left.text(-0.62, 0.78, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    for _v, _xy, _off in (("$1$", (1, 0), (4, -10)), ("$-1$", (-1, 0), (-4, -10)), ("$1$", (0, 1), (5, 2)), ("$-1$", (0, -1), (5, -2))):
        _left.annotate(_v, _xy, textcoords="offset points", xytext=_off, fontsize=12, ha="left" if _off[0] > 0 else "right", va="center")
    _left.set_xlim(-1.25, 1.25)
    _left.set_ylim(-1.25, 1.25)
    _left.set_aspect("equal")
    _left.axis("off")
    _yy = np.linspace(-1, 1, 401)
    _right.fill_between([-_h, _h], 0, 1 / (2 * _h), color=lk.LIGHT, lw=0)
    _right.plot([-1.1, -_h, -_h, _h, _h, 1.1], [0, 0, 1 / (2 * _h), 1 / (2 * _h), 0, 0], color=lk.BLUE, lw=1.4)
    _right.plot(_yy, 1 - np.abs(_yy), color=lk.RED, lw=1.2)
    _right.plot([0, 0], [0, 1.08 * _top], color=lk.GREEN, lw=1.2, ls=(0, (4, 3)))
    _right.text(0, 1.1 * _top, r"$E[Y \mid X = x]$", color=lk.GREEN, fontsize=12, ha="center", va="bottom")
    _right.text(1.1, 1.15 * _top, r"$f_{Y|X}(y \mid x)$", color=lk.BLUE, fontsize=12, ha="right", va="top")
    _right.text(1.1, 0.97 * _top, r"$f_Y(y)$", color=lk.RED, fontsize=12, ha="right", va="top")
    _right.set_xlim(-1.1, 1.1)
    _right.set_ylim(0, 1.2 * _top)
    _right.set_yticks([0, 0.5, 1, 1.5, 2])
    _right.set_xlabel("$y$")
    _right.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _right.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _right.tick_params(labelsize=12)
    lk.example(
        [
            r"""
            $(X, Y)$ uniform on $S_{X,Y} = \{ (x, y) \mid |x| + |y| < 1 \}$

            > $\Longrightarrow$ &nbsp; $f_{X,Y}(x, y) = c = {\large\tfrac{1}{2}}$

            $$
            \begin{aligned}
            \Longrightarrow \quad & \begin{cases} f_X(x) = \displaystyle\int_{-(1 - |x|)}^{1 - |x|} \frac{1}{2} \, dy = 1 - |x|, & |x| < 1\\[14pt] f_Y(y) = \displaystyle\int_{-(1 - |y|)}^{1 - |y|} \frac{1}{2} \, dx = 1 - |y|, & |y| < 1 \end{cases}\\[10pt]
            \Longrightarrow \quad & \begin{cases} \mu_X = E[X] = \displaystyle\int_{-1}^{1} x (1 - |x|) \, dx = 0\\[14pt] \mu_Y = E[Y] = \displaystyle\int_{-1}^{1} y (1 - |y|) \, dy = 0 \end{cases}\\[10pt]
            \Longrightarrow \quad & \sigma_{X,Y} = E[XY] - \mu_X \mu_Y = \int_{-1}^{1} \int_{-(1 - |x|)}^{1 - |x|} xy \, \frac{1}{2} \, dy \, dx\\[4pt]
            & \phantom{\sigma_{X,Y} = E[XY] - \mu_X \mu_Y} = \int_{-1}^{1} x \, \underbrace{\frac{y^2}{4} \bigg|_{-(1 - |x|)}^{1 - |x|}}_{=\, 0} \, dx = 0
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            But, &nbsp; $f_{X,Y}(x, y) = {\large\tfrac{1}{2}} \neq f_X(x) \, f_Y(y) = (1 - |x|)(1 - |y|)$ &nbsp; for most $(x, y) \in S_{X,Y}$
            """,
            lk.interactive(_fig, controls=[d_x]),
        ],
        label="ex-square",
    )
    return


@app.cell(hide_code=True)
def _(Figure, Fraction, lk):
    # module: covariance
    # example: two 4-sided dice
    # each pair (x, y) with its probability (dot area), blue where it adds to the covariance, red where it subtracts
    _n, _N = 4, 16
    _counts = {}
    for _i in range(1, _n + 1):
        for _j in range(1, _n + 1):
            _counts[(max(_i, _j), _i + _j)] = _counts.get((max(_i, _j), _i + _j), 0) + 1
    _mx = Fraction(sum(x * k for (x, y), k in _counts.items()), _N)
    _my = Fraction(sum(y * k for (x, y), k in _counts.items()), _N)
    _part = {xy: (xy[0] - _mx) * (xy[1] - _my) * Fraction(k, _N) for xy, k in _counts.items()}
    _plus = sum((p for p in _part.values() if p > 0), Fraction(0))
    _minus = sum((p for p in _part.values() if p < 0), Fraction(0))
    _fig = Figure(figsize=(4.6, 3.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(float(_mx), color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.axhline(float(_my), color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    for (_x, _y), _k in _counts.items():
        _p = _part[(_x, _y)]
        _ax.scatter(_x, _y, s=2000 * _k / _N, color=lk.BLUE if _p > 0 else lk.RED if _p < 0 else lk.GREY, lw=0, zorder=3)
    for _q, _xy, _ha, _va, _color in (("Q1", (0.99, 0.98), "right", "top", lk.BLUE), ("Q2", (0.01, 0.98), "left", "top", lk.RED), ("Q3", (0.01, 0.02), "left", "bottom", lk.BLUE), ("Q4", (0.99, 0.02), "right", "bottom", lk.RED)):
        _ax.text(*_xy, _q, transform=_ax.transAxes, color=_color, fontsize=13, ha=_ha, va=_va)
    _ax.text(float(_mx), 2 * _n + 0.9, r"$\mu_X$", color=lk.GREY, fontsize=12, ha="center", va="bottom")
    _ax.text(_n + 0.85, float(_my), r"$\mu_Y$", color=lk.GREY, fontsize=12, ha="left", va="center")
    _ax.set_xlim(0.3, _n + 0.7)
    _ax.set_ylim(1.2, 2 * _n + 0.8)
    _ax.set_xticks(range(1, _n + 1))
    _ax.set_yticks(range(2, 2 * _n + 1))
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$y$")
    _ax.tick_params(labelsize=12)
    lk.example(
        [
            r"""
            $X$ = largest face, &nbsp; $Y$ = sum of faces

            | $f_{X,Y}(x, y)$ | $x = 1$ | $2$ | $3$ | $4$ | $f_Y(y)$ |
            |:--:|:--:|:--:|:--:|:--:|:--:|
            | $y = 8$ | $0$ | $0$ | $0$ | $1/16$ | $1/16$ |
            | $7$ | $0$ | $0$ | $0$ | $2/16$ | $2/16$ |
            | $6$ | $0$ | $0$ | $1/16$ | $2/16$ | $3/16$ |
            | $5$ | $0$ | $0$ | $2/16$ | $2/16$ | $4/16$ |
            | $4$ | $0$ | $1/16$ | $2/16$ | $0$ | $3/16$ |
            | $3$ | $0$ | $2/16$ | $0$ | $0$ | $2/16$ |
            | $2$ | $1/16$ | $0$ | $0$ | $0$ | $1/16$ |
            | $f_X(x)$ | $1/16$ | $3/16$ | $5/16$ | $7/16$ | $1$ |
            """,
            lk.aside(
                r"""
                $$
                \begin{alignedat}{2}
                E[X] &= 1 \cdot \frac{1}{16} + 2 \cdot \frac{3}{16} + 3 \cdot \frac{5}{16} + 4 \cdot \frac{7}{16} &&{}= \frac{50}{16}\\[4pt]
                E[Y] &= 2 \cdot \frac{1}{16} + 3 \cdot \frac{2}{16} + 4 \cdot \frac{3}{16} + 5 \cdot \frac{4}{16}\\
                &\hphantom{{}={}} + 6 \cdot \frac{3}{16} + 7 \cdot \frac{2}{16} + 8 \cdot \frac{1}{16} &&{}= \frac{80}{16}\\[4pt]
                E[XY] &= 1 \cdot 2 \cdot \frac{1}{16} + 2 \cdot 3 \cdot \frac{2}{16} + 2 \cdot 4 \cdot \frac{1}{16}\\
                &\hphantom{{}={}} + 3 \cdot 4 \cdot \frac{2}{16} + \dots + 4 \cdot 8 \cdot \frac{1}{16} &&{}= \frac{270}{16}\\[4pt]
                \Longrightarrow \quad \mathrm{Cov}(X, Y) &= \sigma_{X,Y} = \frac{270 - 50 \cdot 5}{16} = \frac{5}{4} > 0
                \end{alignedat}
                $$
                """,
                "big largest face goes<br>together with big sum",
                at="last",
            ),
            lk.interactive(
                _fig,
                readout=lk.table(
                    [
                        (r"contributions $(x - \mu_X)(y - \mu_Y) \, f_{X,Y}(x, y)$ from Q1 and Q3", rf"${float(_plus):.2f}$"),
                        (r"contributions from Q2 and Q4", rf"${float(_minus):.4f}$"),
                    ]
                ),
            ),
        ],
        title="two 4-sided dice",
        label="ex-dice",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: variance of a sum
    # theorem: variance of a linear combination
    lk.theorem(
        r"""
        Given $X, Y$ random variables on $(S, \mathcal{E}, P)$, &nbsp; $a, b \in \mathbb{R}$

        $$
        \mathrm{Var}(aX + bY) = a^2 \, \mathrm{Var}(X) + b^2 \, \mathrm{Var}(Y) + 2ab \, \mathrm{Cov}(X, Y)
        $$
        """,
        label="thm-var-sum",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: variance of a sum
    # proof
    lk.proof(
        r"""
        $$
        \begin{aligned}
        \mathrm{Var}(aX + bY) &= \mathrm{Cov}(aX + bY, aX + bY)\\
        &= a^2 \, \mathrm{Cov}(X, X) + b^2 \, \mathrm{Cov}(Y, Y) + 2ab \, \mathrm{Cov}(X, Y)
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: variance of a sum
    # corollary: independent
    lk.corollary(
        [
            "If $X, Y$ are independent",
            lk.aside(
                r"""
                $$
                \mathrm{Var}(aX + bY) = a^2 \, \mathrm{Var}(X) + b^2 \, \mathrm{Var}(Y)
                $$
                """,
                "like Pythagoras!",
            ),
        ],
        label="cor-var-independent",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: correlation
    # section
    lk.section("Correlation")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: correlation
    # definition: correlation
    lk.definition(
        [
            r"Given $X, Y$ random variables on $(S, \mathcal{E}, P)$",
            lk.aside(
                r"""
                $$
                \rho_{X,Y} = \mk{\frac{\sigma_{X,Y}}{\sigma_X \, \sigma_Y}} = \textbf{correlation} \text{ between } X \text{ and } Y
                $$
                """,
                "normalized covariance in<br>units of standard deviations<br>(for $\sigma_X, \sigma_Y > 0$)",
            ),
        ],
        label="def-correlation",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: correlation
    # example: two 4-sided dice, correlation
    lk.example(
        r"""
        $$
        \left.
        \begin{aligned}
        \mathrm{Var}(X) &= \sigma_X^2 = \frac{55}{64}\\[6pt]
        \mathrm{Var}(Y) &= \sigma_Y^2 = \frac{5}{2}
        \end{aligned}
        \ \right\} \quad \rho_{X,Y} = \frac{5/4}{\sqrt{\dfrac{55}{64} \cdot \dfrac{5}{2}}} = \sqrt{\frac{8}{11}} \approx 0.85
        $$
        """,
        title="two 4-sided dice",
        label="ex-dice-rho",
    )
    return


@app.cell(hide_code=True)
def _(Figure, g_a, g_b, g_xy, lk, math, np, v_rho, v_sx, v_sy):
    # module: correlation
    # theorem: range of the correlation
    # top: X and Y as vectors of lengths sigma_X, sigma_Y at the angle theta with cos(theta) = rho, and X + Y, whose
    # length squared is Var(X + Y); bottom: 400 simulated values of (X, Z), Z = aX + bY
    def _vector(ax, tip, color, label, turn=0):
        dx, dy = tip
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            lk.arrow(ax, (0, 0), tip, color)
            d = math.atan2(dy, dx) + math.radians(turn)
        from matplotlib.textpath import TextPath

        ext = TextPath((0, 0), label, size=13).get_extents()
        c, s = math.cos(d), math.sin(d)
        ax.annotate(label, tip, textcoords="offset points", xytext=(c * (5 + ext.width / 2), s * (5 + ext.height / 2)), ha="center", va="center", color=color, fontsize=13, zorder=5)

    _sx, _sy, _rho = v_sx.value, v_sy.value, round(v_rho.value, 2) + 0.0
    _th = math.acos(_rho)
    _X, _Y = (_sx, 0.0), (round(_sy * math.cos(_th), 9), round(_sy * math.sin(_th), 9))
    _S = (round(_X[0] + _Y[0], 9), _Y[1])
    _fv = Figure(figsize=(5.6, 2.45), layout="constrained")
    _av = _fv.subplots()
    _av.set_xlim(-2.4, 4.4)
    _av.set_ylim(-0.45, 2.45)
    _av.set_aspect("equal")
    _av.axis("off")
    _av.plot([_X[0], _S[0]], [_X[1], _S[1]], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _av.plot([_Y[0], _S[0]], [_Y[1], _S[1]], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    if _rho == 0:
        _av.plot([0.2, 0.2, 0], [0, 0.2, 0.2], color=lk.GREY, lw=1.0)
    elif _rho < 1:
        _t = np.linspace(0, _th, 60)
        _av.plot(0.4 * np.cos(_t), 0.4 * np.sin(_t), color=lk.GREY, lw=1.0)
        _sd = math.atan2(_S[1], _S[0])
        _m = _th / 2 if _rho == -1 else (_sd + _th) / 2 if _sx >= _sy else _sd / 2
        _av.text(0.65 * math.cos(_m), 0.65 * math.sin(_m), r"$\theta$", color=lk.GREY, fontsize=13, ha="center", va="center")
    _vector(_av, _S, lk.GREEN, r"$X + Y$", turn=(-135 if _S == (0, 0) else -90) if _rho == -1 else math.degrees(_th / 2 - math.atan2(_S[1], _S[0])))
    for _args in sorted([(_X, lk.BLUE, "$X$", -40), (_Y, lk.RED, "$Y$", 40)], key=lambda _v: -math.hypot(*_v[0])):
        _vector(_av, _args[0], _args[1], _args[2], turn=_args[3])

    _a, _b = round(g_a.value, 1) + 0.0, round(g_b.value, 1) + 0.0
    _Xs, _Ys = g_xy
    _Z = _a * _Xs + _b * _Ys
    _prod = _Xs * _Z
    _fs = Figure(figsize=(4.0, 3.9), layout="constrained")
    _as = _fs.subplots()
    _as.axvline(0, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _as.axhline(0, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    for _mask, _color in ((_prod > 0, lk.BLUE), (_prod < 0, lk.RED), (_prod == 0, lk.GREY)):
        _as.scatter(_Xs[_mask], _Z[_mask], s=9, color=_color, lw=0, zorder=3)
    for _q, _xy, _ha, _va, _color in (("Q1", (0.99, 0.98), "right", "top", lk.BLUE), ("Q2", (0.01, 0.98), "left", "top", lk.RED), ("Q3", (0.01, 0.02), "left", "bottom", lk.BLUE), ("Q4", (0.99, 0.02), "right", "bottom", lk.RED)):
        _as.text(*_xy, _q, transform=_as.transAxes, color=_color, fontsize=13, ha=_ha, va=_va)
    _lim = 3.5 * max(1.0, math.sqrt(_a**2 + _b**2))
    _as.set_xlim(-_lim, _lim)
    _as.set_ylim(-_lim, _lim)
    _as.set_aspect("equal")
    _as.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _as.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _as.set_xlabel("$x$")
    _as.set_ylabel("$z$", rotation=0, labelpad=10)
    _as.tick_params(labelsize=12)
    _vz = _a**2 + _b**2
    lk.theorem(
        [
            r"Given $X, Y$ random variables on $(S, \mathcal{E}, P)$ with $\sigma_X, \sigma_Y > 0$",
            lk.aside(r"$$\rho_{X,Y} \in [-1, 1]$$", "cosine of the “angle”<br>between $X$, $Y$"),
            "and",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \rho_{X,Y} = 1 \quad &\Longleftrightarrow \quad Y = aX + b \ \text{ with } a > 0\\[2pt]
                \rho_{X,Y} = -1 \quad &\Longleftrightarrow \quad Y = aX + b \ \text{ with } a < 0
                \end{aligned}
                $$
                """,
                "linear relation",
            ),
            lk.interactive(
                _fv,
                controls=[v_sx, v_sy, v_rho],
            ),
            lk.gap(),
            r"400 simulated values of $(X, Z)$, &nbsp; $Z = aX + bY$ &nbsp; with $X, Y \sim \mathcal{N}(0, 1)$ independent",
            lk.interactive(
                _fs,
                controls=[g_a, g_b],
                readout=lk.table([(r"$\rho_{X,Z} = a / \sqrt{a^2 + b^2}$", rf"${_a / math.sqrt(_vz):.2f}$" if _vz > 0 else "undefined")]),
            ),
        ],
        label="thm-rho-range",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: correlation
    # example: customer arrivals
    # S_{X,Y} above the line y = x, the slice at x and the point (x, y)
    _fig = Figure(figsize=(2.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill_between([0, 3], [0, 3], 3, color=lk.LIGHT, lw=0)
    _ax.plot([0, 3], [0, 3], color=lk.GREY, lw=1.0)
    _ax.plot([1, 1], [1, 3], color=lk.RED, lw=1.6)
    _ax.plot(1, 2.1, "o", color="black", ms=4, zorder=4)
    _ax.annotate("$(x, y)$", (1, 2.1), textcoords="offset points", xytext=(6, 2), fontsize=12, ha="left", va="bottom")
    _ax.text(2.3, 2.75, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    _ax.set_xlim(0, 3)
    _ax.set_ylim(0, 3)
    _ax.set_aspect("equal")
    _ax.set_xticks([1], ["$x$"])
    _ax.set_yticks([1, 2.1], ["$x$", "$y$"])
    _ax.tick_params(labelsize=12)
    lk.example(
        [
            lk.aside(
                r"$X$ = arrival time of 1st customer $\sim \mathrm{Gamma}(1, \mk{\lambda})$",
                r"average rate $\lambda > 0$",
            ),
            r"""
            $Y$ = arrival time of 2nd customer $\sim \mathrm{Gamma}(2, \lambda)$

            > $\leadsto$ &nbsp; $f_{X,Y}(x, y) = \lambda^2 e^{-\lambda y}$, &nbsp; $0 < x < y$

            > $\leadsto$ &nbsp; $f_{Y|X}(y \mid x) = \lambda e^{-\lambda (y - x)}$, &nbsp; $y > x$

            <span class="lk-tab" style="--lk-tab: 13em">$\mu_X = E[X] = 1/\lambda$</span>$\mu_Y = E[Y] = 2/\lambda$

            <span class="lk-tab" style="--lk-tab: 13em">$\sigma_X^2 = \mathrm{Var}(X) = 1/\lambda^2$</span>$\sigma_Y^2 = \mathrm{Var}(Y) = 2/\lambda^2$

            $\sigma_{X,Y} = \mathrm{Cov}(X, Y) = E[XY] - \mu_X \mu_Y$

            $$
            \begin{aligned}
            E[XY] &= \int_{S_{X,Y}} xy \, \underbrace{f_{X,Y}(x, y)}_{f_{Y|X}(y \mid x) \, f_X(x)} \, dx \, dy\\[2pt]
            &= \int_0^{\infty} x \left( \int_x^{\infty} y \, f_{Y|X}(y \mid x) \, dy \right) f_X(x) \, dx\\[4pt]
            &= \int_0^{\infty} x \left( \int_x^{\infty} y \, \lambda e^{-\lambda (y - x)} \, dy \right) \lambda e^{-\lambda x} \, dx\\[4pt]
            &= \int_0^{\infty} x \left( x + \frac{1}{\lambda} \right) \lambda e^{-\lambda x} \, dx = E[X^2] + \frac{1}{\lambda} E[X]\\[4pt]
            &= \frac{2}{\lambda^2} + \frac{1}{\lambda^2} = \frac{3}{\lambda^2}\\[6pt]
            \Longrightarrow \quad \mathrm{Cov}(X, Y) &= \frac{1}{\lambda^2}, \quad \rho_{X,Y} = \frac{1/\lambda^2}{\sqrt{2/\lambda^4}} = \frac{1}{\sqrt{2}}
            \end{aligned}
            $$
            """,
            lk.figure(_fig),
        ],
        title="customer arrivals",
        label="ex-arrivals",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # section
    lk.section("Practice")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: joint pmf
    lk.exercise(
        r"""
        Let $X, Y$ have joint pmf

        $$
        f_{X,Y}(x, y) = \begin{cases} 0.4 & \text{if } (x, y) = (0, 0) \text{ or } (1, 1)\\ 0.1 & \text{if } (x, y) = (0, 1) \text{ or } (1, 0)\\ 0 & \text{otherwise} \end{cases}
        $$

        Find:

        a) marginal pmfs of $X$ and of $Y$

        > $\leadsto$ &nbsp; are $X$ and $Y$ independent?

        b) conditional pmf of $Y$ given $X = 1$

        > $\leadsto$ &nbsp; conditional expectation of $Y$ given $X = 1$?

        c) covariance and correlation of $X$ and $Y$

        d) $\mathrm{Var}(X + Y)$
        """,
        label="ex-joint-pmf",
    )
    return


if __name__ == "__main__":
    app.run()

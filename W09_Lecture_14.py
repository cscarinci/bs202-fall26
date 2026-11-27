import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 14 · Joint and conditional distributions", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys
    from fractions import Fraction

    import marimo as mo
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap, PowerNorm
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, Fraction, LinearSegmentedColormap, PowerNorm, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(14, "Joint and conditional distributions")
    return


@app.cell(hide_code=True)
def _(LinearSegmentedColormap, PowerNorm, lk):
    # Helpers of this lecture: the two dice, a joint pdf drawn as a density, and the axes of a joint distribution with
    # its marginals in the margins

    def dice_counts(n):
        """Number of outcomes, out of n^2, of two fair n-sided dice for each pair (largest face, sum)."""
        counts = {}
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                counts[(max(i, j), i + j)] = counts.get((max(i, j), i + j), 0) + 1
        return counts

    def density(ax, f, extent, top):
        """The joint pdf values `f` (NaN outside the state space) as a density: white where it is 0, blue where it
        reaches `top`, on a square-root scale so that the tail stays visible."""
        cmap = LinearSegmentedColormap.from_list("density", ["white", lk.BLUE])
        ax.imshow(f, origin="lower", extent=extent, cmap=cmap, norm=PowerNorm(0.5, vmin=0, vmax=top), aspect="auto", interpolation="bilinear")

    def margins(fig):
        """The main axes of a joint distribution with the axes of its two marginals above and to the right."""
        grid = fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 3])
        main = fig.add_subplot(grid[1, 0])
        top = fig.add_subplot(grid[0, 0], sharex=main)
        side = fig.add_subplot(grid[1, 1], sharey=main)
        top.tick_params(labelbottom=False)
        side.tick_params(labelleft=False)
        for ax in (main, top, side):
            ax.tick_params(labelsize=12)
        return main, top, side

    return density, dice_counts, margins


@app.cell(hide_code=True)
def _(lk, mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    j_x = mo.ui.range_slider(1, 4, 1, value=[3, 4], label="$X$", show_value=True)
    j_y = mo.ui.range_slider(2, 8, 1, value=[2, 5], label="$Y$", show_value=True)
    m_prod = mo.ui.switch(value=False, label=r"$f_X(x)\, f_Y(y)$")
    c_x = lk.slider(1, 4, step=1, value=3, label="$x$")
    a_a = lk.slider(0.2, 2.5, step=0.1, value=0.5, label="$a$")
    a_b = lk.slider(0.2, 2.5, step=0.1, value=1, label="$b$")
    r_lam = lk.slider(1, 4, step=0.1, value=2, label=r"$\lambda$")
    r_x = lk.slider(0.25, 3, step=0.05, value=1, label="$x$")
    return a_a, a_b, c_x, j_x, j_y, m_prod, r_lam, r_x


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Probabilistic models

        $\leadsto$ &nbsp; one measurement on a random experiment

        $\leadsto$ &nbsp; single random variable $X : S \longrightarrow \mathbb{R}$
        """,
        lk.aside(
            r"$$ P(X \in \mk{A}) = \sum_{x \in S_X \cap A} f_X(x) \quad \text{or} \quad \int_{S_X \cap A} f_X(x) \, dx $$",
            r"$A \subseteq \mathbb{R}$",
        ),
        r"$$ E[u(X)] = \sum_{x \in S_X} u(x) \, f_X(x) \quad \text{or} \quad \int_{S_X} u(x) \, f_X(x) \, dx $$",
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Multiple measurements on the same experiment

        $\leadsto$ &nbsp; joint behavior

        $\leadsto$ &nbsp; mutual dependence

        $\leadsto$ &nbsp; conditional expectations
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 5.2–5.4, 5.11")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: joint
    # section
    lk.section("Joint distributions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: joint
    # definition: joint distribution
    lk.definition(
        [
            r"Let $X, Y : S \longrightarrow \mathbb{R}$ be random variables on the same $(S, \mathcal{E}, P)$.",
            lk.aside(
                r"The **joint distribution** of the pair $\mk{(X, Y) : S \longrightarrow \mathbb{R}^2}$ is the assignment of probabilities",
                "a vector valued random variable",
            ),
            r"""
            $$
            P_{X,Y}(A) = P((X, Y) \in A), \quad \text{for } A \subseteq \mathbb{R}^2.
            $$

            The **state space** of $(X, Y)$ is $S_{X,Y} = \mathrm{Im}(X, Y) \subseteq \mathbb{R}^2$.
            """,
            lk.gap(),
            r"$\leadsto$ &nbsp; we call $(X, Y)$ **discrete** if $S_{X,Y}$ is countable",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\displaystyle P_{X,Y}(A) = \sum_{(x, y) \in S_{X,Y} \cap A} \mk{f_{X,Y}(x, y)}$",
                r"$f_{X,Y}(x, y)$ = joint pmf of $(X, Y)$",
            ),
            r"$\leadsto$ &nbsp; we call $(X, Y)$ **continuous** if $S_{X,Y}$ is uncountable *and* there exists $f_{X,Y} : \mathbb{R}^2 \longrightarrow \mathbb{R}$ with",
            lk.aside(
                r"> <span class='lk-ghost'>$\Longrightarrow$ &nbsp; </span>$\displaystyle P_{X,Y}(A) = \iint_{S_{X,Y} \cap A} \mk{f_{X,Y}(x, y)} \, dx \, dy$",
                r"$f_{X,Y}(x, y)$ = joint pdf of $(X, Y)$<br>(integrable function)",
            ),
            r"""
            $\leadsto$ &nbsp; in both cases $f_{X,Y}(x, y) \geq 0$

            > <span class='lk-ghost'>in both cases </span>$f_{X,Y}(x, y) = 0$ for $(x, y) \notin S_{X,Y}$

            > <span class='lk-ghost'>in both cases </span><span style="display: inline-block; width: 0; position: relative"><span style="position: absolute; right: 0.35em; bottom: -0.25em; white-space: nowrap">and</span></span>$P_{X,Y}(S_{X,Y}) = 1$
            """,
        ],
        label="def-joint",
    )
    return


@app.cell(hide_code=True)
def _(Figure, dice_counts, j_x, j_y, lk, margins):
    # module: joint
    # example: two 4-sided dice
    # the joint pmf on S_{X,Y} (dot area), the marginals in the margins; the event {a <= X <= b, c <= Y <= d} chosen
    # with the two range sliders is a rectangle, its points blue
    _n, _N = 4, 16
    _counts = dice_counts(_n)
    (_a, _b), (_c, _d) = j_x.value, j_y.value
    _xs, _ys = list(range(1, _n + 1)), list(range(2, 2 * _n + 1))
    _fx = [sum(k for (x, y), k in _counts.items() if x == v) for v in _xs]
    _fy = [sum(k for (x, y), k in _counts.items() if y == v) for v in _ys]
    _fig = Figure(figsize=(5.4, 4.1), layout="constrained")
    _main, _top, _side = margins(_fig)
    _main.fill_between([_a - 0.5, _b + 0.5], _c - 0.5, _d + 0.5, color=lk.LIGHT, lw=0)
    _main.plot([_a - 0.5, _b + 0.5, _b + 0.5, _a - 0.5, _a - 0.5], [_c - 0.5, _c - 0.5, _d + 0.5, _d + 0.5, _c - 0.5], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    for (_x, _y), _k in _counts.items():
        _color = lk.BLUE if _a <= _x <= _b and _c <= _y <= _d else lk.GREY
        _main.scatter(_x, _y, s=1800 * _k / _N, color=_color, lw=0, zorder=3)
        # the value right of its dot, ending before the edge of the rectangle half way to the next column
        _main.annotate(f"{_k}/{_N}", (_x, _y), textcoords="offset points", xytext=((1800 * _k / _N) ** 0.5 / 2 + 2, 0), va="center", fontsize=9, color=_color)
    _main.set_xlim(0.4, _n + 0.9)
    _main.set_ylim(1.3, 2 * _n + 0.7)
    _main.set_xticks(_xs)
    _main.set_yticks(_ys)
    _main.set_xlabel("$x$")
    _main.set_ylabel("$y$")
    _cx = [lk.BLUE if _a <= v <= _b else lk.GREY for v in _xs]
    _top.vlines(_xs, 0, [k / _N for k in _fx], color=_cx, lw=1.0)
    _top.scatter(_xs, [k / _N for k in _fx], s=18, color=_cx, zorder=3)
    for _x, _k, _col in zip(_xs, _fx, _cx):
        _top.annotate(f"{_k}/{_N}", (_x, _k / _N), textcoords="offset points", xytext=(0, 4), ha="center", va="bottom", fontsize=9, color=_col)
    _top.set_ylim(0, 1.45 * max(_fx) / _N)
    _top.set_yticks([])
    _top.set_ylabel("$f_X(x)$", fontsize=12)
    _cy = [lk.BLUE if _c <= v <= _d else lk.GREY for v in _ys]
    _side.hlines(_ys, 0, [k / _N for k in _fy], color=_cy, lw=1.0)
    _side.scatter([k / _N for k in _fy], _ys, s=18, color=_cy, zorder=3)
    for _y, _k, _col in zip(_ys, _fy, _cy):
        _side.annotate(f"{_k}/{_N}", (_k / _N, _y), textcoords="offset points", xytext=(5, 0), ha="left", va="center", fontsize=9, color=_col)
    _side.set_xlim(0, 1.9 * max(_fy) / _N)
    _side.set_xticks([])
    _side.set_xlabel("$f_Y(y)$", fontsize=12)
    lk.example(
        [
            r"""
            Roll two fair 4-sided dice

            > $\leadsto$ &nbsp; $S = \{ (i, j) \mid i, j = 1, 2, 3, 4 \}$

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

            <span class="lk-tab" style="--lk-tab: 21em">$\leadsto$ &nbsp; $P(X = 1, Y \leq 4) = {\large\tfrac{1}{16}} + 0 + 0 = {\large\tfrac{1}{16}}$</span>$P(Y = 5) = {\large\tfrac{4}{16}}$

            <span class="lk-tab" style="--lk-tab: 21em">$\leadsto$ &nbsp; $P(X > 2, Y \leq 5) = {\large\tfrac{6}{16}}$</span>$P(X = 2) = {\large\tfrac{3}{16}}$
            """,
            lk.interactive(
                _fig,
                controls=[j_x, j_y],
            ),
        ],
        label="ex-dice",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: marginal
    # section
    lk.section("Marginal distributions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: marginal
    # theorem: marginals from the joint
    lk.theorem(
        [
            r"The pmfs/pdfs of $X$ and $Y$ alone can be recovered from the joint pmf/pdf of $(X, Y)$ via",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \mk{f_X(x)} &= \sum_y f_{X,Y}(x, y) \quad \text{or} \quad \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dy\\[4pt]
                \mk{f_Y(y)} &= \sum_x f_{X,Y}(x, y) \quad \text{or} \quad \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dx.
                \end{aligned}
                $$
                """,
                [(1.5, r"$f_X$, $f_Y$ = marginal distributions")],
                rows=2,
            ),
        ],
        label="thm-marginals",
    )
    return


@app.cell(hide_code=True)
def _(Figure, dice_counts, lk, m_prod):
    # module: marginal
    # remark: marginals do not determine the joint
    # the joint pmf of the dice against the product f_X f_Y of its marginals (switch): the same marginals, a different
    # joint distribution
    _counts = dice_counts(4)
    _xs, _ys = list(range(1, 5)), list(range(2, 9))
    _fx = [sum(k for (x, y), k in _counts.items() if x == v) for v in _xs]
    _fy = [sum(k for (x, y), k in _counts.items() if y == v) for v in _ys]
    if m_prod.value:
        _cells = {(x, y): (kx * ky, 256) for x, kx in zip(_xs, _fx) for y, ky in zip(_ys, _fy)}
        _color, _name = lk.RED, r"$f_X(x)\, f_Y(y)$"
    else:
        _cells = {xy: (k, 16) for xy, k in _counts.items()}
        _color, _name = lk.BLUE, r"$f_{X,Y}(x, y)$"
    _fig = Figure(figsize=(5.4, 4.1), layout="constrained")
    _grid = _fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 3])
    _main = _fig.add_subplot(_grid[1, 0])
    _top = _fig.add_subplot(_grid[0, 0], sharex=_main)
    _side = _fig.add_subplot(_grid[1, 1], sharey=_main)
    _corner = _fig.add_subplot(_grid[0, 1])
    _corner.axis("off")
    _corner.text(0.5, 0.5, _name, color=_color, fontsize=14, ha="center", va="center", transform=_corner.transAxes)
    for (_x, _y), (_k, _N) in _cells.items():
        _main.scatter(_x, _y, s=1800 * _k / _N, color=_color, lw=0, zorder=3)
    _main.set_xlim(0.4, 4.9)
    _main.set_ylim(1.3, 8.7)
    _main.set_xticks(_xs)
    _main.set_yticks(_ys)
    _main.set_xlabel("$x$")
    _main.set_ylabel("$y$")
    _top.vlines(_xs, 0, [k / 16 for k in _fx], color=lk.GREY, lw=1.0)
    _top.scatter(_xs, [k / 16 for k in _fx], s=18, color=lk.GREY, zorder=3)
    for _x, _k in zip(_xs, _fx):
        _top.annotate(f"{_k}/16", (_x, _k / 16), textcoords="offset points", xytext=(0, 4), ha="center", va="bottom", fontsize=9, color=lk.GREY)
    _top.set_ylim(0, 1.45 * max(_fx) / 16)
    _top.set_yticks([])
    _top.set_ylabel("$f_X(x)$", fontsize=12)
    _top.tick_params(labelbottom=False)
    _side.hlines(_ys, 0, [k / 16 for k in _fy], color=lk.GREY, lw=1.0)
    _side.scatter([k / 16 for k in _fy], _ys, s=18, color=lk.GREY, zorder=3)
    for _y, _k in zip(_ys, _fy):
        _side.annotate(f"{_k}/16", (_k / 16, _y), textcoords="offset points", xytext=(5, 0), ha="left", va="center", fontsize=9, color=lk.GREY)
    _side.set_xlim(0, 1.9 * max(_fy) / 16)
    _side.set_xticks([])
    _side.set_xlabel("$f_Y(y)$", fontsize=12)
    _side.tick_params(labelleft=False)
    for _ax in (_main, _top, _side):
        _ax.tick_params(labelsize=12)
    lk.remark(
        [
            lk.aside(
                r"Joint distribution determines marginals, but marginals <span class='lk-mark'>*do not* determine</span> the joint!",
                "distinct joint distributions can<br>define the same marginals!",
            ),
            lk.interactive(_fig, controls=[m_prod]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditional
    # section
    lk.section("Conditional distributions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditional
    # definition: conditional pmf/pdf
    lk.definition(
        [
            r"For $x \in S_X$, with $f_X(x) > 0$, we define the **conditional pmf/pdf** of $Y$ given $X = x$ as",
            lk.aside(
                r"$$ f_{Y|X}(\mk{y} \mid \mk{x}) = \frac{f_{X,Y}(x, y)}{f_X(x)}. $$",
                r"$x$ = given value of $X$<br>$y$ = possible values of $Y$",
            ),
        ],
        label="def-conditional",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditional
    # prose: interpretation
    lk.prose(
        r"""
        $\leadsto$ &nbsp; in the discrete case we have a direct interpretation

        > $$
        > \begin{aligned}
        > f_{Y|X}(y \mid x) &= P(Y = y \mid X = x)\\[2pt]
        > &= \frac{P(X = x \text{ and } Y = y)}{P(X = x)} = \frac{f_{X,Y}(x, y)}{f_X(x)}
        > \end{aligned}
        > $$

        $\leadsto$ &nbsp; also in the continuous case the conditional pdf gives probabilities of $Y$ given knowledge of $X = x$
        """
    )
    return


@app.cell(hide_code=True)
def _(Figure, Fraction, c_x, dice_counts, lk):
    # module: conditional
    # example: 4-sided dice, conditional pmf
    # f_{Y|X}(y | x) (blue) against f_Y(y) (red), x chosen with the slider
    _x = c_x.value
    _counts = dice_counts(4)
    _ys = list(range(2, 9))
    _kx = sum(k for (x, y), k in _counts.items() if x == _x)
    _ky = [sum(k for (x, y), k in _counts.items() if y == v) for v in _ys]
    _cond = [Fraction(_counts.get((_x, v), 0), _kx) for v in _ys]
    _fig = Figure(figsize=(5.4, 2.5), layout="constrained")
    _ax = _fig.subplots()
    for _vals, _color, _shift in (([k / 16 for k in _ky], lk.RED, 0.1), ([float(p) for p in _cond], lk.BLUE, -0.1)):
        _at = [v + _shift for v in _ys]
        _ax.vlines(_at, 0, _vals, color=_color, lw=1.2)
        _ax.plot(_at, _vals, "o", color=_color, ms=4.5, zorder=4)
    _ax.text(8.6, 1.0, rf"$f_{{Y|X}}(y \mid {_x})$", color=lk.BLUE, fontsize=12, ha="right", va="top")
    _ax.text(8.6, 0.82, r"$f_Y(y)$", color=lk.RED, fontsize=12, ha="right", va="top")
    _ax.set_xlim(1.4, 8.6)
    _ax.set_ylim(0, 1.05)
    _ax.set_xticks(_ys)
    _ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    _ax.set_xlabel("$y$")
    _ax.tick_params(labelsize=12)
    lk.example(
        [
            r"$X$ = largest face $= 3$, &nbsp; $Y$ = sum of faces $= y$",
            lk.aside(
                r"""
                | $y$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ | $8$ |
                |:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
                | $f_{Y \vert X}(y \mid 3)$ | $0$ | $0$ | $\frac{2/16}{5/16} = \frac{2}{5}$ | $\frac{2/16}{5/16} = \frac{2}{5}$ | $\frac{1/16}{5/16} = \frac{1}{5}$ | $0$ | $0$ |
                """,
                r"$\dfrac{2/16}{5/16} = \dfrac{f_{X,Y}(3, 4)}{f_X(3)}$",
            ),
            r"$\leadsto$ &nbsp; are the two measurements independent?",
            lk.aside(
                r"$\leadsto$ &nbsp; knowledge about measurement $X$ <span class='lk-mark'>changed the probabilities</span> of measurement $Y$",
                "we shouldn't call them independent",
            ),
            lk.interactive(_fig, controls=[c_x]),
        ],
        title="4-sided dice",
        label="ex-dice-conditional",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # section
    lk.section("Independence")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # definition: independent random variables
    lk.definition(
        [
            lk.aside(r"$X$ and $Y$ are **independent** if, for all $(x, y)$", "(for $f_X(x), f_Y(y) > 0$)"),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                & f_{Y|X}(y \mid x) = f_Y(y)\\[8pt]
                \Longleftrightarrow \quad & f_{X,Y}(x, y) = f_X(x) \, f_Y(y)\\[8pt]
                \Longleftrightarrow \quad & f_{X|Y}(x \mid y) = f_X(x).
                \end{aligned}
                $$
                """,
                [(1, "knowledge about $X$ does not<br>affect our beliefs about $Y$"), (3, "knowledge about $Y$ does not<br>affect our beliefs about $X$")],
                rows=3,
            ),
        ],
        label="def-independent",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # remark: product rule
    lk.remark(
        r"""
        If $X, Y$ are independent

        $$
        P(X \in A \text{ and } Y \in B) = P(X \in A) \cdot P(Y \in B),
        $$

        for any $A \subseteq \mathbb{R}$ and $B \subseteq \mathbb{R}$
        """
    )
    return


@app.cell(hide_code=True)
def _(Figure, a_a, a_b, density, lk, margins, math, np):
    # module: independence
    # example: customer arrivals
    # the joint pdf for lambda = 2 with its marginals and the event {X <= a, Y <= b}
    _lam, _a, _b = 2, a_a.value, a_b.value
    _L = 3.0
    _g = np.linspace(0, _L, 301)
    _X, _Y = np.meshgrid(_g, _g)
    _f = np.where(_X < _Y, _lam**2 * np.exp(-_lam * _Y), np.nan)
    _fig = Figure(figsize=(5.4, 4.1), layout="constrained")
    _main, _top, _side = margins(_fig)
    density(_main, _f, (0, _L, 0, _L), _lam**2)
    _main.plot([0, _L], [0, _L], color=lk.GREY, lw=1.0)
    _main.plot([0, _a, _a], [_b, _b, 0], color=lk.GREEN, lw=1.4)
    _main.text(0.3, 2.7, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    _main.set_xlim(0, _L)
    _main.set_ylim(0, _L)
    _main.set_xticks([0, 1, 2, 3])
    _main.set_yticks([0, 1, 2, 3])
    _main.set_xlabel("$x$")
    _main.set_ylabel("$y$")
    _ga, _gb = np.linspace(0, _a, 200), np.linspace(0, _b, 200)
    _top.fill_between(_ga, _lam * np.exp(-_lam * _ga), color=lk.LIGHT, lw=0)
    _top.plot(_g, _lam * np.exp(-_lam * _g), color=lk.BLUE, lw=1.4)
    _top.axvline(_a, color=lk.GREEN, lw=1.0, ls=(0, (4, 3)))
    _top.set_ylim(0, 1.1 * _lam)
    _top.set_yticks([])
    _top.set_ylabel(r"$f_X(x)$", fontsize=12)
    _side.fill_betweenx(_gb, 0, _lam**2 * _gb * np.exp(-_lam * _gb), color=lk.LIGHT, lw=0)
    _side.plot(_lam**2 * _g * np.exp(-_lam * _g), _g, color=lk.BLUE, lw=1.4)
    _side.axhline(_b, color=lk.GREEN, lw=1.0, ls=(0, (4, 3)))
    _side.set_xlim(0, 1.1 * _lam / math.e)
    _side.set_xticks([])
    _side.set_xlabel(r"$f_Y(y)$", fontsize=12)
    lk.example(
        [
            r"""
            Customers arrive following a Poisson model $\mathrm{Pois}(\lambda)$

            $X$ = arrival time of 1st customer

            $Y$ = arrival time of 2nd customer

            > $\Longrightarrow$ &nbsp; $f_{X,Y}(x, y) = \begin{cases} \lambda^2 e^{-\lambda y}, & 0 < x < y,\\ 0, & \text{otherwise} \end{cases}$
            """,
            r"""
            > > $\leadsto$ &nbsp; $f_X(x) = \mathrm{Gamma}(1, \lambda)(x) = \lambda e^{-\lambda x}$

            > > <span class='lk-ghost'>$\leadsto$ &nbsp; </span>$Y - x$ = arrival time of 2nd customer counted from $x$

            > > > $\Longrightarrow$ &nbsp; $f_{Y|X}(y \mid x) = \mathrm{Gamma}(1, \lambda)(y - x) = \lambda e^{-\lambda (y - x)}$

            > > > $\Longrightarrow$ &nbsp; $f_{X,Y}(x, y) = f_{Y|X}(y \mid x) \, f_X(x) = \lambda^2 e^{-\lambda y}$ for $0 < x < y$
            """,
            lk.gap(),
            r"""
            $\leadsto$ &nbsp; marginals

            > $$
            > \begin{aligned}
            > f_X(x) &= \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dy\\[2pt]
            > &= \int_x^{\infty} \lambda^2 e^{-\lambda y} \, dy = \lambda e^{-\lambda x}\\[2pt]
            > &= \mathrm{Gamma}(1, \lambda)(x) = \mathrm{Exp}(\lambda)(x)\\[10pt]
            > f_Y(y) &= \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dx\\[2pt]
            > &= \int_0^{y} \lambda^2 e^{-\lambda y} \, dx = \lambda^2 y \, e^{-\lambda y} = \mathrm{Gamma}(2, \lambda)(y)
            > \end{aligned}
            > $$
            """,
            lk.interactive(
                _fig,
                controls=[a_a, a_b],
            ),
        ],
        label="ex-arrivals",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # remark: the conditional pmf/pdf is a pmf/pdf
    lk.remark(
        [
            lk.aside(r"For any $\mk{x} \in S_X$, $f_{Y|X}(\cdot \mid x)$ is a proper pmf/pdf!", r"$x$ fixed"),
            r"""
            > • &nbsp; $f_{Y|X}(y \mid x) \geq 0 \quad \forall \, y \in \mathbb{R}$

            > • &nbsp; $\displaystyle \sum_y f_{Y|X}(y \mid x) = \sum_y \frac{f_{X,Y}(x, y)}{f_X(x)} = \frac{1}{f_X(x)} \sum_y f_{X,Y}(x, y) = 1$

            > • &nbsp; $\displaystyle \int_{-\infty}^{\infty} f_{Y|X}(y \mid x) \, dy = \int_{-\infty}^{\infty} \frac{f_{X,Y}(x, y)}{f_X(x)} \, dy = \frac{1}{f_X(x)} \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dy = 1$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # section
    lk.section("Conditional expectation")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # definition: conditional expectation
    lk.definition(
        [
            r"""
            Given $u : \mathbb{R} \longrightarrow \mathbb{R}$ real valued single variable function,

            the **conditional expectation** of $u(Y)$, given $X = x$ is
            """,
            r"""
            $$
            \begin{aligned}
            E[u(Y) \mid X = x] &= \sum_y u(y) \, f_{Y|X}(y \mid x)\\[4pt]
            \text{or} \quad &= \int_{-\infty}^{\infty} u(y) \, f_{Y|X}(y \mid x) \, dy.
            \end{aligned}
            $$
            """,
            lk.gap(),
            lk.aside(
                r"• &nbsp; $u(Y) = Y$ &nbsp; $\leadsto$ &nbsp; $E[Y \mid X = x] = g(x)$ <span class='lk-mark'>**conditional mean**</span> of $Y$ given $X = x$",
                "expected value of $Y$ given the<br>observed value of $X = x$",
            ),
            lk.aside(
                r"> $\leadsto$ &nbsp; **regression function** of $Y$ on $X$",
                "$g(X)$ will later become our best guess for<br>the values of $Y$ given the values of $X$",
            ),
        ],
        label="def-conditional-expectation",
    )
    return


@app.cell(hide_code=True)
def _(Figure, density, lk, np, r_lam, r_x):
    # module: expectation
    # example: customer arrivals, regression
    # left: the regression line y = x + 1/lambda through the joint pdf, and the slice X = x; right: the conditional pdf
    # of Y given X = x against the marginal pdf of Y
    _lam, _x = r_lam.value, r_x.value
    _m = _x + 1 / _lam
    _L = 5.0
    _g = np.linspace(0, _L, 301)
    _X, _Y = np.meshgrid(_g, _g)
    _f = np.where(_X < _Y, _lam**2 * np.exp(-_lam * _Y), np.nan)
    _fig = Figure(figsize=(lk.FULL, 3.2), layout="constrained")
    _fig.get_layout_engine().set(wspace=0.08)
    _left, _right = _fig.subplots(1, 2)
    density(_left, _f, (0, _L, 0, _L), _lam**2)
    _left.plot([0, _L], [0, _L], color=lk.GREY, lw=1.0)
    _left.plot([_x, _x], [_x, _L], color=lk.BLUE, lw=1.2, ls=(0, (4, 3)))
    _left.plot(_g, _g + 1 / _lam, color=lk.GREEN, lw=1.4)
    _left.plot(_x, _m, "o", color=lk.GREEN, ms=5, zorder=4, clip_on=False)
    _left.text(_L - 0.15, 0.3, r"$y = x + 1/\lambda$", color=lk.GREEN, fontsize=12, ha="right", va="bottom")
    _left.set_xlim(0, _L)
    _left.set_ylim(0, _L)
    _left.set_xlabel("$x$")
    _left.set_ylabel("$y$")
    _yy = np.linspace(_x, _L, 300)
    _right.fill_between(_yy, _lam * np.exp(-_lam * (_yy - _x)), color=lk.LIGHT, lw=0)
    _right.plot(np.r_[0, _x, _yy], np.r_[0, 0, _lam * np.exp(-_lam * (_yy - _x))], color=lk.BLUE, lw=1.4)
    _right.plot(_g, _lam**2 * _g * np.exp(-_lam * _g), color=lk.RED, lw=1.2)
    _right.plot([_m, _m], [0, _lam * np.exp(-1)], color=lk.GREEN, lw=1.2, ls=(0, (4, 3)))
    _right.text(_L, 1.15 * _lam, r"$f_{Y|X}(y \mid x)$", color=lk.BLUE, fontsize=12, ha="right", va="top")
    _right.text(_L, 0.95 * _lam, r"$f_Y(y)$", color=lk.RED, fontsize=12, ha="right", va="top")
    _right.set_xlim(0, _L)
    _right.set_ylim(0, 1.2 * _lam)
    _right.set_yticks([])
    _right.set_xlabel("$y$")
    for _ax in (_left, _right):
        _ax.tick_params(labelsize=12)
    lk.example(
        [
            r"""
            $f_{X,Y}(x, y) = \lambda^2 e^{-\lambda y}$, &nbsp; $0 < x < y$

            > $\leadsto$ &nbsp; $f_{Y|X}(y \mid x) = \lambda e^{-\lambda (y - x)}$, &nbsp; $y > x$

            > $\Longrightarrow$ &nbsp; $\displaystyle E[Y \mid X = x] = \int_{-\infty}^{+\infty} y \, f_{Y|X}(y \mid x) \, dy$

            > <span class='lk-ghost'>$\Longrightarrow$ &nbsp; $\displaystyle E[Y \mid X = x]$ </span>$\displaystyle = \int_x^{+\infty} y \, \lambda e^{-\lambda (y - x)} \, dy = x + \frac{1}{\lambda}$

            > > $\leadsto$ &nbsp; the regression function of $Y$ on $X$ is linear

            if $\lambda = 2$ customers per hour and 1st customer arrived at $x = 1$ hour

            > we expect 2nd customer to arrive at hour $y = 1.5$
            """,
            lk.interactive(_fig, controls=[r_lam, r_x]),
        ],
        title="customer arrivals",
        label="ex-regression",
    )
    return


if __name__ == "__main__":
    app.run()

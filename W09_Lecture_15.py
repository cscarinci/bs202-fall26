import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 15 · Covariance and correlation", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math
    from fractions import Fraction

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Figure, Fraction, math, mo, np


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS202 &bull; {running}</div>
      <div class="bs-title">Introduction to Probability<br>and Mathematical Statistics</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>BS202a</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def proposition(body, title=""):
        return _statement("Proposition", title, body)

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def postulate(body, title=""):
        return _statement("Postulate", title, body)

    def note(body):
        """Editorial note of the notebook (not part of the lecture)."""
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        The head is sized in points from the line width (length 4 lw, full width 2.5 lw), never in data units,
        so arrows look alike in every figure whatever its axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"-|>,head_length={4 * lw:g},head_width={1.25 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        from matplotlib.figure import Figure as _Figure

        fig = _Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        import numpy as _np

        rng = _np.random.default_rng(seed)
        t = _np.linspace(0, 2 * _np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * _np.cos(k * t + rng.uniform(0, 2 * _np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * _np.cos(t), cy + ry * r * _np.sin(t)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 15", "Week 09", "Lecture 15 • Covariance and correlation")
    return


@app.cell(hide_code=True)
def _(arrow, math):
    def vector(ax, tail, tip, color, label=None, turn=0, r=5, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            arrow(ax, tail, tip, color, **kw)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            from matplotlib.textpath import TextPath

            ext = TextPath((0, 0), label, size=13).get_extents()
            c, s = math.cos(d), math.sin(d)
            ax.annotate(label, tip, textcoords="offset points", xytext=(c * (r + ext.width / 2), s * (r + ext.height / 2)), ha="center", va="center", color=color, fontsize=13, zorder=5)

    return (vector,)


@app.cell(hide_code=True)
def _():
    def dice_counts(n):
        """Number of outcomes, out of n^2, of two fair n-sided dice for each pair (largest face, sum)."""
        counts = {}
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                counts[(max(i, j), i + j)] = counts.get((max(i, j), i + j), 0) + 1
        return counts

    def over(k, n):
        """k/n in TeX, left unreduced like the lecture's sixteenths."""
        return "0" if k == 0 else rf"\dfrac{{{k}}}{{{n}}}"

    def tex(q):
        """A Fraction in TeX."""
        sign, q = ("-", -q) if q < 0 else ("", q)
        return sign + (f"{q.numerator}" if q.denominator == 1 else rf"\dfrac{{{q.numerator}}}{{{q.denominator}}}")

    def num(v, digits=2):
        """Number for the readout tables: exact when a multiple of 1/2, otherwise two decimals (never a negative zero)."""
        if abs(2 * v - round(2 * v)) < 1e-9:
            return f"{round(2 * v) / 2 + 0.0:g}"
        return f"{round(v, digits) + 0.0:.{digits}f}"

    def val(q):
        """A Fraction for the readout tables: exact and inline in quarters (as the lecture's 5/4), small values to two significant digits, otherwise two decimals."""
        if q.denominator in (1, 2, 4):
            return f"{q.numerator}" if q.denominator == 1 else f"{q.numerator}/{q.denominator}"
        if abs(q) < 0.1:
            return f"{float(q):.2g}"
        return f"{float(q):.2f}"

    return dice_counts, num, over, tex, val


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - joint distributions &nbsp; $f_{X,Y}(x, y)$
    - marginal distributions &nbsp; $f_X(x)$, $f_Y(y)$
    - conditional distributions &nbsp; $f_{Y|X}(y \mid x) = \dfrac{f_{X,Y}(x, y)}{f_X(x)}$
    - $\leadsto$ &nbsp; independence: &nbsp; $f_{X,Y}(x, y) = f_X(x)\, f_Y(y)$
    - $\leadsto$ &nbsp; conditional expectation

        $$
        E[u(Y) \mid X = x] = \sum_y u(y)\, f_{Y|X}(y \mid x)
        $$

        (expected value of $u(Y)$ given the measured value of $X = x$)

    **In this lecture:** how strongly are $X$ and $Y$ related? &nbsp; <span class="nw">$\leadsto$ &nbsp; covariance</span> and correlation

    **References:** WMS 5.5–5.8
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## IV.2 &nbsp; Covariance and correlation

    ### Expectations of functions of two random variables
    """
            ),
            definition(
                r"""
    Given $u : \mathbb{R}^2 \longrightarrow \mathbb{R}$ bivariate function

    $$
    \begin{aligned}
    \underbrace{E[u(X, Y)]}_{\mathclap{\footnotesize \text{expectation of } u(X, Y)}} &= \sum_x \sum_y u(x, y)\, f_{X,Y}(x, y) \\[2.6em]
    \text{or} \qquad &= \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} u(x, y)\, f_{X,Y}(x, y)\, dx\, dy
    \end{aligned}
    $$
    """,
                "Expectation of a function of two random variables",
            ),
            theorem(
                r"""
    - $E[a\, u(X, Y) + b\, v(X, Y)] = a\, E[u(X, Y)] + b\, E[v(X, Y)]$
    - $E[u(X)\, v(Y)] = E[u(X)]\, E[v(Y)]$ &nbsp; if $X, Y$ independent
    """,
                "Properties of expectations",
            ),
            mo.md(
                r"""
    **Proof** (of the second property).

    <span class="chain">$\displaystyle \sum_x \sum_y u(x)\, v(y)\, f_{X,Y}(x, y)$ $\displaystyle = \sum_x \sum_y u(x)\, v(y)\, f_X(x)\, f_Y(y) \qquad \text{(independence)}$ $\displaystyle = \sum_x u(x)\, f_X(x) \sum_y v(y)\, f_Y(y)$ <span class="qed">$\square$</span></span>
    """
            ),
        ],
        gap=1.5,
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, RED, definition, mo):
    _fig = Figure(figsize=(HALF, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(1.5, color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.axhline(1.2, color=GREY, lw=1.0, ls=(0, (4, 3)))
    for _q, _xy, _color in (("Q1", (2.3, 1.95), BLUE), ("Q2", (0.75, 1.95), RED), ("Q3", (0.75, 0.55), BLUE), ("Q4", (2.3, 0.55), RED)):
        _ax.text(*_xy, _q, color=_color, fontsize=13, ha="center", va="center")
    _ax.set_xlim(0, 3)
    _ax.set_ylim(0, 2.5)
    _ax.set_xticks([1.5], [r"$\mu_X$"])
    _ax.set_yticks([1.2], [r"$\mu_Y$"])
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$y$", rotation=0, labelpad=10)
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(r"""### Covariance"""),
            definition(
                r"""
    Given $X, Y$ random variables on $(S, \mathcal{E}, P)$

    $$
    \sigma_{X,Y} = \mathrm{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)]
    $$

    is called the **covariance** of $X$ and $Y$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $\mu_X = E[X]$,</span> $\mu_Y = E[Y]$ means of $X$, $Y$
    """,
                "Covariance",
            ),
            _fig,
            mo.md(
                r"""
    $$
    \begin{aligned}
    &\text{Q1:} \ \ (x - \mu_X)(y - \mu_Y) > 0, & \qquad &\text{Q2:} \ \ (x - \mu_X)(y - \mu_Y) < 0 \\[4pt]
    &\text{Q3:} \ \ (x - \mu_X)(y - \mu_Y) > 0, & \qquad &\text{Q4:} \ \ (x - \mu_X)(y - \mu_Y) < 0
    \end{aligned}
    $$

    $\leadsto$ &nbsp; if $\mathrm{Cov}(X, Y) > 0$ we expect to see values of $(X, Y)$ in Q1 and Q3

    $\leadsto$ &nbsp; $X$ and $Y$ get large or small together!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, GREY, HALF, LIGHT, mo, theorem):
    _fig = Figure(figsize=(HALF, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill([1, 0, -1, 0], [0, 1, 0, -1], facecolor=LIGHT, edgecolor=GREY, lw=1.0)
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.text(0.75, 0.75, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    for _v, _xy, _off in (("$1$", (1, 0), (4, -12)), ("$-1$", (-1, 0), (-4, -12)), ("$1$", (0, 1), (6, 2)), ("$-1$", (0, -1), (6, -2))):
        _ax.annotate(_v, _xy, textcoords="offset points", xytext=_off, fontsize=12, ha="left" if _off[0] > 0 else "right", va="center")
    _ax.set_xlim(-1.3, 1.3)
    _ax.set_ylim(-1.3, 1.3)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            theorem(
                r"""
    $$
    \mathrm{Cov}(X, Y) = E[XY] - \mu_X \mu_Y
    $$

    $$
    \mathrm{Cov}(X, X) = \mathrm{Var}(X) = \sigma_X^2, \qquad \mathrm{Cov}(Y, Y) = \mathrm{Var}(Y) = \sigma_Y^2
    $$

    (maybe this makes the squares more natural)

    Also:

    $$
    \begin{alignedat}{2}
    \mathrm{Cov}(X, Y) &= \mathrm{Cov}(Y, X) &\qquad& \text{symmetric} \\[4pt]
    \mathrm{Cov}(aX + bY, Z) &= a\, \mathrm{Cov}(X, Z) + b\, \mathrm{Cov}(Y, Z) && \text{bilinear} \\[4pt]
    \mathrm{Cov}(X, Y) &= 0 \quad \text{if } X, Y \text{ are independent}
    \end{alignedat}
    $$
    """,
                "Properties of covariance",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $\mathrm{Cov}$ is like an inner product and independent random variables are orthogonal!

    $\leadsto$ &nbsp; $\mathrm{Var}$ is like length squared! &nbsp; (However, some non-zero random variables have zero variance!)

    **Remark.** Not every pair $(X, Y)$ of random variables with $\mathrm{Cov}(X, Y) = 0$ is independent!

    **Example.** &nbsp; $(X, Y)$ **uniform** on $S_{X,Y} = \{\, (x, y) \mid |x| + |y| < 1 \,\}$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $f_{X,Y}(x, y) = c = \dfrac{1}{2}$</span>
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \Longrightarrow \qquad \begin{cases}
    f_X(x) = \displaystyle\int_{-(1 - |x|)}^{1 - |x|} \frac{1}{2}\, dy = 1 - |x|, & |x| < 1 \\[14pt]
    f_Y(y) = \displaystyle\int_{-(1 - |y|)}^{1 - |y|} \frac{1}{2}\, dx = 1 - |y|, & |y| < 1
    \end{cases}
    $$

    $$
    \Longrightarrow \qquad \begin{cases}
    \mu_X = E[X] = \displaystyle\int_{-1}^{1} x\, (1 - |x|)\, dx = 0 \\[14pt]
    \mu_Y = E[Y] = \displaystyle\int_{-1}^{1} y\, (1 - |y|)\, dy = 0
    \end{cases}
    $$

    <span class="chain">$\displaystyle \Longrightarrow \qquad \sigma_{X,Y} = E[XY] - \mu_X \mu_Y = \int_{-1}^{1} \int_{-(1 - |x|)}^{1 - |x|} xy\, \frac{1}{2}\, dy\, dx$ $\displaystyle = \int_{-1}^{1} x\, \underbrace{\left. \frac{y^2}{4} \right|_{-(1 - |x|)}^{1 - |x|}}_{\footnotesize =\, 0}\, dx = 0$</span>

    But &nbsp; $f_{X,Y}(x, y) = \dfrac{1}{2} \neq f_X(x)\, f_Y(y) = (1 - |x|)(1 - |y|)$ &nbsp; for most $(x, y) \in S_{X,Y}$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    d_x = mo.ui.slider(-0.75, 0.75, 0.05, value=0.5, label="$x$", show_value=True)
    return (d_x,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, LIGHT, RED, d_x, mo, np):
    _x = d_x.value
    _h = 1 - abs(_x)  # the slice X = x of the diamond is the interval |y| < 1 - |x|
    _top = 2.0  # the tallest slice, 1/(2 h) at |x| = 0.75

    _fig = Figure(figsize=(5.8, 2.6), layout="constrained")
    _left, _right = _fig.subplots(1, 2, gridspec_kw={"width_ratios": [1, 1.4]})

    # left: the diamond and its slice at X = x
    _left.fill([1, 0, -1, 0], [0, 1, 0, -1], facecolor=LIGHT, edgecolor=GREY, lw=1.0)
    _left.axhline(0, color="black", lw=0.8)
    _left.axvline(0, color="black", lw=0.8)
    _left.plot([_x, _x], [-_h, _h], color=BLUE, lw=2.4, solid_capstyle="butt")
    _left.plot(_x, 0, "o", color=GREEN, ms=5, zorder=4)
    _left.annotate("$x$", (_x, -_h), textcoords="offset points", xytext=(4, -6), color=BLUE, fontsize=12, ha="left", va="top")
    _left.set_xlim(-1.2, 1.2)
    _left.set_ylim(-1.2, 1.2)
    _left.set_aspect("equal")
    _left.axis("off")

    # right: the conditional pdf of Y given X = x, uniform on the slice, against the marginal pdf of Y
    _yy = np.linspace(-1, 1, 401)
    _right.fill_between([-_h, _h], 0, 1 / (2 * _h), color=LIGHT, lw=0)
    _right.plot([-1.1, -_h, -_h, _h, _h, 1.1], [0, 0, 1 / (2 * _h), 1 / (2 * _h), 0, 0], color=BLUE, lw=1.4)
    _right.plot(_yy, 1 - np.abs(_yy), color=RED, lw=1.2)
    _right.plot([0, 0], [0, 1.08 * _top], color=GREEN, lw=1.2, ls=(0, (4, 3)))
    _right.text(0, 1.1 * _top, r"$E[Y \mid X = x]$", color=GREEN, fontsize=12, ha="center", va="bottom")
    _right.text(1.1, 1.15 * _top, r"$f_{Y|X}(y \mid x)$", color=BLUE, fontsize=12, ha="right", va="top")
    _right.text(1.1, 0.97 * _top, r"$f_Y(y)$", color=RED, fontsize=12, ha="right", va="top")
    _right.set_xlim(-1.1, 1.1)
    _right.set_ylim(0, 1.2 * _top)
    _right.set_yticks([0, 0.5, 1, 1.5, 2])
    _right.set_xlabel("$y$")
    _right.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _right.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _right.spines["top"].set_visible(False)
    _right.spines["right"].set_visible(False)
    for _ax in (_left, _right):
        _ax.tick_params(labelsize=12)

    mo.vstack(
        [
            mo.hstack([d_x], justify="start", gap=2, wrap=True),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example** (Two 4-sided dice). &nbsp; $X$ = largest face, &nbsp; $Y$ = sum of faces

    | $f_{X,Y}(x, y)$ | $x = 1$ | $2$ | $3$ | $4$ | $f_Y(y)$ |
    |:--|:-:|:-:|:-:|:-:|:-:|
    | $y = 8$ | $0$ | $0$ | $0$ | $1/16$ | $1/16$ |
    | $7$ | $0$ | $0$ | $0$ | $2/16$ | $2/16$ |
    | $6$ | $0$ | $0$ | $1/16$ | $2/16$ | $3/16$ |
    | $5$ | $0$ | $0$ | $2/16$ | $2/16$ | $4/16$ |
    | $4$ | $0$ | $1/16$ | $2/16$ | $0$ | $3/16$ |
    | $3$ | $0$ | $2/16$ | $0$ | $0$ | $2/16$ |
    | $2$ | $1/16$ | $0$ | $0$ | $0$ | $1/16$ |
    | $f_X(x)$ | $1/16$ | $3/16$ | $5/16$ | $7/16$ | $1$ |

    <span class="chain">$\displaystyle E[X] = 1 \cdot \frac{1}{16} + 2 \cdot \frac{3}{16} + 3 \cdot \frac{5}{16} + 4 \cdot \frac{7}{16} = \frac{50}{16}$</span>

    <span class="chain">$\displaystyle E[Y] = 2 \cdot \frac{1}{16} + 3 \cdot \frac{2}{16} + 4 \cdot \frac{3}{16} + 5 \cdot \frac{4}{16}$ $\displaystyle + 6 \cdot \frac{3}{16} + 7 \cdot \frac{2}{16} + 8 \cdot \frac{1}{16} = \frac{80}{16}$</span>

    <span class="chain">$\displaystyle E[XY] = 1 \cdot 2 \cdot \frac{1}{16} + 2 \cdot 3 \cdot \frac{2}{16} + 2 \cdot 4 \cdot \frac{1}{16}$ $\displaystyle + 3 \cdot 4 \cdot \frac{2}{16} + \cdots + 4 \cdot 8 \cdot \frac{1}{16} = \frac{270}{16}$</span>

    $$
    \Longrightarrow \qquad \mathrm{Cov}(X, Y) = \sigma_{X,Y} = \frac{270 - 50 \cdot 5}{16} = \frac{5}{4} > 0
    $$

    $\leadsto$ &nbsp; big largest face goes together with big sum
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, Fraction, GREY, RED, dice_counts, mo, table, val):
    _n = 4  # the lecture's two 4-sided dice
    _N = _n**2
    _counts = dice_counts(_n)
    _sx = sum(x * k for (x, y), k in _counts.items())
    _sy = sum(y * k for (x, y), k in _counts.items())
    _sxy = sum(x * y * k for (x, y), k in _counts.items())
    _mx, _my = Fraction(_sx, _N), Fraction(_sy, _N)
    # each point contributes (x - mu_X)(y - mu_Y) f_{X,Y}(x, y) to the covariance
    _part = {xy: (xy[0] - _mx) * (xy[1] - _my) * Fraction(k, _N) for xy, k in _counts.items()}
    _plus = sum((p for p in _part.values() if p > 0), Fraction(0))
    _minus = sum((p for p in _part.values() if p < 0), Fraction(0))

    _fig = Figure(figsize=(5.6, 3.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(float(_mx), color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.axhline(float(_my), color=GREY, lw=1.0, ls=(0, (4, 3)))
    for (_x, _y), _k in _counts.items():
        _p = _part[(_x, _y)]
        _ax.scatter(_x, _y, s=2400 * _k / _N, color=BLUE if _p > 0 else RED if _p < 0 else GREY, lw=0, zorder=3)
    for _q, _xy, _ha, _va, _color in (("Q1", (0.99, 0.98), "right", "top", BLUE), ("Q2", (0.01, 0.98), "left", "top", RED), ("Q3", (0.01, 0.02), "left", "bottom", BLUE), ("Q4", (0.99, 0.02), "right", "bottom", RED)):
        _ax.text(*_xy, _q, transform=_ax.transAxes, color=_color, fontsize=13, ha=_ha, va=_va)
    _ax.text(float(_mx), 2 * _n + 0.9, r"$\mu_X$", color=GREY, fontsize=12, ha="center", va="bottom")
    _ax.text(_n + 0.85, float(_my), r"$\mu_Y$", color=GREY, fontsize=12, ha="left", va="center")
    _ax.set_xlim(0.3, _n + 0.7)
    _ax.set_ylim(1.2, 2 * _n + 0.8)
    _ax.set_xticks(range(1, _n + 1))
    _ax.set_yticks(range(2, 2 * _n + 1, 1 if _n <= 5 else 2))
    _ax.set_xlabel("$x$ (largest face)")
    _ax.set_ylabel("$y$ (sum of faces)")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            table(
                [
                    (r"contributions $(x - \mu_X)(y - \mu_Y)\, f_{X,Y}(x, y)$ from Q1 and Q3 &nbsp; (blue&nbsp;dots)", rf"${val(_plus)}$"),
                    (r"contributions from Q2 and Q4 &nbsp; (red&nbsp;dots)", rf"${val(_minus)}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(corollary, definition, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Given $X, Y$ random variables on $(S, \mathcal{E}, P)$, &nbsp; $a, b \in \mathbb{R}$

    $$
    \mathrm{Var}(aX + bY) = a^2\, \mathrm{Var}(X) + b^2\, \mathrm{Var}(Y) + 2ab\, \mathrm{Cov}(X, Y)
    $$
    """,
                "Variance of a linear combination",
            ),
            mo.md(
                r"""
    **Proof.**

    <span class="chain">$\displaystyle \mathrm{Var}(aX + bY) = \mathrm{Cov}(aX + bY,\ aX + bY)$ $\displaystyle = a^2\, \mathrm{Cov}(X, X) + b^2\, \mathrm{Cov}(Y, Y) + 2ab\, \mathrm{Cov}(X, Y)$ <span class="qed">$\square$</span></span>
    """
            ),
            corollary(
                r"""
    If $X, Y$ are independent

    $$
    \mathrm{Var}(aX + bY) = a^2\, \mathrm{Var}(X) + b^2\, \mathrm{Var}(Y)
    $$

    $\leadsto$ &nbsp; like Pythagoras!
    """,
                "Variance of a linear combination of independent random variables",
            ),
            mo.md(r"""### Correlation"""),
            definition(
                r"""
    Given $X, Y$ random variables on $(S, \mathcal{E}, P)$

    $$
    \rho_{X,Y} = \frac{\sigma_{X,Y}}{\sigma_X\, \sigma_Y} = \text{\textbf{correlation} between } X \text{ and } Y
    $$

    $\leadsto$ &nbsp; normalized covariance in units of standard deviations
    """,
                "Correlation",
            ),
            mo.md(
                r"""
    **Example** (Two 4-sided dice).

    $$
    \left.
    \begin{aligned}
    \mathrm{Var}(X) &= \sigma_X^2 = \frac{55}{64} \\[6pt]
    \mathrm{Var}(Y) &= \sigma_Y^2 = \frac{5}{2}
    \end{aligned}
    \ \right\} \qquad \rho_{X,Y} = \frac{5/4}{\sqrt{\dfrac{55}{64} \cdot \dfrac{5}{2}}} = \sqrt{\frac{8}{11}} \approx 0.85
    $$
    """
            ),
            theorem(
                r"""
    $$
    \rho_{X,Y} \in [-1, 1] \qquad (\text{cosine of the “angle” between } X, Y)
    $$

    and

    $$
    \rho_{X,Y} = \pm 1 \qquad \Longleftrightarrow \qquad \underbrace{Y = aX + b}_{\footnotesize \text{linear relation!}} \quad \text{with } \pm a > 0
    $$
    """,
                "Range of the correlation",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    v_sx = mo.ui.slider(1, 2, 0.1, value=2, label=r"$\sigma_X$", show_value=True)
    v_sy = mo.ui.slider(1, 2, 0.1, value=1.5, label=r"$\sigma_Y$", show_value=True)
    v_rho = mo.ui.slider(-1, 1, 0.05, value=0.5, label=r"$\rho_{X,Y}$", show_value=True)
    return v_rho, v_sx, v_sy


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, RED, blank, math, mo, np, num, table, v_rho, v_sx, v_sy, vector):
    _sx, _sy, _rho = v_sx.value, v_sy.value, round(v_rho.value, 2) + 0.0
    _th = math.acos(_rho)
    _X, _Y = (_sx, 0.0), (round(_sy * math.cos(_th), 9), round(_sy * math.sin(_th), 9))
    _S = (round(_X[0] + _Y[0], 9), _Y[1])
    _cov = _rho * _sx * _sy
    _var = _sx**2 + _sy**2 + 2 * _cov

    _fig, _ax = blank(5.6, 2.45, (-2.4, 4.4), (-0.45, 2.45))
    _ax.plot([_X[0], _S[0]], [_X[1], _S[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([_Y[0], _S[0]], [_Y[1], _S[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    if _rho == 0:
        _r = 0.2
        _ax.plot([_r, _r, 0], [0, _r, _r], color=GREY, lw=1.0)
    elif _rho < 1:
        _t = np.linspace(0, _th, 60)
        _ax.plot(0.4 * np.cos(_t), 0.4 * np.sin(_t), color=GREY, lw=1.0)
        _sd = math.atan2(_S[1], _S[0])
        _m = _th / 2 if _rho == -1 else (_sd + _th) / 2 if _sx >= _sy else _sd / 2
        _ax.text(0.65 * math.cos(_m), 0.65 * math.sin(_m), r"$\theta$", color=GREY, fontsize=13, ha="center", va="center")
    vector(_ax, (0, 0), _S, GREEN, r"$X + Y$", turn=(-135 if _S == (0, 0) else -90) if _rho == -1 else math.degrees(_th / 2 - math.atan2(_S[1], _S[0])))
    for _args in sorted([(_X, BLUE, "$X$", -40), (_Y, RED, "$Y$", 40)], key=lambda _v: -math.hypot(*_v[0])):
        vector(_ax, (0, 0), _args[0], _args[1], _args[2], turn=_args[3])

    mo.vstack(
        [
            mo.hstack([v_sx, v_sy, v_rho], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\mathrm{Var}(X + Y) = \sigma_X^2 + \sigma_Y^2 + 2\, \rho_{X,Y}\, \sigma_X \sigma_Y$ &nbsp; (length of the green arrow, squared)", rf"${num(_var)}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    g_a = mo.ui.slider(-2, 2, 0.1, value=1, label="$a$", show_value=True)
    g_b = mo.ui.slider(0, 2, 0.1, value=1, label="$b$", show_value=True)
    return g_a, g_b


@app.cell(hide_code=True)
def _(np):
    # one fixed sample (fixed seed); moving a or c keeps it
    g_xy = np.random.default_rng(1515).standard_normal((2, 400))
    return (g_xy,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, g_a, g_b, g_xy, math, mo, np, num, table):
    _a, _b = round(g_a.value, 1) + 0.0, round(g_b.value, 1) + 0.0
    _X, _Y = g_xy
    _Z = _a * _X + _b * _Y
    _prod = _X * _Z  # both means are 0, so the sign of the product gives the quadrant

    _fig = Figure(figsize=(4.6, 4.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.axhline(0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    for _mask, _color in ((_prod > 0, BLUE), (_prod < 0, RED), (_prod == 0, GREY)):
        _ax.scatter(_X[_mask], _Z[_mask], s=10, color=_color, lw=0, zorder=3)
    for _q, _xy, _ha, _va, _color in (("Q1", (0.99, 0.98), "right", "top", BLUE), ("Q2", (0.01, 0.98), "left", "top", RED), ("Q3", (0.01, 0.02), "left", "bottom", BLUE), ("Q4", (0.99, 0.02), "right", "bottom", RED)):
        _ax.text(*_xy, _q, transform=_ax.transAxes, color=_color, fontsize=13, ha=_ha, va=_va)
    # the frame follows the spread of Z (sigma_Z = sqrt(a^2 + b^2)), never smaller than that of X; one scale on both axes
    _lim = 3.5 * max(1.0, math.sqrt(_a**2 + _b**2))
    _ax.set_xlim(-_lim, _lim)
    _ax.set_ylim(-_lim, _lim)
    _ax.set_aspect("equal")
    _ax.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _ax.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$z$", rotation=0, labelpad=10)
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _var = _a**2 + _b**2
    _rho = rf"${num(_a / math.sqrt(_var))}$" if _var > 0 else "undefined"
    mo.vstack(
        [
            mo.md(r"400 simulated values of $(X, Z)$, with $X, Y \sim \mathcal{N}(0, 1)$ independent and $Z = aX + bY$"),
            mo.hstack([g_a, g_b], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\rho_{X,Z} = a / \sqrt{a^2 + b^2}$", _rho),
                    (r"share of the points in Q1 and Q3 &nbsp; (blue)", rf"${100 * float(np.mean(_prod > 0)):.0f}\%$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, RED, mo):
    _fig = Figure(figsize=(HALF, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill_between([0, 3], [0, 3], 3, color=LIGHT, lw=0)
    _ax.plot([0, 3], [0, 3], color=GREY, lw=1.0)
    _ax.plot([1, 1], [1, 3], color=RED, lw=1.6)
    _ax.plot([0, 3], [0, 0], color=BLUE, lw=2.4, solid_capstyle="butt", clip_on=False)
    _ax.plot(1, 2.1, "o", color="black", ms=4, zorder=4)
    _ax.annotate("$(x, y)$", (1, 2.1), textcoords="offset points", xytext=(6, 2), fontsize=12, ha="left", va="bottom")
    _ax.text(2.3, 2.75, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    _ax.set_xlim(0, 3)
    _ax.set_ylim(0, 3)
    _ax.set_aspect("equal")
    _ax.set_xticks([1], ["$x$"])
    _ax.set_yticks([1, 2.1], ["$x$", "$y$"])
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(
                r"""
    **Example** (Customer arrivals, average rate $\lambda > 0$).

    $X$ = arrival time of 1st customer $\sim \mathrm{Gamma}(1, \lambda)$

    $Y$ = arrival time of 2nd customer $\sim \mathrm{Gamma}(2, \lambda)$

    $$
    \begin{aligned}
    &\leadsto \quad f_{X,Y}(x, y) = \lambda^2 e^{-\lambda y}, &\quad& 0 < x < y \\[6pt]
    &\leadsto \quad f_{Y|X}(y \mid x) = \lambda e^{-\lambda (y - x)}, && y > x
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \mu_X &= E[X] = \frac{1}{\lambda}, & \qquad \mu_Y &= E[Y] = \frac{2}{\lambda} \\[14pt]
    \sigma_X^2 &= \mathrm{Var}(X) = \frac{1}{\lambda^2}, & \sigma_Y^2 &= \mathrm{Var}(Y) = \frac{2}{\lambda^2}
    \end{aligned}
    $$

    $$
    \sigma_{X,Y} = \mathrm{Cov}(X, Y) = E[XY] - \mu_X \mu_Y
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    <span class="chain">$\displaystyle E[XY] = \int_{S_{X,Y}} xy\, f_{X,Y}(x, y)\, dx\, dy$ $\displaystyle = \int_{S_{X,Y}} xy\, f_{Y|X}(y \mid x)\, f_X(x)\, dx\, dy$ $\displaystyle = \int_{0}^{\infty} x \left( \int_{x}^{\infty} y\, f_{Y|X}(y \mid x)\, dy \right) f_X(x)\, dx$ $\displaystyle = \int_{0}^{\infty} x \left( \int_{x}^{\infty} y\, \lambda e^{-\lambda (y - x)}\, dy \right) \lambda e^{-\lambda x}\, dx$ $\displaystyle = \int_{0}^{\infty} x \left( x + \frac{1}{\lambda} \right) \lambda e^{-\lambda x}\, dx$ $\displaystyle = E[X^2] + \frac{1}{\lambda}\, E[X] = \frac{2}{\lambda^2} + \frac{1}{\lambda^2} = \frac{3}{\lambda^2}$</span>

    $$
    \Longrightarrow \qquad \mathrm{Cov}(X, Y) = \frac{1}{\lambda^2}, \qquad \rho_{X,Y} = \frac{1/\lambda^2}{\sqrt{2/\lambda^4}} = \frac{1}{\sqrt{2}}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ### Question 1

    Let $X, Y$ have joint pmf

    $$
    f_{X,Y}(x, y) = \begin{cases} 0.4 & \text{if } (x, y) = (0, 0) \text{ or } (1, 1) \\ 0.1 & \text{if } (x, y) = (0, 1) \text{ or } (1, 0) \\ 0 & \text{otherwise} \end{cases}
    $$

    Find:

    (a) marginal pmfs of $X$ and of $Y$

    $\leadsto$ &nbsp; are $X$ and $Y$ independent?

    (b) conditional pmf of $Y$ given $X = 1$

    $\leadsto$ &nbsp; conditional expectation of $Y$ given $X = 1$?

    (c) covariance and correlation of $X$ and $Y$

    (d) $\mathrm{Var}(X + Y)$
    """)
    return

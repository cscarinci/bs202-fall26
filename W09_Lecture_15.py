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
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#1b458f", "#b3261e", "#2e7d32", "#e65100", "#888888", "#cfe3f5"
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
        One head size and one line weight for every figure, so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>,head_width=0.15,head_length=0.35", "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 15", "Week 09", "Lecture 15 · Covariance and correlation")
    return


@app.cell(hide_code=True)
def _(arrow, math):
    def vector(ax, tail, tip, color, label=None, turn=0, r=15, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip on a white box;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            arrow(ax, tail, tip, color, **kw)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    return (vector,)


@app.cell(hide_code=True)
def _(mo):
    def ask(label, field, answer, tol=1e-6):
        """A labelled answer box with a feedback mark; accepts decimals, decimal commas and percentages."""
        raw = field.value.strip()
        mark = ""
        if raw:
            try:
                value = float(raw.rstrip("%").replace(",", ".")) / (100 if raw.endswith("%") else 1)
                mark = "✅" if abs(value - answer) <= tol else "❌ try again"
            except ValueError:
                mark = "⚠️ enter a number"
        return mo.hstack([mo.md(label), field, mo.md(mark)], justify="start", align="center")

    def box():
        return mo.ui.text(placeholder="?", debounce=True)

    return ask, box


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

    return dice_counts, over, tex


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

    **In this lecture:** how strongly are $X$ and $Y$ related? &nbsp; $\leadsto$ &nbsp; covariance and correlation

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
    \underbrace{E[u(X, Y)]}_{\text{expectation of } u(X, Y)} = \sum_x \sum_y u(x, y)\, f_{X,Y}(x, y) \qquad \text{or} \qquad \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} u(x, y)\, f_{X,Y}(x, y)\, dx\, dy
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

    $$
    \begin{aligned}
    \sum_x \sum_y u(x)\, v(y)\, f_{X,Y}(x, y) &\overset{\text{independence}}{=} \sum_x \sum_y u(x)\, v(y)\, f_X(x)\, f_Y(y) \\[6pt]
    &= \sum_x u(x)\, f_X(x) \sum_y v(y)\, f_Y(y) \qquad \square
    \end{aligned}
    $$
    """
            ),
        ]
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

    is called the **covariance** of $X$ and $Y$ &nbsp; $\leadsto$ &nbsp; $\mu_X = E[X]$, $\mu_Y = E[Y]$ means of $X$, $Y$
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
    \begin{aligned}
    \mathrm{Cov}(X, Y) &= \mathrm{Cov}(Y, X) && \text{symmetric} \\[4pt]
    \mathrm{Cov}(aX + bY, Z) &= a\, \mathrm{Cov}(X, Z) + b\, \mathrm{Cov}(Y, Z) && \text{bilinear} \\[4pt]
    \mathrm{Cov}(X, Y) &= 0 && \text{if } X, Y \text{ are independent}
    \end{aligned}
    $$
    """,
                "Properties of covariance",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $\mathrm{Cov}$ is like an inner product and independent random variables are orthogonal!

    $\leadsto$ &nbsp; $\mathrm{Var}$ is like length squared! &nbsp; (However, some non-zero random variables have zero variance!)

    **Remark.** Not every pair $(X, Y)$ of random variables with $\mathrm{Cov}(X, Y) = 0$ is independent!

    **Example.** &nbsp; $(X, Y)$ **uniform** on $S_{X,Y} = \{\, (x, y) \mid |x| + |y| < 1 \,\}$ &nbsp; $\leadsto$ &nbsp; $f_{X,Y}(x, y) = c = \dfrac{1}{2}$
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

    $$
    \begin{aligned}
    \Longrightarrow \qquad \sigma_{X,Y} = E[XY] - \mu_X \mu_Y &= \int_{-1}^{1} \int_{-(1 - |x|)}^{1 - |x|} xy\, \frac{1}{2}\, dy\, dx \\[6pt]
    &= \int_{-1}^{1} x\, \underbrace{\left. \frac{y^2}{4} \right|_{-(1 - |x|)}^{1 - |x|}}_{=\, 0}\, dx = 0
    \end{aligned}
    $$

    But &nbsp; $f_{X,Y}(x, y) = \dfrac{1}{2} \neq f_X(x)\, f_Y(y) = (1 - |x|)(1 - |y|)$ &nbsp; for most $(x, y) \in S_{X,Y}$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    d_x = mo.ui.slider(-0.9, 0.9, 0.05, value=0.5, label="given value $x$ of $X$", show_value=True)
    return (d_x,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, RED, d_x, mo, np, table):
    _x = d_x.value
    _h = 1 - abs(_x)  # the slice X = x of the diamond is the interval |y| < 1 - |x|
    _top = max(1.0, 1 / (2 * _h))

    _fig = Figure(figsize=(FULL, 2.9), layout="constrained")
    _left, _right = _fig.subplots(1, 2, gridspec_kw={"width_ratios": [1, 1.4]})

    # left: the diamond and its slice at X = x
    _left.fill([1, 0, -1, 0], [0, 1, 0, -1], facecolor=LIGHT, edgecolor=GREY, lw=1.0)
    _left.axhline(0, color="black", lw=0.8)
    _left.axvline(0, color="black", lw=0.8)
    _left.plot([_x, _x], [-_h, _h], color=BLUE, lw=2.4, solid_capstyle="butt")
    _left.plot(_x, 0, "o", color=GREEN, ms=5, zorder=4)
    _left.annotate("$x$", (_x, -_h), textcoords="offset points", xytext=(0, -6), color=BLUE, fontsize=12, ha="center", va="top")
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
    _right.text(1.1, 1.15 * _top, r"$f_{Y|X}(y \mid x)$", color=BLUE, fontsize=12, ha="right", va="top")
    _right.text(1.1, 0.97 * _top, r"$f_Y(y)$", color=RED, fontsize=12, ha="right", va="top")
    _right.set_xlim(-1.1, 1.1)
    _right.set_ylim(0, 1.2 * _top)
    _right.set_xlabel("$y$")
    _right.spines["top"].set_visible(False)
    _right.spines["right"].set_visible(False)
    for _ax in (_left, _right):
        _ax.tick_params(labelsize=12)

    mo.vstack(
        [
            mo.hstack([d_x], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f_X(x) = 1 - \lvert x \rvert$", rf"${_h:.2f}$"),
                    (r"$f_{Y\vert X}(y \mid x) = \dfrac{1/2}{1 - \lvert x \rvert}$ &nbsp; for $\lvert y \rvert < 1 - \lvert x \rvert$", rf"$\textcolor{{{BLUE}}}{{{1 / (2 * _h):.3f}}}$"),
                    (r"$E[Y \mid X = x]$ &nbsp; (green)", rf"$\textcolor{{{GREEN}}}{{0}}$"),
                ]
            ),
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
    | $y = 8$ | $0$ | $0$ | $0$ | $\dfrac{1}{16}$ | $\dfrac{1}{16}$ |
    | $7$ | $0$ | $0$ | $0$ | $\dfrac{2}{16}$ | $\dfrac{2}{16}$ |
    | $6$ | $0$ | $0$ | $\dfrac{1}{16}$ | $\dfrac{2}{16}$ | $\dfrac{3}{16}$ |
    | $5$ | $0$ | $0$ | $\dfrac{2}{16}$ | $\dfrac{2}{16}$ | $\dfrac{4}{16}$ |
    | $4$ | $0$ | $\dfrac{1}{16}$ | $\dfrac{2}{16}$ | $0$ | $\dfrac{3}{16}$ |
    | $3$ | $0$ | $\dfrac{2}{16}$ | $0$ | $0$ | $\dfrac{2}{16}$ |
    | $2$ | $\dfrac{1}{16}$ | $0$ | $0$ | $0$ | $\dfrac{1}{16}$ |
    | $f_X(x)$ | $\dfrac{1}{16}$ | $\dfrac{3}{16}$ | $\dfrac{5}{16}$ | $\dfrac{7}{16}$ | $1$ |

    $$
    E[X] = 1 \cdot \frac{1}{16} + 2 \cdot \frac{3}{16} + 3 \cdot \frac{5}{16} + 4 \cdot \frac{7}{16} = \frac{50}{16}
    $$

    $$
    E[Y] = 2 \cdot \frac{1}{16} + 3 \cdot \frac{2}{16} + 4 \cdot \frac{3}{16} + 5 \cdot \frac{4}{16} + 6 \cdot \frac{3}{16} + 7 \cdot \frac{2}{16} + 8 \cdot \frac{1}{16} = \frac{80}{16}
    $$

    $$
    E[XY] = 1 \cdot 2 \cdot \frac{1}{16} + 2 \cdot 3 \cdot \frac{2}{16} + 2 \cdot 4 \cdot \frac{1}{16} + 3 \cdot 4 \cdot \frac{2}{16} + \cdots + 4 \cdot 8 \cdot \frac{1}{16} = \frac{270}{16}
    $$

    $$
    \Longrightarrow \qquad \mathrm{Cov}(X, Y) = \sigma_{X,Y} = \frac{270 - 50 \cdot 5}{16} = \frac{5}{4} > 0
    $$

    $\leadsto$ &nbsp; big largest face goes together with big sum
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    k_sides = mo.ui.slider(2, 8, 1, value=4, label="sides of each die", show_value=True)
    return (k_sides,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, Fraction, GREY, RED, dice_counts, k_sides, mo, over, table, tex):
    _n = k_sides.value
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

    _fig = Figure(figsize=(FULL, 3.6), layout="constrained")
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
            mo.hstack([k_sides], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\mu_X = E[X]$", rf"${over(_sx, _N)}$"),
                    (r"$\mu_Y = E[Y]$", rf"${over(_sy, _N)}$"),
                    (r"$E[XY]$", rf"${over(_sxy, _N)}$"),
                    (r"$\mathrm{Cov}(X, Y) = E[XY] - \mu_X \mu_Y$", rf"${tex(_plus + _minus)}$"),
                    (r"contributions $(x - \mu_X)(y - \mu_Y)\, f_{X,Y}(x, y)$ from Q1 and Q3 &nbsp; (blue)", rf"$\textcolor{{{BLUE}}}{{{tex(_plus)}}}$"),
                    (r"contributions from Q2 and Q4 &nbsp; (red)", rf"$\textcolor{{{RED}}}{{{tex(_minus)}}}$"),
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

    $$
    \begin{aligned}
    \mathrm{Var}(aX + bY) &= \mathrm{Cov}(aX + bY,\ aX + bY) \\[4pt]
    &= a^2\, \mathrm{Cov}(X, X) + b^2\, \mathrm{Cov}(Y, Y) + 2ab\, \mathrm{Cov}(X, Y) \qquad \square
    \end{aligned}
    $$
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
    \rho_{X,Y} = \pm 1 \qquad \Longleftrightarrow \qquad \underbrace{Y = aX + b}_{\text{linear relation!}} \quad \text{with } \pm a > 0
    $$
    """,
                "Range of the correlation",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    v_sx = mo.ui.slider(0.5, 2, 0.1, value=2, label=r"$\sigma_X$", show_value=True)
    v_sy = mo.ui.slider(0.5, 2, 0.1, value=1.5, label=r"$\sigma_Y$", show_value=True)
    v_rho = mo.ui.slider(-1, 1, 0.05, value=0.5, label=r"$\rho_{X,Y}$", show_value=True)
    return v_rho, v_sx, v_sy


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, RED, blank, math, mo, np, table, v_rho, v_sx, v_sy, vector):
    _sx, _sy, _rho = v_sx.value, v_sy.value, round(v_rho.value, 2) + 0.0
    _th = math.acos(_rho)
    _X, _Y = (_sx, 0.0), (round(_sy * math.cos(_th), 9), round(_sy * math.sin(_th), 9))
    _S = (round(_X[0] + _Y[0], 9), _Y[1])
    _cov = _rho * _sx * _sy
    _var = _sx**2 + _sy**2 + 2 * _cov

    _fig, _ax = blank(FULL, 3.1, (-2.4, 4.4), (-0.45, 2.45))
    _ax.plot([_X[0], _S[0]], [_X[1], _S[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([_Y[0], _S[0]], [_Y[1], _S[1]], color=GREY, lw=1.0, ls=(0, (4, 3)))
    if _rho == 0:
        _r = 0.2
        _ax.plot([_r, _r, 0], [0, _r, _r], color=GREY, lw=1.0)
    elif _rho < 1:
        _t = np.linspace(0, _th, 60)
        _ax.plot(0.4 * np.cos(_t), 0.4 * np.sin(_t), color=GREY, lw=1.0)
        _ax.text(0.58 * math.cos(_th / 2), 0.58 * math.sin(_th / 2), r"$\theta$", color=GREY, fontsize=13, ha="center", va="center")
    vector(_ax, (0, 0), _S, GREEN, r"$X + Y$", turn=-90 if _S == (0, 0) else 0)
    vector(_ax, (0, 0), _X, BLUE, "$X$", turn=-40)
    vector(_ax, (0, 0), _Y, RED, "$Y$", turn=40)

    mo.vstack(
        [
            mo.hstack([v_sx, v_sy, v_rho], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\theta$ with $\cos \theta = \rho_{X,Y}$", rf"${math.degrees(_th):.1f}^\circ$"),
                    (r"$\mathrm{Cov}(X, Y) = \rho_{X,Y}\, \sigma_X \sigma_Y$", rf"${_cov:.3f}$"),
                    (r"$\mathrm{Var}(X + Y) = \sigma_X^2 + \sigma_Y^2 + 2\, \mathrm{Cov}(X, Y)$ &nbsp; (green length, squared)", rf"$\textcolor{{{GREEN}}}{{{_var:.3f}}}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    g_a =mo.ui.slider(-2, 2, 0.1, value=1, label="$a$", show_value=True)
    g_c = mo.ui.slider(0, 2, 0.1, value=1, label="$c$", show_value=True)
    g_redo = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Repeat")
    return g_a, g_c, g_redo


@app.cell(hide_code=True)
def _(g_redo, np):
    # a fresh sample, unseeded, on every run of the page and every press of Repeat; moving a or c keeps it
    _presses = g_redo.value
    g_xw = np.random.default_rng().standard_normal((2, 400))
    return (g_xw,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, RED, g_a, g_c, g_redo, g_xw, math, mo, np, table):
    _a, _c = round(g_a.value, 1) + 0.0, round(g_c.value, 1) + 0.0
    _X, _W = g_xw
    _Y = _a * _X + _c * _W
    _prod = _X * _Y  # both means are 0, so the sign of the product gives the quadrant

    _fig = Figure(figsize=(FULL, 3.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.axhline(0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    for _mask, _color in ((_prod > 0, BLUE), (_prod < 0, RED), (_prod == 0, GREY)):
        _ax.scatter(_X[_mask], _Y[_mask], s=10, color=_color, lw=0, zorder=3)
    for _q, _xy, _ha, _va, _color in (("Q1", (0.99, 0.98), "right", "top", BLUE), ("Q2", (0.01, 0.98), "left", "top", RED), ("Q3", (0.01, 0.02), "left", "bottom", BLUE), ("Q4", (0.99, 0.02), "right", "bottom", RED)):
        _ax.text(*_xy, _q, transform=_ax.transAxes, color=_color, fontsize=13, ha=_ha, va=_va)
    _ax.set_xlim(-3.5, 3.5)
    _ax.set_ylim(-7, 7)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$y$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _var = _a**2 + _c**2
    _rho = rf"${_a / math.sqrt(_var):.3f}$" if _var > 0 else r"undefined ($\sigma_Y = 0$)"
    mo.vstack(
        [
            mo.md(r"400 simulated values of $(X, Y)$, with $X, W \sim \mathcal{N}(0, 1)$ independent and $Y = aX + cW$"),
            mo.hstack([g_a, g_c, g_redo], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\mathrm{Cov}(X, Y) = a\, \mathrm{Var}(X) + c\, \mathrm{Cov}(W, X) = a$", rf"${_a:.1f}$"),
                    (r"$\mathrm{Var}(Y) = a^2\, \mathrm{Var}(X) + c^2\, \mathrm{Var}(W) = a^2 + c^2$", rf"${_var:.2f}$"),
                    (r"$\rho_{X,Y} = a / \sqrt{a^2 + c^2}$", _rho),
                    (r"points in Q1 and Q3 &nbsp; (blue)", rf"${100 * float(np.mean(_prod > 0)):.0f}\%$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, mo):
    _fig = Figure(figsize=(HALF, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill_between([0, 3], [0, 3], 3, color=LIGHT, lw=0)
    _ax.plot([0, 3], [0, 3], color=GREY, lw=1.0)
    _ax.plot([1, 1], [1, 3], color=BLUE, lw=1.6)
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

    $X$ = arrival time of 1st customer $\sim \mathrm{Gamma}(1, \lambda)$, &nbsp; $Y$ = arrival time of 2nd customer $\sim \mathrm{Gamma}(2, \lambda)$

    $$
    \leadsto \quad f_{X,Y}(x, y) = \lambda^2 e^{-\lambda y}, \quad 0 < x < y \qquad \leadsto \quad f_{Y|X}(y \mid x) = \lambda e^{-\lambda (y - x)}, \quad y > x
    $$

    $$
    \mu_X = E[X] = \frac{1}{\lambda}, \qquad \mu_Y = E[Y] = \frac{2}{\lambda}, \qquad \sigma_X^2 = \mathrm{Var}(X) = \frac{1}{\lambda^2}, \qquad \sigma_Y^2 = \mathrm{Var}(Y) = \frac{2}{\lambda^2}
    $$

    $$
    \sigma_{X,Y} = \mathrm{Cov}(X, Y) = E[XY] - \mu_X \mu_Y
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \begin{aligned}
    E[XY] &= \int_{S_{X,Y}} xy\, \underbrace{f_{X,Y}(x, y)}_{f_{Y|X}(y \mid x)\, f_X(x)}\, dx\, dy = \int_{0}^{\infty} x \left( \int_{x}^{\infty} y\, f_{Y|X}(y \mid x)\, dy \right) f_X(x)\, dx \\[6pt]
    &= \int_{0}^{\infty} x \left( \int_{x}^{\infty} y\, \lambda e^{-\lambda (y - x)}\, dy \right) \lambda e^{-\lambda x}\, dx = \int_{0}^{\infty} x \left( x + \frac{1}{\lambda} \right) \lambda e^{-\lambda x}\, dx \\[6pt]
    &= E[X^2] + \frac{1}{\lambda}\, E[X] = \frac{2}{\lambda^2} + \frac{1}{\lambda^2} = \frac{3}{\lambda^2}
    \end{aligned}
    $$

    $$
    \Longrightarrow \qquad \mathrm{Cov}(X, Y) = \frac{1}{\lambda^2}, \qquad \rho_{X,Y} = \frac{1/\lambda^2}{\sqrt{2/\lambda^4}} = \frac{1}{\sqrt{2}}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(box):
    answers = tuple(box() for _ in range(4))
    pmf_answers = tuple(box() for _ in range(4))
    cond_answers = tuple(box() for _ in range(2))
    return answers, cond_answers, pmf_answers


@app.cell(hide_code=True)
def _(answers, ask, cond_answers, mo, pmf_answers):
    _e, _cov, _rho, _var = answers
    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $X, Y$ have joint pmf

    $$
    f_{X,Y}(x, y) = \begin{cases} 0.4 & \text{if } (x, y) = (0, 0) \text{ or } (1, 1) \\ 0.1 & \text{if } (x, y) = (0, 1) \text{ or } (1, 0) \\ 0 & \text{otherwise} \end{cases}
    $$

    Find:

    (a) marginal pmfs of $X$ and of $Y$
    """
            ),
            *[ask(rf"$f_{_r}({_v}) =$", _f, 0.5, 0.0005) for (_r, _v), _f in zip((("X", 0), ("X", 1), ("Y", 0), ("Y", 1)), pmf_answers)],
            mo.md(
                r"""
    $\leadsto$ &nbsp; are $X$ and $Y$ independent?

    (b) conditional pmf of $Y$ given $X = 1$
    """
            ),
            *[ask(rf"$f_{{Y|X}}({_y} \mid 1) =$", _f, _p, 0.0005) for _y, _f, _p in zip(range(2), cond_answers, (0.2, 0.8))],
            mo.md(r"$\leadsto$ &nbsp; conditional expectation of $Y$ given $X = 1$?"),
            ask(r"$E[Y \mid X = 1] =$", _e, 0.8, 0.0005),
            mo.md(r"(c) covariance and correlation of $X$ and $Y$"),
            ask(r"$\mathrm{Cov}(X, Y) =$", _cov, 0.15, 0.0005),
            ask(r"$\rho_{X,Y} =$", _rho, 0.6, 0.0005),
            mo.md(r"(d) $\mathrm{Var}(X + Y)$"),
            ask(r"$\mathrm{Var}(X + Y) =$", _var, 0.8, 0.0005),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - $E[u(X, Y)] = \sum_x \sum_y u(x, y)\, f_{X,Y}(x, y)$ or $\iint u(x, y)\, f_{X,Y}(x, y)\, dx\, dy$; &nbsp; linear, and for $X, Y$ independent

        $$
        E[u(X)\, v(Y)] = E[u(X)]\, E[v(Y)]
        $$
    - covariance: symmetric and bilinear, with $\mathrm{Cov}(X, X) = \mathrm{Var}(X)$

        $$
        \sigma_{X,Y} = \mathrm{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - \mu_X \mu_Y
        $$

        $\mathrm{Cov}(X, Y) > 0$: $X$ and $Y$ get large or small together
    - $X, Y$ independent $\Longrightarrow$ $\mathrm{Cov}(X, Y) = 0$, but not conversely: $(X, Y)$ uniform on $|x| + |y| < 1$
    - variance of a linear combination (for $X, Y$ independent, the last term drops: like Pythagoras)

        $$
        \mathrm{Var}(aX + bY) = a^2\, \mathrm{Var}(X) + b^2\, \mathrm{Var}(Y) + 2ab\, \mathrm{Cov}(X, Y)
        $$
    - correlation, the normalized covariance:

        $$
        \rho_{X,Y} = \frac{\sigma_{X,Y}}{\sigma_X\, \sigma_Y} \in [-1, 1], \qquad \rho_{X,Y} = \pm 1 \ \Longleftrightarrow \ Y = aX + b \ \text{ with } \pm a > 0
        $$
    - two 4-sided dice and customer arrivals:

        $$
        \text{dice: } \ \mathrm{Cov}(X, Y) = \frac{5}{4}, \ \ \rho_{X,Y} = \sqrt{\frac{8}{11}} \approx 0.85, \qquad \text{arrivals: } \ \mathrm{Cov}(X, Y) = \frac{1}{\lambda^2}, \ \ \rho_{X,Y} = \frac{1}{\sqrt{2}}
        $$
    """)
    return


if __name__ == "__main__":
    app.run()

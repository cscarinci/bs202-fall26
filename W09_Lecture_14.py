import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 14 · Joint and conditional distributions", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math
    from fractions import Fraction

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap, PowerNorm
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Figure, Fraction, LinearSegmentedColormap, PowerNorm, math, mo, np


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
            return "correct" if abs(float(s) - answer) < 1e-6 else "try again"
        except ValueError:
            return "enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 14", "Week 09", "Lecture 14 · Joint and conditional distributions")
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
def _(BLUE, LinearSegmentedColormap, PowerNorm):
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
        return f"{q.numerator}" if q.denominator == 1 else rf"\dfrac{{{q.numerator}}}{{{q.denominator}}}"

    def density(ax, f, extent, top):
        """Draw the joint pdf values `f` (NaN outside the state space) as a density: white where it is 0,
        BLUE where it reaches `top`, on a square-root scale so that the tail stays visible."""
        cmap = LinearSegmentedColormap.from_list("density", ["white", BLUE])
        ax.imshow(f, origin="lower", extent=extent, cmap=cmap, norm=PowerNorm(0.5, vmin=0, vmax=top), aspect="auto", interpolation="bilinear")

    return density, dice_counts, over, tex


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## So far

    Probabilistic models &nbsp; $\leadsto$ &nbsp; one measurement on a random experiment &nbsp; $\leadsto$ &nbsp; single random variable $X : S \longrightarrow \mathbb{R}$

    $$
    P(X \in A) = \sum_{x \in S_X \cap A} f_X(x) \quad \text{or} \quad \int_{S_X \cap A} f_X(x)\, dx \qquad (A \subseteq \mathbb{R})
    $$

    $$
    E[u(X)] = \sum_{x \in S_X} u(x)\, f_X(x) \quad \text{or} \quad \int_{S_X} u(x)\, f_X(x)\, dx
    $$

    **In this lecture:** multiple measurements on the same experiment &nbsp; $\leadsto$ &nbsp; joint behavior, mutual dependence, conditional expectations

    **References:** WMS 5.2–5.4, 5.11
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## IV.1 &nbsp; Joint and conditional distributions

    ### Joint distributions
    """
            ),
            definition(
                r"""
    Let $X, Y : S \longrightarrow \mathbb{R}$ be random variables on the same $(S, \mathcal{E}, P)$. The **joint distribution** of the pair

    $$
    \underbrace{(X, Y) : S \longrightarrow \mathbb{R}^2}_{\text{a vector valued random variable}}
    $$

    is the assignment of probabilities

    $$
    P_{X,Y}(A) = P((X, Y) \in A), \qquad \text{for } A \subseteq \mathbb{R}^2
    $$

    The **state space** of $(X, Y)$ is $S_{X,Y} = \mathrm{Im}(X, Y) \subseteq \mathbb{R}^2$

    - $\leadsto$ &nbsp; we call $(X, Y)$ **discrete** if $S_{X,Y}$ is countable

        $$
        \Longrightarrow \qquad P_{X,Y}(A) = \sum_{(x, y) \in S_{X,Y} \cap A} \underbrace{f_{X,Y}(x, y)}_{\text{joint pmf of } (X, Y)}
        $$

    - $\leadsto$ &nbsp; we call $(X, Y)$ **continuous** if $S_{X,Y}$ is uncountable **and** there exists $f_{X,Y} : \mathbb{R}^2 \longrightarrow \mathbb{R}$ with

        $$
        P_{X,Y}(A) = \iint_{S_{X,Y} \cap A} \underbrace{f_{X,Y}(x, y)}_{\substack{\text{joint pdf of } (X, Y) \\ \text{(integrable function)}}}\, dx\, dy
        $$

    - $\leadsto$ &nbsp; in both cases

        $$
        f_{X,Y}(x, y) \geq 0, \qquad f_{X,Y}(x, y) = 0 \ \text{ for } (x, y) \notin S_{X,Y}, \qquad P_{X,Y}(S_{X,Y}) = 1
        $$
    """,
                "Joint distribution",
            ),
            mo.md(
                r"""
    **Example** (Roll two fair 4-sided dice). &nbsp; $\leadsto$ &nbsp; $S = \{\, (i, j) \mid i, j = 1, 2, 3, 4 \,\}$

    $X$ = largest face, &nbsp; $Y$ = sum of faces

    | $f_{X,Y}(x, y)$ | $y = 2$ | $3$ | $4$ | $5$ | $6$ | $7$ | $8$ | $f_X(x)$ |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | $x = 1$ | $\dfrac{1}{16}$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $\dfrac{1}{16}$ |
    | $2$ | $0$ | $\dfrac{2}{16}$ | $\dfrac{1}{16}$ | $0$ | $0$ | $0$ | $0$ | $\dfrac{3}{16}$ |
    | $3$ | $0$ | $0$ | $\dfrac{2}{16}$ | $\dfrac{2}{16}$ | $\dfrac{1}{16}$ | $0$ | $0$ | $\dfrac{5}{16}$ |
    | $4$ | $0$ | $0$ | $0$ | $\dfrac{2}{16}$ | $\dfrac{2}{16}$ | $\dfrac{2}{16}$ | $\dfrac{1}{16}$ | $\dfrac{7}{16}$ |
    | $f_Y(y)$ | $\dfrac{1}{16}$ | $\dfrac{2}{16}$ | $\dfrac{3}{16}$ | $\dfrac{4}{16}$ | $\dfrac{3}{16}$ | $\dfrac{2}{16}$ | $\dfrac{1}{16}$ | |

    $$
    \leadsto \qquad P(X = 1,\ Y \leq 4) = \frac{1}{16} + 0 + 0 = \frac{1}{16}, \qquad P(X > 2,\ Y \leq 5) = \frac{6}{16}
    $$

    $$
    P(Y = 5) = \frac{4}{16}, \qquad P(X = 2) = \frac{3}{16}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    j_sides = mo.ui.slider(2, 6, 1, value=4, label="sides of each die", show_value=True)
    return (j_sides,)


@app.cell(hide_code=True)
def _(j_sides, mo):
    _n = j_sides.value
    j_x = mo.ui.range_slider(1, _n, 1, value=[min(3, _n), _n], label="$X$ from / to", show_value=True)
    j_y = mo.ui.range_slider(2, 2 * _n, 1, value=[2, min(5, 2 * _n)], label="$Y$ from / to", show_value=True)
    return j_x, j_y


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, LIGHT, dice_counts, j_sides, j_x, j_y, mo, over, table):
    _n = j_sides.value
    _N = _n**2
    _counts = dice_counts(_n)
    (_a, _b), (_c, _d) = j_x.value, j_y.value
    _xs, _ys = list(range(1, _n + 1)), list(range(2, 2 * _n + 1))
    _fx = [sum(k for (x, y), k in _counts.items() if x == v) for v in _xs]
    _fy = [sum(k for (x, y), k in _counts.items() if y == v) for v in _ys]
    _both = sum(k for (x, y), k in _counts.items() if _a <= x <= _b and _c <= y <= _d)
    _onx = sum(k for x, k in zip(_xs, _fx) if _a <= x <= _b)
    _ony = sum(k for y, k in zip(_ys, _fy) if _c <= y <= _d)

    _fig = Figure(figsize=(FULL, 4.6), layout="constrained")
    _grid = _fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 3])
    _main = _fig.add_subplot(_grid[1, 0])
    _top = _fig.add_subplot(_grid[0, 0], sharex=_main)
    _side = _fig.add_subplot(_grid[1, 1], sharey=_main)

    # the event {a <= X <= b, c <= Y <= d} is a rectangle in the plane; the joint pmf sits on S_{X,Y}
    _main.fill_between([_a - 0.5, _b + 0.5], _c - 0.5, _d + 0.5, color=LIGHT, lw=0)
    _main.plot([_a - 0.5, _b + 0.5, _b + 0.5, _a - 0.5, _a - 0.5], [_c - 0.5, _c - 0.5, _d + 0.5, _d + 0.5, _c - 0.5], color=GREY, lw=1.0, ls=(0, (4, 3)))
    for (_x, _y), _k in _counts.items():
        _color = BLUE if _a <= _x <= _b and _c <= _y <= _d else GREY
        _main.scatter(_x, _y, s=2400 * _k / _N, color=_color, lw=0, zorder=3)
        _main.annotate(f"{_k}/{_N}", (_x, _y), textcoords="offset points", xytext=(9, 0), va="center", fontsize=10, color=_color)
    _main.set_xlim(0.4, _n + 0.9)
    _main.set_ylim(1.3, 2 * _n + 0.7)
    _main.set_xticks(_xs)
    _main.set_yticks(_ys)
    _main.set_xlabel("$x$ (largest face)")
    _main.set_ylabel("$y$ (sum of faces)")

    # the marginal pmfs, written in the margins
    _cx = [BLUE if _a <= v <= _b else GREY for v in _xs]
    _top.vlines(_xs, 0, [k / _N for k in _fx], color=_cx, lw=1.0)
    _top.scatter(_xs, [k / _N for k in _fx], s=18, color=_cx, zorder=3)
    for _x, _k, _col in zip(_xs, _fx, _cx):
        _top.annotate(f"{_k}/{_N}", (_x, _k / _N), textcoords="offset points", xytext=(0, 4), ha="center", va="bottom", fontsize=10, color=_col)
    _top.set_ylim(0, 1.45 * max(_fx) / _N)
    _top.set_yticks([])
    _top.set_ylabel("$f_X(x)$", fontsize=12)
    _top.tick_params(labelbottom=False)
    _cy = [BLUE if _c <= v <= _d else GREY for v in _ys]
    _side.hlines(_ys, 0, [k / _N for k in _fy], color=_cy, lw=1.0)
    _side.scatter([k / _N for k in _fy], _ys, s=18, color=_cy, zorder=3)
    for _y, _k, _col in zip(_ys, _fy, _cy):
        _side.annotate(f"{_k}/{_N}", (_k / _N, _y), textcoords="offset points", xytext=(5, 0), ha="left", va="center", fontsize=10, color=_col)
    _side.set_xlim(0, 1.9 * max(_fy) / _N)
    _side.set_xticks([])
    _side.set_xlabel("$f_Y(y)$", fontsize=12)
    _side.tick_params(labelleft=False)
    for _ax in (_main, _top, _side):
        _ax.tick_params(labelsize=12)
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([j_sides, j_x, j_y], justify="start", gap=2, wrap=True),
            table(
                [
                    (rf"$P({_a} \leq X \leq {_b},\ {_c} \leq Y \leq {_d})$ &nbsp; (blue points)", rf"$\textcolor{{{BLUE}}}{{{over(_both, _N)}}}$"),
                    (rf"$P({_a} \leq X \leq {_b})$ &nbsp; (top margin)", rf"${over(_onx, _N)}$"),
                    (rf"$P({_c} \leq Y \leq {_d})$ &nbsp; (right margin)", rf"${over(_ony, _N)}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Marginal distributions"""),
            theorem(
                r"""
    The pmfs/pdfs of $X$ and $Y$ alone can be recovered from the joint pmf/pdf of $(X, Y)$ via

    $$
    \begin{aligned}
    f_X(x) &= \sum_y f_{X,Y}(x, y) \qquad \text{or} \qquad \int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dy \\[6pt]
    f_Y(y) &= \sum_x f_{X,Y}(x, y) \qquad \text{or} \qquad \int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dx
    \end{aligned}
    $$

    $\leadsto$ &nbsp; **marginal distributions**
    """,
                "Marginal distributions",
            ),
            mo.md(
                r"""
    **Remark.** The joint distribution determines the marginals, but the marginals **do not** determine the joint! &nbsp; $\leadsto$ &nbsp; distinct joint distributions can define the same marginals!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    m_prod = mo.ui.switch(value=False, label=r"$f_X(x)\, f_Y(y)$")
    return (m_prod,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, RED, dice_counts, m_prod, mo):
    _counts = dice_counts(4)
    _xs, _ys = list(range(1, 5)), list(range(2, 9))
    _fx = [sum(k for (x, y), k in _counts.items() if x == v) for v in _xs]
    _fy = [sum(k for (x, y), k in _counts.items() if y == v) for v in _ys]
    if m_prod.value:
        _cells = {(x, y): (kx * ky, 256) for x, kx in zip(_xs, _fx) for y, ky in zip(_ys, _fy)}
        _color, _name = RED, r"$f_X(x)\, f_Y(y)$"
    else:
        _cells = {xy: (k, 16) for xy, k in _counts.items()}
        _color, _name = BLUE, r"$f_{X,Y}(x, y)$"

    _fig = Figure(figsize=(FULL, 4.6), layout="constrained")
    _grid = _fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 3])
    _main = _fig.add_subplot(_grid[1, 0])
    _top = _fig.add_subplot(_grid[0, 0], sharex=_main)
    _side = _fig.add_subplot(_grid[1, 1], sharey=_main)
    _corner = _fig.add_subplot(_grid[0, 1])
    _corner.axis("off")
    _corner.text(0.5, 0.5, _name, color=_color, fontsize=14, ha="center", va="center", transform=_corner.transAxes)

    for (_x, _y), (_k, _N) in _cells.items():
        _main.scatter(_x, _y, s=2400 * _k / _N, color=_color, lw=0, zorder=3)
        _main.annotate(f"{_k}/{_N}", (_x, _y), textcoords="offset points", xytext=(9, 0), va="center", fontsize=10, color=_color)
    _main.set_xlim(0.4, 4.9)
    _main.set_ylim(1.3, 8.7)
    _main.set_xticks(_xs)
    _main.set_yticks(_ys)
    _main.set_xlabel("$x$ (largest face)")
    _main.set_ylabel("$y$ (sum of faces)")

    _top.vlines(_xs, 0, [k / 16 for k in _fx], color=GREY, lw=1.0)
    _top.scatter(_xs, [k / 16 for k in _fx], s=18, color=GREY, zorder=3)
    for _x, _k in zip(_xs, _fx):
        _top.annotate(f"{_k}/16", (_x, _k / 16), textcoords="offset points", xytext=(0, 4), ha="center", va="bottom", fontsize=10, color=GREY)
    _top.set_ylim(0, 1.45 * max(_fx) / 16)
    _top.set_yticks([])
    _top.set_ylabel("$f_X(x)$", fontsize=12)
    _top.tick_params(labelbottom=False)
    _side.hlines(_ys, 0, [k / 16 for k in _fy], color=GREY, lw=1.0)
    _side.scatter([k / 16 for k in _fy], _ys, s=18, color=GREY, zorder=3)
    for _y, _k in zip(_ys, _fy):
        _side.annotate(f"{_k}/16", (_k / 16, _y), textcoords="offset points", xytext=(5, 0), ha="left", va="center", fontsize=10, color=GREY)
    _side.set_xlim(0, 1.9 * max(_fy) / 16)
    _side.set_xticks([])
    _side.set_xlabel("$f_Y(y)$", fontsize=12)
    _side.tick_params(labelleft=False)
    for _ax in (_main, _top, _side):
        _ax.tick_params(labelsize=12)
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    mo.vstack([mo.hstack([m_prod], justify="start", gap=2, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Conditional distributions"""),
            definition(
                r"""
    Given $x \in S_X$, with $f_X(x) > 0$, we define the **conditional pmf/pdf** of $Y$ given $X = x$ as

    $$
    f_{Y|X}(y \mid x) = \frac{f_{X,Y}(x, y)}{f_X(x)} \qquad (y \text{: possible values of } Y, \quad x \text{: given value of } X)
    $$
    """,
                "Conditional pmf and pdf",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; in the discrete case we have a direct interpretation

    $$
    f_{Y|X}(y \mid x) = P(Y = y \mid X = x) = \frac{P(X = x \text{ and } Y = y)}{P(X = x)} = \frac{f_{X,Y}(x, y)}{f_X(x)}
    $$

    $\leadsto$ &nbsp; also in the continuous case the conditional pdf gives probabilities of $Y$ given knowledge of $X = x$

    **Example** (4-sided dice). &nbsp; $X$ = largest face $= 3$, &nbsp; $Y$ = sum of faces $= y$

    | $y$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ | $8$ |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | $f_{Y\vert X}(y \mid 3)$ | $0$ | $0$ | $\dfrac{2/16}{5/16} = \dfrac{2}{5}$ | $\dfrac{2}{5}$ | $\dfrac{1}{5}$ | $0$ | $0$ |

    $$
    \text{e.g.} \qquad f_{Y|X}(4 \mid 3) = \frac{f_{X,Y}(3, 4)}{f_X(3)} = \frac{2/16}{5/16} = \frac{2}{5}
    $$

    $\leadsto$ &nbsp; are the two measurements independent?

    $\leadsto$ &nbsp; knowledge about measurement $X$ **changed the probabilities** of measurement $Y$! &nbsp; $\leadsto$ &nbsp; we shouldn't call them independent
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    c_x = mo.ui.slider(1, 4, 1, value=3, label="given value $x$ of $X$ (largest face)", show_value=True)
    return (c_x,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, Fraction, RED, c_x, dice_counts, mo, over, table, tex):
    _x = c_x.value
    _counts = dice_counts(4)
    _ys = list(range(2, 9))
    _kx = sum(k for (x, y), k in _counts.items() if x == _x)
    _ky = [sum(k for (x, y), k in _counts.items() if y == v) for v in _ys]
    _cond = [Fraction(_counts.get((_x, v), 0), _kx) for v in _ys]

    _fig = Figure(figsize=(FULL, 2.6), layout="constrained")
    _ax = _fig.subplots()
    for _vals, _color, _shift in (([k / 16 for k in _ky], RED, 0.1), ([float(p) for p in _cond], BLUE, -0.1)):
        _at = [v + _shift for v in _ys]
        _ax.vlines(_at, 0, _vals, color=_color, lw=1.2)
        _ax.plot(_at, _vals, "o", color=_color, ms=4.5, zorder=4)
    _ax.text(8.6, 1.0, rf"$f_{{Y|X}}(y \mid {_x})$", color=BLUE, fontsize=12, ha="right", va="top")
    _ax.text(8.6, 0.82, r"$f_Y(y)$", color=RED, fontsize=12, ha="right", va="top")
    _ax.set_xlim(1.4, 8.6)
    _ax.set_ylim(0, 1.05)
    _ax.set_xticks(_ys)
    _ax.set_yticks([0, 0.5, 1])
    _ax.set_xlabel("$y$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _rows = "\n".join(
        [
            "| $y$ | " + " | ".join(f"${v}$" for v in _ys) + " |",
            "|:--|" + ":-:|" * len(_ys),
            rf"| $f_{{Y\vert X}}(y \mid {_x})$ | " + " | ".join(rf"$\textcolor{{{BLUE}}}{{{tex(p)}}}$" for p in _cond) + " |",
            r"| $f_Y(y)$ | " + " | ".join(rf"$\textcolor{{{RED}}}{{{over(k, 16)}}}$" for k in _ky) + " |",
        ]
    )
    mo.vstack(
        [
            mo.hstack([c_x], justify="start", gap=2, wrap=True),
            table([(rf"$f_X({_x}) = P(X = {_x})$", rf"${over(_kx, 16)}$")]),
            mo.md(_rows),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Independence"""),
            definition(
                r"""
    $X$ and $Y$ are **independent** if, for all $(x, y)$,

    $$
    \begin{aligned}
    & f_{Y|X}(y \mid x) = f_Y(y) && \text{knowledge about } X \text{ does not affect our beliefs about } Y \\[6pt]
    \Longleftrightarrow \quad & f_{X,Y}(x, y) = f_X(x)\, f_Y(y) \\[6pt]
    \Longleftrightarrow \quad & f_{X|Y}(x \mid y) = f_X(x) && \text{knowledge about } Y \text{ does not affect our beliefs about } X
    \end{aligned}
    $$
    """,
                "Independent random variables",
            ),
            mo.md(
                r"""
    **Remark.** If $X, Y$ are independent

    $$
    P(X \in A \text{ and } Y \in B) = P(X \in A) \cdot P(Y \in B) \qquad \text{for any } A \subseteq \mathbb{R} \text{ and } B \subseteq \mathbb{R}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, GREY, HALF, LIGHT, mo, np):
    _fig = Figure(figsize=(HALF, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _t = np.array([0.0, 3.0])
    _ax.fill_between(_t, _t, 3, color=LIGHT, lw=0)
    _ax.plot(_t, _t, color=GREY, lw=1.0)
    _ax.text(0.95, 2.1, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    _ax.text(2.2, 1.75, "$y = x$", color=GREY, fontsize=12, ha="left", va="center")
    _ax.set_xlim(0, 3)
    _ax.set_ylim(0, 3)
    _ax.set_aspect("equal")
    _ax.set_xticks([])
    _ax.set_yticks([])
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$y$", rotation=0, labelpad=10)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** Customers arrive following a Poisson model $\mathrm{Pois}(\lambda)$

    $X$ = arrival time of 1st customer, &nbsp; $Y$ = arrival time of 2nd customer

    $$
    \Longrightarrow \qquad f_{X,Y}(x, y) = \begin{cases} \lambda^2 e^{-\lambda y}, & 0 < x < y \\[4pt] 0, & \text{otherwise} \end{cases}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; $f_X(x) = \mathrm{Gamma}(1, \lambda)(x) = \lambda e^{-\lambda x}$

    $Y - x$ = arrival time of 2nd customer counted from $x$

    $$
    \Longrightarrow \qquad f_{Y|X}(y \mid x) = \mathrm{Gamma}(1, \lambda)(y - x) = \lambda e^{-\lambda (y - x)}
    $$

    $$
    \Longrightarrow \qquad f_{X,Y}(x, y) = f_{Y|X}(y \mid x)\, f_X(x) = \lambda^2 e^{-\lambda y} \qquad \text{for } 0 < x < y
    $$

    $\leadsto$ &nbsp; marginals

    $$
    \begin{aligned}
    f_X(x) &= \int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dy = \int_{x}^{\infty} \lambda^2 e^{-\lambda y}\, dy = \lambda e^{-\lambda x} = \mathrm{Gamma}(1, \lambda)(x) = \mathrm{Exp}(\lambda)(x) \\[6pt]
    f_Y(y) &= \int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dx = \int_{0}^{y} \lambda^2 e^{-\lambda y}\, dx = \lambda^2 y\, e^{-\lambda y} = \mathrm{Gamma}(2, \lambda)(y)
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_lam = mo.ui.slider(0.5, 3, 0.1, value=1, label=r"$\lambda$", show_value=True)
    a_a = mo.ui.slider(0, 5, 0.1, value=1, label="$a$", show_value=True)
    a_b = mo.ui.slider(0, 5, 0.1, value=2, label="$b$", show_value=True)
    return a_a, a_b, a_lam


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, a_a, a_b, a_lam, density, math, mo, np, table):
    _lam, _a, _b = a_lam.value, a_a.value, a_b.value
    _L = 5.0
    _g = np.linspace(0, _L, 301)
    _X, _Y = np.meshgrid(_g, _g)
    _f = np.where(_X < _Y, _lam**2 * np.exp(-_lam * _Y), np.nan)

    _fig = Figure(figsize=(FULL, 4.6), layout="constrained")
    _grid = _fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 3])
    _main = _fig.add_subplot(_grid[1, 0])
    _top = _fig.add_subplot(_grid[0, 0], sharex=_main)
    _side = _fig.add_subplot(_grid[1, 1], sharey=_main)

    # joint pdf on the triangle 0 < x < y, and the event {X <= a, Y <= b}
    density(_main, _f, (0, _L, 0, _L), _lam**2)
    _main.plot([0, _L], [0, _L], color=GREY, lw=1.0)
    _main.plot([0, _a, _a], [_b, _b, 0], color=GREEN, lw=1.4)
    _main.text(0.5, 4.5, "$S_{X,Y}$", fontsize=13, ha="center", va="center")
    _main.set_xlim(0, _L)
    _main.set_ylim(0, _L)
    _main.set_xlabel("$x$")
    _main.set_ylabel("$y$")

    # the marginal pdfs in the margins, with the areas P(X <= a) and P(Y <= b)
    _ga, _gb = np.linspace(0, _a, 200), np.linspace(0, _b, 200)
    _top.fill_between(_ga, _lam * np.exp(-_lam * _ga), color=LIGHT, lw=0)
    _top.plot(_g, _lam * np.exp(-_lam * _g), color=BLUE, lw=1.4)
    _top.axvline(_a, color=GREEN, lw=1.0, ls=(0, (4, 3)))
    _top.set_ylim(0, 1.1 * _lam)
    _top.set_yticks([])
    _top.set_ylabel(r"$f_X(x)$", fontsize=12)
    _top.tick_params(labelbottom=False)
    _side.fill_betweenx(_gb, 0, _lam**2 * _gb * np.exp(-_lam * _gb), color=LIGHT, lw=0)
    _side.plot(_lam**2 * _g * np.exp(-_lam * _g), _g, color=BLUE, lw=1.4)
    _side.axhline(_b, color=GREEN, lw=1.0, ls=(0, (4, 3)))
    _side.set_xlim(0, 1.1 * _lam / math.e)
    _side.set_xticks([])
    _side.set_xlabel(r"$f_Y(y)$", fontsize=12)
    _side.tick_params(labelleft=False)
    for _ax in (_main, _top, _side):
        _ax.tick_params(labelsize=12)
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    _px = 1 - math.exp(-_lam * _a)
    _py = 1 - math.exp(-_lam * _b) - _lam * _b * math.exp(-_lam * _b)
    _m = min(_a, _b)  # beyond a = b the event {X <= a, Y <= b} is {Y <= b}
    _pxy = 1 - math.exp(-_lam * _m) - _lam * _m * math.exp(-_lam * _b)
    mo.vstack(
        [
            mo.hstack([a_lam, a_a, a_b], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$P(X \leq a,\ Y \leq b) = \iint f_{X,Y}(x, y)\, dx\, dy$ &nbsp; (inside the green corner)", rf"$\textcolor{{{GREEN}}}{{{_pxy:.4f}}}$"),
                    (r"$P(X \leq a) = 1 - e^{-\lambda a}$ &nbsp; (area, top)", rf"${_px:.4f}$"),
                    (r"$P(Y \leq b) = 1 - e^{-\lambda b} - \lambda b\, e^{-\lambda b}$ &nbsp; (area, right)", rf"${_py:.4f}$"),
                    (r"$P(X \leq a) \cdot P(Y \leq b)$", rf"${_px * _py:.4f}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** For any (fixed) $x \in S_X$, &nbsp; $f_{Y|X}(\cdot \mid x)$ is a proper pmf/pdf!

    - $f_{Y|X}(y \mid x) \geq 0 \quad \forall\, y \in \mathbb{R}$
    - $\displaystyle\sum_y f_{Y|X}(y \mid x) = \sum_y \frac{f_{X,Y}(x, y)}{f_X(x)} = \frac{1}{f_X(x)} \sum_y f_{X,Y}(x, y) = 1$
    - $\displaystyle\int_{-\infty}^{\infty} f_{Y|X}(y \mid x)\, dy = \int_{-\infty}^{\infty} \frac{f_{X,Y}(x, y)}{f_X(x)}\, dy = \frac{1}{f_X(x)} \int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dy = 1$

    ### Conditional expectation
    """
            ),
            definition(
                r"""
    Given $u : \mathbb{R} \longrightarrow \mathbb{R}$ real valued single variable function, the **conditional expectation** of $u(Y)$, given $X = x$, is

    $$
    E[u(Y) \mid X = x] = \sum_y u(y)\, f_{Y|X}(y \mid x) \qquad \text{or} \qquad \int_{-\infty}^{\infty} u(y)\, f_{Y|X}(y \mid x)\, dy
    $$
    """,
                "Conditional expectation",
            ),
            mo.md(
                r"""
    - $u(Y) = Y$ &nbsp; $\leadsto$ &nbsp; $\underbrace{E[Y \mid X = x]}_{=\, g(x)}$ &nbsp; **conditional mean** of $Y$ given $X = x$

        = expected value of $Y$ given the observed value of $X = x$

        $\leadsto$ &nbsp; **regression function** of $Y$ on $X$

        ($g(X)$ will later become our best guess for the values of $Y$ given the values of $X$!)

    **Example** (Customer arrivals).

    $$
    f_{X,Y}(x, y) = \lambda^2 e^{-\lambda y}, \quad 0 < x < y \qquad \leadsto \qquad f_{Y|X}(y \mid x) = \lambda e^{-\lambda (y - x)}, \quad y > x
    $$

    $$
    \Longrightarrow \qquad E[Y \mid X = x] = \int_{-\infty}^{+\infty} y\, f_{Y|X}(y \mid x)\, dy = \int_{x}^{+\infty} y\, \lambda e^{-\lambda (y - x)}\, dy = x + \frac{1}{\lambda}
    $$

    $\leadsto$ &nbsp; the regression function of $Y$ on $X$ is linear

    If $\lambda = 2$ customers per hour and the 1st customer arrived at $x = 1$ hour, we expect the 2nd customer to arrive at hour $y = 1.5$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    r_lam = mo.ui.slider(0.5, 4, 0.1, value=2, label=r"$\lambda$ (customers per hour)", show_value=True)
    r_x = mo.ui.slider(0, 3, 0.05, value=1, label="$x$ (1st arrival, hours)", show_value=True)
    return r_lam, r_x


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, RED, density, mo, np, r_lam, r_x, table):
    _lam, _x = r_lam.value, r_x.value
    _m = _x + 1 / _lam
    _L = 5.0
    _g = np.linspace(0, _L, 301)
    _X, _Y = np.meshgrid(_g, _g)
    _f = np.where(_X < _Y, _lam**2 * np.exp(-_lam * _Y), np.nan)

    _fig = Figure(figsize=(FULL, 3.2), layout="constrained")
    _left, _right = _fig.subplots(1, 2)

    # left: the regression line y = x + 1/lambda through the joint pdf, and the slice X = x
    density(_left, _f, (0, _L, 0, _L), _lam**2)
    _left.plot([0, _L], [0, _L], color=GREY, lw=1.0)
    _left.plot([_x, _x], [_x, _L], color=BLUE, lw=1.2, ls=(0, (4, 3)))
    _left.plot(_g, _g + 1 / _lam, color=GREEN, lw=1.4)
    _left.plot(_x, _m, "o", color=GREEN, ms=5, zorder=4)
    _left.text(0.15, _L - 0.2, r"$y = x + 1/\lambda$", color=GREEN, fontsize=12, ha="left", va="top", bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})
    _left.set_xlim(0, _L)
    _left.set_ylim(0, _L)
    _left.set_xlabel("$x$")
    _left.set_ylabel("$y$")

    # right: the conditional pdf of Y given X = x, against the marginal pdf of Y
    _yy = np.linspace(_x, _L, 300)
    _right.fill_between(_yy, _lam * np.exp(-_lam * (_yy - _x)), color=LIGHT, lw=0)
    _right.plot(np.r_[0, _x, _yy], np.r_[0, 0, _lam * np.exp(-_lam * (_yy - _x))], color=BLUE, lw=1.4)
    _right.plot(_g, _lam**2 * _g * np.exp(-_lam * _g), color=RED, lw=1.2)
    _right.plot([_m, _m], [0, 1.1 * _lam], color=GREEN, lw=1.2, ls=(0, (4, 3)))
    _right.text(_L, 1.15 * _lam, r"$f_{Y|X}(y \mid x)$", color=BLUE, fontsize=12, ha="right", va="top")
    _right.text(_L, 0.95 * _lam, r"$f_Y(y)$", color=RED, fontsize=12, ha="right", va="top")
    _right.set_xlim(0, _L)
    _right.set_ylim(0, 1.2 * _lam)
    _right.set_yticks([])
    _right.set_xlabel("$y$")
    for _ax in (_left, _right):
        _ax.tick_params(labelsize=12)
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([r_lam, r_x], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$E[Y \mid X = x] = x + 1/\lambda$ &nbsp; (green)", rf"$\textcolor{{{GREEN}}}{{{_m:.3f}}}$"),
                    (r"$E[Y] = 2/\lambda$ &nbsp; (mean of $f_Y$, not knowing $x$)", rf"${2 / _lam:.3f}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - joint distribution of a pair $(X, Y)$ on the same $(S, \mathcal{E}, P)$, with joint pmf or pdf $f_{X,Y}$:

        $$
        P_{X,Y}(A) = P((X, Y) \in A) = \sum_{(x, y) \in S_{X,Y} \cap A} f_{X,Y}(x, y) \qquad \text{or} \qquad \iint_{S_{X,Y} \cap A} f_{X,Y}(x, y)\, dx\, dy
        $$
    - marginals: &nbsp; $f_X(x) = \sum_y f_{X,Y}(x, y)$ or $\int f_{X,Y}(x, y)\, dy$, and similarly $f_Y$; the marginals do not determine the joint
    - conditional pmf/pdf, a proper pmf/pdf in $y$ for each fixed $x$:

        $$
        f_{Y|X}(y \mid x) = \frac{f_{X,Y}(x, y)}{f_X(x)}
        $$
    - $X$ and $Y$ independent:

        $$
        f_{Y|X}(y \mid x) = f_Y(y) \quad \Longleftrightarrow \quad f_{X,Y}(x, y) = f_X(x)\, f_Y(y) \quad \Longleftrightarrow \quad f_{X|Y}(x \mid y) = f_X(x)
        $$

        and then $P(X \in A \text{ and } Y \in B) = P(X \in A)\, P(Y \in B)$
    - conditional expectation:

        $$
        E[u(Y) \mid X = x] = \sum_y u(y)\, f_{Y|X}(y \mid x) \qquad \text{or} \qquad \int_{-\infty}^{\infty} u(y)\, f_{Y|X}(y \mid x)\, dy
        $$

        the conditional mean $E[Y \mid X = x]$ is the regression function of $Y$ on $X$
    - customer arrivals: &nbsp; marginals $\mathrm{Exp}(\lambda)$ and $\mathrm{Gamma}(2, \lambda)$, and a linear regression function

        $$
        f_{X,Y}(x, y) = \lambda^2 e^{-\lambda y} \quad (0 < x < y), \qquad E[Y \mid X = x] = x + \frac{1}{\lambda}
        $$
    """)
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 05 · Discrete random variables: pmf, cdf, expectation", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np


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
    header("Lecture 05", "Week 03", "Lecture 05 • Discrete random variables: pmf, cdf, expectation")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - random variables on probability spaces = measurements on random experiments
    - $(S, \mathcal{E}, P)$ probability space, random variable = function on the sample space $S$: &nbsp; $X : S \longrightarrow \mathbb{R}$
    - $\leadsto$ &nbsp; $S_X$ = state space $= \mathrm{Im}\, X \subseteq \mathbb{R}$
    - $\leadsto$ &nbsp; $\mathcal{E}_X$ = algebra of subsets of $\mathbb{R}$
    - $\leadsto$ &nbsp; $P_X$ = probability distribution $P_X : \mathcal{E}_X \longrightarrow \mathbb{R}$, &nbsp; $P_X(A) = P(X \in A)$ &nbsp; (probability that the measurement of $X$ is valued in $A$)

    **In this lecture:** discrete random variables: pmf, cdf and expectation

    **References:** WMS 3.1–3.3
    """)
    return


@app.cell(hide_code=True)
def _(BLUE):
    def stems(ax, xs, pmf, color=BLUE):
        """A pmf: a thin stem with a dot over every point of the state space."""
        ax.vlines(xs, 0, pmf, color=color, lw=1.0)
        ax.plot(xs, pmf, "o", color=color, ms=4.5, zorder=3)
        ax.set_xticks(xs)
        ax.set_xlim(xs[0] - 0.6, xs[-1] + 0.6)
        ax.set_ylim(0, max(pmf) * 1.25)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    def steps(ax, xs, levels, color=BLUE):
        """A step cdf: `levels[k]` is the value on the k-th interval cut out by the points `xs`;
        every step is closed on the left and open on the right."""
        edges = [xs[0] - 1] + list(xs) + [xs[-1] + 1]
        for k, lev in enumerate(levels):
            ax.plot([edges[k], edges[k + 1]], [lev, lev], color=color, lw=1.4)
            if k > 0:
                ax.plot(edges[k], lev, "o", color=color, ms=4.5, zorder=3)
            if k < len(levels) - 1:
                ax.plot(edges[k + 1], lev, "o", color=color, ms=4.5, mfc="white", zorder=3)
        ax.set_xlim(edges[0], edges[-1])
        ax.set_ylim(-0.05, 1.15)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    return stems, steps


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, HALF, arrow, definition, mo, stems, steps):
    # Generic step cdf: the jump at x equals f_X(x)
    _sketch = Figure(figsize=(HALF, 2.4), layout="constrained")
    _ax = _sketch.subplots()
    steps(_ax, [1, 2, 3, 4], [0.0, 0.15, 0.35, 0.75, 1.0])
    arrow(_ax, (3, 0.55), (3, 0.705), GREEN)
    arrow(_ax, (3, 0.55), (3, 0.395), GREEN)
    _ax.text(3.15, 0.55, "$f_X(x)$", color=GREEN, fontsize=12, va="center")
    _ax.text(4.5, 1.06, "$y = F_X(x)$", color=BLUE, fontsize=12, ha="center", va="bottom")
    _ax.set_xticks([2, 3], [r"$x^{\!\!-}$", "$x$"])
    _ax.set_yticks([0, 1])
    _ax.set_ylim(-0.05, 1.3)

    _fig = Figure(figsize=(FULL, 2.9), layout="constrained")
    _l, _r = _fig.subplots(1, 2)
    stems(_l, [1, 2, 3, 4], [1 / 16, 3 / 16, 5 / 16, 7 / 16])
    _l.set_yticks([1 / 16, 3 / 16, 5 / 16, 7 / 16], [r"$1/16$", r"$3/16$", r"$5/16$", r"$7/16$"])
    _l.set_xlabel("$x$")
    _l.set_ylabel("$f_X(x)$")
    steps(_r, [1, 2, 3, 4], [0, 1 / 16, 4 / 16, 9 / 16, 1])
    _r.set_xticks([1, 2, 3, 4])
    _r.set_yticks([1 / 16, 1 / 4, 9 / 16, 1], [r"$1/16$", r"$1/4$", r"$9/16$", "$1$"])
    _r.set_xlabel("$x$")
    _r.set_ylabel("$F_X(x)$")

    mo.vstack(
        [
            mo.md(
                r"""
    ## II.2 &nbsp; Discrete random variables: pmf, cdf, expectation

    ### pmf and cdf
    """
            ),
            definition(
                r"""
    A random variable $X : S \longrightarrow \mathbb{R}$ is **discrete** if $S_X = \mathrm{Im}\, X$ is a countable set.
    """,
                "Discrete random variable",
            ),
            definition(
                r"""
    The **pmf** (probability mass function) of a discrete random variable $X : S \longrightarrow \mathbb{R}$ is the function $f_X : \mathbb{R} \longrightarrow \mathbb{R}$ given by

    $$
    f_X(x) = P_X(\{x\}) = P(X = x)
    $$

    (probability that the measurement of $X$ is exactly equal to $x$)
    """,
                "Probability mass function",
            ),
            mo.md(
                r"""
    **Remark.** WMS denotes $f_X(x) = p(x)$!

    $\leadsto$ &nbsp; $f_X$ must satisfy:

    - $f_X(x) \geq 0$
    - $f_X(x) = 0$ for $x \notin S_X$
    - $\displaystyle\sum_{x \in A} f_X(x) = P_X(A)$ for $A \subseteq \mathbb{R}$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $f_X$</span> completely determines $P_X$
    """
            ),
            definition(
                r"""
    The **cdf** (cumulative distribution function) of a random variable $X : S \longrightarrow \mathbb{R}$ is the function $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ given by

    $$
    F_X(x) = P(X \leq x)
    $$

    (probability that the measurement of $X$ is valued at most $x$)
    """,
                "Cumulative distribution function",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $F_X$ must satisfy

    - $F_X(x) \geq 0$
    - $F_X(x_1) \leq F_X(x_2)$ for $x_1 \leq x_2 \in \mathbb{R}$
    - $\displaystyle\lim_{x \to -\infty} F_X(x) = 0$, &nbsp; $\displaystyle\lim_{x \to +\infty} F_X(x) = 1$
    - $F_X(x) - F_X(x^-) = f_X(x)$ &nbsp; ($x^-$ = 1st element of $S_X$ smaller than $x$; $F_X(x^-) = P(X < x)$) &nbsp; <span class="nw">$\leadsto$ &nbsp; $F_X(x) = \displaystyle\sum_{t \leq x} f_X(t)$</span>
    """
            ),
            _sketch,
            mo.md(
                r"""
    **Example** (roll two fair 4-sided dice).

    <span class="chain">$\displaystyle S = \{\, (i, j) \mid i, j = 1, 2, 3, 4 \,\},$ $\displaystyle \quad X(i, j) = \max(i, j)$ $\displaystyle \qquad \leadsto \qquad S_X = \{1, 2, 3, 4\}$</span>
    """
            ),
            mo.Html('<div class="readout cases">' + mo.md(r"""
    | | |
    |:--|:--|
    | $f_X(1) = P(X = 1) = 1/16$ | $X = 1 \iff (i, j) = (1, 1)$ |
    | $f_X(2) = P(X = 2) = 3/16$ | $X = 2 \iff (i, j) = (1, 2),$ $(2, 2),$ $(2, 1)$ |
    | $f_X(3) = P(X = 3) = 5/16$ | $X = 3 \iff (i, j) = (1, 3),$ $(2, 3),$ $(3, 3),$ $(3, 2),$ $(3, 1)$ |
    | $f_X(4) = P(X = 4) = 7/16$ | $X = 4 \iff (i, j) = (1, 4),$ $(2, 4),$ $(3, 4),$ $(4, 4),$ $(4, 3),$ $(4, 2),$ $(4, 1)$ |
    | $f_X(5) = f_X(3/2) = f_X(-\pi) = 0$ | $X$ never takes those values |
    """).text + "</div>"),
            mo.Html('<div class="readout cases">' + mo.md(r"""
    | | |
    |:--|:--|
    | $F_X(1) = P(X \leq 1) = 1/16$ | $X \leq 1 \iff (i, j) = (1, 1)$ |
    | $F_X(2) = P(X \leq 2) = 4/16$ | $X \leq 2 \iff (i, j) = (1, 1),$ $(1, 2),$ $(2, 2),$ $(2, 1)$ |
    | $F_X(3) = P(X \leq 3) = 9/16$ | $X \leq 3 \iff (i, j) = (1, 1), \dots, (3, 1)$ |
    | $F_X(4) = P(X \leq 4) = 16/16$ | $X \leq 4 \iff (i, j) = \underbrace{(1, 1), \dots, (4, 1)}_{\footnotesize\text{all outcomes!}}$ |
    | $F_X(5) = 1$ | $X \leq 5$ for every outcome |
    | $F_X(3/2) = 1/16$ | $X \leq 3/2$ for $(1, 1)$ only |
    | $F_X(-\pi) = 0$ | $X \leq -\pi$ for no outcome |
    """).text + "</div>"),
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
    ### Expectation

    $\leadsto$ &nbsp; pmf of a discrete random variable $X : S \longrightarrow \mathbb{R}$ gives the relative frequency of a result $x$ over infinitely many independent measurements

    $\leadsto$ &nbsp; to study their properties, it is useful to summarize the main characteristics of pmfs into certain numbers (mean, variance, …) &nbsp; <span class="nw">$\leadsto$ &nbsp; expectations</span> of $X$
    """
            ),
            definition(
                r"""
    Let $X$ be a discrete random variable with pmf $f_X$. Given any function $u : \mathbb{R} \longrightarrow \mathbb{R}$, we define the **expectation** of $u(X) = u \circ X : S \longrightarrow \mathbb{R}$ &nbsp; (function of $X$, or composition of $u$ and $X$)

    $$
    E[u(X)] = \sum_{x} u(x)\, f_X(x)
    $$
    """,
                "Expectation",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $X(i, j) = \max(i, j)$

    <span class="chain">$\displaystyle \leadsto \qquad E[X] = \sum_{x=1}^{4} x\, f_X(x) = 1 \cdot \frac{1}{16} + 2 \cdot \frac{3}{16} + 3 \cdot \frac{5}{16} + 4 \cdot \frac{7}{16}$ $\displaystyle = \frac{50}{16} \approx 3.1$</span>

    **Example.** Game: pay 3000 won to roll a 6-sided die, get 1000 won times the face value $X$. How much do you expect to win?

    $$
    \text{fair die} \quad \leadsto \quad E[1000 X - 3000] = \sum_{x=1}^{6} (1000 x - 3000) \times \frac{1}{6} = 500
    $$

    not fair &nbsp; (say $f_X(1) = f_X(2) = f_X(3) = \dfrac{1}{3}$, &nbsp; $f_X(4) = f_X(5) = f_X(6) = 0$)

    <span class="chain">$\displaystyle \leadsto \qquad E[1000 X - 3000] = \sum_{x=1}^{3} (1000 x - 3000) \times \frac{1}{3}$ $\displaystyle {} + \sum_{x=4}^{6} (1000 x - 3000) \times 0 = -1000$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(FULL, Figure, mo, stems):
    _fig = Figure(figsize=(FULL, 2.8), layout="constrained")
    _l, _r = _fig.subplots(1, 2)
    stems(_l, [0, 1, 2, 3, 4], [1 / 16, 4 / 16, 6 / 16, 4 / 16, 1 / 16])
    _l.set_yticks([1 / 16, 4 / 16, 6 / 16], [r"$1/16$", r"$4/16$", r"$6/16$"])
    _l.text(0.98, 0.98, "fair coin", transform=_l.transAxes, fontsize=13, ha="right", va="top")
    stems(_r, [0, 1, 2, 3, 4], [16 / 81, 32 / 81, 24 / 81, 8 / 81, 1 / 81])
    _r.set_yticks([1 / 81, 8 / 81, 16 / 81, 24 / 81, 32 / 81], [r"$1/81$", r"$8/81$", r"$16/81$", r"$24/81$", r"$32/81$"])
    _r.text(0.98, 0.98, "biased coin", transform=_r.transAxes, fontsize=13, ha="right", va="top")
    for _a in (_l, _r):
        _a.set_xlabel("$x$")
        _a.set_ylabel("$f_X(x)$")

    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; **mean** = expectation of $X$ &nbsp; (measures the “center” of the distribution)

    $$
    \mu_X = E[X] = \sum_{x} x\, f_X(x)
    $$

    $\leadsto$ &nbsp; **variance** = expectation of $(X - \mu_X)^2$ &nbsp; (measures the “width” of the distribution)

    $$
    \underbrace{\sigma_X^2}_{\mathclap{\footnotesize (\text{standard deviation})^2}} = E[(X - \mu_X)^2] = \sum_{x} (x - \mu_X)^2\, f_X(x)
    $$

    $\leadsto$ &nbsp; **skewness** = expectation of $\left( \dfrac{X - \mu_X}{\sigma_X} \right)^3$ &nbsp; (measures “symmetry” around the center)

    $$
    \gamma_X = E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = \sum_{x} \left( \frac{x - \mu_X}{\sigma_X} \right)^{\!3} f_X(x)
    $$

    **Example.** Toss a coin 4 times, $X$ = number of heads
    """
            ),
            _fig,
            mo.Html('<div class="readout cases">' + mo.md(r"""
    | | | |
    |:--|:--|:--|
    | | fair coin | biased coin |
    | | $P(\{H\}) = P(\{T\}) = 1/2$ | $P(\{H\}) = 1/3,$ $P(\{T\}) = 2/3$ |
    | $\mu_X$ | $E[X] = 2$ | $E[X] = 4/3$ |
    | $\sigma_X^2$ | $E[(X - 2)^2] = 1$ | $E[(X - 4/3)^2] = 8/9$ |
    | $\gamma_X$ | $E\!\left[ \left( \dfrac{X - 2}{1} \right)^3 \right] = 0$ | $E\!\left[ \left( \dfrac{X - 4/3}{\sqrt{8/9}} \right)^3 \right] = \dfrac{1}{\sqrt{8}}$ |
    """).text + "</div>"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    coin_p = mo.ui.slider(0.05, 0.95, 0.05, value=0.5, label=r"$P(\{H\})$", show_value=True)
    return (coin_p,)


@app.cell(hide_code=True)
def _(Figure, GREEN, GREY, coin_p, math, mo, stems):
    _p, _n = coin_p.value, 4
    _xs = list(range(_n + 1))
    _f = [math.comb(_n, _k) * _p**_k * (1 - _p) ** (_n - _k) for _k in _xs]
    _mu = _n * _p
    _var = _n * _p * (1 - _p)
    _sd = math.sqrt(_var)
    _g = (1 - 2 * _p) / _sd
    _fig = Figure(figsize=(5.6, 3.4), layout="constrained")
    _ax = _fig.subplots()
    stems(_ax, _xs, _f)
    _ax.set_ylim(-0.2, 0.85)
    _ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8], ["0", "0.2", "0.4", "0.6", "0.8"])
    _ax.spines["bottom"].set_visible(False)
    _ax.spines["left"].set_bounds(0, 0.8)
    _ax.tick_params(axis="x", length=0)
    _ax.axhline(0, color="black", lw=0.8)
    _y = -0.08
    _ax.plot([_mu - _sd, _mu + _sd], [_y, _y], color=GREY, lw=1.4)
    for _e in (_mu - _sd, _mu + _sd):
        _ax.plot([_e, _e], [_y - 0.015, _y + 0.015], color=GREY, lw=1.4)
    _ax.plot(_mu, _y, "o", color=GREEN, ms=6, zorder=3)
    _ax.text(_mu, _y - 0.02, r"$\mu_X$", color=GREEN, ha="center", va="top", fontsize=13)
    for _c in (_mu - _sd / 2, _mu + _sd / 2):
        _ax.text(_c, _y - 0.02, r"$\sigma_X$", color=GREY, ha="center", va="top", fontsize=13)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    _ax.set_title(rf"$\mu_X = {_mu:.2g}, \quad \sigma_X^2 = {_var:.2g}, \quad \gamma_X = {_g:.2f}$", fontsize=14)
    mo.vstack([coin_p, _fig])
    return


@app.cell(hide_code=True)
def _(corollary, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Let $X$ be a discrete random variable, $u, v : \mathbb{R} \longrightarrow \mathbb{R}$ functions and $a, b, c \in \mathbb{R}$ constants

    $$
    E[a\, u(X) + b\, v(X)] = a\, E[u(X)] + b\, E[v(X)], \qquad E[c] = c
    $$
    """,
                "Linearity of expectation",
            ),
            corollary(
                r"""
    $$
    \sigma_X^2 = E[X^2] - E[X]^2
    $$
    """,
                "Variance formula",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{align*}
    E[(X - \mu_X)^2] &= E[X^2 - 2 \mu_X X + \mu_X^2] = E[X^2] - 2 \mu_X E[X] + \mu_X^2 \\[6pt]
    &= E[X^2] - E[X]^2 \tag*{$\square$}
    \end{align*}
    $$

    **Example.** Flip a fair coin 4 times, $X$ = number of heads

    <span class="chain">$\displaystyle \leadsto \qquad E[X] = 0 \times \frac{1}{16} + 1 \times \frac{4}{16} + 2 \times \frac{6}{16} + 3 \times \frac{4}{16} + 4 \times \frac{1}{16}$ $\displaystyle = \frac{32}{16} = 2$</span>

    <span class="chain">$\displaystyle \leadsto \qquad E[X^2] = 0^2 \times \frac{1}{16} + 1^2 \times \frac{4}{16} + 2^2 \times \frac{6}{16} + 3^2 \times \frac{4}{16} + 4^2 \times \frac{1}{16}$ $\displaystyle = \frac{80}{16} = 5$</span>

    $$
    \Longrightarrow \qquad \sigma_X^2 = E[X^2] - E[X]^2 = 5 - 2^2 = 1
    $$
    """
            ),
        ]
    )
    return

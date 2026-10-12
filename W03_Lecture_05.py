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
    RED, GREEN, BLUE, GREY = "#b3261e", "#2e7d32", "#1b458f", "#888888"

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS202 &bull; {running}</div>
      <div class="bs-title">Introduction to Probability and Mathematical Statistics</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>BS202a</span>
        <b>Date</b><span>{date}</span><b>Instructor</b><span>Professor Scarinci</span>
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

    def warning(body):
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 2.2, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=18)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color="#cfe3f5", lw=0.6)
        ax.set_axisbelow(True)

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, GREEN, GREY, RED, arrow, check, definition, header, plane, theorem, warning


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED):
    _PIPS = {
        1: [(2, 2)],
        2: [(1, 1), (3, 3)],
        3: [(1, 1), (2, 2), (3, 3)],
        4: [(1, 1), (1, 3), (3, 1), (3, 3)],
        5: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)],
        6: [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3)],
    }

    def die(n, color=BLUE):
        """A small picture of a die face, for use inside text."""
        dots = "".join(f'<circle cx="{6 * x}" cy="{6 * y}" r="2" fill="{color}"/>' for x, y in _PIPS[n])
        return (
            '<svg viewBox="0 0 24 24" style="display:inline-block;width:1.25em;height:1.25em;vertical-align:-0.25em">'
            f'<rect x="1.5" y="1.5" width="21" height="21" rx="4" fill="none" stroke="{color}" stroke-width="1.6"/>{dots}</svg>'
        )

    def dice(faces, color=BLUE):
        return ", ".join(die(n, color) for n in faces)

    return dice, die


@app.cell(hide_code=True)
def _(arrow):
    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    return (cross_axes,)


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
def _(header):
    header("Lecture 05", "Week 03", "Lecture 05 · Discrete random variables: pmf, cdf, expectation")
    return


@app.cell(hide_code=True)
def _(GREEN, RED):
    def pmf_cdf(fig, xs, pmf, color=RED):
        """Draw a pmf (left) and its cdf (right) on a figure."""
        left, right = fig.subplots(1, 2)
        left.vlines(xs, 0, pmf, color=color, lw=1, alpha=0.4)
        left.plot(xs, pmf, "o", color=color, ms=5)
        left.set_title("pmf  $f_X(x)$", fontsize=13)
        left.set_xticks(xs)
        left.set_ylim(0, max(pmf) * 1.25)
        edges = [xs[0] - 1] + list(xs) + [xs[-1] + 1]
        levels = [0.0]
        for p in pmf:
            levels.append(levels[-1] + p)
        for k, lev in enumerate(levels):
            right.plot([edges[k], edges[k + 1]], [lev, lev], color=color, lw=1.8)
            if k > 0:
                right.plot(edges[k], lev, "o", color=color, ms=5)
                right.plot(edges[k], levels[k - 1], "o", color=color, ms=5, mfc="white")
                right.plot([edges[k], edges[k]], [levels[k - 1], lev], ":", color=GREEN, lw=1)
        right.set_title("cdf  $F_X(x)$", fontsize=13)
        right.set_xticks(xs)
        right.set_ylim(-0.05, 1.1)
        for a in (left, right):
            for s in ("top", "right"):
                a.spines[s].set_visible(False)
        return left, right

    return (pmf_cdf,)


@app.cell(hide_code=True)
def _(Figure, GREEN, RED, definition, mo, pmf_cdf):
    _fig = Figure(figsize=(8.6, 3.2), layout="constrained")
    _l, _r = pmf_cdf(_fig, [1, 2, 3, 4], [1 / 16, 3 / 16, 5 / 16, 7 / 16], GREEN)
    _l.set_yticks([1 / 16, 3 / 16, 5 / 16, 7 / 16], [r"$\frac{1}{16}$", r"$\frac{3}{16}$", r"$\frac{5}{16}$", r"$\frac{7}{16}$"])
    _r.set_yticks([1 / 16, 1 / 4, 9 / 16, 1], [r"$\frac{1}{16}$", r"$\frac{1}{4}$", r"$\frac{9}{16}$", "$1$"])

    # Generic step cdf: the jump at x equals f_X(x)
    _sketch = Figure(figsize=(4.6, 2.6), layout="constrained")
    _ax = _sketch.subplots()
    _pts, _lev = [1, 2, 3, 4], [0.0, 0.15, 0.35, 0.75, 1.0]
    _edges = [0] + _pts + [5.2]
    for _k in range(len(_lev)):
        _ax.plot([_edges[_k], _edges[_k + 1]], [_lev[_k], _lev[_k]], color=RED, lw=1.8)
        if _k > 0:
            _ax.plot(_edges[_k], _lev[_k], "o", color=RED, ms=5)
            _ax.plot(_edges[_k], _lev[_k - 1], "o", color=RED, ms=5, mfc="white")
    _ax.annotate("", xy=(3, 0.75), xytext=(3, 0.35), arrowprops={"arrowstyle": "<->", "color": GREEN, "lw": 1.2})
    _ax.text(3.12, 0.55, "$f_X(x)$", color=GREEN, fontsize=12, va="center")
    _ax.text(4.3, 1.04, "$y = F_X(x)$", color=RED, fontsize=11)
    _ax.text(2.88, 0.80, "$F_X(x)$", color=RED, fontsize=10, ha="right")
    _ax.text(2.88, 0.30, "$F_X(x^-)$", color=RED, fontsize=10, ha="right", va="top")
    _ax.set_xticks([3], ["$x$"])
    _ax.set_yticks([0, 1])
    _ax.set_xlim(0, 5.3)
    _ax.set_ylim(-0.05, 1.15)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$y$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Random Variables on probability spaces = measurements on random experiments (WMS 3.1, 3.2)

    $(S, \mathcal{E}, P)$ probability space

    random variable = function on the sample space $S$

    $$
    X : S \longrightarrow \mathbb{R}
    $$

    - $S_X$ = state space $= \mathrm{Im}\, X \subseteq \mathbb{R}$
    - $\mathcal{E}_X$ = algebra of subsets of $\mathbb{R}$
    - $P_X$ = probability distribution

    $$
    P_X : \mathcal{E}_X \longrightarrow \mathbb{R}, \qquad P_X(A) = P(X \in A) \qquad (\text{probability that the measurement of } X \text{ is valued in } A)
    $$
    """
            ),
            definition(
                r"""
    A RV $X : S \longrightarrow \mathbb{R}$ is **discrete** if $S_X = \mathrm{Im}\, X$ is a countable set.
    """
            ),
            definition(
                r"""
    The **pmf** (probability mass function) of a discrete RV $X : S \longrightarrow \mathbb{R}$ is the function $f_X : \mathbb{R} \longrightarrow \mathbb{R}$ given by

    $$
    f_X(x) = P_X(\{x\}) = P(X = x) \qquad (\text{probability that the measurement of } X \text{ is exactly equal to } x)
    $$
    """
            ),
            mo.md(
                r"""
    **Remark.** WMS denotes $f_X(x) = p(x)$!

    $f_X$ must satisfy:

    - $f_X(x) \geq 0$
    - $f_X(x) = 0$ for $x \notin S_X$
    - $\displaystyle\sum_{x \in A} f_X(x) = P_X(A)$ for $A \subseteq \mathbb{R}$ &nbsp; $\leadsto$ &nbsp; $f_X$ completely determines $P_X$
    """
            ),
            definition(
                r"""
    The **cdf** (cumulative distribution function) of a RV $X : S \longrightarrow \mathbb{R}$ is the function $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ given by

    $$
    F_X(x) = P(X \leq x) \qquad (\text{probability that the measurement of } X \text{ is valued at most } x)
    $$
    """
            ),
            mo.md(
                r"""
    $F_X$ must satisfy

    - $F_X(x) \geq 0$
    - $F_X(x_1) \leq F_X(x_2)$ for $x_1 \leq x_2 \in \mathbb{R}$
    - $\displaystyle\lim_{x \to -\infty} F_X(x) = 0$, &nbsp; $\displaystyle\lim_{x \to +\infty} F_X(x) = 1$
    - $F_X(x) - F_X(x^-) = f_X(x)$ &nbsp; ($F_X(x^-) = P(X < x)$: value of $F_X$ just before $x$) &nbsp; $\leadsto$ &nbsp; $F_X(x) = \displaystyle\sum_{t \leq x} f_X(t)$
    """
            ),
            _sketch,
            mo.md(
                r"""
    **Example** (roll two fair 4-sided dice).

    $$
    S = \{\, (i, j) \mid i, j = 1, 2, 3, 4 \,\}, \qquad X(i, j) = \max(i, j) \quad \leadsto \quad S_X = \{1, 2, 3, 4\}
    $$

    $$
    \begin{aligned}
    f_X(1) &= P(X = 1) = \tfrac{1}{16} && X = 1 \iff (i, j) = (1, 1) \\
    f_X(2) &= P(X = 2) = \tfrac{3}{16} && X = 2 \iff (i, j) = (1, 2), (2, 2), (2, 1) \\
    f_X(3) &= P(X = 3) = \tfrac{5}{16} && X = 3 \iff (i, j) = (1, 3), (2, 3), (3, 3), (3, 2), (3, 1) \\
    f_X(4) &= P(X = 4) = \tfrac{7}{16} && X = 4 \iff (i, j) = (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1)
    \end{aligned}
    $$

    $$
    f_X(5) = f_X(\tfrac{3}{2}) = f_X(-\pi) = 0 \qquad (X \text{ never takes those values})
    $$

    $$
    \begin{aligned}
    F_X(1) &= P(X \leq 1) = \tfrac{1}{16} && X \leq 1 \iff (i, j) = (1, 1) \\
    F_X(2) &= P(X \leq 2) = \tfrac{4}{16} && X \leq 2 \iff (i, j) = (1, 1), (1, 2), (2, 2), (2, 1) \\
    F_X(3) &= P(X \leq 3) = \tfrac{9}{16} && X \leq 3 \iff (i, j) = (1, 1), \dots, (3, 1) \\
    F_X(4) &= P(X \leq 4) = \tfrac{16}{16} && X \leq 4 \iff (i, j) = (1, 1), \dots, (4, 1) \quad (\text{all outcomes!})
    \end{aligned}
    $$

    $$
    \underbrace{F_X(5) = 1}_{X \leq 5 \text{ for every outcome}}, \qquad \underbrace{F_X(\tfrac{3}{2}) = \tfrac{1}{16}}_{X \leq \frac{3}{2} \text{ for } (1, 1) \text{ only}}, \qquad \underbrace{F_X(-\pi) = 0}_{X \leq -\pi \text{ for no outcome}}
    $$
    """
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
    ## Expectation (WMS 3.3)

    pmf of a discrete RV $X : S \longrightarrow \mathbb{R}$ gives the relative frequency of a result $x$ over infinitely many independent measurements

    To study their properties, it is useful to summarize the main characteristics of pmfs into certain numbers (mean, variance, …) &nbsp; $\leadsto$ &nbsp; expectations of $X$
    """
            ),
            definition(
                r"""
    Let $X$ be a discrete RV with pmf $f_X$. Given any function $u : \mathbb{R} \longrightarrow \mathbb{R}$, we define the **expectation** of $u(X) = u \circ X : S \longrightarrow \mathbb{R}$ &nbsp; (function of $X$, or composition of $u$ and $X$)

    $$
    E[u(X)] = \sum_{x} u(x)\, f_X(x)
    $$
    """
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $X(i, j) = \max(i, j)$

    $$
    \leadsto \quad E[X] = \sum_{x=1}^{4} x\, f_X(x) = 1 \cdot \tfrac{1}{16} + 2 \cdot \tfrac{3}{16} + 3 \cdot \tfrac{5}{16} + 4 \cdot \tfrac{7}{16} = \tfrac{50}{16} \approx 3.1
    $$

    **Example.** game: pay 3000 won to roll a 6-sided die, get 1000 won times the face value $X$. How much do you expect to win?

    $$
    \text{fair die} \quad \leadsto \quad E[1000 X - 3000] = \sum_{x=1}^{6} (1000 x - 3000) \times \tfrac{1}{6} = 500
    $$

    not fair &nbsp; (say $f_X(1) = f_X(2) = f_X(3) = \tfrac{1}{3}$, &nbsp; $f_X(4) = f_X(5) = f_X(6) = 0$)

    $$
    \leadsto \quad E[1000 X - 3000] = \sum_{x=1}^{3} (1000 x - 3000) \times \tfrac{1}{3} + \sum_{x=4}^{6} (1000 x - 3000) \times 0 = -1000
    $$

    **mean** = expectation of $X$ &nbsp; (measures the “center” of the distribution)

    $$
    \mu_X = E[X] = \sum_{x} x\, f_X(x)
    $$

    **variance** = expectation of $(X - \mu_X)^2$ &nbsp; (measures the “width” of the distribution)

    $$
    \sigma_X^2 = E[(X - \mu_X)^2] = \sum_{x} (x - \mu_X)^2\, f_X(x) \qquad (\sigma_X^2 = (\text{std deviation})^2)
    $$

    **skewness** = expectation of $\left( \dfrac{X - \mu_X}{\sigma_X} \right)^3$ &nbsp; (measures “symmetry” around the center)

    $$
    \gamma_X = E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = \sum_{x} \left( \frac{x - \mu_X}{\sigma_X} \right)^{\!3} f_X(x)
    $$

    **Example.** Toss a coin 4 times, $X$ = number of heads

    | | fair coin | biased coin |
    |:--|:--|:--|
    | | $P(\{H\}) = P(\{T\}) = \tfrac{1}{2}$ | $P(\{H\}) = \tfrac{1}{3}$, $P(\{T\}) = \tfrac{2}{3}$ |
    | $\mu_X$ | $E[X] = 2$ | $E[X] = \tfrac{4}{3}$ |
    | $\sigma_X^2$ | $E[(X - 2)^2] = 1$ | $E[(X - \tfrac{4}{3})^2] = \tfrac{8}{9}$ |
    | $\gamma_X$ | $E\!\left[ \left( \tfrac{X - 2}{1} \right)^3 \right] = 0$ | $E\!\left[ \left( \tfrac{X - 4/3}{\sqrt{8/9}} \right)^3 \right] = \tfrac{1}{\sqrt{8}}$ |
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    tosses = mo.ui.slider(1, 12, 1, value=4, label="number of tosses", show_value=True)
    coin = mo.ui.dropdown({"fair (1/2)": 0.5, "biased (1/3)": 1 / 3, "custom (slider)": None}, value="fair (1/2)", label="coin", allow_select_none=False)
    p_head = mo.ui.slider(0.05, 0.95, 0.01, value=0.5, label=r"custom $P(\{H\})$", show_value=True)
    return coin, p_head, tosses


@app.cell(hide_code=True)
def _(Figure, RED, coin, math, mo, p_head, tosses):
    _n = tosses.value
    _p = p_head.value if coin.value is None else coin.value
    _xs = list(range(_n + 1))
    _pmf = [math.comb(_n, _k) * _p**_k * (1 - _p) ** (_n - _k) for _k in _xs]
    _mu = sum(_x * _f for _x, _f in zip(_xs, _pmf))
    _m2 = sum(_x**2 * _f for _x, _f in zip(_xs, _pmf))
    _var = sum((_x - _mu) ** 2 * _f for _x, _f in zip(_xs, _pmf))
    _skew = sum(((_x - _mu) / math.sqrt(_var)) ** 3 * _f for _x, _f in zip(_xs, _pmf))

    _fig = Figure(figsize=(5.6, 3.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.vlines(_xs, 0, _pmf, color=RED, lw=1, alpha=0.4)
    _ax.plot(_xs, _pmf, "o", color=RED, ms=5)
    _ax.axvline(_mu, color="#555555", lw=1, ls="--")
    _ax.set_xticks(_xs)
    _ax.set_ylim(0, max(_pmf) * 1.25)
    _ax.set_xlabel("$x$")
    _ax.set_title(rf"$P(\{{H\}}) = {_p:.3f}$,  dashed line: $\mu_X$", fontsize=11)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $\mu_X = E[X]$ | ${_mu:.4f}$ |",
            rf"| $\sigma_X^2 = E[(X - \mu_X)^2]$ | ${_var:.4f}$ |",
            rf"| $\gamma_X$ | ${_skew:.4f}$ |",
            rf"| $E[X^2]$ | ${_m2:.4f}$ |",
            rf"| $E[X^2] - E[X]^2$ | ${_m2 - _mu**2:.4f}$ |",
        ]
    )
    mo.vstack(
        [
            mo.hstack([tosses, coin, p_head], justify="start", gap=3, wrap=True),
            mo.hstack([_fig, mo.md(_table)], widths=[1, 1], gap=2, align="center", wrap=True),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    game_preset = mo.ui.dropdown({"fair": (1, 1, 1, 1, 1, 1), "not fair (faces 1–3 only)": (1, 1, 1, 0, 0, 0)}, value="fair", label="die", allow_select_none=False)
    game_price = mo.ui.slider(0, 10000, 500, value=3000, label="price to play (won)", show_value=True)
    game_payout = mo.ui.slider(0, 3000, 100, value=1000, label="won per face value", show_value=True)
    return game_payout, game_preset, game_price


@app.cell(hide_code=True)
def _(game_preset, mo):
    game_weights = mo.ui.array([mo.ui.slider(0, 10, 1, value=w, label=f"face {i + 1}", show_value=True) for i, w in enumerate(game_preset.value)])
    return (game_weights,)


@app.cell(hide_code=True)
def _(game_payout, game_preset, game_price, game_weights, mo):
    from fractions import Fraction as _Fr

    _w = list(game_weights.value)
    _total = sum(_w)
    _a, _c = game_payout.value, game_price.value
    if _total == 0:
        _text = mo.md("**Note.** The weights must not all be zero.")
    else:
        _pmf = [_Fr(_wi, _total) for _wi in _w]
        _E = sum((_a * (_x + 1) - _c) * _f for _x, _f in enumerate(_pmf))
        _terms = " + ".join(rf"({_a}\cdot{_x + 1} - {_c}) \cdot \tfrac{{{_f.numerator}}}{{{_f.denominator}}}" for _x, _f in enumerate(_pmf) if _f)
        _text = mo.md(
            rf"$u(X) = {_a}\, X - {_c}$ &nbsp; (winnings)"
            + "\n\n"
            + rf"$E[u(X)] = \sum_x u(x)\, f_X(x) = {_terms}$"
            + "\n\n"
            + rf"$= {float(_E):,.0f}$ won".replace(",", r"\,")
        )
    mo.vstack(
        [
            mo.hstack([game_preset, game_price, game_payout], justify="start", gap=2, wrap=True),
            mo.hstack([game_weights[_i] for _i in range(6)], justify="start", gap=1.5, wrap=True),
            _text,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Let $X$ be a discrete RV, $u, v : \mathbb{R} \longrightarrow \mathbb{R}$ functions and $a, b, c \in \mathbb{R}$ constants

    $$
    E[a\, u(X) + b\, v(X)] = a\, E[u(X)] + b\, E[v(X)], \qquad E[c] = c
    $$
    """
            ),
            mo.md(
                r"""
    **Corollary.** &nbsp; $\sigma_X^2 = E[X^2] - E[X]^2$

    **Proof.**

    $$
    \begin{aligned}
    E[(X - \mu_X)^2] &= E[X^2 - 2 \mu_X X + \mu_X^2] \\
    &= E[X^2] - 2 \mu_X E[X] + \mu_X^2 \\
    &= E[X^2] - E[X]^2 \qquad \square
    \end{aligned}
    $$

    **Example.** flip a fair coin 4 times, $X$ = # heads

    $$
    \leadsto \quad E[X] = 0 \times \tfrac{1}{16} + 1 \times \tfrac{4}{16} + 2 \times \tfrac{6}{16} + 3 \times \tfrac{4}{16} + 4 \times \tfrac{1}{16} = \tfrac{32}{16} = 2
    $$

    $$
    \leadsto \quad E[X^2] = 0^2 \times \tfrac{1}{16} + 1^2 \times \tfrac{4}{16} + 2^2 \times \tfrac{6}{16} + 3^2 \times \tfrac{4}{16} + 4^2 \times \tfrac{1}{16} = \tfrac{80}{16} = 5
    $$

    $$
    \Longrightarrow \quad \sigma_X^2 = E[X^2] - E[X]^2 = 5 - 2^2 = 1
    $$
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

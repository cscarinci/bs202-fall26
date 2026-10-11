import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 04 · Random variables", css_file="bs202.css")


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
    header("Lecture 04", "Week 02", "Lecture 04 · Random variables")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, mo, np):
    ORANGE = "#f5a623"
    _fig = Figure(figsize=(4.2, 2.4), layout="constrained")
    _ax = _fig.subplots()
    for _x0, _x1, _col, _name in ((0, 1, RED, "$B_1$"), (1, 2, GREEN, "$B_2$"), (2, 3, BLUE, "$B_3$")):
        _ax.plot([_x0, _x1, _x1, _x0, _x0], [0, 0, 1.3, 1.3, 0], color=_col, lw=1.6)
        _lo, _hi = max(_x0, 0.72), min(_x1, 2.35)
        _ax.fill_between([_lo, _hi], 0.3, 1.0, color=_col, alpha=0.35, lw=0)
        _ax.text((_x0 + _x1) / 2 + (0.25 if _x0 == 2 else -0.25 if _x0 == 0 else 0), 0.08, _name, color=_col, fontsize=13, ha="center")
    _ax.plot([0.72, 2.35, 2.35, 0.72, 0.72], [0.3, 0.3, 1.0, 1.0, 0.3], color=ORANGE, lw=1.8)
    _ax.text(2.45, 1.05, "$A$", color=ORANGE, fontsize=14)
    _ax.text(-0.15, 1.35, "$S$", fontsize=14)
    for _x, _col, _name in ((0.33, RED, r"$A \cap B_1$"), (1.5, GREEN, r"$A \cap B_2$"), (2.68, BLUE, r"$A \cap B_3$")):
        _ax.text(_x, 0.62 if _x != 1.5 else 1.1, _name, color=_col, fontsize=10, ha="center")
    _ax.set_xlim(-0.25, 3.1)
    _ax.set_ylim(-0.1, 1.55)
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Knowledge about an event can change our belief about other events

    $$
    \underbrace{P(A \mid B)}_{\text{probability of } A \text{ given } B \text{ has occurred}} = \underbrace{\frac{P(A \cap B)}{P(B)}}_{\text{probability of } A \text{ and } B \text{ relative to probability of } B}
    \qquad \leadsto \qquad P(A \cap B) = P(A \mid B)\, P(B)
    $$

    If knowledge about $B$ does not change our belief about $A$, then $A$ and $B$ are independent!

    $$
    \leadsto \quad P(A \mid B) = P(A) \quad \Longleftrightarrow \quad P(A \cap B) = P(A)\, P(B)
    $$

    $$
    \text{Bayes' rule:} \qquad P(B \mid A) = \frac{P(A \cap B)}{P(A)} = \frac{P(A \mid B)\, P(B)}{P(A \mid B)\, P(B) + P(A \mid B^c)\, P(B^c)}
    $$

    $$
    \leadsto \quad \text{more generally:} \qquad P(B_j \mid A) = \frac{P(A \cap B_j)}{P(A)} = \frac{P(A \mid B_j)\, P(B_j)}{\displaystyle\sum_{i=1}^{k} P(A \mid B_i)\, P(B_i)}
    $$
    """
            ),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"""
    $$
    \begin{aligned}
    & B_1 \cup B_2 \cup \cdots \cup B_k = S && (\text{exhaustive}) \\
    & B_i \cap B_j = \emptyset \quad \forall\, i \neq j \in \{1, 2, \dots, k\} && (\text{mutually disjoint})
    \end{aligned}
    $$
    """
                    ),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
                wrap=True,
            ),
            mo.md(
                r"""
    - $P(B_i)$ = prior level of belief &nbsp; $\leadsto$ &nbsp; probability of having a disease before testing
    - $P(B_i \mid A)$ = posterior level of belief &nbsp; $\leadsto$ &nbsp; probability of having a disease after testing
    - $P(A \mid B_i)$ = likelihoods &nbsp; $\leadsto$ &nbsp; true positive rates and false positive rates

    $$
    \text{Law of total probability:} \qquad P(A) = \sum_{i=1}^{k} P(A \mid B_i)\, P(B_i)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, RED, cross_axes, definition, mo):
    _fig = Figure(figsize=(5.6, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.8, 17.5)
    _ax.set_ylim(-1.6, 6.2)
    _ax.axis("off")
    _ax.annotate("", xy=(17.3, 0), xytext=(-0.5, 0), arrowprops={"arrowstyle": "-|>", "color": "black", "lw": 0.9})
    _ax.annotate("", xy=(0, 6), xytext=(0, -0.3), arrowprops={"arrowstyle": "-|>", "color": "black", "lw": 0.9})
    _vals = [0, 0, 0, 0, 0, 0, 0, 0.3, 0.6, 1.5, 2.6, 3.6, 4.3, 4.9, 5.2, 5.6]
    for _k, _v in enumerate(_vals):
        _ax.plot(_k + 1, _v, "o", color=RED, ms=3.5)
        _ax.text(_k + 1, -0.6, f"{11 + _k}", fontsize=8, ha="center")
    _ax.text(17.2, -0.6, "$x$", fontsize=12)
    _ax.text(0.3, 5.8, "$y$", fontsize=12)
    _ax.text(3.0, 4.0, r"$y = P_X(\{x\})$", color=RED, fontsize=13)
    _ax.plot([1, 7], [-1.0, -1.0], color="#2e7d32", lw=1)
    _ax.text(4, -1.6, "graduated", color="#2e7d32", fontsize=10, ha="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## 4 &nbsp; Random variables

    random experiment &nbsp; $\leftrightsquigarrow$ &nbsp; probability space $(S, \mathcal{E}, P)$

    So far we considered “simple” examples

    - equally likely outcomes
    - easy algebra of finite sets
    - probability = counting

    In general, $(S, \mathcal{E}, P)$ too complicated

    - no direct description
    - messy algebra of events
    - hard to compute probability

    measurements on random experiments &nbsp; $\leftrightsquigarrow$ &nbsp; real valued functions on the sample space

    - associates real numbers to each outcome (measurements)
    - simplify the model by only focusing on those numbers
    """
            ),
            definition(
                r"""
    Given a probability space $(S, \mathcal{E}, P)$, a **random variable** on $S$ is a function

    $$
    \begin{aligned}
    X : S &\longrightarrow \mathbb{R} \\
    o &\longmapsto X(o)
    \end{aligned}
    $$

    The image of $X$

    $$
    S_X = \mathrm{Im}(X) = \{\, x \in \mathbb{R} \mid X(o) = x \text{ for some } o \in S \,\} \subseteq \mathbb{R}
    $$

    is called the **state space** of $X$.
    """
            ),
            mo.md(
                r"""
    It will serve as a simplified version of the true sample space $S$.

    **Example.** Choose a DGIST student at random

    $$
    S = \{\text{3000 individual human beings}\}
    $$

    How can we describe events?

    $$
    A = \{\text{male}\}, \quad B = \{\text{female}\}, \quad C = \{\text{non-binary}\}, \quad D = \{\text{Korean}\}, \quad E = \{\text{plays football}\}, \ \dots
    $$

    We can come up with an enormous number of events. Hopeless to try to find a “complete” model.

    Instead, we can collect measurements of aspects we are interested in and focus on modeling those measurements only!

    $$
    \begin{aligned}
    X &= \text{year in DGIST} && \leadsto \quad S_X = \{2011, 2012, \dots, 2026\} \\
    Y &= \text{current GPA} && \leadsto \quad S_Y = [0, 4]
    \end{aligned}
    $$

    **Remark.** Given $X : S \longrightarrow \mathbb{R}$

    | | definition | role |
    |:--|:--|:--|
    | state space | $S_X = \mathrm{Im}(X) \subseteq \mathbb{R}$ | simplified version of $S$ |
    | algebra of subsets of $S_X$ | $\mathcal{E}_X = \{\, A \subseteq S_X \subseteq \mathbb{R} \,\}$ &nbsp; (collection of subsets in $\mathbb{R}$: intervals and points) | simplified version of $\mathcal{E}$ |
    | probability distribution of $X : S \longrightarrow \mathbb{R}$ | $P_X : \mathcal{E}_X \longrightarrow \mathbb{R}$ | simplified version of $P : \mathcal{E} \longrightarrow \mathbb{R}$ |

    $$
    P_X(A) = P\big( \underbrace{\{\, o \in S \mid X(o) \in A \,\}}_{\text{outcomes whose value of } X \text{ belongs to } A} \big) = P(X \in A)
    $$

    **Example.** &nbsp; $S = \{\text{all students}\}$, &nbsp; $X$ = year in DGIST &nbsp; $\leadsto$ &nbsp; $S_X = \{2011, \dots, 2025, 2026\}$

    $$
    \underbrace{P_X(\{2026\})}_{\substack{\{2026\}:\ \text{subset of } \mathbb{R} \\ \text{easy to characterize with a census of DGIST}}} = \underbrace{P(\{\text{is freshman}\})}_{\substack{\text{subset of humans} \\ \text{impossible to model “completely”}}} = P(\{X = 2026\})
    $$
    """
            ),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"In probability theory, we are more interested in modeling RV and their distributions, than in the full probability spaces!"
                    ),
                ],
                widths=[3, 2],
                gap=2,
                align="center",
                wrap=True,
            ),
            definition(
                r"""
    A RV $X : S \longrightarrow \mathbb{R}$ is called

    - **discrete** if $S_X = \mathrm{Im}(X)$ consists of *countably many points* (we can count them: 1st, 2nd, 3rd, …)
    - **continuous** if $S_X = \mathrm{Im}(X)$ is uncountable + extra conditions (later)
    """
            ),
            mo.md(
                r"""
    **Example** (Roll two fair 4-sided dice). &nbsp; $\leadsto$ &nbsp; $S = \{\, (i, j) \mid i, j \in \{1, 2, 3, 4\} \,\}$

    $$
    X(i, j) = \begin{cases} \max(i, j), & i \neq j \\ i, & i = j \end{cases} \ = \text{largest face} \qquad \leadsto \quad S_X = \{1, 2, 3, 4\}
    $$

    $$
    Y(i, j) = i + j = \text{sum of faces} \qquad \leadsto \quad S_Y = \{2, 3, \dots, 7, 8\}
    $$
    """
            ),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ discrete RV, the **probability mass function** (pmf) of $X$ is

    $$
    f_X : \mathbb{R} \longrightarrow [0, 1], \qquad x \longmapsto f_X(x) = P(X = x) \qquad (\text{probability of } X \text{ having value } x)
    $$

    $f_X$ satisfies

    - $f_X(x) \geq 0 \quad \forall\, x \in S_X$
    - $f_X(x) = 0 \quad \forall\, x \notin S_X$
    - $\displaystyle\sum_{x \in S_X} f_X(x) = 1$
    - $\displaystyle\sum_{x \in A} f_X(x) = P(X \in A)$
    """
            ),
            mo.md(
                r"""
    $$
    X(i, j) = \begin{cases} \max(i, j), & i \neq j \in \{1, 2, 3, 4\} \\ i, & i = j \in \{1, 2, 3, 4\} \end{cases}
    $$

    $$
    \begin{aligned}
    f_X(1) &= P(X = 1) = P(\{(1, 1)\}) = \tfrac{1}{16} \\
    f_X(2) &= P(X = 2) = P(\{(2, 1), (2, 2), (1, 2)\}) = \tfrac{3}{16} \\
    f_X(3) &= P(\{(3, 1), (3, 2), (3, 3), (2, 3), (1, 3)\}) = \tfrac{5}{16} \\
    f_X(4) &= \tfrac{7}{16}, \qquad f_X(5) = 0, \qquad f_X(6) = 0
    \end{aligned}
    $$
    """
            ),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ discrete RV, the **cumulative distribution function** (cdf) of $X$ is

    $$
    F_X : \mathbb{R} \longrightarrow [0, 1], \qquad x \longmapsto F_X(x) = P(X \leq x) \qquad (\text{probability of } X \text{ having value at most } x)
    $$
    """
            ),
            mo.md(
                r"""
    $$
    \begin{aligned}
    F_X(1) &= P(X \leq 1) = P(X = 1) = \tfrac{1}{16} \\
    F_X(2) &= P(X \leq 2) = P(X \leq 1) + P(X = 2) = \tfrac{1}{16} + \tfrac{3}{16} = \tfrac{1}{4} \\
    F_X(3) &= P(X \leq 3) = P(X \leq 2) + P(X = 3) = \tfrac{1}{4} + \tfrac{5}{16} = \tfrac{9}{16} \\
    F_X(4) &= \tfrac{9}{16} + \tfrac{7}{16} = 1, \qquad F_X(5) = 1, \qquad F_X(6) = 1
    \end{aligned}
    $$

    $$
    \leadsto \quad
    \begin{aligned}
    F_X(4) - F_X(3) &= f_X(4) \\
    F_X(3) - F_X(2) &= f_X(3) \\
    F_X(2) - F_X(1) &= f_X(2) \\
    F_X(1) - F_X(0) &= f_X(1)
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    rv_choice = mo.ui.dropdown(["X = largest face", "Y = sum of faces"], value="X = largest face", label="random variable")
    sides = mo.ui.slider(2, 8, 1, value=4, label="sides of each die", show_value=True)
    return rv_choice, sides


@app.cell(hide_code=True)
def _(mo, rv_choice, sides):
    _n = sides.value
    _lo, _hi = (1, _n) if rv_choice.value.startswith("X") else (2, 2 * _n)
    range_a = mo.ui.slider(_lo, _hi, 1, value=_lo, label="$a$", show_value=True)
    range_b = mo.ui.slider(_lo, _hi, 1, value=_hi, label="$b$", show_value=True)
    return range_a, range_b


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, mo, range_a, range_b, rv_choice, sides):
    from fractions import Fraction as _Fr

    _n = sides.value
    _is_max = rv_choice.value.startswith("X")
    _counts = {}
    for _i in range(1, _n + 1):
        for _j in range(1, _n + 1):
            _v = max(_i, _j) if _is_max else _i + _j
            _counts[_v] = _counts.get(_v, 0) + 1
    _xs = sorted(_counts)
    _pmf = [_counts[_x] / _n**2 for _x in _xs]
    _cdf = [sum(_pmf[: _k + 1]) for _k in range(len(_xs))]
    _a, _b = range_a.value, range_b.value

    _fig = Figure(figsize=(9.0, 3.4), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    if _a <= _b:
        _left.axvspan(_a - 0.5, _b + 0.5, color=BLUE, alpha=0.08, lw=0)
    _left.vlines(_xs, 0, _pmf, color=RED, lw=1, alpha=0.4)
    _left.plot(_xs, _pmf, "o", color=RED, ms=5)
    _left.set_title("pmf  $f(x)$", fontsize=13)
    _left.set_xticks(_xs)
    _left.set_ylim(0, max(_pmf) * 1.25)
    _lo, _hi = _xs[0] - 1, _xs[-1] + 1
    _edges = [_lo] + _xs + [_hi]
    _levels = [0] + _cdf
    for _k, _lev in enumerate(_levels):
        _right.plot([_edges[_k], _edges[_k + 1]], [_lev, _lev], color=RED, lw=1.8)
        if _k > 0:
            _right.plot(_edges[_k], _lev, "o", color=RED, ms=5)
            _right.plot(_edges[_k], _levels[_k - 1], "o", color=RED, ms=5, mfc="white")
            _right.plot([_edges[_k], _edges[_k]], [_levels[_k - 1], _lev], ":", color=GREEN, lw=1)
            if len(_xs) <= 8:
                _q = _Fr(_counts[_xs[_k - 1]], _n**2)
                _right.text(_edges[_k] + 0.08, (_lev + _levels[_k - 1]) / 2, rf"$f({_xs[_k - 1]}) = \frac{{{_q.numerator}}}{{{_q.denominator}}}$", color=GREEN, fontsize=9, va="center")
    if _a <= _b:
        for _v, _ls in ((_a - 1, "--"), (_b, "-")):
            _right.axvline(_v, color=BLUE, lw=1, ls=_ls, alpha=0.6)
    _right.set_title("cdf  $F(x)$", fontsize=13)
    _right.set_xticks(_xs)
    _right.set_ylim(-0.05, 1.1)
    for _ax in (_left, _right):
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    _F = lambda x: sum(_counts[_v] for _v in _xs if _v <= x)
    _row_f = " | ".join(str(_Fr(_counts[_x], _n**2)) for _x in _xs)
    _row_F = " | ".join(str(_Fr(_F(_x), _n**2)) for _x in _xs)
    _table = "| $x$ | " + " | ".join(str(_x) for _x in _xs) + " |\n|:--|" + ":-:|" * len(_xs) + "\n| $f(x)$ | " + _row_f + " |\n| $F(x)$ | " + _row_F + " |"
    if _a <= _b:
        _p = _Fr(_F(_b) - _F(_a - 1), _n**2)
        _rv = "X" if _is_max else "Y"
        _prob = rf"$P({_a} \le {_rv} \le {_b}) = F({_b}) - F({_a - 1}) = \sum_{{x = {_a}}}^{{{_b}}} f(x) = \tfrac{{{_p.numerator}}}{{{_p.denominator}}}$"
    else:
        _prob = r"need $a \le b$"
    mo.vstack(
        [
            mo.hstack([rv_choice, sides], justify="start", gap=3, wrap=True),
            _fig,
            mo.md(_table),
            mo.hstack([range_a, range_b], justify="start", gap=3, wrap=True),
            mo.md(_prob),
        ]
    )
    return


@app.cell(hide_code=True)
def _(box):
    answers = tuple(box() for _ in range(5))
    pmf_answers = tuple(box() for _ in range(5))
    return answers, pmf_answers


@app.cell(hide_code=True)
def _(answers, ask, mo, pmf_answers):
    _a1, _b1, _q2, _c1, _c2 = answers
    mo.vstack(
        [
            mo.md(
                r"""
    pmf and cdf are different ways to encode the probability distribution of a RV $X$.

    We will spend the next several lectures studying properties and examples of such functions!

    ## Practice

    ### Question 1

    A lab uses chemicals kits from three suppliers

    $$
    P(S_1) = 50\%, \qquad P(S_2) = 30\%, \qquad P(S_3) = 20\%
    $$

    Contamination rate of kits from each supplier is

    $$
    P(C \mid S_1) = 1\%, \qquad P(C \mid S_2) = 2\%, \qquad P(C \mid S_3) = 5\%
    $$

    (a) What is the probability that a kit is contaminated?
    """
            ),
            ask("probability $=$", _a1, 0.021, 0.0005),
            mo.md(r"(b) Given a contaminated kit, what is the probability it came from supplier 3?"),
            ask("probability $=$", _b1, 10 / 21, 0.005),
            mo.md(
                r"""
    ### Question 2

    A box has 5 red, 4 blue and 3 green balls. Choose 3 without replacement. Find the probability that no ball is red.
    """
            ),
            ask("probability $=$", _q2, 35 / 220, 0.005),
            mo.md(
                r"""
    ### Question 3

    Suppose $X$ has state space $S_X = \{0, 1, 2, 3, 4\}$ with cdf

    $$
    F_X(0) = 0.1, \quad F_X(1) = 0.35, \quad F_X(2) = 0.65, \quad F_X(3) = 0.9, \quad F_X(4) = 1.
    $$

    (a) Find $f_X$ (pmf).
    """
            ),
            *[ask(rf"$f_X({_x}) =$", _f, _v, 0.0005) for _x, _f, _v in zip(range(5), pmf_answers, (0.1, 0.25, 0.3, 0.25, 0.1))],
            mo.md(r"(b) Compute $P(X > 2)$ and $P(1 \leq X \leq 3)$."),
            ask(r"$P(X > 2) =$", _c1, 0.35, 0.0005),
            ask(r"$P(1 \leq X \leq 3) =$", _c2, 0.8, 0.0005),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

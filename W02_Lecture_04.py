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
      <div class="bs-title">Introduction to Probability and Mathematical Statistics</div>
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
    header("Lecture 04", "Week 02", "Lecture 04 · Random variables")
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
def _(BLUE, HALF, LIGHT, blank, mo):
    _fig, _ax = blank(HALF, 1.9, (-0.25, 3.15), (-0.1, 1.55))
    _ax.fill([0.3, 2.7, 2.7, 0.3], [0.35, 0.35, 0.95, 0.95], color=LIGHT, lw=0)
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 1.3, 1.3, 0], color="black", lw=1.0)
    for _x in (1, 2):
        _ax.plot([_x, _x], [0, 1.3], color="black", lw=1.0)
    _ax.plot([0.3, 2.7, 2.7, 0.3, 0.3], [0.35, 0.35, 0.95, 0.95, 0.35], color=BLUE, lw=1.4)
    for _k, _x in enumerate((0.65, 1.5, 2.35)):
        _ax.text(_x, 0.65, rf"$A \cap B_{_k + 1}$", fontsize=12, ha="center", va="center")
        _ax.text(_k + 0.5, 0.16, rf"$B_{_k + 1}$", fontsize=12, ha="center", va="center")
    _ax.text(2.72, 1.0, "$A$", color=BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(-0.06, 1.34, "$S$", fontsize=13, ha="right", va="bottom")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - knowledge about an event can change our belief about other events

        $$
        \underbrace{P(A \mid B)}_{\substack{\text{probability of } A \\ \text{given } B \text{ has occurred}}} = \underbrace{\frac{P(A \cap B)}{P(B)}}_{\substack{\text{probability of } A \text{ and } B \\ \text{relative to probability of } B}}
        \qquad \leadsto \qquad P(A \cap B) = P(A \mid B)\, P(B)
        $$

    - if knowledge about $B$ does not change our belief about $A$, then $A$ and $B$ are **independent**!

        $$
        \leadsto \qquad P(A \mid B) = P(A) \qquad \Longleftrightarrow \qquad P(A \cap B) = P(A)\, P(B)
        $$
    - Bayes' rule:

        $$
        P(B \mid A) = \frac{P(A \cap B)}{P(A)} = \frac{P(A \mid B)\, P(B)}{P(A \mid B)\, P(B) + P(A \mid B^c)\, P(B^c)}
        $$

    - $\leadsto$ &nbsp; more generally, for $B_1 \cup B_2 \cup \cdots \cup B_k = S$ (exhaustive) and $B_i \cap B_j = \emptyset \ \ \forall\, i \neq j \in \{1, 2, \dots, k\}$ (mutually disjoint):

        $$
        P(B_j \mid A) = \frac{P(A \cap B_j)}{P(A)} = \frac{P(A \mid B_j)\, P(B_j)}{\displaystyle\sum_{i=1}^{k} P(A \mid B_i)\, P(B_i)}
        $$
    """
            ),
            _fig,
            mo.md(
                r"""
    - $P(B_i)$ = prior level of belief &nbsp; $\leadsto$ &nbsp; probability of having a disease before testing
    - $P(B_i \mid A)$ = posterior level of belief &nbsp; $\leadsto$ &nbsp; probability of having a disease after testing
    - $P(A \mid B_i)$ = likelihoods &nbsp; $\leadsto$ &nbsp; true positive rates and false positive rates
    - law of total probability: &nbsp; $P(A) = \displaystyle\sum_{i=1}^{k} P(A \mid B_i)\, P(B_i)$

    **In this lecture:** random variables and their probability distributions: pmf and cdf
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.1 &nbsp; Random variables

    random experiment &nbsp; $\leftrightsquigarrow$ &nbsp; probability space $(S, \mathcal{E}, P)$

    $\leadsto$ &nbsp; so far we considered “simple” examples

    - equally likely outcomes
    - easy algebra of finite sets
    - probability = counting

    $\leadsto$ &nbsp; in general, $(S, \mathcal{E}, P)$ too complicated

    - no direct description
    - messy algebra of events
    - hard to compute probability

    measurements on random experiments &nbsp; $\leftrightsquigarrow$ &nbsp; real valued functions on the sample space

    - associates real numbers to each outcome (measurements)
    - simplify the model by only focusing on those numbers

    ### Random variables and their state space
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
    """,
                "Random variable and state space",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; it will serve as a simplified version of the true sample space $S$

    **Example.** Choose a DGIST student at random

    $$
    S = \{\text{3000 individual human beings}\}
    $$

    $\leadsto$ &nbsp; how can we describe events?

    $$
    A = \{\text{male}\}, \quad B = \{\text{female}\}, \quad C = \{\text{non-binary}\}, \quad D = \{\text{Korean}\}, \quad E = \{\text{plays football}\}, \ \dots
    $$

    $\leadsto$ &nbsp; we can come up with an enormous number of events

    $\leadsto$ &nbsp; hopeless to try to find a “complete” model

    $\leadsto$ &nbsp; instead, we can collect measurements of aspects we are interested in and focus on modeling those measurements only!

    $$
    \begin{aligned}
    X &= \text{year in DGIST} && \leadsto \qquad S_X = \{2011, 2012, \dots, 2026\} \\
    Y &= \text{current GPA} && \leadsto \qquad S_Y \subseteq [0, 4] \\[2pt]
    & && \phantom{\leadsto \qquad} (\text{finitely many values here; usually modeled by all of } [0, 4])
    \end{aligned}
    $$

    **Remark.** Given $X : S \longrightarrow \mathbb{R}$

    | | | |
    |:--|:--|:--|
    | **state space** | $S_X = \mathrm{Im}(X) \subseteq \mathbb{R}$ | simplified version of $S$ |
    | **algebra of subsets** of $S_X$ | $\mathcal{E}_X = \{\, A \subseteq S_X \subseteq \mathbb{R} \,\}$ &nbsp; (collection of subsets in $\mathbb{R}$: intervals and points) | simplified version of $\mathcal{E}$ |
    | **probability distribution** of $X : S \longrightarrow \mathbb{R}$ | $P_X : \mathcal{E}_X \longrightarrow \mathbb{R}$ | simplified version of $P : \mathcal{E} \longrightarrow \mathbb{R}$ |

    $$
    P_X(A) = P\big( \underbrace{\{\, o \in S \mid X(o) \in A \,\}}_{\text{outcomes whose value of } X \text{ belongs to } A} \big) = P(X \in A)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREY, arrow, blank, definition, mo):
    _fig, _ax = blank(FULL, 2.9, (-1.0, 18.4), (-2.3, 6.6))
    arrow(_ax, (-0.5, 0), (17.8, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 6.4), "black", lw=0.9)
    _vals = [0, 0, 0, 0, 0, 0, 0, 0.3, 0.6, 1.5, 2.6, 3.6, 4.3, 4.9, 5.2, 5.6]
    for _k, _v in enumerate(_vals):
        _ax.plot([_k + 1, _k + 1], [-0.1, 0.1], color="black", lw=0.9)
        _ax.plot(_k + 1, _v, "o", color=BLUE, ms=4, zorder=4)
        _ax.text(_k + 1, -0.3, f"${11 + _k}$", fontsize=12, ha="center", va="top")
    _ax.text(17.9, -0.3, "$x$", fontsize=13, ha="center", va="top")
    _ax.text(0.35, 6.3, "$y$", fontsize=13, ha="left", va="top")
    _ax.text(4.0, 3.6, r"$y = P_X(\{x\})$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.plot([0.7, 0.7, 7.3, 7.3], [-1.15, -1.4, -1.4, -1.15], color=GREY, lw=1.0)
    _ax.text(4, -1.55, "graduated", fontsize=12, ha="center", va="top")

    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** &nbsp; $S = \{\text{all students}\}$, &nbsp; $X$ = year in DGIST &nbsp; $\leadsto$ &nbsp; $S_X = \{2011, \dots, 2025, 2026\}$

    $$
    \underbrace{P_X(\{2026\})}_{\substack{\{2026\}:\ \text{subset of } \mathbb{R} \\ \text{easy to characterize with a census of DGIST}}} = \underbrace{P(\{\text{is freshman}\})}_{\substack{\text{subset of humans} \\ \text{impossible to model “completely”}}} = P(\{X = 2026\})
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    In probability theory, we are more interested in modeling random variables and their distributions, than in the full probability spaces!

    ### Discrete and continuous random variables
    """
            ),
            definition(
                r"""
    A random variable $X : S \longrightarrow \mathbb{R}$ is called

    - **discrete** if $S_X = \mathrm{Im}(X)$ consists of *countably many points* (we can count them: 1st, 2nd, 3rd, …)
    - **continuous** if $S_X = \mathrm{Im}(X)$ is uncountable + extra conditions (later)
    """,
                "Discrete and continuous random variables",
            ),
            mo.md(
                r"""
    **Example** (Roll two fair 4-sided dice). &nbsp; $\leadsto$ &nbsp; $S = \{\, (i, j) \mid i, j \in \{1, 2, 3, 4\} \,\}$

    $$
    X(i, j) = \begin{cases} \max(i, j), & i \neq j \\ i, & i = j \end{cases} \ = \text{largest face} \qquad \leadsto \qquad S_X = \{1, 2, 3, 4\}
    $$

    $$
    Y(i, j) = i + j = \text{sum of faces} \qquad \leadsto \qquad S_Y = \{2, 3, \dots, 7, 8\}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, HALF, arrow, definition, mo):
    # pmf of X = largest face of two fair 4-sided dice
    _fig1 = Figure(figsize=(HALF, 2.5), layout="constrained")
    _ax = _fig1.subplots()
    _pmf = [0, 1 / 16, 3 / 16, 5 / 16, 7 / 16, 0, 0]
    for _x, _p in enumerate(_pmf):
        _ax.plot([_x, _x], [0, _p], color=BLUE, lw=1.0)
        _ax.plot(_x, _p, "o", color=BLUE, ms=4.5, zorder=4, clip_on=False)
    _ax.set_xlim(-0.5, 6.5)
    _ax.set_ylim(0, 0.5)
    _ax.set_xticks(range(7))
    _ax.set_yticks([_k / 16 for _k in (1, 3, 5, 7)], [rf"$\frac{{{_k}}}{{16}}$" for _k in (1, 3, 5, 7)])
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")

    # cdf of X: a step function, closed dot where the value is attained
    _fig2 = Figure(figsize=(HALF, 2.7), layout="constrained")
    _bx = _fig2.subplots()
    _edges = [-1, 1, 2, 3, 4, 6.4]
    _levels = [0, 1 / 16, 1 / 4, 9 / 16, 1]
    for _k, _lev in enumerate(_levels):
        _bx.plot([_edges[_k], _edges[_k + 1]], [_lev, _lev], color=BLUE, lw=1.6)
        if _k > 0:
            if _k < 3:
                _bx.plot([_edges[_k], _edges[_k]], [_levels[_k - 1], _lev], color=GREY, lw=0.9, ls=(0, (1, 2)))
            _bx.plot(_edges[_k], _levels[_k - 1], "o", color=BLUE, ms=4.5, mfc="white", zorder=4)
            _bx.plot(_edges[_k], _lev, "o", color=BLUE, ms=4.5, zorder=4)
    for _x, _lo, _hi, _name in ((3, 1 / 4, 9 / 16, r"$f_X(3) = \frac{5}{16}$"), (4, 9 / 16, 1, r"$f_X(4) = \frac{7}{16}$")):
        _mid = (_lo + _hi) / 2
        arrow(_bx, (_x, _mid), (_x, _hi), GREEN, shrinkB=3)
        arrow(_bx, (_x, _mid), (_x, _lo), GREEN, shrinkB=3)
        _bx.text(_x + 0.22, _mid, _name, color=GREEN, fontsize=12, ha="left", va="center")
    _bx.set_xlim(-1, 6.4)
    _bx.set_ylim(-0.06, 1.12)
    _bx.set_xticks(range(7))
    _bx.set_yticks([0.25, 0.5, 0.75, 1], [r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{3}{4}$", "$1$"])
    _bx.set_xlabel("$x$")
    _bx.set_ylabel("$F_X(x)$")
    for _a in (_ax, _bx):
        for _s in ("top", "right"):
            _a.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(r"""### The probability mass function"""),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ discrete random variable, the **probability mass function** (pmf) of $X$ is

    $$
    f_X : \mathbb{R} \longrightarrow [0, 1], \qquad x \longmapsto f_X(x) = \underbrace{P(X = x)}_{\text{probability of } X \text{ having value } x}
    $$

    $f_X$ satisfies

    - $f_X(x) \geq 0 \quad \forall\, x \in S_X$
    - $f_X(x) = 0 \quad \forall\, x \notin S_X$
    - $\displaystyle\sum_{x \in S_X} f_X(x) = 1$
    - $\displaystyle\sum_{x \in A} f_X(x) = P(X \in A)$
    """,
                "Probability mass function",
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
            _fig1,
            mo.md(r"""### The cumulative distribution function"""),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ discrete random variable, the **cumulative distribution function** (cdf) of $X$ is

    $$
    F_X : \mathbb{R} \longrightarrow [0, 1], \qquad x \longmapsto F_X(x) = \underbrace{P(X \leq x)}_{\text{probability of } X \text{ having value at most } x}
    $$
    """,
                "Cumulative distribution function",
            ),
            mo.md(
                r"""
    $$
    X(i, j) = \begin{cases} \max(i, j), & i \neq j \\ i, & i = j \end{cases}
    $$

    $$
    \begin{aligned}
    F_X(1) &= P(X \leq 1) = P(X = 1) = \tfrac{1}{16} \\
    F_X(2) &= P(X \leq 2) = P(X \leq 1) + P(X = 2) = \tfrac{1}{16} + \tfrac{3}{16} = \tfrac{1}{4} \\
    F_X(3) &= P(X \leq 3) = P(X \leq 2) + P(X = 3) = \tfrac{1}{4} + \tfrac{5}{16} = \tfrac{9}{16} \\
    F_X(4) &= \tfrac{9}{16} + \tfrac{7}{16} = 1, \qquad F_X(5) = 1, \qquad F_X(6) = 1
    \end{aligned}
    $$

    $$
    \leadsto \qquad
    \begin{aligned}
    F_X(4) - F_X(3) &= f_X(4) \\
    F_X(3) - F_X(2) &= f_X(3) \\
    F_X(2) - F_X(1) &= f_X(2) \\
    F_X(1) - F_X(0) &= f_X(1)
    \end{aligned}
    $$
    """
            ),
            _fig2,
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
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, mo, range_a, range_b, rv_choice, sides, table):
    from fractions import Fraction as _Fr

    _n = sides.value
    _is_max = rv_choice.value.startswith("X")
    _rv = "X" if _is_max else "Y"
    _counts = {}
    for _i in range(1, _n + 1):
        for _j in range(1, _n + 1):
            _v = max(_i, _j) if _is_max else _i + _j
            _counts[_v] = _counts.get(_v, 0) + 1
    _xs = sorted(_counts)
    _pmf = [_counts[_x] / _n**2 for _x in _xs]
    _a, _b = range_a.value, range_b.value

    def _F(x):
        """Number of outcomes (out of n^2) with value at most x."""
        return sum(_counts[_v] for _v in _xs if _v <= x)

    def _tex(q):
        return f"{q.numerator}" if q.denominator == 1 else rf"\tfrac{{{q.numerator}}}{{{q.denominator}}}"

    _lo, _hi = _xs[0] - 1, _xs[-1] + 1
    _ticks = _xs if len(_xs) <= 9 else _xs[::2]

    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    if _a <= _b:
        _left.axvspan(_a - 0.5, _b + 0.5, color=LIGHT, lw=0)
        for _v in (_a - 0.5, _b + 0.5):
            _left.axvline(_v, color=GREY, lw=1.0, ls=(0, (4, 3)))
    _left.vlines(_xs, 0, _pmf, color=BLUE, lw=1.0)
    _left.plot(_xs, _pmf, "o", color=BLUE, ms=4.5, zorder=4)
    _left.set_xlim(_lo, _hi)
    _left.set_ylim(0, max(_pmf) * 1.25)
    _left.set_xticks(_ticks)
    _left.set_xlabel("$x$")
    _left.set_ylabel(f"$f_{_rv}(x)$")

    _edges = [_lo] + _xs + [_hi]
    _levels = [0] + [_F(_x) / _n**2 for _x in _xs]
    for _k, _lev in enumerate(_levels):
        _right.plot([_edges[_k], _edges[_k + 1]], [_lev, _lev], color=BLUE, lw=1.6)
        if _k > 0:
            _right.plot([_edges[_k], _edges[_k]], [_levels[_k - 1], _lev], color=GREY, lw=0.9, ls=(0, (1, 2)))
            _right.plot(_edges[_k], _levels[_k - 1], "o", color=BLUE, ms=4.5, mfc="white", zorder=4)
            _right.plot(_edges[_k], _lev, "o", color=BLUE, ms=4.5, zorder=4)
    _span = _hi - _lo
    _xg = _hi + 0.09 * _span  # the difference F(b) - F(a - 1) is read off on the right of the plot
    if _a <= _b:
        _y0, _y1 = _F(_a - 1) / _n**2, _F(_b) / _n**2
        _right.plot([_a, _xg], [_y0, _y0], color=GREY, lw=1.0, ls=(0, (4, 3)))
        _right.plot([_b, _xg], [_y1, _y1], color=GREY, lw=1.0, ls=(0, (4, 3)))
        _cap = 0.02 * _span
        _right.plot([_xg - _cap, _xg + _cap, _xg, _xg, _xg - _cap, _xg + _cap], [_y0, _y0, _y0, _y1, _y1, _y1], color=GREEN, lw=1.6, zorder=3)
    _right.set_xlim(_lo, _hi + 0.16 * _span)
    _right.set_ylim(-0.06, 1.12)
    _right.set_xticks(_ticks)
    _right.set_xlabel("$x$")
    _right.set_ylabel(f"$F_{_rv}(x)$")
    for _ax in (_left, _right):
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    _values = (
        "| $x$ | " + " | ".join(str(_x) for _x in _xs) + " |\n|:--|" + ":-:|" * len(_xs)
        + f"\n| $f_{_rv}(x)$ | " + " | ".join(f"${_tex(_Fr(_counts[_x], _n**2))}$" for _x in _xs)
        + f" |\n| $F_{_rv}(x)$ | " + " | ".join(f"${_tex(_Fr(_F(_x), _n**2))}$" for _x in _xs) + " |"
    )
    if _a <= _b:
        _p = _Fr(_F(_b) - _F(_a - 1), _n**2)
        _sum = rf"$\displaystyle\sum_{{x = {_a}}}^{{{_b}}} f_{_rv}(x) = \textcolor{{{GREEN}}}{{{_tex(_p)}}}$"
        _diff = rf"${_tex(_Fr(_F(_b), _n**2))} - {_tex(_Fr(_F(_a - 1), _n**2))} = \textcolor{{{GREEN}}}{{{_tex(_p)}}}$"
    else:
        _sum = _diff = r"need $a \leq b$"
    mo.vstack(
        [
            mo.hstack([rv_choice, sides, range_a, range_b], justify="start", gap=2, wrap=True),
            mo.md(_values),
            table(
                [
                    (rf"$P(a \leq {_rv} \leq b)$", _sum),
                    (rf"$F_{_rv}(b) - F_{_rv}(a - 1)$", _diff),
                ]
            ),
            _fig,
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
    pmf and cdf are different ways to encode the probability distribution of a random variable $X$.

    We will spend the next several lectures studying properties and examples of such functions!

    ## Practice

    ### Question 1

    A lab uses chemical kits from three suppliers

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a random variable is a function $X : S \longrightarrow \mathbb{R}$ on the sample space; its state space $S_X = \mathrm{Im}(X) \subseteq \mathbb{R}$ serves as a simplified version of $S$
    - probability distribution of $X$: &nbsp; $P_X(A) = P(\{\, o \in S \mid X(o) \in A \,\}) = P(X \in A)$ for $A \subseteq S_X$
    - $X$ is discrete if $S_X$ consists of countably many points, continuous if $S_X$ is uncountable + extra conditions (later)
    - pmf: $f_X(x) = P(X = x)$, with $f_X \geq 0$, $\sum_{x \in S_X} f_X(x) = 1$ and $\sum_{x \in A} f_X(x) = P(X \in A)$
    - cdf: $F_X(x) = P(X \leq x)$; for the largest face of two fair 4-sided dice, $F_X(k) - F_X(k - 1) = f_X(k)$

    **Next:** discrete random variables: pmf, cdf, expectation
    """)
    return


if __name__ == "__main__":
    app.run()

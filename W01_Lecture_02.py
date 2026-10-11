import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 02 · Properties of probability; counting methods", css_file="bs202.css")


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
def _(header):
    header("Lecture 02", "Week 01", "Lecture 02 · Properties of probability; counting methods")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Started Probability theory

    **random experiment** = repeatable, uncertain outcome whose *set of all outcomes* is defined &nbsp; $\leadsto$ &nbsp; sample space $S$

    **events in an experiment** = *collections of outcomes* (subsets $A \subseteq S$) *sharing some property* &nbsp; $\leadsto$ &nbsp; if outcome has property “$A$” we say “$A$ has occurred”
    """
            ),
            definition(
                r"""
    A **probability measure** in an experiment is a function $P$ that assigns probabilities to each event

    $$
    P : \mathcal{E} \longrightarrow \mathbb{R} \qquad (\mathcal{E}: \text{collection of all relevant events})
    $$

    $P$ must satisfy 3 axioms

    - $P(A) \geq 0 \quad \forall\, A \in \mathcal{E}$ &nbsp; (positivity)
    - $P(S) = 1$ &nbsp; (normalization)
    - for $A \cap B = \emptyset$, &nbsp; $P(A \cup B) = P(A) + P(B)$ &nbsp; (additivity)
    """
            ),
            mo.md(
                r"""
    To be precise, we need a bit more from additivity

    $$
    P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots \qquad \text{countable additivity}
    $$

    for $A_1, A_2, \dots$ (possibly infinite) *pairwise disjoint* &nbsp; ($A_i \cap A_j = \emptyset \ \ \forall\, i \neq j$)

    We won't need to be this precise.
    """
            ),
            definition(
                r"""
    We call a triple $(S, \mathcal{E}, P)$ a **probability space** &nbsp; $\leadsto$ &nbsp; a mathematical model for a random experiment
    """
            ),
            mo.md(
                r"""
    **Example** (Rolling a die).

    $$
    S = \{1, 2, 3, 4, 5, 6\}, \qquad \mathcal{E} = \big\{\, \emptyset, \{1\}, \{2\}, \dots, \{1, 2\}, \dots, \{1, 2, 3, 4, 5, 6\} \,\big\}
    $$

    For a “fair” die (extra assumption): &nbsp; $P(\{i\}) = P(\{j\}) \quad \forall\, i \neq j \in S$

    $$
    \text{axioms} \quad \Longrightarrow \quad P(\{i\}) = \tfrac{1}{6}, \quad P(\{i, j\}) = \tfrac{2}{6}, \quad P(\{i, j, k\}) = \tfrac{3}{6}, \ \dots
    \qquad \Longrightarrow \qquad P(A) = \frac{\# A}{\# S} \quad \forall\, A \in \mathcal{E}
    $$

    But not every die is fair…

    $$
    P(\{i\}) = \begin{cases} 0, & i \neq 6 \\ 1, & i = 6 \end{cases} \qquad \text{is also possible (different assumption)}
    $$

    $$
    \text{axioms} \quad \Longrightarrow \quad P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6 \\ 1, & i = 6 \text{ or } j = 6 \end{cases}
    \qquad \Longrightarrow \qquad P(A) = \begin{cases} 0, & 6 \notin A \\ 1, & 6 \in A \end{cases}
    $$

    Different probability measure on $(S, \mathcal{E})$ &nbsp; $\leadsto$ &nbsp; different mathematical model for the “dice experiment”
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, np):
    def venn_row(panels, three=False, width=9.6):
        """A row of small Venn diagrams. Each panel is (sign, region, colour, note);
        `region` is a function of the boolean grids A, B, C."""
        g = np.linspace(0, 1, 260)
        X, Y = np.meshgrid(g * 3.2, g * 2.4)
        circles = [((1.2, 1.45, 0.62), RED), ((2.0, 1.45, 0.62), GREEN)] + ([((1.6, 0.9, 0.62), BLUE)] if three else [])
        A, B = ((X - cx) ** 2 + (Y - cy) ** 2 < r**2 for (cx, cy, r), _ in circles[:2])
        C = (X - 1.6) ** 2 + (Y - 0.9) ** 2 < 0.62**2 if three else np.zeros_like(A)
        th = np.linspace(0, 2 * np.pi, 120)
        fig = Figure(figsize=(width, width / len(panels) * 0.95), layout="constrained")
        for ax, (sign, region, color, note) in zip(np.atleast_1d(fig.subplots(1, len(panels))), panels):
            ax.contourf(X, Y, region(A, B, C).astype(float), levels=[0.5, 1.5], colors=[color], alpha=0.55)
            for (cx, cy, r), col in circles:
                ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=col, lw=1.3)
            ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.4, 2.4, 0], color="black", lw=1.2)
            ax.text(-0.75, 1.2, sign, fontsize=18, ha="center", va="center")
            if note:
                ax.text(1.6, -0.35, note, fontsize=10, ha="center", color=GREEN)
            ax.set_xlim(-1.2, 3.3)
            ax.set_ylim(-0.6, 2.5)
            ax.set_aspect("equal")
            ax.axis("off")
        return fig

    return (venn_row,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, mo, np, theorem, venn_row):
    ORANGE = "#f5a623"
    _fig = Figure(figsize=(2.8, 1.9), layout="constrained")
    _ax = _fig.subplots()
    _th = np.linspace(0, 2 * np.pi, 100)
    _ax.plot(1.5 + 0.7 * np.cos(_th), 1.0 + 0.7 * np.sin(_th), color=RED, lw=1.6)
    _ax.plot([1.2, 1.9, 1.5, 1.2], [0.7, 0.75, 1.4, 0.7], color=GREEN, lw=1.6)
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 2, 2, 0], color=BLUE, lw=1.4)
    _ax.text(1.05, 1.1, "$A$", color=GREEN, fontsize=14)
    _ax.text(2.2, 1.6, "$B$", color=RED, fontsize=14)
    _ax.text(2.65, 0.12, "$S$", color=BLUE, fontsize=14)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(r"## Properties (axioms + algebra of events)"),
            mo.hstack(
                [
                    theorem(
                        r"""
    Given $A, B \in \mathcal{E}$

    1. $P(A^c) = 1 - P(A)$
    2. $P(\emptyset) = 0$
    3. if $A \subseteq B$ then $P(A) \leq P(B)$
    """
                    ),
                    mo.vstack([_fig, mo.md(r"$P$ is similar to “relative size” or “relative weight”")]),
                ],
                widths=[3, 2],
                gap=2,
                align="center",
                wrap=True,
            ),
            mo.md(
                r"""
    **Proof.**

    (i) &nbsp; $A \subseteq S \ \Longrightarrow \ A \cup A^c = S$ and $A \cap A^c = \emptyset$ &nbsp; $\Longrightarrow$ &nbsp; $P(A \cup A^c) = 1 = P(A) + P(A^c)$

    (ii) &nbsp; $A = S \ \Longrightarrow \ A^c = S^c = \emptyset$ &nbsp; $\Longrightarrow$ &nbsp; $P(S \cup \emptyset) = 1 = P(S) + P(\emptyset)$ &nbsp; $\Longrightarrow$ &nbsp; $P(\emptyset) = 0$

    (iii) &nbsp; $A \subseteq B \ \Longrightarrow \ B = (B \cap A) \cup (B \cap A^c) = A \cup (B \cap A^c)$ &nbsp; with $A \cap (B \cap A^c) = \emptyset$ &nbsp; ($A \cap (A^c \cap B) = (A \cap A^c) \cap B$)

    $$
    \Longrightarrow \quad P(B) = P(A) + \underbrace{P(B \cap A^c)}_{\geq\, 0} \geq P(A)
    $$
    """
            ),
            theorem(
                r"""
    For $A, B \in \mathcal{E}$

    $$
    P(A \cup B) = P(A) + P(B) - P(A \cap B)
    $$
    """
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $A \cup B = A \cup (A^c \cap B)$ &nbsp; (with $A \cap (B \cap A^c) = \emptyset$) &nbsp; $\Longrightarrow$ &nbsp; $P(A \cup B) = P(A) + P(A^c \cap B)$

    $(A^c \cap B) \cup (A \cap B) = B$ &nbsp; (with $(A^c \cap B) \cap (A \cap B) = \emptyset$) &nbsp; $\Longrightarrow$ &nbsp; $P(A^c \cap B) + P(A \cap B) = P(B)$

    $$
    \Longrightarrow \quad P(A \cup B) = P(A) + P(B) - P(A \cap B)
    $$
    """
            ),
            venn_row(
                [
                    ("", lambda A, B, C: A | B, ORANGE, ""),
                    ("$=$", lambda A, B, C: A, RED, ""),
                    ("$+$", lambda A, B, C: B, GREEN, ""),
                    ("$-$", lambda A, B, C: A & B, ORANGE, "added 2 times"),
                ],
                width=8.4,
            ),
            theorem(
                r"""
    For $A, B, C \in \mathcal{E}$

    $$
    \begin{aligned}
    P(A \cup B \cup C) = {} & P(A) + P(B) + P(C) \\
    & - P(A \cap B) - P(A \cap C) - P(B \cap C) \\
    & + P(A \cap B \cap C)
    \end{aligned}
    $$
    """
            ),
            venn_row(
                [
                    ("", lambda A, B, C: A | B | C, ORANGE, ""),
                    ("$=$", lambda A, B, C: A, RED, ""),
                    ("$+$", lambda A, B, C: B, GREEN, ""),
                    ("$+$", lambda A, B, C: C, BLUE, ""),
                ],
                three=True,
                width=8.4,
            ),
            venn_row(
                [
                    ("$-$", lambda A, B, C: A & B, BLUE, "added 2 times"),
                    ("$-$", lambda A, B, C: A & C, GREEN, "added 2 times"),
                    ("$-$", lambda A, B, C: B & C, RED, "added 2 times"),
                    ("$+$", lambda A, B, C: A & B & C, ORANGE, "added and subtracted 3 times"),
                ],
                three=True,
                width=8.4,
            ),
            mo.md(
                r"""
    **Example** (Roll two fair dice).

    $$
    S = \{(1, 1), (1, 2), \dots, (6, 6)\}, \qquad A = \{\text{1st is odd}\}, \quad B = \{\text{2nd is odd}\}, \quad C = \{\text{sum is 7}\}
    $$

    $$
    P(A \cup B \cup C) = \frac{3 \times 6}{36} + \frac{3 \times 6}{36} + \frac{6}{36} - \frac{3 \times 3}{36} - \frac{3}{36} - \frac{3}{36} + 0 = \frac{27}{36} = \frac{3}{4}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    ie_sum = mo.ui.slider(2, 12, 1, value=7, label="$C$: sum is", show_value=True)
    return (ie_sum,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, ie_sum, mo):
    _t = ie_sum.value
    _fig = Figure(figsize=(4.0, 4.0), layout="constrained")
    _ax = _fig.subplots()
    _A, _B, _C = set(), set(), set()
    for _i in range(1, 7):
        for _j in range(1, 7):
            if _i % 2 == 1:
                _A.add((_i, _j))
                _ax.plot(_i, _j, "o", ms=19, mfc="none", mec=RED, mew=1.6)
            if _j % 2 == 1:
                _B.add((_i, _j))
                _ax.plot(_i, _j, "s", ms=14, mfc="none", mec=GREEN, mew=1.6)
            if _i + _j == _t:
                _C.add((_i, _j))
                _ax.plot(_i, _j, "D", ms=8, mfc="none", mec=BLUE, mew=1.6)
            _ax.plot(_i, _j, "o", ms=3, color="#555555")
    _ax.set_xlim(0.3, 6.7)
    _ax.set_ylim(0.3, 6.7)
    _ax.set_aspect("equal")
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks(range(1, 7))
    _ax.set_xlabel("first die")
    _ax.set_ylabel("second die")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _n = [len(_A), len(_B), len(_C), len(_A & _B), len(_A & _C), len(_B & _C), len(_A & _B & _C)]
    _union = len(_A | _B | _C)
    _rhs = _n[0] + _n[1] + _n[2] - _n[3] - _n[4] - _n[5] + _n[6]
    mo.vstack(
        [
            ie_sum,
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        rf"$\textcolor{{{RED}}}{{A}}$ (circles), &nbsp; $\textcolor{{{GREEN}}}{{B}}$ (squares), &nbsp; $\textcolor{{{BLUE}}}{{C}}$ (diamonds)"
                        + "\n\n"
                        + rf"$P(A \cup B \cup C) = \frac{{{_n[0]}}}{{36}} + \frac{{{_n[1]}}}{{36}} + \frac{{{_n[2]}}}{{36}} - \frac{{{_n[3]}}}{{36}} - \frac{{{_n[4]}}}{{36}} - \frac{{{_n[5]}}}{{36}} + \frac{{{_n[6]}}}{{36}} = \frac{{{_rhs}}}{{36}}$"
                        + "\n\n"
                        + rf"check by counting the marked points: &nbsp; $\#(A \cup B \cup C) = {_union}$"
                    ),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
                wrap=True,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    If $S = \{o_1, \dots, o_n\}$ is finite and $P(\{o_i\}) = P(\{o_j\}) \quad \forall\, i, j \in \{1, \dots, n\}$ we say $(S, \mathcal{E}, P)$ has **equally likely outcomes**.
    """
            ),
            theorem(
                r"""
    If $(S, \mathcal{E}, P)$ has equally likely outcomes (very strong assumption!)

    $$
    P(A) = \frac{\# A}{\# S}
    $$
    """
            ),
            mo.md(
                r"""
    Probability becomes a counting problem!

    ## 2 &nbsp; Counting methods (WMS 2.6)
    """
            ),
            theorem(
                r"""
    Given a set with $m$ elements $\{a_1, \dots, a_m\}$ and another set with $n$ elements $\{b_1, \dots, b_n\}$ there are exactly $m \cdot n$ possible ordered pairs $(a_i, b_j)$.
    """,
                "Multiplication rule",
            ),
            mo.md(
                r"""
    **Proof.** Think of elements $a_i$ as labels of rows and elements $b_j$ as labels of columns of a matrix &nbsp; $\Longrightarrow$ &nbsp; $(a_i, b_j)$ labels its entries &nbsp; (not a proof… just verification)

    **Example** (Flipping a coin and rolling a die).

    $$
    S = \{(H, 1), (H, 2), \dots, (H, 6), (T, 1), \dots, (T, 6)\} \quad \Longrightarrow \quad \# S = 12 = 2 \times 6
    $$

    Useful to count total number of outcomes on random experiments with *successive stages* (1st the coin, then the die).

    **Remark.** The rule easily extends to more than two sets

    $$
    \text{e.g.} \quad \# A = m, \ \# B = n, \ \# C = p \quad \Longrightarrow \quad \#(A \times B \times C) = m\, n\, p \qquad (\text{ordered triples})
    $$

    **Example** (ordered hands of poker).

    $S = \{\, (A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit),\ (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit),\ \dots \,\}$ &nbsp; (distinct ordered hands)

    $$
    \begin{aligned}
    \# S &= \underbrace{\#(\text{1st card})}_{\text{1st stage}}\ \underbrace{\#(\text{2nd card})}_{\text{2nd stage}} \cdots \underbrace{\#(\text{5th card})}_{\text{5th stage}} \\
    &= 52 \cdot 51 \cdot 50 \cdot 49 \cdot 48 = \frac{52!}{47!} = P^{52}_{5}
    \end{aligned}
    $$

    $P^{52}_5 = \#(\text{orderings of 52 objects taken 5 at a time})$ &nbsp; (orderings: arrangements or permutations)
    """
            ),
            theorem(
                r"""
    Given $n$ objects and $r$ positions

    $$
    P^n_r = \frac{n!}{(n - r)!} = n \cdot (n - 1) \cdot (n - 2) \cdots (n - r + 1) \qquad \text{number of orderings}
    $$
    """
            ),
            mo.md(
                r"""
    **Example** (real hands of poker: unordered).

    If we don't care about order

    $(A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit) = (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit) = (2\heartsuit, 3\spadesuit, 5\diamondsuit, A\diamondsuit, 4\clubsuit) = \cdots$

    $\leadsto$ &nbsp; $P^{52}_5$ over-counts the hands!
    """
            ),
            theorem(
                r"""
    $$
    C^n_r = \#(\text{combinations of } n \text{ objects taken } r \text{ at a time}) = \frac{P^n_r}{r!} = \frac{n!}{r!\,(n - r)!} = \binom{n}{r}
    $$

    (combinations: unordered arrangements)
    """
            ),
            mo.md(
                r"""
    $\binom{n}{r}$: binomial coefficients &nbsp; $\leadsto$ &nbsp; binomial expansion &nbsp; $(a + b)^n = \displaystyle\sum_{r=0}^{n} \binom{n}{r} a^r b^{n-r}$

    **Proof** (using hands of poker).

    $$
    \underbrace{\#\left(\substack{\text{ordered} \\ \text{hands}}\right)}_{\text{deal ordered}} = \underbrace{\#\left(\substack{\text{unordered} \\ \text{hands}}\right)}_{\text{1st stage: deal unordered}}\ \underbrace{\#\left(\substack{\text{ways of ordering} \\ \text{one hand}}\right)}_{\text{2nd stage: order the hand}}
    $$

    $$
    \#\left(\substack{\text{ordered} \\ \text{hands}}\right) = P^{52}_5, \qquad \#\left(\substack{\text{unordered} \\ \text{hands}}\right) = C^{52}_5 = \ ?
    $$

    $$
    \#\left(\substack{\text{ways of ordering} \\ \text{one hand (5 cards)}}\right) = \#(\text{1st})\, \#(\text{2nd})\, \#(\text{3rd})\, \#(\text{4th})\, \#(\text{5th}) = 5 \cdot 4 \cdot 3 \cdot 2 \cdot 1 = 5!
    $$

    $$
    \Longrightarrow \quad P^{52}_5 = C^{52}_5 \cdot 5!
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    cn = mo.ui.slider(1, 52, 1, value=52, label="$n$", show_value=True)
    cr = mo.ui.slider(0, 10, 1, value=5, label="$r$", show_value=True)
    return cn, cr


@app.cell(hide_code=True)
def _(cn, cr, math, mo):
    _n, _r = cn.value, cr.value
    _fmt = lambda k: f"{k:,}".replace(",", r"\,")
    if _r > _n:
        _text = mo.md(rf"need $r \le n$ &nbsp; (here $r = {_r} > n = {_n}$)")
    else:
        _text = mo.md(
            "\n".join(
                [
                    "| | |",
                    "|:--|--:|",
                    rf"| orderings $P^n_r$ | ${_fmt(math.perm(_n, _r))}$ |",
                    rf"| $r!$ | ${_fmt(math.factorial(_r))}$ |",
                    rf"| combinations $C^n_r$ | ${_fmt(math.comb(_n, _r))}$ |",
                    rf"| arrangements with replacement $n^r$ | ${_fmt(_n**_r)}$ |",
                    rf"| combinations with replacement $\binom{{n + r - 1}}{{r}}$ | ${_fmt(math.comb(_n + _r - 1, _r))}$ |",
                ]
            )
        )
    mo.vstack([mo.hstack([cn, cr], justify="start", gap=3), _text])
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Example** (probability of a hand of poker).

    $$
    S = \{\text{unordered hands}\}, \qquad A = \{\text{all cards of same suit}\}
    $$

    $$
    \leadsto \quad \# A = \#(\text{suits}) \cdot \#\left(\substack{\text{hands of} \\ \text{given suit}}\right) = 4 \cdot C^{13}_5 = 4 \cdot \frac{13!}{5!\, 8!} = \cdots = 4 \cdot 1287 = 5148
    $$

    $$
    \leadsto \quad \# S = C^{52}_5 = 2\,598\,960 \qquad \Longrightarrow \qquad P(A) = \frac{\# A}{\# S} \approx 0.002 = 0.2\%
    $$

    **Example** (defective items).

    20 items, 3 defective &nbsp; $\leadsto$ &nbsp; pick 4 items (samples)

    $$
    P(\text{at least one is defective}) = \ ?
    $$

    Counting combinations of 1 defective plus 2 defective plus 3 defective is hard…

    $$
    \{\text{at least one defective}\} = \{\text{none defective}\}^c
    $$

    Counting combinations of none defective is much easier!

    $$
    \#\{\text{none defective}\} = C^{17}_4 = \frac{17!}{4!\, 13!}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad P(\text{at least one}) &= 1 - P(\text{none}) \\
    &= 1 - \frac{C^{17}_4}{C^{20}_4} = 1 - \underbrace{\frac{17!}{20!} \frac{16!}{13!}}_{\textstyle \frac{16 \cdot 15 \cdot 14}{20 \cdot 19 \cdot 18}} \approx 50.9\%
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    d_items = mo.ui.slider(5, 50, 1, value=20, label="items", show_value=True)
    d_def = mo.ui.slider(0, 10, 1, value=3, label="defective", show_value=True)
    d_pick = mo.ui.slider(1, 10, 1, value=4, label="picked", show_value=True)
    return d_def, d_items, d_pick


@app.cell(hide_code=True)
def _(d_def, d_items, d_pick, math, mo):
    _n, _d, _k = d_items.value, d_def.value, d_pick.value
    if _d > _n or _k > _n:
        _text = mo.md(rf"need $\text{{defective}} \le \text{{items}}$ and $\text{{picked}} \le \text{{items}}$ &nbsp; (here items $= {_n}$)")
    else:
        _p = 1 - math.comb(_n - _d, _k) / math.comb(_n, _k)
        _text = mo.md(
            "\n".join(
                [
                    "| | |",
                    "|:--|--:|",
                    rf"| $\#\{{\text{{none defective}}\}}$ | ${math.comb(_n - _d, _k):,}$ |".replace(",", r"\,"),
                    rf"| $\# S$ | ${math.comb(_n, _k):,}$ |".replace(",", r"\,"),
                    rf"| $P(\text{{at least one}}) = 1 - P(\text{{none}})$ | ${100 * _p:.1f}\%$ |",
                ]
            )
        )
    mo.vstack([mo.hstack([d_items, d_def, d_pick], justify="start", gap=3, wrap=True), _text])
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    So far, arrangements and combinations of objects *without replacement* &nbsp; (once an object is selected it cannot be selected again)
    """
            ),
            theorem(
                r"""
    Given $n$ objects and $r$ positions

    $$
    n^r = \#\, \text{arrangements with replacement} = \underbrace{\#\left(\substack{\text{choices in} \\ \text{1st position}}\right)}_{n}\ \underbrace{\#\left(\substack{\text{choices in} \\ \text{2nd position}}\right)}_{n} \cdots \underbrace{\#\left(\substack{\text{choices in} \\ r\text{th position}}\right)}_{n}
    $$

    $$
    \binom{n + r - 1}{r} = \#\, \text{combinations with replacement}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def _field():
        return mo.ui.text(placeholder="?", debounce=True)

    w1, w2, w3, w4 = _field(), _field(), _field(), _field()
    return w1, w2, w3, w4


@app.cell(hide_code=True)
def _(mo, w1, w2, w3, w4):
    def _mark(field, answer, tol):
        s = field.value.strip().replace(",", ".").rstrip("%")
        if not s:
            return ""
        try:
            v = float(s) / (100 if field.value.strip().endswith("%") else 1)
        except ValueError:
            return "⚠️ enter a number"
        return "✅" if abs(v - answer) <= tol else "❌ try again"

    def _ask(label, field, answer, tol):
        return mo.hstack([mo.md(label), field, mo.md(_mark(field, answer, tol))], justify="start", align="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice W01

    ### Question 1

    Roll 3 fair dice. What is the probability that at least one is 6?
    """
            ),
            _ask("probability (decimal) $=$", w1, 1 - (5 / 6) ** 3, 0.005),
            mo.md(
                r"""
    ### Question 2

    A committee of 5 people is chosen from 8 blue, 6 red. Assuming each selection is equally likely, what is the probability that exactly two are red?
    """
            ),
            _ask("probability (decimal) $=$", w2, 15 * 56 / 2002, 0.005),
            mo.md(
                r"""
    ### Question 3

    Count the possibilities of

    (a) seating 5 people on 5 chairs
    """
            ),
            _ask("number $=$", w3, 120, 1e-6),
            mo.md(r"(b) choosing 3 ice-cream flavours from 12"),
            _ask("number $=$", w4, 220, 1e-6),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

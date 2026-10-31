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
    header("Lecture 02", "Week 01", "Lecture 02 • Properties of probability; counting methods")
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
    mo.md(r"""
    ## Last time

    - started Probability theory
    - **random experiment** = repeatable, uncertain outcome whose set of all outcomes is defined &nbsp; <span class="nw">$\leadsto$ &nbsp; sample</span> space $S$
    - **events in an experiment** = collections of outcomes (subsets $A \subseteq S$) sharing some property &nbsp; <span class="nw">$\leadsto$ &nbsp; if</span> the outcome has property “$A$” we say “$A$ has occurred”
    - a **probability measure** in an experiment is a function $P : \mathcal{E} \longrightarrow \mathbb{R}$ that assigns probabilities to each event ($\mathcal{E}$: collection of all relevant events); $P$ must satisfy 3 axioms

        $$
        \begin{aligned}
        & P(A) \geq 0 \quad \forall\, A \in \mathcal{E} && \text{positivity} \\
        & P(S) = 1 && \text{normalization} \\
        & P(A \cup B) = P(A) + P(B) \ \text{ for } A \cap B = \emptyset && \text{additivity}
        \end{aligned}
        $$

    - to be precise, we need a bit more from additivity (**countable additivity**; we won't need to be this precise)

        <span class="chain">$\displaystyle P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots$ $\displaystyle \quad \text{for } \underbrace{A_1, A_2, \dots}_{\mathclap{\footnotesize \text{possibly infinite}}} \text{ pairwise disjoint}$ $\displaystyle \quad (A_i \cap A_j = \emptyset \ \ \forall\, i \neq j)$</span>

    - we call a triple $(S, \mathcal{E}, P)$ a **probability space** &nbsp; <span class="nw">$\leadsto$ &nbsp; a</span> mathematical model for a random experiment
    - rolling a die:

        $$
        \begin{aligned}
        S &= \{1, 2, 3, 4, 5, 6\} \\
        \mathcal{E} &= \big\{ \emptyset, \{1\}, \{2\}, \dots, \{1, 2\}, \dots, \{1, 2, 3, 4, 5, 6\} \big\}
        \end{aligned}
        $$

        for a “fair” die (extra assumption):

        $$
        P(\{i\}) = P(\{j\}) \quad \forall\, i \neq j \in S
        $$

        <span class="chain">$\displaystyle \text{axioms} \ \Longrightarrow \ \ P(\{i\}) = \frac{1}{6},$ $\displaystyle \quad P(\{i, j\}) = \frac{2}{6},$ $\displaystyle \quad P(\{i, j, k\}) = \frac{3}{6}, \ \dots$ $\displaystyle \quad \Longrightarrow \quad P(A) = \frac{\# A}{\# S} \quad \forall\, A \in \mathcal{E}$</span>

    - but not every die is fair… a different assumption is also possible

        <span class="chain">$\displaystyle P(\{i\}) = \begin{cases} 0, & i \neq 6 \\ 1, & i = 6 \end{cases}$ $\displaystyle \quad \text{axioms} \ \Longrightarrow \quad P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6 \\ 1, & i = 6 \text{ or } j = 6 \end{cases}$ $\displaystyle \quad \Longrightarrow \quad P(A) = \begin{cases} 0, & 6 \notin A \\ 1, & 6 \in A \end{cases}$</span>

        different probability measure on $(S, \mathcal{E})$ &nbsp; <span class="nw">$\leadsto$ &nbsp; different</span> mathematical model for the “dice experiment”

    **In this lecture:** properties of probability (axioms + algebra of events) and counting methods

    **References:** WMS 2.5, 2.6, 2.8
    """)
    return


@app.cell(hide_code=True)
def _(Arc, BLUE, FULL, Figure, LIGHT, ORANGE, RED, np):
    def venn_row(panels, three=False):
        """A row of four small Venn diagrams of A (blue), B (red) and, when `three`, C (orange).
        Each panel is (sign, region, remark): `region` is a function of the boolean grids A, B, C
        and is filled; `sign` is written to the left of the panel and `remark` below it."""
        g = np.linspace(0, 1, 700)
        X, Y = np.meshgrid(g * 3.2, g * 2.4)
        cy = 1.5 if three else 1.2
        circles = [((1.2, cy, 0.62), BLUE, "$A$", (0.3, 2.06)), ((2.0, cy, 0.62), RED, "$B$", (2.9, 2.06))]
        if three:
            circles.append(((1.6, 0.85, 0.62), ORANGE, "$C$", (2.55, 0.34)))
        inside = [(X - cx) ** 2 + (Y - c_y) ** 2 < r**2 for (cx, c_y, r), *_ in circles]
        if not three:
            inside.append(np.zeros_like(inside[0]))
        fig = Figure(figsize=(FULL, 1.75), layout="constrained")
        for ax, (sign, region, remark) in zip(fig.subplots(1, len(panels)), panels):
            ax.contourf(X, Y, region(*inside).astype(float), levels=[0.5, 1.5], colors=[LIGHT])
            for (cx, c_y, r), col, name, at in circles:
                ax.add_patch(Arc((cx, c_y), 2 * r, 2 * r, color=col, lw=1.2))
                ax.text(*at, name, color=col, fontsize=14, ha="center", va="center")
            ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.4, 2.4, 0], color="black", lw=1.0, solid_joinstyle="miter")
            ax.text(-0.62, 1.2, sign, fontsize=14, ha="center", va="center")
            ax.text(1.6, -0.2, remark, fontsize=13, ha="center", va="top", linespacing=1.1)
            ax.set_xlim(-1.15, 3.3)
            ax.set_ylim(-1.2, 2.5)
            ax.set_aspect("equal")
            ax.axis("off")
        return fig

    return (venn_row,)


@app.cell(hide_code=True)
def _(Arc, BLUE, HALF, RED, blank, mo, theorem, venn_row):
    _fig, _ax = blank(HALF, 2.3, (-0.1, 3.1), (-0.1, 2.1))
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 2, 2, 0], color="black", lw=1.0, solid_joinstyle="miter")
    _ax.add_patch(Arc((1.5, 1.0), 1.4, 1.4, color=RED, lw=1.2))
    _ax.plot([1.2, 1.9, 1.5, 1.2], [0.7, 0.75, 1.4, 0.7], color=BLUE, lw=1.2, solid_joinstyle="miter")
    _ax.text(1.53, 0.95, "$A$", color=BLUE, fontsize=15, ha="center", va="center")
    _ax.text(2.3, 1.62, "$B$", color=RED, fontsize=15, ha="center", va="center")
    _ax.text(2.75, 0.25, "$S$", fontsize=15, ha="center", va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.2 &nbsp; Properties of probability; counting methods

    ### Properties (axioms + algebra of events)
    """
            ),
            theorem(
                r"""
    Given $A, B \in \mathcal{E}$

    (i) &nbsp; $P(A^c) = 1 - P(A)$

    (ii) &nbsp; $P(\emptyset) = 0$

    (iii) &nbsp; if $A \subseteq B$ then $P(A) \leq P(B)$
    """,
                "Basic properties",
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; $P$ is similar to “relative size” or “relative weight”

    **Proof.**

    (i) &nbsp; $A \subseteq S \ \Longrightarrow \ A \cup A^c = S$ and $A \cap A^c = \emptyset$

    $$
    \Longrightarrow \qquad P(A \cup A^c) = 1 = P(A) + P(A^c)
    $$

    (ii) &nbsp; $A = S \ \Longrightarrow \ A^c = S^c = \emptyset$

    $$
    \Longrightarrow \qquad P(S \cup \emptyset) = 1 = P(S) + P(\emptyset) \qquad \Longrightarrow \qquad P(\emptyset) = 0
    $$

    (iii) &nbsp; $A \subseteq B \ \Longrightarrow \ B = (B \cap A) \cup (B \cap A^c) = A \cup (B \cap A^c)$

    $$
    \text{with} \quad A \cap (B \cap A^c) = \emptyset \qquad \big(\text{since } A \cap (A^c \cap B) = (A \cap A^c) \cap B\big)
    $$

    $$
    \Longrightarrow \qquad P(B) = P(A) + \underbrace{P(B \cap A^c)}_{\footnotesize \geq 0} \geq P(A) \tag*{$\square$}
    $$
    """
            ),
            theorem(
                r"""
    For $A, B \in \mathcal{E}$

    $$
    P(A \cup B) = P(A) + P(B) - P(A \cap B)
    $$
    """,
                "Probability of a union of two events",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $A \cup B = A \cup (A^c \cap B)$ &nbsp; (with $A \cap (B \cap A^c) = \emptyset$)

    $$
    \Longrightarrow \qquad P(A \cup B) = P(A) + P(A^c \cap B)
    $$

    $(A^c \cap B) \cup (A \cap B) = B$ &nbsp; (with $(A^c \cap B) \cap (A \cap B) = \emptyset$)

    $$
    \Longrightarrow \qquad P(A^c \cap B) + P(A \cap B) = P(B)
    $$

    $$
    \Longrightarrow \qquad P(A \cup B) = P(A) + P(B) - P(A \cap B) \tag*{$\square$}
    $$
    """
            ),
            venn_row(
                [
                    ("", lambda A, B, C: A | B, ""),
                    ("$=$", lambda A, B, C: A, ""),
                    ("$+$", lambda A, B, C: B, ""),
                    ("$-$", lambda A, B, C: A & B, "added 2 times"),
                ]
            ),
            theorem(
                r"""
    For $A, B, C \in \mathcal{E}$

    <span class="chain">$\displaystyle P(A \cup B \cup C) = P(A) + P(B) + P(C)$ $\displaystyle {} - P(A \cap B) - P(A \cap C) - P(B \cap C)$ $\displaystyle {} + P(A \cap B \cap C)$</span>
    """,
                "Probability of a union of three events",
            ),
            venn_row(
                [
                    ("", lambda A, B, C: A | B | C, ""),
                    ("$=$", lambda A, B, C: A, ""),
                    ("$+$", lambda A, B, C: B, ""),
                    ("$+$", lambda A, B, C: C, ""),
                ],
                three=True,
            ),
            venn_row(
                [
                    ("$-$", lambda A, B, C: A & B, "added 2 times"),
                    ("$-$", lambda A, B, C: A & C, "added 2 times"),
                    ("$-$", lambda A, B, C: B & C, "added 2 times"),
                    ("$+$", lambda A, B, C: A & B & C, "added and\nsubtracted 3 times"),
                ],
                three=True,
            ),
            mo.md(
                r"""
    **Example** (Roll two fair dice).

    $$
    \begin{gathered}
    S = \{(1, 1), (1, 2), \dots, (6, 6)\} \\
    A = \{\text{1st is odd}\}, \quad B = \{\text{2nd is odd}\}, \quad C = \{\text{sum is 7}\}
    \end{gathered}
    $$

    <span class="chain">$\displaystyle P(A \cup B \cup C) = \frac{3 \times 6}{36} + \frac{3 \times 6}{36} + \frac{6}{36} - \frac{3 \times 3}{36} - \frac{3}{36} - \frac{3}{36} + 0$ $\displaystyle = \frac{27}{36} = \frac{3}{4}$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, ORANGE, RED, mo):
    _fig = Figure(figsize=(4.4, 4.4), layout="constrained")
    _ax = _fig.subplots()
    for _i in (1, 3, 5):
        _ax.axvspan(_i - 0.4, _i + 0.4, ymin=0.06, ymax=0.92, color=BLUE, alpha=0.18, lw=0)
    for _j in (1, 3, 5):
        _ax.fill_between([0.6, 6.4], _j - 0.4, _j + 0.4, color=RED, alpha=0.18, lw=0)
    _ax.plot([0.7, 6.3], [6.3, 0.7], color=ORANGE, lw=1.6)
    for _i in range(1, 7):
        for _j in range(1, 7):
            _in = _i % 2 == 1 or _j % 2 == 1 or _i + _j == 7
            _ax.plot(_i, _j, "o", ms=6, color="black" if _in else "white", mec="black", mew=1, zorder=3)
    _ax.text(1, 6.65, "$A$", color=BLUE, ha="center", fontsize=14)
    _ax.text(6.55, 5, "$B$", color=RED, va="center", fontsize=14)
    _ax.text(6.35, 0.45, "$C$", color=ORANGE, va="center", fontsize=14)
    _ax.set_xlim(0.3, 6.9)
    _ax.set_ylim(0.2, 6.9)
    _ax.set_aspect("equal")
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks(range(1, 7))
    _ax.set_xlabel("first die", fontsize=12)
    _ax.set_ylabel("second die", fontsize=12)
    _ax.set_title(r"$A \cup B \cup C$: 27 of 36 outcomes", fontsize=14)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    mo.as_html(_fig)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Equally likely outcomes"""),
            definition(
                r"""
    If $S = \{o_1, \dots, o_n\}$ is finite and

    $$
    P(\{o_i\}) = P(\{o_j\}) \qquad \forall\, i, j \in \{1, \dots, n\}
    $$

    we say $(S, \mathcal{E}, P)$ has **equally likely outcomes**.
    """,
                "Equally likely outcomes",
            ),
            theorem(
                r"""
    If $(S, \mathcal{E}, P)$ has equally likely outcomes (very strong assumption!)

    $$
    P(A) = \frac{\# A}{\# S}
    $$
    """,
                "Probability by counting",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; probability becomes a counting problem!

    ### Counting methods
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
    **Proof.** Think of elements $a_i$ as labels of rows and elements $b_j$ as labels of columns of a matrix &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; $(a_i, b_j)$</span> labels its entries &nbsp; (not a proof… just verification)

    **Example** (Flipping a coin and rolling a die).

    <span class="chain">$\displaystyle S = \{(H, 1), (H, 2), \dots, (H, 6), (T, 1), \dots, (T, 6)\}$ $\displaystyle \quad \Longrightarrow \quad \# S = 12 = 2 \times 6$</span>

    $\leadsto$ &nbsp; useful to count total number of outcomes on random experiments with **successive stages** (1st the coin, then the die)

    **Remark.** The rule easily extends to more than two sets

    <span class="chain">$\displaystyle \text{e.g.} \quad \# A = m, \ \# B = n, \ \# C = p$ $\displaystyle \quad \Longrightarrow \quad \#(\underbrace{A \times B \times C}_{\mathclap{\footnotesize \text{ordered triples}}}) = m\, n\, p$</span>

    **Example** (ordered hands of poker).

    $$
    S = \{\, \underbrace{(A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit),\ (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit)}_{\footnotesize \text{distinct ordered hands}},\ \dots \,\}
    $$

    <span class="chain">$\displaystyle \# S = \underbrace{\#(\text{1st card})}_{\footnotesize \text{1st stage}}\ \underbrace{\#(\text{2nd card})}_{\footnotesize \text{2nd stage}} \cdots \underbrace{\#(\text{5th card})}_{\footnotesize \text{5th stage}}$ $\displaystyle = 52 \cdot 51 \cdot 50 \cdot 49 \cdot 48 = \frac{52!}{47!} = P^{52}_{5}$</span>

    $$
    P^{52}_5 = \#(\text{orderings of 52 objects taken 5 at a time})
    $$

    (orderings: arrangements or permutations)
    """
            ),
            theorem(
                r"""
    Given $n$ objects and $r$ positions

    <span class="chain">$\displaystyle P^n_r = \frac{n!}{(n - r)!}$ $\displaystyle = n \cdot (n - 1) \cdot (n - 2) \cdots (n - r + 1)$ $\displaystyle \qquad \text{number of orderings}$</span>
    """,
                "Number of orderings",
            ),
            mo.md(
                r"""
    **Example** (real hands of poker: unordered).

    If we don't care about order

    <span class="chain">$\displaystyle (A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit) = (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit)$ $\displaystyle = (2\heartsuit, 3\spadesuit, 5\diamondsuit, A\diamondsuit, 4\clubsuit) = \cdots$</span>

    $\leadsto$ &nbsp; $P^{52}_5$ over-counts the hands!
    """
            ),
            theorem(
                r"""
    <span class="chain">$\displaystyle C^n_r = \#(\text{combinations of } n \text{ objects taken } r \text{ at a time})$ $\displaystyle = \frac{P^n_r}{r!} = \frac{n!}{r!\,(n - r)!} = \binom{n}{r}$</span>

    (combinations: unordered arrangements)
    """,
                "Number of combinations",
            ),
            mo.md(
                r"""
    $\dbinom{n}{r}$: binomial coefficients &nbsp; <span class="nw">$\leadsto$ &nbsp; binomial</span> expansion

    $$
    (a + b)^n = \sum_{r=0}^{n} \binom{n}{r} a^r b^{n-r}
    $$

    **Proof** (using hands of poker).

    <span class="chain">$\displaystyle \underbrace{\#(\text{ordered hands})}_{\footnotesize \text{deal ordered}} = \underbrace{\#(\text{unordered hands})}_{\footnotesize \text{1st stage: deal unordered}}$ $\displaystyle {} \cdot \underbrace{\#(\text{ways of ordering one hand})}_{\footnotesize \text{2nd stage: order the hand}}$</span>

    $$
    \#(\text{ordered hands}) = P^{52}_5, \qquad \#(\text{unordered hands}) = C^{52}_5 = \ ?
    $$

    <span class="chain">$\displaystyle \#(\text{ways of ordering one hand (5 cards)})$ $\displaystyle = \#(\text{1st})\, \#(\text{2nd})\, \#(\text{3rd})\, \#(\text{4th})\, \#(\text{5th})$ $\displaystyle = 5 \cdot 4 \cdot 3 \cdot 2 \cdot 1 = 5!$</span>

    $$
    \Longrightarrow \qquad P^{52}_5 = C^{52}_5 \cdot 5! \tag*{$\square$}
    $$
    """
            ),
        ], gap=1.5
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example** (probability of a hand of poker).

    $$
    S = \{\text{unordered hands}\}, \qquad A = \{\text{all cards of same suit}\}
    $$

    <span class="chain">$\displaystyle \leadsto \quad \# A = \#(\text{suits}) \cdot \#(\text{hands of given suit})$ $\displaystyle = 4 \cdot C^{13}_5 = 4 \cdot \frac{13!}{5!\, 8!}$ $\displaystyle = \cdots = 4 \cdot 1287 = 5148$</span>

    $$
    \begin{aligned}
    \leadsto \quad \# S & = C^{52}_5 = 2\,598\,960 \\[1em]
    \Longrightarrow \quad P(A) & = \frac{\# A}{\# S} \approx 0.002 = 0.2\%
    \end{aligned}
    $$

    **Example** (defective items).

    20 items, 3 defective &nbsp; <span class="nw">$\leadsto$ &nbsp; pick</span> 4 items (samples)

    $$
    P(\text{at least one is defective}) = \ ?
    $$

    $\leadsto$ &nbsp; counting combinations of 1 defective plus 2 defective plus 3 defective is hard…

    $$
    \{\text{at least one defective}\} = \{\text{none defective}\}^c
    $$

    $\leadsto$ &nbsp; counting combinations of none defective is much easier!

    $$
    \#\{\text{none defective}\} = C^{17}_4 = \frac{17!}{4!\, 13!}
    $$

    <span class="chain">$\displaystyle \Longrightarrow \quad P(\text{at least one}) = 1 - P(\text{none}) = 1 - \frac{C^{17}_4}{C^{20}_4}$ $\displaystyle = 1 - \frac{17!}{20!} \frac{16!}{13!}$ $\displaystyle = 1 - \frac{16 \cdot 15 \cdot 14}{20 \cdot 19 \cdot 18} \approx 50.9\%$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; so far, arrangements and combinations of objects **without replacement** &nbsp; (once an object is selected it cannot be selected again)
    """
            ),
            theorem(
                r"""
    Given $n$ objects and $r$ positions

    <span class="chain">$\displaystyle n^r = \#\, \text{arrangements with replacement}$ $\displaystyle = \underbrace{\#(\text{choices in 1st position})}_{\footnotesize n}\ \underbrace{\#(\text{choices in 2nd position})}_{\footnotesize n}$ $\displaystyle \cdots \underbrace{\#(\text{choices in } r\text{th position})}_{\footnotesize n}$</span>

    $$
    \binom{n + r - 1}{r} = \#\, \text{combinations with replacement}
    $$
    """,
                "Arrangements and combinations with replacement",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    ### Question 1

    Roll 3 fair dice. What is the probability that at least one is 6?

    ### Question 2

    A committee of 5 people is chosen from 8 blue, 6 red. Assuming each selection is equally likely, what is the probability that exactly two are red?

    ### Question 3

    Count the possibilities of

    (a) seating 5 people on 5 chairs

    (b) choosing 3 different ice-cream flavours from 12
    """)
    return

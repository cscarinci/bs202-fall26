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
    header("Lecture 02", "Week 01", "Lecture 02 · Properties of probability; counting methods")
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
    - **random experiment** = repeatable, uncertain outcome whose set of all outcomes is defined &nbsp; $\leadsto$ &nbsp; sample space $S$
    - **events in an experiment** = collections of outcomes (subsets $A \subseteq S$) sharing some property &nbsp; $\leadsto$ &nbsp; if the outcome has property “$A$” we say “$A$ has occurred”
    - a **probability measure** in an experiment is a function $P : \mathcal{E} \longrightarrow \mathbb{R}$ that assigns probabilities to each event ($\mathcal{E}$: collection of all relevant events); $P$ must satisfy 3 axioms

        $$
        \underbrace{P(A) \geq 0 \quad \forall\, A \in \mathcal{E}}_{\text{positivity}} \qquad
        \underbrace{P(S) = 1}_{\text{normalization}} \qquad
        \underbrace{P(A \cup B) = P(A) + P(B) \ \text{ for } A \cap B = \emptyset}_{\text{additivity}}
        $$

    - to be precise, we need a bit more from additivity (**countable additivity**; we won't need to be this precise)

        $$
        P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots \qquad \text{for } \underbrace{A_1, A_2, \dots}_{\text{possibly infinite}} \text{ pairwise disjoint} \quad (A_i \cap A_j = \emptyset \ \ \forall\, i \neq j)
        $$

    - we call a triple $(S, \mathcal{E}, P)$ a **probability space** &nbsp; $\leadsto$ &nbsp; a mathematical model for a random experiment
    - rolling a die: $S = \{1, 2, 3, 4, 5, 6\}$, &nbsp; $\mathcal{E} = \big\{ \emptyset, \{1\}, \{2\}, \dots, \{1, 2\}, \dots, \{1, 2, 3, 4, 5, 6\} \big\}$; for a “fair” die (extra assumption): $P(\{i\}) = P(\{j\}) \quad \forall\, i \neq j \in S$

        $$
        \text{axioms} \quad \Longrightarrow \quad P(\{i\}) = \tfrac{1}{6}, \quad P(\{i, j\}) = \tfrac{2}{6}, \quad P(\{i, j, k\}) = \tfrac{3}{6}, \ \dots
        \quad \Longrightarrow \quad P(A) = \frac{\# A}{\# S} \quad \forall\, A \in \mathcal{E}
        $$

    - but not every die is fair… a different assumption is also possible

        $$
        P(\{i\}) = \begin{cases} 0, & i \neq 6 \\ 1, & i = 6 \end{cases}
        \quad \overset{\text{axioms}}{\Longrightarrow} \quad
        P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6 \\ 1, & i = 6 \text{ or } j = 6 \end{cases}
        \quad \Longrightarrow \quad
        P(A) = \begin{cases} 0, & 6 \notin A \\ 1, & 6 \in A \end{cases}
        $$

        different probability measure on $(S, \mathcal{E})$ &nbsp; $\leadsto$ &nbsp; different mathematical model for the “dice experiment”

    **In this lecture:** properties of probability (axioms + algebra of events) and counting methods
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
                ax.text(*at, name, color=col, fontsize=12, ha="center", va="center")
            ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.4, 2.4, 0], color="black", lw=1.0, solid_joinstyle="miter")
            ax.text(-0.62, 1.2, sign, fontsize=14, ha="center", va="center")
            ax.text(1.6, -0.2, remark, fontsize=12, ha="center", va="top", linespacing=1.1)
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
    _ax.text(1.12, 1.15, "$A$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.text(2.3, 1.62, "$B$", color=RED, fontsize=13, ha="center", va="center")
    _ax.text(2.75, 0.25, "$S$", fontsize=13, ha="center", va="center")

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

    1. $P(A^c) = 1 - P(A)$
    2. $P(\emptyset) = 0$
    3. if $A \subseteq B$ then $P(A) \leq P(B)$
    """,
                "Basic properties",
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; $P$ is similar to “relative size” or “relative weight”

    **Proof.**

    (i) &nbsp; $A \subseteq S \ \Longrightarrow \ A \cup A^c = S$ and $A \cap A^c = \emptyset$ &nbsp; $\Longrightarrow$ &nbsp; $P(A \cup A^c) = 1 = P(A) + P(A^c)$

    (ii) &nbsp; $A = S \ \Longrightarrow \ A^c = S^c = \emptyset$ &nbsp; $\Longrightarrow$ &nbsp; $P(S \cup \emptyset) = 1 = P(S) + P(\emptyset)$ &nbsp; $\Longrightarrow$ &nbsp; $P(\emptyset) = 0$

    (iii) &nbsp; $A \subseteq B \ \Longrightarrow \ B = (B \cap A) \cup (B \cap A^c) = A \cup (B \cap A^c)$

    $$
    \text{with} \quad A \cap (B \cap A^c) = \emptyset \qquad \big(\text{since } A \cap (A^c \cap B) = (A \cap A^c) \cap B\big)
    $$

    $$
    \Longrightarrow \quad P(B) = P(A) + \underbrace{P(B \cap A^c)}_{\geq\, 0} \geq P(A) \qquad \square
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
    **Proof.** &nbsp; $A \cup B = A \cup (A^c \cap B)$ &nbsp; (with $A \cap (B \cap A^c) = \emptyset$) &nbsp; $\Longrightarrow$ &nbsp; $P(A \cup B) = P(A) + P(A^c \cap B)$

    $(A^c \cap B) \cup (A \cap B) = B$ &nbsp; (with $(A^c \cap B) \cap (A \cap B) = \emptyset$) &nbsp; $\Longrightarrow$ &nbsp; $P(A^c \cap B) + P(A \cap B) = P(B)$

    $$
    \Longrightarrow \quad P(A \cup B) = P(A) + P(B) - P(A \cap B) \qquad \square
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

    $$
    \begin{aligned}
    P(A \cup B \cup C) = {} & P(A) + P(B) + P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C) \\
    & + P(A \cap B \cap C)
    \end{aligned}
    $$
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
def _(BLUE, Figure, HALF, ORANGE, RED, ie_sum, mo, table):
    _t = ie_sum.value
    _fig = Figure(figsize=(HALF, HALF), layout="constrained")
    _ax = _fig.subplots()
    _A, _B, _C = set(), set(), set()
    for _i in range(1, 7):
        for _j in range(1, 7):
            if _i % 2 == 1:
                _A.add((_i, _j))
                _ax.plot(_i, _j, "o", ms=17, mfc="none", mec=BLUE, mew=1.2)
            if _j % 2 == 1:
                _B.add((_i, _j))
                _ax.plot(_i, _j, "s", ms=12, mfc="none", mec=RED, mew=1.2)
            if _i + _j == _t:
                _C.add((_i, _j))
                _ax.plot(_i, _j, "D", ms=6.5, mfc="none", mec=ORANGE, mew=1.2)
            _ax.plot(_i, _j, "o", ms=2.5, color="black")
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
    _f = lambda k: rf"\frac{{{k}}}{{36}}"
    mo.vstack(
        [
            mo.hstack([ie_sum], justify="start", gap=2, wrap=True),
            table(
                [
                    (rf"$\textcolor{{{BLUE}}}{{A}} = \{{\text{{1st is odd}}\}}$ (circles)", rf"$\# A = \textcolor{{{BLUE}}}{{{_n[0]}}}$"),
                    (rf"$\textcolor{{{RED}}}{{B}} = \{{\text{{2nd is odd}}\}}$ (squares)", rf"$\# B = \textcolor{{{RED}}}{{{_n[1]}}}$"),
                    (rf"$\textcolor{{{ORANGE}}}{{C}} = \{{\text{{sum is }} {_t}\}}$ (diamonds)", rf"$\# C = \textcolor{{{ORANGE}}}{{{_n[2]}}}$"),
                    (r"$\#(A \cap B), \ \#(A \cap C), \ \#(B \cap C), \ \#(A \cap B \cap C)$", rf"${_n[3]}, \ {_n[4]}, \ {_n[5]}, \ {_n[6]}$"),
                    (r"$P(A \cup B \cup C)$", rf"${_f(_n[0])} + {_f(_n[1])} + {_f(_n[2])} - {_f(_n[3])} - {_f(_n[4])} - {_f(_n[5])} + {_f(_n[6])} = {_f(_rhs)}$"),
                    (r"$\#(A \cup B \cup C)$, counting the marked points", rf"${_union}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Equally likely outcomes"""),
            definition(
                r"""
    If $S = \{o_1, \dots, o_n\}$ is finite and $P(\{o_i\}) = P(\{o_j\}) \quad \forall\, i, j \in \{1, \dots, n\}$ we say $(S, \mathcal{E}, P)$ has **equally likely outcomes**.
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

    ### Counting methods (WMS 2.6)
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
    **Proof.** Think of elements $a_i$ as labels of rows and elements $b_j$ as labels of columns of a matrix &nbsp; $\Longrightarrow$ &nbsp; $(a_i, b_j)$ labels its entries &nbsp; (not a proof… just verification) $\square$

    **Example** (Flipping a coin and rolling a die).

    $$
    S = \{(H, 1), (H, 2), \dots, (H, 6), (T, 1), \dots, (T, 6)\} \quad \Longrightarrow \quad \# S = 12 = 2 \times 6
    $$

    $\leadsto$ &nbsp; useful to count total number of outcomes on random experiments with **successive stages** (1st the coin, then the die)

    **Remark.** The rule easily extends to more than two sets

    $$
    \text{e.g.} \quad \# A = m, \ \# B = n, \ \# C = p \quad \Longrightarrow \quad \#(\underbrace{A \times B \times C}_{\text{ordered triples}}) = m\, n\, p
    $$

    **Example** (ordered hands of poker).

    $$
    S = \{\, \underbrace{(A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit),\ (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit)}_{\text{distinct ordered hands}},\ \dots \,\}
    $$

    $$
    \# S = \underbrace{\#(\text{1st card})}_{\text{1st stage}}\ \underbrace{\#(\text{2nd card})}_{\text{2nd stage}} \cdots \underbrace{\#(\text{5th card})}_{\text{5th stage}}
    = 52 \cdot 51 \cdot 50 \cdot 49 \cdot 48 = \frac{52!}{47!} = P^{52}_{5}
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
    """,
                "Number of orderings",
            ),
            mo.md(
                r"""
    **Example** (real hands of poker: unordered).

    If we don't care about order

    $$
    (A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit) = (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit) = (2\heartsuit, 3\spadesuit, 5\diamondsuit, A\diamondsuit, 4\clubsuit) = \cdots
    $$

    $\leadsto$ &nbsp; $P^{52}_5$ over-counts the hands!
    """
            ),
            theorem(
                r"""
    $$
    C^n_r = \#(\text{combinations of } n \text{ objects taken } r \text{ at a time}) = \frac{P^n_r}{r!} = \frac{n!}{r!\,(n - r)!} = \binom{n}{r}
    $$

    (combinations: unordered arrangements)
    """,
                "Number of combinations",
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
    \Longrightarrow \quad P^{52}_5 = C^{52}_5 \cdot 5! \qquad \square
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
def _(cn, cr, math, mo, table):
    _n, _r = cn.value, cr.value
    _fmt = lambda k: "$" + f"{k:,}".replace(",", r"\,") + "$"
    _need = r"need $r \leq n$"
    mo.vstack(
        [
            mo.hstack([cn, cr], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"orderings $P^n_r$", _fmt(math.perm(_n, _r)) if _r <= _n else _need),
                    (r"$r!$", _fmt(math.factorial(_r))),
                    (r"combinations $C^n_r$", _fmt(math.comb(_n, _r)) if _r <= _n else _need),
                    (r"arrangements with replacement $n^r$", _fmt(_n**_r)),
                    (r"combinations with replacement $\binom{n + r - 1}{r}$", _fmt(math.comb(_n + _r - 1, _r))),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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

    $\leadsto$ &nbsp; counting combinations of 1 defective plus 2 defective plus 3 defective is hard…

    $$
    \{\text{at least one defective}\} = \{\text{none defective}\}^c
    $$

    $\leadsto$ &nbsp; counting combinations of none defective is much easier!

    $$
    \#\{\text{none defective}\} = C^{17}_4 = \frac{17!}{4!\, 13!}
    $$

    $$
    \Longrightarrow \quad P(\text{at least one}) = 1 - P(\text{none}) = 1 - \frac{C^{17}_4}{C^{20}_4} = 1 - \underbrace{\frac{17!}{20!} \frac{16!}{13!}}_{\textstyle \frac{16 \cdot 15 \cdot 14}{20 \cdot 19 \cdot 18}} \approx 50.9\%
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    d_items = mo.ui.slider(5, 50, 1, value=20, label="items", show_value=True)
    d_def = mo.ui.slider(0, 10, 1, value=3, label="defective", show_value=True)
    d_pick = mo.ui.slider(1, 10, 1, value=4, label="picked", show_value=True)
    return d_def, d_items, d_pick


@app.cell(hide_code=True)
def _(d_def, d_items, d_pick, math, mo, table):
    _n, _d, _k = d_items.value, d_def.value, d_pick.value
    _fmt = lambda k: "$" + f"{k:,}".replace(",", r"\,") + "$"
    _need_d, _need_k = r"need defective $\leq$ items", r"need picked $\leq$ items"
    if _d > _n:
        _none = _p = _need_d
    elif _k > _n:
        _none = _p = _need_k
    else:
        _none = _fmt(math.comb(_n - _d, _k))
        _p = rf"${100 * (1 - math.comb(_n - _d, _k) / math.comb(_n, _k)):.1f}\%$"
    mo.vstack(
        [
            mo.hstack([d_items, d_def, d_pick], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\#\{\text{none defective}\}$", _none),
                    (r"$\# S$", _fmt(math.comb(_n, _k)) if _k <= _n else _need_k),
                    (r"$P(\text{at least one}) = 1 - P(\text{none})$", _p),
                ]
            ),
        ]
    )
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

    $$
    n^r = \#\, \text{arrangements with replacement} = \underbrace{\#\left(\substack{\text{choices in} \\ \text{1st position}}\right)}_{n}\ \underbrace{\#\left(\substack{\text{choices in} \\ \text{2nd position}}\right)}_{n} \cdots \underbrace{\#\left(\substack{\text{choices in} \\ r\text{th position}}\right)}_{n}
    $$

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
    ## Practice

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - axioms + algebra of events &nbsp; $\Longrightarrow$ &nbsp; $P(A^c) = 1 - P(A)$, &nbsp; $P(\emptyset) = 0$, &nbsp; if $A \subseteq B$ then $P(A) \leq P(B)$
    - $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ &nbsp; (the intersection is added 2 times), and similarly for three events
    - equally likely outcomes (very strong assumption!) &nbsp; $\Longrightarrow$ &nbsp; $P(A) = \# A / \# S$: probability becomes a counting problem
    - multiplication rule: $m \cdot n$ ordered pairs &nbsp; $\leadsto$ &nbsp; count outcomes of experiments with successive stages
    - orderings $P^n_r = n!/(n - r)!$ and combinations $C^n_r = P^n_r / r! = \binom{n}{r}$ (without replacement); $n^r$ arrangements and $\binom{n + r - 1}{r}$ combinations with replacement

    **Next:** conditioning, independence, and Bayes' rule
    """)
    return


if __name__ == "__main__":
    app.run()

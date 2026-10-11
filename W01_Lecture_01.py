import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 01 · Probability basics", css_file="bs202.css")


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
def _(header):
    header("Lecture 01", "Week 01", "Lecture 01 · Probability basics")
    return


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
def _(GREEN, RED, definition, dice, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## 1 &nbsp; Probability Basics (WMS 2.1 ~ 2.4)

    Mathematical language used to describe unpredictable phenomena
    """
            ),
            definition(
                r"""
    A **random experiment** is a *repeatable process* whose *outcomes cannot be predicted with certainty* (on any individual trial of the experiment) but whose *set of possible outcomes is specified in advance* (all that can happen is known).
    """
            ),
            mo.md(r"This is the type of phenomena we will deal with."),
            definition(
                r"""
    The **sample space** of a random experiment is the set of all possible outcomes &nbsp; $\leadsto$ &nbsp; denoted by $S$

    An **event** of a random experiment is a subset of outcomes satisfying some interesting property &nbsp; $\leadsto$ &nbsp; $A \subseteq S$
    """,
                "Sample space and events",
            ),
            mo.md(
                r"""
    When we deal with probability (to be defined soon) we should not focus on individual outcomes… rather, we focus on *properties that we wish to see*.

    If the outcome of the experiment has a given property, we say “the property has occurred” &nbsp; $\leadsto$ &nbsp; hence the term “event”!

    The **event space** is the collection of all relevant events &nbsp; $\leadsto$ &nbsp; denoted $\mathcal{E}$
    """
            ),
            mo.md(
                rf"""
    **Example** (Rolling one die).

    - repeatable
    - uncertain outcome
    - pre-determined set of outcomes

    $\Longrightarrow$ &nbsp; rolling a die is a random experiment!

    $S = \{{$ {dice(range(1, 7))} $\}}$ &nbsp;&nbsp; sample space

    $A = \{{$ {dice((2, 4, 6))} $\}}$ &nbsp;&nbsp; event “even faces”

    $B = \{{$ {dice((2,))} $\}}$ &nbsp;&nbsp; event “face = two” &nbsp; (simple event; set with one element $\neq$ the element itself)

    $\mathcal{{E}} = \big\{{\, \emptyset,\ \{{$ {dice((1,))} $\}},\ \{{$ {dice((2,))} $\}} = B,\ \dots,\ \{{$ {dice((2, 4, 6))} $\}} = A,\ \dots,\ \{{$ {dice((1,))}$, \dots,$ {dice((6,))} $\}} \,\big\}}$ &nbsp;&nbsp; all subsets of outcomes
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"## Algebra of events (basic operations of set theory)"),
            definition(
                r"""
    Given $A, B \subseteq S$

    - $A \cup B$ = outcomes in $A$ <u>or</u> in $B$ &nbsp; (union)
    - $A \cap B$ = outcomes in $A$ <u>and</u> in $B$ &nbsp; (intersection)
    - $A^c$ = outcomes <u>not</u> in $A$ &nbsp; (complement)
    """
            ),
            mo.md(
                r"""
    $A$ and $B$ are **disjoint** (mutually exclusive) when $A \cap B = \emptyset$ (empty set)

    $A$ and $B$ are **exhaustive** (cover all outcomes) when $A \cup B = S$
    """
            ),
            theorem(
                r"""
    $$
    \begin{aligned}
    &\begin{cases} A \cup B = B \cup A \\ A \cap B = B \cap A \end{cases} && (\text{commutativity}) \\[6pt]
    &\begin{cases} (A \cup B) \cup C = A \cup (B \cup C) \\ (A \cap B) \cap C = A \cap (B \cap C) \end{cases} && (\text{associativity}) \\[6pt]
    &\begin{cases} A \cap (B \cup C) = (A \cap B) \cup (A \cap C) \\ A \cup (B \cap C) = (A \cup B) \cap (A \cup C) \end{cases} && (\text{distributivity}) \\[6pt]
    &\begin{cases} (A \cup B)^c = A^c \cap B^c \\ (A \cap B)^c = A^c \cup B^c \end{cases} && (\text{De Morgan's Law})
    \end{aligned}
    $$
    """,
                "Laws of set theory",
            ),
            mo.md(r"Exercise: convince yourself using diagrams."),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    venn_options = [
        "A ∪ B",
        "B ∪ A",
        "A ∩ B",
        "B ∩ A",
        "Aᶜ",
        "(A ∪ B) ∪ C",
        "A ∪ (B ∪ C)",
        "(A ∩ B) ∩ C",
        "A ∩ (B ∩ C)",
        "A ∩ (B ∪ C)",
        "(A ∩ B) ∪ (A ∩ C)",
        "A ∪ (B ∩ C)",
        "(A ∪ B) ∩ (A ∪ C)",
        "(A ∪ B)ᶜ",
        "Aᶜ ∩ Bᶜ",
        "(A ∩ B)ᶜ",
        "Aᶜ ∪ Bᶜ",
    ]
    _laws = {
        "commutativity (∪)": ("A ∪ B", "B ∪ A"),
        "commutativity (∩)": ("A ∩ B", "B ∩ A"),
        "associativity (∪)": ("(A ∪ B) ∪ C", "A ∪ (B ∪ C)"),
        "associativity (∩)": ("(A ∩ B) ∩ C", "A ∩ (B ∩ C)"),
        "distributivity (∩ over ∪)": ("A ∩ (B ∪ C)", "(A ∩ B) ∪ (A ∩ C)"),
        "distributivity (∪ over ∩)": ("A ∪ (B ∩ C)", "(A ∪ B) ∩ (A ∪ C)"),
        "De Morgan (∪)": ("(A ∪ B)ᶜ", "Aᶜ ∩ Bᶜ"),
        "De Morgan (∩)": ("(A ∩ B)ᶜ", "Aᶜ ∪ Bᶜ"),
    }
    # The pair shown in the two panels; a law sets both sides, the left/right dropdowns set one each
    get_venn, set_venn = mo.state(_laws["distributivity (∩ over ∪)"])
    venn_law = mo.ui.dropdown(_laws, label="law", on_change=lambda pair: pair and set_venn(pair))
    return get_venn, set_venn, venn_law, venn_options


@app.cell(hide_code=True)
def _(get_venn, mo, set_venn, venn_options):
    _l, _r = get_venn()
    venn_left = mo.ui.dropdown(venn_options, value=_l, label="left", allow_select_none=False, on_change=lambda v: set_venn((v, get_venn()[1])))
    venn_right = mo.ui.dropdown(venn_options, value=_r, label="right", allow_select_none=False, on_change=lambda v: set_venn((get_venn()[0], v)))
    return venn_left, venn_right


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, mo, np, venn_law, venn_left, venn_right):
    _g = np.linspace(0, 1, 500)
    _X, _Y = np.meshgrid(_g * 3.2, _g * 2.1)
    _A = (_X - 1.25) ** 2 + (_Y - 1.2) ** 2 < 0.48**2
    _B = (_X - 1.95) ** 2 + (_Y - 1.2) ** 2 < 0.54**2
    _C = (_X - 1.6) ** 2 + (_Y - 0.78) ** 2 < 0.44**2
    _sets = {
        "A ∪ B": _A | _B,
        "B ∪ A": _B | _A,
        "A ∩ B": _A & _B,
        "B ∩ A": _B & _A,
        "Aᶜ": ~_A,
        "(A ∪ B) ∪ C": _A | _B | _C,
        "A ∪ (B ∪ C)": _A | (_B | _C),
        "(A ∩ B) ∩ C": _A & _B & _C,
        "A ∩ (B ∩ C)": _A & (_B & _C),
        "A ∩ (B ∪ C)": _A & (_B | _C),
        "(A ∩ B) ∪ (A ∩ C)": (_A & _B) | (_A & _C),
        "A ∪ (B ∩ C)": _A | (_B & _C),
        "(A ∪ B) ∩ (A ∪ C)": (_A | _B) & (_A | _C),
        "(A ∪ B)ᶜ": ~(_A | _B),
        "Aᶜ ∩ Bᶜ": ~_A & ~_B,
        "(A ∩ B)ᶜ": ~(_A & _B),
        "Aᶜ ∪ Bᶜ": ~_A | ~_B,
    }

    _fig = Figure(figsize=(8.4, 2.9), layout="constrained")
    _th = np.linspace(0, 2 * np.pi, 200)
    for _ax, _choice in zip(_fig.subplots(1, 2), (venn_left.value, venn_right.value)):
        _ax.contourf(_X, _Y, _sets[_choice].astype(float), levels=[0.5, 1.5], colors=["#c9c9c9"])
        for (_cx, _cy, _r), _col, _name, _lx, _ly in (
            ((1.25, 1.2, 0.48), RED, "$A$", 0.72, 1.72),
            ((1.95, 1.2, 0.54), GREEN, "$B$", 2.45, 1.72),
            ((1.6, 0.78, 0.44), BLUE, "$C$", 2.05, 0.3),
        ):
            _ax.plot(_cx + _r * np.cos(_th), _cy + _r * np.sin(_th), color=_col, lw=1.8)
            _ax.text(_lx, _ly, _name, color=_col, fontsize=15)
        _ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.1, 2.1, 0], color="black", lw=1.4)
        _ax.text(0.12, 0.12, "$S$", fontsize=15)
        _ax.set_xlim(-0.05, 3.25)
        _ax.set_ylim(-0.05, 2.15)
        _ax.set_aspect("equal")
        _ax.axis("off")

    _same = np.array_equal(_sets[venn_left.value], _sets[venn_right.value])
    _verdict = mo.md("**equal ✓**" if _same else "**not equal ✗**")
    mo.vstack([mo.hstack([venn_law, venn_left, venn_right, _verdict], justify="space-around", align="center", wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(GREEN, RED, dice, mo):
    mo.md(
        rf"""
    **Example** (Rolling two dice).

    $S = \{{$ {dice(range(1, 7), RED)} $\}} \times \{{$ {dice(range(1, 7), GREEN)} $\}}$

    $A = \{{\text{{faces add to 7}}\}}, \qquad B = \{{\text{{at least one face is 5}}\}}$

    $A \cap B = \{{\, ($ {dice((2,), RED)}$,$ {dice((5,), GREEN)} $),\ ($ {dice((5,), RED)}$,$ {dice((2,), GREEN)} $) \,\}}$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    total = mo.ui.slider(2, 12, 1, value=7, label="$A$: faces add to", show_value=True)
    face = mo.ui.slider(1, 6, 1, value=5, label="$B$: at least one face is", show_value=True)
    return face, total


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, die, face, mo, total):
    _t, _k = total.value, face.value
    _fig = Figure(figsize=(4.0, 4.0), layout="constrained")
    _ax = _fig.subplots()
    _both, _nA, _nB = [], 0, 0
    for _i in range(1, 7):
        for _j in range(1, 7):
            _inA, _inB = _i + _j == _t, _k in (_i, _j)
            if _inA:
                _nA += 1
                _ax.plot(_i, _j, "o", ms=17, mfc="none", mec=GREEN, mew=1.8)
            if _inB:
                _nB += 1
                _ax.plot(_i, _j, "s", ms=13, mfc="none", mec="#e65100", mew=1.8)
            if _inA and _inB:
                _both.append((_i, _j))
            _ax.plot(_i, _j, "o", ms=4, color=BLUE)
    _ax.set_xlim(0.3, 6.7)
    _ax.set_ylim(0.3, 6.7)
    _ax.set_aspect("equal")
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks(range(1, 7))
    _ax.set_xlabel("first die", color=RED)
    _ax.set_ylabel("second die", color=GREEN)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _pairs = ", ".join(f"$($ {die(_i, RED)}$,$ {die(_j, GREEN)} $)$" for _i, _j in _both)
    mo.vstack(
        [
            mo.hstack([total, face], justify="start", gap=3),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        rf"$\textcolor{{{GREEN}}}{{A}}$ (circles), &nbsp; $\textcolor{{#e65100}}{{B}}$ (squares), &nbsp; $\textcolor{{{BLUE}}}{{S}}$ (dots)"
                        "\n\n"
                        + (rf"$A \cap B = \{{\,$ {_pairs} $\,\}}$" if _both else r"$A \cap B = \emptyset$")
                        + "\n\n"
                        + rf"$|A| = {_nA}, \quad |B| = {_nB}, \quad |A \cap B| = {len(_both)}$"
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
def _(BLUE, Figure, GREEN, RED, definition, mo, np):
    _fig = Figure(figsize=(3.4, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _th = np.linspace(0, 2 * np.pi, 200)
    for (_cx, _cy, _r), _col, _name in (((0.75, 1.3, 0.52), RED, "$A_1$"), ((2.3, 1.5, 0.38), GREEN, "$A_2$"), ((1.7, 0.65, 0.52), BLUE, "$A_3$")):
        _ax.plot(_cx + _r * np.cos(_th), _cy + _r * np.sin(_th), color=_col, lw=1.8)
        _ax.text(_cx, _cy, _name, color=_col, fontsize=15, ha="center", va="center")
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 2, 2, 0], color="black", lw=1.4)
    _ax.text(3.1, 0.05, "$S$", fontsize=15)
    _ax.set_xlim(-0.05, 3.5)
    _ax.set_ylim(-0.05, 2.05)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(r"## Axioms of Probability"),
            definition(
                r"""
    Given a random experiment, we define probability as a measure of events relative to the sample space.

    Precisely: Given $(S, \mathcal{E})$, a **probability measure** is $P : \mathcal{E} \longrightarrow \mathbb{R}$ s.t.

    - $P(S) = 1$
    - $P(A) \geq 0$ for every event $A \in \mathcal{E}$
    - $P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots$ for every countable sequence of *pairwise disjoint* events $A_1, A_2, \dots$ &nbsp; ($A_i \cap A_j = \emptyset \ \ \forall\, i \neq j$)
    """
            ),
            mo.hstack(
                [_fig, mo.md(r"$$P(A_1 \cup A_2 \cup A_3) = P(A_1) + P(A_2) + P(A_3)$$")],
                widths=[1, 1],
                gap=2,
                align="center",
                wrap=True,
            ),
            mo.md(
                r"""
    Probability is an additive notion of size of events relative to the full sample space.

    It can be interpreted as the relative frequency of event occurrences in infinite independent trials.
    """
            ),
            definition(
                r"""
    We call a triple $(S, \mathcal{E}, P)$ a **probability space** (abstract model of a random experiment).
    """
            ),
            mo.md(
                r"""
    First goal of probability theory is to study properties and give examples of such spaces!

    **Example** (Rolling one die).

    $$
    S = \{1, 2, 3, 4, 5, 6\}
    $$

    $$
    \mathcal{E} = \big\{\, \underbrace{\{1\}}_{\text{“face is 1”}}, \dots, \{6\},\ \underbrace{\{1, 2\}}_{\substack{\text{“1 or 2”} \\ =\, \{1\} \cup \{2\}}}, \dots, \{5, 6\},\ \dots,\ \underbrace{\{1, 2, 3, 4, 5, 6\}}_{\text{“1 or 2 or … or 6”}},\ \underbrace{\emptyset}_{\text{“not (1 or … or 6)”}} \,\big\}
    $$

    $P = \,?$

    Fair die: &nbsp; $P(\{i\}) = \tfrac{1}{6} \quad \forall\, i = 1, \dots, 6$

    $$
    \begin{aligned}
    \Longrightarrow \quad & P(\{i, j\}) = P(\{i\}) + P(\{j\}) = \tfrac{2}{6} && \forall\, i \neq j \\
    \Longrightarrow \quad & P(\{i, j, k\}) = \tfrac{3}{6} && \forall\, i \neq j \neq k \\
    & \ \vdots
    \end{aligned}
    $$

    In particular: &nbsp; $P(\{\text{even faces}\}) = \tfrac{3}{6}$

    Not fair die (one example): &nbsp; $P(\{6\}) = 1$, &nbsp; $P(\{i\}) = 0$ for $i \neq 6$

    $$
    \Longrightarrow \quad P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6 \\ 1, & i = 6 \text{ or } j = 6 \end{cases}
    $$

    $$
    P(\{\text{even faces}\}) = 1\,!
    $$

    There can be many distinct probability measures on the same sample space / event space.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    die_preset = mo.ui.dropdown(
        {"fair": (1, 1, 1, 1, 1, 1), "loaded (always 6)": (0, 0, 0, 0, 0, 1), "loaded (even faces)": (1, 3, 1, 3, 1, 3)},
        value="fair",
        label="preset",
    )
    return (die_preset,)


@app.cell(hide_code=True)
def _(die_preset, mo):
    weights = mo.ui.array([mo.ui.slider(0, 10, 1, value=w, label=f"face {i + 1}", show_value=True) for i, w in enumerate(die_preset.value)])
    return (weights,)


@app.cell(hide_code=True)
def _(BLUE, Figure, die_preset, mo, np, weights):
    _w = np.array(weights.value, dtype=float)
    _total = int(_w.sum())
    pmf = _w / _total if _total > 0 else np.full(6, 1 / 6)
    _even = int(_w[1::2].sum())

    _fig = Figure(figsize=(4.2, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.bar(range(1, 7), pmf, width=0.6, color=BLUE)
    _ax.set_xticks(range(1, 7))
    _ax.set_ylim(0, 1)
    _ax.set_xlabel("face $i$")
    _ax.set_ylabel(r"$P(\{i\})$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(r"Choose $P$ by assigning a weight to each face (probabilities are the weights divided by their sum):"),
            mo.hstack([die_preset] + list(weights), justify="start", gap=1.5, align="end", wrap=True),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        rf"$P(\{{\text{{even faces}}\}}) = \tfrac{{{_even}}}{{{_total}}}$" + "\n\n" + rf"$P(\{{1, 2\}}) = \tfrac{{{int(_w[0] + _w[1])}}}{{{_total}}}$"
                        if _total > 0
                        else "**Note.** The weights must not all be zero ($P(S) = 1$)."
                    ),
                ],
                widths=[1, 1],
                gap=2,
                align="center",
                wrap=True,
            ),
        ]
    )
    return (pmf,)


@app.cell(hide_code=True)
def _(mo):
    n_rolls = mo.ui.slider(10, 5000, 10, value=500, label="number of rolls", show_value=True)
    reroll = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Roll again")
    return n_rolls, reroll


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, mo, n_rolls, np, pmf, reroll):
    _rng = np.random.default_rng(202 + reroll.value)
    _n = n_rolls.value
    _p = float(pmf[1::2].sum())
    _even = _rng.choice(np.arange(1, 7), size=_n, p=pmf) % 2 == 0
    _freq = np.cumsum(_even) / np.arange(1, _n + 1)

    _fig = Figure(figsize=(7.4, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.axhline(_p, color=RED, lw=1.2)
    _ax.plot(np.arange(1, _n + 1), _freq, color=BLUE, lw=1.4)
    _ax.set_ylim(0, 1)
    _ax.set_xlim(1, _n)
    _ax.set_xlabel("number of rolls")
    _ax.set_ylabel("relative frequency")
    _ax.text(_n * 0.98, 0.88 if _p < 0.8 else 0.06, rf"$P(\{{\mathrm{{even\ faces}}\}}) = {_p:.3f}$", color=RED, ha="right", fontsize=13)

    mo.vstack(
        [
            mo.md(r"Relative frequency of “even faces” in repeated rolls of the die chosen above:"),
            mo.hstack([n_rolls, reroll], justify="start", gap=2, align="center"),
            _fig,
        ]
    )
    return


if __name__ == "__main__":
    app.run()

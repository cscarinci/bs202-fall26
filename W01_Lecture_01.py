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
    header("Lecture 01", "Week 01", "Lecture 01 • Probability basics")
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
def _():
    _PIPS = {
        1: [(2, 2)],
        2: [(1, 1), (3, 3)],
        3: [(1, 1), (2, 2), (3, 3)],
        4: [(1, 1), (1, 3), (3, 1), (3, 3)],
        5: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)],
        6: [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3)],
    }

    def die(n):
        """A small line drawing of a die face, for use inside text (it takes the colour of the text)."""
        dots = "".join(f'<circle cx="{6 * x}" cy="{6 * y}" r="2" fill="currentColor"/>' for x, y in _PIPS[n])
        return (
            '<svg viewBox="0 0 24 24" style="display:inline-block;width:1.25em;height:1.25em;vertical-align:-0.25em">'
            f'<rect x="1.5" y="1.5" width="21" height="21" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>{dots}</svg>'
        )

    def dice(faces):
        return ", ".join(die(n) for n in faces)

    return dice, die


@app.cell(hide_code=True)
def _(definition, dice, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## I.1 &nbsp; Probability Basics

    **References:** WMS 2.1–2.4

    $\leadsto$ &nbsp; mathematical language used to describe unpredictable phenomena
    """
            ),
            definition(
                r"""
    A **random experiment** is a *repeatable process* whose *outcomes cannot be predicted with certainty* (on any individual trial of the experiment) but whose *set of possible outcomes is specified in advance* (all that can happen is known).
    """,
                "Random experiment",
            ),
            mo.md(r"$\leadsto$ &nbsp; this is the type of phenomena we will deal with"),
            definition(
                r"""
    The **sample space** of a random experiment is the set of all possible outcomes &nbsp; <span class="nw">$\leadsto$ &nbsp; denoted</span> by $S$

    An **event** of a random experiment is a subset of outcomes satisfying some interesting property &nbsp; <span class="nw">$\leadsto$ &nbsp; $A \subseteq S$</span>
    """,
                "Sample space and events",
            ),
            mo.md(
                r"""
    When we deal with probability (to be defined soon) we should not focus on individual outcomes… rather, we focus on *properties that we wish to see*

    $\leadsto$ &nbsp; if the outcome of the experiment has a given property, we say “the property has occurred” &nbsp; <span class="nw">$\leadsto$ &nbsp; hence</span> the term “event”!

    The **event space** is the collection of all relevant events &nbsp; <span class="nw">$\leadsto$ &nbsp; denoted</span> $\mathcal{E}$
    """
            ),
            mo.md(
                rf"""
    **Example** (Rolling one die).

    - repeatable
    - uncertain outcome
    - pre-determined set of outcomes

    $\Longrightarrow$ &nbsp; rolling a die is a random experiment!

    $S = \{{$ {dice(range(1, 7))} $\}}$ &nbsp;&nbsp; (sample space)

    $A = \{{$ {dice((2, 4, 6))} $\}}$ &nbsp;&nbsp; (event “even faces”)

    $B = \{{$ {dice((2,))} $\}}$ &nbsp;&nbsp; (event “face = two”: a simple event; a set with one element $\neq$ the element itself)

    <span style="white-space:nowrap">$\mathcal{{E}} = \big\{{\, \emptyset,\ \{{$ {dice((1,))} $\}},\ \{{$ {dice((2,))} $\}} = B,\ \dots,$</span> <span style="white-space:nowrap">$\{{$ {dice((2, 4, 6))} $\}} = A,\ \dots,$</span> <span style="white-space:nowrap">$\{{$ {dice((1,))}$, \dots,$ {dice((6,))} $\}} \,\big\}}$</span> &nbsp;&nbsp; (all&nbsp;subsets&nbsp;of&nbsp;outcomes)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Algebra of events (basic operations of set theory)"""),
            definition(
                r"""
    Given $A, B \subseteq S$

    - $A \cup B$ = outcomes in $A$ <u>or</u> in $B$ &nbsp; (**union**)
    - $A \cap B$ = outcomes in $A$ <u>and</u> in $B$ &nbsp; (**intersection**)
    - $A^c$ = outcomes <u>not</u> in $A$ &nbsp; (**complement**)
    """,
                "Union, intersection and complement",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $A$ and $B$ are **disjoint** (mutually exclusive) when $A \cap B = \emptyset$ (the empty set)

    $\leadsto$ &nbsp; $A$ and $B$ are **exhaustive** (cover all outcomes) when $A \cup B = S$
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
            mo.md(r"$\leadsto$ &nbsp; exercise: convince yourself using diagrams"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    venn_set = mo.ui.dropdown(
        [
            "A ∪ B",
            "A ∩ B",
            "Aᶜ",
            "A ∪ B ∪ C",
            "A ∩ B ∩ C",
            "A ∩ (B ∪ C)",
            "(A ∩ B) ∪ (A ∩ C)",
            "A ∪ (B ∩ C)",
            "(A ∪ B) ∩ (A ∪ C)",
            "(A ∪ B)ᶜ",
            "Aᶜ ∩ Bᶜ",
            "(A ∩ B)ᶜ",
            "Aᶜ ∪ Bᶜ",
        ],
        value="A ∪ B",
        label="set",
        allow_select_none=False,
    )
    return (venn_set,)


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, ORANGE, RED, mo, np, venn_set):
    _g = np.linspace(0, 1, 600)
    _X, _Y = np.meshgrid(_g * 3.2, _g * 2.1)
    _circles = {"A": (1.25, 1.2, 0.48), "B": (1.95, 1.2, 0.54), "C": (1.6, 0.78, 0.44)}
    _A, _B, _C = [(_X - _cx) ** 2 + (_Y - _cy) ** 2 < _r**2 for _cx, _cy, _r in _circles.values()]
    _sets = {
        "A ∪ B": _A | _B,
        "A ∩ B": _A & _B,
        "Aᶜ": ~_A,
        "A ∪ B ∪ C": _A | _B | _C,
        "A ∩ B ∩ C": _A & _B & _C,
        "A ∩ (B ∪ C)": _A & (_B | _C),
        "(A ∩ B) ∪ (A ∩ C)": (_A & _B) | (_A & _C),
        "A ∪ (B ∩ C)": _A | (_B & _C),
        "(A ∪ B) ∩ (A ∪ C)": (_A | _B) & (_A | _C),
        "(A ∪ B)ᶜ": ~(_A | _B),
        "Aᶜ ∩ Bᶜ": ~_A & ~_B,
        "(A ∩ B)ᶜ": ~(_A & _B),
        "Aᶜ ∪ Bᶜ": ~_A | ~_B,
    }
    _choice = venn_set.value
    _fig = Figure(figsize=(4.6, 3.3), layout="constrained")
    _ax = _fig.subplots()
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.set_title("$" + _choice.replace("∪", r"\cup").replace("∩", r"\cap").replace("ᶜ", "^c") + "$", fontsize=15)
    _ax.contourf(_X, _Y, _sets[_choice].astype(float), levels=[0.5, 1.5], colors=[LIGHT])
    for _name, _col, _lx, _ly in (("A", BLUE, 0.72, 1.72), ("B", RED, 2.45, 1.72), ("C", ORANGE, 2.08, 0.3)):
        _cx, _cy, _r = _circles[_name]
        _ax.plot(_cx + _r * np.cos(_th), _cy + _r * np.sin(_th), color=_col, lw=1.4)
        _ax.text(_lx, _ly, f"${_name}$", color=_col, fontsize=15, ha="center", va="center")
    _ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.1, 2.1, 0], color="black", lw=1.0)
    _ax.text(0.2, 0.2, "$S$", fontsize=15, ha="center", va="center")
    _ax.set_xlim(-0.05, 3.25)
    _ax.set_ylim(-0.05, 2.15)
    _ax.set_aspect("equal")
    _ax.axis("off")
    mo.vstack([venn_set, _fig])
    return


@app.cell(hide_code=True)
def _(dice, mo):
    mo.md(
        rf"""
    **Example** (Rolling two dice).

    $S = \{{$ {dice(range(1, 7))} $\}} \times \{{$ {dice(range(1, 7))} $\}}$

    $A = \{{\text{{faces add to 7}}\}}, \qquad B = \{{\text{{at least one face is 5}}\}}$

    $A \cap B = \{{\, ($ {dice((2,))}$,$ {dice((5,))} $),\ ($ {dice((5,))}$,$ {dice((2,))} $) \,\}}$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    total = mo.ui.slider(2, 12, 1, value=7, label="$A$: faces add to", show_value=True)
    face = mo.ui.slider(1, 6, 1, value=5, label="$B$: at least one face is", show_value=True)
    return face, total


@app.cell(hide_code=True)
def _(BLUE, HALF, LIGHT, RED, arrow, blank, face, math, mo, np, total):
    _t, _k = total.value, face.value

    def _loop(ax, p, q, r, color):
        """Closed outline at distance r around the segment from p to q (a circle when p = q)."""
        a = math.atan2(q[1] - p[1], q[0] - p[0])
        s = np.linspace(-np.pi / 2, np.pi / 2, 40)
        xs = np.concatenate([q[0] + r * np.cos(a + s), p[0] + r * np.cos(a + np.pi + s)])
        ys = np.concatenate([q[1] + r * np.sin(a + s), p[1] + r * np.sin(a + np.pi + s)])
        ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=color, lw=1.4)

    _fig, _ax = blank(HALF, HALF, (-1.35, 7.55), (-1.35, 7.55))
    arrow(_ax, (-0.4, 0), (7.3, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.4), (0, 7.3), "black", lw=0.9)
    for _i in range(1, 7):
        _ax.plot([_i, _i], [-0.07, 0.07], color="black", lw=0.9)
        _ax.plot([-0.07, 0.07], [_i, _i], color="black", lw=0.9)
        _ax.text(_i, -0.2, f"${_i}$", fontsize=12, ha="center", va="top")
        _ax.text(-0.2, _i, f"${_i}$", fontsize=12, ha="right", va="center")
    _ax.text(3.5, -0.85, "first die", fontsize=12, ha="center", va="top")
    _ax.text(-0.85, 3.5, "second die", fontsize=12, ha="right", va="center", rotation=90)

    _inA = [(_i, _t - _i) for _i in range(max(1, _t - 6), min(6, _t - 1) + 1)]
    _both = [(_i, _j) for _i, _j in _inA if _k in (_i, _j)]
    for _p in _both:
        _ax.fill(_p[0] + 0.3 * np.cos(np.linspace(0, 2 * np.pi, 60)), _p[1] + 0.3 * np.sin(np.linspace(0, 2 * np.pi, 60)), color=LIGHT, lw=0)
    for _i in range(1, 7):
        for _j in range(1, 7):
            _ax.plot(_i, _j, "o", ms=2.5, color="black")
    _loop(_ax, _inA[0], _inA[-1], 0.36, BLUE)
    _loop(_ax, (1, _k), (6, _k), 0.3, RED)
    _loop(_ax, (_k, 1), (_k, 6), 0.3, RED)
    # the label of A goes beyond the upper-left end of its loop: above the grid when that end is in the top row
    _la = (_inA[0][0] - 0.6, 6.85) if _t >= 7 else (0.36, _inA[0][1] + 0.55)
    _ax.text(*_la, "$A$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.text(6.75, _k, "$B$", color=RED, fontsize=13, ha="center", va="center")
    _ax.text(7.1, 7.1, "$S$", fontsize=13, ha="center", va="center")

    mo.vstack(
        [
            mo.hstack([total, face], justify="start", gap=2, wrap=True),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, HALF, ORANGE, RED, blank, definition, mo, np):
    _fig, _ax = blank(HALF, 2.2, (-0.05, 3.4), (-0.05, 2.05))
    _th = np.linspace(0, 2 * np.pi, 200)
    for (_cx, _cy, _r), _col, _name in (((0.75, 1.3, 0.52), BLUE, "$A_1$"), ((2.3, 1.5, 0.38), RED, "$A_2$"), ((1.7, 0.65, 0.52), ORANGE, "$A_3$")):
        _ax.plot(_cx + _r * np.cos(_th), _cy + _r * np.sin(_th), color=_col, lw=1.4)
        _ax.text(_cx, _cy, _name, color=_col, fontsize=13, ha="center", va="center")
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 2, 2, 0], color="black", lw=1.0)
    _ax.text(3.2, 0.12, "$S$", fontsize=13, ha="center", va="center")

    mo.vstack(
        [
            mo.md(r"""### Axioms of Probability"""),
            definition(
                r"""
    Given a random experiment, we define probability as a measure of events relative to the sample space.

    Precisely: given $(S, \mathcal{E})$, a **probability measure** is $P : \mathcal{E} \longrightarrow \mathbb{R}$ such that

    - $P(S) = 1$
    - $P(A) \geq 0$ for every event $A \in \mathcal{E}$
    - for every countable sequence of *pairwise disjoint* events $A_1, A_2, \dots$ &nbsp; $(A_i \cap A_j = \emptyset \ \ \forall\, i \neq j)$

        $$
        P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots
        $$
    """,
                "Probability measure",
            ),
            _fig,
            mo.md(
                r"""
    $$
    P(A_1 \cup A_2 \cup A_3) = P(A_1) + P(A_2) + P(A_3)
    $$

    $\leadsto$ &nbsp; probability is an additive notion of size of events relative to the full sample space

    $\leadsto$ &nbsp; it can be interpreted as the relative frequency of event occurrences in infinite independent trials
    """
            ),
            definition(
                r"""
    We call a triple $(S, \mathcal{E}, P)$ a **probability space** (abstract model of a random experiment).
    """,
                "Probability space",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; first goal of probability theory is to study properties and give examples of such spaces!

    **Example** (Rolling one die).

    $$
    S = \{1, 2, 3, 4, 5, 6\}
    $$

    $$
    \begin{aligned}
    \mathcal{E} = \big\{\, & \underbrace{\{1\}}_{\mathclap{\footnotesize \text{“face is 1”}}\vphantom{\footnotesize \text{“face is 1”}}}, \dots, \{6\},\ \underbrace{\{1, 2\}}_{\mathclap{\footnotesize \begin{matrix} \text{“1 or 2”} \\ =\, \{1\} \cup \{2\} \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{“1 or 2”} \\ =\, \{1\} \cup \{2\} \end{matrix}}}, \dots, \{5, 6\}, \\[3.5em]
    & \dots,\ \underbrace{\{1, 2, 3, 4, 5, 6\}}_{\mathclap{\footnotesize \text{“1 or 2 or … or 6”}}\vphantom{\footnotesize \text{“1 or 2 or … or 6”}}},\ \underbrace{\emptyset}_{\mathrlap{\footnotesize \text{“not (1 or … or 6)”}}\vphantom{\footnotesize \text{“not (1 or … or 6)”}}} \,\big\}
    \end{aligned}
    $$

    $P = \,?$

    Fair die: &nbsp; $P(\{i\}) = \dfrac{1}{6} \quad \forall\, i = 1, \dots, 6$

    $$
    \begin{aligned}
    \Longrightarrow \qquad & P(\{i, j\}) = P(\{i\}) + P(\{j\}) = \frac{2}{6} && \forall\, i \neq j \\
    \Longrightarrow \qquad & P(\{i, j, k\}) = \frac{3}{6} && \forall\, i \neq j \neq k \\
    & \ \vdots
    \end{aligned}
    $$

    In particular: &nbsp; $P(\{\text{even faces}\}) = \dfrac{3}{6}$

    Not fair die (one example): &nbsp; $P(\{6\}) = 1$, &nbsp; $P(\{i\}) = 0$ for $i \neq 6$

    $$
    \begin{aligned}
    \Longrightarrow \qquad & P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6 \\ 1, & i = 6 \text{ or } j = 6 \end{cases} \\[6pt]
    \Longrightarrow \qquad & P(\{\text{even faces}\}) = 1
    \end{aligned}
    $$

    $\leadsto$ &nbsp; there can be many distinct probability measures on the same sample space / event space
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    die_preset = mo.ui.dropdown(
        {"fair": (1, 1, 1, 1, 1, 1), "not fair": (0, 0, 0, 0, 0, 1)},
        value="fair",
        label="preset",
    )
    return (die_preset,)


@app.cell(hide_code=True)
def _(die_preset, mo):
    weights = mo.ui.array([mo.ui.slider(0, 10, 1, value=w, label=f"weight of face {i + 1}", show_value=True) for i, w in enumerate(die_preset.value)])
    weight_controls = mo.hstack([die_preset] + list(weights), justify="start", gap=2, wrap=True)
    return weight_controls, weights


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, mo, np, table, weight_controls, weights):
    _w = np.array(weights.value, dtype=float)
    _total = int(_w.sum())
    # the weights define a probability measure only when their total is positive
    pmf = _w / _total if _total > 0 else None

    _fig = Figure(figsize=(HALF, 2.5), layout="constrained")
    _ax = _fig.subplots()
    if pmf is not None:
        _ax.vlines(range(1, 7), 0, pmf, color=BLUE, lw=1.4)
        _ax.plot(range(1, 7), pmf, "o", color=BLUE, ms=5, clip_on=False, zorder=4)
    _ax.set_xticks(range(1, 7))
    _ax.set_xlim(0.4, 6.6)
    _ax.set_ylim(0, 1.05)
    _ax.set_yticks([0, 0.5, 1], ["$0$", "$0.5$", "$1$"])
    _ax.set_xlabel("face $i$")
    _ax.set_ylabel(r"$P(\{i\})$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    def _value(k):
        """P of an event of total weight k: 0 or 1; k/6 when the total is 6, as the page writes it (a stacked fraction crowds the rows); 1/2; otherwise two decimals."""
        if k in (0, _total):
            return f"${k // _total}$"
        if _total == 6:
            return f"${k}/6$"
        if 2 * k == _total:
            return "$1/2$"
        return f"${k / _total:.2f}$"

    if pmf is not None:
        _pe, _p2 = _value(int(_w[1::2].sum())), _value(int(_w[0] + _w[1]))

    mo.vstack(
        [
            weight_controls,
            table(
                [
                    (r"$P(\{\text{even faces}\})$", _pe),
                    (r"$P(\{1, 2\})$", _p2),
                ]
            )
            if pmf is not None
            else mo.md("at least one weight must be positive"),
            _fig,
        ]
    )
    return (pmf,)


@app.cell(hide_code=True)
def _(mo):
    n_rolls = mo.ui.slider(10, 5000, 10, value=500, label="number of rolls", show_value=True)
    reroll = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Roll again")
    return n_rolls, reroll


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, RED, mo, n_rolls, np, pmf, reroll):
    _rng = np.random.default_rng(202 + reroll.value)
    _n = n_rolls.value

    _fig = Figure(figsize=(FULL, 2.8), layout="constrained")
    _ax = _fig.subplots()
    if pmf is not None:
        _p = float(pmf[1::2].sum())
        _even = _rng.choice(np.arange(1, 7), size=_n, p=pmf) % 2 == 0
        _freq = np.cumsum(_even) / np.arange(1, _n + 1)
        _ax.plot(np.arange(1, _n + 1), _freq, color=BLUE, lw=1.4, zorder=4)
        _ax.axhline(_p, color=RED, lw=1.0, zorder=3)
        _ax.text(1.01, _p, r"$P(\{\mathrm{even\ faces}\})$", transform=_ax.get_yaxis_transform(), color=RED, fontsize=13, ha="left", va="center")
    _ax.set_ylim(-0.05, 1.05)
    _ax.set_xlim(1, _n)
    _ax.set_yticks([0, 0.5, 1], ["$0$", "$0.5$", "$1$"])
    _ax.set_xlabel("number of rolls")
    _ax.set_title("relative frequency of even faces", loc="left", color=BLUE, fontsize=13)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([n_rolls, reroll], justify="start", gap=2, wrap=True),
            _fig,
        ]
    )
    return

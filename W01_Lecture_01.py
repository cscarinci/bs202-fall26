import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 1 · Probability basics", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(1, "Probability basics")
    return


@app.cell(hide_code=True)
def _(Figure):
    # Helpers of this lecture: die faces inside text, bare sketches

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
        """Several die faces separated by commas."""
        return ", ".join(die(n) for n in faces)

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    return blank, dice


@app.cell(hide_code=True)
def _(lk, mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    venn_set = mo.ui.dropdown(
        ["A ∪ B", "A ∩ B", "Aᶜ", "A ∪ B ∪ C", "A ∩ B ∩ C", "A ∩ (B ∪ C)", "(A ∩ B) ∪ (A ∩ C)", "A ∪ (B ∩ C)", "(A ∪ B) ∩ (A ∪ C)",
         "(A ∪ B)ᶜ", "Aᶜ ∩ Bᶜ", "(A ∩ B)ᶜ", "Aᶜ ∪ Bᶜ"],
        value="A ∪ B",
        label="set",
        allow_select_none=False,
    )
    total = lk.slider(2, 12, step=1, value=7, label="$A$: faces add to")
    face = lk.slider(1, 6, step=1, value=5, label="$B$: at least one face is")
    die_preset = mo.ui.dropdown({"fair": (1, 1, 1, 1, 1, 1), "not fair": (0, 0, 0, 0, 0, 1)}, value="fair", label="die", allow_select_none=False)
    n_rolls = lk.slider(10, 5000, step=10, value=500, label="number of rolls")
    reroll = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Roll again")
    return die_preset, face, n_rolls, reroll, total, venn_set


@app.cell(hide_code=True)
def _(die_preset, lk, mo):
    # the weights of the six faces, starting from the chosen die
    weights = mo.ui.array([mo.ui.slider(0, 10, step=1, value=w, label=f"${i + 1}$", show_value=True, orientation="vertical") for i, w in enumerate(die_preset.value)])
    return (weights,)


@app.cell(hide_code=True)
def _(lk):
    # module: basics
    # motivation
    lk.prose(r"$\leadsto$ &nbsp; mathematical language used to describe unpredictable phenomena")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: basics
    # references
    lk.references("WMS 2.1–2.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: basics
    # definition: random experiment
    lk.definition(
        [
            r"A **random experiment** is a *repeatable process*",
            lk.aside(r"whose <span class='lk-mark'>*outcomes cannot be predicted with certainty*</span>", "on any individual trial of the experiment"),
            lk.aside(r"but whose <span class='lk-mark'>*set of possible outcomes is specified in advance*</span>", "all that can happen is known"),
        ],
        label="def-random-experiment",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: basics
    # remark
    lk.prose(r"$\leadsto$ &nbsp; this is the type of phenomena we will deal with")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: basics
    # definition: sample space, events, event space
    lk.definition(
        [
            r"The **sample space** of a random experiment is the set of all possible outcomes &nbsp; $\leadsto$ &nbsp; denoted by $S$",
            r"An **event** of a random experiment is a subset of outcomes satisfying some interesting property &nbsp; $\leadsto$ &nbsp; $A \subseteq S$",
            r"> when we deal with probability (to be defined soon) we should not focus on individual outcomes…",
            lk.aside(
                r"> rather, we focus on <span class='lk-mark'>properties that we wish to see</span>",
                r"if the outcome of the experiment has a given property,<br>we say “the property has occurred”<br>$\leadsto$ hence the term “event”!",
            ),
            r"The **event space** is the collection of all relevant events &nbsp; $\leadsto$ &nbsp; denoted $\mathcal{E}$",
        ],
        title="sample space and events",
        label="def-sample-space",
    )
    return


@app.cell(hide_code=True)
def _(dice, lk):
    # module: basics
    # example: rolling one die
    lk.example(
        [
            r"- repeatable",
            r"- uncertain outcome",
            r"- pre-determined set of outcomes",
            r"> $\Longrightarrow$ &nbsp; rolling a die is a random experiment!",
            lk.gap(),
            rf"$S = \{{$ {dice(range(1, 7))} $\}}$ &nbsp; (sample space)",
            rf"$A = \{{$ {dice((2, 4, 6))} $\}}$ &nbsp; (event “even faces”)",
            lk.aside(rf"$B = \{{$ {dice((2,))} $\}}$ &nbsp; (event “face = two”)", "simple event<br>set with one element ≠ the element itself"),
            lk.aside(
                rf"$\mathcal{{E}} = \big\{{ \emptyset, \{{$ {dice((1,))} $\}}, \{{$ {dice((2,))} $\}} = B, \dots, \{{$ {dice((2, 4, 6))} $\}} = A, \dots, \{{$ {dice((1,))}$, \dots,$ {dice((6,))} $\}} \big\}}$",
                "all subsets of outcomes",
            ),
        ],
        title="rolling one die",
        label="ex-one-die",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: algebra of events
    # section
    lk.section("Algebra of events (basic operations of set theory)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: algebra of events
    # definition: union, intersection, complement
    lk.definition(
        [
            r"Given $A, B \subseteq S$",
            r"""
            $$
            \begin{aligned}
            &\bullet \ \ A \cup B = \text{outcomes in } A \ \textit{or} \text{ in } B && (\text{union})\\
            &\bullet \ \ A \cap B = \text{outcomes in } A \ \textit{and} \text{ in } B \qquad && (\text{intersection})\\
            &\bullet \ \ A^c = \text{outcomes } \textit{not} \text{ in } A && (\text{complement})
            \end{aligned}
            $$
            """,
        ],
        label="def-set-operations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: algebra of events
    # consequences: disjoint and exhaustive events
    lk.prose(
        lk.aside(r"$\leadsto$ &nbsp; $A$ and $B$ are **disjoint** (mutually exclusive) when $A \cap B = \mk{\emptyset}$", r"$\emptyset$ = empty set"),
        r"$\leadsto$ &nbsp; $A$ and $B$ are **exhaustive** (cover all outcomes) when $A \cup B = S$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: algebra of events
    # theorem: laws of set theory
    lk.theorem(
        r"""
        $$
        \begin{aligned}
        &\begin{cases} A \cup B = B \cup A \\ A \cap B = B \cap A \end{cases} && (\text{commutativity})\\[6pt]
        &\begin{cases} (A \cup B) \cup C = A \cup (B \cup C) \\ (A \cap B) \cap C = A \cap (B \cap C) \end{cases} && (\text{associativity})\\[6pt]
        &\begin{cases} A \cap (B \cup C) = (A \cap B) \cup (A \cap C) \\ A \cup (B \cap C) = (A \cup B) \cap (A \cup C) \end{cases} \qquad && (\text{distributivity})\\[6pt]
        &\begin{cases} (A \cup B)^c = A^c \cap B^c \\ (A \cap B)^c = A^c \cup B^c \end{cases} && (\text{De Morgan's Law})
        \end{aligned}
        $$
        """,
        title="laws of set theory",
        label="thm-set-laws",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, np, venn_set):
    # module: algebra of events
    # exercise hint, with the sketch of S, A, B, C: the chosen set is shaded
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
    _fig = Figure(figsize=(3.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.set_title("$" + _choice.replace("∪", r"\cup").replace("∩", r"\cap").replace("ᶜ", "^c") + "$", fontsize=14)
    _ax.contourf(_X, _Y, _sets[_choice].astype(float), levels=[0.5, 1.5], colors=[lk.LIGHT])
    for _name, _col, _lx, _ly in (("A", lk.BLUE, 0.72, 1.72), ("B", lk.RED, 2.45, 1.72), ("C", lk.ORANGE, 2.08, 0.3)):
        _cx, _cy, _r = _circles[_name]
        _ax.plot(_cx + _r * np.cos(_th), _cy + _r * np.sin(_th), color=_col, lw=1.4)
        _ax.text(_lx, _ly, f"${_name}$", color=_col, fontsize=13, ha="center", va="center")
    _ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.1, 2.1, 0], color="black", lw=1.0)
    _ax.text(0.2, 0.2, "$S$", fontsize=13, ha="center", va="center")
    _ax.set_xlim(-0.05, 3.25)
    _ax.set_ylim(-0.05, 2.15)
    _ax.set_aspect("equal")
    _ax.axis("off")
    lk.prose(
        r"$\leadsto$ &nbsp; exercise: convince yourself using diagrams",
        lk.interactive(_fig, controls=[venn_set]),
    )
    return


@app.cell(hide_code=True)
def _(blank, dice, face, lk, math, np, total):
    # module: algebra of events
    # example: two dice, A = faces add to 7, B = at least one face is 5, with the grid of outcomes; the sliders
    # change the sum and the face
    _t, _k = total.value, face.value

    def _loop(ax, p, q, r, color):
        """Closed outline at distance r around the segment from p to q (a circle when p = q)."""
        a = math.atan2(q[1] - p[1], q[0] - p[0])
        s = np.linspace(-np.pi / 2, np.pi / 2, 40)
        xs = np.concatenate([q[0] + r * np.cos(a + s), p[0] + r * np.cos(a + np.pi + s)])
        ys = np.concatenate([q[1] + r * np.sin(a + s), p[1] + r * np.sin(a + np.pi + s)])
        ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=color, lw=1.4)

    _fig, _ax = blank(3.2, 3.2, (-1.35, 7.55), (-1.35, 7.55))
    lk.arrow(_ax, (-0.4, 0), (7.3, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.4), (0, 7.3), "black", lw=0.9)
    for _i in range(1, 7):
        _ax.plot([_i, _i], [-0.07, 0.07], color="black", lw=0.9)
        _ax.plot([-0.07, 0.07], [_i, _i], color="black", lw=0.9)
        _ax.text(_i, -0.2, f"${_i}$", fontsize=12, ha="center", va="top")
        _ax.text(-0.2, _i, f"${_i}$", fontsize=12, ha="right", va="center")
    _ax.text(3.5, -0.85, "1st die", fontsize=12, ha="center", va="top")
    _ax.text(-0.85, 3.5, "2nd die", fontsize=12, ha="right", va="center", rotation=90)
    _inA = [(_i, _t - _i) for _i in range(max(1, _t - 6), min(6, _t - 1) + 1)]
    for _p in [(_i, _j) for _i, _j in _inA if _k in (_i, _j)]:
        _ax.fill(_p[0] + 0.3 * np.cos(np.linspace(0, 2 * np.pi, 60)), _p[1] + 0.3 * np.sin(np.linspace(0, 2 * np.pi, 60)), color=lk.LIGHT, lw=0)
    for _i in range(1, 7):
        for _j in range(1, 7):
            _ax.plot(_i, _j, "o", ms=2.5, color="black")
    _loop(_ax, _inA[0], _inA[-1], 0.36, lk.BLUE)
    _loop(_ax, (1, _k), (6, _k), 0.3, lk.RED)
    _loop(_ax, (_k, 1), (_k, 6), 0.3, lk.RED)
    # the label of A goes beyond the upper-left end of its loop: above the grid when that end is in the top row
    _la = (_inA[0][0] - 0.6, 6.85) if _t >= 7 else (0.36, _inA[0][1] + 0.55)
    _ax.text(*_la, "$A$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _ax.text(6.75, _k, "$B$", color=lk.RED, fontsize=13, ha="center", va="center")
    _ax.text(7.1, 7.1, "$S$", fontsize=13, ha="center", va="center")

    lk.example(
        [
            rf"$S = \{{$ {dice(range(1, 7))} $\}} \times \{{$ {dice(range(1, 7))} $\}}$",
            r"$A = \{\text{faces add to } 7\}, \quad B = \{\text{at least one face is } 5\}$",
            rf"$A \cap B = \{{ ($ {dice((2,))}$,$ {dice((5,))} $), ($ {dice((5,))}$,$ {dice((2,))} $) \}}$",
            lk.interactive(_fig, controls=[total, face]),
        ],
        title="rolling two dice",
        label="ex-two-dice",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: axioms
    # section
    lk.section("Axioms of probability")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: axioms
    # definition: probability measure
    lk.definition(
        [
            r"Given a random experiment, we define probability as a measure of events relative to the sample space.",
            r"Precisely: Given $(S, \mathcal{E})$, a **probability measure** is",
            r"$P : \mathcal{E} \longrightarrow \mathbb{R}$ &nbsp; such that",
            r"""
            $$
            \begin{aligned}
            &\bullet \ \ P(S) = 1\\
            &\bullet \ \ P(A) \geq 0 \quad \text{for every event } A \in \mathcal{E}\\
            &\bullet \ \ P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots
            \end{aligned}
            $$
            """,
            lk.aside(
                r"> > for every countable sequence of <span class='lk-mark'>pairwise disjoint</span> events $A_1, A_2, \dots$",
                r"pairwise disjoint: $A_i \cap A_j = \emptyset \ \ \forall\, i \neq j$",
            ),
        ],
        label="def-probability-measure",
    )
    return


@app.cell(hide_code=True)
def _(blank, lk, np):
    # module: axioms
    # illustration: three disjoint events, with a sketch
    _fig, _ax = blank(3.2, 2.1, (-0.05, 3.4), (-0.05, 2.05))
    _th = np.linspace(0, 2 * np.pi, 200)
    for (_cx, _cy, _r), _col, _name in (((0.75, 1.3, 0.52), lk.BLUE, "$A_1$"), ((2.3, 1.5, 0.38), lk.RED, "$A_2$"), ((1.7, 0.65, 0.52), lk.ORANGE, "$A_3$")):
        _ax.plot(_cx + _r * np.cos(_th), _cy + _r * np.sin(_th), color=_col, lw=1.4)
        _ax.text(_cx, _cy, _name, color=_col, fontsize=13, ha="center", va="center")
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 2, 2, 0], color="black", lw=1.0)
    _ax.text(3.2, 0.12, "$S$", fontsize=13, ha="center", va="center")
    lk.prose(
        lk.figure(_fig),
        r"$$ P(A_1 \cup A_2 \cup A_3) = P(A_1) + P(A_2) + P(A_3) $$",
        r"$\leadsto$ &nbsp; probability is an additive notion of size of events relative to the full sample space",
        r"$\leadsto$ &nbsp; it can be interpreted as the relative frequency of event occurrences in infinite independent trials",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: axioms
    # definition: probability space
    lk.definition(
        lk.aside(r"We call a triple $(S, \mathcal{E}, P)$ a <span class='lk-mark'>**probability space**</span>", "abstract model of a random experiment"),
        label="def-probability-space",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: axioms
    # remark
    lk.prose(r"$\leadsto$ &nbsp; first goal of probability theory is to study properties and give examples of such spaces!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: axioms
    # example: probability measures on one die
    _ub = lambda body, label: r"\underbrace{" + body + r"}_{\scriptstyle " + label + "}"
    lk.example(
        [
            r"$S = \{1, 2, 3, 4, 5, 6\}$",
            r"$$ \mathcal{E} = \big\{ "
            + _ub(r"\{1\}", r"\text{“face is 1”}")
            + r", \dots, \{6\}, "
            + _ub(r"\{1, 2\}", r"\substack{\text{“1 or 2”} \\ = \{1\} \cup \{2\}}")
            + r", \dots, \{5, 6\}, \dots, "
            + _ub(r"\{1, 2, 3, 4, 5, 6\}", r"\text{“1 or 2 or … or 6”}")
            + ", "
            + _ub(r"\emptyset", r"\text{“not (1 or … or 6)”}")
            + r" \big\} $$",
            r"$P = \ ?$",
            r"fair die: &nbsp; $P(\{i\}) = \dfrac{1}{6} \quad \forall\, i = 1, \dots, 6$",
            r"""
            $$
            \begin{aligned}
            \Longrightarrow \quad & P(\{i, j\}) = P(\{i\}) + P(\{j\}) = \frac{2}{6} && \forall\, i \neq j\\[4pt]
            \Longrightarrow \quad & P(\{i, j, k\}) = \frac{3}{6} && \forall\, i \neq j \neq k\\
            & \ \ \vdots
            \end{aligned}
            $$
            """,
            r"> in particular: &nbsp; $P(\{\text{even faces}\}) = \dfrac{3}{6}$",
            lk.gap(),
            r"not fair die (one example): &nbsp; $P(\{6\}) = 1$, &nbsp; $P(\{i\}) = 0$ for $i \neq 6$",
            r"$$ \Longrightarrow \quad P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6 \\ 1, & i = 6 \text{ or } j = 6 \end{cases} $$",
            r"> $P(\{\text{even faces}\}) = 1$",
        ],
        title="rolling one die",
        label="ex-die-measures",
    )
    return


@app.cell(hide_code=True)
def _(Figure, die_preset, lk, mo, np, weights):
    # module: axioms
    # remark: many probability measures, with the weighted die
    _w = np.array(weights.value, dtype=float)
    _total = _w.sum()
    pmf = _w / _total if _total > 0 else None  # the weights define a probability measure only when their total is positive
    _fig = Figure(figsize=(3.4, 2.4), layout="constrained")
    _ax = _fig.subplots()
    if pmf is not None:
        _ax.vlines(range(1, 7), 0, pmf, color=lk.BLUE, lw=1.4)
        _ax.plot(range(1, 7), pmf, "o", color=lk.BLUE, ms=5, clip_on=False, zorder=4)
    _ax.set_xticks(range(1, 7), [f"${k}$" for k in range(1, 7)])
    _ax.set_xlim(0.4, 6.6)
    _ax.set_ylim(0, 1.05)
    _ax.set_yticks([0, 0.5, 1], ["$0$", "$0.5$", "$1$"])
    _ax.set_xlabel("face $i$")
    _ax.set_ylabel(r"$P(\{i\})$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    lk.prose(
        r"$\leadsto$ &nbsp; there can be many distinct probability measures on the same sample space / event space",
        lk.interactive(_fig, controls=[die_preset, *weights]),
    )
    return (pmf,)


@app.cell(hide_code=True)
def _(Figure, lk, n_rolls, np, pmf, reroll):
    # module: axioms
    # illustration: relative frequency of even faces in repeated rolls of the die above
    _rng = np.random.default_rng(202 + reroll.value)
    _n = n_rolls.value
    _fig = Figure(figsize=(lk.FULL, 2.6), layout="constrained")
    _ax = _fig.subplots()
    if pmf is not None:
        _p = float(pmf[1::2].sum())
        _even = _rng.choice(np.arange(1, 7), size=_n, p=pmf) % 2 == 0
        _freq = np.cumsum(_even) / np.arange(1, _n + 1)
        _ax.plot(np.arange(1, _n + 1), _freq, color=lk.BLUE, lw=1.4, zorder=4)
        _ax.axhline(_p, color=lk.RED, lw=1.0, zorder=3)
        _ax.text(1.01, _p, r"$P(\{\mathrm{even\ faces}\})$", transform=_ax.get_yaxis_transform(), color=lk.RED, fontsize=13, ha="left", va="center")
    _ax.set_ylim(-0.05, 1.05)
    _ax.set_xlim(1, _n)
    _ax.set_yticks([0, 0.5, 1], ["$0$", "$0.5$", "$1$"])
    _ax.set_xlabel("number of rolls")
    _ax.set_ylabel("relative frequency\nof even faces")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    lk.prose(lk.interactive(_fig, controls=[n_rolls, reroll]))
    return


if __name__ == "__main__":
    app.run()

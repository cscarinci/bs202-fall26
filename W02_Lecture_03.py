import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 03 · Conditioning, independence, and Bayes' rule", css_file="bs202.css")


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
    header("Lecture 03", "Week 02", "Lecture 03 · Conditioning, independence, and Bayes' rule")
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

    - probability spaces with equally likely outcomes: &nbsp; $P(A) = \dfrac{\# A}{\# S}$ &nbsp; $\leadsto$ &nbsp; calculating probability reduces to counting
    - basic counting rules ($n$ objects, $r$ positions):
    - **ordered** without repetitions: &nbsp; $P^n_r = \dfrac{n!}{(n - r)!}$ &nbsp; (ranking of a competition)
    - **unordered** without repetitions: &nbsp; $C^n_r = \dfrac{n!}{r!\,(n - r)!}$ &nbsp; (hands of poker)
    - **ordered** with repetitions: &nbsp; $n^r = n \times n \times \cdots \times n$ &nbsp; (passwords of given length)
    - **unordered** with repetitions: &nbsp; $C^{n + r - 1}_r = \dfrac{(n + r - 1)!}{r!\,(n - 1)!}$ &nbsp; (ice cream cups)

        $$
        \text{e.g.} \quad \#\left(\substack{\text{cups of 4 scoops} \\ \text{from 6 flavours}}\right) = C^{6 + 4 - 1}_4 = C^9_4 = \frac{9!}{4!\, 5!} = 126
        $$

    - **Example** (defective items). 20 items, 3 defective &nbsp; $\leadsto$ &nbsp; pick 4 (samples): &nbsp; $P(\text{at least one is defective}) = \ ?$ &nbsp; (not easy to compute…)

        $$
        \{\text{at least 1}\} = \{\text{exactly 1}\} \cup \{\text{exactly 2}\} \cup \{\text{exactly 3}\} = \{\text{none}\}^c
        \qquad \leadsto \quad \#\{\text{none}\} = C^{17}_4 = \frac{17!}{4!\, 13!}
        $$

        $$
        \Longrightarrow \qquad P(\text{at least one}) = 1 - \frac{\ \dfrac{17!}{4!\, 13!}\ }{\dfrac{20!}{4!\, 16!}} = 1 - \frac{17!\, 16!}{20!\, 13!} \approx 50.9\%
        $$

    **In this lecture:** how knowledge about one event changes the probability of another
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, LIGHT, RED, table):
    def outcome_grid(left=0.1):
        """The 36 outcomes of two dice as a grid of dots: 1st die across, 2nd die up."""
        fig = Figure(figsize=(HALF, HALF), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(left, 7.1)
        ax.set_ylim(0.1, 7.1)
        ax.set_aspect("equal")
        ax.set_xticks(range(1, 7))
        ax.set_yticks(range(1, 7))
        ax.set_xlabel("1st")
        ax.set_ylabel("2nd")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for i in range(1, 7):
            for j in range(1, 7):
                ax.plot(i, j, "o", ms=3, color="black", zorder=4)
        return fig, ax

    def strip(ax, k, color, label, across=False):
        """Outline the outcomes with 1st die = k (or 2nd die = k when `across`), labelled outside the grid."""
        x = [k - 0.32, k + 0.32, k + 0.32, k - 0.32, k - 0.32]
        y = [0.6, 0.6, 6.4, 6.4, 0.6]
        if across:
            ax.plot(y, x, color=color, lw=1.4)
            ax.text(6.75, k, label, color=color, fontsize=13, ha="center", va="center")
        else:
            ax.plot(x, y, color=color, lw=1.4)
            ax.text(k, 6.75, label, color=color, fontsize=13, ha="center", va="center")

    def _frac(n, d):
        from fractions import Fraction

        q = Fraction(n, d)
        reduced = rf"\dfrac{{{q.numerator}}}{{{q.denominator}}}" if q.denominator != 1 else str(q.numerator)
        return rf"\dfrac{{{n}}}{{{d}}}" + ("" if q.denominator == d else " = " + reduced)

    def cond_panel(t, verdict=False):
        """Two-dice outcomes with A = {sum is t} circled and B = {1st is even} outlined;
        readout of P(A), P(A | B), P(B | A), optionally with the independence verdict."""
        fig, ax = outcome_grid()
        for k in (2, 4, 6):
            strip(ax, k, RED, "$B$")
        nA = nAB = 0
        for i in range(1, 7):
            j = t - i
            if 1 <= j <= 6:
                nA += 1
                nAB += i % 2 == 0
                ax.plot(i, j, "o", ms=15, mfc=LIGHT if i % 2 == 0 else "white", mec=BLUE, mew=1.4, zorder=3)
        i0 = max(1, t - 6)  # the circled outcome with the largest 2nd die carries the label
        ax.text(i0 + (0.45 if i0 % 2 else -0.56), t - i0 + (0.36 if i0 % 2 else 0.3), "$A$", color=BLUE, fontsize=13, ha="center", va="center", zorder=5)

        rows = [
            (rf"$\textcolor{{{BLUE}}}{{\# A}}$ &nbsp; ($A$ = sum is ${t}$)", rf"$\textcolor{{{BLUE}}}{{{nA}}}$"),
            (rf"$\textcolor{{{RED}}}{{\# B}}$ &nbsp; ($B$ = 1st is even)", rf"$\textcolor{{{RED}}}{{18}}$"),
            (r"$\# A \cap B$", rf"${nAB}$"),
            (r"$P(A) = \dfrac{\# A}{\# S}$", rf"${_frac(nA, 36)}$"),
            (r"$P(A \mid B) = \dfrac{\# A \cap B}{\# B}$", rf"${_frac(nAB, 18)}$"),
            (r"$P(B \mid A) = \dfrac{\# A \cap B}{\# A}$", rf"${_frac(nAB, nA)}$"),
        ]
        if verdict:
            same = nAB * 36 == nA * 18
            rows.append((r"$A, B$ independent", r"yes: $P(A \mid B) = P(A)$" if same else r"no: $P(A \mid B) \neq P(A)$"))
        return table(rows), fig

    return cond_panel, outcome_grid, strip


@app.cell(hide_code=True)
def _(BLUE, HALF, LIGHT, RED, blank, definition, mo, np, theorem):
    _fig, _ax = blank(HALF, 2.5, (-0.1, 3.7), (-0.1, 2.6))
    _th = np.linspace(0, 2 * np.pi, 240)
    _cx, _cy = 1.2 + 0.72 * np.cos(_th), 0.95 + 0.72 * np.sin(_th)
    _ax.fill(np.maximum(_cx, 0.95), np.maximum(_cy, 0.6), color=LIGHT, lw=0)  # A ∩ B (the corner of B lies inside A)
    _ax.plot(_cx, _cy, color=BLUE, lw=1.4)
    _ax.plot([0.95, 3.3, 3.3, 0.95, 0.95], [0.6, 0.6, 2.3, 2.3, 0.6], color=RED, lw=1.4)
    _ax.plot([0, 3.6, 3.6, 0, 0], [0, 0, 2.5, 2.5, 0], color="black", lw=1.0)
    _ax.text(0.3, 1.5, "$A$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.text(3.05, 0.85, "$B$", color=RED, fontsize=13, ha="center", va="center")
    _ax.text(3.45, 0.22, "$S$", fontsize=13, ha="center", va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.3 &nbsp; Conditioning, independence, and Bayes' rule (WMS 2.7–2.10)

    ### Conditional probability

    $\leadsto$ &nbsp; the probability of an event might change depending on our knowledge about the occurrence of other events!

    $$
    \text{roll two fair dice:} \qquad P(\text{sum is 8}) = \tfrac{5}{36}, \qquad P\left(\substack{\text{sum is 8 when} \\ \text{1st die is even}}\right) = \tfrac{3}{18} = \tfrac{1}{6}
    $$
    """
            ),
            definition(
                r"""
    The **conditional probability** of an event $A \subseteq S$, given that an event $B$ is known to have occurred, is

    $$
    \underbrace{P(A \mid B)}_{\text{probability of } A \text{ given } B} = \frac{P(A \cap B)}{P(B)} \qquad (\text{provided } P(B) > 0)
    $$
    """,
                "Conditional probability",
            ),
            _fig,
            mo.md(
                r"""
    Once we know $B$ has occurred

    $$
    P(A) \qquad \leadsto \qquad P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad
    P(B) \qquad \leadsto \qquad P(B \mid B) = \frac{P(B \cap B)}{P(B)} = 1
    $$

    $$
    \leadsto \qquad P(S \mid B) = \frac{P(S \cap B)}{P(B)} = 1
    $$

    $\leadsto$ &nbsp; for the purpose of calculating $P(A \mid B)$, we think of $B$ as the “new version” of $S$, and of $A \cap B$ as the “new version” of $A$ inside $B$
    """
            ),
            theorem(
                r"""
    Given $A, B \subseteq S$, with $P(B) > 0$

    - $P(A \mid B) \geq 0$
    - $P(B \mid B) = 1$
    - $P(A_1 \cup A_2 \mid B) = P(A_1 \mid B) + P(A_2 \mid B)$ &nbsp; for $(A_1 \cap B) \cap (A_2 \cap B) = \emptyset$ &nbsp; (also true for countably many)

    that is, $P(\,\cdot \mid B)$ is a probability measure on events $A \cap B$!
    """,
                "Conditional probability is a probability measure",
            ),
            mo.md(
                r"""
    **Example.**

    $A = \{\text{sum is 8}\} = \{(2, 6), (3, 5), (4, 4), (5, 3), (6, 2)\}$ &nbsp; $\leadsto$ &nbsp; $\# A = 5$

    $B = \{\text{1st is even}\} = \{(2, 1), (2, 2), \dots, (4, 1), (4, 2), \dots, (6, 5), (6, 6)\}$ &nbsp; $\leadsto$ &nbsp; $\# B = 3 \times 6 = 18$

    $A \cap B = \{(2, 6), (4, 4), (6, 2)\}$ &nbsp; $\leadsto$ &nbsp; $\# A \cap B = 3$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    total = mo.ui.slider(2, 12, 1, value=8, label="$A$: sum is", show_value=True)
    return (total,)


@app.cell(hide_code=True)
def _(cond_panel, mo, total):
    _table, _fig = cond_panel(total.value)
    mo.vstack([mo.hstack([total], justify="start", gap=2, wrap=True), _table, _fig])
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** In general $P(A \mid B) \neq P(B \mid A)$

    $$
    P(\text{sum is 8} \mid \text{1st is even}) = \tfrac{1}{6} \ \neq \ P(\text{1st is even} \mid \text{sum is 8}) = \tfrac{3}{5}
    $$

    **Remark.** Many times it is useful to read

    $$
    P(A \cap B) = P(A \mid B)\, P(B)
    $$

    $$
    \leadsto \qquad P\left(\substack{\text{sum is 8 and} \\ \text{1st is even}}\right) = \underbrace{P\left(\substack{\text{sum is 8 given} \\ \text{1st is even}}\right)}_{\text{2nd stage}}\ \underbrace{P(\text{1st is even})}_{\text{1st stage}} \qquad (\text{stages of the random experiment})
    $$

    $\leadsto$ &nbsp; generalizations:

    $$
    P(A \cap B \cap C) = P(A \mid B \cap C)\, P(B \cap C) = P(A \mid B \cap C)\, P(B \mid C)\, P(C)
    $$

    $$
    \begin{aligned}
    \underbrace{P(A_1 \cap A_2 \cap \cdots \cap A_n)}_{n \text{ stages}} = {} & \underbrace{P(A_1 \mid A_2 \cap \cdots \cap A_n)}_{n\text{th}} \\
    & \times \underbrace{P(A_2 \mid A_3 \cap \cdots \cap A_n)}_{(n-1)\text{th}} \cdots \underbrace{P(A_{n-1} \mid A_n)}_{\text{2nd}}\ \underbrace{P(A_n)}_{\text{1st}}
    \end{aligned}
    $$

    **Remark.** Here we see another possible interpretation of probability:

    from “relative frequency of event occurrences in infinitely many trials of an experiment” (frequentist interpretation)

    to “measure of belief in the likelihood of event occurrences in each trial of an experiment” (Bayesian interpretation)

    $\leadsto$ &nbsp; if $P(A)$ is our original measure of belief about $A$, $P(A \mid B)$ is our updated measure of belief about $A$ given new knowledge about $B$!

    ### Independent events
    """
            ),
            definition(
                r"""
    Two events $A, B \subseteq S$ are called **independent** if

    $$
    P(A \mid B) = P(A) \qquad \Longleftrightarrow \qquad P(A \cap B) = P(A)\, P(B) \qquad \Longleftrightarrow \qquad P(B \mid A) = P(B)
    $$

    (knowledge about $B$ does not influence our belief about $A$; the conditional forms require $P(B) > 0$, $P(A) > 0$)
    """,
                "Independent events",
            ),
            mo.md(
                r"""
    **Example.** two fair dice &nbsp; $\leadsto$ &nbsp; $S = \{(1, 1), \dots, (6, 6)\}$

    $A$ = sum is 7 $= \{(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)\}$ &nbsp; and &nbsp; $B$ = 1st is even $= \{(2, 1), (2, 2), \dots, (6, 5), (6, 6)\}$ &nbsp; are independent:

    $$
    P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{3/36}{18/36} = \frac{1}{6} = \frac{6}{36} = P(A)
    $$

    $\leadsto$ &nbsp; if $A$ = “sum is 8”, relative counting changes if we know $B$ = “1st is even” &nbsp; $\Longrightarrow$ &nbsp; $A, B$ not independent

    $\leadsto$ &nbsp; if $A$ = “sum is 7”, relative counting remains same if we know $B$ = “1st is even” &nbsp; $\Longrightarrow$ &nbsp; $A, B$ independent
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    total_ind = mo.ui.slider(2, 12, 1, value=7, label="$A$: sum is", show_value=True)
    return (total_ind,)


@app.cell(hide_code=True)
def _(cond_panel, mo, total_ind):
    _table, _fig = cond_panel(total_ind.value, verdict=True)
    mo.vstack([mo.hstack([total_ind], justify="start", gap=2, wrap=True), _table, _fig])
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** independence $\neq$ mutually exclusive!

    $$
    P(A \cap B) = P(A)\, P(B) \qquad \not\Longleftrightarrow \qquad A \cap B = \emptyset
    $$

    $$
    A \cap B = \emptyset \qquad \Longrightarrow \qquad P(A \cap B) = 0 \qquad \Longrightarrow \qquad \text{not independent if } P(A) \neq 0 \text{ and } P(B) \neq 0
    $$
    """
            ),
            theorem(
                r"""
    If $A$ and $B$ are independent, then so are $A$ and $B^c$, &nbsp; $A^c$ and $B$, &nbsp; $A^c$ and $B^c$.
    """,
                "Independence of complements",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    P(A^c \cap B) = P(A^c \mid B)\, P(B) = \big( 1 - P(A \mid B) \big)\, P(B) = \big( 1 - P(A) \big)\, P(B) = P(A^c)\, P(B) \qquad \square
    $$
    """
            ),
            definition(
                r"""
    $A, B, C \subseteq S$ are **pairwise independent** if

    $$
    \underbrace{P(A \cap B) = P(A)\, P(B), \qquad P(B \cap C) = P(B)\, P(C), \qquad P(C \cap A) = P(C)\, P(A)}_{\text{each pair is independent}}
    $$

    $A, B, C \subseteq S$ are **mutually independent** if they are pairwise independent and

    $$
    P(A \cap B \cap C) = P(A)\, P(B)\, P(C)
    $$
    """,
                "Pairwise and mutual independence",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, mo, outcome_grid, strip):
    _fig, _ax = outcome_grid(left=-0.4)
    _A, _B, _C = set(), set(), set()
    for _i in range(1, 7):
        for _j in range(1, 7):
            if _i % 2 == 1:
                _A.add((_i, _j))
            if _j % 2 == 1:
                _B.add((_i, _j))
            if (_i + _j) % 2 == 1:
                _C.add((_i, _j))
                _ax.plot(_i, _j, "D", ms=9, mfc="none", mec=GREEN, mew=1.4, zorder=3)
    for _k in (1, 3, 5):
        strip(_ax, _k, BLUE, "$A$")
        strip(_ax, _k, RED, "$B$", across=True)
    for _k in (2, 4, 6):
        _ax.text(0.15, _k, "$C$", color=GREEN, fontsize=13, ha="center", va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** Pairwise does not imply mutual independence!

    **Example.** Roll two dice

    $$
    A = \{\text{1st is odd}\}, \qquad B = \{\text{2nd is odd}\}, \qquad C = \{\text{sum is odd}\}
    $$

    $$
    P(A) = \frac{3 \times 6}{36}, \qquad P(B) = \frac{3 \times 6}{36}, \qquad P(C) = \frac{18}{36}
    $$

    $$
    P(A \cap B) = \frac{9}{36} = P(A)\, P(B), \qquad P(B \cap C) = \frac{9}{36} = P(B)\, P(C), \qquad P(C \cap A) = \frac{9}{36} = P(C)\, P(A)
    $$

    $$
    P(A \cap B \cap C) = 0
    $$
    """
            ),
            _fig,
            mo.md(
                rf"""
    $$
    \# A = {len(_A)}, \quad \# B = {len(_B)}, \quad \# C = {len(_C)}
    $$

    $$
    \# A \cap B = {len(_A & _B)}, \quad \# B \cap C = {len(_B & _C)}, \quad \# C \cap A = {len(_C & _A)}, \qquad \underbrace{{\# A \cap B \cap C = {len(_A & _B & _C)}}}_{{\text{{odd + odd is even}}}}
    $$

    $\leadsto$ &nbsp; knowledge about $A$ does not affect our belief in $C$; &nbsp; $B$ does not affect our belief in $C$; &nbsp; knowledge about **$A$ and $B$** affects our belief in $C$!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bayes' rule

    $\leadsto$ &nbsp; updating our level of belief in a collection of hypotheses after a new event has occurred

    **Example.** A disease affects 1% of a population &nbsp; $\leadsto$ &nbsp; $P(\text{have disease}) = 1\%$ &nbsp; (disease prevalence)

    A test has 90% **sensitivity** $P(+\text{ve} \mid \text{disease})$ (true positive rate) and 95% **specificity** $P(-\text{ve} \mid \text{no disease})$ (true negative rate)

    $\leadsto$ &nbsp; what is the probability of having the disease given a positive test?

    $$
    \left.\begin{aligned} D &= \text{has disease} \\ D^c &= \text{doesn't have disease} \end{aligned}\right\} \quad P(D) = 1\%, \quad P(D^c) = 99\%
    $$

    $$
    \left.\begin{aligned} T &= \text{tested positive} \\ T^c &= \text{tested negative} \end{aligned}\right\} \quad P(T \mid D) = 90\%, \quad \underbrace{P(T^c \mid D^c) = 95\%}_{P(T \mid D^c) \,=\, 5\%}
    $$

    $$
    \leadsto \qquad P(D \mid T) = \ ?
    $$

    $$
    \begin{aligned}
    \text{Bayes' rule:} \qquad P(D \mid T) &= \frac{P(D \cap T)}{P(T)} = \frac{P(T \mid D)\, P(D)}{P(T)} \\[10pt]
    &= \frac{P(T \mid D)\, P(D)}{P(T \cap D) + P(T \cap D^c)} = \frac{P(T \mid D)\, P(D)}{P(T \mid D)\, P(D) + P(T \mid D^c)\, P(D^c)} \\[10pt]
    &= \frac{0.9 \times 0.01}{0.9 \times 0.01 + 0.05 \times 0.99} = \frac{2}{13} \approx 15.4\%
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    prev = mo.ui.slider(0.1, 50, 0.1, value=1, label="prevalence $P(D)$ (%)", show_value=True)
    sens = mo.ui.slider(50, 100, 0.5, value=90, label=r"sensitivity $P(T \mid D)$ (%)", show_value=True)
    spec = mo.ui.slider(50, 100, 0.5, value=95, label=r"specificity $P(T^c \mid D^c)$ (%)", show_value=True)
    return prev, sens, spec


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, LIGHT, RED, mo, prev, sens, spec, table):
    _p, _se, _sp = prev.value / 100, sens.value / 100, spec.value / 100
    _tp, _fp = _se * _p, (1 - _sp) * (1 - _p)
    _post = _tp / (_tp + _fp)  # P(T) > 0 on the whole slider range

    _fig = Figure(figsize=(FULL, 1.5), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill([0, _tp, _tp, 0], [0, 0, 1, 1], color=LIGHT, lw=0)
    _ax.plot([_tp, _tp + _fp, _tp + _fp, _tp, _tp], [0, 0, 1, 1, 0], color=RED, lw=1.4)
    _ax.plot([0, _tp, _tp, 0, 0], [0, 0, 1, 1, 0], color=BLUE, lw=1.4)
    _ax.text(0, 1.25, r"$P(T \cap D)$", color=BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(_tp + _fp, 1.25, r"$P(T \cap D^c)$", color=RED, fontsize=13, ha="right", va="bottom")
    _ax.set_xlim(-0.01 * (_tp + _fp), 1.01 * (_tp + _fp))
    _ax.set_ylim(-0.1, 2.0)
    _ax.set_yticks([])
    _ax.set_xlabel(r"$P(T) = P(T \cap D) + P(T \cap D^c)$")
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _N = 1_000_000  # every count below is then a whole number for all slider positions

    def _n(v):
        return f"{round(v):,}".replace(",", r"\,")

    _nD = _N * _p

    mo.vstack(
        [
            mo.hstack([prev, sens, spec], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$P(D \mid T) = \dfrac{P(T \mid D)\, P(D)}{P(T \mid D)\, P(D) + P(T \mid D^c)\, P(D^c)}$", rf"$\dfrac{{{_se:g} \times {_p:g}}}{{{_se:g} \times {_p:g} + {1 - _sp:.3g} \times {1 - _p:g}}} \approx {100 * _post:.1f}\%$"),
                    (r"out of $1\,000\,000$ people: have the disease ($D$)", rf"${_n(_nD)}$"),
                    (r"&nbsp;&nbsp; of which test positive ($T \cap D$)", rf"$\textcolor{{{BLUE}}}{{{_n(_nD * _se)}}}$"),
                    (r"do not have the disease ($D^c$)", rf"${_n(_N - _nD)}$"),
                    (r"&nbsp;&nbsp; of which test positive ($T \cap D^c$)", rf"$\textcolor{{{RED}}}{{{_n((_N - _nD) * (1 - _sp))}}}$"),
                    (r"test positive in total ($T$)", rf"${_n(_N * (_tp + _fp))}$"),
                    (r"$P(D \mid T)$ = positives with the disease / all positives", rf"${100 * _post:.1f}\%$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    More generally:

    If $S = B_1 \cup B_2 \cup \cdots \cup B_k$ with $B_i \cap B_j = \emptyset$ for $i \neq j$

    $\leadsto$ &nbsp; $\{B_1, B_2, \dots, B_k\}$ is an exhaustive, mutually exclusive collection of events &nbsp; (a **partition** of $S$)

    $$
    P(A) = \sum_{i=1}^{k} P(A \mid B_i)\, P(B_i) \qquad (\text{law of total probability})
    $$

    $$
    P(B_j \mid A) = \frac{P(A \mid B_j)\, P(B_j)}{\displaystyle\sum_{i=1}^{k} P(A \mid B_i)\, P(B_i)} \qquad (\text{Bayes' rule})
    $$

    $P(B_i)$ = **prior**, &nbsp; $P(B_i \mid A)$ = **posterior**, &nbsp; $P(A \mid B_i)$ = **likelihood**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - conditional probability $P(A \mid B) = \dfrac{P(A \cap B)}{P(B)}$ (for $P(B) > 0$): $B$ is the “new version” of $S$, and $P(\,\cdot \mid B)$ is again a probability measure; in general $P(A \mid B) \neq P(B \mid A)$
    - multiplication by stages: $P(A \cap B) = P(A \mid B)\, P(B)$, and $P(A \cap B \cap C) = P(A \mid B \cap C)\, P(B \mid C)\, P(C)$
    - $A, B$ independent if $P(A \cap B) = P(A)\, P(B)$ (not the same as mutually exclusive!); pairwise independence does not imply mutual independence
    - for a partition $\{B_1, \dots, B_k\}$ of $S$: law of total probability $P(A) = \sum_{i} P(A \mid B_i)\, P(B_i)$ and Bayes' rule $P(B_j \mid A) = \dfrac{P(A \mid B_j)\, P(B_j)}{\sum_{i} P(A \mid B_i)\, P(B_i)}$ (posterior from prior and likelihood)

    **Next:** random variables
    """)
    return


if __name__ == "__main__":
    app.run()

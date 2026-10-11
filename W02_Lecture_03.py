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
    header("Lecture 03", "Week 02", "Lecture 03 · Conditioning, independence, and Bayes' rule")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Probability spaces with equally likely outcomes

    $$
    P(A) = \frac{\# A}{\# S} \qquad \leadsto \quad \text{calculating probability reduces to counting}
    $$

    Basic counting rules: $n$ objects, $r$ positions

    | | count | example |
    |:--|:--|:--|
    | **ordered** without repetitions | $P^n_r = \dfrac{n!}{(n - r)!}$ | ranking of a competition |
    | **unordered** without repetitions | $C^n_r = \dfrac{n!}{r!\,(n - r)!}$ | hands of poker |
    | **ordered** with repetitions | $n^r = n \times n \times \cdots \times n$ | passwords of given length |
    | **unordered** with repetitions | $C^{n + r - 1}_r = \dfrac{(n + r - 1)!}{r!\,(n - 1)!}$ | ice cream cups |

    $$
    \text{e.g.} \quad \#\left(\substack{\text{cups of 4 scoops} \\ \text{from 6 flavours}}\right) = C^{6 + 4 - 1}_4 = C^9_4 = \frac{9!}{4!\, 5!} = 126
    $$

    **Example** (defective items).

    20 items, 3 defective &nbsp; $\leadsto$ &nbsp; pick 4 (samples)

    $$
    P(\text{at least one is defective}) = \ ? \qquad (\text{not easy to compute…})
    $$

    $$
    \{\text{at least 1}\} = \{\text{exactly 1}\} \cup \{\text{exactly 2}\} \cup \{\text{exactly 3}\} = \{\text{none}\}^c
    \qquad \leadsto \quad \#\{\text{none}\} = C^{17}_4 = \frac{17!}{4!\, 13!}
    $$

    $$
    \Longrightarrow \quad P(\text{at least one}) = 1 - \frac{\ \dfrac{17!}{4!\, 13!}\ }{\dfrac{20!}{4!\, 16!}} = 1 - \frac{17!\, 16!}{20!\, 13!} \approx 50.9\%
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, definition, mo, np, theorem):
    _fig = Figure(figsize=(3.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _g = np.linspace(0, 1, 300)
    _X, _Y = np.meshgrid(_g * 3.6, _g * 2.5)
    _A = (_X - 1.2) ** 2 + (_Y - 0.95) ** 2 < 0.72**2
    _B = (_X > 0.95) & (_X < 3.3) & (_Y > 0.6) & (_Y < 2.3)
    _ax.contourf(_X, _Y, (_A & _B).astype(float), levels=[0.5, 1.5], colors=[GREEN], alpha=0.45)
    _th = np.linspace(0, 2 * np.pi, 120)
    _ax.plot(1.2 + 0.72 * np.cos(_th), 0.95 + 0.72 * np.sin(_th), color=GREEN, lw=1.6)
    _ax.plot([0.95, 3.3, 3.3, 0.95, 0.95], [0.6, 0.6, 2.3, 2.3, 0.6], color=RED, lw=1.6)
    _ax.plot([0, 3.6, 3.6, 0, 0], [0, 0, 2.5, 2.5, 0], color=BLUE, lw=1.4)
    _ax.text(0.2, 1.5, "$A$", color=GREEN, fontsize=14)
    _ax.text(2.9, 0.75, "$B$", color=RED, fontsize=14)
    _ax.text(3.2, 0.12, "$S$", color=BLUE, fontsize=14)
    _ax.set_aspect("equal")
    _ax.axis("off")

    mo.vstack(
        [
            mo.md(
                r"""
    ## 3 &nbsp; Conditioning, Independence, and Bayes' Rule (WMS 2.7–2.10)

    The probability of an event might change depending on our knowledge about the occurrence of other events!

    $$
    \text{roll two fair dice:} \qquad P(\text{sum is 8}) = \tfrac{5}{36}, \qquad P\left(\substack{\text{sum is 8 when} \\ \text{1st dice is even}}\right) = \tfrac{3}{18} = \tfrac{1}{6}
    $$
    """
            ),
            definition(
                r"""
    The **conditional probability** of an event $A \subseteq S$, given that an event $B$ is known to have occurred, is

    $$
    P(A \mid B) = \frac{P(A \cap B)}{P(B)} \qquad (\text{provided } P(B) > 0)
    $$

    (probability of $A$ given $B$)
    """
            ),
            mo.hstack(
                [
                    _fig,
                    mo.md(
                        r"""
    Once we know $B$ has occurred

    $$
    \begin{aligned}
    P(A) \ &\leadsto \ P(A \mid B) = \frac{P(A \cap B)}{P(B)} \\[4pt]
    P(B) \ &\leadsto \ P(B \mid B) = \frac{P(B \cap B)}{P(B)} = 1 \\[4pt]
    &\phantom{\leadsto} \ \ P(S \mid B) = \frac{P(S \cap B)}{P(B)} = 1
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
    For the purpose of calculating $P(A \mid B)$, we think of $B$ as the “new version” of $S$, and of $A \cap B$ as the “new version” of $A$ inside $B$.
    """
            ),
            theorem(
                r"""
    Given $A, B \subseteq S$, with $P(B) > 0$

    - $P(A \mid B) \geq 0$
    - $P(B \mid B) = 1$
    - $P(A_1 \cup A_2 \mid B) = P(A_1 \mid B) + P(A_2 \mid B)$ &nbsp; for $(A_1 \cap B) \cap (A_2 \cap B) = \emptyset$ &nbsp; (also true for countably many)

    i.e. $P(\,\cdot \mid B)$ is a probability measure on events $A \cap B$!
    """
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
def _(BLUE, Figure, GREEN, RED, mo):
    from fractions import Fraction

    def _frac(q):
        return rf"\tfrac{{{q.numerator}}}{{{q.denominator}}}" if q.denominator != 1 else str(q.numerator)

    def cond_panel(slider, verdict=False):
        """Grid of the two-dice outcomes with A = {sum is t} circled and B = {1st is even} shaded,
        with P(A), P(A | B), P(B | A); optionally the independence verdict."""
        t = slider.value
        fig = Figure(figsize=(4.0, 4.0), layout="constrained")
        ax = fig.subplots()
        for x in (1.5, 3.5, 5.5):
            ax.fill_between([x, x + 1], 0.5, 6.5, color=RED, alpha=0.12, lw=0)
        nA = nAB = 0
        for i in range(1, 7):
            for j in range(1, 7):
                if i + j == t:
                    nA += 1
                    nAB += i % 2 == 0
                    ax.plot(i, j, "o", ms=17, mfc="none", mec=GREEN, mew=1.8)
                ax.plot(i, j, "o", ms=4, color=BLUE)
        ax.set_xlim(0.3, 6.7)
        ax.set_ylim(0.3, 6.7)
        ax.set_aspect("equal")
        ax.set_xticks(range(1, 7))
        ax.set_yticks(range(1, 7))
        ax.set_xlabel("1st")
        ax.set_ylabel("2nd")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

        pA, pAB, pBA = Fraction(nA, 36), Fraction(nAB, 18), Fraction(nAB, nA)
        text = (
            rf"$\textcolor{{{GREEN}}}{{A}}$ (circles), &nbsp; $\textcolor{{{RED}}}{{B = \text{{1st is even}}}}$ (shaded)"
            + "\n\n"
            + rf"$$P(A) = {_frac(pA)}, \qquad P(A \mid B) = {_frac(pAB)}, \qquad P(B \mid A) = {_frac(pBA)}$$"
        )
        if verdict:
            text += "\n\n" + (r"$P(A \mid B) = P(A)$ &nbsp; $\Longrightarrow$ &nbsp; $A, B$ independent" if pA == pAB else r"$P(A \mid B) \neq P(A)$ &nbsp; $\Longrightarrow$ &nbsp; $A, B$ not independent")
        return mo.vstack([slider, mo.hstack([fig, mo.md(text)], widths=[1, 1], gap=2, align="center", wrap=True)])

    return (cond_panel,)


@app.cell(hide_code=True)
def _(mo):
    total = mo.ui.slider(2, 12, 1, value=8, label="$A$: sum is", show_value=True)
    return (total,)


@app.cell(hide_code=True)
def _(cond_panel, total):
    cond_panel(total)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
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
    \leadsto \quad P\left(\substack{\text{sum is 8 and} \\ \text{1st is even}}\right) = \underbrace{P\left(\substack{\text{sum is 8 given} \\ \text{1st is even}}\right)}_{\text{2nd stage}}\ \underbrace{P(\text{1st is even})}_{\text{1st stage}} \qquad (\text{of the random experiment})
    $$

    Generalizations:

    $$
    P(A \cap B \cap C) = P(A \mid B \cap C)\, P(B \cap C) = P(A \mid B \cap C)\, P(B \mid C)\, P(C)
    $$

    $$
    \underbrace{P(A_1 \cap A_2 \cap \cdots \cap A_n)}_{n \text{ stages}} = \underbrace{P(A_1 \mid A_2 \cap \cdots \cap A_n)}_{n\text{th}} \times \underbrace{P(A_2 \mid A_3 \cap \cdots \cap A_n)}_{(n-1)\text{th}} \cdots \underbrace{P(A_{n-1} \mid A_n)}_{\text{2nd}}\ \underbrace{P(A_n)}_{\text{1st}}
    $$

    **Remark.** Here we see another possible interpretation of probability

    from “relative frequency of event occurrences in infinitely many trials of an experiment” (frequentist interpretation)

    to “measure of belief in the likelihood of event occurrences in each trial of an experiment” (Bayesian interpretation)

    If $P(A)$ is our original measure of belief about $A$, $P(A \mid B)$ is our updated measure of belief about $A$ given new knowledge about $B$!
    """
            ),
            definition(
                r"""
    Two events $A, B \subseteq S$ are called **independent** if

    $$
    P(A \mid B) = P(A) \quad \Longleftrightarrow \quad P(A \cap B) = P(A)\, P(B) \quad \Longleftrightarrow \quad P(B \mid A) = P(B)
    $$

    (knowledge about $B$ does not influence our belief about $A$; the conditional forms require $P(B) > 0$, $P(A) > 0$)
    """
            ),
            mo.md(
                r"""
    **Example.** two fair dice &nbsp; $\leadsto$ &nbsp; $S = \{(1, 1), \dots, (6, 6)\}$

    $A$ = sum is 7 $= \{(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)\}$ &nbsp; and &nbsp; $B$ = 1st is even $= \{(2, 1), (2, 2), \dots, (6, 5), (6, 6)\}$ &nbsp; are independent

    $$
    P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{3/36}{18/36} = \frac{1}{6} = \frac{6}{36} = P(A)
    $$

    If $A$ = “sum is 8”, relative counting changes if we know $B$ = “1st is even” &nbsp; $\Longrightarrow$ &nbsp; $A, B$ not independent

    If $A$ = “sum is 7”, relative counting remains same if we know $B$ = “1st is even” &nbsp; $\Longrightarrow$ &nbsp; $A, B$ independent
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
def _(cond_panel, total_ind):
    cond_panel(total_ind, verdict=True)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** independence $\neq$ mutually exclusive!

    $$
    P(A \cap B) = P(A)\, P(B) \quad \not\Longleftrightarrow \quad A \cap B = \emptyset
    $$

    $$
    A \cap B = \emptyset \ \ \Longrightarrow \ \ P(A \cap B) = 0 \ \ \Longrightarrow \ \ \text{not independent if } P(A) \neq 0 \text{ and } P(B) \neq 0
    $$
    """
            ),
            theorem(
                r"""
    If $A$ and $B$ are independent, then so are $A$ and $B^c$, &nbsp; $A^c$ and $B$, &nbsp; $A^c$ and $B^c$.
    """
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    P(A^c \cap B) &= P(A^c \mid B)\, P(B) \\
    &= \big( 1 - P(A \mid B) \big)\, P(B) \\
    &= \big( 1 - P(A) \big)\, P(B) = P(A^c)\, P(B) \qquad \square
    \end{aligned}
    $$
    """
            ),
            definition(
                r"""
    $A, B, C \subseteq S$ are **pairwise independent** if

    $$
    P(A \cap B) = P(A)\, P(B), \qquad P(B \cap C) = P(B)\, P(C), \qquad P(C \cap A) = P(C)\, P(A)
    $$

    (each pair is independent)

    $A, B, C \subseteq S$ **mutually independent** if they are pairwise independent and

    $$
    P(A \cap B \cap C) = P(A)\, P(B)\, P(C)
    $$
    """
            ),
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

    Knowledge about $A$ does not affect our belief in $C$; &nbsp; $B$ does not affect our belief in $C$; &nbsp; knowledge about *$A$ and $B$* affects our belief in $C$!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, mo):
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
            if (_i + _j) % 2 == 1:
                _C.add((_i, _j))
                _ax.plot(_i, _j, "D", ms=8, mfc="none", mec=BLUE, mew=1.6)
            _ax.plot(_i, _j, "o", ms=3, color="#555555")
    _ax.set_xlim(0.3, 6.7)
    _ax.set_ylim(0.3, 6.7)
    _ax.set_aspect("equal")
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks(range(1, 7))
    _ax.set_xlabel("1st")
    _ax.set_ylabel("2nd")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.hstack(
        [
            _fig,
            mo.md(
                rf"$\textcolor{{{RED}}}{{A}}$ = 1st is odd (circles), &nbsp; $\textcolor{{{GREEN}}}{{B}}$ = 2nd is odd (squares), &nbsp; $\textcolor{{{BLUE}}}{{C}}$ = sum is odd (diamonds)"
                + "\n\n"
                + rf"$\# A = {len(_A)}, \quad \# B = {len(_B)}, \quad \# C = {len(_C)}$"
                + "\n\n"
                + rf"$\#(A \cap B) = {len(_A & _B)}, \quad \#(B \cap C) = {len(_B & _C)}, \quad \#(C \cap A) = {len(_C & _A)}$"
                + "\n\n"
                + rf"$\#(A \cap B \cap C) = {len(_A & _B & _C)}$ &nbsp; (odd + odd is even)"
            ),
        ],
        widths=[1, 1],
        gap=2,
        align="center",
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Bayes' Rule

    Updating our level of belief in a collection of hypotheses after a new event has occurred

    **Example.** A disease affects 1% of a population &nbsp; $\leadsto$ &nbsp; $P(\text{have disease}) = 1\%$ &nbsp; (disease prevalence)

    A test has 90% *sensitivity* &nbsp; $P(+\text{ve} \mid \text{disease})$ &nbsp; (true positive rate) &nbsp; and 95% *specificity* &nbsp; $P(-\text{ve} \mid \text{no disease})$ &nbsp; (true negative rate)

    What is the probability of having the disease given a positive test?

    $$
    \left.\begin{aligned} D &= \text{has disease} \\ D^c &= \text{doesn't have disease} \end{aligned}\right\} \quad P(D) = 1\%, \quad P(D^c) = 99\%
    $$

    $$
    \left.\begin{aligned} T &= \text{tested positive} \\ T^c &= \text{tested negative} \end{aligned}\right\} \quad P(T \mid D) = 90\%, \quad \underbrace{P(T^c \mid D^c) = 95\%}_{P(T \mid D^c) \,=\, 5\%}
    $$

    $$
    \leadsto \quad P(D \mid T) = \ ?
    $$

    $$
    \begin{aligned}
    \text{Bayes' rule:} \qquad P(D \mid T) &= \frac{P(D \cap T)}{P(T)} \\[4pt]
    &= \frac{P(T \mid D)\, P(D)}{P(T)} \\[4pt]
    &= \frac{P(T \mid D)\, P(D)}{P(T \cap D) + P(T \cap D^c)} \\[4pt]
    &= \frac{P(T \mid D)\, P(D)}{P(T \mid D)\, P(D) + P(T \mid D^c)\, P(D^c)} \\[4pt]
    &= \frac{0.9 \times 0.01}{0.9 \times 0.01 + 0.05 \times 0.99} = \frac{2}{13} \approx 15.4\%
    \end{aligned}
    $$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    prev = mo.ui.slider(0.1, 50, 0.1, value=1, label="prevalence $P(D)$ (%)", show_value=True)
    sens = mo.ui.slider(50, 100, 0.5, value=90, label=r"sensitivity $P(T \mid D)$ (%)", show_value=True)
    spec = mo.ui.slider(50, 100, 0.5, value=95, label=r"specificity $P(T^c \mid D^c)$ (%)", show_value=True)
    return prev, sens, spec


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, mo, prev, sens, spec):
    _p, _se, _sp = prev.value / 100, sens.value / 100, spec.value / 100
    _tp, _fp = _se * _p, (1 - _sp) * (1 - _p)
    _post = _tp / (_tp + _fp) if _tp + _fp > 0 else 0.0

    _fig = Figure(figsize=(7.0, 1.5), layout="constrained")
    _ax = _fig.subplots()
    _ax.barh([0], [_tp], color=RED)
    _ax.barh([0], [_fp], left=[_tp], color=BLUE, alpha=0.6)
    _ax.set_yticks([])
    _ax.set_xlim(0, max(_tp + _fp, 1e-9))
    _ax.set_xlabel(r"$P(T) = P(T \cap D) + P(T \cap D^c)$")
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _N = 10_000
    _nD = _N * _p
    _table = "\n".join(
        [
            "| out of 10 000 people | |",
            "|:--|--:|",
            rf"| have the disease ($D$) | ${_nD:,.0f}$ |",
            rf"| &nbsp;&nbsp; of which test positive ($T \cap D$) | ${_nD * _se:,.0f}$ |",
            rf"| do not have the disease ($D^c$) | ${_N - _nD:,.0f}$ |",
            rf"| &nbsp;&nbsp; of which test positive ($T \cap D^c$) | ${(_N - _nD) * (1 - _sp):,.0f}$ |",
            rf"| test positive in total ($T$) | ${_N * (_tp + _fp):,.0f}$ |",
            rf"| $P(D \mid T)$ = positives with the disease / all positives | ${100 * _post:.1f}\%$ |",
        ]
    ).replace(",", r"\,")

    mo.vstack(
        [
            mo.hstack([prev, sens, spec], justify="start", gap=2, wrap=True),
            mo.md(rf"$$P(D \mid T) = \frac{{{_se:g} \times {_p:g}}}{{{_se:g} \times {_p:g} + {1 - _sp:.3g} \times {1 - _p:g}}} \approx {100 * _post:.1f}\%$$"),
            _fig,
            mo.md(rf"$\textcolor{{{RED}}}{{P(T \cap D)}}$ &nbsp; and &nbsp; $\textcolor{{{BLUE}}}{{P(T \cap D^c)}}$"),
            mo.md(_table),
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
    P(A) = \sum_{i=1}^{k} P(A \mid B_i)\, P(B_i) \qquad \text{law of total probability}
    $$

    $$
    P(B_j \mid A) = \frac{P(A \mid B_j)\, P(B_j)}{\displaystyle\sum_{i=1}^{k} P(A \mid B_i)\, P(B_i)} \qquad \text{Bayes' rule}
    $$

    $P(B_i)$ = prior, &nbsp; $P(B_i \mid A)$ = posterior, &nbsp; $P(A \mid B_i)$ = likelihood
    """)
    return


if __name__ == "__main__":
    app.run()

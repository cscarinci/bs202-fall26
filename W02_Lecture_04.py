import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 4 · Random variables", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, mo


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(4, "Random variables")
    return


@app.cell(hide_code=True)
def _(Figure):
    # Helpers of this lecture: bare sketches, plain axes

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def plain(ax):
        """No top/right spines, plain numbers on the y axis."""
        ax.yaxis.set_major_formatter(lambda v, _: f"${v:g}$")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    return blank, plain


@app.cell(hide_code=True)
def _(mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    rv_choice = mo.ui.dropdown(["X = largest face", "Y = sum of faces"], value="X = largest face", label="random variable")
    return (rv_choice,)


@app.cell(hide_code=True)
def _(lk, rv_choice):
    # Controls (continued): the range of a and b follows the state space of the chosen random variable
    _lo, _hi = (1, 4) if rv_choice.value.startswith("X") else (2, 8)
    range_a = lk.slider(_lo, _hi, step=1, value=min(max(3, _lo), _hi), label="$a$")
    range_b = lk.slider(_lo, _hi, step=1, value=min(max(3, _lo), _hi), label="$b$")
    return range_a, range_b


@app.cell(hide_code=True)
def _(blank, lk):
    # module: recap
    # recap: conditional probability, independence, Bayes' rule, with the sketch of S split into B_1, B_2, B_3 and the event
    # A across them
    _fig, _ax = blank(3.2, 1.9, (-0.25, 3.15), (-0.1, 1.55))
    _ax.fill([0.3, 2.7, 2.7, 0.3], [0.35, 0.35, 0.95, 0.95], color=lk.LIGHT, lw=0)
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 1.3, 1.3, 0], color="black", lw=1.0)
    for _x in (1, 2):
        _ax.plot([_x, _x], [0, 1.3], color="black", lw=1.0)
    _ax.plot([0.3, 2.7, 2.7, 0.3, 0.3], [0.35, 0.35, 0.95, 0.95, 0.35], color=lk.BLUE, lw=1.4)
    for _k, _x in enumerate((0.65, 1.5, 2.35)):
        _ax.text(_x, 0.65, rf"$A \cap B_{_k + 1}$", fontsize=12, ha="center", va="center")
        _ax.text(_k + 0.5, 0.16, rf"$B_{_k + 1}$", fontsize=12, ha="center", va="center")
    _ax.text(2.72, 1.0, "$A$", color=lk.BLUE, fontsize=13, ha="left", va="bottom")
    _ax.text(-0.06, 1.34, "$S$", fontsize=13, ha="right", va="bottom")

    lk.recap(
        lk.aside(
            r"$\mk{P(A \mid B)} = \dfrac{P(A \cap B)}{P(B)}$",
            r"$P(A \mid B)$ = probability of $A$ given $B$ has occurred<br>= probability of $A$ and $B$ relative to probability of $B$",
        ),
        r"""
        > $\leadsto$ &nbsp; $P(A \cap B) = P(A \mid B) \, P(B)$

        if knowledge about $B$ does not change our belief about $A$, then $A$ and $B$ are **independent**!
        """,
        lk.aside(r"> $\leadsto$ &nbsp; $P(A \mid B) = P(A) \iff P(A \cap B) = P(A) \, P(B)$", "(for $P(B) > 0$)"),
        lk.gap(),
        r"Bayes' rule: &nbsp; $P(B \mid A) = \dfrac{P(A \cap B)}{P(A)} = \dfrac{P(A \mid B) \, P(B)}{P(A \mid B) \, P(B) + P(A \mid B^c) \, P(B^c)}$ $\rule[-1em]{0pt}{2.6em}$",
        r"$\leadsto$ &nbsp; more generally: &nbsp; $P(B_j \mid A) = \dfrac{P(A \cap B_j)}{P(A)} = \dfrac{P(A \mid B_j) \, P(B_j)}{\sum_{i=1}^{k} P(A \mid B_i) \, P(B_i)}$ $\rule[-1em]{0pt}{2.6em}$",
        lk.figure(_fig),
        lk.aside(r"$B_1 \cup B_2 \cup \dots \cup B_k = S$", "exhaustive"),
        lk.aside(r"$B_i \cap B_j = \emptyset \quad \forall \, i \neq j \in \{1, 2, \dots, k\}$", "mutually disjoint"),
        lk.gap(),
        lk.aside(r"$P(B_i)$ = prior level of belief", "probability of having a disease before testing"),
        lk.aside(r"$P(B_i \mid A)$ = posterior level of belief", "probability of having a disease after testing"),
        lk.aside(r"$P(A \mid B_i)$ = likelihoods", "true positive rates and false positive rates"),
        lk.gap(),
        r"law of total probability: &nbsp; $P(A) = \displaystyle\sum_{i=1}^{k} P(A \mid B_i) \, P(B_i)$",
        topic="knowledge about an event can change our belief about other events",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 2.11, 3.1–3.2, 4.2")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # section
    lk.section("Random variables")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # motivation: measurements instead of the full probability space
    lk.prose(
        r"""
        random experiment &nbsp; $\leftrightsquigarrow$ &nbsp; probability space $(S, \mathcal{E}, P)$

        > $\leadsto$ &nbsp; so far we considered “simple” examples

        > > $\leadsto$ &nbsp; equally likely outcomes

        > > $\leadsto$ &nbsp; easy algebra of finite sets

        > > $\leadsto$ &nbsp; probability = counting

        > $\leadsto$ &nbsp; in general, $(S, \mathcal{E}, P)$ too complicated

        > > $\leadsto$ &nbsp; no direct description

        > > $\leadsto$ &nbsp; messy algebra of events

        > > $\leadsto$ &nbsp; hard to compute probability
        """,
        lk.gap(),
        r"""
        measurements on random experiments &nbsp; $\leftrightsquigarrow$ &nbsp; real valued functions on the sample space

        > $\leadsto$ &nbsp; associates real numbers to each outcome (measurements)

        > $\leadsto$ &nbsp; simplify the model by only focusing on those numbers
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # definition: random variable and state space
    lk.definition(
        [
            r"""
            Given a probability space $(S, \mathcal{E}, P)$, a **random variable** on $S$ is a function &nbsp; $X : S \longrightarrow \mathbb{R}$, &nbsp; $o \longmapsto X(o)$

            The image of $X$

            $$
            S_X = \mathrm{Im}(X) = \{ x \in \mathbb{R} \mid X(o) = x \text{ for some } o \in S \} \subseteq \mathbb{R}
            $$
            """,
            lk.aside(
                r"is called the <span class='lk-mark'>**state space** of $X$</span>",
                r"it will serve as a simplified version<br>of the true sample space $S$",
            ),
        ],
        label="def-rv",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # example: a DGIST student at random
    lk.example(
        r"""
        Choose a DGIST student at random

        $S = \{ \text{3000 individual human beings} \}$

        > $\leadsto$ &nbsp; how can we describe events?

        > > $A = \{\text{male}\}$, $B = \{\text{female}\}$, $C = \{\text{non-binary}\}$, $D = \{\text{Korean}\}$, $E = \{\text{plays football}\}$, …

        > $\leadsto$ &nbsp; we can come up with a huge number of events

        > $\leadsto$ &nbsp; hopeless to try to find a “complete” model

        > $\leadsto$ &nbsp; instead, we can collect measurements of aspects we are interested in and focus on modeling those measurements only!

        $X$ = year in DGIST &nbsp; $\leadsto$ &nbsp; $S_X = \{2011, 2012, \dots, 2026\}$

        $Y$ = current GPA &nbsp;&nbsp; $\leadsto$ &nbsp; $S_Y \subseteq [0, 4]$
        """,
        label="ex-dgist",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # remark: state space, algebra and distribution of X as simplified versions of S, E and P
    lk.remark(
        [
            r"Given $X : S \longrightarrow \mathbb{R}$",
            r"> **state space** &nbsp; $S_X = \mathrm{Im}(X) \subseteq \mathbb{R}$ &nbsp; simplified version of $S$",
            lk.aside(
                r"> **algebra of subsets** of $S_X$ &nbsp; $\mk{\mathcal{E}_X} = \{ A \subseteq S_X \subseteq \mathbb{R} \}$ &nbsp; simplified version of $\mathcal{E}$",
                r"collection of subsets in $\mathbb{R}$<br>(intervals and points)",
            ),
            r"> **probability distribution** of $X : S \longrightarrow \mathbb{R}$ &nbsp; $P_X : \mathcal{E}_X \longrightarrow \mathbb{R}$ &nbsp; simplified version of $P : \mathcal{E} \longrightarrow \mathbb{R}$",
            lk.aside(
                r"> > $P_X(A) = P(\mk{\{ o \in S \mid X(o) \in A \}}) = P(X \in A)$",
                r"outcomes whose value of $X$ belongs to $A$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(blank, lk):
    # module: random variables
    # example: the year in DGIST, with the sketch of y = P_X({x})
    _fig, _ax = blank(5.6, 2.6, (-1.0, 18.4), (-2.3, 6.6))
    lk.arrow(_ax, (-0.5, 0), (17.8, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.4), (0, 6.4), "black", lw=0.9)
    _vals = [0, 0, 0, 0, 0, 0, 0, 0.3, 0.6, 1.5, 2.6, 3.6, 4.3, 4.9, 5.2, 5.6]
    for _k, _v in enumerate(_vals):
        _ax.plot([_k + 1, _k + 1], [-0.1, 0.1], color="black", lw=0.9)
        _ax.plot(_k + 1, _v, "o", color=lk.BLUE, ms=4, zorder=4)
        if _k % 3 == 0:  # full years, every third one
            _ax.text(_k + 1, -0.3, f"${2011 + _k}$", fontsize=12, ha="center", va="top")
    _ax.text(17.9, -0.3, "$x$", fontsize=13, ha="center", va="top")
    _ax.text(0.35, 6.3, "$y$", fontsize=13, ha="left", va="top")
    _ax.text(11.5, 4.4, r"$y = P_X(\{x\})$", color=lk.BLUE, fontsize=13, ha="right", va="center")
    _ax.plot([0.7, 0.7, 7.3, 7.3], [-1.15, -1.4, -1.4, -1.15], color=lk.GREY, lw=1.0)
    _ax.text(4, -1.55, "graduated", fontsize=12, ha="center", va="top")

    _ub = lambda body, *rows: r"\underbrace{" + body + r"}_{\begin{array}{c} " + r" \\ ".join(r"\scriptstyle \text{" + r + "}" for r in rows) + r" \end{array}}"
    lk.example(
        [
            r"""
            $S = \{ \text{all students} \}$

            $X$ = year in DGIST &nbsp; $\leadsto$ &nbsp; $S_X = \{2011, \dots, 2025, 2026\}$
            """,
            r"$$ "
            + _ub(r"P_X(\{2026\})", r"\{2026\}: subset of } \mathbb{R} \text{", "easy to characterize", "with a census of DGIST")
            + r" \quad = \quad "
            + _ub(r"P(\{\text{is freshman}\})", "subset of humans", "impossible to model", "“completely”")
            + r" \quad = \quad P(\{X = 2026\}) \rule[-3.2em]{0pt}{0pt} $$",
            lk.figure(_fig),
            r"In probability theory, we are more interested in modeling random variables and their distributions, than in the full probability spaces!",
        ],
        label="ex-year",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # definition: discrete and continuous random variables
    lk.definition(
        [
            r"A random variable $X : S \longrightarrow \mathbb{R}$ is called",
            lk.aside(
                r"> • &nbsp; **discrete** if $S_X = \mathrm{Im}(X)$ consists of <span class='lk-mark'>countably many</span> points",
                "we can count them 1st, 2nd, 3rd, …",
            ),
            r"> • &nbsp; **continuous** if $S_X = \mathrm{Im}(X)$ is uncountable + extra conditions (later)",
        ],
        label="def-discrete-continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random variables
    # example: two dice, largest face and sum of faces
    lk.example(
        r"""
        > $\leadsto$ &nbsp; $S = \{ (i, j) \mid i, j \in \{1, 2, 3, 4\} \}$

        $X(i, j) = \begin{cases} \max(i, j), & i \neq j \\ i, & i = j \end{cases} \ = \text{largest face} \quad \leadsto \quad S_X = \{1, 2, 3, 4\}$

        $Y(i, j) = i + j = \text{sum of faces} \quad \leadsto \quad S_Y = \{2, 3, \dots, 7, 8\}$
        """,
        title="rolling two fair 4-sided dice",
        label="ex-dice",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf
    # section
    lk.section("Probability mass function")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf
    # definition: pmf and its properties
    lk.definition(
        [
            r"Given $X : S \longrightarrow \mathbb{R}$ discrete random variable, the **probability mass function** (pmf) of $X$ is",
            lk.aside(
                r"$$ f_X : \mathbb{R} \longrightarrow [0, 1], \qquad x \longmapsto f_X(x) = \mk{P(X = x)} $$",
                r"probability of $X$ having value $x$",
            ),
            r"""
            $f_X$ satisfies

            > • &nbsp; $f_X(x) \geq 0 \quad \forall \, x \in S_X$

            > • &nbsp; $f_X(x) = 0 \quad \forall \, x \notin S_X$

            > • &nbsp; $\displaystyle\sum_{x \in S_X} f_X(x) = 1$

            > • &nbsp; $\displaystyle\sum_{x \in A} f_X(x) = P(X \in A)$
            """,
        ],
        label="def-pmf",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: pmf
    # example: the pmf of the largest face, with its graph
    _fig = Figure(figsize=(3.4, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _pmf = [0, 1 / 16, 3 / 16, 5 / 16, 7 / 16, 0, 0]
    for _x, _p in enumerate(_pmf):
        _ax.plot([_x, _x], [0, _p], color=lk.BLUE, lw=1.0)
        _ax.plot(_x, _p, "o", color=lk.BLUE, ms=4.5, zorder=4, clip_on=False)
    _ax.set_xlim(-0.5, 6.5)
    _ax.set_ylim(0, 0.5)
    _ax.set_xticks(range(7))
    _ax.set_yticks([_k / 16 for _k in (1, 3, 5, 7)], [rf"${_k}/16$" for _k in (1, 3, 5, 7)])
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    lk.example(
        [
            r"$$ X(i, j) = \begin{cases} \max(i, j), & i \neq j \in \{1, 2, 3, 4\} \\ i, & i = j \in \{1, 2, 3, 4\} \end{cases} $$",
            lk.side(
                r"""
                $$
                \begin{aligned}
                f_X(1) &= P(X = 1) = P(\{(1, 1)\}) = {\large\tfrac{1}{16}}\\[8pt]
                f_X(2) &= P(X = 2) = P(\{(2, 1), (2, 2), (1, 2)\}) = {\large\tfrac{3}{16}}\\[8pt]
                f_X(3) &= P(\{(3, 1), (3, 2), (3, 3), (2, 3), (1, 3)\}) = {\large\tfrac{5}{16}}\\[8pt]
                f_X(4) &= {\large\tfrac{7}{16}}, \quad f_X(5) = 0, \quad f_X(6) = 0
                \end{aligned}
                $$
                """,
                lk.figure(_fig),
            ),
        ],
        title="rolling two fair 4-sided dice, continued",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cdf
    # section
    lk.section("Cumulative distribution function")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cdf
    # definition: cdf
    lk.definition(
        [
            r"Given $X : S \longrightarrow \mathbb{R}$ discrete random variable, the **cumulative distribution function** (cdf) of $X$ is",
            lk.aside(
                r"$$ F_X : \mathbb{R} \longrightarrow [0, 1], \qquad x \longmapsto F_X(x) = \mk{P(X \leq x)} $$",
                r"probability of $X$ having value at most $x$",
            ),
        ],
        label="def-cdf",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: cdf
    # example: the cdf of the largest face, its jumps, with its graph
    _fig = Figure(figsize=(3.6, 2.6), layout="constrained")
    _bx = _fig.subplots()
    _edges = [-1, 1, 2, 3, 4, 6.4]
    _levels = [0, 1 / 16, 1 / 4, 9 / 16, 1]
    for _k, _lev in enumerate(_levels):
        _bx.plot([_edges[_k], _edges[_k + 1]], [_lev, _lev], color=lk.BLUE, lw=1.6)
        if _k > 0:
            if _k < 3:
                _bx.plot([_edges[_k], _edges[_k]], [_levels[_k - 1], _lev], color=lk.GREY, lw=0.9, ls=(0, (1, 2)))
            _bx.plot(_edges[_k], _levels[_k - 1], "o", color=lk.BLUE, ms=4.5, mfc="white", zorder=4)
            _bx.plot(_edges[_k], _lev, "o", color=lk.BLUE, ms=4.5, zorder=4)
    for _x, _lo, _hi, _name in ((3, 1 / 4, 9 / 16, r"$f_X(3) = \dfrac{5}{16}$"), (4, 9 / 16, 1, r"$f_X(4) = \dfrac{7}{16}$")):
        _mid = (_lo + _hi) / 2
        lk.arrow(_bx, (_x, _mid), (_x, _hi), lk.GREEN, shrinkB=3)
        lk.arrow(_bx, (_x, _mid), (_x, _lo), lk.GREEN, shrinkB=3)
        _bx.text(_x + 0.22, _mid, _name, color=lk.GREEN, fontsize=12, ha="left", va="center")
    _bx.set_xlim(-1, 6.4)
    _bx.set_ylim(-0.06, 1.12)
    _bx.set_xticks(range(7))
    _bx.set_yticks([0.25, 0.5, 0.75, 1], [r"$1/4$", r"$1/2$", r"$3/4$", "$1$"])
    _bx.set_xlabel("$x$")
    _bx.set_ylabel("$F_X(x)$")
    for _s in ("top", "right"):
        _bx.spines[_s].set_visible(False)

    lk.example(
        [
            r"$$ X(i, j) = \begin{cases} \max(i, j), & i \neq j \\ i, & i = j \end{cases} $$",
            r"""
            $$
            \begin{aligned}
            F_X(1) &= P(X \leq 1) = P(X = 1) = {\large\tfrac{1}{16}}\\[8pt]
            F_X(2) &= P(X \leq 2) = P(X \leq 1) + P(X = 2) = {\large\tfrac{1}{16}} + {\large\tfrac{3}{16}} = {\large\tfrac{1}{4}}\\[8pt]
            F_X(3) &= P(X \leq 3) = P(X \leq 2) + P(X = 3) = {\large\tfrac{1}{4}} + {\large\tfrac{5}{16}} = {\large\tfrac{9}{16}}\\[8pt]
            F_X(4) &= {\large\tfrac{9}{16}} + {\large\tfrac{7}{16}} = 1, \quad F_X(5) = 1, \quad F_X(6) = 1
            \end{aligned}
            $$
            """,
            lk.side(
                r"""
                $$
                \leadsto \quad
                \begin{aligned}
                F_X(4) - F_X(3) &= f_X(4)\\
                F_X(3) - F_X(2) &= f_X(3)\\
                F_X(2) - F_X(1) &= f_X(2)\\
                F_X(1) - F_X(0) &= f_X(1)
                \end{aligned}
                $$
                """,
                lk.figure(_fig),
            ),
        ],
        title="rolling two fair 4-sided dice, continued",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, plain, range_a, range_b, rv_choice):
    # module: cdf
    # interactive figure: pmf and cdf of X = largest face or Y = sum of faces, with P(a <= X <= b) read off both
    _is_max = rv_choice.value.startswith("X")
    _rv = "X" if _is_max else "Y"
    _counts = {}
    for _i in range(1, 5):
        for _j in range(1, 5):
            _v = max(_i, _j) if _is_max else _i + _j
            _counts[_v] = _counts.get(_v, 0) + 1
    _xs = sorted(_counts)
    _pmf = [_counts[_x] / 16 for _x in _xs]
    _a, _b = range_a.value, range_b.value

    def _F(x):
        return sum(_counts[_v] for _v in _xs if _v <= x)

    _lo, _hi = _xs[0] - 1, _xs[-1] + 1
    _fig = Figure(figsize=(lk.FULL, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    if _a <= _b:
        _left.axvspan(_a - 0.5, _b + 0.5, color=lk.LIGHT, lw=0)
        for _v in (_a - 0.5, _b + 0.5):
            _left.axvline(_v, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _left.vlines(_xs, 0, _pmf, color=lk.BLUE, lw=1.0)
    _left.plot(_xs, _pmf, "o", color=lk.BLUE, ms=4.5, zorder=4)
    _left.set_xlim(_lo, _hi)
    _left.set_ylim(0, max(_pmf) * 1.25)
    _left.set_xticks(_xs)
    _left.set_xlabel("$x$")
    _left.set_ylabel(f"$f_{_rv}(x)$")

    _edges = [_lo] + _xs + [_hi]
    _levels = [0] + [_F(_x) / 16 for _x in _xs]
    for _k, _lev in enumerate(_levels):
        _right.plot([_edges[_k], _edges[_k + 1]], [_lev, _lev], color=lk.BLUE, lw=1.6)
        if _k > 0:
            _right.plot([_edges[_k], _edges[_k]], [_levels[_k - 1], _lev], color=lk.GREY, lw=0.9, ls=(0, (1, 2)))
            _right.plot(_edges[_k], _levels[_k - 1], "o", color=lk.BLUE, ms=4.5, mfc="white", zorder=4)
            _right.plot(_edges[_k], _lev, "o", color=lk.BLUE, ms=4.5, zorder=4)
    _span = _hi - _lo
    _xg = _hi + 0.09 * _span  # the difference F(b) - F(a - 1) is read off on the right of the plot
    if _a <= _b:
        _y0, _y1 = _F(_a - 1) / 16, _F(_b) / 16
        _right.plot([_a, _xg], [_y0, _y0], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
        _right.plot([_b, _xg], [_y1, _y1], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
        _cap = 0.02 * _span
        _right.plot([_xg - _cap, _xg + _cap, _xg, _xg, _xg - _cap, _xg + _cap], [_y0, _y0, _y0, _y1, _y1, _y1], color=lk.GREEN, lw=1.6, zorder=3)
        _right.text(_xg + _cap, 1.1, f"$F_{_rv}(b) - F_{_rv}(a - 1)$", color=lk.GREEN, fontsize=12, ha="right", va="bottom")
    _right.set_xlim(_lo, _hi + 0.16 * _span)
    _right.set_ylim(-0.06, 1.12)
    _right.set_xticks(_xs)
    _right.set_xlabel("$x$")
    _right.set_ylabel(f"$F_{_rv}(x)$")
    plain(_left)
    plain(_right)
    # fraction ticks, set after plain(), which formats decimals
    _left.set_yticks(sorted(set(_pmf)), [f"${round(_p * 16)}/16$" for _p in sorted(set(_pmf))])
    _right.set_yticks([0.25, 0.5, 0.75, 1], [r"$1/4$", r"$1/2$", r"$3/4$", "$1$"])

    lk.interactive(_fig, controls=[rv_choice, range_a, range_b])
    return


@app.cell(hide_code=True)
def _(lk):
    # module: cdf
    # consequences: pmf and cdf encode the distribution
    lk.prose(
        r"""
        $\leadsto$ &nbsp; pmf and cdf are different ways to encode the probability distribution of a random variable $X$

        $\leadsto$ &nbsp; we will spend the next several lectures studying properties and examples of such functions!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # section
    lk.section("Practice")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: contaminated kits
    lk.exercise(
        r"""
        A lab uses chemical kits from three suppliers

        > $P(S_1) = 50\%$, $P(S_2) = 30\%$, $P(S_3) = 20\%$

        Contamination rate of kits from each supplier is

        > $P(C \mid S_1) = 1\%$, $P(C \mid S_2) = 2\%$, $P(C \mid S_3) = 5\%$

        a) what is the probability that a kit is contaminated?

        b) given a contaminated kit, what is the probability it came from supplier 3?
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: balls without replacement
    lk.exercise(
        r"""
        A box has 5 red, 4 blue and 3 green balls

        Choose 3 without replacement. Find the probability that no ball is red
        """,
        label="ex-practice-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: pmf from a cdf
    lk.exercise(
        [
            r"Suppose $X$ has state space $S_X = \{0, 1, 2, 3, 4\}$",
            lk.aside(r"with &nbsp; $F_X(0) = 0.1$, $F_X(1) = 0.35$, $F_X(2) = 0.65$, $F_X(3) = 0.9$, $F_X(4) = 1$", "cdf"),
            r"a) Find $f_X$ (pmf)",
            r"b) Compute $P(X > 2)$ and $P(1 \leq X \leq 3)$",
        ],
        label="ex-practice-3",
    )
    return


if __name__ == "__main__":
    app.run()

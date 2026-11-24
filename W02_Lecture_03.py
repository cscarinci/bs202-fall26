import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 3 · Conditioning, independence, and Bayes' rule", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(3, "Conditioning, independence, and Bayes' rule")
    return


@app.cell(hide_code=True)
def _(Figure):
    # Helpers of this lecture: bare sketches, the 36 outcomes of two dice, strips of outcomes

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def outcome_grid(left=0.1):
        """The 36 outcomes of two dice as a grid of dots: 1st die across, 2nd die up."""
        fig = Figure(figsize=(3.0, 3.0), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(left, 7.1)
        ax.set_ylim(0.1, 7.1)
        ax.set_aspect("equal")
        ax.set_xticks(range(1, 7), [f"${k}$" for k in range(1, 7)])
        ax.set_yticks(range(1, 7), [f"${k}$" for k in range(1, 7)])
        ax.set_xlabel("1st die")
        ax.set_ylabel("2nd die")
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

    return blank, outcome_grid, strip


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    dice_sum = lk.slider(2, 12, step=1, value=8, label="$A$: sum is")
    return (dice_sum,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: equally likely outcomes, counting rules, defective items (repeated from the end of the last lecture)
    lk.recap(
        lk.aside(r"$P(A) = \dfrac{\# A}{\# S}$", "calculating probability reduces to counting"),
        lk.gap(),
        "Basic counting rules",
        r"> $n$ objects, $r$ positions",
        lk.aside(r"> > **ordered** without repetitions &nbsp; $\leadsto$ &nbsp; $P^n_r = \dfrac{n!}{(n - r)!}$", "ranking of a competition"),
        lk.aside(r"> > **unordered** without repetitions &nbsp; $\leadsto$ &nbsp; $C^n_r = \dfrac{n!}{r! \, (n - r)!}$", "hands of poker"),
        lk.aside(r"> > **ordered** with repetitions &nbsp; $\leadsto$ &nbsp; $n^r = n \times n \times \dots \times n$", "passwords of given length"),
        lk.aside(r"> > **unordered** with repetitions &nbsp; $\leadsto$ &nbsp; $C^{n + r - 1}_r = \dfrac{(n + r - 1)!}{r! \, (n - 1)!}$", "ice cream cups"),
        r"> > > e.g. &nbsp; $\#\left( \begin{array}{c} \text{cups of 4 scoops} \\ \text{from 6 flavours} \end{array} \right) = C^{6 + 4 - 1}_4 = C^9_4 = \dfrac{9!}{4! \, 5!} = 126$ $\rule[-1em]{0pt}{2.6em}$",
        lk.example(
            [
                r"20 items, 3 defective &nbsp; $\leadsto$ &nbsp; pick 4 (samples)",
                lk.aside(r"> $P(\text{at least one is defective}) = \ ?$", "not easy to compute…"),
                r"""
                $$
                \begin{aligned}
                \{\text{at least 1}\} &= \{\text{exactly 1}\} \cup \{\text{exactly 2}\} \cup \{\text{exactly 3}\}\\
                &= \{\text{none}\}^c \qquad \leadsto \quad \#\{\text{none}\} = C^{17}_4 = \frac{17!}{4! \, 13!}
                \end{aligned}
                $$
                """,
                r"$$ \Longrightarrow \quad P(\text{at least one}) = 1 - \frac{\ \dfrac{17!}{4! \, 13!}\ }{\dfrac{20!}{4! \, 16!}} = 1 - \frac{17! \, 16!}{20! \, 13!} \approx 50.9\% $$",
            ],
            title="defective items",
        ),
        topic="Probability spaces with equally likely outcomes",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 2.7–2.10")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # section
    lk.section("Conditional probability")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # motivation: knowledge changes probability
    lk.prose(
        r"the probability of an event might change depending on our knowledge about the occurrence of other events!",
        r"> $\leadsto$ &nbsp; roll two fair dice:",
        r"""
        $$
        \begin{aligned}
        P(\text{sum is 8}) &= \dfrac{5}{36}\\[6pt]
        P(\text{sum is 8 when 1st die is even}) &= \dfrac{3}{18} = \dfrac{1}{6}
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # definition: conditional probability
    lk.definition(
        [
            r"The **conditional probability** of an event $A \subseteq S$, given that an event $B$ is known to have occurred, is",
            lk.aside(
                r"$$ \mk{P(A \mid B)} = \frac{P(A \cap B)}{P(B)} \qquad (\text{provided } P(B) > 0) $$",
                "probability of $A$ given $B$",
            ),
        ],
        label="def-conditional",
    )
    return


@app.cell(hide_code=True)
def _(blank, lk, np):
    # module: conditioning
    # consequences: B as the new sample space, with the sketch of S, B and A, with A ∩ B shaded
    _fig, _ax = blank(3.2, 2.2, (-0.1, 3.7), (-0.1, 2.6))
    _th = np.linspace(0, 2 * np.pi, 240)
    _cx, _cy = 1.2 + 0.72 * np.cos(_th), 0.95 + 0.72 * np.sin(_th)
    _ax.fill(np.maximum(_cx, 0.95), np.maximum(_cy, 0.6), color=lk.LIGHT, lw=0)  # A ∩ B (the corner of B lies inside A)
    _ax.plot(_cx, _cy, color=lk.BLUE, lw=1.4)
    _ax.plot([0.95, 3.3, 3.3, 0.95, 0.95], [0.6, 0.6, 2.3, 2.3, 0.6], color=lk.RED, lw=1.4)
    _ax.plot([0, 3.6, 3.6, 0, 0], [0, 0, 2.5, 2.5, 0], color="black", lw=1.0)
    _ax.text(0.3, 1.5, "$A$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _ax.text(3.05, 0.85, "$B$", color=lk.RED, fontsize=13, ha="center", va="center")
    _ax.text(3.45, 0.22, "$S$", fontsize=13, ha="center", va="center")
    _ax.text(1.43, 1.08, r"$A \cap B$", fontsize=12, ha="center", va="center")

    lk.prose(
        lk.figure(_fig),
        lk.aside(
            r"""
            $$
            \begin{aligned}
            P(A) \quad &\leadsto \quad P(A \mid B) = \frac{P(A \cap B)}{P(B)}\\[6pt]
            P(B) \quad &\leadsto \quad P(B \mid B) = \frac{P(B \cap B)}{P(B)} = 1\\[6pt]
            &\leadsto \quad P(S \mid B) = \frac{P(S \cap B)}{P(B)} = 1
            \end{aligned}
            $$
            """,
            "once we know $B$ has occurred",
            at=1,
            rows=3,
        ),
        r"$\leadsto$ &nbsp; for the purpose of calculating $P(A \mid B)$, we think of $B$ as the “new version” of $S$, and of $A \cap B$ as the “new version” of $A$ inside $B$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # theorem: P( . | B) is a probability measure
    lk.theorem(
        [
            r"Given $A, B \subseteq S$, with $P(B) > 0$",
            r"""
            - $P(A \mid B) \geq 0$
            - $P(B \mid B) = 1$
            """,
            lk.aside(r"- $P(A_1 \cup A_2 \mid B) = P(A_1 \mid B) + P(A_2 \mid B)$ &nbsp; for $(A_1 \cap B) \cap (A_2 \cap B) = \emptyset$", "also true for countably many"),
            r"$\leadsto$ &nbsp; i.e. $P(\, \cdot \mid B)$ is a probability measure on events $A \cap B$",
        ],
        label="thm-conditional-measure",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # example: sum is 8, 1st is even
    lk.example(
        r"""
        $A = \{\text{sum is 8}\} = \{(2, 6), (3, 5), (4, 4), (5, 3), (6, 2)\}$

        > $\leadsto$ &nbsp; $\# A = 5$

        $B = \{\text{1st is even}\} = \{(2, 1), (2, 2), \dots, (4, 1), (4, 2), \dots, (6, 5), (6, 6)\}$

        > $\leadsto$ &nbsp; $\# B = 3 \times 6 = 18$

        $A \cap B = \{(2, 6), (4, 4), (6, 2)\}$ &nbsp; $\leadsto$ &nbsp; $\# A \cap B = 3$
        """,
        label="ex-sum8",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # remark: P(A | B) is not P(B | A)
    lk.remark(
        r"""
        in general $P(A \mid B) \neq P(B \mid A)$

        > $\leadsto$ &nbsp; $P(\text{sum is 8} \mid \text{1st is even}) = \dfrac{1}{6} \ \neq \ P(\text{1st is even} \mid \text{sum is 8}) = \dfrac{3}{5}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # remark: multiplication rule and its stages
    _ub = lambda body, label: r"\underbrace{" + body + r"}_{\scriptstyle " + label + "}"
    lk.remark(
        [
            "many times it is useful to read",
            r"$$ P(A \cap B) = P(A \mid B) \, P(B) $$",
            lk.aside(
                r"> $\leadsto$ &nbsp; $P\left( \begin{array}{c} \text{sum is 8 and} \\ \text{1st is even} \end{array} \right) = "
                + _ub(r"P\left( \begin{array}{c} \text{sum is 8 given} \\ \text{1st is even} \end{array} \right)", r"\text{2nd stage}")
                + r" \, "
                + _ub(r"P(\text{1st is even})", r"\text{1st stage}")
                + r"$ $\rule[-1.8em]{0pt}{0pt}$",
                "stages of the random experiment",
            ),
            lk.gap(),
            r"""
            $\leadsto$ &nbsp; generalizations:

            $$
            \begin{aligned}
            P(A \cap B \cap C) &= P(A \mid B \cap C) \, P(B \cap C)\\
            &= P(A \mid B \cap C) \, P(B \mid C) \, P(C)
            \end{aligned}
            $$
            """,
            r"$$ \begin{aligned} "
            + _ub(r"P(A_1 \cap A_2 \cap \dots \cap A_n)", r"n \text{ stages}")
            + r" &= "
            + _ub(r"P(A_1 \mid A_2 \cap \dots \cap A_n)", r"n\text{th}")
            + r"\\[4pt] &\quad \times "
            + _ub(r"P(A_2 \mid A_3 \cap \dots \cap A_n)", r"(n-1)\text{th}")
            + r" \cdots "
            + _ub(r"P(A_{n-1} \mid A_n)", r"\text{2nd}")
            + r" \, "
            + _ub(r"P(A_n)", r"\text{1st}")
            + r" \end{aligned} $$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conditioning
    # remark: frequentist and Bayesian interpretations
    lk.remark(
        [
            "Here we see another possible interpretation of probability",
            "from",
            lk.aside(r"> “relative frequency of event occurrences in infinitely many trials of an experiment”", "frequentist interpretation"),
            "to",
            lk.aside(r"> “measure of belief in the likelihood of event occurrences in each trial of an experiment”", "Bayesian interpretation"),
            lk.gap(),
            r"$\leadsto$ &nbsp; if $P(A)$ is our original measure of belief about $A$, $P(A \mid B)$ is our updated measure of belief about $A$ given new knowledge about $B$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # section
    lk.section("Independence")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # definition: independent events
    lk.definition(
        [
            r"Two events $A, B \subseteq S$ are called **independent** if",
            lk.aside(
                r"""
                $$
                \begin{gathered}
                P(A \mid B) = P(A)\\
                \Updownarrow\\
                P(A \cap B) = P(A) \, P(B)\\
                \Updownarrow\\
                P(B \mid A) = P(B)
                \end{gathered}
                $$
                """,
                [(1, "knowledge about $B$ does not influence<br>our belief about $A$"), (5, "(for $P(A), P(B) > 0$)")],
                rows=5,
            ),
        ],
        label="def-independent",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # example: sum is 7 and 1st is even are independent
    lk.example(
        r"""
        two fair dice &nbsp; $\leadsto$ &nbsp; $S = \{(1, 1), \dots, (6, 6)\}$

        $$
        A = \text{sum is 7} \quad \underset{\text{independent}}{\longleftrightarrow} \quad B = \text{1st is even}
        $$

        $$
        \begin{aligned}
        A &= \{(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)\}\\
        B &= \{(2, 1), (2, 2), \dots, (6, 5), (6, 6)\}
        \end{aligned}
        $$

        $$
        P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{3/36}{18/36} = \frac{1}{6} = \frac{6}{36} = P(A)
        $$
        """,
        label="ex-sum7",
    )
    return


@app.cell(hide_code=True)
def _(dice_sum, lk, outcome_grid, strip):
    # module: independence
    # consequences, with the 36 outcomes of two dice: B = {1st is even} outlined and A = {sum is t} circled, t from the
    # slider
    _t = dice_sum.value
    _fig, _ax = outcome_grid()
    for _k in (2, 4, 6):
        strip(_ax, _k, lk.RED, "$B$")
    for _i in range(1, 7):
        _j = _t - _i
        if 1 <= _j <= 6:
            _ax.plot(_i, _j, "o", ms=15, mfc=lk.LIGHT if _i % 2 == 0 else "white", mec=lk.BLUE, mew=1.4, zorder=3)
    _i0 = max(1, _t - 6)  # the circled outcome with the largest 2nd die carries the label
    _ax.text(_i0 + (0.45 if _i0 % 2 else -0.56), _t - _i0 + (0.36 if _i0 % 2 else 0.3), "$A$", color=lk.BLUE, fontsize=13, ha="center", va="center", zorder=5)

    lk.prose(
        r"$\leadsto$ &nbsp; if $A$ = “sum is 8”, relative counting changes if we know $B$ = “1st is even”",
        r"> > $\Longrightarrow$ &nbsp; $A, B$ not independent",
        r"<span class='lk-ghost'>$\leadsto$ &nbsp;</span> if $A$ = “sum is 7”, relative counting remains same if we know $B$ = “1st is even”",
        r"> > $\Longrightarrow$ &nbsp; $A, B$ independent",
        lk.interactive(_fig, controls=[dice_sum]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # remark: independence is not mutual exclusion
    _no = r"\mathrel{\Longleftrightarrow\mathllap{/\hspace{0.72em}}}"
    lk.remark(
        [
            "independence $\\neq$ mutually exclusive!",
            r"> $P(A \cap B) = P(A) \, P(B)$ &nbsp; $" + _no + r"$ &nbsp; $A \cap B = \emptyset$",
            lk.aside(
                r"> <span class='lk-ghost'>$P(A \cap B) = P(A) \, P(B)$ &nbsp; $" + _no + r"$ &nbsp;</span>$\Longrightarrow$ &nbsp; $\mk{P(A \cap B) = 0}$",
                r"not independent if $P(A) \neq 0$ and $P(B) \neq 0$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # theorem: complements of independent events
    lk.theorem(
        r"If $A$ and $B$ are independent, then so are &nbsp; $A$ and $B^c$, &nbsp; $A^c$ and $B$, &nbsp; $A^c$ and $B^c$",
        label="thm-complements",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # proof
    lk.proof(
        r"""
        $$
        \begin{aligned}
        P(A^c \cap B) &= P(A^c \mid B) \, P(B)\\
        &= \big( 1 - P(A \mid B) \big) \, P(B)\\
        &= \big( 1 - P(A) \big) \, P(B) = P(A^c) \, P(B)
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # definition: pairwise independence
    lk.definition(
        [
            r"$A, B, C \subseteq S$ are **pairwise independent** if",
            lk.aside(
                r"""
                $$
                \left. \begin{aligned}
                P(A \cap B) &= P(A) \, P(B)\\
                P(B \cap C) &= P(B) \, P(C)\\
                P(C \cap A) &= P(C) \, P(A)
                \end{aligned} \right\}
                $$
                """,
                "each pair is independent",
                at="middle",
            ),
        ],
        label="def-pairwise",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # definition: mutual independence
    lk.definition(
        r"""
        $A, B, C \subseteq S$ **mutually independent** if they are pairwise independent and

        $$
        P(A \cap B \cap C) = P(A) \, P(B) \, P(C)
        $$
        """,
        label="def-mutual",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: independence
    # remark: pairwise is not mutual
    lk.remark("Pairwise does not imply mutual independence!")
    return


@app.cell(hide_code=True)
def _(lk, outcome_grid, strip):
    # module: independence
    # example: 1st odd, 2nd odd, sum odd, with the 36 outcomes of two dice: A and B outlined, C marked
    _fig, _ax = outcome_grid(left=-0.4)
    for _i in range(1, 7):
        for _j in range(1, 7):
            if (_i + _j) % 2 == 1:  # C = sum is odd
                _ax.plot(_i, _j, "D", ms=9, mfc="none", mec=lk.GREEN, mew=1.4, zorder=3)
    for _k in (1, 3, 5):
        strip(_ax, _k, lk.BLUE, "$A$")
        strip(_ax, _k, lk.RED, "$B$", across=True)
    _ax.text(0.42, 6.45, "$C$", color=lk.GREEN, fontsize=13, ha="center", va="center")  # at the corner of the diamond (1, 6)

    lk.example(
        [
            r"""
            Roll two dice

            $$
            A = \{\text{1st is odd}\} \qquad B = \{\text{2nd is odd}\} \qquad C = \{\text{sum is odd}\}
            $$

            $$
            \begin{aligned}
            P(A) &= \dfrac{3 \times 6}{36} &\qquad P(A \cap B) &= \dfrac{9}{36} = P(A) \, P(B)\\[10pt]
            P(B) &= \dfrac{3 \times 6}{36} &\qquad P(B \cap C) &= \dfrac{9}{36} = P(B) \, P(C)\\[10pt]
            P(C) &= \dfrac{18}{36} &\qquad P(C \cap A) &= \dfrac{9}{36} = P(C) \, P(A)
            \end{aligned}
            $$

            $$
            P(A \cap B \cap C) = 0
            $$
            """,
            lk.figure(_fig),
            r"""
            $\leadsto$ &nbsp; knowledge about $A$ does not affect our belief in $C$

            > <span class='lk-ghost'>knowledge about</span> $B$ does not affect our belief in $C$

            > knowledge about **$A$ and $B$** affects our belief in $C$
            """,
        ],
        label="ex-pairwise",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: bayes
    # section
    lk.section("Bayes' rule")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: bayes
    # motivation
    lk.prose(r"Bayes' rule &nbsp; $\leadsto$ &nbsp; updating our level of belief in a collection of hypotheses after a new event has occurred")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: bayes
    # example: disease test
    lk.example(
        [
            r"a disease affects 1% of a population",
            r"> $\leadsto$ &nbsp; $P(\text{have disease}) = 1\%$ &nbsp; (disease prevalence)",
            lk.aside(
                r"a test has 90% <span class='lk-mark'>sensitivity</span> and 95% <span class='lk-mark'>specificity</span>",
                r"sensitivity = $P(+\text{ve} \mid \text{disease})$ (true positive rate)<br>specificity = $P(-\text{ve} \mid \text{no disease})$ (true negative rate)",
            ),
            r"> $\leadsto$ &nbsp; what is the probability of having the disease given a positive test?",
            lk.gap(),
            r"""
            $$
            \begin{aligned}
            &\left. \begin{aligned} D &= \text{has disease}\\ D^c &= \text{doesn't have disease} \end{aligned} \right\} \quad P(D) = 1\%, \quad P(D^c) = 99\%\\[10pt]
            &\left. \begin{aligned} T &= \rlap{\text{tested positive}}\hphantom{\text{doesn't have disease}}\\ T^c &= \text{tested negative} \end{aligned} \right\} \quad P(T \mid D) = 90\%, \quad \underbrace{P(T^c \mid D^c) = 95\%}_{P(T \mid D^c) \, = \, 5\%}
            \end{aligned}
            $$
            """,
            r"> $\leadsto$ &nbsp; $P(D \mid T) = \ ?$",
            lk.gap(),
            "Bayes' rule:",
            r"""
            $$
            \begin{aligned}
            P(D \mid T) &= \frac{P(D \cap T)}{P(T)} = \frac{P(T \mid D) \, P(D)}{P(T)} = \frac{P(T \mid D) \, P(D)}{P(T \cap D) + P(T \cap D^c)}\\[8pt]
            &= \frac{P(T \mid D) \, P(D)}{P(T \mid D) \, P(D) + P(T \mid D^c) \, P(D^c)}\\[8pt]
            &= \frac{0.9 \times 0.01}{0.9 \times 0.01 + 0.05 \times 0.99} = \frac{2}{13} \approx 15.4\%
            \end{aligned}
            $$
            """,
        ],
        label="ex-disease",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: bayes
    # theorem-like prose: law of total probability and Bayes' rule
    lk.prose(
        "More generally:",
        r"> If $S = B_1 \cup B_2 \cup \dots \cup B_k$ with $B_i \cap B_j = \emptyset$ for $i \neq j$",
        lk.aside(r"> > $\leadsto$ &nbsp; $\{B_1, B_2, \dots, B_k\}$ is an exhaustive mutually exclusive collection of events", "a partition of $S$"),
        r"$$ P(A) = \sum_{i=1}^{k} P(A \mid B_i) \, P(B_i) \qquad (\text{law of total probability}) $$",
        r"$$ P(B_j \mid A) = \frac{P(A \mid B_j) \, P(B_j)}{\sum_{i=1}^{k} P(A \mid B_i) \, P(B_i)} \qquad (\text{Bayes' rule}) $$",
        r"$P(B_i)$ = prior, &nbsp; $P(B_i \mid A)$ = posterior, &nbsp; $P(A \mid B_i)$ = likelihood",
    )
    return


if __name__ == "__main__":
    app.run()

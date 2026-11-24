import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 2 · Properties of probability; counting methods", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Arc, Figure, lk, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(2, "Properties of probability; counting methods")
    return


@app.cell(hide_code=True)
def _(Arc, Figure, lk, np):
    # Helpers of this lecture: bare sketches, rows of Venn diagrams, stacked words in #( )

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def venn_rows(rows, three=False):
        """Rows of four small Venn diagrams of A (blue), B (red) and, when `three`, C (orange).
        Each panel is (sign, region, remark): `region` is a function of the boolean grids A, B, C
        and is filled; `sign` is written to the left of the panel and `remark` below it."""
        g = np.linspace(0, 1, 600)
        X, Y = np.meshgrid(g * 3.2, g * 2.4)
        cy = 1.5 if three else 1.2
        circles = [((1.2, cy, 0.62), lk.BLUE, "$A$", (0.3, 2.06)), ((2.0, cy, 0.62), lk.RED, "$B$", (2.9, 2.06))]
        if three:
            circles.append(((1.6, 0.85, 0.62), lk.ORANGE, "$C$", (2.55, 0.34)))
        inside = [(X - cx) ** 2 + (Y - c_y) ** 2 < r**2 for (cx, c_y, r), *_ in circles]
        if not three:
            inside.append(np.zeros_like(inside[0]))
        fig = Figure(figsize=(lk.FULL, 1.75 * len(rows)), layout="constrained")
        axes = np.atleast_2d(fig.subplots(len(rows), 4))
        for row, axrow in zip(rows, axes):
            for ax, (sign, region, remark) in zip(axrow, row):
                ax.contourf(X, Y, region(*inside).astype(float), levels=[0.5, 1.5], colors=[lk.LIGHT])
                for (cx, c_y, r), col, name, at in circles:
                    ax.add_patch(Arc((cx, c_y), 2 * r, 2 * r, color=col, lw=1.2))
                    ax.text(*at, name, color=col, fontsize=13, ha="center", va="center")
                ax.plot([0, 3.2, 3.2, 0, 0], [0, 0, 2.4, 2.4, 0], color="black", lw=1.0, solid_joinstyle="miter")
                ax.text(-0.62, 1.2, sign, fontsize=14, ha="center", va="center")
                ax.text(1.6, -0.2, remark, fontsize=12, ha="center", va="top", linespacing=1.1)
                ax.set_xlim(-1.15, 3.3)
                ax.set_ylim(-1.2, 2.5)
                ax.set_aspect("equal")
                ax.axis("off")
        return fig

    def hash2(top, bottom):
        """#( ) of two stacked words: #(ordered / hands)."""
        return r"\#\left( \begin{array}{c} " + top + r" \\ " + bottom + r" \end{array} \right)"

    return blank, hash2, venn_rows


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: random experiments and events, probability measures and spaces, rolling a die (repeated from the end of the last lecture)
    lk.recap(
        lk.aside(
            r"**random experiment** = repeatable, uncertain outcome whose <span class='lk-mark'>set of all outcomes</span> is defined",
            "set of all outcomes = sample space $S$",
        ),
        lk.aside(
            r"**events** in an experiment = collections of outcomes (subsets $A \subseteq S$) <span class='lk-mark'>sharing some property</span>",
            "if outcome has property “$A$”<br>we say “$A$ has occurred”",
        ),
        lk.definition(
            [
                r"A **probability measure** in an experiment is a function $P$ that assigns probabilities to each event",
                lk.aside(r"$$ P : \mk{\mathcal{E}} \longrightarrow \mathbb{R} $$", r"$\mathcal{E}$ = collection of all relevant events"),
                r"$P$ must satisfy 3 axioms",
                r"""
                $$
                \begin{aligned}
                &\bullet \ \ P(A) \geq 0 \quad \forall\, A \in \mathcal{E} && (\text{positivity})\\
                &\bullet \ \ P(S) = 1 && (\text{normalization})\\
                &\bullet \ \ \text{for } A \cap B = \emptyset, \ \ P(A \cup B) = P(A) + P(B) \qquad && (\text{additivity})
                \end{aligned}
                $$
                """,
                r"$\leadsto$ &nbsp; to be precise, we need a bit more from additivity",
                lk.aside(
                    r"""
                    $$
                    \begin{gathered}
                    P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots \qquad (\text{countable additivity})\\[4pt]
                    \text{for } \mk{A_1, A_2, \dots} \ \text{ pairwise disjoint} \ \ (A_i \cap A_j = \emptyset \ \ \forall\, i \neq j)
                    \end{gathered}
                    $$
                    """,
                    r"$A_1, A_2, \dots$ possibly infinite<br>we won't need to be this precise",
                    at="last",
                ),
            ],
        ),
        lk.definition(
            r"We call a triple $(S, \mathcal{E}, P)$ a **probability space** &nbsp; $\leadsto$ &nbsp; a mathematical model for a random experiment",
        ),
        lk.example(
            [
                r"""
                $$
                \begin{aligned}
                S &= \{1, 2, 3, 4, 5, 6\}\\
                \mathcal{E} &= \big\{ \emptyset, \{1\}, \{2\}, \dots, \{1, 2\}, \dots, \{1, 2, 3, 4, 5, 6\} \big\}
                \end{aligned}
                $$
                """,
                lk.aside(r"for a <span class='lk-mark'>“fair”</span> die &nbsp; $P(\{i\}) = P(\{j\}) \quad \forall\, i \neq j \in S$", "extra assumption"),
                r"""
                $$
                \begin{aligned}
                \text{axioms} \quad &\Longrightarrow \quad P(\{i\}) = \frac{1}{6}, \ \ P(\{i, j\}) = \frac{2}{6}, \ \ P(\{i, j, k\}) = \frac{3}{6}, \ \dots\\[6pt]
                &\Longrightarrow \quad P(A) = \frac{\# A}{\# S} \quad \forall\, A \in \mathcal{E}
                \end{aligned}
                $$
                """,
                r"$\leadsto$ &nbsp; but not every die is fair…",
                lk.aside(
                    r"$$ P(\{i\}) = \begin{cases} 0, & i \neq 6\\ 1, & i = 6 \end{cases} \qquad \text{is also possible} $$",
                    "different assumption",
                ),
                lk.aside(
                    r"""
                    $$
                    \begin{aligned}
                    \text{axioms} \quad &\Longrightarrow \quad P(\{i, j\}) = \begin{cases} 0, & i \neq 6 \text{ and } j \neq 6\\ 1, & i = 6 \text{ or } j = 6 \end{cases}\\[6pt]
                    &\Longrightarrow \quad P(A) = \begin{cases} 0, & 6 \notin A\\ 1, & 6 \in A \end{cases}
                    \end{aligned}
                    $$
                    """,
                    r"different probability measure on $(S, \mathcal{E})$",
                    at="last",
                ),
                r"$\leadsto$ &nbsp; different mathematical model for the “dice experiment”",
            ],
            title="rolling a die",
        ),
        topic="Started probability theory",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 2.6")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: properties
    # section
    lk.section("Properties (axioms + algebra of events)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: properties
    # theorem: complement, empty set, monotonicity
    lk.theorem(
        [
            r"Given $A, B \in \mathcal{E}$",
            r"i) &nbsp; $P(A^c) = 1 - P(A)$",
            r"ii) &nbsp; $P(\emptyset) = 0$",
            r"iii) &nbsp; if $A \subseteq B$ then $P(A) \leq P(B)$",
        ],
        label="thm-basic",
    )
    return


@app.cell(hide_code=True)
def _(Arc, blank, lk):
    # module: properties
    # illustration: S ⊇ B ⊇ A, P as relative size
    _fig, _ax = blank(3.2, 2.2, (-0.1, 3.1), (-0.1, 2.1))
    _ax.plot([0, 3, 3, 0, 0], [0, 0, 2, 2, 0], color="black", lw=1.0, solid_joinstyle="miter")
    _ax.add_patch(Arc((1.5, 1.0), 1.4, 1.4, color=lk.RED, lw=1.3))
    _ax.plot([1.2, 1.85, 1.5, 1.2], [0.72, 0.76, 1.38, 0.72], color=lk.BLUE, lw=1.3, solid_joinstyle="miter")
    _ax.text(1.52, 0.94, "$A$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _ax.text(2.3, 1.62, "$B$", color=lk.RED, fontsize=13, ha="center", va="center")
    _ax.text(2.78, 0.22, "$S$", fontsize=13, ha="center", va="center")
    lk.prose(lk.aside(lk.figure(_fig), "$P$ is similar to “relative size” or “relative weight”"))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: properties
    # proof
    lk.proof(
        [
            r"(i) &nbsp; $A \subseteq S \ \Longrightarrow \ A \cup A^c = S$ &nbsp; and &nbsp; $A \cap A^c = \emptyset$",
            r"> $\Longrightarrow$ &nbsp; $P(A \cup A^c) = 1 = P(A) + P(A^c)$",
            r"(ii) &nbsp; $A = S \ \Longrightarrow \ A^c = S^c = \emptyset$",
            r"> $\Longrightarrow$ &nbsp; $P(S \cup \emptyset) = 1 = P(S) + P(\emptyset)$",
            r"> $\Longrightarrow$ &nbsp; $P(\emptyset) = 0$",
            r"(iii) &nbsp; $A \subseteq B \ \Longrightarrow \ B = (B \cap A) \cup (B \cap A^c) = A \cup (B \cap A^c)$",
            lk.aside(r"> with &nbsp; $\mk{A \cap (B \cap A^c) = \emptyset}$", r"since $A \cap (A^c \cap B) = (A \cap A^c) \cap B$"),
            r"> $\Longrightarrow$ &nbsp; $P(B) = P(A) + \underbrace{P(B \cap A^c)}_{\geq 0} \geq P(A)$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: union
    # theorem: union of two events
    lk.theorem(
        [
            r"For $A, B \in \mathcal{E}$",
            r"$$ P(A \cup B) = P(A) + P(B) - P(A \cap B) $$",
        ],
        label="thm-union-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: union
    # proof
    lk.proof(
        [
            r"$A \cup B = A \cup (A^c \cap B)$ &nbsp; (with $A \cap (B \cap A^c) = \emptyset$)",
            r"> $\Longrightarrow$ &nbsp; $P(A \cup B) = P(A) + P(A^c \cap B)$",
            r"$(A^c \cap B) \cup (A \cap B) = B$ &nbsp; (with $(A^c \cap B) \cap (A \cap B) = \emptyset$)",
            r"> $\Longrightarrow$ &nbsp; $P(A^c \cap B) + P(A \cap B) = P(B)$",
            r"> $\Longrightarrow$ &nbsp; $P(A \cup B) = P(A) + P(B) - P(A \cap B)$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, venn_rows):
    # module: union
    # illustration: union = A + B − A ∩ B
    lk.prose(
        lk.figure(
            venn_rows(
                [
                    [
                        ("", lambda A, B, C: A | B, ""),
                        ("$=$", lambda A, B, C: A, ""),
                        ("$+$", lambda A, B, C: B, ""),
                        ("$-$", lambda A, B, C: A & B, "added 2 times"),
                    ]
                ]
            )
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: union
    # theorem: union of three events
    lk.theorem(
        [
            r"For $A, B, C \in \mathcal{E}$",
            r"""
            $$
            \begin{aligned}
            P(A \cup B \cup C) = {} & P(A) + P(B) + P(C)\\
            & - P(A \cap B) - P(A \cap C) - P(B \cap C) + P(A \cap B \cap C)
            \end{aligned}
            $$
            """,
        ],
        label="thm-union-3",
    )
    return


@app.cell(hide_code=True)
def _(lk, venn_rows):
    # module: union
    # illustration: inclusion–exclusion for three events
    lk.prose(
        lk.figure(
            venn_rows(
                [
                    [
                        ("", lambda A, B, C: A | B | C, ""),
                        ("$=$", lambda A, B, C: A, ""),
                        ("$+$", lambda A, B, C: B, ""),
                        ("$+$", lambda A, B, C: C, ""),
                    ],
                    [
                        ("$-$", lambda A, B, C: A & B, "added 2 times"),
                        ("$-$", lambda A, B, C: A & C, "added 2 times"),
                        ("$-$", lambda A, B, C: B & C, "added 2 times"),
                        ("$+$", lambda A, B, C: A & B & C, "added and\nsubtracted 3 times"),
                    ],
                ],
                three=True,
            )
        )
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: union
    # example: two dice, A ∪ B ∪ C
    _fig = Figure(figsize=(3.0, 3.0), layout="constrained")
    _ax = _fig.subplots()
    for _i in (1, 3, 5):
        _ax.fill_between([_i - 0.32, _i + 0.32], 0.6, 6.4, color=lk.BLUE, alpha=0.16, lw=0)
        _ax.fill_between([0.6, 6.4], _i - 0.32, _i + 0.32, color=lk.RED, alpha=0.16, lw=0)
    _ax.plot([0.7, 6.3], [6.3, 0.7], color=lk.ORANGE, lw=1.4)
    for _i in range(1, 7):
        for _j in range(1, 7):
            _in = _i % 2 == 1 or _j % 2 == 1 or _i + _j == 7
            _ax.plot(_i, _j, "o", ms=4.5, color="black" if _in else "white", mec="black", mew=0.9, zorder=3)
    _ax.text(1, 6.75, "$A$", color=lk.BLUE, ha="center", va="center", fontsize=13)
    _ax.text(6.75, 5, "$B$", color=lk.RED, ha="center", va="center", fontsize=13)
    _ax.text(6.55, 0.5, "$C$", color=lk.ORANGE, ha="center", va="center", fontsize=13)
    _ax.set_xlim(0.1, 7.1)
    _ax.set_ylim(0.1, 7.1)
    _ax.set_aspect("equal")
    _ax.set_xticks(range(1, 7), [f"${k}$" for k in range(1, 7)])
    _ax.set_yticks(range(1, 7), [f"${k}$" for k in range(1, 7)])
    _ax.set_xlabel("1st die")
    _ax.set_ylabel("2nd die")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    lk.example(
        [
            lk.aside(r"$S = \{(1, 1), (1, 2), \dots, (6, 6)\}$", "fair dice!"),
            r"$A = \{\text{1st is odd}\}, \quad B = \{\text{2nd is odd}\}, \quad C = \{\text{sum is } 7\}$",
            r"""
            $$
            \begin{aligned}
            P(A \cup B \cup C) &= \frac{3 \times 6}{36} + \frac{3 \times 6}{36} + \frac{6}{36} - \frac{3 \times 3}{36} - \frac{3}{36} - \frac{3}{36} + 0\\[6pt]
            &= \frac{27}{36} = \frac{3}{4}
            \end{aligned}
            $$
            """,
            lk.figure(_fig),
        ],
        title="rolling two dice",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: equally likely
    # definition: equally likely outcomes
    lk.definition(
        [
            r"If $S = \{o_1, \dots, o_n\}$ is finite and $P(\{o_i\}) = P(\{o_j\}) \quad \forall\, i, j \in \{1, \dots, n\}$",
            r"we say $(S, \mathcal{E}, P)$ has **equally likely outcomes**",
        ],
        label="def-equally-likely",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: equally likely
    # theorem: P(A) = #A / #S
    lk.theorem(
        [
            lk.aside(r"If $(S, \mathcal{E}, P)$ has <span class='lk-mark'>equally likely outcomes</span>", "very strong assumption!"),
            r"$$ P(A) = \frac{\# A}{\# S} $$",
        ],
        label="thm-counting",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: equally likely
    # consequence
    lk.prose(r"$\leadsto$ &nbsp; probability becomes a counting problem!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication rule
    # section
    lk.section("Counting methods")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication rule
    # theorem: multiplication rule
    lk.theorem(
        [
            r"Given a set with $m$ elements $\{a_1, \dots, a_m\}$ and another set with $n$ elements $\{b_1, \dots, b_n\}$",
            r"there are exactly $m \cdot n$ possible ordered pairs $(a_i, b_j)$",
        ],
        title="multiplication rule",
        label="thm-multiplication",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication rule
    # proof
    lk.proof(
        [
            r"think of elements $a_i$ as labels of rows and elements $b_j$ as labels of columns of a matrix",
            lk.aside(r"> $\Longrightarrow$ &nbsp; $(a_i, b_j)$ labels its entries", "not a proof… just verification"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication rule
    # example: coin and die
    lk.example(
        [
            r"$S = \{(H, 1), (H, 2), \dots, (H, 6), (T, 1), \dots, (T, 6)\}$",
            r"> $\Longrightarrow$ &nbsp; $\# S = 12 = 2 \times 6$",
        ],
        title="flipping a coin and rolling a die",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication rule
    # consequence: successive stages
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; useful to count total number of outcomes on random experiments with <span class='lk-mark'>successive stages</span>",
            "1st the coin, then the die",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: multiplication rule
    # remark: more than two sets
    lk.remark(
        [
            r"The rule easily extends to more than two sets",
            lk.aside(r"> e.g. &nbsp; $\# A = m, \ \# B = n, \ \# C = p \ \Longrightarrow \ \# (\mk{A \times B \times C}) = mnp$", "ordered triples"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: arrangements
    # example: ordered hands of poker
    lk.example(
        [
            lk.aside(
                r"$S = \{(A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit), (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit), \dots\}$",
                "distinct ordered hands",
            ),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \# S &= \underbrace{\# (\text{1st card})}_{\text{1st stage}} \, \underbrace{\# (\text{2nd card})}_{\text{2nd stage}} \cdots \underbrace{\# (\text{5th card})}_{\text{5th stage}}\\[4pt]
                &= 52 \cdot 51 \cdot 50 \cdot 49 \cdot 48 = \frac{52!}{47!} = \mk{P^{52}_5}
                \end{aligned}
                $$
                """,
                r"$P^{52}_5$ = #(orderings of 52 objects taken 5 at a time)<br>(orderings: arrangements or permutations)",
                at="last",
            ),
        ],
        title="ordered hands of poker",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: arrangements
    # theorem: number of orderings
    lk.theorem(
        [
            r"Given $n$ objects and $r$ positions",
            lk.aside(r"$$ \mk{P^n_r} = \frac{n!}{(n - r)!} = n \cdot (n - 1) \cdot (n - 2) \cdot \dots \cdot (n - r + 1) $$", "number of orderings"),
        ],
        label="thm-arrangements",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: combinations
    # example: real hands of poker
    lk.example(
        [
            lk.aside(r"if we don't care about order", "real = unordered"),
            r"""
            $$
            (A\diamondsuit, 2\heartsuit, 3\spadesuit, 4\clubsuit, 5\diamondsuit) = (A\diamondsuit, 2\heartsuit, 3\spadesuit, 5\diamondsuit, 4\clubsuit) = (2\heartsuit, 3\spadesuit, 5\diamondsuit, A\diamondsuit, 4\clubsuit) = \dots
            $$
            """,
            r"$\leadsto$ &nbsp; $P^{52}_5$ over-counts the hands!",
        ],
        title="real hands of poker",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: combinations
    # theorem: number of combinations
    lk.theorem(
        [
            lk.aside(
                r"$C^n_r = \#$(<span class='lk-mark'>combinations</span> of $n$ objects taken $r$ at a time)",
                "combinations = unordered arrangements",
            ),
            lk.aside(
                r"> $\displaystyle = \frac{P^n_r}{r!} = \frac{n!}{r! \, (n - r)!} = \binom{n}{r}$ &nbsp; (binomial coefficients) $\rule[-1em]{0pt}{2.6em}$",
                r"$\displaystyle (a + b)^n = \sum_{r = 0}^{n} \binom{n}{r} a^r b^{n - r}$<br>$\leadsto$ binomial expansion",
            ),
        ],
        label="thm-combinations",
    )
    return


@app.cell(hide_code=True)
def _(hash2, lk):
    # module: combinations
    # proof: using hands of poker
    _ub = lambda body, label: r"\underbrace{" + body + r"}_{\substack{\text{" + label[0] + r"} \\[2pt] \text{" + label[1] + r"}}}"
    _lhs = r"\underset{\substack{\phantom{x} \\[2pt] \text{deal ordered}}}{" + hash2(r"\text{ordered}", r"\text{hands}") + "}"
    lk.proof(
        [
            r"$$ "
            + _lhs
            + " = "
            + _ub(hash2(r"\text{unordered}", r"\text{hands}"), ("1st stage", "deal unordered"))
            + r" \, "
            + _ub(hash2(r"\text{ways of ordering}", r"\text{one hand}"), ("2nd stage", "order the hand"))
            + r" $$",
            r"$$ " + hash2(r"\text{ordered}", r"\text{hands}") + r" = P^{52}_5 \qquad " + hash2(r"\text{unordered}", r"\text{hands}") + r" = C^{52}_5 = \ ? $$",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                """
                + hash2(r"\text{ways of ordering}", r"\mk{\text{one hand}}")
                + r""" &= \# (\text{1st}) \, \# (\text{2nd}) \, \# (\text{3rd}) \, \# (\text{4th}) \, \# (\text{5th})\\[4pt]
                &= 5 \cdot 4 \cdot 3 \cdot 2 \cdot 1 = 5!
                \end{aligned}
                $$
                """,
                "one hand = 5 cards",
                at=1,
                rows=2,
            ),
            r"> $\Longrightarrow$ &nbsp; $P^{52}_5 = C^{52}_5 \cdot 5!$",
        ],
        title="using hands of poker",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: combinations
    # example: probability of a hand of poker
    lk.example(
        [
            r"$S = \{\text{unordered hands}\} \qquad A = \{\text{all cards of same suit}\}$",
            r"""
            $$
            \begin{aligned}
            \leadsto \quad \# A &= \# (\text{suits}) \cdot \# (\text{hands of given suit})\\[4pt]
            &= 4 \cdot C^{13}_5 = 4 \cdot \frac{13!}{5! \, 8!} = \dots = 4 \cdot 1287 = 5148\\[8pt]
            \leadsto \quad \# S &= C^{52}_5 = 2\,598\,960\\[8pt]
            \Longrightarrow \quad P(A) &= \frac{\# A}{\# S} \approx 0.002 = 0.2\%
            \end{aligned}
            $$
            """,
        ],
        title="probability of a hand of poker",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: combinations
    # example: defective items
    lk.example(
        [
            r"20 items, 3 defective &nbsp; $\leadsto$ &nbsp; pick 4 items (samples)",
            lk.aside(r"> $P(\text{at least one is defective}) = \ ?$", "counting combinations of 1 defective plus 2 defective plus 3 defective is hard…"),
            lk.aside(r"$$ \{\text{at least one defective}\} = \{\text{none defective}\}^c $$", "counting combinations of none defective is much easier!"),
            r"$$ \# \{\text{none defective}\} = C^{17}_4 = \frac{17!}{4! \, 13!} $$",
            r"""
            $$
            \begin{aligned}
            \Longrightarrow \quad P(\text{at least one}) &= 1 - P(\text{none})\\[4pt]
            &= 1 - \frac{C^{17}_4}{C^{20}_4} = 1 - \underbrace{\frac{17!}{20!} \, \frac{16!}{13!}}_{\textstyle \frac{16 \cdot 15 \cdot 14}{20 \cdot 19 \cdot 18}} \approx 50.9\%
            \end{aligned}
            $$
            """,
        ],
        title="defective items",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: replacement
    # motivation: without replacement so far
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; so far, arrangements and combinations of objects <span class='lk-mark'>without replacement</span>",
            "once an object is selected it cannot be selected again",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: replacement
    # theorem: with replacement
    lk.theorem(
        [
            r"Given $n$ objects and $r$ positions",
            r"""
            $$
            \begin{aligned}
            n^r &= \# \, \text{arrangements with replacement}\\[4pt]
            &= \underbrace{\# \left( \begin{array}{c} \text{choices in} \\ \text{1st position} \end{array} \right)}_{n} \underbrace{\# \left( \begin{array}{c} \text{choices in} \\ \text{2nd position} \end{array} \right)}_{n} \cdots \underbrace{\# \left( \begin{array}{c} \text{choices in} \\ r\text{th position} \end{array} \right)}_{n}
            \end{aligned}
            $$
            """,
            r"$$ \binom{n + r - 1}{r} = \# \, \text{combinations with replacement} $$",
        ],
        label="thm-replacement",
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
    # exercise: three dice
    lk.exercise(
        r"""
        Roll 3 fair dice

        What is the probability that at least one is 6?
        """,
        label="ex-practice-1",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: committee
    lk.exercise(
        r"""
        A committee of 5 people is chosen from 8 blue, 6 red

        Assuming each selection is equally likely, what is the probability that exactly two are red?
        """,
        label="ex-practice-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: counting
    lk.exercise(
        r"""
        Count the possibilities of

        a) seating 5 people on 5 chairs

        b) choosing 3 ice-cream flavours from 12 (repetitions allowed)
        """,
        label="ex-practice-3",
    )
    return


if __name__ == "__main__":
    app.run()

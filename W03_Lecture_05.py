import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 5 · Discrete random variables: pmf, cdf, expectation", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(5, "Discrete random variables: pmf, cdf, expectation")
    return


@app.cell(hide_code=True)
def _(lk):
    # Helpers of this lecture: pmf stems and step cdfs

    def plain(ax):
        """No top/right spines."""
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    def stems(ax, xs, pmf, color=lk.BLUE):
        """A pmf: a thin stem with a dot over every point of the state space."""
        ax.vlines(xs, 0, pmf, color=color, lw=1.0)
        ax.plot(xs, pmf, "o", color=color, ms=4.5, zorder=3)
        ax.set_xticks(xs)
        ax.set_xlim(xs[0] - 0.6, xs[-1] + 0.6)
        ax.set_ylim(0, max(pmf) * 1.25)
        plain(ax)

    def steps(ax, xs, levels, color=lk.BLUE):
        """A step cdf: `levels[k]` is the value on the k-th interval cut out by the points `xs`;
        every step is closed on the left and open on the right."""
        edges = [xs[0] - 1] + list(xs) + [xs[-1] + 1]
        for k, lev in enumerate(levels):
            ax.plot([edges[k], edges[k + 1]], [lev, lev], color=color, lw=1.4)
            if k > 0:
                ax.plot(edges[k], lev, "o", color=color, ms=4.5, zorder=3)
            if k < len(levels) - 1:
                ax.plot(edges[k + 1], lev, "o", color=color, ms=4.5, mfc="white", zorder=3)
        ax.set_xlim(edges[0], edges[-1])
        ax.set_ylim(-0.05, 1.15)
        plain(ax)

    return plain, stems, steps


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    coin_p = lk.slider(steps=sorted([round(0.05 * k, 2) for k in range(1, 20)] + [round(1 / 3, 3)]), value=0.5, label=r"$P(\{H\})$")  # 1/3 is the biased coin of the example
    return (coin_p,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: random variables on probability spaces
    lk.recap(
        r"$(S, \mathcal{E}, P)$ probability space",
        r"random variable = function on the sample space $S$",
        r"""
        $X : S \longrightarrow \mathbb{R}$

        > $\leadsto$ &nbsp; $S_X$ = state space = $\mathrm{Im}\, X \subseteq \mathbb{R}$

        > $\leadsto$ &nbsp; $\mathcal{E}_X$ = algebra of subsets of $\mathbb{R}$

        > $\leadsto$ &nbsp; $P_X$ = probability distribution
        """,
        lk.aside(
            r"> > $P_X : \mathcal{E}_X \longrightarrow \mathbb{R}, \qquad P_X(A) = \mk{P(X \in A)}$",
            r"probability that the measurement<br>of $X$ is valued in $A$",
        ),
        topic="Random variables on probability spaces = measurements on random experiments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 3.1–3.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf and cdf
    # section
    lk.section("Discrete random variables")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf and cdf
    # definition: discrete random variable
    lk.definition(
        r"A random variable $X : S \longrightarrow \mathbb{R}$ is **discrete** if $S_X = \mathrm{Im}\, X$ is a countable set",
        label="def-discrete",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf and cdf
    # definition: pmf
    lk.definition(
        [
            r"The **pmf** (probability mass function) of a discrete random variable $X : S \longrightarrow \mathbb{R}$ is the function $f_X : \mathbb{R} \longrightarrow \mathbb{R}$ given by",
            lk.aside(
                r"$$ f_X(x) = P_X(\{x\}) = \mk{P(X = x)} $$",
                r"probability that the measurement<br>of $X$ is exactly equal to $x$",
            ),
        ],
        label="def-pmf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf and cdf
    # remark: the notation of WMS
    lk.remark(r"WMS denotes $f_X(x) = p(x)$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf and cdf
    # consequences: properties of the pmf
    lk.prose(
        r"""
        $\leadsto$ &nbsp; $f_X$ must satisfy:

        > • &nbsp; $f_X(x) \geq 0$

        > • &nbsp; $f_X(x) = 0 \quad$ for $x \notin S_X$
        """,
        lk.aside(
            r"> • &nbsp; $\displaystyle\sum_{x \in A} f_X(x) = P_X(A) \quad$ for $A \subseteq \mathbb{R}$",
            r"$f_X$ completely determines $P_X$",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: pmf and cdf
    # definition: cdf
    lk.definition(
        [
            r"The **cdf** (cumulative distribution function) of a random variable $X : S \longrightarrow \mathbb{R}$ is the function $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ given by",
            lk.aside(
                r"$$ F_X(x) = \mk{P(X \leq x)} $$",
                r"probability that the measurement<br>of $X$ is valued at most $x$",
            ),
        ],
        label="def-cdf",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, steps):
    # module: pmf and cdf
    # consequences: properties of the cdf, with the sketch of a step cdf: the jump at x equals f_X(x)
    _sketch = Figure(figsize=(3.6, 2.4), layout="constrained")
    _ax = _sketch.subplots()
    steps(_ax, [1, 2, 3, 4], [0.0, 0.15, 0.35, 0.75, 1.0])
    lk.arrow(_ax, (3, 0.55), (3, 0.705), lk.GREEN)
    lk.arrow(_ax, (3, 0.55), (3, 0.395), lk.GREEN)
    _ax.text(3.15, 0.55, "$f_X(x)$", color=lk.GREEN, fontsize=12, va="center")
    _ax.text(4.5, 1.06, "$y = F_X(x)$", color=lk.BLUE, fontsize=12, ha="center", va="bottom")
    _ax.set_xticks([2, 3], [r"$x^{\!\!-}$", "$x$"])
    _ax.set_yticks([0, 1])
    _ax.set_ylim(-0.05, 1.3)

    lk.prose(
        r"""
        $\leadsto$ &nbsp; $F_X$ must satisfy

        > • &nbsp; $F_X(x) \geq 0$

        > • &nbsp; $F_X(x_1) \leq F_X(x_2) \quad$ for $x_1 \leq x_2 \in \mathbb{R}$

        > • &nbsp; $\displaystyle\lim_{x \to -\infty} F_X(x) = 0$, &nbsp; $\displaystyle\lim_{x \to +\infty} F_X(x) = 1$
        """,
        lk.aside(
            r"> • &nbsp; $F_X(x) - F_X(\mk{x^-}) = f_X(x) \quad \leadsto \quad F_X(x) = \displaystyle\sum_{t \leq x} f_X(t)$",
            r"$x^-$ = 1st element of $S_X$ smaller than $x$",
        ),
        lk.figure(_sketch),
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, stems, steps):
    # module: pmf and cdf
    # example: roll two fair 4-sided dice, X = max, its pmf and cdf
    _fig = Figure(figsize=(lk.FULL, 2.9), layout="constrained")
    _l, _r = _fig.subplots(1, 2)
    stems(_l, [1, 2, 3, 4], [1 / 16, 3 / 16, 5 / 16, 7 / 16])
    _l.set_yticks([1 / 16, 3 / 16, 5 / 16, 7 / 16], [r"$1/16$", r"$3/16$", r"$5/16$", r"$7/16$"])
    _l.set_xlabel("$x$")
    _l.set_ylabel("$f_X(x)$")
    steps(_r, [1, 2, 3, 4], [0, 1 / 16, 4 / 16, 9 / 16, 1])
    _r.set_xticks([1, 2, 3, 4])
    _r.set_yticks([1 / 16, 1 / 4, 9 / 16, 1], [r"$1/16$", r"$1/4$", r"$9/16$", "$1$"])
    _r.set_xlabel("$x$")
    _r.set_ylabel("$F_X(x)$")

    lk.example(
        [
            r"""
            $S = \{ (i, j) \mid i, j = 1, 2, 3, 4 \}$

            $X(i, j) = \max(i, j) \quad \leadsto \quad S_X = \{1, 2, 3, 4\}$
            """,
            lk.gap(),
            lk.aside(r"$f_X(1) = P(X = 1) = 1/16$", r"$X = 1 \iff (i, j) = (1, 1)$"),
            lk.aside(r"$f_X(2) = P(X = 2) = 3/16$", r"$X = 2 \iff (i, j) = (1, 2), (2, 2), (2, 1)$"),
            lk.aside(r"$f_X(3) = P(X = 3) = 5/16$", r"$X = 3 \iff (i, j) = (1, 3), (2, 3), (3, 3),$<br>$\phantom{X = 3 \iff (i, j) = {}}(3, 2), (3, 1)$"),
            lk.aside(r"$f_X(4) = P(X = 4) = 7/16$", r"$X = 4 \iff (i, j) = (1, 4), (2, 4), (3, 4),$<br>$\phantom{X = 4 \iff (i, j) = {}}(4, 4), (4, 3), (4, 2), (4, 1)$"),
            lk.aside(r"$f_X(5) = f_X(3/2) = f_X(-\pi) = 0$", r"$X$ never takes those values"),
            lk.gap(),
            lk.aside(r"$F_X(1) = P(X \leq 1) = 1/16$", r"$X \leq 1 \iff (i, j) = (1, 1)$"),
            lk.aside(r"$F_X(2) = P(X \leq 2) = 4/16$", r"$X \leq 2 \iff (i, j) = (1, 1), (1, 2), (2, 2), (2, 1)$"),
            lk.aside(r"$F_X(3) = P(X \leq 3) = 9/16$", r"$X \leq 3 \iff (i, j) = (1, 1), \dots, (3, 1)$"),
            lk.aside(
                r"$F_X(4) = P(X \leq 4) = 16/16$",
                r"$X \leq 4 \iff (i, j) = \underbrace{(1, 1), \dots, (4, 1)}_{\text{all outcomes!}}$ $\rule[-1.4em]{0pt}{0pt}$",
            ),
            lk.gap(),
            lk.aside(r"$F_X(5) = 1$", r"$X \leq 5$ for every outcome"),
            lk.aside(r"$F_X(3/2) = 1/16$", r"$X \leq 3/2$ for $(1, 1)$ only"),
            lk.aside(r"$F_X(-\pi) = 0$", r"$X \leq -\pi$ for no outcome"),
            lk.figure(_fig),
        ],
        title="rolling two fair 4-sided dice",
        label="ex-dice",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # section
    lk.section("Expectation")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # motivation: summarize pmfs into numbers
    lk.prose(
        r"""
        $\leadsto$ &nbsp; pmf of a discrete random variable $X : S \longrightarrow \mathbb{R}$ gives the relative frequency of a result $x$ over infinitely many independent measurements

        $\leadsto$ &nbsp; to study their properties, it is useful to summarize the main characteristics of pmfs into certain numbers (mean, variance, …)

        > $\leadsto$ &nbsp; expectations of $X$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # definition: expectation of u(X)
    lk.definition(
        [
            r"Let $X$ be a discrete random variable with pmf $f_X$",
            lk.aside(
                r"Given any function $u : \mathbb{R} \longrightarrow \mathbb{R}$, we define the **expectation** of $\mk{u(X)} = u \circ X : S \longrightarrow \mathbb{R}$",
                r"function of $X$,<br>or composition of $u$ and $X$",
            ),
            lk.aside(r"$$ E[u(X)] = \sum_{x} u(x) \, f_X(x) $$", "(when the sum converges)"),
        ],
        label="def-expectation",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # example: the expectation of the maximum of two dice
    lk.example(
        r"""
        $X(i, j) = \max(i, j)$

        > $\leadsto$ &nbsp; $E[X] = \displaystyle\sum_{x=1}^{4} x \, f_X(x) = 1 \cdot \frac{1}{16} + 2 \cdot \frac{3}{16} + 3 \cdot \frac{5}{16} + 4 \cdot \frac{7}{16} = \frac{50}{16} \approx 3.1$
        """,
        label="ex-max-mean",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # example: game with a die
    _not = r"not fair &nbsp; $\leadsto$ &nbsp; $E[1000 X - 3000]$"
    lk.example(
        [
            r"""
            game: pay 3000 won to roll a 6-sided die

            > get 1000 won times the face value $X$

            > how much do you expect to win?
            """,
            lk.gap(),
            r"fair die &nbsp; $\leadsto$ &nbsp; $E[1000 X - 3000] = \displaystyle\sum_{x=1}^{6} (1000 x - 3000) \times \frac{1}{6} = 500$",
            lk.aside(
                r"<span class='lk-mark'>not fair</span> &nbsp; $\leadsto$ &nbsp; $E[1000 X - 3000] = \displaystyle\sum_{x=1}^{3} (1000 x - 3000) \times \frac{1}{3}$ $\rule[-0.2em]{0pt}{2.2em}$",
                r"say $f_X(1) = f_X(2) = f_X(3) = \frac{1}{3}$,<br>$\phantom{say} f_X(4) = f_X(5) = f_X(6) = 0$",
            ),
            "<span class='lk-ghost'>" + _not + r"</span> $\displaystyle {} + \sum_{x=4}^{6} (1000 x - 3000) \times 0$ $\rule[-0.2em]{0pt}{2.2em}$",
            "<span class='lk-ghost'>" + _not + r"</span> $= -1000$",
        ],
        label="ex-game",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectation
    # consequences: mean, variance and skewness
    lk.prose(
        lk.aside(r"$\leadsto$ &nbsp; **mean** = expectation of $X$", r"measures the “center”<br>of the distribution"),
        r"$$ \mu_X = E[X] = \sum_{x} x \, f_X(x) $$",
        lk.aside(r"$\leadsto$ &nbsp; **variance** = expectation of $(X - \mu_X)^2$", r"measures the “width”<br>of the distribution"),
        lk.aside(
            r"$$ \mk{\sigma_X^2} = E[(X - \mu_X)^2] = \sum_{x} (x - \mu_X)^2 f_X(x) $$",
            r"$\sigma_X^2$ = (standard deviation)$^2$",
        ),
        lk.aside(
            r"$\leadsto$ &nbsp; **skewness** = expectation of $\left( \dfrac{X - \mu_X}{\sigma_X} \right)^3$",
            r"measures “symmetry”<br>around the center",
        ),
        r"$$ \gamma_X = E\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{3} \right] = \sum_{x} \left( \frac{x - \mu_X}{\sigma_X} \right)^{3} f_X(x) $$",
    )
    return


@app.cell(hide_code=True)
def _(Figure, coin_p, lk, math, plain, stems):
    # module: expectation
    # example: toss a coin 4 times, the pmf for any bias with its mean and standard deviation
    _p, _n = coin_p.value, 4
    _xs = list(range(_n + 1))
    _f = [math.comb(_n, _k) * _p**_k * (1 - _p) ** (_n - _k) for _k in _xs]
    _mu = _n * _p
    _sd = math.sqrt(_n * _p * (1 - _p))
    _live = Figure(figsize=(5.6, 3.2), layout="constrained")
    _ax = _live.subplots()
    stems(_ax, _xs, _f)
    _ax.set_ylim(-0.2, 0.85)
    _ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8], ["$0$", "$0.2$", "$0.4$", "$0.6$", "$0.8$"])
    _ax.spines["bottom"].set_visible(False)
    _ax.spines["left"].set_bounds(0, 0.8)
    _ax.tick_params(axis="x", length=0)
    _ax.axhline(0, color="black", lw=0.8)
    _y = -0.08
    _ax.plot([_mu - _sd, _mu + _sd], [_y, _y], color=lk.GREY, lw=1.4)
    for _e in (_mu - _sd, _mu + _sd):
        _ax.plot([_e, _e], [_y - 0.015, _y + 0.015], color=lk.GREY, lw=1.4)
    _ax.plot(_mu, _y, "o", color=lk.GREEN, ms=6, zorder=3)
    _ax.text(_mu, _y - 0.02, r"$\mu_X$", color=lk.GREEN, ha="center", va="top", fontsize=13)
    for _c in (_mu - _sd / 2, _mu + _sd / 2):
        _ax.text(_c, _y - 0.02, r"$\sigma_X$", color=lk.GREY, ha="center", va="top", fontsize=13)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    plain(_ax)

    lk.example(
        [
            r"Toss a coin 4 times, &nbsp; $X$ = number of heads",
            lk.side(
                r"""
                fair coin: $P(\{H\}) = P(\{T\}) = \frac{1}{2}$

                > $\leadsto$ &nbsp; $\mu_X = E[X] = 2$

                > $\leadsto$ &nbsp; $\sigma_X^2 = E[(X - 2)^2] = 1$

                > $\leadsto$ &nbsp; $\gamma_X = E\left[ \left( \dfrac{X - 2}{1} \right)^3 \right] = 0$
                """,
                r"""
                biased coin: $P(\{H\}) = \frac{1}{3}$, $P(\{T\}) = \frac{2}{3}$

                > $\leadsto$ &nbsp; $\mu_X = E[X] = 4/3$

                > $\leadsto$ &nbsp; $\sigma_X^2 = E[(X - 4/3)^2] = 8/9$

                > $\leadsto$ &nbsp; $\gamma_X = E\left[ \left( \dfrac{X - 4/3}{\sqrt{8/9}} \right)^3 \right] = \dfrac{1}{\sqrt{8}}$
                """,
            ),
            lk.interactive(_live, controls=[coin_p]),
        ],
        label="ex-coin-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linearity
    # theorem: linearity of expectation
    lk.theorem(
        r"""
        Let $X$ be a discrete random variable, $u, v : \mathbb{R} \longrightarrow \mathbb{R}$ functions and $a, b, c \in \mathbb{R}$ constants

        $$
        \begin{gathered}
        E[a \, u(X) + b \, v(X)] = a \, E[u(X)] + b \, E[v(X)]\\[6pt]
        E[c] = c
        \end{gathered}
        $$
        """,
        label="thm-linearity",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linearity
    # corollary: variance formula
    lk.corollary(r"$$ \sigma_X^2 = E[X^2] - E[X]^2 $$", label="cor-variance")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linearity
    # proof
    lk.proof(
        [
            r"$E[(X - \mu_X)^2] = E[X^2 - 2 \mu_X X + \mu_X^2]$",
            r"$\phantom{E[(X - \mu_X)^2]} = E[X^2] - 2 \mu_X E[X] + \mu_X^2$",
            r"$\phantom{E[(X - \mu_X)^2]} = E[X^2] - E[X]^2$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: linearity
    # example: the variance of the number of heads in 4 tosses of a fair coin
    lk.example(
        r"""
        flip a fair coin 4 times, &nbsp; $X$ = number of heads

        > $\leadsto$ &nbsp; $E[X] = 0 \times \dfrac{1}{16} + 1 \times \dfrac{4}{16} + 2 \times \dfrac{6}{16} + 3 \times \dfrac{4}{16} + 4 \times \dfrac{1}{16} = \dfrac{32}{16} = 2$ $\rule[-0.9em]{0pt}{2.6em}$

        > $\leadsto$ &nbsp; $E[X^2] = 0^2 \times \dfrac{1}{16} + 1^2 \times \dfrac{4}{16} + 2^2 \times \dfrac{6}{16} + 3^2 \times \dfrac{4}{16} + 4^2 \times \dfrac{1}{16} = \dfrac{80}{16} = 5$ $\rule[-0.9em]{0pt}{2.6em}$

        > > $\Longrightarrow$ &nbsp; $\sigma_X^2 = E[X^2] - E[X]^2 = 5 - 2^2 = 1$
        """,
        label="ex-coin-variance",
    )
    return


if __name__ == "__main__":
    app.run()

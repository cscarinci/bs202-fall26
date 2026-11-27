import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 6 · Binomial and negative binomial models", css_file="lecturekit/style.css")


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
    lk.lecture(6, "Binomial and negative binomial models")
    return


@app.cell(hide_code=True)
def _(Figure):
    # Helpers of this lecture: pmf plots

    def pmf_axes(xlabel, ylabel, h=3.0):
        """A figure with one axis for pmf plots: no top/right spines, plain numbers on the y axis."""
        fig = Figure(figsize=(5.6, h), layout="constrained")
        ax = fig.subplots()
        ax.yaxis.set_major_formatter(lambda v, _: f"${v:g}$")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        return fig, ax

    return (pmf_axes,)


@app.cell(hide_code=True)
def _(lk, mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    bn = lk.slider(1, 40, step=1, value=10, label="$n$")
    bp = lk.slider(0.01, 0.99, step=0.01, value=0.3, label="$p$")
    b_reps = lk.slider(10, 2000, step=10, value=200, label="repetitions of the experiment")
    b_redo = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Repeat")
    nr = lk.slider(1, 10, step=1, value=3, label="$r$")
    nbp = lk.slider(0.1, 0.95, step=0.01, value=0.4, label="$p$")
    return b_redo, b_reps, bn, bp, nbp, nr


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: probability spaces, random variables, distributions, expectation
    lk.recap(
        r"""
        $$
        \begin{array}{ll}
        \text{Probability spaces} & (S, \mathcal{E}, P)\\[6pt]
        \text{Random variables} & X : S \longrightarrow \mathbb{R}\\[6pt]
        \text{Probability distributions} & f_X : \mathbb{R} \longrightarrow \mathbb{R}, \ \ x \longmapsto P(X = x)\\[6pt]
        \text{Expectation} & E[u(X)] = \displaystyle\sum_{x \in S_X} u(x) f_X(x)
        \end{array}
        $$
        """,
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Probabilistic models (specific pmfs)", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 3.4–3.8")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # section
    lk.section("Binomial models")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # definition: binomial model
    lk.definition(
        r"""
        A **binomial model** is a random experiment that

        > 1\. &nbsp; consists of a sequence of identical independent trials

        > 2\. &nbsp; each single trial has one of **two outcomes** with probabilities $P(\text{“success”}) = p$, $P(\text{“failure”}) = 1 - p = q$

        > 3\. &nbsp; measures the number $X$ of “successes” in a fixed number $n$ of trials
        """,
        label="def-binomial-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # illustration: tossing a coin, the sample space, the probability of one outcome and the pmf
    _pq = lambda i: r"\underbrace{P(\{c_" + i + r"\})}_{\begin{array}{l} \scriptstyle p \text{ if } c_" + i + r" = H \\ \scriptstyle q \text{ if } c_" + i + r" = T \end{array}}"
    lk.prose(
        lk.aside(r"$\leadsto$ &nbsp; toss a coin with bias $p = P(\{\mk{H}\})$ $n$ independent times", "“success”"),
        r"""
        > count $X = \#(\text{heads on } n \text{ trials})$

        > $S = \{ (c_1, c_2, \dots, c_n) \mid c_i = H \text{ or } T \}$

        > $S_X = \{0, 1, 2, \dots, n\}$
        """,
        r"$P(\{(c_1, c_2, \dots, c_n)\}) = " + _pq("1") + " " + _pq("2") + r" \cdots " + _pq("n") + r"$ $\rule[-2.4em]{0pt}{0pt}$",
        lk.aside(
            r"$\phantom{P(\{(c_1, c_2, \dots, c_n)\})} = \mk{p^x q^{n-x}}$ &nbsp; if $X(c_1, c_2, \dots, c_n) = x$",
            r"probability of one specific outcome<br>with $x$ heads (if $x \in S_X$)",
        ),
        r"""
        $$
        \begin{aligned}
        f_X(x) &= p^x q^{n-x} \times \underbrace{\#(\text{outcomes with } x \text{ heads})}_{\binom{n}{x}}\\[4pt]
        &= \binom{n}{x} p^x q^{n-x}.
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # definition: binomial distribution
    lk.definition(
        r"""
        A random variable $X$ has a **binomial distribution** on $n$ trials with bias $p$ if its pmf is

        $$
        f_X(x) = \binom{n}{x} p^x q^{n-x}, \qquad \text{for } x = 0, 1, 2, \dots, n,
        $$

        and $f_X(x) = 0$ otherwise.
        """,
        label="def-binomial",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # remark: the pmf sums to 1
    lk.remark(
        r"""
        $$
        \begin{aligned}
        \sum_{x=0}^n f_X(x) &= \sum_{x=0}^n \binom{n}{x} p^x (1 - p)^{n-x}\\
        &= (p + 1 - p)^n = (1)^n = 1\\[4pt]
        &= P(X \in \{0, 1, 2, \dots, n\})
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # example: patients recovering without treatment
    lk.example(
        [
            r"""
            30% of patients recover without treatment

            > what is the probability that 9 out of 10 patients will recover without treatment?
            """,
            lk.aside(r"$X = \#(\text{recovering patients out of } \mk{10})$", "$n = 10$"),
            lk.aside(r"$0.3 = P($<span class='lk-mark'>one patient</span> recovers$) = p$", "out of one"),
            r"> $\Longrightarrow$ &nbsp; $f_X(9) = \dbinom{10}{9} (0.3)^9 (0.7)^{10-9} \approx 0.01\%$",
        ],
        label="ex-patients",
    )
    return


@app.cell(hide_code=True)
def _(b_redo, b_reps, bn, bp, lk, math, np, pmf_axes):
    # module: binomial
    # theorem: mean and variance, with the pmf of B(n, p), its mean np, and the relative frequencies of one simulation of
    # the experiment repeated many times
    _n, _p = bn.value, bp.value
    _xs = list(range(_n + 1))
    _pmf = [math.comb(_n, _k) * _p**_k * (1 - _p) ** (_n - _k) for _k in _xs]
    _rng = np.random.default_rng(606 + b_redo.value)  # toss n coins, count heads, repeat
    _N = b_reps.value
    _freq = np.bincount((_rng.random((_N, _n)) < _p).sum(axis=1), minlength=_n + 1) / _N

    _fig, _ax = pmf_axes("$x$", "$f_X(x)$")
    _high = max(max(_pmf), float(_freq.max()))
    _ax.plot([_n * _p] * 2, [0, _high * 1.12], color=lk.GREEN, lw=1.2, ls=(0, (4, 3)), zorder=1)
    _ax.text(_n * _p, _high * 1.13, "$np$", color=lk.GREEN, fontsize=13, ha="center", va="bottom")
    _ax.text(1.0, 1.0, "relative frequencies", transform=_ax.transAxes, color=lk.RED, fontsize=13, ha="right", va="bottom", clip_on=False)
    _ax.vlines(_xs, 0, _pmf, color=lk.BLUE, lw=1.2, zorder=3)
    _ax.plot(_xs, _pmf, "o", color=lk.BLUE, ms=3.5, zorder=4)
    _ax.plot(_xs, _freq, "o", mfc="none", mec=lk.RED, ms=6.5, mew=1.1, zorder=5)
    _ax.set_xlim(-0.7, _n + 0.7)
    _ax.set_ylim(0, _high * 1.3)
    if _n <= 20:
        _ax.set_xticks(range(_n + 1))

    lk.theorem(
        [
            r"""
            Let $X$ be a binomial random variable on $n$ trials with bias $p$. Then

            $$
            \mu_X = E[X] = np, \qquad \sigma_X^2 = \mathrm{Var}(X) = npq.
            $$
            """,
            lk.interactive(_fig, controls=[bn, bp, b_reps, b_redo]),
        ],
        label="thm-binomial-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: binomial
    # proof
    _g = lambda s: "<span class='lk-ghost'>" + s + "</span> "
    _xx = r"$\leadsto$ &nbsp; $E[X(X - 1)]$"
    _ex2 = r"$\Longrightarrow$ &nbsp; $E[X^2]$"
    _var = r"$\Longrightarrow$ &nbsp; $\mathrm{Var}(X)$"
    lk.proof(
        [
            r"$E[X] = \displaystyle\sum_{x=0}^n x \binom{n}{x} p^x q^{n-x}$ $\rule[-0.2em]{0pt}{2em}$",
            r"$\phantom{E[X]} = \displaystyle\sum_{x=0}^n x \, \frac{n!}{x! \, (n - x)!} \, p^x q^{n-x}$ $\rule[-0.2em]{0pt}{2em}$",
            r"$\phantom{E[X]} = \displaystyle\sum_{x=1}^n \frac{n!}{(x - 1)! \, (n - x)!} \, p^x q^{n-x}$ $\rule[-0.2em]{0pt}{2em}$",
            r"$\phantom{E[X]} = np \underbrace{\displaystyle\sum_{x-1=0}^{n-1} \frac{(n - 1)!}{(x - 1)! \, (n - 1 - x + 1)!} \, p^{x-1} q^{n-1-x+1}}_{(p + q)^{n-1} = 1} = np$ $\rule[-2.6em]{0pt}{0pt}$",
            lk.gap(),
            r"$\mathrm{Var}(X) = E[X^2] - \underbrace{E[X]^2}_{(np)^2}$ $\rule[-2.1em]{0pt}{0pt}$",
            r"> $\leadsto$ &nbsp; $E[X^2] = E[X(X - 1)] + E[X]$",
            r"> $\leadsto$ &nbsp; $E[X(X - 1)] = \displaystyle\sum_{x=0}^n x (x - 1) \frac{n!}{x! \, (n - x)!} \, p^x q^{n-x}$ $\rule[-0.2em]{0pt}{2em}$",
            "> " + _g(_xx) + r"$= \displaystyle\sum_{x=2}^n \frac{n (n - 1)(n - 2)!}{(x - 2)! \, (n - 2 - x + 2)!} \, p^2 p^{x-2} q^{n-x}$ $\rule[-0.2em]{0pt}{2em}$",
            "> " + _g(_xx) + r"$= n (n - 1) p^2 \underbrace{\displaystyle\sum_{x-2=0}^{n-2} \frac{(n - 2)!}{(x - 2)! \, (n - 2 - x + 2)!} \, p^{x-2} q^{n-x}}_{(p + q)^{n-2} = 1}$ $\rule[-2.6em]{0pt}{0pt}$",
            r"> $\Longrightarrow$ &nbsp; $E[X(X - 1)] = n (n - 1) p^2$",
            r"> $\Longrightarrow$ &nbsp; $E[X^2] = E[X(X - 1)] + E[X]$",
            "> " + _g(_ex2) + r"$= n (n - 1) p^2 + np$",
            r"> $\Longrightarrow$ &nbsp; $\mathrm{Var}(X) = E[X^2] - E[X]^2$",
            "> " + _g(_var) + r"$= n (\cancel{n} - 1) p^2 + np - (\cancel{n} p)^2$",
            "> " + _g(_var) + r"$= -np^2 + np = np (1 - p) = npq$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative binomial
    # section
    lk.section("Negative binomial models")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative binomial
    # definition: negative binomial model
    lk.definition(
        r"""
        A **negative binomial model** is an experiment that

        > 1\. &nbsp; consists of a sequence of identical independent trials

        > 2\. &nbsp; each single trial has one of **two outcomes** with probabilities $P(\text{“success”}) = p$, $P(\text{“failure”}) = 1 - p = q$

        > 3\. &nbsp; measures the number $Y$ of trials until a fixed number $r$ of “successes”
        """,
        label="def-nb-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative binomial
    # illustration: tossing a coin until r heads, the sample space, the probability of one outcome and the pmf
    lk.prose(
        r"""
        $\leadsto$ &nbsp; toss a coin with bias $p = P(\{H\})$ until $r$ heads are achieved

        > count $Y = \#(\text{tosses until } r \text{ heads})$

        > $S = \{ (c_1, \dots, c_k) \mid c_i = H \text{ or } T \text{ with } c_k = H \text{ and } r - 1 \text{ other } c_i = H \text{ for } 1 \leq i < k \}$

        > > $\Longrightarrow$ &nbsp; $k \geq r$

        > $S_Y = \{r, r + 1, r + 2, \dots\}$
        """,
        lk.aside(
            r"$P(\{(\underbrace{c_1, \dots, c_{k-1}}_{\text{exactly } r - 1 \ H\text{s}}, \mk{c_k})\}) = p^r q^{k-r}$ &nbsp; if $Y(c_1, \dots, c_k) = k$ $\rule[-1.6em]{0pt}{0pt}$",
            "$c_k = H$",
        ),
        r"""
        $$
        \begin{aligned}
        f_Y(y) &= p^r q^{y-r} \, \underbrace{\#(\text{outcomes with } y \text{ trials})}_{\binom{y-1}{r-1}}\\[4pt]
        &= \binom{y - 1}{r - 1} p^r q^{y-r}.
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk, math, nbp, nr, pmf_axes):
    # module: negative binomial
    # definition: negative binomial distribution, with the pmf of NB(r, p)
    _r, _p = nr.value, nbp.value

    def _f(y):
        return math.comb(y - 1, _r - 1) * _p**_r * (1 - _p) ** (y - _r) if y >= _r else 0.0

    # the support is infinite: the frame runs until 99.5 % of the mass is inside
    _ys, _pmf, _mass = [], [], 0.0
    while _mass < 0.995:
        _ys.append(_r + len(_ys))
        _pmf.append(_f(_ys[-1]))
        _mass += _pmf[-1]

    _fig, _ax = pmf_axes("$y$", "$f_Y(y)$")
    _many = len(_ys) > 80
    _ax.vlines(_ys, 0, _pmf, color=lk.BLUE, lw=0.8 if _many else 1.2, zorder=3)
    _ax.plot(_ys, _pmf, "o", color=lk.BLUE, ms=2 if _many else 3.5, zorder=4)
    _left = 1  # the frame starts at y = 1: the empty stretch before r shows that S_Y starts at r
    _ax.set_xlim(_left - 0.7, _ys[-1] + 0.7)
    _ax.set_ylim(0, max(_pmf) * 1.15)
    if _ys[-1] - _left <= 14:
        _ax.set_xticks(range(_left, _ys[-1] + 1))
    elif _ys[-1] - _left <= 28:  # every second y, so that the numbers stay apart
        _ax.set_xticks(range(_left, _ys[-1] + 1, 2))

    lk.module(
        lk.definition(
            [
                r"""
                A random variable $Y$ has a **negative binomial distribution** with target $r$ and bias $p$ if its pmf is

                $$
                f_Y(y) = \binom{y - 1}{r - 1} p^r q^{y-r}, \qquad \text{for } y = r, r + 1, r + 2, \dots,
                $$

                and $f_Y(y) = 0$ otherwise.
                """,
            ],
            label="def-nb",
        ),
        lk.prose(lk.interactive(_fig, controls=[nr, nbp])),
    )
    return


if __name__ == "__main__":
    app.run()

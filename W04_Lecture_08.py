import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 8 · Poisson, exponential and gamma models", css_file="lecturekit/style.css")


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
    lk.lecture(8, "Poisson, exponential and gamma models")
    return


@app.cell(hide_code=True)
def _(lk, math):
    # Helpers of this lecture: pmfs, and pmf plots with thin stems

    def pois_pmf(m, x):
        """Pois(m)(x), computed through logarithms so that large m, x do not overflow."""
        return math.exp(-m + x * math.log(m) - math.lgamma(x + 1))

    def binom_pmf(n, p, x):
        """B(n, p)(x), zero outside 0 <= x <= n."""
        return math.comb(n, x) * p**x * (1 - p) ** (n - x) if 0 <= x <= n else 0.0

    def stems(ax, xs, ps, color, shift=0.0):
        """pmf plot: thin vertical stems with a dot."""
        _at = [x + shift for x in xs]
        ax.vlines(_at, 0, ps, color=color, lw=1.0)
        ax.plot(_at, ps, "o", color=color, ms=3.5 if len(xs) <= 60 else 2.0)

    def pmf_axis(ax, top):
        """Axis of a pmf plot, with head room for the names of the two series."""
        ax.set_ylim(0, 1.25 * top)
        ax.yaxis.set_major_formatter(lambda v, _pos: f"{v:g}")
        ax.set_xlabel("$x$")
        ax.xaxis.get_major_locator().set_params(integer=True)
        for _s in ("top", "right"):
            ax.spines[_s].set_visible(False)
        ax.spines["left"].set_color(lk.GREY)
        ax.spines["bottom"].set_color(lk.GREY)

    return binom_pmf, pmf_axis, pois_pmf, stems


@app.cell(hide_code=True)
def _(lk, mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    lam_t = lk.slider(0.5, 21, step=0.5, value=2, label=r"$\lambda t$")
    n_sub = lk.slider(1, 200, step=1, value=10, label="$n$")
    p_redo = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Repeat")
    an = lk.slider(1, 500, step=1, value=100, label="$n$")
    ap = lk.slider(0.01, 0.5, step=0.01, value=0.02, label="$p$")
    return an, ap, lam_t, n_sub, p_redo


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: the discrete distributions so far
    lk.recap(
        r"""
        $B(n, p)(x) = \dbinom{n}{x} p^x q^{n-x}$, &nbsp; $0 \leq x \leq n$

        $NB(r, p)(y) = \dbinom{y - 1}{r - 1} p^r q^{y-r}$, &nbsp; $y \geq r$

        $HG(N, K, n)(x) = \dfrac{\dbinom{n}{x} \dbinom{N - n}{K - x}}{\dbinom{N}{K}} = \dfrac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}$, &nbsp; $\max(0, n + K - N) \leq x \leq \min(n, K)$

        $NHG(N, K, r)(y) = \dfrac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}} = \dfrac{K}{N} \, \dfrac{\dbinom{K - 1}{r - 1} \dbinom{N - K}{y - r}}{\dbinom{N - 1}{y - 1}}$, &nbsp; $r \leq y \leq N - K + r$
        """,
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Poisson, exponential and gamma models", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 3.8")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson model
    # section
    lk.section("Poisson models")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson model
    # definition: Poisson model
    lk.definition(
        r"""
        A **Poisson model** is a random experiment that

        > 1\. &nbsp; consists of occurrences along a continuous interval, with the number of occurrences in disjoint subintervals being independent of one another

        > 2\. &nbsp; the average rate of occurrences is a constant $\lambda > 0$, and for small subintervals of length $h$ we have:

        $$
        P\binom{\text{exactly one}}{\text{occurrence}} \approx \lambda h, \qquad P\binom{\text{two or more}}{\text{occurrences}} \approx 0.
        $$

        > 3\. &nbsp; measures the number $X$ of occurrences in a fixed interval of length $t$
        """,
        label="def-poisson-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson model
    # illustration: emails
    lk.prose(
        r"""
        $\leadsto$ &nbsp; emails arrive with average rate $\lambda = 3$ per day

        > $X = \#(\text{emails in 7 days})$

        > > $\Longrightarrow$ &nbsp; $S_X = \{0, 1, 2, \dots\}$
        """
    )
    return


@app.cell(hide_code=True)
def _(Figure, binom_pmf, lam_t, lk, math, n_sub, np, p_redo, pmf_axis, pois_pmf, stems):
    # module: Poisson model
    # argument: the pmf of X as the limit of binomials, with B(n, lambda t / n) against Pois(lambda t) and one run of the
    # n trials
    _m, _n = lam_t.value, n_sub.value
    _top = int(_m + 4 * math.sqrt(_m) + 4)
    _xs = list(range(_top + 1))
    _pois = [pois_pmf(_m, _k) for _k in _xs]
    _p = _m / _n

    _fig = Figure(figsize=(5.6, 3.6), layout="constrained")
    _ax, _tl = _fig.subplots(2, 1, height_ratios=[3, 1])
    _peak = max(_pois)
    stems(_ax, _xs, _pois, lk.BLUE, -0.12)
    if _p <= 1:
        _bin = [binom_pmf(_n, _p, _k) for _k in _xs]
        _peak = max(_peak, max(_bin))
        stems(_ax, _xs, _bin, lk.RED, 0.12)
    pmf_axis(_ax, _peak)
    _ax.text(0.99, 0.99, r"$\mathrm{Pois}(\lambda t)$", color=lk.BLUE, fontsize=12, ha="right", va="top", transform=_ax.transAxes)
    if _p <= 1:
        _ax.text(0.78, 0.99, r"$B(n, \lambda t / n)$", color=lk.RED, fontsize=12, ha="right", va="top", transform=_ax.transAxes)

    # one run of the construction: n subintervals of [0, t], each with an occurrence with probability lambda t / n
    _tl.set_xlim(-0.03, 1.03)
    _tl.set_ylim(-1.6, 1)
    _tl.axis("off")
    _tl.plot([0, 1], [0, 0], color="black", lw=0.9)
    # the subinterval marks merge into a grey band above about 50 subintervals: then only the ends are marked
    _tl.vlines([_k / _n for _k in range(_n + 1)] if _n <= 50 else [0, 1], -0.35, 0.35, color=lk.GREY, lw=0.6)
    _tl.text(0, -0.6, "$0$", fontsize=12, ha="center", va="top")
    _tl.text(1, -0.6, "$t$", fontsize=12, ha="center", va="top")
    if _p <= 1:
        _rng = np.random.default_rng(808 + p_redo.value)
        _hits = np.nonzero(_rng.random(_n) < _p)[0]
        _tl.plot((_hits + 0.5) / _n, np.zeros(len(_hits)), "o", color="black", ms=4 if _n <= 100 else 2.5, zorder=4)
    else:
        _tl.text(0, 0.55, r"need $n \geq \lambda t$", fontsize=12, ha="left", va="bottom")

    lk.prose(
        r"""
        To compute $f_X$

        > i) &nbsp; split $[0, t]$ into $n$ subintervals of length $h = t / n$

        > ii) &nbsp; for large $n$, each subinterval has 0 or 1 occurrence, with

        > > $P(\text{exactly 1 occurrence}) \approx \lambda t / n$

        > > $P(\text{no occurrences}) \approx 1 - \lambda t / n$

        > iii) &nbsp; by assumption each subinterval is independent
        """,
        r"$\therefore$ &nbsp; we can think of our Poisson model as a sequence of identical independent "
        + lk.gloss("trials", "occurrences in each subinterval")
        + r" each with one of two possible outcomes with $P($"
        + lk.gloss("“success”", "occurrence")
        + r"$) \approx \lambda t / n$, &nbsp; $P(\text{“failure”}) \approx 1 - \lambda t / n$, where we are measuring the number $X$ of “successes” in $n$ trials!",
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $f_X(x) \approx B(\mk{n}, \lambda t / n)(x)$",
            r"for large $n$",
        ),
        r"""
        $$
        \begin{aligned}
        \Longrightarrow \quad f_X(x) &= \lim_{n \to \infty} \binom{n}{x} \left( \frac{\lambda t}{n} \right)^x \left( 1 - \frac{\lambda t}{n} \right)^{n-x}\\[4pt]
        &= \lim_{n \to \infty} \underbrace{\frac{n (n - 1) \cdots (n - x + 1)}{n^x}}_{\approx \, 1} \, \frac{(\lambda t)^x}{x!} \left( 1 - \frac{\lambda t}{n} \right)^n \underbrace{\left( 1 - \frac{\lambda t}{n} \right)^{-x}}_{\approx \, 1}\\[4pt]
        &= \frac{(\lambda t)^x}{x!} \underbrace{\lim_{n \to \infty} \left( 1 - \frac{\lambda t}{n} \right)^n}_{e^{-\lambda t}} = e^{-\lambda t} \, \frac{(\lambda t)^x}{x!}, \quad x = 0, 1, 2, \dots\\[18pt]
        \end{aligned}
        $$
        """,
        lk.interactive(_fig, controls=[lam_t, n_sub, p_redo]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson distribution
    # definition: Poisson distribution
    lk.definition(
        [
            r"A random variable $X$ has a **Poisson distribution** with rate $\lambda$ over an interval of length $t$ if its pmf is",
            lk.aside(
                r"""
                $$
                \mk{f_X(x)} = \begin{cases} e^{-\lambda t} \, \dfrac{(\lambda t)^x}{x!}, & x = 0, 1, 2, \dots,\\[8pt] 0, & x \neq 0, 1, 2, \dots \end{cases}
                $$
                """,
                r"$f_X(x) = \mathrm{Pois}(\lambda t)(x)$<br>single parameter",
            ),
        ],
        label="def-poisson",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson distribution
    # example: car accidents
    lk.example(
        [
            r"""
            In Hyeonpung, there is an average of 2 car accidents per month.

            What is more likely this month?

            > $A$ = there will be no accidents

            > $B$ = there will be 3 or more accidents

            $\leadsto$ &nbsp; $X = \#(\text{accidents in one month})$

            $$
            \begin{aligned}
            P(X = 0) &= e^{-2} \approx 13.5\%\\[8pt]
            P(X \geq 3) &= 1 - P(X < 3)\\[4pt]
            &= 1 - e^{-2} - e^{-2} \cdot 2 - e^{-2} \cdot \frac{4}{2!} = 1 - 5 e^{-2} \approx 32.3\%
            \end{aligned}
            $$
            """,
        ],
        label="ex-accidents",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson distribution
    # theorem: mean, variance and skewness
    lk.theorem(
        r"""
        $X$ a Poisson random variable with rate $\lambda$ over a period $t$

        $$
        E[X] = \lambda t, \qquad \mathrm{Var}(X) = \lambda t, \qquad \mathrm{Skew}(X) = \frac{1}{\sqrt{\lambda t}}.
        $$
        """,
        label="thm-poisson-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson distribution
    # proof
    lk.proof(
        [
            r"""
            $E[X] = \displaystyle\sum_{x=0}^{\infty} x \, e^{-\lambda t} \, \frac{(\lambda t)^x}{x!} = \sum_{x=1}^{\infty} e^{-\lambda t} \, \frac{(\lambda t)^x}{(x - 1)!}$

            $\phantom{E[X]} = \displaystyle\underbrace{\sum_{x-1=0}^{\infty} e^{-\lambda t} \, \frac{(\lambda t)^{x-1}}{(x - 1)!}}_{= \, 1} \cdot (\lambda t) = \lambda t\rule[-2.2em]{0pt}{0pt}$
            """,
            lk.gap(),
            r"""
            $\mathrm{Var}(X) = E[X(X - 1)] + E[X] - E[X]^2$

            $\phantom{\mathrm{Var}(X)} = \displaystyle\sum_{x=0}^{\infty} x (x - 1) \, e^{-\lambda t} \, \frac{(\lambda t)^x}{x!} + \lambda t - (\lambda t)^2$

            $\phantom{\mathrm{Var}(X)} = \displaystyle\underbrace{\sum_{x-2=0}^{\infty} e^{-\lambda t} \, \frac{(\lambda t)^{x-2}}{(x - 2)!}}_{= \, 1} (\lambda t)^2 + \lambda t - (\lambda t)^2 = \lambda t\rule[-2.2em]{0pt}{0pt}$
            """,
            lk.gap(),
            r"$\mathrm{Skew}(X) = E\left[ \left( \dfrac{X - \mu_X}{\sigma_X} \right)^3 \right]$",
            lk.aside(
                r"$\phantom{\mathrm{Skew}(X)} = E\left[ \left( \dfrac{X - \lambda t}{\sqrt{\lambda t}} \right)^3 \right] = \displaystyle\sum_{x=0}^{\infty} \left( \frac{x - \lambda t}{\sqrt{\lambda t}} \right)^3 e^{-\lambda t} \, \frac{(\lambda t)^x}{x!} = \cdots$",
                "we will learn later<br>a simpler way...",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, an, ap, binom_pmf, lk, math, pmf_axis, pois_pmf, stems):
    # module: Poisson distribution
    # remark: Poisson approximation of the binomial, with B(n, p) against Pois(np)
    _n, _p = an.value, ap.value
    _m = _n * _p
    _lo = max(0, int(_m - 4 * math.sqrt(_m) - 4))
    _top = int(_m + 4 * math.sqrt(_m) + 4)
    _xs = list(range(_lo, _top + 1))
    _bin = [binom_pmf(_n, _p, _k) for _k in _xs]
    _pois = [pois_pmf(_m, _k) for _k in _xs]

    _fig = Figure(figsize=(5.6, 3.0), layout="constrained")
    _ax = _fig.subplots()
    stems(_ax, _xs, _bin, lk.RED, 0.12)
    stems(_ax, _xs, _pois, lk.BLUE, -0.12)
    pmf_axis(_ax, max(max(_bin), max(_pois)))
    _ax.text(0.99, 0.99, r"$\mathrm{Pois}(np)$", color=lk.BLUE, fontsize=12, ha="right", va="top", transform=_ax.transAxes)
    _ax.text(0.80, 0.99, r"$B(n, p)$", color=lk.RED, fontsize=12, ha="right", va="top", transform=_ax.transAxes)

    lk.remark(
        [
            r"""
            $\mathrm{Pois}(\lambda t)$ is also useful as an approximation for $B(n, p)$ for large $n$, small $p$, with $\lambda t = np$

            $$
            B(n, p)(x) \approx \mathrm{Pois}(np)(x).
            $$
            """,
            lk.interactive(_fig, controls=[an, ap]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma model
    # section
    lk.section("Gamma models")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma model
    # definition: gamma model
    lk.definition(
        r"""
        A **gamma model** is a random experiment that

        > 1\. &nbsp; consists of occurrences along a continuous interval, with the number of occurrences in disjoint subintervals being independent of one another

        > 2\. &nbsp; the average rate of occurrences is a constant $\lambda > 0$, and for small subintervals of length $h$ we have:

        $$
        P\binom{\text{exactly one}}{\text{occurrence}} \approx \lambda h, \qquad P\binom{\text{two or more}}{\text{occurrences}} \approx 0.
        $$

        > 3\. &nbsp; measures the length $Y$ until a fixed number $r$ of occurrences is achieved
        """,
        label="def-gamma-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma model
    # illustration: emails
    lk.prose(
        r"$\leadsto$ &nbsp; emails arriving at an average rate $\lambda = 3$ per day",
        lk.aside(r"> $Y = \mk{\text{time until the 2nd email}}$", "not necessarily an integer"),
        lk.aside(r"> $\mk{S_Y = (0, \infty)}$", "not discrete!"),
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
    # exercise: balls without replacement
    lk.exercise(
        r"""
        A box contains 5 red, 4 blue, 3 green balls. Select 3 without replacement, and let $X = \#(\text{red balls out of 3})$

        > a) &nbsp; What is the pmf of $X$?

        > b) &nbsp; Find $E[X]$ and $\mathrm{Var}(X)$

        > c) &nbsp; If we allow replacement, what is the pmf?
        """,
        label="ex-balls",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: defects along a cable
    lk.exercise(
        r"""
        Defects occur along a cable according to a Poisson model with rate 0.5 per meter. Let $N = \#(\text{defects in the first 4 meters})$

        > a) &nbsp; What is the pmf of $N$? What is its state space?

        > b) &nbsp; Find $P(N = 0)$ and $P(N \geq 2)$
        """,
        label="ex-cable",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: distances until the first and second defect
    lk.exercise(
        r"""
        For the same cable above, let

        > $Y$ = distance until 1st defect

        > $Z$ = distance until 2nd defect

        > a) &nbsp; Express $\{Y > 4\}$ and $\{Z > 4\}$ as events involving $N$

        > b) &nbsp; Find $P(\{Y > 4\})$ and $P(\{Z > 4\})$
        """,
        label="ex-cable-distances",
    )
    return


if __name__ == "__main__":
    app.run()

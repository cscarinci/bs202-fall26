import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 7 · Hypergeometric and negative hypergeometric models", css_file="lecturekit/style.css")


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
    lk.lecture(7, "Hypergeometric and negative hypergeometric models")
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # Helpers of this lecture: pmf plots with thin stems

    def pmf_axes(xlabel, h=2.8):
        """A full-width figure with one axis for pmf plots: integer ticks, no top/right spines."""
        from matplotlib.ticker import FuncFormatter, MaxNLocator

        fig = Figure(figsize=(5.6, h), layout="constrained")
        ax = fig.subplots()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:g}$"))
        ax.set_xlabel(xlabel)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        return fig, ax

    def stems(ax, xs, ps, color, dx=0.0, dots=None):
        """A pmf as thin vertical stems with a dot, shifted sideways by `dx` to sit next to a second pmf;
        on a long range (more than 60 values) the stems would merge, so only the dots are drawn."""
        if (len(xs) > 60) if dots is None else dots:
            ax.plot(xs, ps, "o", color=color, ms=2.2)
        else:
            pos = [x + dx for x in xs]
            ax.vlines(pos, 0, ps, color=color, lw=1.0)
            ax.plot(pos, ps, "o", color=color, ms=3.5)

    return pmf_axes, stems


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    hN = lk.slider(10, 1000, step=10, value=1000, label="$N$")
    hK = lk.slider(1, 200, step=1, value=50, label="$K$")
    hn = lk.slider(1, 200, step=1, value=100, label="$n$")
    gN = lk.slider(2, 200, step=1, value=30, label="$N$")
    gK = lk.slider(1, 60, step=1, value=10, label="$K$")
    gr = lk.slider(1, 20, step=1, value=3, label="$r$")
    return gK, gN, gr, hK, hN, hn


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: binomial and negative binomial models
    lk.recap(
        r"""
        Binomial models

        > $\leadsto$ &nbsp; count number of “successes” in a fixed number of trials
        """,
        lk.aside(
            r"> $S = \{ c_1 c_2 \cdots c_{\mk{n}} \mid c_i = \mk{H} \text{ or } \mk{T} \}$",
            r"$n$ = number of trials<br>$H$ = success with $P(\{H\}) = p$<br>$T$ = failure with $P(\{T\}) = 1 - p = q$",
        ),
        r"""
        > $P(\underbrace{c_1 c_2 \cdots c_n}_{r \ H\text{s}}) = p^r (1 - p)^{n-r} = p^r q^{n-r}$

        > $X(c_1 c_2 \cdots c_n) = \#(H \text{ in } n \text{ trials})$
        """,
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\mk{f_X(x)} = \begin{cases} \mk{\dbinom{n}{x}} p^x q^{n-x}, & \text{for } x = \underbrace{0, 1, 2, \dots, n}_{S_X},\\[8pt] 0, & \text{otherwise} \end{cases}$",
            r"$f_X(x) = B(n, p)(x)$<br>$\binom{n}{x}$ = # combinations of $x$ objects in $n$ positions",
        ),
        lk.gap(),
        r"""
        Negative binomial models

        > $\leadsto$ &nbsp; count number of trials until a fixed target of successes is achieved
        """,
        r"> $S = \{ c_1 \cdots c_{n-1} c_n \mid$ "
        + lk.gloss(r"$n \geq r$", r"$n$ allowed to vary!")
        + r"$, \ c_n = H, \ c_i = H \text{ or } T \text{ for } 1 \leq i \leq n - 1, \text{ and } \#(H \text{ in } c_1 \cdots c_{n-1}) = r - 1 \}$",
        r"> $P(\underbrace{c_1 \cdots c_{n-1}}_{r - 1 \ H\text{s}}$" + lk.gloss(r"$c_n$", r"$c_n$ always $= H$") + r"$) = p^r q^{n-r}$",
        r"> $Y(c_1 \cdots c_{n-1} c_n) = \#(\text{trials until } r \ H)$",
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\mk{f_Y(y)} = \begin{cases} \mk{\dbinom{y - 1}{r - 1}} p^r q^{y-r}, & \text{for } y = \underbrace{r, r + 1, \dots}_{S_Y},\\[8pt] 0, & \text{otherwise} \end{cases}$",
            r"$f_Y(y) = NB(r, p)(y)$<br>$\binom{y-1}{r-1}$ = # combinations of $r - 1$ objects<br>in $y - 1$ positions",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # theorem: mean, variance and skewness of binomial and negative binomial random variables (from last time)
    lk.theorem(
        r"""
        $X$ binomial random variable with bias $p$ on $n$ trials

        $Y$ negative binomial random variable with bias $p$ and target $r$

        $$
        \begin{aligned}
        E[X] &= \mu_X = np, & \qquad E[Y] &= \mu_Y = r / p\\[8pt]
        \mathrm{Var}(X) &= \sigma_X^2 = npq, & \qquad \mathrm{Var}(Y) &= \sigma_Y^2 = \frac{rq}{p^2}\\[8pt]
        \mathrm{Skew}(X) &= \gamma_X = \frac{q - p}{\sqrt{npq}}, & \qquad \mathrm{Skew}(Y) &= \gamma_Y = \frac{1 + q}{\sqrt{rq}}.
        \end{aligned}
        $$
        """,
        label="thm-binomial-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Hypergeometric and negative hypergeometric models", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 3.7")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypergeometric
    # section
    lk.section("Hypergeometric models")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypergeometric
    # definition: hypergeometric model
    lk.definition(
        [
            r"A **hypergeometric model** is an experiment that",
            lk.aside(r"> 1\. &nbsp; consists of a sequence of <span class='lk-mark'>trials</span>", "not independent!"),
            r"""
            > 2\. &nbsp; each single trial has one of two outcomes, with exactly $K$ possible “successes” and $N - K$ possible “failures” in total, with all combinations of the $K$ possible successes among the $N$ possible trials being equally likely

            > 3\. &nbsp; measures the number $X$ of “successes” in a fixed number $n$ of trials
            """,
        ],
        label="def-hg-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypergeometric
    # illustration: coins from a bag, the sample space, the probabilities of outcomes, two checks and the pmf
    lk.prose(
        r"""
        $\leadsto$ &nbsp; draw coins from a bag with $K$ red and $N - K$ blue coins, without replacing them

        > count $X = \#(\text{red coins in } n \text{ draws})$

        > $S = \{ c_1 c_2 \cdots c_n \mid c_i = R \text{ or } B, \ i = 1, \dots, n \}$

        > $S_X = \{0, 1, \dots, n\}$ &nbsp; (if $n \leq K$ and $n \leq N - K$)

        $$
        P(\{c_1 c_2 \cdots c_n\}) = \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}}, \quad \text{if } X(c_1 c_2 \cdots c_n) = x.
        $$

        > $\leadsto$ &nbsp; $N = 5$, $K = 3$, $n = 3$

        $$
        \begin{aligned}
        P(\{RBB\}) &= \frac{3}{5} \cdot \frac{2}{4} \cdot \frac{1}{3} = \frac{\dbinom{5 - 3}{3 - 1}}{\dbinom{5}{3}} = \frac{1}{\dfrac{5!}{2! \, 3!}}\\[12pt]
        P(\{BRR\}) &= \frac{2}{5} \cdot \frac{3}{4} \cdot \frac{2}{3} = \frac{\dbinom{5 - 3}{3 - 2}}{\dbinom{5}{3}} = \frac{2!}{\dfrac{5!}{2! \, 3!}}
        \end{aligned}
        $$

        > $\leadsto$ &nbsp; $N = 9$, $K = 5$, $n = 4$

        $$
        P(\{BBBR\}) = \frac{\dbinom{5}{4}}{\dbinom{9}{5}} = \frac{4}{9} \cdot \frac{3}{8} \cdot \frac{2}{7} \cdot \frac{5}{6}
        $$
        """,
        r"""
        $$
        \begin{aligned}
        f_X(x) &= \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}} \times \underbrace{\#(\text{outcomes with } x \ R\text{s})}_{\binom{n}{x}}\\[8pt]
        &= \frac{\dbinom{n}{x} \dbinom{N - n}{K - x}}{\dbinom{N}{K}} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypergeometric
    # definition: hypergeometric distribution
    lk.definition(
        [
            r"A random variable $X$ has a **hypergeometric distribution** if its pmf is",
            lk.aside(
                r"$$ \mk{f_X(x)} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}, \quad \text{for } x \in \mathbb{Z}, \ 0 \leq x \leq K \text{ and } 0 \leq n - x \leq N - K, $$",
                r"$f_X(x) = HG(N, K, n)(x)$",
            ),
            r"and $f_X(x) = 0$ otherwise.",
        ],
        label="def-hg",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypergeometric
    # example: defective devices
    lk.example(
        r"""
        A factory produced 1000 devices, 50 defective

        > we check a sample of 100 distinct devices

        > Probability of 7 defective objects in the sample?

        $X = \#\dbinom{\text{defective objects}}{\text{in a sample of } 100}$

        > $\leadsto$ &nbsp; $HG(1000, 50, 100)(x) = \dfrac{\dbinom{50}{x} \dbinom{1000 - 50}{100 - x}}{\dbinom{1000}{100}} = f_X(x)$

        > $\leadsto$ &nbsp; $f_X(7) \approx 11\%$

        > <span class='lk-ghost'>$\leadsto$ &nbsp; </span>$f_X(5) \approx 19\%$

        > <span class='lk-ghost'>$\leadsto$ &nbsp; </span>$f_X(3) \approx 14\%$
        """,
        label="ex-devices",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative hypergeometric
    # section
    lk.section("Negative hypergeometric models")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative hypergeometric
    # definition: negative hypergeometric model, with its state space and pmf
    lk.definition(
        [
            r"""
            A **negative hypergeometric model** is an experiment

            > 1\. &nbsp; consists of a sequence of trials

            > 2\. &nbsp; each single trial has one of two outcomes with exactly $K$ possible “successes” and $N - K$ possible “failures” in total, with all combinations of the $K$ possible successes among the $N$ possible trials being equally likely

            > 3\. &nbsp; measures the number $Y$ of trials until a fixed number $r$ of “successes”
            """,
            lk.gap(),
            r"$S_Y = \{r, r + 1, \dots, N - K + r\}$ &nbsp; ($r \leq K$)",
            lk.aside(
                r"$$ \mk{f_Y(y)} = \frac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}}. $$",
                r"$f_Y(y) = NHG(N, K, r)(y)$",
            ),
        ],
        label="def-nhg-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative hypergeometric
    # remark: the four models
    lk.remark(
        lk.aside(
            r"""
            $$
            \begin{array}{ccc}
            \text{Binomial} & \mk{\longleftrightarrow} & \text{Hypergeometric}\\[6pt]
            \mk{\big\updownarrow} & & \big\updownarrow\\[6pt]
            \text{Negative binomial} & \longleftrightarrow & \text{Negative hypergeometric}
            \end{array}
            $$
            """,
            r"$\longleftrightarrow$ : replacement allowed vs not allowed<br>$\updownarrow$ : \# successes in $n$ trials vs<br>\# trials until $r$ successes",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative hypergeometric
    # theorem: mean and variance
    lk.theorem(
        [
            r"""
            For $X$ a hypergeometric random variable

            > $Y$ a negative hypergeometric random variable

            $E[X] = n \, \dfrac{K}{N}$

            $\phantom{E[X]} = np$ &nbsp; if $p = K / N$
            """,
            r"$\mathrm{Var}(X) = n \, \dfrac{K}{N} \left( 1 - \dfrac{K}{N} \right) \dfrac{N - n}{N - 1}$",
            lk.aside(
                r"$\phantom{\mathrm{Var}(X)} = np(1 - p) \times \mk{\dfrac{N - n}{N - 1}}$",
                "finite population correction term",
            ),
            r"""
            $E[Y] = r \, \dfrac{N + 1}{K + 1}$, &nbsp; $\mathrm{Var}(Y) = \dfrac{r (N + 1)(N - K)(K + 1 - r)}{(K + 1)^2 (K + 2)}$
            """,
        ],
        label="thm-hg-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: negative hypergeometric
    # proof sketch
    lk.sketch(
        [
            r"""
            similar trick as for binomial

            $$
            x \binom{K}{x} = K \binom{K - 1}{x - 1}, \qquad y \binom{y - 1}{r - 1} = r \binom{y}{r}
            $$

            together with the binomial coefficient identity

            $$
            \binom{N}{n} = \sum_{\substack{0 \leq x \leq K \\ 0 \leq n - x \leq N - K}} \binom{K}{x} \binom{N - K}{n - x}
            $$

            > $\leadsto$ &nbsp; $(1 + t)^N = (1 + t)^K (1 + t)^{N-K}$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \sum_n \binom{N}{n} t^{N-n} &= \sum_x \binom{K}{x} t^{K-x} \cdot \sum_\ell \binom{N - K}{\ell} t^{N-K-\ell}\\[4pt]
                &= \sum_x \sum_\ell \binom{K}{x} \binom{N - K}{\ell} t^{\mk{N - x - \ell}} = \sum_x \binom{K}{x} \binom{N - K}{n - x} t^{N-n}
                \end{aligned}
                $$
                """,
                r"$x + \ell = n$",
                at="last",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(gK, gN, gr, hK, hN, hn, lk, math, pmf_axes, stems):
    # module: negative hypergeometric
    # illustration: HG(N, K, n) against B(n, K/N) and NHG(N, K, r) against NB(r, K/N), each with its mean
    def _hg_figure():
        _N, _K, _n = hN.value, hK.value, hn.value
        _fig, _ax = pmf_axes("$x$")
        _ax.text(0, 1.03, "$HG(N, K, n)$", color=lk.BLUE, fontsize=12, ha="left", va="bottom", transform=_ax.transAxes)
        _ax.text(1, 1.03, "$B(n, p)$,  $p = K/N$", color=lk.RED, fontsize=12, ha="right", va="bottom", transform=_ax.transAxes)
        if not (_K <= _N and _n <= _N):
            _ax.axis("off")
            _ax.text(0.5, 0.5, r"need $K \leq N$ and $n \leq N$", fontsize=12, ha="center", va="center", transform=_ax.transAxes)
            return _fig
        _p = _K / _N
        _lo, _hi = max(0, _n - (_N - _K)), min(_K, _n)
        _total = math.comb(_N, _n)
        _xs = list(range(_n + 1))
        _hg = [math.comb(_K, _i) * math.comb(_N - _K, _n - _i) / _total if _lo <= _i <= _hi else 0.0 for _i in _xs]
        _bi = [math.comb(_n, _i) * _p**_i * (1 - _p) ** (_n - _i) for _i in _xs]
        _keep = [_i for _i in _xs if _hg[_i] > 5e-4 or _bi[_i] > 5e-4]
        _a, _b = _keep[0], _keep[-1]
        _mean = _n * _p
        _top = max(max(_hg), max(_bi))
        # HG is drawn only on S_X: no zero dots along the axis
        _on = [_i for _i in range(_a, _b + 1) if _lo <= _i <= _hi]
        _dots = _b - _a + 1 > 60
        stems(_ax, _on, [_hg[_i] for _i in _on], lk.BLUE, -0.15, _dots)
        stems(_ax, _xs[_a : _b + 1], _bi[_a : _b + 1], lk.RED, 0.15, _dots)
        _ax.set_xlim(min(_a, _mean) - 1, max(_b, _mean) + 1)
        _ax.set_ylim(0, 1.3 * _top)
        _ax.plot([_mean, _mean], [0, 1.06 * _top], color=lk.GREEN, lw=1.0, ls=(0, (4, 3)))
        _ax.text(_mean, 1.12 * _top, "$nK/N = np$", color=lk.GREEN, fontsize=12, ha="center", va="bottom")
        return _fig

    def _nhg_figure():
        _N, _K, _r = gN.value, gK.value, gr.value
        _fig, _ax = pmf_axes("$y$")
        _ax.text(0, 1.03, "$NHG(N, K, r)$", color=lk.BLUE, fontsize=12, ha="left", va="bottom", transform=_ax.transAxes)
        _ax.text(1, 1.03, "$NB(r, p)$,  $p = K/N$", color=lk.RED, fontsize=12, ha="right", va="bottom", transform=_ax.transAxes)
        if not (_K <= _N and _r <= _K):
            _ax.axis("off")
            _ax.text(0.5, 0.5, r"need $K \leq N$ and $r \leq K$", fontsize=12, ha="center", va="center", transform=_ax.transAxes)
            return _fig
        _p = _K / _N
        _total = math.comb(_N, _K)
        _last = _N - _K + _r

        def _nb(y):
            return math.comb(y - 1, _r - 1) * _p**_r * (1 - _p) ** (y - _r)

        # NHG lives on r, ..., N - K + r; NB has no upper end: continue until it is negligible
        _ys = list(range(_r, _last + 1))
        while _nb(_ys[-1] + 1) > 5e-4 or _ys[-1] + 1 < _r / _p:
            _ys.append(_ys[-1] + 1)
        _nhg = [math.comb(_y - 1, _r - 1) * math.comb(_N - _y, _K - _r) / _total if _y <= _last else 0.0 for _y in _ys]
        _nbs = [_nb(_y) for _y in _ys]
        _keep = [_i for _i in range(len(_ys)) if _nhg[_i] > 5e-4 or _nbs[_i] > 5e-4] or list(range(len(_ys)))
        _a, _b = _keep[0], _keep[-1]
        _mean = _r * (_N + 1) / (_K + 1)
        _top = max(max(_nhg), max(_nbs))
        _on = [_i for _i in range(_a, _b + 1) if _ys[_i] <= _last]
        _dots = _b - _a + 1 > 60
        stems(_ax, [_ys[_i] for _i in _on], [_nhg[_i] for _i in _on], lk.BLUE, -0.15, _dots)
        stems(_ax, _ys[_a : _b + 1], _nbs[_a : _b + 1], lk.RED, 0.15, _dots)
        _ax.set_xlim(min(_ys[_a], _mean) - 1, max(_ys[_b], _mean) + 1)
        _ax.set_ylim(0, 1.3 * _top)
        _ax.plot([_mean, _mean], [0, 1.06 * _top], color=lk.GREEN, lw=1.0, ls=(0, (4, 3)))
        _ax.text(_mean, 1.12 * _top, "$r(N+1)/(K+1)$", color=lk.GREEN, fontsize=12, ha="center", va="bottom")
        return _fig

    lk.prose(
        lk.interactive(_hg_figure(), controls=[hN, hK, hn]),
        lk.interactive(_nhg_figure(), controls=[gN, gK, gr]),
    )
    return


if __name__ == "__main__":
    app.run()

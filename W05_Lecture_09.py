import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 9 · Continuous random variables; gamma and exponential distributions", css_file="lecturekit/style.css")


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
    lk.lecture(9, "Continuous random variables; gamma and exponential distributions")
    return


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    g_lam = lk.slider(1, 4, step=0.1, value=1, label=r"$\lambda$")
    g_r = lk.slider(1, 3, step=1, value=2, label="$r$")
    g_a = lk.slider(0, 10, step=0.1, value=0, label="$a$")
    g_b = lk.slider(0, 10, step=0.1, value=3, label="$b$")
    m_lam = lk.slider(0.1, 2, step=0.1, value=2, label=r"$\lambda$")
    m_s = lk.slider(steps=[round(k / 30, 4) for k in range(0, 31)], value=0.6667, label="$s$")
    m_t = lk.slider(steps=[round(k / 30, 4) for k in range(1, 31)], value=0.3333, label="$t$")
    return g_a, g_b, g_lam, g_r, m_lam, m_s, m_t


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap: Poisson and gamma models
    lk.recap(
        lk.aside(
            r"$X = \#($<span class='lk-mark'>occurrences</span> in fixed interval $[0, t])$",
            r"constant average rate $\lambda$<br>independent for disjoint intervals",
        ),
        r"""
        > $S_X = \{0, 1, 2, \dots\}$

        > $f_X(x) = e^{-\lambda t} \, \dfrac{(\lambda t)^x}{x!}$ &nbsp; $\leadsto$ &nbsp; $\displaystyle\sum_{x=0}^{\infty} e^{-\lambda t} \, \frac{(\lambda t)^x}{x!} = e^{-\lambda t} e^{\lambda t} = 1$
        """,
        lk.gap(),
        r"$Y$ = length of interval until $r$ occurrences",
        lk.aside(
            r"> $\mk{S_Y = (0, +\infty)}$",
            "continuous (not countable)",
        ),
        topic="Poisson and gamma models",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Random variables with continuous state spaces", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 4.1, 4.2, 4.6")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuous random variables
    # section
    lk.section("Continuous random variables")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuous random variables
    # recall: discrete random variables, pmf and cdf
    lk.recall(
        [
            r"""
            $X : S \longrightarrow \mathbb{R}$ discrete random variable

            > if $S_X = \mathrm{Im}(X)$ is countable
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $P_X(A) = P(X \in A) = \displaystyle\sum_{x \in A \cap S_X} \mk{f_X(x)}$",
                r"$f_X(x)$ = pmf<br>= $P(X = x)$",
            ),
            lk.aside(
                r"> $\leadsto$ &nbsp; $\mk{F_X(x)} = P(X \leq x) = \displaystyle\sum_{y \in (-\infty, x] \cap S_X} f_X(y)$",
                r"$F_X(x)$ = cdf",
            ),
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $f_X(x) = F_X(x) - F_X(\mk{x^-})$",
                r"$x^-$ = first element in $S_X$<br>smaller than $x$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuous random variables
    # definition: continuous random variable, through its cdf
    lk.definition(
        [
            r"""
            A random variable $X : S \longrightarrow \mathbb{R}$ is **continuous** if

            > • &nbsp; $S_X$ is uncountable
            """,
            lk.aside(
                r"> • &nbsp; there exists $\mk{F_X} : \mathbb{R} \longrightarrow \mathbb{R}$ continuous such that",
                r"$F_X$ = cdf",
            ),
            lk.aside(
                r"$$ P(X \leq x) = \mk{F_X(x)}. $$",
                r"does not follow from the<br>assumption on $S_X$ only!",
            ),
        ],
        label="def-continuous-cdf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuous random variables
    # corollary: no point carries probability
    lk.corollary(
        [
            lk.aside(
                r"$X$ continuous random variable &nbsp; $\Longrightarrow$ &nbsp; $\mk{P(X = x) = 0}$ $\ \forall \, x \in \mathbb{R}$",
                "no notion of pmf",
            ),
            r"<span class='lk-ghost'>$X$ continuous random variable &nbsp; </span>$\Longrightarrow$ &nbsp; $P(a \leq X \leq b) = F_X(b) - F_X(a)$",
        ],
        label="cor-no-pmf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuous random variables
    # definition: continuous random variable, through its pdf
    lk.definition(
        [
            lk.aside(
                r"A random variable $X : S \longrightarrow \mathbb{R}$ is **continuous** if",
                "from now on: continuous = has a pdf",
            ),
            r"> • &nbsp; $S_X$ is uncountable",
            lk.aside(
                r"> • &nbsp; there exists $\mk{f_X} : \mathbb{R} \longrightarrow \mathbb{R}$ integrable such that",
                r"$f_X$ = pdf (probability density function)",
            ),
            r"""
            $$
            P(a \leq X \leq b) = \int_a^b f_X(x) \, dx = F_X(b) - F_X(a).
            $$
            """,
        ],
        label="def-continuous-pdf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: continuous random variables
    # consequences: properties of cdf and pdf, and how one gives the other
    lk.prose(
        r"""
        $\leadsto$ &nbsp; $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ must satisfy

        > • &nbsp; $F_X(x_1) \leq F_X(x_2) \quad \forall \, x_1 \leq x_2$

        > • &nbsp; $\displaystyle\lim_{x \to -\infty} F_X(x) = 0$, &nbsp; $\displaystyle\lim_{x \to +\infty} F_X(x) = 1$

        $\leadsto$ &nbsp; $f_X$ must satisfy

        > • &nbsp; $f_X(x) \geq 0 \quad \forall \, x \in \mathbb{R}$

        > • &nbsp; $\displaystyle\int_{-\infty}^{+\infty} f_X(x) \, dx = 1$

        Given $F_X$ &nbsp; $\Longrightarrow$ &nbsp; $f_X(x) = \dfrac{d}{dx} F_X(x)$

        Given $f_X$ &nbsp; $\Longrightarrow$ &nbsp; $F_X(x) = \displaystyle\int_{-\infty}^{x} f_X(u) \, du$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma distribution
    # section
    lk.section("The gamma distribution")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma distribution
    # example: the gamma random variable of a Poisson process is continuous
    lk.example(
        r"""
        Given $X$ a Poisson random variable with average rate $\lambda$ over an interval $[0, t]$, the corresponding Gamma random variable $Y$ with average rate $\lambda$ and occurrence target $r$ is a continuous random variable!
        """,
        label="ex-gamma-continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma distribution
    # proof: the pdf of the gamma random variable
    lk.proof(
        [
            lk.aside(
                r"Note that $\mk{P(X \geq r) = P(Y \leq t)}$",
                r"at least $r$ occurrences by length $t$<br>= at most length $t$ until $r$ occurrences",
            ),
            r"""
            $$
            \begin{aligned}
            &\Longrightarrow \quad \sum_{x=r}^{\infty} e^{-\lambda t} \, \frac{(\lambda t)^x}{x!} = P(Y \leq t) = F_Y(t)\\[4pt]
            &\Longrightarrow \quad f_Y(t) = \frac{d}{dt} \left( \sum_{x=r}^{\infty} e^{-\lambda t} \, \frac{(\lambda t)^x}{x!} \right) = \sum_{x=r}^{\infty} \lambda e^{-\lambda t} \left( -\frac{(\lambda t)^x}{x!} + \frac{(\lambda t)^{x-1}}{(x-1)!} \right)\\[4pt]
            &\phantom{\Longrightarrow \quad f_Y(t)} = \lambda e^{-\lambda t} \left[ \sum_{x=r}^{\infty} \frac{(\lambda t)^{x-1}}{(x-1)!} - \sum_{x=r}^{\infty} \frac{(\lambda t)^x}{x!} \right]\\[4pt]
            &\phantom{\Longrightarrow \quad f_Y(t)} = \lambda e^{-\lambda t} \, \frac{(\lambda t)^{r-1}}{(r-1)!} = \underbrace{\frac{\lambda^r t^{r-1}}{(r-1)!} \, e^{-\lambda t}}_{\mathrm{Gamma}(r, \lambda)(t)}.\\[22pt]
            \end{aligned}
            $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gamma distribution
    # remark: the same derivation for the negative binomial and negative hypergeometric distributions
    lk.remark(
        [
            r"Similarly, we can derive $NB(r, p)$ from $B(n, p)$ and $NHG(N, K, r)$ from $HG(N, K, n)$.",
            lk.aside(
                r"$$ P(X_n \geq r) = P(Y_r \leq n) $$",
                r"at least $r$ Hs in $n$ flips<br>= at most $n$ flips until $r$ Hs",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, g_a, g_b, g_lam, g_r, lk, math, np):
    # module: gamma distribution
    # definition: gamma distribution, with the pdf curves r = 1, 2, 3 of the sketch and P(a <= Y <= b) on pdf and cdf
    _lam, _r, _a, _b = g_lam.value, g_r.value, g_a.value, g_b.value

    def _pdf(y, r):
        return _lam**r * y ** (r - 1) / math.factorial(r - 1) * np.exp(-_lam * y)

    def _cdf(t, r):
        return 1 - sum(np.exp(-_lam * t) * (_lam * t) ** k / math.factorial(k) for k in range(r))

    # the frame reaches at least 10 and at least the 99.5 % point of the chosen r
    _grid = np.linspace(0, 200, 4001)
    _xmax = max(10.0, float(np.ceil(_grid[np.argmax(_cdf(_grid, _r) >= 0.995)])))
    _y = np.linspace(0, _xmax, 500)
    _fig = Figure(figsize=(lk.FULL, 2.6), layout="constrained")
    _ax, _cx = _fig.subplots(1, 2)

    if _a <= _b:
        _yy = np.linspace(_a, _b, 200)
        _ax.fill_between(_yy, _pdf(_yy, _r), color=lk.LIGHT, lw=0)
    for _x, _name, _ha in ((_a, "$a$", "right" if _a <= _b else "left"), (_b, "$b$", "left" if _a <= _b else "right")):
        _ax.axvline(_x, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.annotate(_name, (_x, 1.0), xycoords=("data", "axes fraction"), textcoords="offset points", xytext=(-2 if _ha == "right" else 2, 3), ha=_ha, va="bottom", fontsize=12, annotation_clip=False)
    _spot = {1: (0.3, (5, 0), "center"), 2: (1.2, (3, 3), "bottom"), 3: (3.5, (3, 3), "bottom")}  # (lambda x, offset, va): a free spot beside each curve
    for _k in sorted({1, 2, 3, _r}):
        _col = lk.BLUE if _k == _r else lk.GREY
        _ax.plot(_y, _pdf(_y, _k), color=_col, lw=1.4 if _k == _r else 1.0, zorder=3 if _k == _r else 2)
        _x = _spot[_k][0] / _lam
        _ax.annotate(f"$r = {_k}$", (_x, float(_pdf(_x, _k))), textcoords="offset points", xytext=_spot[_k][1], ha="left", va=_spot[_k][2], color=_col, fontsize=12, zorder=5, annotation_clip=False)
    _ax.set_xlim(0, _xmax)
    _ax.set_ylim(0, 1.05 * _lam)
    _ax.set_xlabel("$y$")
    _ax.set_ylabel("$f_Y(y)$")

    # cdf of the chosen r: the same probability as a difference of two values
    _Fa, _Fb = float(_cdf(_a, _r)), float(_cdf(_b, _r))
    _cx.plot(_y, _cdf(_y, _r), color=lk.BLUE, lw=1.4)
    for _x, _F in ((_a, _Fa), (_b, _Fb)):
        _cx.plot([_x, _x, 0], [0, _F, _F], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    if _a <= _b:
        _cx.plot([0, 0], [_Fa, _Fb], color=lk.GREEN, lw=3.5, solid_capstyle="butt", clip_on=False, zorder=4)
    _cx.set_xlim(0, _xmax)
    _cx.set_ylim(0, 1.05)
    _cx.set_xlabel("$y$")
    _cx.set_ylabel("$F_Y(y)$")
    for _axx in (_ax, _cx):
        for _s in ("top", "right"):
            _axx.spines[_s].set_visible(False)
        _axx.xaxis.set_major_formatter(lambda v, _p: f"{v:g}")
        _axx.yaxis.set_major_formatter(lambda v, _p: f"{v:g}")

    lk.module(
        lk.definition(
            [
                r"""
                A continuous random variable $Y : S \longrightarrow \mathbb{R}$ has a **gamma distribution** with rate $\lambda$ and target $r$ if its pdf is

                $$
                f_Y(y) = \begin{cases} \dfrac{\lambda^r y^{r-1}}{(r-1)!} \, e^{-\lambda y}, & y \in (0, +\infty),\\[8pt] 0, & y \notin (0, +\infty). \end{cases}
                $$
                """,
            ],
            label="def-gamma",
        ),
        lk.prose(lk.interactive(_fig, controls=[g_lam, g_r, g_a, g_b])),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: exponential distribution
    # section
    lk.section("The exponential distribution")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: exponential distribution
    # example: car accidents
    lk.example(
        [
            r"""
            Hyeonpung has 2 car accidents per month

            > $P(\text{1 car accident in less than } \underbrace{\text{10 days}}_{1/3 \text{ months}}) = \ ?\rule[-1.4em]{0pt}{0pt}$

            > > $\leadsto$ &nbsp; $Y$ = time until 1 accident
            """,
            lk.aside(
                r"> > > $\Longrightarrow$ &nbsp; $\mk{f_Y(y) = \lambda e^{-\lambda y}}$",
                r"$\mathrm{Gamma}(1, \lambda) = \mathrm{Exp}(\lambda)$<br>(exponential distribution)",
            ),
            r"""
            $$
            \begin{aligned}
            \underbrace{P(Y \leq 1/3)}_{F_Y(1/3)} &= \int_{0}^{1/3} \lambda e^{-\lambda y} \, dy\\[4pt]
            &= -e^{-\lambda y} \Big|_{0}^{1/3} = 1 - e^{-\lambda / 3}\\[4pt]
            &= 1 - e^{-2/3} \approx 48.7\%
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $$
            \begin{aligned}
            P\left( \begin{array}{c} \text{1 car accident in the 10 days after} \\ \text{20 days without accidents} \end{array} \right) &= \ ?\\[4pt]
            &= P(Y \leq 1 \mid Y > 2/3)\\[4pt]
            &= \frac{P(2/3 < Y \leq 1)}{P(2/3 < Y)} = \frac{F_Y(1) - F_Y(2/3)}{1 - F_Y(2/3)}\\[4pt]
            &= \frac{(1 - e^{-\lambda}) - (1 - e^{-2\lambda/3})}{1 - (1 - e^{-2\lambda/3})}\\[4pt]
            &= \frac{e^{-2\lambda/3} - e^{-\lambda}}{e^{-2\lambda/3}} = 1 - e^{-\lambda/3}\\[4pt]
            &= 1 - e^{-2/3} \approx 48.7\%
            \end{aligned}
            $$
            """,
        ],
        label="ex-accidents",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, m_lam, m_s, m_t, np):
    # module: exponential distribution
    # theorem: the exponential distribution is memoryless, with the areas P(Y <= t), P(s < Y <= s + t), P(Y > s)
    _l, _s, _t = m_lam.value, m_s.value, m_t.value

    def _f(y):
        return _l * np.exp(-_l * y)

    _fig = Figure(figsize=(5.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _hi = max(1.4 * (_s + _t) + 0.3, min(6 / _l, 3 * (_s + _t)))  # the frame follows s + t
    _top = 1.5 * _l
    _yy = np.linspace(0, _t, 100)
    _ax.fill_between(_yy, _f(_yy), color=lk.LIGHT, lw=0)
    # (s, s + t] and (s, oo) get flat see-through fills of their label colours, so that overlaps stay visible
    _yy = np.linspace(_s, _hi, 200)
    _ax.fill_between(_yy, _f(_yy), color=lk.GREY, alpha=0.18, lw=0)
    _yy = np.linspace(_s, _s + _t, 100)
    _ax.fill_between(_yy, _f(_yy), color=lk.BLUE, alpha=0.25, lw=0)
    for _x in (_t, _s, _s + _t):
        _ax.plot([_x, _x], [0, _f(_x)], color=lk.GREY, lw=1.0)
    _y = np.linspace(0, _hi, 400)
    _ax.plot(_y, _f(_y), color=lk.BLUE, lw=1.4)

    # area labels above the curve, stacked so that they never meet (u = one point in data units, roughly)
    _u = _top / 150
    _x1, _x2, _x3 = _t / 2, _s + _t / 2, _s + _t + 0.08 * _hi
    _y1, _y2, _y3 = (_f(_x) + 3 * _u for _x in (_x1, _x2, _x3))
    _y2 = max(_y2, _y3 + 18 * _u)
    _y1 = max(_y1, _y2 + 18 * _u)
    for _x, _yv, _name, _c in ((_x1, _y1, r"$P(Y \leq t)$", "black"), (_x2, _y2, r"$P(s < Y \leq s + t)$", lk.BLUE), (_x3, _y3, r"$P(Y > s)$", lk.GREY)):
        _ax.annotate(_name, (_x, _yv), textcoords="offset points", xytext=(4, 0), ha="left", va="bottom", fontsize=12, color=_c)

    # the marks 0, t and s, s + t on two rows, so that they stay apart for every s and t
    for _x, _name, _row, _ha in ((0, "$0$", 0, "right"), (_t, "$t$", 0, "left"), (_s, "$s$", 1, "right"), (_s + _t, "$s + t$", 1, "left")):
        _ax.annotate(_name, (_x, 0), xycoords=("data", "axes fraction"), textcoords="offset points", xytext=(-1 if _ha == "right" else 1, -5 - 16 * _row), ha=_ha, va="top", fontsize=12, annotation_clip=False)
    _ax.set_xlim(0, _hi)
    _ax.set_ylim(0, _top)
    _ax.set_xticks([])
    _ax.set_ylabel("$f_Y(y)$")
    _ax.set_yticks([_l], [r"$\lambda$"])  # the height of the curve at 0; the room above is for the labels
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)

    lk.theorem(
        [
            lk.aside(
                r"The <span class='lk-mark'>exponential distribution</span> has no memory!",
                r"gamma with $r = 1$",
            ),
            lk.aside(
                r"> If $\mk{Y \sim \mathrm{Exp}(\lambda)}$, then",
                r"$Y$ has $f_Y(y) = \mathrm{Exp}(\lambda)(y)$",
            ),
            lk.aside(
                r"$$ P(Y \leq s + t \mid Y > s) = \mk{P(Y \leq t)}. $$",
                r"the remaining waiting time does not depend<br>on how long we have already waited",
            ),
            lk.interactive(_fig, controls=[m_lam, m_s, m_t]),
        ],
        label="thm-memoryless",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: exponential distribution
    # example: LED lightbulbs
    lk.example(
        [
            lk.aside(
                r"LED lightbulbs have failure rate of $\lambda = 0.2$ per year following an <span class='lk-mark'>exponential model</span>",
                "approximately",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; the probability of a failure in the next 3 months is independent of how long ago you bought the lightbulb!

            > > $P(Y \leq s + 1/4 \mid Y > s) = P(Y \leq 1/4)$

            > > <span class='lk-ghost'>$P(Y \leq s + 1/4 \mid Y > s)$ </span>$= 1 - e^{-\lambda / 4} \approx 0.05$
            """,
        ],
        label="ex-lightbulbs",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: exponential distribution
    # remark: the geometric distribution is memoryless too
    lk.remark(
        r"""
        The negative binomial distribution with target $r = 1$ is also memoryless!

        > $NB(1, p) = \mathrm{Geom}(p)$ is called the **geometric distribution**
        """
    )
    return


if __name__ == "__main__":
    app.run()

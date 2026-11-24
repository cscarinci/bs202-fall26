import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 12 · Uniform, beta and Gaussian distributions", css_file="lecturekit/style.css")


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
    lk.lecture(12, "Uniform, beta and Gaussian distributions")
    return


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    b_n = lk.slider(1, 30, step=1, value=10, label="$n$")
    b_r = lk.slider(1, 30, step=1, value=3, label="$r$")
    b_y = lk.slider(0, 1, step=0.01, value=0.25, label="$y$")
    g_m = lk.slider(1, 60, step=1, value=2, label="$m$")
    return b_n, b_r, b_y, g_m


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(
            r"$m_X(t) = E[e^{tX}]$, &nbsp; $\mk{K_X(t)} = \ln(m_X(t))$",
            r"$K_X(t)$ = cumulant generating function",
        ),
        r"""
        > $\Longrightarrow$ &nbsp; $\begin{cases} E[X^k] = \dfrac{d^k}{dt^k} \Big|_{t=0} m_X(t)\\[10pt] E[(X - \mu_X)^k] = \dfrac{d^k}{dt^k} \Big|_{t=0} K_X(t) \quad (\text{for } k = 2, 3) \end{cases}$
        """,
        topic="Moments and the mgf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Families of continuous random variables

        $\leadsto$ &nbsp; uniform, beta, Gaussian
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 4.4, 4.5, 4.7")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: uniform
    # section
    lk.section("The uniform distribution")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: uniform
    # definition: uniform model
    lk.definition(
        r"""
        A **uniform model** is a random experiment that

        1. consists of a single occurrence along $(a, b)$
        2. the probability of occurrence in any subinterval is proportional to its length (all are equally likely)
        3. measures the position of the occurrence
        """,
        label="def-uniform-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: uniform
    # prose: the bakery, one sale between 9AM and 9PM
    lk.prose(
        r"""
        $\leadsto$ &nbsp; a bakery is open from 9AM to 9PM, assuming sales are equally likely at any time

        > $Y$ = time until sale &nbsp; $\leadsto$ &nbsp; $S_Y = (9, 21)$

        > > $\Longrightarrow$ &nbsp; $P(Y \leq y) = {\large\tfrac{y - 9}{21 - 9}} = {\large\tfrac{y - 9}{12}}$

        > > $\Longrightarrow$ &nbsp; $f_Y(y) = {\large\tfrac{1}{12}}$, $y \in (9, 21)$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: uniform
    # definition: uniform distribution
    lk.definition(
        [
            r"A random variable $Y$ has **uniform distribution** over $[a, b]$ if its pdf is",
            lk.aside(
                r"""
                $$
                \mk{f_Y(y)} = \begin{cases} \dfrac{1}{b - a}, & y \in (a, b)\\[8pt] 0, & y \notin (a, b) \end{cases}
                $$
                """,
                r"$= \mathrm{Unif}(a, b)(y)$",
            ),
        ],
        label="def-uniform",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: uniform
    # theorem: mean, variance and skewness of the uniform distribution
    # the pdf 1/(b - a) between a and b
    _fig = Figure(figsize=(3.6, 1.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-1.0, 4.3)
    _ax.set_ylim(-0.5, 2.0)
    _ax.set_aspect("equal")
    _ax.axis("off")
    lk.arrow(_ax, (-0.3, 0), (4.2, 0), "black", lw=0.9)
    lk.arrow(_ax, (0, -0.2), (0, 1.95), "black", lw=0.9)
    _ax.plot([1, 1], [0, 1.2], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([3, 3], [0, 1.2], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([0, 1], [1.2, 1.2], color=lk.GREY, lw=0.8, ls=(0, (2, 3)))
    _ax.plot([1, 3], [1.2, 1.2], color=lk.BLUE, lw=1.4)
    _ax.plot([1, 3], [1.2, 1.2], "o", mfc="white", mec=lk.BLUE, ms=5, mew=1.2, zorder=3)
    _ax.plot([-0.07, 0.07], [1.2, 1.2], color="black", lw=0.9)
    _ax.text(-0.18, 1.2, r"$\dfrac{1}{b-a}$", ha="right", va="center", fontsize=13)
    _ax.text(1, -0.14, "$a$", ha="center", va="top", fontsize=13)
    _ax.text(3, -0.14, "$b$", ha="center", va="top", fontsize=13)
    _ax.text(4.2, -0.14, "$y$", ha="center", va="top", fontsize=13)
    lk.theorem(
        [
            r"""
            Given $Y \sim \mathrm{Unif}(a, b)$

            $$
            E[Y] = \frac{a + b}{2}, \qquad \mathrm{Var}(Y) = \frac{(b - a)^2}{12}, \qquad \mathrm{Skew}(Y) = 0
            $$
            """,
            lk.figure(_fig),
        ],
        label="thm-uniform-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: uniform
    # proof
    lk.proof(
        r"""
        $$
        E[Y] = \int_a^b y \, \frac{1}{b - a} \, dy = \frac{y^2 / 2}{b - a} \, \Big|_a^b = \frac{1}{2} \, \frac{b^2 - a^2}{b - a} = \frac{a + b}{2}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # section
    lk.section("The beta distribution")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # definition: beta model
    lk.definition(
        r"""
        A **beta model** is a random experiment that

        1. consists of a fixed number $n$ of occurrences along a unit interval $(0, 1)$
        2. each occurrence being independent and following a uniform model on $(0, 1)$
        3. measures the position $Y$ of the $r$th occurrence
        """,
        label="def-beta-model",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # prose: the bakery, time until the 3rd of 10 cakes, and the pdf of Y
    lk.prose(
        r"""
        $\leadsto$ &nbsp; a bakery sells 10 cakes in one shift
        """,
        lk.aside(
            r"> $Y$ = <span class='lk-mark'>time</span> until sale of the 3rd cake (assuming sales are equally likely at any time)",
            "in shifts",
        ),
        r"""
        > > $\Longrightarrow$ &nbsp; $S_Y = (0, 1)$
        """,
        lk.gap(),
        r"""
        $f_Y(y) = \ ?$
        """,
        lk.aside(
            r"> Let $X = \#(\text{cakes sold in } \mk{y} \text{ shifts})$",
            r"$y \in (0, 1)$",
        ),
        r"""
        > > (2) &nbsp; $\Longrightarrow$ &nbsp; each sale happens in $(0, y)$ with probability $y$

        > > <span class='lk-ghost'>(2) &nbsp; </span>$\Longrightarrow$ &nbsp; $X \sim \mathrm{Binom}(10, y)$

        > > <span class='lk-ghost'>(2) &nbsp; </span>$\Longrightarrow$ &nbsp; $\displaystyle P(Y \leq y) = P(X \geq 3) = \sum_{x=3}^{10} \binom{10}{x} y^x (1 - y)^{10 - x}$

        > > <span style='white-space: nowrap'><span class='lk-ghost'>(2)&nbsp;&nbsp;&nbsp;</span>$\displaystyle\begin{aligned} \Longrightarrow\enspace f_Y(y) &= \frac{d}{dy} \left[ \sum_{x=3}^{10} \binom{10}{x} y^x (1 - y)^{10 - x} \right]\\[4pt] &= \sum_{x=3}^{10} \underbrace{\binom{10}{x} x}_{10 \binom{9}{x - 1}} y^{x - 1} (1 - y)^{10 - x} - \sum_{x=3}^{9} \underbrace{\binom{10}{x} (10 - x)}_{10 \binom{9}{x}, \ x \neq 10} y^x (1 - y)^{9 - x}\\[4pt] &= 10 \left[ \sum_{x=3}^{10} \binom{9}{x - 1} y^{x - 1} (1 - y)^{10 - x} - \sum_{x=3}^{9} \binom{9}{x} y^x (1 - y)^{9 - x} \right]\\[4pt] &= 10 \left[ \sum_{\tilde{x}=2}^{9} \binom{9}{\tilde{x}} y^{\tilde{x}} (1 - y)^{9 - \tilde{x}} - \sum_{x=3}^{9} \binom{9}{x} y^x (1 - y)^{9 - x} \right]\\[4pt] &= 10 \binom{9}{2} y^2 (1 - y)^7 = n \binom{n - 1}{r - 1} y^{r - 1} (1 - y)^{n - r}, \quad y \in (0, 1) \end{aligned}$</span>
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # remark: r and n - r + 1
    lk.remark(
        r"""
        <span class="lk-tab" style="--lk-tab: 4.6em">$r$</span>= target occurrence counting from the start

        <span class="lk-tab" style="--lk-tab: 4.6em">$n - r + 1$</span>= target occurrence counting from the end
        """
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # module: beta
    # scene: the beta model simulated
    # top: ten runs of n uniform points on (0, 1), the r-th from the left ringed; the points left of y are red and
    # counted in the column X; bottom: the pdf Beta(r, n - r + 1) over the histogram of Y in 10,000 runs, with the area
    # P(Y <= y) = P(X >= r) shaded
    def beta_scene(n, r, y0):
        _fig = Figure(figsize=(5.6, 4.6), layout="constrained")
        _ok = r <= n
        _rng = np.random.default_rng(1212)
        _runs, _rows = 10000, 10
        _pts = np.sort(_rng.random((_runs, n)), axis=1)
        _top, _bot = _fig.subplots(2, 1, height_ratios=[1, 1.4])
        for _k in range(_rows):
            _left = _pts[_k] <= y0
            _top.plot(_pts[_k][~_left], np.full((~_left).sum(), -_k), "|", color="black", ms=8, mew=1.0)
            _top.plot(_pts[_k][_left], np.full(_left.sum(), -_k), "|", color=lk.RED, ms=8, mew=1.4)
            _top.text(1.03, -_k, f"${_left.sum()}$", color=lk.RED, fontsize=11, ha="left", va="center", transform=_top.get_yaxis_transform())
            if _ok:
                _top.plot(_pts[_k, r - 1], -_k, "o", mfc="none", mec=lk.BLUE, ms=9, mew=1.4, clip_on=False)
        _top.text(1.03, 1, "$X$", color=lk.RED, fontsize=13, ha="left", va="bottom", transform=_top.transAxes)
        _top.axvline(y0, color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
        _top.annotate("$y$", (y0, 1), xycoords=("data", "axes fraction"), textcoords="offset points", xytext=(0, 3), ha="center", va="bottom", fontsize=13, color=lk.GREY, annotation_clip=False)
        _top.set_xlim(0, 1)
        _top.set_ylim(-_rows + 0.4, 0.6)
        _top.set_yticks(-np.arange(_rows), np.arange(1, _rows + 1), fontsize=10)
        _top.set_ylabel("run")
        if _ok:
            _c = n * math.comb(n - 1, r - 1)
            _y = np.linspace(0, 1, 400)
            _pdf = _c * _y ** (r - 1) * (1 - _y) ** (n - r)
            _counts, _edges = np.histogram(_pts[:, r - 1], bins=np.linspace(0, 1, 51), density=True)
            _m = _y <= y0
            _bot.fill_between(_y[_m], _pdf[_m], color=lk.LIGHT, lw=0)
            _bot.plot([y0, y0], [0, _c * y0 ** (r - 1) * (1 - y0) ** (n - r)], color=lk.GREY, lw=1.0)
            _bot.stairs(_counts, _edges, color=lk.GREY, lw=0.9)
            _bot.plot(_y, _pdf, color=lk.BLUE, lw=1.4)
            _bot.set_ylim(0, 1.35 * max(_pdf.max(), _counts.max()))
            _bot.text(0.015, 0.97, rf"$\mathrm{{Beta}}({r}, {n - r + 1})$", color=lk.BLUE, fontsize=12, ha="left", va="top", transform=_bot.transAxes)
            _bot.text(0.985, 0.97, rf"$Y$ in {_runs:,} runs", color=lk.GREY, fontsize=12, ha="right", va="top", transform=_bot.transAxes)
        else:
            _bot.text(0.5, 0.5, r"need $r \leq n$", fontsize=13, ha="center", va="center", transform=_bot.transAxes)
            _bot.set_yticks([])
        _bot.set_xlim(0, 1)
        _bot.set_xlabel("$y$")
        _bot.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
        for _ax in (_top, _bot):
            _ax.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
        return _fig

    return (beta_scene,)


@app.cell(hide_code=True)
def _(b_n, b_r, b_y, beta_scene, lk):
    # module: beta
    # definition: beta distribution
    lk.definition(
        [
            lk.aside(
                r"A random variable $Y$ has a **beta distribution** with parameters $\mk{\alpha}$ and $\mk{\beta}$ if its pdf is",
                r"$\alpha = r$, counting from start<br>$\beta = n - r + 1$, counting from end",
            ),
            lk.aside(
                r"""
                $$
                \mk{f_Y(y)} = \frac{(\alpha + \beta - 1)!}{(\alpha - 1)! \, (\beta - 1)!} \, y^{\alpha - 1} (1 - y)^{\beta - 1}, \quad y \in (0, 1), \quad \alpha, \beta > 0
                $$
                """,
                r"$= \mathrm{Beta}(\alpha, \beta)(y)$<br>$(k - 1)! = \Gamma(k)$ for non-integer $k$ (L11)",
            ),
            lk.interactive(beta_scene(b_n.value, b_r.value, b_y.value), controls=[b_n, b_r, b_y]),
        ],
        label="def-beta",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # example: the bakery, first cake within 2 hours
    lk.example(
        [
            lk.aside(
                r"Bakery sells 10 cakes in <span class='lk-mark'>12 hours</span>",
                "one shift",
            ),
            r"""
            > $P(\text{sells 1st cake within 2 hours from opening}) = \ ?$
            """,
            lk.gap(),
            lk.aside(
                r"$Y$ = <span class='lk-mark'>time</span> until sale of 1st cake $\sim \mathrm{Beta}(1, 10)$",
                r"measured in shifts",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $f_Y(y) = {\large\tfrac{10!}{0! \, 9!}} \, y^0 (1 - y)^9 = 10 (1 - y)^9$
            """,
            lk.aside(
                r"> $\displaystyle\begin{alignedat}{2} \Longrightarrow\kern0.85em & P(Y \leq \mk{1/6}) && {}= \int_0^{1/6} 10 (1 - y)^9 \, dy = -(1 - y)^{10} \, \Big|_0^{1/6}\\[4pt] & && {}= 1 - (1 - 1/6)^{10} \approx 0.84\\[8pt] & P(Y \leq 1/12) && {}\approx 0.58\\[4pt] & P(Y \leq 1/24) && {}\approx 0.35 \end{alignedat}$",
                r"1 shift = 12 hours<br>1/6 shifts = 2 hours",
                rows=4,
                at=1,
            ),
        ],
        label="ex-bakery",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # remark: r-th of n points in (a, b)
    lk.remark(
        r"""
        If $\tilde{Y}$ is the location of the $r$th point out of $n$ in $(a, b)$

        > $\Longrightarrow$ &nbsp; $f_{\tilde{Y}}(\tilde{y}) = {\large\tfrac{1}{b - a}} \, \mathrm{Beta}(r, n - r + 1) \left( {\large\tfrac{\tilde{y} - a}{b - a}} \right)$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # theorem: mean, variance and skewness of the beta distribution
    lk.theorem(
        [
            lk.aside(
                r"Given $Y \sim \mathrm{Beta}(\alpha, \beta)$",
                r"$\alpha = r$, $\beta = n - r + 1$",
            ),
            r"""
            $$
            \begin{aligned}
            E[Y] &= \frac{\alpha}{\alpha + \beta} = \frac{r}{n + 1}\\[12pt]
            \mathrm{Var}(Y) &= \frac{\alpha \beta}{(\alpha + \beta)^2 (\alpha + \beta + 1)} = \frac{r (n - r + 1)}{(n + 1)^2 (n + 2)}\\[12pt]
            \mathrm{Skew}(Y) &= \frac{2 (\beta - \alpha) \sqrt{\alpha + \beta + 1}}{(\alpha + \beta + 2) \sqrt{\alpha \beta}} = \frac{2 (n + 1 - 2r) \sqrt{n + 2}}{(n + 3) \sqrt{r (n - r + 1)}}
            \end{aligned}
            $$
            """,
        ],
        label="thm-beta-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: beta
    # remark: the uniform distribution is a beta distribution
    lk.remark(
        r"$\mathrm{Unif}(a, b)(y) = {\large\tfrac{1}{b - a}} \, \mathrm{Beta}(1, 1) \left( {\large\tfrac{y - a}{b - a}} \right)$"
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gaussian
    # section
    lk.section("The Gaussian distribution")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gaussian
    # definition: Gaussian model
    lk.definition(
        r"""
        A **Gaussian model** is a random experiment that

        1. consists of a large number $n \to \infty$ of occurrences along a large interval of radius $\ell \to \infty$,<br>with fixed center $\mu$ and a fixed ratio $\ell^2 / n = \sigma^2$
        2. the location of each occurrence being independent and following a uniform distribution on $(\mu - \ell, \mu + \ell)$
        3. measures the location $X$ of the middle occurrence $m = {\large\tfrac{n + 1}{2}}$ (we can assume $n$ is odd)<br>in the limit $n \to \infty$ (with $\ell^2 / n = \sigma^2$)
        """,
        label="def-gaussian-model",
    )
    return


@app.cell(hide_code=True)
def _(Figure, g_m, lk, math, np):
    # module: gaussian
    # prose: the pdf of the middle occurrence in the limit
    # figure: the scaled Beta(m, m) pdf (dashed) against N(0, 1), with mu = 0, sigma^2 = 1, l = sqrt(n); m chosen with
    # the slider
    _m = g_m.value
    _n = 2 * _m - 1
    _l = math.sqrt(_n)
    _x = np.linspace(-4, 4, 801)
    _u = 0.5 + _x / (2 * _l)
    _inside = (_u > 0) & (_u < 1)
    _logc = math.lgamma(2 * _m) - 2 * math.lgamma(_m)
    _beta = np.zeros_like(_x)
    _beta[_inside] = np.exp(_logc + (_m - 1) * np.log(_u[_inside]) + (_m - 1) * np.log(1 - _u[_inside])) / (2 * _l)
    _fig = Figure(figsize=(5.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_x, np.exp(-(_x**2) / 2) / math.sqrt(2 * math.pi), color=lk.RED, lw=1.4)
    _ax.plot(_x, _beta, color=lk.BLUE, lw=1.4, ls=(0, (5, 3)))
    _ax.text(-3.6, 0.74, r"$\dfrac{1}{2\ell} \, \mathrm{Beta}(m, m)\left( \dfrac{1}{2} + \dfrac{x}{2\ell} \right)$", color=lk.BLUE, fontsize=13, ha="left", va="top")
    _ax.text(3.9, 0.72, r"$\mathcal{N}(0, 1)(x)$", color=lk.RED, fontsize=13, ha="right", va="top")
    _ax.set_xlim(-4, 4)
    _ax.set_ylim(0, 0.76)
    _ax.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _ax.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _ax.set_xlabel("$x$")
    lk.prose(
        r"""
        Assuming $n = 2m - 1$, $X$ = location of the $m$th occurrence

        > $\Longrightarrow$ &nbsp; $U = {\large\tfrac{X - (\mu - \ell)}{2\ell}} \sim \mathrm{Beta}(m, m)$

        $$
        \begin{aligned}
        \Longrightarrow \quad f_X(x) &= \lim_{\substack{m \to \infty\\ \ell^2 / n = \sigma^2}} \frac{1}{2\ell} \, \mathrm{Beta}(m, m) \left( \frac{1}{2} + \frac{x - \mu}{2\ell} \right)\\[4pt]
        &= \lim_{\substack{m \to \infty\\ \ell^2 / n = \sigma^2}} \frac{1}{2\ell} \, \frac{(2m - 1)!}{(m - 1)! \, (m - 1)!} \left( \frac{1}{2} + \frac{x - \mu}{2\ell} \right)^{m - 1} \left( \frac{1}{2} - \frac{x - \mu}{2\ell} \right)^{m - 1}\\[4pt]
        &= \lim_{\substack{m \to \infty\\ \ell^2 / n = \sigma^2}} \underbrace{\frac{1}{2\ell} \, m \binom{2m - 1}{m - 1} \frac{1}{4^{m - 1}}}_{\textstyle \longrightarrow {\large\tfrac{1}{\sqrt{2\pi\sigma^2}}}} \, \underbrace{\left( 1 - \frac{(x - \mu)^2}{\ell^2} \right)^{m - 1}}_{\textstyle \longrightarrow \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)}\\[4pt]
        &= \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
        \end{aligned}
        $$
        """,
        lk.interactive(_fig, controls=[g_m]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gaussian
    # definition: Gaussian distribution
    lk.definition(
        [
            r"A random variable $X$ has **Gaussian** (Normal) **distribution** with mean $\mu$ and variance $\sigma^2$ if its pdf is",
            lk.aside(
                r"""
                $$
                \mk{f_X(x)} = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right), \quad x \in (-\infty, +\infty)
                $$
                """,
                r"$= \mathcal{N}(\mu, \sigma^2)(x)$",
            ),
        ],
        label="def-gaussian",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gaussian
    # theorem: mean, variance and skewness of the Gaussian distribution
    lk.theorem(
        r"""
        $X \sim \mathcal{N}(\mu, \sigma^2)$

        $$
        E[X] = \mu, \qquad \mathrm{Var}(X) = \sigma^2, \qquad \mathrm{Skew}(X) = 0
        $$
        """,
        label="thm-gaussian-moments",
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
    # exercise: c x e^(-2x)
    lk.exercise(
        r"""
        Let $X$ have pdf $f_X(x) = \begin{cases} c \, x \, e^{-2x}, & x \in (0, +\infty)\\ 0, & x \notin (0, +\infty) \end{cases}$

        Find $c$, $E[X]$ and $\mathrm{Var}(X)$
        """,
        label="ex-gamma-pdf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: c y (1 - y)^2
    lk.exercise(
        r"""
        Let $Y$ have pdf $f_Y(y) = \begin{cases} c \, y (1 - y)^2, & y \in (0, 1)\\ 0, & y \notin (0, 1) \end{cases}$

        Find $c$, $E[Y]$ and $\mathrm{Var}(Y)$
        """,
        label="ex-beta-pdf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: practice
    # exercise: mgf of the standard normal
    lk.exercise(
        r"""
        Let $Z \sim \mathcal{N}(0, 1)$, &nbsp; $f_Z(z) = {\large\tfrac{1}{\sqrt{2\pi}}} \, e^{-z^2 / 2}$, $z \in \mathbb{R}$

        Show that $m_Z(t) = e^{t^2 / 2}$, use $K_Z(t) = \ln(m_Z(t))$ to compute $E[Z]$, $\mathrm{Var}(Z)$, $\mathrm{Skew}(Z)$

        **Hint:** $tz - z^2 / 2 = t^2 / 2 - (z - t)^2 / 2$
        """,
        label="ex-normal-mgf",
    )
    return


if __name__ == "__main__":
    app.run()

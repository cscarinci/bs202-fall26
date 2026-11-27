import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 11 · Expectations and moment generating functions", css_file="lecturekit/style.css")


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
    lk.lecture(11, "Expectations and moment generating functions")
    return


@app.cell(hide_code=True)
def _(lk, mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    gp_r = lk.slider(1, 10, step=1, value=2, label="$r$")
    mg_dist = mo.ui.dropdown(["Binom(n, p)", "Pois(λ)", "Gamma(r, λ)"], value="Binom(n, p)", label="distribution", allow_select_none=False)
    mg_bn = lk.slider(1, 10, step=1, value=10, label="$n$")
    mg_bp = lk.slider(0.05, 0.95, step=0.05, value=0.3, label="$p$")
    mg_pl = lk.slider(0.1, 10, step=0.1, value=0.3, label=r"$\lambda$")
    mg_gr = lk.slider(1, 10, step=1, value=10, label="$r$")
    mg_gl = lk.slider(1, 5, step=0.1, value=2, label=r"$\lambda$")
    return gp_r, mg_bn, mg_bp, mg_dist, mg_gl, mg_gr, mg_pl


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"$X : S \longrightarrow \mathbb{R}$, $S_X = \mathrm{Im}(X)$ uncountable",
        lk.aside(
            r"> $\leadsto$ &nbsp; $\mk{F_X(x)} = P(X \leq x)$ continuous",
            r"$F_X(x)$ = cdf",
        ),
        lk.aside(
            r"> $\leadsto$ &nbsp; $\mk{f_X(x)} = \dfrac{d}{dx} F_X(x)$",
            r"$f_X(x)$ = pdf, where the derivative is<br>well-defined (usually, piecewise continuous)",
        ),
        topic="Continuous random variables",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Expectations for continuous random variables

        Moment generating functions
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 3.9, 4.3, 4.9")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # remark: the pdf is not a probability
    lk.remark(r"For continuous random variables $f_X(x) \neq \underbrace{P(X = x)}_{= \, 0 \ \forall \, x}$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # section
    lk.section("Expectations for continuous random variables")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # definition: expectation value of u(X)
    lk.definition(
        [
            r"Given $X : S \longrightarrow \mathbb{R}$ continuous random variable and $u : \mathbb{R} \longrightarrow \mathbb{R}$",
            lk.aside(
                r"""
                $$
                \mk{E[u(X)]} = \int_{-\infty}^{+\infty} u(x) \, f_X(x) \, dx = \underbrace{\int_{S_X}}_{f_X(x) = 0 \ \forall \, x \notin S_X} u(x) \, f_X(x) \, dx.
                $$
                """,
                r"$E[u(X)]$ = expectation value of $u(X)$",
            ),
        ],
        label="def-expectation",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # recall: discrete case
    lk.recall(r"For discrete random variables $E[u(X)] = \displaystyle\sum_{x \in S_X} u(x) \, f_X(x)$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # theorem: linearity of expectation
    lk.theorem(
        r"""
        Given $u : \mathbb{R} \longrightarrow \mathbb{R}$, $v : \mathbb{R} \longrightarrow \mathbb{R}$, $a, b, c \in \mathbb{R}$

        $$
        \begin{aligned}
        E[a \, u(X) + b \, v(X)] &= a \, E[u(X)] + b \, E[v(X)]\\[4pt]
        E[c] &= c.
        \end{aligned}
        $$
        """,
        label="thm-linearity",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # definition: mean, variance, skewness, moments
    lk.definition(
        r"""
        For $X : S \longrightarrow \mathbb{R}$ continuous random variable

        $$
        \begin{aligned}
        E[X] &= \mu_X = \int_{-\infty}^{\infty} x \, f_X(x) \, dx && \text{is the \textbf{mean} of } X\\[6pt]
        E[(X - \mu_X)^2] &= \mathrm{Var}(X) = \sigma_X^2 && \text{is the \textbf{variance} of } X\\[2pt]
        &= \int_{-\infty}^{\infty} (x - \mu_X)^2 \, f_X(x) \, dx\\[6pt]
        E\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^3 \right] &= \mathrm{Skew}(X) = \gamma_X && \text{is the \textbf{skewness} of } X\\[2pt]
        &= \int_{-\infty}^{\infty} \left( \frac{x - \mu_X}{\sigma_X} \right)^3 f_X(x) \, dx.
        \end{aligned}
        $$

        More generally,

        $$
        \begin{aligned}
        E[X^k] &= \hat{\mu}_{X,k} && \text{is the } k\text{th \textbf{moment} of } X\\[4pt]
        E[(X - \mu_X)^k] &= \mu_{X,k} && \text{is the } k\text{th \textbf{central moment} of } X
        \end{aligned}
        $$
        """,
        label="def-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # remark: discrete case
    lk.remark("Moments and central moments are defined similarly for discrete random variables.")
    return


@app.cell(hide_code=True)
def _(Figure, gp_r, lk, math, np):
    # module: expectations
    # theorem: mean, variance and skewness of Gamma(r, lambda)
    # figure: the pdf of Gamma(r, 1), its mean and the band mu +- sigma; r chosen with the slider
    _r, _lam = gp_r.value, 1
    _mu, _sd = _r / _lam, math.sqrt(_r) / _lam
    _lo, _hi = max(0.0, _mu - _sd), _mu + _sd
    _end = 2 * math.ceil((_mu + 3.5 * _sd) / 2)  # the frame follows r

    def _f(x):
        return _lam**_r * x ** (_r - 1) / math.factorial(_r - 1) * np.exp(-_lam * x)

    _x = np.linspace(0, _end, 500)
    _top = float(_f(_x).max())
    _in = np.linspace(_lo, _hi, 200)
    _fig = Figure(figsize=(5.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill_between(_in, 0, _f(_in), color=lk.LIGHT, lw=0)
    for _b in (_lo, _hi):
        _ax.plot([_b, _b], [0, 1.12 * _top], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([_mu, _mu], [0, 1.12 * _top], color=lk.GREEN, lw=1.4, ls=(0, (4, 3)))
    _ax.plot(_x, _f(_x), color=lk.BLUE, lw=1.4)
    _ax.annotate(r"$\mu_X$", (_mu, 1.2 * _top), color=lk.GREEN, fontsize=12, ha="center", va="center")
    _ax.annotate(r"$\mu_X \pm \sigma_X$", (_hi, 1.05 * _top), textcoords="offset points", xytext=(4, 0), color=lk.GREY, fontsize=12, ha="left", va="center")
    _ax.text(0.98, 0.96, r"$\mathrm{Gamma}(r, 1)$", color=lk.BLUE, fontsize=12, ha="right", va="top", transform=_ax.transAxes)
    _ax.set_xlim(0, _end)
    _ax.set_ylim(0, 1.3 * _top)
    _ax.set_xlabel("$x$")
    _ax.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _ax.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    lk.theorem(
        [
            lk.aside(
                r"Let $X \mathrel{\mk{\sim}} \mathrm{Gamma}(r, \lambda)$, then",
                r"$\sim$ = be a random variable with pdf",
            ),
            r"""
            $$
            E[X] = r / \lambda, \qquad \mathrm{Var}(X) = r / \lambda^2, \qquad \mathrm{Skew}(X) = 2 / \sqrt{r}.
            $$
            """,
            lk.interactive(_fig, controls=[gp_r]),
        ],
        label="thm-gamma-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: expectations
    # proof: mean and variance of Gamma(r, lambda)
    lk.proof(
        [
            lk.aside(
                r"$\displaystyle\begin{aligned} \text{1.} \quad \int_{-\infty}^{\infty} f_X(x) \, dx &= \int_0^{\infty} \frac{\lambda^r x^{r - 1}}{(r - 1)!} \, e^{-\lambda x} \, dx \overset{?}{=} 1\\[4pt] &= \frac{1}{(r - 1)!} \underbrace{\int_0^{\infty} (\lambda x)^{r - 1} e^{-\lambda x} \, d(\lambda x)}_{\begin{array}{l} \scriptstyle -e^{-\lambda x} (\lambda x)^{r - 1} \big|_0^{\infty} + \int_0^{\infty} (r - 1) (\lambda x)^{r - 2} e^{-\lambda x} \, d(\lambda x)\\[2pt] \scriptstyle = (r - 1) \int_0^{\infty} (\lambda x)^{r - 2} e^{-\lambda x} \, d(\lambda x) \end{array}}\\[34pt] &= \frac{1}{(r - 2)!} \int_0^{\infty} \lambda^{r - 1} x^{r - 2} e^{-\lambda x} \, dx\\[4pt] &= \frac{1}{(r - 3)!} \int_0^{\infty} \lambda^{r - 2} x^{r - 3} e^{-\lambda x} \, dx\\[-2pt] &\ \ \vdots\\[-2pt] &= \frac{1}{0!} \int_0^{\infty} \lambda^1 x^0 e^{-\lambda x} \, dx = -e^{-\lambda x} \Big|_0^{\infty} = 0 - (-1) = 1 \end{aligned}$",
                r"$u = (\lambda x)^{r - 1}$, $dv = e^{-\lambda x} \, d(\lambda x)$",
                rows=7,
                at=2,
            ),
            lk.aside(
                r"> $\leadsto$ &nbsp; $\displaystyle\boxed{\mk{\int_0^{\infty} x^{r - 1} e^{-x} \, dx} = (r - 1)!}$",
                r"$\Gamma(r)$ can be defined for any $r > 0$<br>$\leadsto$ factorials for positive numbers!",
            ),
            r"$\displaystyle\begin{aligned} \text{2.} \quad E[X] &= \int_0^{\infty} x \, \frac{\lambda^r x^{r - 1}}{(r - 1)!} \, e^{-\lambda x} \, dx = \frac{1}{(r - 1)!} \, \frac{1}{\lambda} \int_0^{\infty} (\lambda x)^r e^{-\lambda x} \, d(\lambda x)\\[4pt] &= \frac{1}{(r - 1)!} \, \frac{1}{\lambda} \, \Gamma(r + 1) = \frac{r!}{(r - 1)!} \, \frac{1}{\lambda} = r / \lambda \end{aligned}$",
            lk.gap(),
            r"$\displaystyle \text{3.} \quad \mathrm{Var}(X) = \underbrace{E[X^2]}_{\frac{1}{(r - 1)!} \frac{1}{\lambda^2} \Gamma(r + 2)} - E[X]^2 = \frac{r (r + 1)}{\lambda^2} - \frac{r^2}{\lambda^2} = \frac{r}{\lambda^2}$",
        ],
        title="for mean and variance",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # module: expectations
    # illustration: Gamma(r) for r > 0 through the factorials (n - 1)! at the whole numbers
    _fig = Figure(figsize=(5.6, 2.5), layout="constrained")
    _ax = _fig.subplots()
    _r = np.linspace(0.04, 5.05, 500)
    _ax.plot(_r, [math.gamma(_v) for _v in _r], color=lk.BLUE, lw=1.4)
    _ax.plot(range(1, 6), [math.factorial(_n - 1) for _n in range(1, 6)], "o", color="black", ms=4, zorder=4)
    _ax.text(2.4, 15.5, r"$\Gamma(r) = \int_0^\infty x^{r-1} e^{-x}\, dx$", color=lk.BLUE, fontsize=13, ha="center", va="center")
    _ax.text(3.88, 7.6, r"$\Gamma(n) = (n - 1)!$", fontsize=12, ha="right", va="center")
    _ax.set_xlim(0, 5.3)
    _ax.set_ylim(0, 26)
    _ax.set_xticks(range(0, 6))
    _ax.set_yticks([0, 6, 12, 18, 24])
    _ax.set_xlabel("$r$")
    _ax.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _ax.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    lk.prose(lk.figure(_fig))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mgf
    # section
    lk.section("Moment generating functions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mgf
    # definition: moment generating function
    lk.definition(
        [
            r"For a random variable $X$ (continuous or discrete) the **moment generating function** is the function of a real variable $t$, defined via",
            lk.aside(
                r"""
                $$
                m_X(t) = \mk{E[e^{tX}]}.
                $$
                """,
                "expectation of exponential of $t$ times $X$",
            ),
        ],
        label="def-mgf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mgf
    # example: mgf of the binomial, Poisson and Gamma distributions
    lk.example(
        [
            r"""
            $X \sim \mathrm{Binom}(n, p)$

            $$
            \begin{aligned}
            m_X(t) &= \sum_{x=0}^{n} e^{tx} \binom{n}{x} p^x q^{n - x}\\[4pt]
            &= \sum_{x=0}^{n} \binom{n}{x} (pe^t)^x q^{n - x} = (q + pe^t)^n
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $X \sim \mathrm{Pois}(\lambda)$

            $$
            \begin{aligned}
            m_X(t) &= \sum_{x=0}^{\infty} e^{tx} e^{-\lambda} \frac{\lambda^x}{x!}\\[4pt]
            &= \sum_{x=0}^{\infty} e^{-\lambda} \frac{(\lambda e^t)^x}{x!} = e^{-\lambda} e^{\lambda e^t} = e^{\lambda (e^t - 1)}
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $X \sim \mathrm{Gamma}(r, \lambda)$

            $$
            \begin{aligned}
            m_X(t) &= \int_0^{\infty} e^{tx} \frac{\lambda^r x^{r - 1}}{(r - 1)!} e^{-\lambda x} \, dx\\[4pt]
            &= \int_0^{\infty} \frac{\lambda^r x^{r - 1}}{(r - 1)!} e^{-(\lambda - t) x} \, dx = \frac{\lambda^r}{(\lambda - t)^r}, \quad \text{for } t < \lambda
            \end{aligned}
            $$
            """,
        ],
        label="ex-mgfs",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mgf
    # theorem: moments from the mgf, cumulants from K_X = ln m_X
    lk.theorem(
        r"""
        Given a random variable $X$ with mgf $m_X(t)$, then

        $$
        E[X^k] = \hat{\mu}_{X,k} = \frac{d^k}{dt^k} \Big|_{t=0} m_X(t).
        $$

        Also, writing $K_X(t) = \ln(m_X(t))$, we have

        > $K_X(0) = 0$, &nbsp; $K_X'(0) = E[X]$, &nbsp; $K_X''(0) = \mathrm{Var}(X)$

        > and $K_X'''(0) = E[(X - \mu_X)^3]$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{Skew}(X) = \dfrac{K_X'''(0)}{(K_X''(0))^{3/2}}$
        """,
        label="thm-mgf-moments",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mgf
    # proof: moments from the mgf
    lk.proof(
        r"""
        $m_X(t) = E[e^{tX}]$

        $$
        \begin{aligned}
        &\begin{aligned}
        \frac{d}{dt} m_X(t) &= \frac{d}{dt} E[e^{tX}] = E\left[ \frac{d}{dt} e^{tX} \right] = E[e^{tX} X]\\[4pt]
        \frac{d^2}{dt^2} m_X(t) &= E[e^{tX} X^2] \quad \cdots \quad \frac{d^k}{dt^k} m_X(t) = E[e^{tX} X^k]
        \end{aligned}\\[6pt]
        &\Longrightarrow\quad m_X^{(k)}(0) = E[X^k].
        \end{aligned}
        $$

        Similarly,

        $$
        \begin{aligned}
        \frac{d}{dt} K_X(t) &= \frac{1}{m_X(t)} \, m_X'(t) && \Longrightarrow \quad K_X'(0) = \frac{E[X]}{E[1]}\\[6pt]
        \frac{d^2}{dt^2} K_X(t) &= \frac{1}{(m_X(t))^2} \left[ m_X(t) \, m_X''(t) - (m_X'(t))^2 \right] && \Longrightarrow \quad K_X''(0) = E[X^2] - (E[X])^2\\[6pt]
        \frac{d^3}{dt^3} K_X(t) &= \cdots
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mgf
    # remark: the 4th cumulant
    lk.remark(
        lk.aside(
            r"$\mk{K_X^{(4)}(0)} = E[(X - \mu_X)^4] - 3 E[(X - \mu_X)^2]^2$ (4th cumulant)",
            "not the 4th central moment",
        )
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, mg_bn, mg_bp, mg_dist, mg_gl, mg_gr, mg_pl, np):
    # module: mgf
    # example: mean, variance and skewness from K_X for the binomial, Poisson and Gamma distributions figure: m_X(t)
    # and K_X(t) with the tangent t K_X'(0) at 0, for the distribution chosen in the menu
    _d = mg_dist.value
    _tmax = 1.0
    if _d.startswith("Binom"):
        _sliders = [mg_bn, mg_bp]
        _a, _b = mg_bn.value, mg_bp.value

        def _K(t):
            return _a * np.log1p(_b * np.expm1(t))

        _mu = _a * _b
    elif _d.startswith("Pois"):
        _sliders = [mg_pl]
        _b = mg_pl.value

        def _K(t):
            return _b * np.expm1(t)

        _mu = _b
    else:
        _sliders = [mg_gr, mg_gl]
        _a, _b = mg_gr.value, mg_gl.value

        def _K(t):
            return -_a * np.log1p(-t / _b)

        _mu = _a / _b
        _tmax = min(1.0, 0.8 * _b)  # m_X(t) exists for t < lambda only
    _fig = Figure(figsize=(lk.FULL, 2.8), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax, _name in ((_left, "$m_X(t)$"), (_right, r"$K_X(t) = \ln m_X(t)$")):
        _ax.axvline(0, color="black", lw=0.8)
        for _sp in ("top", "right"):
            _ax.spines[_sp].set_visible(False)
        _ax.set_xlim(-1, _tmax)
        _ax.set_xlabel("$t$")
        _ax.set_ylabel(_name)
        _ax.xaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
        _ax.yaxis.set_major_formatter(lambda _v, _p: f"${_v:g}$")
    _t = np.linspace(-1, _tmax, 300)
    _left.plot(_t, np.exp(_K(_t)), color=lk.BLUE, lw=1.4)
    _left.plot(0, 1, "o", color="black", ms=4, zorder=4)
    _left.set_ylim(0, min(1.05 * float(np.exp(_K(_t)).max()), 5))
    _right.plot(_t, _mu * _t, color=lk.GREEN, lw=1.4)
    _right.plot(_t, _K(_t), color=lk.BLUE, lw=1.4)
    _right.plot(0, 0, "o", color="black", ms=4, zorder=4)
    _right.annotate(r"$t\, K_X'(0)$", (-0.5, -0.5 * _mu), textcoords="offset points", xytext=(4, -6), color=lk.GREEN, fontsize=14, ha="left", va="top")
    lk.example(
        [
            r"""
            $X \sim \mathrm{Binom}(n, p)$ &nbsp; $\leadsto$ &nbsp; $m_X(t) = (q + pe^t)^n$, &nbsp; $K_X(t) = \ln(m_X(t)) = n \ln(q + pe^t)$

            $$
            \begin{aligned}
            K_X'(t) &= \frac{n}{q + pe^t} \, pe^t\\[2pt]
            &\qquad \leadsto \quad \mu_X = K_X'(0) = \frac{n}{q + p} \, p = np\\[8pt]
            K_X''(t) &= \frac{n}{(q + pe^t)^2} \left( pe^t (q + pe^t) - (pe^t)^2 \right) = \frac{npqe^t}{(q + pe^t)^2}\\[2pt]
            &\qquad \leadsto \quad \sigma_X^2 = K_X''(0) = npq\\[8pt]
            K_X'''(t) &= \frac{n}{(q + pe^t)^3} \left( pqe^t (q + pe^t) - 2pqe^t \cdot pe^t \right) = \frac{n}{(q + pe^t)^3} \left( pqe^t (q - pe^t) \right)\\[2pt]
            &\qquad \leadsto \quad \gamma_X = \frac{K'''(0)}{\sigma_X^3} = \frac{npq (q - p)}{(npq)^{3/2}} = \frac{q - p}{\sqrt{npq}}.
            \end{aligned}
            $$
            """,
            lk.gap(),
            r"""
            $X \sim \mathrm{Pois}(\lambda)$ &nbsp; $\leadsto$ &nbsp; $m_X(t) = e^{\lambda (e^t - 1)}$, &nbsp; $K_X(t) = \lambda (e^t - 1)$

            $$
            \begin{array}{lll}
            K_X'(t) = \lambda e^t \qquad\qquad & K_X''(t) = \lambda e^t \qquad\qquad & K_X'''(t) = \lambda e^t\\[6pt]
            \mu_X = \lambda & \sigma_X^2 = \lambda & \gamma_X = \dfrac{\lambda}{\lambda^{3/2}} = 1 / \sqrt{\lambda}.
            \end{array}
            $$
            """,
            lk.gap(),
            r"""
            $X \sim \mathrm{Gamma}(r, \lambda)$ &nbsp; $\leadsto$ &nbsp; $m_X(t) = \left( \dfrac{\lambda}{\lambda - t} \right)^r$, &nbsp; $K_X(t) = r (\ln \lambda - \ln(\lambda - t))$

            $$
            \begin{array}{lll}
            K_X'(t) = \dfrac{r}{\lambda - t} \qquad\qquad & K_X''(t) = \dfrac{r}{(\lambda - t)^2} \qquad\qquad & K_X'''(t) = \dfrac{2r}{(\lambda - t)^3}\\[14pt]
            \mu_X = r / \lambda & \sigma_X^2 = r / \lambda^2 & \gamma_X = \dfrac{2r / \lambda^3}{(r / \lambda^2)^{3/2}} = 2 / \sqrt{r}.
            \end{array}
            $$
            """,
            lk.interactive(_fig, controls=[mg_dist, *_sliders]),
        ],
        label="ex-cumulants",
    )
    return


if __name__ == "__main__":
    app.run()

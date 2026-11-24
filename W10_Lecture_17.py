import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 17 · The central limit theorem", css_file="lecturekit/style.css")


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
    lk.lecture(17, "The central limit theorem")
    return


@app.cell(hide_code=True)
def _(lk, mo):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    v_n = lk.slider(1, 10, step=1, value=4, label="$n$")
    c_pop = mo.ui.dropdown(["fair die", "waiting time ~ Exp(λ)"], value="fair die", label="population", allow_select_none=False)
    c_n = lk.slider(1, 100, step=1, value=10, label="$n$")
    c_z = lk.slider(-3, 3, step=0.1, value=1, label="$z$")
    b_n = lk.slider(1, 100, step=1, value=10, label="$n$")
    return b_n, c_n, c_pop, c_z, v_n


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Given a random variable $X : S \longrightarrow \mathbb{R}$, a random sample of size $n$ from the population $X$ is
        """,
        lk.aside(
            r"> $X_1, \dots, X_n : \underbrace{S \times \dots \times S}_{\footnotesize \begin{array}{c} \text{with independent} \\ \text{probability measures} \end{array}} \longrightarrow \mathbb{R}$, &nbsp; $X_i(o_1, \dots, o_n) = X(o_i)$",
            "probability of products is<br>the product of probabilities",
        ),
        r"""
        > > $\Longrightarrow$ &nbsp; $X_1, \dots, X_n \sim f_X$ iid

        A statistic is a random variable $T = u(X_1, \dots, X_n) : S \times \dots \times S \longrightarrow \mathbb{R}$,<br>and the sampling distribution of $T$ is $f_T : \mathbb{R} \longrightarrow \mathbb{R}$

        $$
        \begin{aligned}
        M_n &= \frac{1}{n} \sum_{i=1}^n X_i && \text{sample mean}\\[6pt]
        S_n^2 &= \frac{1}{n - 1} \sum_{i=1}^n (X_i - M_n)^2 && \text{sample variance}\\[6pt]
        G_n &= \frac{1}{n} \sum_{i=1}^n \left( \frac{X_i - M_n}{S_n} \right)^3 && \text{sample skewness}
        \end{aligned}
        $$

        If $E[X] = \mu$ and $\mathrm{Var}(X) = \sigma^2$ &nbsp; $\Longrightarrow$ &nbsp; $E[M_n] = \mu$ and $\mathrm{Var}(M_n) = \sigma^2 / n$

        """,
        lk.aside(
            r"> $P(|M_n - \mu| \ge \varepsilon) \le {\large\tfrac{1}{n}} {\large\tfrac{\sigma^2}{\varepsilon^2}} \longrightarrow 0$ &nbsp; as $n \to +\infty$, &nbsp; $\forall \varepsilon > 0$",
            "law of large numbers",
        ),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"Sampling distribution of $M_n$ and the CLT", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 7.2–7.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: normal population
    # section
    lk.section("Sampling distribution of $M_n$ and the CLT")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np, v_n):
    # module: normal population
    # example: normal population
    # x in units of sigma from mu: f_X is the N(0, 1) curve, f_{M_n} the N(0, 1/n) curve (the same scale for both)
    _n = v_n.value
    _u = np.linspace(-3.6, 3.6, 721)

    def _phi(v, s):
        return np.exp(-(np.asarray(v, dtype=float) ** 2) / (2 * s**2)) / (s * math.sqrt(2 * math.pi))

    _s = 1 / math.sqrt(_n)
    _fig = Figure(figsize=(4.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_u, _phi(_u, 1), color=lk.BLUE, lw=1.4, zorder=3)
    _ax.plot(_u, _phi(_u, _s), color=lk.GREEN, lw=1.4, zorder=4)
    _ax.annotate(r"$f_X$", (-1.6, float(_phi(-1.6, 1))), textcoords="offset points", xytext=(-4, 4), color=lk.BLUE, fontsize=12, ha="right", va="bottom")
    # the name of f_{M_n} sits at its half height, on the right flank, and moves with the curve
    _h = math.sqrt(2 * math.log(2)) * _s
    _ax.annotate(r"$f_{M_n}$", (_h, float(_phi(_h, _s))), textcoords="offset points", xytext=(7, 3), color=lk.GREEN, fontsize=12, ha="left", va="bottom")
    _ax.set_xlim(-3.6, 3.6)
    _ax.set_ylim(0, 1.36)
    _ax.set_xticks([-2, -1, 0, 1, 2], [r"$\mu - 2\sigma$", r"$\mu - \sigma$", r"$\mu$", r"$\mu + \sigma$", r"$\mu + 2\sigma$"])
    _ax.set_yticks([])
    _ax.tick_params(labelsize=11)
    for _sp in ("top", "right", "left"):
        _ax.spines[_sp].set_visible(False)
    lk.example(
        [
            r"""
            $X \sim \mathcal{N}(\mu, \sigma^2)$ (normal population)

            > $\Longrightarrow$ &nbsp; $f_X(x) = \dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$

            > $\Longrightarrow$ &nbsp; $m_X(t) = \exp\Big( \mu t + {\large\tfrac{\sigma^2}{2}} t^2 \Big)$

            $X_1, \dots, X_n \sim \mathcal{N}(\mu, \sigma^2)$ iid

            > $\Longrightarrow$ &nbsp; $m_{X_1 + \dots + X_n}(t) = (m_X(t))^n = \exp\Big( n\mu t + n {\large\tfrac{\sigma^2}{2}} t^2 \Big)$

            > $\Longrightarrow$ &nbsp; $X_1 + \dots + X_n \sim \mathcal{N}(n\mu, n\sigma^2)$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\mk{M_n} = {\large\tfrac{1}{n}} (X_1 + \dots + X_n) \sim \mathcal{N}(\mu, \sigma^2 / n)$",
                r"$\begin{array}{c} X \sim \mathcal{N}(\mu, \sigma^2) \\[2pt] \Downarrow \\[2pt] Y = aX + b \sim \mathcal{N}(a\mu + b, a^2\sigma^2) \end{array}$",
            ),
            lk.interactive(_fig, controls=[v_n]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: normal population
    # consequence: normal population
    lk.prose(
        r"""
        $\Longrightarrow$ &nbsp; sample mean of normal population is normally distributed around the mean<br>with smaller variance for larger sizes

        > $\leadsto$ &nbsp; what about for other populations?
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: central limit theorem
    # definition: standardized mean
    lk.definition(
        r"""
        Given $X$ with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2 > 0$ and $X_1, \dots, X_n \sim f_X$ iid, the **standardized mean** is

        $$
        Z_n = \frac{M_n - \mu}{\sigma / \sqrt{n}}
        $$
        """,
        label="def-standardized",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: central limit theorem
    # theorem: mean and variance of Z_n, CLT
    lk.theorem(
        [
            r"$E[Z_n] = 0$, &nbsp; $\mathrm{Var}(Z_n) = 1$",
            lk.aside(
                r"""
                $$
                \underbrace{P(Z_n \le z)}_{\mathllap{\text{cdf of } Z_n\kern-1.2em}} \longrightarrow \underbrace{\Phi(z)}_{\mathrlap{\kern-1.2em \text{standard normal cdf}}} \qquad \text{as } n \to +\infty, \quad \forall z \in \mathbb{R}
                $$
                """,
                "central limit theorem",
            ),
        ],
        label="thm-clt",
    )
    return


@app.cell(hide_code=True)
def _(Figure, c_n, c_pop, c_z, lk, math, mo, np):
    # module: central limit theorem
    # consequence: for any population
    # the cdf of Z_n (exact) and Phi, for a fair die (pmf of X_1 + ... + X_n by convolution) or X ~ Exp(lambda)
    # (X_1 + ... + X_n ~ Gamma(n, lambda), so P(Z_n <= z) = P(Gamma(n, 1) <= n + z sqrt(n)) for every lambda)
    _n, _z0 = c_n.value, round(c_z.value, 1) + 0.0
    _zz = np.linspace(-3.2, 3.2, 641)

    def _Phi(z):
        return 0.5 * (1 + np.vectorize(math.erf)(np.asarray(z, dtype=float) / math.sqrt(2)))

    _fig = Figure(figsize=(4.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_zz, _Phi(_zz), color=lk.RED, lw=1.4, zorder=3)
    if c_pop.value == "fair die":
        _p = np.array([1.0])
        for _ in range(_n):
            _p = np.convolve(_p, np.full(6, 1 / 6))
        _k = np.arange(_n, 6 * _n + 1)
        _zk = (_k / _n - 3.5) / math.sqrt(35 / 12 / _n)
        _F = np.cumsum(_p)
        _xs = np.concatenate([[-3.2], np.repeat(np.clip(_zk, -3.2, 3.2), 2), [3.2]])
        _ys = np.concatenate([[0, 0], np.repeat(_F, 2)])
        _ax.plot(_xs, _ys, color=lk.BLUE, lw=1.4, zorder=4)
        _below = _zk <= _z0 + 1e-9
        _P = float(_F[_below][-1]) if _below.any() else 0.0
    else:

        def _cdf(z):
            x = np.maximum(_n + np.asarray(z, dtype=float) * math.sqrt(_n), 0)
            return 1 - np.exp(-x) * sum(x**j / math.factorial(j) for j in range(_n))

        _ax.plot(_zz, _cdf(_zz), color=lk.BLUE, lw=1.4, zorder=4)
        _P = float(_cdf(_z0))
    _ax.plot([_z0, _z0], [0, 1.05], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot(_z0, _P, "o", color=lk.BLUE, ms=4, zorder=5)
    _ax.plot(_z0, float(_Phi(_z0)), "o", color=lk.RED, ms=4, zorder=5)
    _ax.text(-0.45, 0.8, r"$P(Z_n \leq z)$", color=lk.BLUE, fontsize=12, ha="right", va="center")
    _ax.text(0.45, 0.2, r"$\Phi(z)$", color=lk.RED, fontsize=12, ha="left", va="center")
    _ax.text(_z0, 1.06, "$z$", color=lk.GREY, fontsize=12, ha="center", va="bottom")
    _ax.set_xlim(-3.2, 3.2)
    _ax.set_ylim(0, 1.15)
    _ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    _ax.set_yticks([0, 0.5, 1], ["$0$", "$0.5$", "$1$"])
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    lk.prose(
        r"""
        $\leadsto$ &nbsp; the distribution of the standardized mean approaches the standard normal distribution<br>for large sample sizes *for any population*!
        """,
        lk.interactive(_fig, controls=[c_pop, c_n, c_z]),
    )
    return


@app.cell(hide_code=True)
def _(Figure, b_n, lk, math, np):
    # module: central limit theorem
    # example: binomial
    # Binom(n, 1/6) and N(np, npq); the frame follows the distribution: mean +- 4.5 standard deviations
    _n, _pp = b_n.value, 1 / 6
    _mean, _sd = _n * _pp, math.sqrt(_n * _pp * (1 - _pp))
    _ks = np.arange(_n + 1)
    _pmf = np.array([math.comb(_n, int(_k)) * _pp**_k * (1 - _pp) ** (_n - _k) for _k in _ks])
    _lo, _hi = _mean - 4.5 * _sd, _mean + 4.5 * _sd
    _lo, _hi = min(_lo, _hi - 4), max(_hi, _lo + 4)
    _x = np.linspace(_lo, _hi, 600)
    _pdf = np.exp(-((_x - _mean) ** 2) / (2 * _sd**2)) / (_sd * math.sqrt(2 * math.pi))
    _top = 1.3 * max(float(_pmf.max()), float(_pdf.max()))
    _in = (_ks >= _lo) & (_ks <= _hi)
    _fig = Figure(figsize=(4.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.vlines(_ks[_in], 0, _pmf[_in], color=lk.BLUE, lw=1.2, zorder=3)
    _ax.plot(_ks[_in], _pmf[_in], "o", color=lk.BLUE, ms=3, zorder=4)
    _ax.plot(_x, _pdf, color=lk.RED, lw=1.4, zorder=5)
    _xr = _mean + 1.4 * _sd
    _ax.annotate(r"$\mathcal{N}(np, npq)$", (_xr, math.exp(-0.98) / (_sd * math.sqrt(2 * math.pi))), textcoords="offset points", xytext=(6, 4), color=lk.RED, fontsize=12, ha="left", va="bottom")
    _ax.text(_mean - 1.5 * _sd, 0.8 * float(_pmf.max()), r"$\mathrm{Binom}(n, p)$", color=lk.BLUE, fontsize=12, ha="right", va="center")
    _ax.text(0.99, 0.97, r"$p = 1/6$", transform=_ax.transAxes, fontsize=12, ha="right", va="top")
    _ax.set_xlim(_lo, _hi)
    _ax.set_ylim(0, _top)
    _ax.xaxis.get_major_locator().set_params(integer=True)
    _ax.set_yticks([])
    _ax.set_xlabel("$x$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)
    lk.example(
        [
            lk.aside(r"$X \sim \mathrm{Binom}(1, p)$", r"with $E[X] = p$, $\mathrm{Var}(X) = pq$"),
            r"""
            $X_1, \dots, X_n \sim \mathrm{Binom}(1, p)$ iid

            > $\Longrightarrow$ &nbsp; $X_1 + \dots + X_n \sim \mathrm{Binom}(n, p)$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp;</span>$X_1 + \dots + X_n = n M_n = np + \sqrt{npq} \, Z_n$

            > $\overset{\text{CLT}}{\Longrightarrow}$ &nbsp; $\mathrm{Binom}(n, p) \approx \mathcal{N}(np, npq)$ for large $n$
            """,
            lk.interactive(_fig, controls=[b_n]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: central limit theorem
    # proof: CLT
    lk.proof(
        [
            r"""
            $X_1, \dots, X_n \sim f_X$ iid with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2 > 0$

            standardize each measurement $X_i$: &nbsp; $Y_i = \dfrac{X_i - \mu}{\sigma}$

            > $\Longrightarrow$ &nbsp; $Y_1, \dots, Y_n \sim f_Y$ iid with $E[Y] = 0$, $E[Y^2] = 1$

            > > $\leadsto$ &nbsp; $E[Y^3] = \gamma_X = \, ?$
            """,
            lk.gap(),
            r"""
            $Z_n = \dfrac{{\large\tfrac{X_1 + \dots + X_n}{n}} - \mu}{\sigma / \sqrt{n}} = \dfrac{Y_1 + \dots + Y_n}{\sqrt{n}}$

            > $\Longrightarrow$ &nbsp; $m_{Z_n}(t) = E[e^{t Z_n}] = E\big[ e^{t (Y_1 + \dots + Y_n) / \sqrt{n}} \big]$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $m_{Z_n}(t)$ </span>$= m_{Y_1 + \dots + Y_n}(t / \sqrt{n}) = \big( m_Y(t / \sqrt{n}) \big)^n$
            """,
            lk.gap(),
            r"""
            $m_Y(s) = E[e^{sY}] = 1 + s \, E[Y] + \dfrac{s^2}{2} E[Y^2] + \dfrac{s^3}{3!} E[Y^3] + \cdots$

            > $\Longrightarrow$ &nbsp; $m_Y(t / \sqrt{n}) = 1 + \dfrac{t^2}{2n} + \dfrac{t^3}{6n\sqrt{n}} \gamma_X + \cdots$

            > $\Longrightarrow$ &nbsp; $m_{Z_n}(t) = \Big( 1 + \dfrac{t^2}{2n} + \dfrac{t^3}{6n\sqrt{n}} \gamma_X + \cdots \Big)^n$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $m_{Z_n}(t) \underset{n \to \infty}{\longrightarrow} e^{t^2 / 2} = m_Z(t)$, &nbsp; $Z \sim \mathcal{N}(0, 1)$",
                r"convergence of mgfs $\Longrightarrow$<br>convergence of cdfs",
            ),
        ],
        title="of CLT"
    )
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 16 · Random samples and the law of large numbers", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys
    from fractions import Fraction

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, Fraction, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(16, "Random samples and the law of large numbers")
    return


@app.cell(hide_code=True)
def _(lk, mo, np):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    w_n = lk.slider(1, 10, step=1, value=3, label="$n$")
    t_rv = mo.ui.dropdown(["X₁", "X₂", "T = X₁ + X₂"], value="T = X₁ + X₂", label="random variable", allow_select_none=False)
    l_n = lk.slider(1, 200, step=1, value=10, label="$n$")
    d_n = lk.slider(steps=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000], value=100, label="$n$")
    # one fixed run of ten waiting times, and 2000 fixed runs of Y_1, ..., Y_10 (lambda = 2); moving n keeps them
    w_run = np.random.default_rng(1641).exponential(1 / 2, 10)
    w_sims = np.random.default_rng(1642).exponential(1 / 2, (2000, 10)).cumsum(axis=1)
    return d_n, l_n, t_rv, w_n, w_run, w_sims


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Joint expectation &nbsp; $E[u(X, Y)]$

        Covariance and correlation &nbsp; $\mathrm{Cov}(X, Y) = \sigma_{X,Y}$, &nbsp; $\rho_{X,Y} = \dfrac{\sigma_{X,Y}}{\sigma_X \sigma_Y}$
        """,
        lk.gap(),
        lk.aside(r"$X, Y$ <span class='lk-mark'>independent</span> measurements on the same experiment", r"$f_{X,Y}(x, y) = f_X(x) \, f_Y(y)$"),
        r"""
        > $\Longrightarrow$ &nbsp; $E[u(X) v(Y)] = E[u(X)] \, E[v(Y)]$

        > $\Longrightarrow$ &nbsp; $\mathrm{Var}(aX + bY) = a^2 \mathrm{Var}(X) + b^2 \mathrm{Var}(Y)$
        """,
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        $n$ measurements of the same quantity across independent repetitions of an experiment

        > $\leadsto$ &nbsp; random sample from a population
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 5.8, 6.5, 7.1")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # section
    lk.section("Random sample from a population")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # definition: independent, identically distributed
    lk.definition(
        r"""
        A collection of $n$ random variables $X_1, \dots, X_n : S \longrightarrow \mathbb{R}$ on $(S, \mathcal{E}, P)$ is called

        > • &nbsp; **independent** if

        $$
        f_{X_1, \dots, X_n}(x_1, \dots, x_n) = f_{X_1}(x_1) \cdots f_{X_n}(x_n)
        $$

        > • &nbsp; **identically distributed** if

        $$
        f_{X_i}(x) = f_{X_j}(x) \qquad \forall i, j
        $$
        """,
        label="def-iid",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # notation: iid
    lk.prose(r"For $X_1, \dots, X_n$ independent and identically distributed, with $f_{X_i} = f$, we write **$X_1, \dots, X_n \sim f$ iid**.")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # theorem: sums and products
    lk.theorem(
        r"""
        Given $X_1, \dots, X_n : S \longrightarrow \mathbb{R}$ and $a_1, \dots, a_n \in \mathbb{R}$

        > • &nbsp; $E[a_1 X_1 + \dots + a_n X_n] = a_1 E[X_1] + \dots + a_n E[X_n]$

        If $X_1, \dots, X_n$ are independent, then

        > • &nbsp; $E[u_1(X_1) \cdots u_n(X_n)] = E[u_1(X_1)] \cdots E[u_n(X_n)]$

        > • &nbsp; $\mathrm{Var}(a_1 X_1 + \dots + a_n X_n) = a_1^2 \mathrm{Var}(X_1) + \dots + a_n^2 \mathrm{Var}(X_n)$

        > • &nbsp; $m_{X_1 + \dots + X_n}(t) = m_{X_1}(t) \cdots m_{X_n}(t)$
        """,
        label="thm-sums",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # proof: mgf
    lk.proof(
        r"""
        $$
        E[e^{t(X_1 + \dots + X_n)}] = E[e^{tX_1} \cdots e^{tX_n}] = E[e^{tX_1}] \cdots E[e^{tX_n}]
        $$
        """,
        title="for mgf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # theorem: same mgf
    lk.theorem([lk.aside(r"$X_1, \dots, X_n$ are identically distributed iff $m_{X_1}(t) = \dots = m_{X_n}(t)$ near $t = 0$", "(mgfs exist near 0)")], label="thm-same-mgf")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # corollary: mgf of a sum
    lk.corollary(
        r"""
        If $X_1, \dots, X_n \sim f$ iid with mgf $m(t)$

        > $\Longrightarrow$ &nbsp; $m_{X_1 + \dots + X_n}(t) = (m(t))^n$
        """,
        label="cor-mgf-sum",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np, w_n, w_run, w_sims):
    # module: iid
    # example: customers
    # top: the time line of one run, the waiting times X_i between the arrivals; bottom: 2000 simulated values of Y_n
    # against the Gamma(n, lambda) density (lambda = 2, written in the figure)
    _n, _lam = w_n.value, 2
    _y = w_run[:_n].cumsum()
    _prev = np.concatenate([[0], _y[:-1]])
    _fig = Figure(figsize=(5.6, 3.2), layout="constrained")
    _top, _bot = _fig.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [1, 2.6]})
    _top.plot([0, 10], [0, 0], color="black", lw=0.8)
    _top.plot(0, 0, "o", color="black", ms=3.5)
    for _i, _t in enumerate(_y):
        _last = _i == _n - 1
        _top.plot([_t, _t], [-0.18, 0.18], color=lk.GREEN if _last else "black", lw=1.4 if _last else 1.0)
    for _i in range(_n) if _n <= 4 else (0, _n - 1):
        _top.text((_prev[_i] + _y[_i]) / 2, 0.3, f"$X_{{{_i + 1}}}$", color=lk.BLUE, fontsize=12, ha="center", va="bottom")
    if _n > 4:
        _top.text((_prev[1] + _prev[_n - 1]) / 2, 0.3, r"$\cdots$", color=lk.BLUE, fontsize=12, ha="center", va="bottom")
    _top.text(_y[-1], -0.35, f"$Y_{{{_n}}}$", color=lk.GREEN, fontsize=12, ha="center", va="top")
    _top.text(10, 0.3, r"$\lambda = 2$", fontsize=12, ha="right", va="bottom")
    _top.set_ylim(-1.3, 1.3)
    _top.axis("off")
    _t = np.linspace(0.001, 10, 600)
    _f = _lam**_n * _t ** (_n - 1) * np.exp(-_lam * _t) / math.factorial(_n - 1)
    _bins = np.arange(0, 10.01, 0.25)
    _h = np.histogram(w_sims[:, _n - 1], bins=_bins, density=True)[0]
    _bot.stairs(_h, _bins, color=lk.RED, lw=1.0)
    _bot.plot(_t, _f, color=lk.BLUE, lw=1.6, zorder=4)
    _ymax = 1.25 * max(float(_f.max()), float(_h.max()))
    _peak = (_n - 1) / _lam
    _xr = _peak + 1.3 * math.sqrt(_n) / _lam + 0.25
    _fr = _lam**_n * _xr ** (_n - 1) * math.exp(-_lam * _xr) / math.factorial(_n - 1)
    _bot.text(_xr, _fr + 0.04 * _ymax, r"$\mathrm{Gamma}(n, \lambda)$", color=lk.BLUE, fontsize=12, ha="left", va="bottom")
    _bot.text(_peak + 0.35, 0.9 * _ymax, "2000 simulated values of $Y_n$", color=lk.RED, fontsize=12, ha="left", va="center")
    _bot.set_xlim(0, 10)
    _bot.set_ylim(0, _ymax)
    _bot.set_xlabel("$t$")
    _bot.set_yticks([])
    _bot.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _bot.spines[_s].set_visible(False)
    lk.example(
        [
            r"""
            Customers arrive independently following $\mathrm{Pois}(\lambda)$

            > $Y_i$ = time of arrival of $i$th
            """,
            lk.aside(r"> $X_i$ = waiting time between $(i-1)$th and $i$th", r"with $X_1 = Y_1$"),
            r"""
            > > $\Longrightarrow$ &nbsp; $X_1, \dots, X_n \sim \mathrm{Exp}(\lambda)$ iid, &nbsp; $Y_i \sim \mathrm{Gamma}(i, \lambda)$ &nbsp; and &nbsp; $X_1 + \dots + X_n = Y_n$

            > > $\Longrightarrow$ &nbsp; $m_{X_1 + \dots + X_n}(t) = (\text{mgf of } \mathrm{Exp}(\lambda))^n = \Big( \dfrac{\lambda}{\lambda - t} \Big)^n$

            > > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $m_{X_1 + \dots + X_n}(t)$ </span>$= \text{mgf of } \mathrm{Gamma}(n, \lambda) = m_{Y_n}(t)$

            $\therefore$ &nbsp; $X_1, \dots, X_n \sim \mathrm{Exp}(\lambda)$ iid &nbsp; $\Longrightarrow$ &nbsp; $X_1 + \dots + X_n \sim \mathrm{Gamma}(n, \lambda)$
            """,
            lk.interactive(_fig, controls=[w_n]),
        ],
        label="ex-customers",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # theorem: similarly
    lk.theorem(
        [
            "Similarly",
            lk.aside(
                r"> • &nbsp; $X_1, \dots, X_n \sim \mathrm{Binom}(1, p)$ iid &nbsp; $\Longrightarrow$ &nbsp; $X_1 + \dots + X_n \sim \mathrm{Binom}(n, p)$",
                r"also for $\mathrm{NBinom}$",
            ),
            r"""
            > • &nbsp; $X_1, \dots, X_n \sim \mathrm{Pois}(\lambda)$ iid &nbsp; $\Longrightarrow$ &nbsp; $X_1 + \dots + X_n \sim \mathrm{Pois}(n\lambda)$

            > • &nbsp; $X_1, \dots, X_n \sim \mathcal{N}(\mu, \sigma^2)$ iid &nbsp; $\Longrightarrow$ &nbsp; $X_1 + \dots + X_n \sim \mathcal{N}(n\mu, n\sigma^2)$
            """,
        ],
        label="thm-similarly",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: iid
    # remark: different measurements
    lk.remark(
        [
            lk.aside(
                r"So far, $X_1, \dots, X_n$ are <span class='lk-mark'>different measurements</span> on a single random experiment $(S, \mathcal{E}, P)$",
                "identically distributed does not<br>mean same measurement",
            ),
            "Now, we want to consider the same measurement on independent repetitions of the experiment",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random sample
    # definition: random sample
    lk.definition(
        [
            r"""
            Given a random variable $X : S \longrightarrow \mathbb{R}$, a **random sample** from the population $X$<br>is a collection of random variables

            > $X_1, \dots, X_n : S^n \longrightarrow \mathbb{R}$
            """,
            lk.aside(
                r"> > on $S^n = \underbrace{S \times \dots \times S}_{n \text{ repetitions}}$ &nbsp; with &nbsp; $\underbrace{X_i(o_1, \dots, o_n) = X(o_i)}_{\footnotesize \begin{array}{c} \text{measurement of } X \\ \text{on the } i\text{th repetition} \end{array}}$",
                r"repetitions independent:<br>$P(A_1 \times \dots \times A_n)$<br>$= P(A_1) \cdots P(A_n)$",
            ),
            r"""
            > > $\Longrightarrow$ &nbsp; $X_1, \dots, X_n \sim f_X$ iid!
            """,
        ],
        label="def-random-sample",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random sample
    # definition: statistic
    lk.definition(
        [
            r"""
            A **statistic** about $X : S \longrightarrow \mathbb{R}$ is a function $u(X_1, \dots, X_n)$ of a random sample from $X$,<br>which summarizes information about the sample.

            > $\leadsto$ &nbsp; $T = u(X_1, \dots, X_n) : S^n \longrightarrow \mathbb{R}$ is also a random variable on $S^n$
            """,
            lk.aside(
                r"> > $\leadsto$ &nbsp; $f_T : \mathbb{R} \longrightarrow \mathbb{R}$ is called a <span class='lk-mark'>**sampling distribution**</span>",
                r"used to infer properties of a population $X$<br>from observed data $X_1 = x_1, \dots, X_n = x_n$",
            ),
        ],
        label="def-statistic",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: random sample
    # example: special statistics
    lk.example(
        r"""
        $$
        \begin{aligned}
        M_n &= \frac{X_1 + \dots + X_n}{n} = \frac{1}{n} \sum_{i=1}^n X_i && \text{sample mean}\\[6pt]
        S_n^2 &= \frac{1}{n - 1} \sum_{i=1}^n (X_i - M_n)^2 && \text{sample variance}\\[6pt]
        G_n &= \frac{1}{n} \sum_{i=1}^n \left( \frac{X_i - M_n}{S_n} \right)^3 && \text{sample skewness}
        \end{aligned}
        $$
        """,
        title="special statistics",
        label="ex-statistics",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk, t_rv):
    # module: random sample
    # example: a fair die
    # the value of the chosen random variable at each outcome (k_1, k_2) of two rolls
    _value = {
        "X₁": lambda k1, k2: int(k1 == 6),
        "X₂": lambda k1, k2: int(k2 == 6),
        "T = X₁ + X₂": lambda k1, k2: int(k1 == 6) + int(k2 == 6),
    }[t_rv.value]
    _fig = Figure(figsize=(2.9, 2.75), layout="constrained")
    _ax = _fig.subplots()
    for _k1 in range(1, 7):
        for _k2 in range(1, 7):
            _v = _value(_k1, _k2)
            _ax.fill([_k1 - 0.5, _k1 + 0.5, _k1 + 0.5, _k1 - 0.5], [_k2 - 0.5, _k2 - 0.5, _k2 + 0.5, _k2 + 0.5], facecolor=lk.LIGHT if _v else "white", edgecolor=lk.GREY, lw=0.8)
            _ax.text(_k1, _k2, f"${_v}$", ha="center", va="center", fontsize=13)
    _ax.set_xlim(0.5, 6.5)
    _ax.set_ylim(0.5, 6.5)
    _ax.set_aspect("equal")
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks(range(1, 7))
    _ax.set_xlabel("$k_1$")
    _ax.set_ylabel("$k_2$", rotation=0, labelpad=10)
    _ax.tick_params(length=0, labelsize=12)
    for _s in _ax.spines.values():
        _s.set_visible(False)
    lk.example(
        [
            r"""
            Roll a fair die &nbsp; $S = \{1, 2, 3, 4, 5, 6\}$

            > $X : S \longrightarrow \mathbb{R}$, &nbsp; $X(k) = \begin{cases} 1, & k = 6\\ 0, & k \neq 6 \end{cases}$
            """,
            lk.aside(r"> $\leadsto$ &nbsp; $P(\{k\}) = {\large\tfrac{1}{6}}$ &nbsp; $\forall k \in S$", "fair"),
            r"""
            > > $\Longrightarrow$ &nbsp; $f_X(x) = P(X = x) = \begin{cases} {\large\tfrac{1}{6}}, & x = 1\\[4pt] {\large\tfrac{5}{6}}, & x = 0 \end{cases}$

            > > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $f_X(x) = P(X = x)$ </span>$= \dbinom{1}{x} \Big( \dfrac{1}{6} \Big)^x \Big( \dfrac{5}{6} \Big)^{1 - x} = \mathrm{Binom}(1, 1/6)(x)$
            """,
            lk.gap(),
            r"""
            Roll a fair die twice (independently)

            > $X_1, X_2 : S \times S \longrightarrow \mathbb{R}$, &nbsp; $X_1(k_1, k_2) = X(k_1) = \begin{cases} 1, & k_1 = 6\\ 0, & k_1 \neq 6 \end{cases}$

            > <span class="lk-ghost">$X_1, X_2 : S \times S \longrightarrow \mathbb{R}$, &nbsp; </span>$X_2(k_1, k_2) = X(k_2) = \begin{cases} 1, & k_2 = 6\\ 0, & k_2 \neq 6 \end{cases}$
            """,
            lk.aside(r"> $\leadsto$ &nbsp; $P(\{(k_1, k_2)\}) = {\large\tfrac{1}{36}} = P(\{k_1\}) \, P(\{k_2\})$", "fair, independent"),
            r"""
            > > $\Longrightarrow$ &nbsp; $f_{X_1}(x) = P(X_1 = x) = \mathrm{Binom}(1, 1/6)(x)$

            > > $\Longrightarrow$ &nbsp; $f_{X_2}(x) = P(X_2 = x) = \mathrm{Binom}(1, 1/6)(x)$

            > > $\leadsto$ &nbsp; $X_1, X_2 \sim \mathrm{Binom}(1, 1/6)$ iid

            > $T = X_1 + X_2 : S \times S \longrightarrow \mathbb{R}$

            > > $T(k_1, k_2) = X(k_1) + X(k_2) = \begin{cases} 2, & k_1 = 6, \ k_2 = 6\\ 1, & k_1 = 6, \ k_2 \neq 6 \ \text{ or } \ k_1 \neq 6, \ k_2 = 6\\ 0, & k_1 \neq 6, \ k_2 \neq 6 \end{cases}$

            > > > $\Longrightarrow$ &nbsp; $f_T(2) = {\large\tfrac{1}{36}}$, &nbsp; $f_T(1) = {\large\tfrac{10}{36}}$, &nbsp; $f_T(0) = {\large\tfrac{25}{36}}$

            > > > $\leadsto$ &nbsp; $T \sim \mathrm{Binom}(2, 1/6)$
            """,
            lk.interactive(_fig, controls=[t_rv]),
        ],
        label="ex-die",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: law of large numbers
    # theorem: mean and variance of M_n, LLN
    lk.theorem(
        [
            r"""
            Given a random sample $X_1, \dots, X_n$ from a population $X$ with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2$

            $$
            E[M_n] = \mu, \qquad \mathrm{Var}(M_n) = \frac{1}{n} \sigma^2
            $$

            Moreover, for any error threshold $\varepsilon > 0$,
            """,
            lk.aside(
                r"$$P\big(|M_n - \mu| \ge \varepsilon\big) \le \frac{1}{n} \frac{\sigma^2}{\varepsilon^2} \longrightarrow 0 \quad \text{as } n \to \infty$$",
                "law of large numbers",
            ),
            r"""
            > $\leadsto$ &nbsp; the probability that the sample mean is far away from the population mean<br>goes to zero as we take large samples
            """,
        ],
        label="thm-lln",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: law of large numbers
    # proof: LLN
    lk.proof(
        [
            r"""
            $$
            \begin{aligned}
            E[M_n] &= E\big[ {\large\tfrac{1}{n}} (X_1 + \dots + X_n) \big] = \frac{1}{n} \, n\mu = \mu\\[4pt]
            \mathrm{Var}(M_n) &= \mathrm{Var}\big( {\large\tfrac{1}{n}} (X_1 + \dots + X_n) \big) = \frac{1}{n^2} \, n\sigma^2 = \frac{1}{n} \sigma^2
            \end{aligned}
            $$
            """,
            lk.gap(),
            lk.aside(
                r"""
            $$
            \begin{aligned}
            \frac{\sigma^2}{n} = \mathrm{Var}(M_n) &= \int_{-\infty}^{\infty} (m - \mu)^2 f_{M_n}(m) \, dm\\
            &\ge \int_{|m - \mu| \ge \varepsilon} (m - \mu)^2 f_{M_n}(m) \, dm\\
            &\ge \int_{|m - \mu| \ge \varepsilon} \varepsilon^2 f_{M_n}(m) \, dm = \varepsilon^2 P(|M_n - \mu| \ge \varepsilon)
            \end{aligned}
            $$
            """,
                [(1, r"$\sum$ for discrete $M_n$")],
                rows=3,
            ),
            r"""
            $$
            \therefore \quad P(|M_n - \mu| \ge \varepsilon) \le \frac{1}{n} \frac{\sigma^2}{\varepsilon^2} \qquad \forall \varepsilon > 0, \ \forall n \ge 1
            $$
            """,
        ],
        title="of LLN",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: law of large numbers
    # illustration (moved out of the proof):
    # the sketch of the real line: the parts |m - mu| >= epsilon in red, a point m in one of them
    _fig = Figure(figsize=(4.4, 1.15), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-2.75, 2.75)
    _ax.set_ylim(-0.95, 0.6)
    _ax.axis("off")
    lk.arrow(_ax, (-2.7, 0), (2.7, 0), "black", lw=0.8)
    _ax.text(2.72, -0.08, r"$\mathbb{R}$", fontsize=12, ha="left", va="top")
    _ax.plot([-2.6, -1], [0, 0], color=lk.RED, lw=2.6, solid_capstyle="butt", zorder=5)
    _ax.plot([1, 2.45], [0, 0], color=lk.RED, lw=2.6, solid_capstyle="butt", zorder=5)
    for _x, _name in ((-1, r"$\mu - \varepsilon$"), (0, r"$\mu$"), (1, r"$\mu + \varepsilon$")):
        _ax.plot([_x, _x], [-0.1, 0.1], color="black", lw=0.8)
        _ax.text(_x, 0.16, _name, fontsize=12, ha="center", va="bottom")
    _ax.plot(1.7, 0, "o", color=lk.BLUE, ms=4, zorder=5)
    _ax.text(1.7, 0.16, "$m$", color=lk.BLUE, fontsize=12, ha="center", va="bottom")
    _ax.text(0, -0.62, r"$|m - \mu| \geq \varepsilon$", color=lk.RED, fontsize=12, ha="center", va="center")
    lk.arrow(_ax, (-0.75, -0.55), (-1.8, -0.08), lk.RED, lw=0.9)
    lk.arrow(_ax, (0.75, -0.55), (1.3, -0.08), lk.RED, lw=0.9)
    lk.prose(lk.figure(_fig))
    return


@app.cell(hide_code=True)
def _(Figure, Fraction, l_n, lk, math):
    # module: law of large numbers
    # illustration of the LLN (moved out of the theorem):
    # M_n for n rolls of the fair die of the example (X = 1 on a six): n M_n ~ Binom(n, 1/6), so M_n takes the values k/n;
    # mu = 1/6, epsilon = 1/10, the values with |m - mu| >= epsilon in red
    _n = l_n.value
    _p, _eps = Fraction(1, 6), Fraction(1, 10)
    _mu = _p
    _pmf = [math.comb(_n, _k) * float(_p) ** _k * float(1 - _p) ** (_n - _k) for _k in range(_n + 1)]
    _far = [abs(Fraction(_k, _n) - _mu) >= _eps for _k in range(_n + 1)]
    _fig = Figure(figsize=(5.0, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _top = 1.25 * max(_pmf)
    for _x in (float(_mu - _eps), float(_mu + _eps)):
        _ax.plot([_x, _x], [0, _top], color=lk.GREY, lw=1.0, ls=(0, (4, 3)))
    _lw = 2.4 if _n <= 60 else 1.4
    for _k in range(_n + 1):
        _ax.plot([_k / _n, _k / _n], [0, _pmf[_k]], color=lk.RED if _far[_k] else lk.BLUE, lw=_lw, solid_capstyle="butt")
    _ax.text(0.97, 0.92 * _top, r"$|m - \mu| \geq \varepsilon$", color=lk.RED, fontsize=13, ha="right", va="top")
    _ax.text(0.97, 0.7 * _top, r"$\mu = 1/6, \ \varepsilon = 0.1$", fontsize=12, ha="right", va="top")
    _ax.set_xlim(-0.03, 1.03)
    _ax.set_ylim(0, _top)
    _ax.set_xticks([float(_mu - _eps), float(_mu), float(_mu + _eps), 1], [r"$\mu - \varepsilon$", r"$\mu$", r"$\mu + \varepsilon$", "$1$"])
    _ax.set_yticks([])
    _ax.set_xlabel("$m$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)
    _ax.text(0.36, 0.62 * max(_pmf), r"$f_{M_n}$", color=lk.BLUE, fontsize=12, ha="left", va="center")
    lk.prose(lk.interactive(_fig, controls=[l_n]))
    return


@app.cell(hide_code=True)
def _(Figure, d_n, lk, np):
    # module: law of large numbers
    # example: fair die
    # the pmf of M_n for a fair die (X_1 + ... + X_n by repeated convolution, so M_n takes the values k / n), with the
    # values M_n <= 3 or M_n >= 4 in red
    _n = d_n.value
    _p = np.array([1.0])
    for _ in range(_n):
        _p = np.convolve(_p, np.full(6, 1 / 6))
    _k = np.arange(_n, 6 * _n + 1)
    _m = _k / _n
    _tail = (_k <= 3 * _n) | (_k >= 4 * _n)
    _few = len(_k) <= 80
    _top = float(_p.max()) * 1.32
    _fig = Figure(figsize=(4.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    for _x in (3, 4):
        _ax.axvline(_x, color=lk.GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
    for _mask, _c in ((~_tail, lk.BLUE), (_tail, lk.RED)):
        _ax.vlines(_m[_mask], 0, _p[_mask], color=_c, lw=1.2 if _few else 0.8, zorder=3)
        if _few:
            _ax.plot(_m[_mask], _p[_mask], "o", color=_c, ms=3, zorder=4)
    _ax.text(3.5, _top * 0.97, r"$f_{M_n}$", color="black", fontsize=12, ha="center", va="top")
    _ax.text(2.9, _top * 0.97, r"$M_n \leq 3$", color=lk.RED, fontsize=12, ha="right", va="top")
    _ax.text(4.1, _top * 0.97, r"$M_n \geq 4$", color=lk.RED, fontsize=12, ha="left", va="top")
    _ax.set_xlim(0.6, 6.4)
    _ax.set_ylim(0, _top)
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks([])
    _ax.set_xlabel("$m$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)
    lk.example(
        [
            r"""
            $X$ = result &nbsp; $\Longrightarrow$ &nbsp; $f_X(x) = {\large\tfrac{1}{6}}$, &nbsp; $x = 1, 2, \dots, 6$

            > $E[X] = {\large\tfrac{1}{6}} (1 + 2 + 3 + 4 + 5 + 6) = 3.5$

            > $E[X^2] = {\large\tfrac{1}{6}} (1 + 4 + 9 + 16 + 25 + 36) = {\large\tfrac{91}{6}}$

            > $\Longrightarrow$ &nbsp; $\mathrm{Var}(X) = E[X^2] - E[X]^2 = {\large\tfrac{35}{12}}$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $P\big(\underbrace{|M_n - 3.5| \ge 0.5}_{M_n \le 3 \text{ or } M_n \ge 4}\big) \le {\large\tfrac{1}{n}} {\large\tfrac{35}{3}}$",
                r"$n = 100$: &nbsp; $P \le 12\%$<br>$n = 1000$: &nbsp; $P \le 1.2\%$",
            ),
            lk.interactive(_fig, controls=[d_n]),
        ],
        title="fair die",
    )
    return


if __name__ == "__main__":
    app.run()

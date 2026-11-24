import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 18 · Estimators: bias, standard error and consistency", css_file="lecturekit/style.css")


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
    lk.lecture(18, "Estimators: bias, standard error and consistency")
    return


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    dn = lk.slider(5, 50, step=5, value=5, label="$n$")
    return (dn,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Random samples & statistics

        > $\leadsto$ &nbsp; LLN & CLT
        """,
        lk.under(
            r"""
            $X_1, \dots, X_n \sim f_X$ iid with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2$

            > $\Longrightarrow$ &nbsp; $M_n = \frac{1}{n} \sum_{i=1}^n X_i$ has $E[M_n] = \mu$, $\mathrm{Var}(M_n) = \sigma^2 / n$ and

            > > • &nbsp; $\forall \varepsilon > 0$, &nbsp; $P\big(\underbrace{|M_n - \mu|}_{\footnotesize \begin{array}{c} \text{error of} \\ \text{estimation} \end{array}} \ge \varepsilon\big) \le {\large\tfrac{1}{n}} {\large\tfrac{\sigma^2}{\varepsilon^2}} \underset{n \to \infty}{\longrightarrow} 0$

            > > • &nbsp; $\forall z \in \mathbb{R}$, &nbsp; $P\Big(\underbrace{\dfrac{M_n - \mu}{\sigma / \sqrt{n}}}_{\footnotesize \begin{array}{c} \text{standardized} \\ \text{mean } Z_n \end{array}} \le z\Big) = F_{Z_n}(z) \underset{n \to \infty}{\longrightarrow} \Phi(z)$
            """
        ),
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"How good is $M_n$ as an estimator of $\mu$?", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 8.2–8.4, 9.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # section
    lk.section("Estimators: bias, standard error and consistency")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # definition: estimator
    lk.definition(
        [
            r"""
            Given $X : S \longrightarrow \mathbb{R}$ with an unknown parameter $\theta$ (e.g. $\mu$, $\sigma^2$, $\gamma$, …), an **estimator** for $\theta$ is any statistic

            $$
            \hat{\theta}_n = u(X_1, \dots, X_n) : S \times \dots \times S \longrightarrow \mathbb{R}
            $$

            used to estimate $\theta$ from observed values of $X_i$.

            If $X_i(o) = x_i$, then
            """,
            lk.aside(r"> $\hat{\theta}_n(o) = u(x_1, \dots, x_n)$ is <span class='lk-mark'>an estimate of $\theta$</span>", "a guess for its value"),
        ],
        label="def-estimator",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # definition: unbiased
    lk.definition(
        r"""
        We call $\hat{\theta}_n$ an **unbiased estimator** for $\theta$ if

        $$
        \mathrm{Bias}(\hat{\theta}_n) = E[\hat{\theta}_n] - \theta = 0
        $$
        """,
        label="def-unbiased",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # theorem: unbiased estimators
    # the first line is its own display so the label sits on it; all three lines are padded to one width, so that
    # "=" sits under "=" and the words start in one column
    lk.theorem(
        [
            r"""
            $$
            \hphantom{S_n^2}\mathllap{M_n} = \mathrlap{\frac{1}{n} \sum_{i=1}^n X_i}\hphantom{\frac{1}{n} \sum_{i=1}^n \left( \frac{X_i - M_n}{S_n} \right)^3} \qquad \mathrlap{\text{is an unbiased estimator for } \mu \text{}}\hphantom{\text{is an unbiased estimator for } \mu}
            $$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \hphantom{S_n^2}\mathllap{S_n^2} = \mathrlap{\frac{1}{n - 1} \sum_{i=1}^n (X_i - M_n)^2}\hphantom{\frac{1}{n} \sum_{i=1}^n \left( \frac{X_i - M_n}{S_n} \right)^3} \qquad \mathrlap{\text{is unbiased for } \sigma^2 \text{}}\hphantom{\text{is an unbiased estimator for } \mu}\\[14pt]
                \hphantom{S_n^2}\mathllap{G_n} = \mathrlap{\frac{1}{n} \sum_{i=1}^n \left( \frac{X_i - M_n}{S_n} \right)^3}\hphantom{\frac{1}{n} \sum_{i=1}^n \left( \frac{X_i - M_n}{S_n} \right)^3} \qquad \mathrlap{\text{in general is biased for } \gamma \text{}}\hphantom{\text{is an unbiased estimator for } \mu}
                \end{aligned}
                $$
                """,
                "$E[G_n]$ usually depends<br>on higher moments",
                at="last",
            ),
        ],
        label="thm-unbiased",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # proof: S_n^2
    lk.proof(
        [
            r"""
            $X_1, \dots, X_n \sim f_X$ iid

            $$
            \begin{alignedat}{2}
            && \sum_{i=1}^n (X_i - M_n)^2 &= \sum_{i=1}^n (X_i^2 - 2 M_n X_i + M_n^2)\\
            &&&= \sum_{i=1}^n X_i^2 - n M_n^2\\[10pt]
            \Longrightarrow \quad && E\Big[ \sum_{i=1}^n (X_i - M_n)^2 \Big] &= \sum_{i=1}^n E[X_i^2] - n \, E[M_n^2]\\
            &&&= \sum_{i=1}^n \big( \mathrm{Var}(X_i) + E[X_i]^2 \big) - n \, \mathrm{Var}(M_n) - n \, E[M_n]^2\\
            &&&= n \sigma^2 + n \mu^2 - n \, \sigma^2 / n - n \mu^2 = (n - 1) \, \sigma^2
            \end{alignedat}
            $$
            """,
            lk.aside(
                r"$$\Longrightarrow \quad \mk{\frac{1}{n - 1}} \sum_{i=1}^n (X_i - M_n)^2 \ \text{ is an unbiased estimator for } \sigma^2$$",
                r"not $\displaystyle \frac{1}{n} \sum_{i=1}^n (X_i - M_n)^2$",
            ),
        ],
        title="for $S_n^2$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # remark: biased sample variance
    lk.remark(
        r"""
        If we define $\displaystyle \hat{\sigma}_n^2 = \frac{1}{n} \sum_{i=1}^n (X_i - M_n)^2$

        > $\Longrightarrow$ &nbsp; $E[\hat{\sigma}_n^2] = {\large\tfrac{n - 1}{n}} E[S_n^2] = {\large\tfrac{n - 1}{n}} \sigma^2$

        > $\Longrightarrow$ &nbsp; $\mathrm{Bias}(\hat{\sigma}_n^2) = {\large\tfrac{n - 1}{n}} \sigma^2 - \sigma^2 = -{\large\tfrac{1}{n}} \sigma^2$

        $\leadsto$ &nbsp; sometimes we call $\hat{\sigma}_n^2$ the **biased sample variance** and $S_n^2$ the **unbiased sample variance**
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: estimators and bias
    # consequence: what the bias measures
    lk.prose(
        r"""
        $\leadsto$ &nbsp; estimates from a biased estimator are expected to differ from the true value of the parameter

        $\leadsto$ &nbsp; $\mathrm{Bias}(\hat{\theta}_n)$ measures the expected estimate error.
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard error
    # definition: standard error
    lk.definition(
        r"""
        Given an estimator $\hat{\theta}_n$ for a parameter $\theta$, the **standard error** of $\hat{\theta}_n$ is

        $$
        \mathrm{SE}(\hat{\theta}_n) = \sqrt{\mathrm{Var}(\hat{\theta}_n)}
        $$
        """,
        label="def-se",
    )
    return


@app.cell(hide_code=True)
def _(Figure, dn, lk, math, np):
    # module: standard error
    # example: is a die fair?
    # the pmf of M_n for a fair die (X_1 + ... + X_n by repeated convolution, so M_n takes the values k / n), with mu = 3.5
    # dashed and the values 4 and 5.6 of the two samples in red; n moves with the slider (multiples of 5, so 5.6 is a value)
    _n = int(dn.value)
    _p = np.array([1.0])
    for _ in range(_n):
        _p = np.convolve(_p, np.full(6, 1 / 6))
    _k = np.arange(_n, 6 * _n + 1)
    _m = _k / _n
    _se = math.sqrt(35 / (12 * _n))
    _seen = (_k == 4 * _n) | (5 * _k == 28 * _n)
    _top = float(_p.max()) * 1.32
    _few = len(_k) <= 80
    _fig = Figure(figsize=(4.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(3.5, color=lk.GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
    for _mask, _c in ((~_seen, lk.BLUE), (_seen, lk.RED)):
        _ax.vlines(_m[_mask], 0, _p[_mask], color=_c, lw=1.2 if _few else 0.8, zorder=3)
        if _few:
            _ax.plot(_m[_mask], _p[_mask], "o", color=_c, ms=3, zorder=4)
    for _x, _name in ((4, r"$M_5(o)$"), (5.6, r"$M_5(\tilde{o})$")):
        _h = float(_p[np.isclose(_m, _x)][0])
        _ax.plot(_x, _h, "o", color=lk.RED, ms=5, zorder=5, clip_on=False)
        _ax.text(_x + (0.06 if _x == 4 else 0), _h + 0.03 * _top, _name if _n == 5 else f"${_x:g}$", color=lk.RED, fontsize=12, ha="left" if _x == 4 else "center", va="bottom")
    _ax.text(3.45, _top * 0.97, r"$\mu = 3.5$", color="black", fontsize=12, ha="right", va="top")
    _ax.annotate(r"$f_{M_n}$", (3.5 - 1.18 * _se, 0.5 * float(_p.max())), textcoords="offset points", xytext=(-6, 0), color=lk.BLUE, fontsize=12, ha="right", va="center")
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
            Given a die, is it fair?

            $X$ = result of one roll, $X_1, \dots, X_5 \sim f_X$ iid, size $n = 5$

            > fair &nbsp; $\Longrightarrow$ &nbsp; $\mu = 3.5$, &nbsp; $\sigma^2 = {\large\tfrac{35}{12}}$ &nbsp; $\Longrightarrow$ &nbsp; $\mathrm{SE}(M_5) = \sqrt{{\large\tfrac{1}{5}} {\large\tfrac{35}{12}}} \approx 0.76$

            > $o = (2, 5, 3, 6, 4)$ &nbsp; $\Longrightarrow$ &nbsp; $M_5(o) = {\large\tfrac{2 + 5 + 3 + 6 + 4}{5}} = 4$
            """,
            lk.aside(r'> <span class="lk-ghost">$o = (2, 5, 3, 6, 4)$ &nbsp;</span>$\Longrightarrow$ &nbsp; $|M_5(o) - 3.5| = 0.5 \approx 0.66 \, \mathrm{SE}(M_5)$', "not bad!"),
            r"> $\tilde{o} = (6, 5, 6, 6, 5)$ &nbsp; $\Longrightarrow$ &nbsp; $M_5(\tilde{o}) = {\large\tfrac{6 + 5 + 6 + 6 + 5}{5}} = 5.6$",
            lk.aside(r'> <span class="lk-ghost">$\tilde{o} = (6, 5, 6, 6, 5)$ &nbsp;</span>$\Longrightarrow$ &nbsp; $|M_5(\tilde{o}) - 3.5| \approx 2.75 \, \mathrm{SE}(M_5)$', "suspicious!"),
            lk.interactive(_fig, controls=[dn]),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard error
    # remark: CLT
    lk.remark(
        [
            lk.aside(r"For $n$ large, CLT", r"$n = 5$ (not large enough for CLT...)"),
            r"""
        > $\Longrightarrow$ &nbsp; $P\big(|M_n - \mu| \ge k \, \mathrm{SE}(M_n)\big) = P(|Z_n| \ge k) \approx 2\big(1 - \Phi(k)\big)$

        > > $2\big(1 - \Phi(0.66)\big) \approx 51\%$

        > > $2\big(1 - \Phi(2.75)\big) \approx 0.6\%$
        """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard error
    # consequence: what the standard error measures
    lk.prose(r"$\leadsto$ &nbsp; $\mathrm{SE}(\hat{\theta}_n)$ measures the typical error range (but only for unbiased estimators!)")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mean squared error
    # definition: mean squared error
    lk.definition(
        r"""
        The **mean squared error** of $\hat{\theta}_n$ is

        $$
        \mathrm{MSE}(\hat{\theta}_n) = E\big[(\hat{\theta}_n - \theta)^2\big]
        $$
        """,
        label="def-mse",
    )
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # module: mean squared error
    # consequence: MSE = SE^2 + Bias^2
    # the right triangle: theta, E[theta_n] to its right (|Bias|), theta_n above E[theta_n] (SE), and sqrt(MSE) from
    # theta to theta_n
    _fig = Figure(figsize=(3.4, 2.4))
    _ax = _fig.add_axes((0, 0, 1, 1))
    _ax.set_xlim(-0.9, 4.0)
    _ax.set_ylim(-0.75, 2.7)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _t, _e, _h = (0.0, 0.0), (2.8, 0.0), (2.8, 2.0)
    lk.arrow(_ax, _t, _e, "black", lw=1.4)
    lk.arrow(_ax, _e, _h, "black", lw=1.4)
    lk.arrow(_ax, _t, _h, "black", lw=1.4)
    for _q in (_t, _e, _h):
        _ax.plot(*_q, "o", color="black", ms=4, zorder=6)
    _ax.text(-0.15, 0, r"$\theta$", fontsize=13, ha="right", va="center")
    _ax.text(2.95, -0.05, r"$E[\hat{\theta}_n]$", fontsize=13, ha="left", va="top")
    _ax.text(2.8, 2.15, r"$\hat{\theta}_n$", fontsize=13, ha="center", va="bottom")
    _ax.text(1.4, -0.15, r"$|\mathrm{Bias}|$", color=lk.RED, fontsize=13, ha="center", va="top")
    _ax.text(2.95, 1.0, r"$\mathrm{SE}$", color=lk.RED, fontsize=13, ha="left", va="center")
    _ax.text(1.25, 1.15, r"$\sqrt{\mathrm{MSE}}$", color=lk.RED, fontsize=13, ha="right", va="bottom")
    lk.prose(
        r"""
        $$
        \begin{aligned}
        \Longrightarrow \quad \mathrm{MSE}(\hat{\theta}_n) &= E\big[(\hat{\theta}_n - \theta)^2\big]\\
        &= E[\hat{\theta}_n^2] - 2\theta E[\hat{\theta}_n] + \theta^2\\
        &= \mathrm{Var}(\hat{\theta}_n) + E[\hat{\theta}_n]^2 - 2\theta E[\hat{\theta}_n] + \theta^2\\
        &= \mathrm{Var}(\hat{\theta}_n) + \big(E[\hat{\theta}_n] - \theta\big)^2 = \mathrm{SE}(\hat{\theta}_n)^2 + \mathrm{Bias}(\hat{\theta}_n)^2
        \end{aligned}
        $$
        """,
        lk.figure(_fig),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mean squared error
    # consequence: what the mean squared error measures
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; $\mathrm{MSE}(\hat{\theta}_n)$ measures the <span class='lk-mark'>expected squared error</span>",
            r"= square of typical error range<br>(for any estimator!)",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: mean squared error
    # remark: Pythagoras
    lk.remark(
        [
            r"$E\big[(\hat{\theta}_n - E[\hat{\theta}_n])(E[\hat{\theta}_n] - \theta)\big] = 0$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $E\big[(\hat{\theta}_n - \theta)^2\big] = E\big[(\hat{\theta}_n - E[\hat{\theta}_n])^2\big] + E\big[(E[\hat{\theta}_n] - \theta)^2\big]$",
                "another Pythagoras!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: consistency
    # definition: consistent
    lk.definition(
        r"""
        An estimator $\hat{\theta}_n$ for $\theta$ is **consistent** if

        $$
        \forall \varepsilon > 0 \quad P\big(|\hat{\theta}_n - \theta| \ge \varepsilon\big) \longrightarrow 0 \quad \text{as } n \to +\infty
        $$
        """,
        label="def-consistent",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: consistency
    # theorem: bias and SE to 0
    lk.theorem(
        r"If $\mathrm{Bias}(\hat{\theta}_n) \to 0$ and $\mathrm{SE}(\hat{\theta}_n) \to 0$ as $n \to +\infty$, then $\hat{\theta}_n$ is consistent for $\theta$",
        label="thm-consistent",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: consistency
    # proof
    lk.proof(
        r"""
        $$
        \begin{alignedat}{2}
        && \mathrm{MSE}(\hat{\theta}_n) = \int_{-\infty}^{\infty} (t - \theta)^2 f_{\hat{\theta}_n}(t) \, dt &\ge \int_{|t - \theta| \ge \varepsilon} (t - \theta)^2 f_{\hat{\theta}_n}(t) \, dt\\
        &&&\ge \varepsilon^2 \int_{|t - \theta| \ge \varepsilon} f_{\hat{\theta}_n}(t) \, dt = \varepsilon^2 P\big(|\hat{\theta}_n - \theta| \ge \varepsilon\big)\\[10pt]
        \Longrightarrow \quad && P\big(|\hat{\theta}_n - \theta| \ge \varepsilon\big) &\le \frac{\mathrm{SE}(\hat{\theta}_n)^2 + \mathrm{Bias}(\hat{\theta}_n)^2}{\varepsilon^2} \underset{n \to +\infty}{\longrightarrow} 0
        \end{alignedat}
        $$
        """,
        title=r"similar to the LLN, for $\hat{\theta}_n$ continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: consistency
    # theorem: continuous functions
    lk.theorem(
        r"""
        For any continuous function $g : \mathbb{R} \longrightarrow \mathbb{R}$, if $\hat{\theta}_n$ is a consistent estimator for $\theta$,<br>then $g(\hat{\theta}_n)$ is a consistent estimator for $g(\theta)$
        """,
        label="thm-continuous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: consistency
    # example: S_n
    lk.example(
        [
            lk.aside(r"$S_n^2$ is a consistent estimator for $\sigma^2$", "by " + lk.ref("thm-consistent") + r", if $E[X^4] < \infty$"),
            r"""
        > $\Longrightarrow$ &nbsp; $\sqrt{S_n^2}$ is a consistent estimator for $\sigma$
        """,
        ]
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
    # exercise: Bernoulli
    lk.exercise(
        r"""
        Let $X_1, \dots, X_n \sim \mathrm{Binom}(1, p)$ iid, $q = 1 - p$

        > $M_n = \dfrac{1}{n} \displaystyle\sum_{i=1}^n X_i$, &nbsp; $\hat{\sigma}_n^2 = \dfrac{1}{n} \displaystyle\sum_{i=1}^n (X_i - M_n)^2$

        a) find the bias of $M_n(1 - M_n)$ as an estimator for $pq$

        b) is $M_n(1 - M_n)$ a consistent estimator for $pq$?

        c) prove that $\hat{\sigma}_n^2 = M_n(1 - M_n)$
        """,
        label="ex-bernoulli",
    )
    return


if __name__ == "__main__":
    app.run()

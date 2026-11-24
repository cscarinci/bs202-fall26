import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 20 · Confidence intervals", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(20, "Confidence intervals")
    return


@app.cell(hide_code=True)
def _(Figure, lk):
    # Helper of this lecture: the sketch of an interval of half-width eps = 19.6 on the number line,
    # around mu (fixed at 50) or around M_4; the interval is red when it misses mu

    def interval(around, m4=56.0, eps=19.6, mu=50.0):
        fig = Figure(figsize=(6.4, 1.25))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(-6, 106)
        ax.set_ylim(-0.75, 0.75)
        ax.axis("off")

        def name(x, y, text, color, va):
            ax.annotate(text, (x, y), textcoords="offset points", xytext=(0, 9 if va == "bottom" else -9), ha="center", va=va, color=color, fontsize=13, zorder=10)

        lk.arrow(ax, (-4, 0), (104, 0), "black", lw=0.9)
        centre, sym = (mu, r"\mu") if around == "mu" else (m4, "M_4")
        color = lk.RED if abs(centre - mu) > eps else lk.BLUE
        ax.plot([centre - eps, centre + eps], [0, 0], color=color, lw=2.2, solid_capstyle="butt", zorder=3)
        for x in (centre - eps, centre + eps):
            ax.plot([x, x], [-0.16, 0.16], color=color, lw=1.6, zorder=3)
        ax.plot(mu, 0, "o", color=lk.RED, ms=5, zorder=5)
        ax.plot(m4, 0, "o", color=lk.GREEN, ms=5, zorder=5)
        ends = "top" if around == "mu" else "bottom"
        name(centre - eps, 0.16 if ends == "bottom" else -0.16, rf"${sym}-\varepsilon$", color, ends)
        name(centre + eps, 0.16 if ends == "bottom" else -0.16, rf"${sym}+\varepsilon$", color, ends)
        name(m4, 0.1, "$M_4$", lk.GREEN, "bottom")
        name(mu, -0.1, r"$\mu$", lk.RED, "top")
        return fig

    return (interval,)


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    m4 = lk.slider(20, 80, step=1, value=56, label="$M_4$")
    return (m4,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Estimators, bias, SE, and MSE

        $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$

        $\hat\theta_n=u(X_1,\dots,X_n)$ estimator for $\theta$
        """,
        lk.aside(r"> $\leadsto$ &nbsp; $\mathrm{Bias}(\hat\theta_n)=E[\hat\theta_n-\theta]$", "expected error"),
        lk.aside(r"> $\leadsto$ &nbsp; $\mathrm{SE}(\hat\theta_n)=\sqrt{\mathrm{Var}(\hat\theta_n)}$", "typical error range<br>for unbiased estimators"),
        lk.aside(r"> $\leadsto$ &nbsp; $\mathrm{MSE}(\hat\theta_n)=E\big[(\hat\theta_n-\theta)^2\big]$", "square of typical error<br>range for any estimator"),
        r"""
        > <span class="lk-ghost">$\leadsto$ &nbsp; $\mathrm{MSE}(\hat\theta_n)$</span>$=\mathrm{Bias}(\hat\theta_n)^2+\mathrm{SE}(\hat\theta_n)^2$

        If $\mathrm{Bias}(\hat\theta_n)\to0$, $\mathrm{SE}(\hat\theta_n)\to0$ for $n\to\infty$ $\big(\!\Longleftrightarrow\ \mathrm{MSE}(\hat\theta_n)\to0\text{ for }n\to\infty\big)$, then

        > $P\big(|\hat\theta_n-\theta|\ge\varepsilon\big)\longrightarrow0$ &nbsp; as $n\to\infty$ &nbsp; $\forall\varepsilon>0$

        > > $\leadsto$ &nbsp; $\hat\theta_n$ has arbitrarily large probability of being arbitrarily close to $\theta$<br><span class="lk-ghost">$\leadsto$ &nbsp;</span>for sufficiently large sample size $n$
        """,
        lk.aside(
            r"> $\leadsto$ &nbsp; $\hat\theta_n$ is a <span class='lk-mark'>consistent estimator</span> for $\theta$",
            "a good estimator!",
        ),
        title="Last time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        For fixed $n$, how close and with what probability?

        > $\leadsto$ &nbsp; confidence intervals for $\theta$
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 8.5–8.7")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # section
    lk.section("Confidence intervals")
    return


@app.cell(hide_code=True)
def _(interval, lk, m4):
    # module: confidence intervals
    # example: midterm scores, the interval around mu and the interval around M_4
    lk.example(
        [
            r"""
            Midterm scores $X\sim\mathcal N(\mu,20^2)$, $\mu$ unknown

            > $\leadsto$ &nbsp; given 4 scores $X_1=30$, $X_2=54$, $X_3=62$, $X_4=78$ &nbsp; $\Longrightarrow$ &nbsp; $M_4=56$

            > $\leadsto$ &nbsp; how close is $M_4$ to $\mu$? with what probability?

            $M_4=\dfrac{X_1+X_2+X_3+X_4}{4}\sim\mathcal N\Big(\mu,\underbrace{\dfrac{20^2}{4}}_{\footnotesize 10^2=\mathrm{SE}(M_4)^2}\Big)$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $Z_4=\dfrac{M_4-\mu}{\mathrm{SE}(M_4)}\sim\mathcal N(0,1)$",
                r"since $X$ is normal",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $P\big(|M_4-\mu|\le \overbrace{\underbrace{z\,\mathrm{SE}(M_4)}_{\footnotesize\text{error threshold}}}^{\footnotesize\varepsilon}\big)=P(|Z_4|\le z)=\underbrace{\Phi(z)-\Phi(-z)}_{\footnotesize\text{confidence level}}=1-\alpha$

            > $\Longrightarrow$ &nbsp; $M_4$ is within $\varepsilon=z\,\mathrm{SE}(M_4)$ from $\mu$ with probability $1-\alpha=\underbrace{\Phi(z)-\Phi(-z)}_{\footnotesize 2\Phi(z)-1}$

            $$
            \Longrightarrow\quad\underbrace{1-\alpha}_{\footnotesize\text{found}}\text{ chance of }M_4\in\big[\mu-\underbrace{\varepsilon}_{\footnotesize\text{given}},\,\mu+\underbrace{\varepsilon}_{\footnotesize\text{given}}\big]
            $$

            <span class="lk-turn">$\leftrightsquigarrow$</span>

            $$
            \big[M_4-\underbrace{\varepsilon}_{\footnotesize\text{found}},\,M_4+\underbrace{\varepsilon}_{\footnotesize\text{found}}\big]\ni\mu\text{ with confidence level }\underbrace{1-\alpha}_{\footnotesize\text{given}}
            $$

            $\varepsilon=20$ &nbsp; $\Longrightarrow$ &nbsp; $1-\alpha=2\Phi(z)-1=2\Phi(2)-1\approx95.4\%$

            <span class="lk-ghost">$\varepsilon=20$ &nbsp;</span>$\Longrightarrow$ &nbsp; $95.4\%$ chance of $M_4\in[\mu-20,\mu+20]$

            <span class="lk-ghost">$\varepsilon=20$ &nbsp; $\Longrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; $M_4=56$ … is it close?

            <span class="lk-ghost">$\varepsilon=20$ &nbsp; $\Longrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; doesn't help us locate $\mu$ …
            """,
            lk.figure(interval("mu"), caption=r"$P\big(M_4\in[\mu-\varepsilon,\mu+\varepsilon]\big)=1-\alpha$"),
            lk.gap(),
            r"""
            $1-\alpha=95\%$ &nbsp; $\Longrightarrow$ &nbsp; $\varepsilon=\Phi^{-1}(1-\alpha/2)\,\mathrm{SE}(M_4)=10\,\Phi^{-1}(0.975)\approx19.6$

            <span class="lk-ghost">$1-\alpha=95\%$ &nbsp;</span>$\Longrightarrow$ &nbsp; $[M_4-19.6,M_4+19.6]\ni\mu$ with $95\%$ confidence

            <span class="lk-ghost">$1-\alpha=95\%$ &nbsp; $\Longrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; $M_4=56$ &nbsp; $\Longrightarrow$ &nbsp; $[36.4,75.6]\ni\mu$ at $95\%$ confidence level

            <span class="lk-ghost">$1-\alpha=95\%$ &nbsp; $\Longrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; gives us a range expected to contain $\mu$ at a desired level
            """,
            lk.interactive(
                interval("M4", m4=m4.value),
                controls=[m4],
                caption=r"$P\big([M_4-\varepsilon,M_4+\varepsilon]\ni\mu\big)=1-\alpha$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # remark: different data, different interval
    lk.remark(
        r"""
        For different sample data $X_i=x_i$ we have different sample mean $M_4=m_4$

        > $\Longrightarrow$ &nbsp; different interval $[m_4-\varepsilon,m_4+\varepsilon]$ at same confidence level $1-\alpha$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # definition: confidence interval
    lk.definition(
        r"""
        Given $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$,<br>a **confidence interval** for $\theta$ at level $1-\alpha$ is a pair of statistics

        $$
        L_n=\ell(X_1,\dots,X_n),\quad U_n=u(X_1,\dots,X_n)
        $$

        such that

        $$
        P(L_n\le\theta\le U_n)=1-\alpha
        $$
        """,
        label="def-ci",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # example: midterm scores, L_4 and U_4
    lk.example(
        r"""
        $X_1,\dots,X_4\sim\mathcal N(\mu,20^2)$

        > $\Longrightarrow$ &nbsp; $L_4=M_4-z\,\mathrm{SE}(M_4)$, &nbsp; $U_4=M_4+z\,\overbrace{\mathrm{SE}(M_4)}^{\footnotesize\sigma/\sqrt n=20/2=10}$

        > > where $\Phi(z)=1-\alpha/2$ &nbsp; $\leadsto$ &nbsp; $z=z_{1-\alpha/2}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # remark: known sigma, and the CLT
    lk.remark(
        r"""
        For $X_1,\dots,X_n\sim\mathcal N(\mu,\sigma^2)$ iid, with known $\sigma^2>0$,<br>we can find the error threshold $\varepsilon=z_{1-\alpha/2}\,\mathrm{SE}(M_n)$ since

        $$
        Z_n=\frac{M_n-\mu}{\sigma/\sqrt n}=\frac{M_n-\mu}{\mathrm{SE}(M_n)}\sim\mathcal N(0,1)
        $$

        In general, for non-normal $X$, we need the CLT!

        $$
        Z_n\longrightarrow Z\sim\mathcal N(0,1)\quad\text{for }n\to\infty
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # remark: unknown sigma
    lk.remark(
        [
            r"""
            $\varepsilon=z\,\mathrm{SE}(M_n)=z\,\sigma/\sqrt n$ depends explicitly on $\sigma$.

            If $\sigma$ is unknown, we cannot get $\varepsilon$ from
            """,
            lk.aside(
                r"$$P\big(|M_n-\mu|\le\varepsilon\big)=1-\alpha$$",
                r"even for $X\sim\mathcal N(\mu,\sigma^2)$",
            ),
            r"In this case, we must use $\underbrace{S_n^2}_{\footnotesize\text{consistent for }\sigma^2}$ instead of $\sigma^2$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: confidence intervals
    # theorem: large-sample confidence interval for the mean
    lk.theorem(
        r"""
        For any population $X$ with $E[X]=\mu$, $\mathrm{Var}(X)=\sigma^2>0$, both unknown, for large enough $n$,

        $$
        \left[M_n-z_{1-\alpha/2}\frac{S_n}{\sqrt n},\ M_n+z_{1-\alpha/2}\frac{S_n}{\sqrt n}\right]
        $$

        is an approximate confidence interval for $\mu$ at level $1-\alpha$

        $$
        P\left(M_n-z_{1-\alpha/2}\frac{S_n}{\sqrt n}\le\mu\le M_n+z_{1-\alpha/2}\frac{S_n}{\sqrt n}\right)\longrightarrow1-\alpha\quad\text{for }n\to\infty
        $$
        """,
        label="thm-large-sample",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: poll
    # example: poll, the confidence interval for p
    lk.example(
        [
        r"""
        $X=\begin{cases}
        1, & \text{if supports A}\\
        0, & \text{otherwise}
        \end{cases}$
        """,
        lk.aside(
            r"> $X_1,\dots,X_n\sim\mathrm{Binom}(1,p)$ iid with $\underbrace{\mu=\mk{p},\ \sigma^2=p(1-p)}_{\footnotesize\text{both unknown}}$",
            [(1.1, r"$p$ = fraction of all voters who support A")],
            rows=2,
        ),
        r"""
        > $\hat p=M_n$ &nbsp; (fraction of polled voters who support A)

        > $\hat p(1-\hat p)=\hat\sigma_n^2=\dfrac{n-1}{n}\,S_n^2$ &nbsp; (biased sample variance)

        > > $\Longrightarrow$ &nbsp; $\left[\hat p-z_{1-\alpha/2}\sqrt{\dfrac{\hat p(1-\hat p)}{n-1}},\ \hat p+z_{1-\alpha/2}\sqrt{\dfrac{\hat p(1-\hat p)}{n-1}}\right]\ni p$ &nbsp; at level $\approx1-\alpha$

        $n=1000$, with $540$ supporters

        > $\Longrightarrow$ &nbsp; $\hat p=0.54$, &nbsp; $\sqrt{\dfrac{\hat p(1-\hat p)}{n-1}}\approx0.0158$

        > > <span class="lk-tab" style="--lk-tab: 7em">$1-\alpha=95\%$</span>$\Longrightarrow$ &nbsp; <span class="lk-tab" style="--lk-tab: 7em">$z_{1-\alpha/2}\approx1.96$</span>$\Longrightarrow$ &nbsp; $\varepsilon\approx1.96\times0.0158\approx0.031$

        > > <span class="lk-tab" style="--lk-tab: 7em">$1-\alpha=99\%$</span>$\Longrightarrow$ &nbsp; <span class="lk-tab" style="--lk-tab: 7em">$z_{1-\alpha/2}\approx2.58$</span>$\Longrightarrow$ &nbsp; $\varepsilon\approx2.58\times0.0158\approx0.04$

        > > <span class="lk-tab" style="--lk-tab: 7em"></span>$\Longrightarrow$ &nbsp; <span class="lk-tab" style="--lk-tab: 14.5em">$[0.54-0.031,\,0.54+0.031]\ni p$</span>at level $0.95$

        > > <span class="lk-tab" style="--lk-tab: 7em"></span><span class="lk-ghost">$\Longrightarrow$ &nbsp;</span><span class="lk-tab" style="--lk-tab: 14.5em">$[0.54-0.04,\,0.54+0.04]\ni p$</span>at level $0.99$

        > $\leadsto$ &nbsp; we estimate $p$ to be $54\%$

        > > <span class="lk-tab" style="--lk-tab: 9.3em">with margin of error</span><span class="lk-tab" style="--lk-tab: 3.7em">$\pm3.1\%$</span>at $95\%$ confidence

        > > <span class="lk-tab" style="--lk-tab: 9.3em"></span><span class="lk-tab" style="--lk-tab: 3.7em">$\pm4\%$</span>at $99\%$ confidence
        """,
        ],
        title="poll",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: poll
    # consequence: confidence against error
    lk.prose(
        lk.aside(
            r"At same $n$: more confidence &nbsp; $\Longleftrightarrow$ &nbsp; more error",
            r"$z_{1-\alpha/2}$ grows with $1-\alpha$",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: poll
    # example: how many voters
    lk.example(
        r"""
        How many voters are needed for given margin $\varepsilon$ and confidence level $1-\alpha$?

        $\hat p=$ fraction of polled voters in support of A

        > $\Longrightarrow$ &nbsp; $0\le\hat p\le1$ &nbsp; $\Longrightarrow$ &nbsp; $\hat p(1-\hat p)\le\underbrace{1/4}_{\footnotesize\text{worst case scenario}}$

        > $\Longrightarrow$ &nbsp; $z_{1-\alpha/2}\sqrt{\dfrac{\hat p(1-\hat p)}{n-1}}\le z_{1-\alpha/2}\,\dfrac12\,\dfrac1{\sqrt{n-1}}\le\varepsilon$

        > $\Longleftarrow$ &nbsp; $n-1\ge\left(\dfrac{z_{1-\alpha/2}}{2\varepsilon}\right)^2$

        > > $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 10.6em">$\varepsilon=3.1\%$, $1-\alpha=95\%$</span>$\Longrightarrow$ &nbsp; $n-1\ge\left(\dfrac{1.96}{2\times0.031}\right)^2\approx999.4$

        > > $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 10.6em">$\varepsilon=1.55\%$, $1-\alpha=95\%$</span>$\Longrightarrow$ &nbsp; $n-1\ge\left(\dfrac{1.96}{2\times0.0155}\right)^2\approx3997.5$

        $\therefore$ &nbsp; to reduce the margin by factor $1/2$ at same confidence level we need 4 times more polled voters!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: other estimators
    # remark: what M_n had
    lk.remark(
        r"""
        We mainly considered $M_n$ which

        > 1\) &nbsp; is unbiased,

        > 2\) &nbsp; has simple standard error,

        > 3\) &nbsp; satisfies the CLT!

        For other statistics $\hat\theta_n$, we need

        > a) &nbsp; some asymptotic behavior as $n\to\infty$

        > b) &nbsp; some knowledge about bias and standard error
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: other estimators
    # definition: asymptotically normal
    lk.definition(
        [
            lk.aside(
                r"$\hat\theta_n$ is called **asymptotically <span class='lk-mark'>normal</span>** if $\forall z\in\mathbb R$",
                "or another distribution",
            ),
            lk.aside(
                r"""
                $$
                P\Bigg(\underbrace{\frac{\hat\theta_n-E[\hat\theta_n]}{\mathrm{SE}(\hat\theta_n)}}_{\footnotesize\text{standard score of }\hat\theta_n}<z\Bigg)\longrightarrow\mk{\Phi(z)}\quad\text{as }n\to\infty
                $$
                """,
                [(1.55, "or the other corresponding cdf")],
                rows=3,
            ),
        ],
        label="def-asymptotically-normal",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: other estimators
    # consequence: other asymptotic behaviors
    lk.prose(
        r"""
        $\leadsto$ &nbsp; other asymptotic behaviors give rise to different relations between<br>margins of error $\varepsilon=z\,\mathrm{SE}(\hat\theta_n)$ and confidence levels $1-\alpha=\Phi(z)-\Phi(-z)$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: other estimators
    # theorem: confidence interval from an asymptotically normal estimator
    lk.theorem(
        r"""
        If $\hat\theta_n$ is asymptotically normal, and the standard error and bias are known

        $$
        \mathrm{SE}(\hat\theta_n)=A_n\quad\text{and}\quad\mathrm{Bias}(\hat\theta_n)=B_n
        $$

        $$
        \Longrightarrow\quad\left[\hat\theta_n-B_n-z_{1-\alpha/2}A_n,\ \hat\theta_n-B_n+z_{1-\alpha/2}A_n\right]
        $$

        is an approximate confidence interval for $\theta$ at level $1-\alpha$ for sufficiently large $n$
        """,
        label="thm-asymptotic-ci",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: other estimators
    # remark: unknown SE and bias
    lk.remark(
        [
            r"If $\mathrm{SE}(\hat\theta_n)$ and $\mathrm{Bias}(\hat\theta_n)$ are unknown,",
            lk.aside(
                r"we <span class='lk-mark'>must find appropriate estimators</span> for $A_n$ and $B_n$",
                "these are not guaranteed to exist …",
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

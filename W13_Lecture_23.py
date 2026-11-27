import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 23 · p-values and t-tests", css_file="lecturekit/style.css")


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
    return Figure, lk, math, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(23, "p-values and t-tests")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    def _pdf(w, nu=None):
        if nu is None:
            return np.exp(-w**2 / 2) / np.sqrt(2 * np.pi)
        return math.gamma((nu + 1) / 2) / (math.sqrt(nu * math.pi) * math.gamma(nu / 2)) * (1 + w**2 / nu) ** (-(nu + 1) / 2)

    def _axes(fig, right):
        ax = fig.subplots()
        ax.axis("off")
        lk.arrow(ax, (-right - 0.2, 0), (right + 0.4, 0), "black", lw=1.0)
        lk.arrow(ax, (0, -0.01), (0, 0.46), "black", lw=1.0)
        ax.set_xlim(-right - 0.3, right + 0.5)
        ax.set_ylim(-0.14, 0.48)
        return ax

    def p_value_sketch(z=1.6):
        fig = Figure(figsize=(6.4, 2.9), layout="constrained")
        ax = _axes(fig, 3.9)
        x = np.linspace(-3.9, 3.9, 400)
        if z < 3.9:
            for a_, b_ in ((-3.9, -z), (z, 3.9)):
                w = np.linspace(a_, b_, 200)
                ax.fill_between(w, _pdf(w), color=lk.LIGHT, lw=0)
            for c in (-z, z):
                ax.plot([c, c], [0, _pdf(c)], color=lk.BLUE, lw=1.2)
                ax.text(c, -0.03, r"$-|z|$" if c < 0 else r"$|z|$", ha="center", va="top", fontsize=14)
        ax.plot(x, _pdf(x), color=lk.BLUE, lw=2)
        ax.text(-0.9, 0.36, r"$Z\sim\mathcal{N}(0,1)$", color=lk.BLUE, fontsize=14, ha="right")
        ax.text(2.9, 0.24, r"$\mathrm{total\ area}=p$", color=lk.BLUE, fontsize=14, ha="center", va="center")
        return fig

    def t_cdf(x, nu):
        w = np.linspace(0, x, 4001)
        f = _pdf(w, nu)
        return 0.5 + (f[1:] + f[:-1]).sum() * (w[1] - w[0]) / 2

    def t_quantile(p, nu):
        lo, hi = 0.0, 100.0
        for _ in range(50):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if t_cdf(mid, nu) < p else (lo, mid)
        return (lo + hi) / 2

    def t_sketch(n=2):
        fig = Figure(figsize=(6.4, 2.9), layout="constrained")
        ax = _axes(fig, 4.6)
        x = np.linspace(-4.6, 4.6, 500)
        ax.plot(x, _pdf(x), color=lk.BLUE, lw=2)
        ax.plot(x, _pdf(x, n), color=lk.RED, lw=2)
        ax.text(-1.0, 0.36, r"$\mathcal{N}(0,1)$", color=lk.BLUE, fontsize=14, ha="right")
        ax.text(3.0, _pdf(3.0, n) + 0.04, f"$t_{{{n}}}$", color=lk.RED, fontsize=14, ha="center")
        z, q = 1.959964, t_quantile(0.975, n)
        ax.plot([z, z], [0, _pdf(z)], color=lk.BLUE, lw=1.2, ls=(0, (4, 3)))
        ax.text(z, -0.03, r"$z_{0.975}$", color=lk.BLUE, ha="center", va="top", fontsize=13)
        y = -0.03 if q - z > 0.9 else -0.085
        if q < 4.5:
            ax.plot([q, q], [0, _pdf(q, n)], color=lk.RED, lw=1.2, ls=(0, (4, 3)))
            ax.text(q, y, f"$t_{{{n},0.975}}$", color=lk.RED, ha="center", va="top", fontsize=13)
        else:
            ax.annotate(f"$t_{{{n},0.975}}={q:.2f}$", (4.6, 0.005), xytext=(3.4, 0.17), color=lk.RED, ha="center", fontsize=13,
                        arrowprops={"arrowstyle": "-|>", "color": lk.RED, "lw": 1.0})
        return fig
    return p_value_sketch, t_quantile, t_sketch


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    z_abs = lk.slider(0, 3.5, step=0.05, value=2, label=r"$|z|$")
    t_df = lk.slider(1, 30, step=1, value=2, label=r"$k$")
    return t_df, z_abs


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Hypothesis testing

        $X\sim f_X(x;\theta)$ population, $\theta$ unknown

        $\leadsto$ &nbsp; hypothesis = statement about $\theta$
        """,
        lk.aside(r"> $\mk{H_0}=\text{“}\theta=\theta_0\text{”}$", "null-hypothesis"),
        lk.aside(r"> $\mk{H_1}=\text{“}\theta\neq\theta_0\text{”}$", "alternative hypothesis"),
        r"""
        $\leadsto$ &nbsp; test for $H_0$ against $H_1$

        > $\begin{cases}
        T=u(X_1,\dots,X_n) & \text{statistic},\\
        R\subseteq\mathbb R & \text{rejection region}
        \end{cases}$

        given data $X_1=x_1,\dots,X_n=x_n$

        > <span class="lk-tab" style="--lk-tab: 10.6em">$t=u(x_1,\dots,x_n)\in R$</span>$\Longrightarrow$ &nbsp; reject $H_0$

        > <span class="lk-tab" style="--lk-tab: 10.6em">$t=u(x_1,\dots,x_n)\notin R$</span>$\Longrightarrow$ &nbsp; do not reject $H_0$

        $\leadsto$ &nbsp; test design:
        """,
        r"> fix $\alpha$ significance level (tolerance level)",
        r"> choose the region $R_\alpha\subset\mathbb R$",
        lk.aside(r"> > - $\mk{P(T\in R_\alpha;\theta=\theta_0)}\le\alpha$", "probability of type I error"),
        lk.aside(r"> > - $\mk{P(T\in R_\alpha;\theta\neq\theta_0)}$ is as large as possible", "1 − probability of type II error"),
        lk.example(
            r"""
            $X\sim\mathrm{Binom}(1,p)$, $p$ unknown

            $H_0=\text{“}p=1/2\text{”}$, &nbsp; $H_1=\text{“}p\neq1/2\text{”}$

            > $\leadsto$ &nbsp; $Z=\dfrac{M_n-\overbrace{1/2}^{\mathclap{\footnotesize p\text{ under }H_0}}}{\underbrace{1/2}_{\mathclap{\footnotesize \text{standard deviation under }H_0}}/\sqrt n}$, &nbsp; $R_\alpha=\lbrace |z|\ge z_{1-\alpha/2}\rbrace$

            $n=100$, $60$ heads, $40$ tails &nbsp; $\Longrightarrow$ &nbsp; $M_n=0.6$

            > $\Longrightarrow$ &nbsp; $Z=2$ &nbsp; $\leadsto$ &nbsp; $2\in R_{5\%}=\lbrace |z|\ge1.96\rbrace$ &nbsp; $\Longrightarrow$ &nbsp; reject at $\alpha=5\%$

            > <span class="lk-ghost">$\Longrightarrow$ &nbsp; $Z=2$ &nbsp;</span>$\leadsto$ &nbsp; $2\notin R_{1\%}=\lbrace |z|\ge2.58\rbrace$ &nbsp; $\Longrightarrow$ &nbsp; do not reject at $\alpha=1\%$
            """,
            title="coin",
        ),
        lk.aside("What is the right <span class='lk-mark'>significance level</span>?", "somewhat arbitrary choice"),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        "p-values = measure of how strong the evidence is against $H_0$",
        lk.aside(r"<span class='lk-mark'>$t$-tests</span> = another type of hypothesis test", r"used when $E[X]$ and $\mathrm{Var}(X)$ are both unknown parameters"),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 7.2, 10.6, 10.8")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: p-value
    # section
    lk.section("p-values")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: p-value
    # lead-in
    lk.prose(r"""
    Instead of fixing the significance level $\alpha$, we ask: if $H_0$ is true, how surprising is a given observed value of $T$?

    $\leadsto$ &nbsp; very surprising = strong evidence against $H_0$
    """)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: p-value
    # definition: p-value
    lk.definition(
        r"""
        Given a test statistic $T=u(X_1,\dots,X_n)$ and rejection regions $R_\alpha$, for each $\alpha\in(0,1)$, define the **p-value** of a data set $X_1=x_1,\dots,X_n=x_n$ as

        $$
        p=\min\lbrace \alpha\in(0,1)\mid u(x_1,\dots,x_n)\in R_\alpha\rbrace.
        $$
        """,
        label="def-p-value",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: p-value
    # consequence
    lk.prose(
        lk.aside(r"$\leadsto$ &nbsp; a data set rejects $H_0$ at level $\alpha$ if and only if $\mk{p}\le\alpha$", r"$p$ computed from data!<br>$\Longrightarrow$ no choices involved!"),
        r"""
        $\leadsto$ &nbsp; data with small p-value reject $H_0$ even at small significance levels!

        > $\Longrightarrow$ &nbsp; strong evidence against $H_0$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk, math, p_value_sketch, z_abs):
    # module: p-value of the z-test
    # example: z-test for mu
    lk.example(
        [
            r"""
            a data set with $Z=z$ rejects $H_0$ at level $\alpha$

            > $\Longleftrightarrow$ &nbsp; $|z|\ge z_{1-\alpha/2}$

            > $\Longleftrightarrow$ &nbsp; $\Phi(|z|)\ge1-\alpha/2$

            > $\Longleftrightarrow$ &nbsp; $\alpha\ge2(1-\Phi(|z|))$
            """,
            lk.interactive(
                p_value_sketch(z_abs.value),
                controls=[z_abs],
            ),
            r"""
            > $\Longrightarrow$ &nbsp; $p=2(1-\Phi(|z|))=\underbrace{P(|Z|\ge|z|;\mu=\mu_0)}_{\mathrlap{\footnotesize\begin{gathered}\text{probability under } H_0 \text{ of observing data sets}\\ \text{with more extreme statistic}\end{gathered}}}$
            """,
        ],
        title=r"$z$-test for $\mu$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: p-value of the z-test
    # example: coin
    lk.example(
        r"""
        $n=100$, $60$ heads, $40$ tails

        > $\leadsto$ &nbsp; $z=2$ &nbsp; $\Longrightarrow$ &nbsp; $p=2(1-\Phi(2))\approx4.6\%$

        > <span class="lk-ghost">$\leadsto$ &nbsp; $z=2$ &nbsp;</span>$\Longrightarrow$ &nbsp; $\begin{cases}
        \text{reject “coin is fair” at }\alpha\ge4.6\%\\
        \text{do not reject at }\alpha<4.6\%
        \end{cases}$

        > <span class="lk-ghost">$\leadsto$ &nbsp; $z=2$ &nbsp;</span>$\Longrightarrow$ &nbsp; if the coin were fair, only $4.6\%$ of outcomes of $n=100$ coin flips<br>would give $|Z|\ge2$

        > <span class="lk-ghost">$\leadsto$ &nbsp; $z=2$ &nbsp;</span>$\Longrightarrow$ &nbsp; if the coin were fair, only $4.6\%$ of outcomes of $n=100$ coin flips<br>would speak against “coin is fair” as strongly as this outcome!

        > > <span class="lk-ghost">$\leadsto$ &nbsp; $z=2$ &nbsp;</span>$\leadsto$ &nbsp; our outcome is in the top $4.6\%$ against $H_0$
        """,
        title="coin",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: p-value of the z-test
    # remark: important!
    lk.remark(
        [
            r"The p-value of a data set is **not** the probability that $H_0$ is true!",
            lk.aside(
                r"$\leadsto$ &nbsp; $H_0$ is either true or false! This is unknown, <span class='lk-mark'>not random</span>!",
                r"there is no meaning to “probability of $H_0$ is true”!",
            ),
        ],
        title="important!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: t-distribution
    # section
    lk.section("t-tests")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: t-distribution
    # lead-in
    lk.prose(r"""
    $X$ with both $E[X]=\mu$ and $\mathrm{Var}(X)=\sigma^2$ unknown

    $H_0=\text{“}\mu=\mu_0\text{”}$ &nbsp; against &nbsp; $H_1=\text{“}\mu\neq\mu_0\text{”}$

    $\leadsto$ &nbsp; $\displaystyle Z=\frac{M_n-\mu_0}{\sigma/\sqrt n}$ &nbsp; depends on $\sigma$ and we have no hypothesis on $\sigma$…

    > $\Longrightarrow$ &nbsp; cannot use $Z$ as a test statistic…

    $\leadsto$ &nbsp; $\displaystyle T=\frac{M_n-\mu_0}{S_n/\sqrt n}$ &nbsp; obtained by replacing $\sigma^2$ by $S_n^2$
    """)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: t-distribution
    # theorem
    lk.theorem(
        [
            r"If $X_1,\dots,X_n\sim\mathcal N(\mu,\sigma^2)$ iid then",
            lk.aside(r"$$\mk{T_n}=\frac{M_n-\mu}{S_n/\sqrt n},$$", "Studentized mean"),
            lk.aside(
                r"has distribution $\mk{t_{n-1}}$ independent of $\mu$ and $\sigma^2$.",
                r"$t$-distribution with $n-1$ degrees of freedom",
            ),
        ],
        label="thm-studentized",
    )
    return


@app.cell(hide_code=True)
def _(lk, t_df, t_quantile, t_sketch):
    # module: t-distribution
    # consequence
    lk.prose(
        r"$\leadsto$ &nbsp; this has a tabulated cdf similar to the standard normal distribution",
        lk.interactive(
            t_sketch(t_df.value),
            controls=[t_df],
            readout=lk.table([(r"$t_{k,0.975}$", f"{t_quantile(0.975, t_df.value):.2f}"), (r"$z_{0.975}$", "1.96")]),
        ),
        r"$t_k$ has heavier tails than $\mathcal N(0,1)$ and $t_k\to\mathcal N(0,1)$ as $k\to+\infty$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: t-distribution
    # example: z vs t quantiles
    lk.example(
        r"""
        For $Z\sim\mathcal N(0,1)$ and $T\sim t_{n-1}$

        > $P(Z<z_{1-\alpha/2})=1-\alpha/2=P(T<t_{n-1,1-\alpha/2})$

        | $\alpha$ | $z_{1-\alpha/2}$ | $t_{29,1-\alpha/2}$ | $t_{9,1-\alpha/2}$ | $t_{4,1-\alpha/2}$ |
        |:--:|:--:|:--:|:--:|:--:|
        | $5\%$ | $1.96$ | $2.05$ | $2.26$ | $2.78$ |
        | $1\%$ | $2.58$ | $2.76$ | $3.25$ | $4.60$ |

        $\leadsto$ &nbsp; $t_{n-1,1-\alpha/2}>z_{1-\alpha/2}$

        $\leadsto$ &nbsp; $t_{n-1,1-\alpha/2}\to z_{1-\alpha/2}$ for $n\to\infty$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: t-test
    # example: t-test for mu
    lk.example(
        r"""
        $E[X]=\mu$ and $\mathrm{Var}(X)=\sigma^2$ unknown

        $H_0=\text{“}\mu=\mu_0\text{”}$ &nbsp; against &nbsp; $H_1=\text{“}\mu\neq\mu_0\text{”}$

        $T=\dfrac{M_n-\mu_0}{S_n/\sqrt n}$, &nbsp; $R_\alpha=\lbrace |t|\ge t_{n-1,1-\alpha/2}\rbrace$

        $\leadsto$ &nbsp; needs stronger evidence than the $z$-test in order to reject $H_0$

        $\leadsto$ &nbsp; doesn't need knowledge about $\sigma^2$
        """,
        title=r"$t$-test for $\mu$",
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
    # exercise: battery
    lk.exercise(
        r"""
        $X=$ lifetime of a battery (in hours) $\sim\mathcal N(\mu,\sigma^2)$

        we tested $n=16$ batteries and found

        $$
        M_{16}=38\qquad\text{and}\qquad S_{16}^2=(3.2)^2.
        $$

        a) test $H_0=\text{“}\mu=40\text{”}$ against $H_1=\text{“}\mu\neq40\text{”}$ at significance level $\alpha=5\%$

        b) find the p-value of the data set. Do you reject $H_0$ at $\alpha=1\%$?

        c) find a confidence interval for $\mu$ with confidence level $1-\alpha=95\%$

        **Hint:** $t_{15,0.975}=2.13$ for $\alpha=5\%$; &nbsp; $P(T<2.5)=0.988$ for $T\sim t_{15}$
        """,
        label="ex-battery",
    )
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 22 · Hypothesis testing", css_file="lecturekit/style.css")


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
    lk.lecture(22, "Hypothesis testing")
    return


@app.cell(hide_code=True)
def _(Figure, lk, np):
    def _pdf(w):
        return np.exp(-w**2 / 2) / np.sqrt(2 * np.pi)

    def power_sketch(z0=1.5, delta=0.5):
        # the density of Z - delta ~ N(0, 1); both tails beyond -z0 - delta and z0 - delta shaded: their area is K(mu)
        fig = Figure(figsize=(6.4, 2.9), layout="constrained")
        ax = fig.subplots()
        ax.axis("off")
        right = 3.9
        lk.arrow(ax, (-right - 0.2, 0), (right + 0.4, 0), "black", lw=1.0)
        lk.arrow(ax, (0, -0.01), (0, 0.46), "black", lw=1.0)
        ax.set_xlim(-right - 0.3, right + 0.5)
        ax.set_ylim(-0.14, 0.48)
        x = np.linspace(-right, right, 400)
        lo, hi = -z0 - delta, z0 - delta
        for a_, b_ in ((-right, lo), (hi, right)):
            if a_ < b_:
                w = np.linspace(a_, b_, 200)
                ax.fill_between(w, _pdf(w), color=lk.LIGHT, lw=0)
        close = hi - lo < 1.3
        for c, name, y in ((lo, r"$-z_0-\delta$", -0.03), (hi, r"$z_0-\delta$", -0.085 if close else -0.03)):
            if -right < c < right:
                ax.plot([c, c], [0, _pdf(c)], color=lk.BLUE, lw=1.2)
                ax.text(c, y, name, ha="center", va="top", fontsize=13)
        ax.plot(x, _pdf(x), color=lk.BLUE, lw=2)
        ax.text(-1.0, 0.36, r"$Z-\delta\sim\mathcal{N}(0,1)$", color=lk.BLUE, fontsize=14, ha="right")
        ax.text(2.9 if hi < right else -2.9, 0.24, r"$\mathrm{total\ area}=K(\mu)$", color=lk.BLUE, fontsize=14, ha="center", va="center")
        return fig
    return (power_sketch,)


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    z0_val = lk.slider(0, 3, step=0.05, value=1.5, label=r"$z_0$")
    delta_val = lk.slider(-2, 2, step=0.1, value=0.5, label=r"$\delta$")
    return delta_val, z0_val


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Estimators and confidence intervals

        $\leadsto$ &nbsp; <span class="lk-tab">how to make an informed guess about $\theta$?</span> $\hat\theta_n$

        $\leadsto$ &nbsp; <span class="lk-tab">how to determine a plausible range for $\theta$?</span> $[L_n,U_n]$
        """,
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        "Hypothesis testing",
        r"""
        $\leadsto$ &nbsp; how plausible is a given value of $\theta$?
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 10.1–10.4, 10.10")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypotheses
    # section
    lk.section("Hypothesis testing")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypotheses
    # definition: hypothesis
    lk.definition(
        [
            r"""
            Given a population $X$, a **hypothesis** about $X$ is any statement $H$ about some of its parameters.

            Usually, if $\theta$ is an unknown parameter and $\theta_0\in\mathbb R$ is a given value, we call
            """,
            lk.aside(
                r"$$H_0=\text{“}\theta=\theta_0\text{”}\qquad\mk{\rlap{\text{the null-hypothesis}}\hphantom{\text{the alternative hypothesis}}}$$",
                "the default claim",
            ),
            lk.aside(
                r"$$H_1=\text{“}\theta\neq\theta_0\text{”}\qquad\mk{\text{the alternative hypothesis}}$$",
                "usually the negative claim",
            ),
        ],
        label="def-hypothesis",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypotheses
    # example: coin
    lk.example(
        r"""
        $X=$ result of one coin toss $\sim\mathrm{Binom}(1,p)$ &nbsp; $\Longrightarrow$ &nbsp; $S_X=\lbrace 0,1\rbrace$

        Is the coin fair?

        > $\leadsto$ &nbsp; <span class="lk-tab" style="--lk-tab: 7.6em">$H_0=\text{“}p=1/2\text{”}$</span>$=$ “the coin is fair”

        > <span class="lk-ghost">$\leadsto$ &nbsp;</span><span class="lk-tab" style="--lk-tab: 7.6em">$H_1=\text{“}p\neq1/2\text{”}$</span>$=$ “the coin is not fair”
        """,
        title="coin",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypothesis test
    # definition: hypothesis test
    lk.definition(
        [
            r"A **hypothesis test** of $H_0$ against $H_1$ consists of",
            lk.aside(
                r"- a <span class='lk-mark'>**test statistic**</span> $T=u(X_1,\dots,X_n)$",
                r"to compare data with predictions<br>made under the assumption $H_0$ is true",
            ),
            lk.aside(
                r"- a <span class='lk-mark'>**rejection region**</span> $R\subseteq\mathbb R$",
                r"describing the values of $T$<br>that are unlikely under $H_0$",
            ),
        ],
        label="def-test",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypothesis test
    # consequence: reject or not
    lk.prose(
        r"Given data $X_1=x_1,\dots,X_n=x_n$ (evidence)",
        lk.aside(
            r"> we <span class='lk-mark'>reject $H_0$</span><span class='lk-ghost'> do not</span> if &nbsp; $T=t=u(x_1,\dots,x_n)\in R$",
            r"$T=t\in R$ is unlikely under $H_0$",
        ),
        r"""
        > > $\leadsto$ &nbsp; evidence against $H_0$

        > or
        """,
        lk.aside(
            r"> we <span class='lk-mark'>do not reject $H_0$</span> if &nbsp; $T=t=u(x_1,\dots,x_n)\notin R$",
            r"$T=t\notin R$ is likely under $H_0$, but<br>$T=t\notin R$ might also be likely under $H_1=H_0^c$",
        ),
        r"""
        > > $\leadsto$ &nbsp; evidence does not rule out $H_0$

        > > $\leadsto$ &nbsp; not the same as evidence in favor of $H_0$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: hypothesis test
    # example: presumption of innocence
    lk.example(
        [
            r"Criminal trial: &nbsp; $H_0=\text{“innocent”}$",
            lk.aside(
                r"<span class='lk-mark'>convicted</span> &nbsp; $\Longleftrightarrow$ &nbsp; sufficient evidence to reduce doubt beyond a reasonable level",
                r"$=$ reject $H_0$",
            ),
            r"<span class='lk-ghost'>convicted &nbsp; $\Longleftrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; $T\in R$",
            lk.aside(
                r"<span class='lk-mark'>$\mathrlap{\text{acquitted}}\hphantom{\text{convicted}}$</span> &nbsp; $\Longleftrightarrow$ &nbsp; insufficient evidence",
                r"$=$ do not reject $H_0$",
            ),
            r"<span class='lk-ghost'>convicted &nbsp; $\Longleftrightarrow$ &nbsp;</span>$\leadsto$ &nbsp; $T\notin R$",
        ],
        title="presumption of innocence",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: errors and power
    # definition: type I and type II errors
    lk.definition(
        [
            r"""
            A test can be wrong in two different ways

            - rejects $H_0$, but $H_0$ is true &nbsp; (**type I error**)
            """,
            lk.aside(r"> $\leadsto$ &nbsp; <span class='lk-mark'>convicted, but innocent</span>", "wrongful conviction"),
            r"- does not reject $H_0$, but $H_0$ is false &nbsp; (**type II error**)",
            lk.aside(r"> $\leadsto$ &nbsp; <span class='lk-mark'>acquitted, but guilty</span>", "wrongful acquittal"),
            r"$\leadsto$ &nbsp; we would like our test to minimize the probability of both types of error!",
        ],
        label="def-errors",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: errors and power
    # definition: power
    lk.definition(
        r"""
        The **power** of a test $(T,R)$ is the function

        $$
        K(\theta)=P(T\in R;\theta)
        $$

        measuring the probability of rejecting $H_0=\text{“}\theta=\theta_0\text{”}$.
        """,
        label="def-power",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: errors and power
    # remark
    lk.remark(
        [
            r"""
            <span class="lk-tab" style="--lk-tab: 4.6em">If $\theta=\theta_0$</span>$\Longrightarrow$ &nbsp; $K(\theta_0)=P(\text{type I error})$

            <span class="lk-tab" style="--lk-tab: 4.6em">If $\theta\neq\theta_0$</span>$\Longrightarrow$ &nbsp; $K(\theta)=1-P(\text{type II error};\theta)$

            $\leadsto$ &nbsp; ideally, we would like our test to have &nbsp; $K(\theta)=\begin{cases}
            0, & \theta=\theta_0\\
            1, & \theta\neq\theta_0
            \end{cases}$
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; not possible if $f_X(x;\theta)$ is <span class='lk-mark'>continuous in $\theta$</span>",
                "usually the case!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: test design
    # lead-in: strategy for test design
    lk.prose(
        "Strategy for test design:",
        lk.aside(
            r"> 1\. &nbsp; choose a test statistic $T=u(X_1,\dots,X_n)$",
            r"usually an appropriate<br>estimator for the parameter",
        ),
        lk.aside(
            r"> 2\. &nbsp; fix a <span class='lk-mark'>significance level</span> $\alpha$ for type I errors,",
            "tolerance level",
        ),
        r"> <span class='lk-ghost'>2\.&nbsp;&nbsp;&nbsp;</span>and choose a rejection region $R\subseteq\mathbb R$ such that",
        r"> > - $K(\theta_0)=P(T\in R;\theta=\theta_0)\le\alpha$",
        lk.aside(
            r"> > - $K(\theta)\hphantom{_0}=P(T\in R;\theta\neq\theta_0)$ is <span class='lk-mark'>the largest possible</span>",
            "at least amongst<br>regions of certain type",
        ),
    )
    return


@app.cell(hide_code=True)
def _(delta_val, lk, math, power_sketch, z0_val):
    # module: z-test
    # example: z-test for mu
    _z0, _d = z0_val.value, delta_val.value
    lk.example(
        [
            r"""
            $X\sim\mathcal N(\mu,\sigma^2)$ with known $\sigma^2>0$

            $H_0=\text{“}\mu=\mu_0\text{”}$, &nbsp; $H_1=\text{“}\mu\neq\mu_0\text{”}$

            1\. &nbsp; $\displaystyle Z=\frac{M_n-\mu_0}{\sigma/\sqrt n}$

            > $\Longrightarrow$ &nbsp; under $H_0$: &nbsp; $Z\sim\mathcal N(0,1)$

            > $\Longrightarrow$ &nbsp; under $H_1$: &nbsp; $Z\sim\mathcal N(\delta,1)$ &nbsp; with &nbsp; $\displaystyle\delta=\frac{\mu-\mu_0}{\sigma/\sqrt n}$
            """,
            lk.aside(
                r"2\. &nbsp; fix $\alpha\in(0,1)$, and regions &nbsp; $R=\underbrace{\lbrace |z|\ge z_0\rbrace}_{\mathclap{\footnotesize\text{symmetric around }z=0}}$",
                "choice of type of<br>rejection region",
            ),
            lk.gap(),
            r"""
            - if $\mu=\mu_0$
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                K(\mu_0)&=P(|Z|\ge z_0;\mu=\mu_0)\\
                &=1-\Phi(z_0)+\Phi(-z_0)=2(1-\Phi(z_0))\le\alpha\\
                &\Longleftrightarrow\quad z_0\ge \mk{z_{1-\alpha/2}}
                \end{aligned}
                $$
                """,
                r"$\Phi(z_{1-\alpha/2})=1-\alpha/2$",
                at="last",
            ),
            lk.gap(),
        r"- if $\mu\neq\mu_0$",
        lk.aside(
            r"""
            $$
            \begin{aligned}
            K(\mu)&=P(|Z|\ge z_0;\mu)\\
            &=1-P(-z_0-\delta<Z-\delta<z_0-\delta;\mu)\\
            &=1-\Phi(z_0-\delta)+\Phi(-z_0-\delta)
            \end{aligned}
            $$
            """,
            r"$\mu=\mu_0+\delta\sigma/\sqrt n$",
            at="middle",
        ),
        lk.interactive(
            power_sketch(_z0, _d),
            controls=[z0_val, delta_val],
        ),
        r"$\Longrightarrow$ &nbsp; $K(\mu)$ decreases with $z_0$",
        lk.aside(
            r"$\Longrightarrow$ &nbsp; $\displaystyle\left(Z=\frac{M_n-\mu_0}{\sigma/\sqrt n},\ R=\lbrace |z|\ge z_{1-\alpha/2}\rbrace\right)$<br>is the test with <span class='lk-mark'>largest power</span> at significance level $\alpha$",
            "with symmetric rejection region",
        ),
        ],
        title=r"$z$-test for $\mu$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: z-test
    # remark: X not normal
    lk.remark(
        [
            r"""
            If $X$ is not normal, $\mu=E[X]$ unknown and $\sigma^2=\mathrm{Var}(X)$ known

            > $\Longrightarrow$ &nbsp; $\left(Z=\dfrac{M_n-\mu_0}{\sigma/\sqrt n},\ R=\lbrace |z|\ge z_{1-\alpha/2}\rbrace\right)$ tests $H_0=\text{“}\mu=\mu_0\text{”}$ against $H_1=\text{“}\mu\neq\mu_0\text{”}$<br><span class="lk-ghost">$\Longrightarrow$ &nbsp;</span>with significance level $\approx\alpha$, if $n$ is sufficiently large.

            > $\leadsto$ &nbsp; $\sigma^2=\mathrm{Var}(X)$ unknown &nbsp; $\Longrightarrow$ &nbsp; $\displaystyle Z=\frac{M_n-\mu_0}{S_n/\sqrt n}$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: z-test
    # example: coin
    lk.example(
        r"""
        $n=100$, $60$ $\underbrace{\text{heads}}_{X=1}$, $40$ $\underbrace{\text{tails}}_{X=0}$ &nbsp; $\Longrightarrow$ &nbsp; $M_n=0.6$

        $\leadsto$ &nbsp; test $H_0=\text{“}p=1/2\text{”}$ with $\alpha=5\%$ and with $\alpha=1\%$

        > $\leadsto$ &nbsp; $Z=\dfrac{0.6-0.5}{\underbrace{0.5/10}_{\mathclap{\footnotesize\sigma^2=0.25\text{ under }H_0}}}=2$

        > $\leadsto$ &nbsp; $2\in R=\lbrace |z|\ge1.96\rbrace$ &nbsp; $\Longrightarrow$ &nbsp; we reject $H_0$ at $\alpha=5\%$

        > $\leadsto$ &nbsp; $2\notin R=\lbrace |z|\ge2.58\rbrace$ &nbsp; $\Longrightarrow$ &nbsp; we do not reject $H_0$ at $\alpha=1\%$
        """,
        title="coin",
    )
    return


if __name__ == "__main__":
    app.run()

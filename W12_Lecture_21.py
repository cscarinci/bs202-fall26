import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 21 · Methods of estimation", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return (lk,)


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(21, "Methods of estimation")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $\hat\theta_n$ asymptotically normal with known $\mathrm{SE}(\hat\theta_n)=A_n$ and $\mathrm{Bias}(\hat\theta_n)=B_n$

        > $\Longrightarrow$ &nbsp; $\left[\hat\theta_n-B_n-z_{1-\alpha/2}A_n,\ \hat\theta_n-B_n+z_{1-\alpha/2}A_n\right]$ is an approximate confidence interval for $\theta$ at level $1-\alpha$,<br><span class="lk-ghost">$\Longrightarrow$ &nbsp;</span>for sufficiently large $n$.

        If $A_n$ or $B_n$ unknown
        """,
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; we must <span class='lk-mark'>find appropriate estimators</span>!",
            "how?",
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
        Methods to construct estimators

        > $\leadsto$ &nbsp; maximum likelihood

        > $\leadsto$ &nbsp; method of moments
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 9.6, 9.7")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # section
    lk.section("Maximum likelihood estimators")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # example: poll, the data
    lk.example(
        [
            r"$X_1,\dots,X_5\sim\mathrm{Binom}(1,p)$ iid, $p$ unknown",
            lk.aside(r"> $\leadsto$ &nbsp; $(X_1,\dots,X_5)(o)=(0,1,1,0,1)$", "data"),
            lk.aside(r"> > $\hat p(o)=M_5(o)=3/5$", "estimate"),
            r"""
            > $\leadsto$ &nbsp; why is $3/5$ a better estimate than, say, $1/5$?

            > > $P(X_1=0,X_2=1,X_3=1,X_4=0,X_5=1)=p^3(1-p)^2$
            """,
            lk.aside(
                r"""
                > > | $p$ | $0$ | $1/5$ | $2/5$ | <span class='lk-mark'>$3/5$</span> | $4/5$ | $1$ |
                > > |:--:|:--:|:--:|:--:|:--:|:--:|:--:|
                > > | $p^3(1-p)^2$ | $0$ | $0.5\%$ | $2.3\%$ | <span class='lk-mark'>$3.5\%$</span> | $2.0\%$ | $0$ |
                """,
                "estimate which makes<br>the data most probable",
            ),
        ],
        title="poll",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # definition: likelihood
    lk.definition(
        [
            r"""
            Given $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$,<br>and given sample data $X_i=x_i\in\mathbb R$, the **likelihood** of $\theta$ is
            """,
            lk.aside(
                r"""
                $$
                \begin{aligned}
                L(\underbrace{\theta}_{\mathllap{\footnotesize\begin{matrix}\text{variable}\\\text{parameter}\end{matrix}\kern-1.2em}};\,\underbrace{x_1,\dots,x_n}_{\mathclap{\footnotesize\begin{matrix}\text{fixed}\\\text{data}\end{matrix}}})
                &=\underbrace{f_{X_1\dots X_n}(x_1,\dots,x_n;\theta)}_{\footnotesize\text{joint pmf / pdf}}\\[6pt]
                &=f_X(x_1;\theta)\cdots f_X(x_n;\theta)
                \end{aligned}
                $$
                """,
                "iid",
                at="last",
            ),
            r"""
            $$
            \begin{array}{c}
            \text{likelihood of }\theta\\
            \text{parameterized by}\\
            \text{the observed data}
            \end{array}
            \quad=\quad
            \begin{array}{c}
            \text{probability (density)}\\
            \text{of the observed data}\\
            \text{parameterized by }\theta
            \end{array}
            $$
            """,
        ],
        label="def-likelihood",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # definition: maximum likelihood estimator
    lk.definition(
        [
            r'''
            The **maximum likelihood estimator** of $\theta$ is a statistic

            $$
            \hat\theta_n^{\mathrm{MLE}}=u(X_1,\dots,X_n)
            $$
            ''',
            lk.aside(
                r"where <span class='lk-mark'>$u(x_1,\dots,x_n)$</span> is the value of $\theta$ which maximizes the likelihood function.",
                "maximum likelihood estimate for $\\theta$<br>(if it exists and is unique)",
            ),
        ],
        label="def-mle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # remark: log-likelihood
    lk.remark(
        [
            r"""
            Assuming $L(\theta;x_1,\dots,x_n)$ is strictly positive and sufficiently smooth in $\theta$,

            $$
            L(\theta;x_1,\dots,x_n)\quad\text{and}\quad\ell(\theta;x_1,\dots,x_n)=\ln\big(L(\theta;x_1,\dots,x_n)\big)
            $$

            have the same points of maxima and minima!
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $\displaystyle\ell(\theta;x_1,\dots,x_n)=\sum_{i=1}^n\ln\big(f_X(x_i;\theta)\big)$",
                "easier to maximize!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # recall: maximum of a function
    lk.recall(
        r"""
        Given $\ell:I\subseteq\mathbb R\longrightarrow\mathbb R$ $C^2$-smooth, find maximum by solving

        $$
        \ell'(\theta)=0,\quad\text{with}\quad\ell''(\theta)<0
        $$

        (or use boundary values of $\theta$)
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # example: poll, MLE
    lk.example(
        r"""
        $X_1,\dots,X_n\sim\mathrm{Binom}(1,p)$ iid, $p$ unknown

        > $\leadsto$ &nbsp; $L(p;x_1,\dots,x_n)=p^{\sum_{i=1}^n x_i}(1-p)^{n-\sum_{i=1}^n x_i}$

        > $\leadsto$ &nbsp; $\displaystyle\ell(p;x_1,\dots,x_n)=\ln(p)\sum_{i=1}^n x_i+\ln(1-p)\Big(n-\sum_{i=1}^n x_i\Big)$

        $$
        \begin{aligned}
        &\ell'(p)=\frac1p\sum_{i=1}^n x_i-\frac1{1-p}\Big(n-\sum_{i=1}^n x_i\Big)=0\\
        \Longleftrightarrow\quad&(1-p)\sum_{i=1}^n x_i-p\Big(n-\sum_{i=1}^n x_i\Big)=0\\
        \Longleftrightarrow\quad&p=\frac1n\sum_{i=1}^n x_i
        \end{aligned}
        $$

        $$
        \ell''(p)=-\frac1{p^2}\sum_{i=1}^n x_i-\frac1{(1-p)^2}\Big(n-\sum_{i=1}^n x_i\Big)<0,\quad\forall p\in(0,1)
        $$

        > $\Longrightarrow$ &nbsp; maximum likelihood estimator for $p$ is &nbsp; $\displaystyle\hat p_n^{\mathrm{MLE}}=\frac1n\sum_{i=1}^n X_i=M_n$

        If $n=5$ and $\displaystyle\sum_{i=1}^5 x_i=3$ &nbsp; $\Longrightarrow$ &nbsp; $\hat p_5^{\mathrm{MLE}}=3/5$
        """,
        title="poll",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # example: midterm, MLE
    lk.example(
        r"""
        $X\sim\mathcal N(\underbrace{\mu}_{\mathllap{\footnotesize\text{unknown}\kern-0.4em}},\underbrace{\sigma^2}_{\mathrlap{\kern-0.4em\footnotesize\text{known}}})$, $X_1=x_1,\dots,X_n=x_n$

        > $\leadsto$ &nbsp; $L(\mu;x_1,\dots,x_n)=\left(\dfrac1{\sqrt{2\pi}\,\sigma}\right)^n\exp\left(-\dfrac{\sum_{i=1}^n\left(\frac{x_i-\mu}{\sigma}\right)^2}{2}\right)$

        > $\leadsto$ &nbsp; $\displaystyle\ell(\mu;x_1,\dots,x_n)=-n\ln\big(\sqrt{2\pi}\,\sigma\big)-\frac12\sum_{i=1}^n\left(\frac{x_i-\mu}{\sigma}\right)^2$

        $$
        \begin{aligned}
        \ell'(\mu)&=\sum_{i=1}^n\frac{x_i-\mu}{\sigma^2}=0\quad\Longleftrightarrow\quad n\mu=\sum_{i=1}^n x_i\\
        \ell''(\mu)&=-\frac n{\sigma^2}<0\quad\forall\mu
        \end{aligned}
        $$

        > $\Longrightarrow$ &nbsp; <span class="lk-tab" style="--lk-tab: 17.5em">maximum likelihood estimate for $\mu$</span>$\displaystyle u(x_1,\dots,x_n)=\frac1n\sum_{i=1}^n x_i$

        > $\Longrightarrow$ &nbsp; <span class="lk-tab" style="--lk-tab: 17.5em">maximum likelihood estimator for $\mu$</span>$\displaystyle \hat\mu_n^{\mathrm{MLE}}=\frac1n\sum_{i=1}^n X_i=M_n$

        if $X_1=30$, $X_2=54$, $X_3=62$, $X_4=78$

        > $\Longrightarrow$ &nbsp; $\hat\mu_4^{\mathrm{MLE}}=56=\frac14(30+54+62+78)$

        > <span class="lk-ghost">$\Longrightarrow$ &nbsp;</span>has the largest likelihood amongst all values of $\mu$
        """,
        title="midterm",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: maximum likelihood
    # remark: least squares
    lk.remark(
        [
            r"Here maximizing $\ell(\mu)$ is the same as minimizing $\displaystyle\sum_{i=1}^n(x_i-\mu)^2$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $M_n$ is the <span class='lk-mark'>estimator with least squared errors</span>",
                "least squares estimator",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: method of moments
    # section
    lk.section("Method of moments estimators")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: method of moments
    # definition: method of moments estimator
    lk.definition(
        [
            r"""
            $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$

            The **method of moments estimator** for $\theta$ is a statistic

            $$
            \hat\theta_n^{\mathrm{MoM}}=u(X_1,\dots,X_n)
            $$

            where $u(x_1,\dots,x_n)$ is the value of $\theta$ which solves
            """,
            lk.aside(
                r"""
                $$
                \underbrace{E[X^k]}_{\mathclap{\footnotesize\text{function of }\theta}}
                =\underbrace{\frac1n\sum_{i=1}^n x_i^k}_{\mathclap{\footnotesize\text{determined by data}}}
                $$
                """,
                "one equation per unknown parameter<br>(usually the lowest $k$s that work)",
            ),
        ],
        label="def-mom",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: method of moments
    # example: poll, MoM
    lk.example(
        r"""
        $X\sim\mathrm{Binom}(1,p)$ &nbsp; $\leadsto$ &nbsp; $E[X]=p$

        > $\Longrightarrow$ &nbsp; $\displaystyle\hat p_n^{\mathrm{MoM}}=\frac1n\sum_{i=1}^n X_i=M_n$
        """,
        title="poll",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: method of moments
    # example: midterm, MoM
    lk.example(
        [
            r"$X\sim\mathcal N(\mu,\underbrace{\sigma^2}_{\mathclap{\footnotesize\text{also unknown}}})$ &nbsp; $\leadsto$ &nbsp; $E[X]=\mu$, $E[X^2]=\sigma^2+\mu^2$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\left\lbrace\begin{aligned}\hat\mu_n^{\mathrm{MoM}}&=\frac1n\sum_{i=1}^n X_i=M_n\\[2pt]\hat\sigma_n^{2\,\mathrm{MoM}}&=\frac1n\sum_{i=1}^n X_i^2-\big(\hat\mu_n^{\mathrm{MoM}}\big)^2=\hat\sigma_n^2\end{aligned}\right.$",
                "biased",
                at="last",
            ),
            r"$\leadsto$ &nbsp; same as MLE with no calculus!",
        ],
        title="midterm",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: method of moments
    # example: uniform, MoM against MLE
    lk.example(
        [
            r"""
            $X\sim\mathrm{Unif}(0,\theta)$, $\theta$ unknown

            > $\leadsto$ &nbsp; $\displaystyle f_X(x;\theta)=\frac1\theta,\quad x\in[0,\theta]$

            > > $\Longrightarrow$ &nbsp; $\displaystyle E[X]=\int_0^\theta x\,\frac1\theta\,dx=\frac{x^2}{2}\,\frac1\theta\,\bigg|_0^\theta=\frac\theta2$

            > > $\Longrightarrow$ &nbsp; $\dfrac{\hat\theta_n^{\mathrm{MoM}}}{2}=\displaystyle\frac1n\sum_{i=1}^n X_i$ &nbsp; $\Longrightarrow$ &nbsp; $\hat\theta_n^{\mathrm{MoM}}=2M_n$

            $X_1=1$, $X_2=1$, $X_3=2$, $X_4=6$ &nbsp; $\Longrightarrow$ &nbsp; $\hat\theta_4^{\mathrm{MoM}}=\overbrace{5}^{\mathclap{\footnotesize\text{estimate}}}<\underbrace{6}_{\mathclap{\footnotesize\text{observed}}}$

            > $\leadsto$ &nbsp; MoM estimates can sometimes be incoherent with the actual data!
            """,
            lk.gap(),
            r"""
            MLE: &nbsp; $L(\theta;x_1,\dots,x_n)=
            \begin{cases}
            \left({\large\tfrac{1}{\theta}}\right)^n & \text{if }\max(x_1,\dots,x_n)\in[0,\theta]\\[4pt]
            0 & \text{otherwise}
            \end{cases}$

            > $L'(\theta)=-n\theta^{-n-1}<0$ for $\theta>0$

            > > $\Longrightarrow$ &nbsp; $L(\theta)$ has maximum at the boundary

            > > $\Longrightarrow$ &nbsp; $\hat\theta_n^{\mathrm{MLE}}=\max(X_1,\dots,X_n)$
            """,
            lk.aside(
                r"if $X_1=1$, $X_2=1$, $X_3=2$, $X_4=6$ &nbsp; $\Longrightarrow$ &nbsp; $\hat\theta_4^{\mathrm{MLE}}=\mk{6}$",
                r"smallest $\theta$ which makes<br>the data possible!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: method of moments
    # remark: MLE and MoM
    lk.remark(
        r"""
        Many times MLE and MoM give the same estimator, but not always!

        > <span class="lk-tab" style="--lk-tab: 3.2em">MLE:</span>always coherent with the data and usually the most accurate, but requires calculus…

        > <span class="lk-tab" style="--lk-tab: 3.2em">MoM:</span>usually easier to compute, but sometimes incoherent with the data…
        """
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
    # exercise: Beta(theta, 1)
    lk.exercise(
        [
            lk.aside(
                r"Let $X_1,\dots,X_n\sim$ <span class='lk-mark'>$\mathrm{Beta}(\theta,1)$</span> iid, $\theta$ unknown",
                r"$f_X(x;\theta)=\theta x^{\theta-1}$, $x\in(0,1)$",
            ),
            r"""
            a) find the maximum likelihood estimator for $\theta$

            b) find the MoM estimator for $\theta$ (1st moment)

            c) compute both estimates for

            $$
            X_1=0.5,\quad X_2=0.5,\quad X_3=0.8,\quad X_4=0.2
            $$

            **Hint:** $\ln(0.04)\approx-3.22$
            """,
        ],
        label="ex-beta",
    )
    return


if __name__ == "__main__":
    app.run()

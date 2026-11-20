import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 20 · Confidence intervals", css_file="bs202.css")

@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False, "savefig.format": "svg"})

    return Figure, math, mo, np

@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#9a9a9a", "#e3ebf4"
    # Figure widths: HALF sits beside text or in a pair
    HALF = 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS202 &bull; {running}</div>
      <div class="bs-title">Introduction to Probability<br>and Mathematical Statistics</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>BS202a</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        The head is sized in points from the line width (length 4 lw, full width 2.5 lw), never in data units,
        so arrows look alike in every figure whatever its axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"-|>,head_length={4 * lw:g},head_width={1.25 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    return corollary, LIGHT, BLUE, GREEN, GREY, HALF, RED, arrow, definition, header, table, theorem

@app.cell(hide_code=True)
def _(header):
    header("Lecture 20","Week 12","Lecture 20 • Confidence intervals")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, arrow):
    # the sketches of pp. 2-3: [mu - eps, mu + eps] around mu, or [M_4 - eps, M_4 + eps] around M_4,
    # with eps = 19.6 and mu = 50; the interval is red when it misses mu
    def lecture_sketch(kind, value=56):
        fig = Figure(figsize=(6.6, 1.7))
        ax = fig.add_axes((0.07, 0.08, 0.85, 0.84))
        ax.axis("off")
        ax.set_xlim(-10, 110)
        ax.set_ylim(-0.6, 0.7)

        def label(p, text, color, offset):
            ax.annotate(text, p, xytext=offset, textcoords="offset points", color=color, fontsize=13, ha="center", va="bottom", zorder=10, clip_on=False)

        arrow(ax, (-5, 0), (105, 0), "black", lw=0.9)
        centre = 50 if kind == "fixed_interval" else value
        mean = 56 if kind == "fixed_interval" else value
        colour = RED if abs(centre - 50) > 19.6 else BLUE
        for x in (centre - 19.6, centre + 19.6):
            ax.plot([x, x], [-0.08, 0.08], color=colour, lw=1.4)
        ax.plot([centre - 19.6, centre + 19.6], [0, 0], color=colour, lw=2)
        ax.plot(mean, 0, "o", color=GREEN, zorder=5, ms=5)
        ax.plot(50, 0, "o", color=RED, zorder=5, ms=4)
        label((50, 0), r"$\mu$", RED, (0, -26))
        label((mean, 0), r"$M_4$", GREEN, (0, 16))
        name = r"\mu" if kind == "fixed_interval" else "M_4"
        for sign in (-1, 1):
            label((centre + sign * 19.6, 0), f"${name} {'-' if sign < 0 else '+'} \\varepsilon$", colour, (0, 16))
        return fig
    return (lecture_sketch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Estimators, bias, SE and MSE.

    $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$.

    $\hat\theta_n=u(X_1,\dots,X_n)$ &nbsp; estimator for $\theta$.

    $$
    \begin{aligned}
    \mathrm{Bias}(\hat\theta_n)&=E[\hat\theta_n-\theta]
    &&\text{expected error},\\
    \mathrm{SE}(\hat\theta_n)&=\sqrt{\mathrm{Var}(\hat\theta_n)}
    &&\text{typical error range for unbiased estimators},\\
    \mathrm{MSE}(\hat\theta_n)&=E[(\hat\theta_n-\theta)^2]
    &&\text{square of typical error range for any estimator}\\
    &=\mathrm{Bias}(\hat\theta_n)^2+\mathrm{SE}(\hat\theta_n)^2
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $\mathrm{Bias}(\hat\theta_n)\to0$ and $\mathrm{SE}(\hat\theta_n)\to0$ as $n\to\infty$

    $\qquad\Longleftrightarrow\quad$ $\mathrm{MSE}(\hat\theta_n)\to0$ as $n\to\infty$,

    then

    $$
    P(|\hat\theta_n-\theta|\ge\varepsilon)\longrightarrow0
    \quad\text{as }n\to\infty,\quad\forall\,\varepsilon>0
    $$
    """, "Consistent estimator")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; $\hat\theta_n$ has arbitrarily large probability of being arbitrarily close to $\theta$ for sufficiently large sample size $n$!

    $\leadsto$ &nbsp; $\hat\theta_n$ is a **consistent estimator** for $\theta$ &nbsp; $\leadsto$ &nbsp; a good estimator!

    **In this lecture:** for fixed $n$, how close and with what probability?

    $\leadsto$ &nbsp; confidence intervals for $\theta$.

    **References:** WMS 8.5–8.7

    ## V.2 &nbsp; Confidence intervals

    **Example.** Midterm scores $X\sim \mathcal{N}(\mu,20^2)$, $\mu$ unknown.

    $\leadsto$ &nbsp; given 4 scores $X_1=30$, $X_2=54$, $X_3=62$, $X_4=78$ &nbsp; $\Longrightarrow$ &nbsp; $M_4=56$.

    How close is $M_4$ to $\mu$? With what probability?

    $$
    M_4=\frac{X_1+X_2+X_3+X_4}{4}
    \sim \mathcal{N}\Bigl(\mu,\underbrace{\frac{20^2}{4}}_{\mathclap{\footnotesize 10^2=\mathrm{SE}(M_4)^2}}\Bigr)
    $$

    $$
    \Longrightarrow\quad Z_4=\frac{M_4-\mu}{\mathrm{SE}(M_4)}\sim \mathcal{N}(0,1)
    \qquad\text{(since }X\text{ is normal)}
    $$

    $$
    \begin{aligned}
    \Longrightarrow\quad P\bigl(|M_4-\mu|<\underbrace{z\,\mathrm{SE}(M_4)}_{\mathclap{\footnotesize \text{error threshold }\varepsilon}}\bigr)
    &=P(|Z_4|<z)\\[1.6em]
    &=\underbrace{\Phi(z)-\Phi(-z)}_{\mathclap{\footnotesize \text{confidence level}}}=1-\alpha
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; $M_4$ is within $\varepsilon=z\,\mathrm{SE}(M_4)$ of $\mu$ with probability

    $$
    1-\alpha=\Phi(z)-\Phi(-z)=2\Phi(z)-1
    $$

    $$
    \underbrace{1-\alpha}_{\mathclap{\footnotesize \text{found}}}\text{ chance of }
    M_4\in\underbrace{[\mu-\varepsilon,\mu+\varepsilon]}_{\mathclap{\footnotesize \text{given}}}
    $$

    $$
    \Updownarrow
    $$

    $$
    \underbrace{[M_4-\varepsilon,M_4+\varepsilon]}_{\mathclap{\footnotesize \text{found}}}
    \ni\mu\text{ with confidence level }\underbrace{1-\alpha}_{\mathclap{\footnotesize \text{given}}}
    $$

    $$
    \varepsilon=20\quad\Longrightarrow\quad
    1-\alpha=2\Phi(z)-1=2\Phi(2)-1\approx95.4\%
    $$

    $\Longrightarrow$ &nbsp; $95.4\%$ chance of $M_4\in[\mu-20,\mu+20]$.

    $M_4=56$ … is it close? Doesn't help us locate $\mu$…
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch("fixed_interval")
    mo.vstack([mo.hstack([_fig], justify="center"), mo.hstack([mo.md(r"$P(M_4\in[\mu-\varepsilon,\mu+\varepsilon])=1-\alpha$")], justify="center")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    1-\alpha=95\%\quad\Longrightarrow\quad
    \varepsilon=\Phi^{-1}(1-\alpha/2)\mathrm{SE}(M_4)
    =10\Phi^{-1}(0.975)\approx19.6
    $$

    $\Longrightarrow$ &nbsp; $[M_4-19.6,M_4+19.6]\ni\mu$ with $95\%$ confidence.

    $\leadsto$ &nbsp; $M_4=56$ &nbsp; $\Longrightarrow$ &nbsp; $[36.4,75.6]\ni\mu$ at $95\%$ confidence level.

    $\leadsto$ &nbsp; gives us a range expected to contain $\mu$ at a desired level.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sample_mean = mo.ui.slider(20,80,step=1,value=56,label=r"$M_4$",show_value=True)
    return (sample_mean,)


@app.cell(hide_code=True)
def _(lecture_sketch, mo, sample_mean):
    _fig = lecture_sketch("moving_interval", sample_mean.value)
    mo.vstack(
        [
            mo.hstack([sample_mean], justify="start", gap=2, wrap=True),
            mo.hstack([_fig], justify="center"),
            mo.hstack([mo.md(r"$P([M_4-\varepsilon,M_4+\varepsilon]\ni\mu)=1-\alpha$")], justify="center"),
            mo.md(r"Here $\mu=50$ (unknown in practice). In red: an interval that misses $\mu$."),
        ],
        gap=1,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** For different sample data $X_i=x_i$, we have different sample mean $M_4=m_4$.

    $\Longrightarrow$ &nbsp; different interval $[m_4-\varepsilon,m_4+\varepsilon]$ at the same confidence level $1-\alpha$.
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    Given $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$, a **confidence interval** for $\theta$ at level $1-\alpha$ is a pair of statistics

    $$
    L_n=\ell(X_1,\dots,X_n),\qquad U_n=u(X_1,\dots,X_n)
    $$

    such that

    $$
    P(L_n\le\theta\le U_n)=1-\alpha
    $$
    """, "Confidence interval")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** $X_1,\dots,X_4\sim \mathcal{N}(\mu,20^2)$,

    $$
    \Longrightarrow\quad L_4=M_4-z\,\mathrm{SE}(M_4),\qquad
    U_4=M_4+z\,\underbrace{\mathrm{SE}(M_4)}_{\mathclap{\footnotesize \sigma/\sqrt n=20/2=10}}
    $$

    where $\Phi(z)=1-\alpha/2$ &nbsp; $\leadsto$ &nbsp; $z=z_{1-\alpha/2}$.

    **Remark.** For $X_1,\dots,X_n\sim \mathcal{N}(\mu,\sigma^2)$ iid, with known $\sigma^2>0$, we can find the error threshold $\varepsilon=z_{1-\alpha/2}\mathrm{SE}(M_n)$ since

    $$
    Z_n=\frac{M_n-\mu}{\sigma/\sqrt n}
    =\frac{M_n-\mu}{\mathrm{SE}(M_n)}\sim \mathcal{N}(0,1)
    $$

    In general, for non-normal $X$, we need the CLT!

    $$
    Z_n\longrightarrow Z\sim \mathcal{N}(0,1)\qquad\text{as }n\to\infty
    $$

    **Remark.** $\varepsilon=z\,\mathrm{SE}(M_n)=z\sigma/\sqrt n$ depends explicitly on $\sigma$.

    If $\sigma$ is unknown, we cannot get $\varepsilon$ from

    $$
    P(|M_n-\mu|<\varepsilon)=1-\alpha
    \qquad\text{(even for }X\sim \mathcal{N}(\mu,\sigma^2)\text{)}
    $$

    In this case, we must use $S_n^2$ (consistent for $\sigma^2$) instead of $\sigma^2$!
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    For any population $X$ with $E[X]=\mu$, $\mathrm{Var}(X)=\sigma^2>0$, both unknown, for large enough $n$,

    $$
    \left[M_n-z_{1-\alpha/2}\frac{S_n}{\sqrt n},\ M_n+z_{1-\alpha/2}\frac{S_n}{\sqrt n}\right]
    $$

    is an approximate confidence interval for $\mu$ at level $1-\alpha$:

    $$
    P\left(M_n-z_{1-\alpha/2}\frac{S_n}{\sqrt n}\le\mu\le
    M_n+z_{1-\alpha/2}\frac{S_n}{\sqrt n}\right)\longrightarrow1-\alpha
    \quad\text{as }n\to\infty
    $$
    """, "Large-sample confidence interval for the mean")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example (poll).**

    $$
    X=\begin{cases}1&\text{if supports A},\\0&\text{otherwise}.
    \end{cases}
    $$

    $$
    X_1,\dots,X_n\sim\mathrm{Binom}(1,p)\text{ iid},\qquad
    \mu=\underbrace{p}_{\mathclap{\footnotesize \text{fraction of all voters who support A}}},\quad\sigma^2=p(1-p)
    $$

    both unknown.

    $$
    \hat p=M_n=\text{fraction of polled voters who support A}
    $$

    $$
    \hat p(1-\hat p)=\hat\sigma_n^2=\text{biased sample variance}
    =\frac{n-1}{n}S_n^2
    $$

    $$
    \Longrightarrow\quad
    \left[\hat p-z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n-1}},\
    \hat p+z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n-1}}\right]
    $$

    is a confidence interval for $p$ at level $\approx1-\alpha$.

    $n=1000$, with $540$ supporters:

    $$
    \Longrightarrow\quad\hat p=0.54,\qquad
    \sqrt{\frac{\hat p(1-\hat p)}{n-1}}\approx0.0158
    $$

    $$
    \begin{aligned}
    1-\alpha=95\%&\quad\Longrightarrow\quad z_{1-\alpha/2}\approx1.96
    \quad\Longrightarrow\quad\varepsilon\approx1.96\times0.0158\approx0.031,\\
    1-\alpha=99\%&\quad\Longrightarrow\quad z_{1-\alpha/2}\approx2.58
    \quad\Longrightarrow\quad\varepsilon\approx2.58\times0.0158\approx0.04
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; $[0.54-0.031,0.54+0.031]$ for $p$ at approximate level $0.95$,

    $[0.54-0.04,0.54+0.04]$ at approximate level $0.99$.

    $\leadsto$ &nbsp; we estimate $p$ to be $54\%$, with margin of error $\pm3.1$ percentage points at $95\%$ confidence ($\pm4$ at $99\%$).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At the same $n$: more confidence $\Longleftrightarrow$ larger margin of error.

    $z_{1-\alpha/2}$ grows with $1-\alpha$.

    **Example.** How many voters are needed for given margin $\varepsilon$ and confidence level $1-\alpha$?

    $\hat p=$ fraction of polled voters in support of A.

    $$
    \Longrightarrow\quad\hat p\le1\quad\Longrightarrow\quad\hat p(1-\hat p)\le\underbrace{1/4}_{\mathclap{\footnotesize \text{worst case scenario}}}
    $$

    $$
    \Longrightarrow\quad z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n-1}}
    \le z_{1-\alpha/2}\frac1{2\sqrt{n-1}}\le\varepsilon
    $$

    $$
    \Longleftrightarrow\quad n-1\ge\left(\frac{z_{1-\alpha/2}}{2\varepsilon}\right)^2
    $$

    $\leadsto$ &nbsp; $\varepsilon=3.1\%$, $1-\alpha=95\%$ &nbsp; $\Longrightarrow$ &nbsp; $n-1\ge\left(\dfrac{1.96}{2\times0.031}\right)^2\approx999.4$

    $\leadsto$ &nbsp; $\varepsilon=1.55\%$, $1-\alpha=95\%$ &nbsp; $\Longrightarrow$ &nbsp; $n-1\ge\left(\dfrac{1.96}{2\times0.0155}\right)^2\approx3997.5$

    $\therefore$ &nbsp; to reduce the margin by a factor $1/2$ at the same confidence level, we need about $4$ times as many polled voters!

    **Remark.** We mainly considered $M_n$, which

    1. is unbiased,
    2. has simple standard error,
    3. satisfies the CLT!

    For other statistics $\hat\theta_n$, we need

     a) some asymptotic behavior as $n\to\infty$,

     b) some knowledge about bias and standard error.
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    $\hat\theta_n$ is called **asymptotically normal** if, $\forall\,z\in\mathbb R$,

    $$
    P\Bigg(\underbrace{\frac{\hat\theta_n-E[\hat\theta_n]}{\mathrm{SE}(\hat\theta_n)}}_{\mathclap{\footnotesize \text{standard score of }\hat\theta_n}}<z\Bigg)
    \longrightarrow\Phi(z)\quad\text{as }n\to\infty
    $$
    """, "Asymptotically normal estimator")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Or another distribution, with its corresponding cdf.

    $\leadsto$ &nbsp; other asymptotic behaviors give rise to different relations between margins of error $\varepsilon=z\,\mathrm{SE}(\hat\theta_n)$ and confidence levels (in the normal case, $1-\alpha=\Phi(z)-\Phi(-z)$).
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $\hat\theta_n$ is asymptotically normal and the standard error and bias are known,

    $$
    \mathrm{SE}(\hat\theta_n)=A_n,\qquad\mathrm{Bias}(\hat\theta_n)=B_n
    $$

    then

    $$
    [\hat\theta_n-B_n-z_{1-\alpha/2}A_n,\ \hat\theta_n-B_n+z_{1-\alpha/2}A_n]
    $$

    is an approximate CI for $\theta$ at level $1-\alpha$ for sufficiently large $n$.
    """, "Confidence interval from an asymptotically normal estimator")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** If $\mathrm{SE}(\hat\theta_n)$ and $\mathrm{Bias}(\hat\theta_n)$ are unknown, we must find appropriate estimators for $A_n$ and $B_n$.

    $\leadsto$ &nbsp; these are not guaranteed to exist!
    """)
    return


if __name__ == "__main__":
    app.run()

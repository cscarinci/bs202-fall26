import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 22 · Hypothesis testing", css_file="bs202.css")

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
    header("Lecture 22","Week 13","Lecture 22 • Hypothesis testing")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, arrow, np):
    def power_sketch(z0=1.5, delta=0.5):
        fig = Figure(figsize=(6.4, 2.9), layout="constrained")
        ax = fig.subplots()
        ax.axis("off")
        pdf = lambda w: np.exp(-w**2 / 2) / np.sqrt(2 * np.pi)
        x = np.linspace(-3.9, 3.9, 400)
        lo, hi = -z0 - delta, z0 - delta
        if lo > -3.9:
            w = np.linspace(-3.9, lo, 200)
            ax.fill_between(w, pdf(w), facecolor=LIGHT, edgecolor=BLUE, hatch="////", lw=0)
        if hi < 3.9:
            w = np.linspace(hi, 3.9, 200)
            ax.fill_between(w, pdf(w), facecolor=LIGHT, edgecolor=BLUE, hatch="////", lw=0)
        for c, name, y in ((lo, r"$-z_0-\delta$", -0.03), (hi, r"$z_0-\delta$", -0.03 if hi - lo > 1.3 else -0.075)):
            if -3.9 < c < 3.9:
                ax.plot([c, c], [0, pdf(c)], color=BLUE, lw=1.2)
                ax.plot([c, c], [-0.012, 0.012], color="black", lw=1.0)
                ax.text(c, y, name, ha="center", va="top", fontsize=14)
        ax.plot(x, pdf(x), color=BLUE, lw=2)
        arrow(ax, (-4.1, 0), (4.3, 0), "black", lw=1.0)
        ax.text(-1.55, 0.33, r"$Z-\delta\sim\mathcal{N}(0,1)$", color=BLUE, fontsize=14, ha="right")
        if hi + lo < 0:
            tip, text_at = min(max(hi, -3.9) + 0.35, 3.6), (2.7, 0.25)
        else:
            tip, text_at = max(min(lo, 3.9) - 0.35, -3.6), (-2.9, 0.17)
        ax.annotate(r"$\mathrm{area}=K(\mu)$", (tip, pdf(tip) / 2), xytext=text_at, color=BLUE, fontsize=14, ha="center",
                    arrowprops={"arrowstyle": "-", "color": BLUE, "lw": 0.9})
        ax.set_xlim(-4.2, 4.4)
        ax.set_ylim(-0.1, 0.43)
        return fig
    return (power_sketch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## So far

    Estimators and confidence intervals

    $\leadsto$ &nbsp; how to make an informed guess about $\theta$? &nbsp; $\hat\theta_n$

    $\leadsto$ &nbsp; how to determine a plausible range for $\theta$? &nbsp; $[L_n,U_n]$

    **In this lecture:** hypothesis testing

    $\leadsto$ &nbsp; how plausible is a given value of $\theta$?

    $\leadsto$ &nbsp; a given statement about $\theta$

    **References:** WMS 10.1–10.4, 10.10

    ## VI.1 &nbsp; Hypothesis testing
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    Given a population $X$, a **hypothesis** about $X$ is any statement $H$ about some of its parameters.

    Usually, if $\theta$ is an unknown parameter and $\theta_0\in\mathbb R$ is a given value, we call

    $$
    \begin{aligned}
    H_0&=\text{“}\theta=\theta_0\text{”}
    &&\underbrace{\text{the null-hypothesis}}_{\mathclap{\footnotesize \text{the default claim}}}\\[18pt]
    H_1&=\text{“}\theta\neq\theta_0\text{”}
    &&\underbrace{\text{the alternative hypothesis}}_{\mathclap{\footnotesize \text{usually the negative claim}}}
    \end{aligned}
    $$
    """, "Hypothesis")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example (coin).** $X=$ result of one coin toss $\Longrightarrow$ $S_X=\lbrace 0,1\rbrace$.

    Is the coin fair?

    $$
    \leadsto\quad
    \begin{aligned}
    H_0&=\text{“}p=1/2\text{”} & H_1&=\text{“}p\neq1/2\text{”}\\
    &=\text{“the coin is fair”} & &=\text{“the coin is not fair”}
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    A **hypothesis test** of $H_0$ against $H_1$ consists of

    - a **test statistic** $T=u(X_1,\dots,X_n)$

        $\leadsto$ &nbsp; to compare data with predictions made under the assumption $H_0$ is true

    - a **rejection region** $R\subseteq\mathbb R$

        $\leadsto$ &nbsp; describing the values of $T$ that are unlikely under $H_0$
    """, "Hypothesis test")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Given data $X_1=x_1,\dots,X_n=x_n$ (evidence), we **reject** $H_0$ if

    $$
    T=t=u(x_1,\dots,x_n)\in R
    $$

    $\leadsto$ &nbsp; $T=t\in R$ is unlikely under $H_0$

    $\leadsto$ &nbsp; evidence against $H_0$

    or we **do not reject** $H_0$ if

    $$
    T=t=u(x_1,\dots,x_n)\notin R
    $$

    $\leadsto$ &nbsp; $T=t\notin R$ is likely under $H_0$

    $\leadsto$ &nbsp; but $T=t\notin R$ might also be likely under $H_1=H_0^c$

    $\leadsto$ &nbsp; evidence does not rule out $H_0$!

    $\leadsto$ &nbsp; not the same as evidence in favor of $H_0$!

    **Example (presumption of innocence).** Criminal trial: $H_0=\text{“innocent”}$.

    convicted (= reject $H_0$) &nbsp; $\Longleftrightarrow$ &nbsp; sufficient evidence to reduce doubt beyond a reasonable level &nbsp; $\leadsto$ &nbsp; $T\in R$

    acquitted (= do not reject $H_0$) &nbsp; $\Longleftrightarrow$ &nbsp; insufficient evidence &nbsp; $\leadsto$ &nbsp; $T\notin R$
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    A test can be wrong in two different ways:

    - rejects $H_0$, but $H_0$ is true &nbsp; (**type I error**)

        $\leadsto$ &nbsp; convicted, but innocent: wrongful conviction

    - does not reject $H_0$, but $H_0$ is false &nbsp; (**type II error**)

        $\leadsto$ &nbsp; acquitted, but guilty: wrongful acquittal

    $\leadsto$ &nbsp; we would like our test to minimize the probability of both types of error!
    """, "Type I and type II errors")
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    The **power** of a test $(T,R)$ is the function

    $$
    K(\theta)=P(T\in R;\theta)
    $$

    measuring the probability of rejecting $H_0=\text{“}\theta=\theta_0\text{”}$.
    """, "Power")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.**

    $$
    \begin{aligned}
    \text{If }\theta=\theta_0&\quad\Longrightarrow\quad K(\theta_0)=P(\text{type I error})\\
    \text{If }\theta\neq\theta_0&\quad\Longrightarrow\quad K(\theta)=1-P(\text{type II error};\theta)
    \end{aligned}
    $$

    $\leadsto$ &nbsp; ideally, we would like our test to have

    $$
    K(\theta)=
    \begin{cases}
    0, & \theta=\theta_0\\
    1, & \theta\neq\theta_0
    \end{cases}
    $$

    $\leadsto$ &nbsp; not possible if $f_X(x;\theta)$ is continuous in $\theta$

    $\leadsto$ &nbsp; usually the case!

    **Strategy for test design.**

    ① choose a test statistic

    $$
    T=u(X_1,\dots,X_n)
    $$

    $\leadsto$ &nbsp; usually an appropriate estimator for the parameter

    ② fix a **significance level** $\alpha$ (tolerance level) for type I errors, and choose a rejection region $R\subseteq\mathbb R$ such that

    $$
    K(\theta_0)=P(T\in R;\theta=\theta_0)\le\alpha
    $$

    $$
    K(\theta)=P(T\in R;\theta\neq\theta_0)
    $$

    is the largest possible

    $\leadsto$ &nbsp; at least amongst regions of a certain type

    **Example ($z$-test for $\mu$).** $X\sim\mathcal N(\mu,\sigma^2)$ with known $\sigma^2>0$.

    $$
    H_0=\text{“}\mu=\mu_0\text{”},\qquad H_1=\text{“}\mu\neq\mu_0\text{”}
    $$

    ① test statistic

    $$
    Z=\frac{M_n-\mu_0}{\sigma/\sqrt n}
    $$

    $$
    \begin{aligned}
    &\Longrightarrow\quad\text{under }H_0:\ Z\sim\mathcal N(0,1)\\
    &\Longrightarrow\quad\text{under }H_1:\ Z\sim\mathcal N(\delta,1)
    \quad\text{with }\delta=\frac{\mu-\mu_0}{\sigma/\sqrt n}
    \end{aligned}
    $$

    ② fix $\alpha\in(0,1)$, and regions

    $$
    R=\lbrace |z|\ge z_0\rbrace
    $$

    $\leadsto$ &nbsp; symmetric around $z=0$: choice of type of rejection region

    If $\mu=\mu_0$,

    $$
    \begin{aligned}
    K(\mu_0)&=P(|Z|\ge z_0;\mu=\mu_0)\\
    &=1-\Phi(z_0)+\Phi(-z_0)=2(1-\Phi(z_0))\le\alpha\\
    &\Longleftrightarrow\quad z_0\ge z_{1-\alpha/2}\qquad(\Phi(z_{1-\alpha/2})=1-\alpha/2)
    \end{aligned}
    $$

    If $\mu\neq\mu_0$ &nbsp; $(\mu=\mu_0+\delta\sigma/\sqrt n)$,

    $$
    \begin{aligned}
    K(\mu)&=P(|Z|\ge z_0;\mu)\\
    &=1-P(-z_0-\delta<Z-\delta<z_0-\delta;\mu)\\
    &=1-\Phi(z_0-\delta)+\Phi(-z_0-\delta)
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    z0_val = mo.ui.slider(0, 3, step=0.05, value=1.5, label=r"$z_0$", show_value=True)
    delta_val = mo.ui.slider(-2, 2, step=0.1, value=0.5, label=r"$\delta$", show_value=True)
    return delta_val, z0_val


@app.cell(hide_code=True)
def _(delta_val, math, mo, power_sketch, table, z0_val):
    _Phi = lambda w: 0.5 * (1 + math.erf(w / math.sqrt(2)))
    _z0, _d = z0_val.value, delta_val.value
    mo.vstack(
        [
            mo.hstack([z0_val, delta_val], justify="start", gap=2, wrap=True),
            table([(r"$K(\mu)=1-\Phi(z_0-\delta)+\Phi(-z_0-\delta)$", f"{100 * (1 - _Phi(_z0 - _d) + _Phi(-_z0 - _d)):.1f}%")]),
            mo.hstack([power_sketch(_z0, _d)], justify="center"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\Longrightarrow$ &nbsp; $K(\mu)$ decreases with $z_0$

    $$
    \Longrightarrow\quad\left(Z=\frac{M_n-\mu_0}{\sigma/\sqrt n},\ R=\lbrace |z|\ge z_{1-\alpha/2}\rbrace\right)
    $$

    is the test with largest power at significance level $\alpha$ (with symmetric rejection region).

    **Remark.** If $X$ is not normal, $\mu=E[X]$ unknown and $\sigma^2=\mathrm{Var}(X)$ known

    $$
    \Longrightarrow\quad\left(Z=\frac{M_n-\mu_0}{\sigma/\sqrt n},\ R=\lbrace |z|\ge z_{1-\alpha/2}\rbrace\right)
    $$

    tests $H_0=\text{“}\mu=\mu_0\text{”}$ against $H_1=\text{“}\mu\neq\mu_0\text{”}$ with significance level $\approx\alpha$, if $n$ is sufficiently large.

    If $\sigma^2$ is unknown, replace $Z$ by

    $$
    \frac{M_n-\mu_0}{S_n/\sqrt n}
    $$

    **Example (coin).**

    $$
    n=100,\quad 60\ \underbrace{\text{heads}}_{\mathclap{\footnotesize X=1}},\quad 40\ \underbrace{\text{tails}}_{\mathclap{\footnotesize X=0}}\quad\Longrightarrow\quad M_n=0.6
    $$

    $\leadsto$ &nbsp; test $H_0=\text{“}p=0.5\text{”}$ with $\alpha=5\%$ (or $1\%$)

    $$
    \leadsto\quad Z=\frac{0.6-0.5}{\underbrace{0.5/10}_{\mathclap{\footnotesize \sigma^2=0.25\text{ under }H_0}}}=2\in R=\lbrace |z|\ge1.96\rbrace
    $$

    For $\alpha=1\%$: &nbsp; $R=\lbrace |z|\ge2.58\rbrace$.

    $\Longrightarrow$ &nbsp; we reject $H_0$ at $\alpha=5\%$

    $\Longrightarrow$ &nbsp; we do not reject $H_0$ at $\alpha=1\%$!
    """)
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 23 · p-values and t-tests", css_file="bs202.css")

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
    header("Lecture 23","Week 13","Lecture 23 • p-values and t-tests")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, LIGHT, RED, math, np):
    def _pdf(w, nu=None):
        if nu is None:
            return np.exp(-w**2 / 2) / np.sqrt(2 * np.pi)
        return math.gamma((nu + 1) / 2) / (math.sqrt(nu * math.pi) * math.gamma(nu / 2)) * (1 + w**2 / nu) ** (-(nu + 1) / 2)

    def _axes(fig):
        ax = fig.subplots()
        ax.set_yticks([])
        ax.tick_params(labelsize=12)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        return ax

    # the sketch of p. 3: the pdf of Z ~ N(0, 1), with the tails beyond -|z| and |z| shaded (area = p); drawn with |z| = 1.5
    def p_value_sketch(z=1.5):
        fig = Figure(figsize=(5.6, 2.4), layout="constrained")
        ax = _axes(fig)
        x = np.linspace(-4, 4, 400)
        for a, b in ((-4, -z), (z, 4)):
            w = np.linspace(a, b, 200)
            ax.fill_between(w, _pdf(w), color=LIGHT, lw=0)
        for c in (-z, z):
            ax.plot([c, c], [0, _pdf(c)], color=BLUE, lw=1.0)
        ax.plot(x, _pdf(x), color=BLUE, lw=1.4)
        ax.annotate(r"area $=p$", (2.1, _pdf(2.1) / 2), xytext=(2.6, 0.17), color=BLUE, fontsize=12, ha="center", arrowprops={"arrowstyle": "-", "color": BLUE, "lw": 0.8})
        ax.set_xticks([-z, z], [r"$-|z|$", r"$|z|$"])
        ax.set_xlim(-4, 4)
        ax.set_ylim(0, 0.43)
        return fig

    # the sketch of p. 5: the pdfs of t_1, t_2 and N(0, 1)
    def t_sketch():
        fig = Figure(figsize=(5.6, 2.6), layout="constrained")
        ax = _axes(fig)
        x = np.linspace(-5, 5, 500)
        ax.plot(x, _pdf(x), color=GREY, lw=1.4)
        ax.plot(x, _pdf(x, 2), color=RED, lw=1.4)
        ax.plot(x, _pdf(x, 1), color=BLUE, lw=1.4)
        ax.text(1.75, 0.20, r"$\mathcal{N}(0,1)$", color=GREY, fontsize=12, ha="left")
        ax.text(2.6, 0.075, r"$t_2$", color=RED, fontsize=12, ha="left")
        ax.text(3.4, 0.040, r"$t_1$", color=BLUE, fontsize=12, ha="left")
        ax.set_xticks([])
        ax.set_xlim(-5, 5)
        ax.set_ylim(0, 0.43)
        return fig
    return p_value_sketch, t_sketch


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Hypothesis testing.

    $X\sim f_X(x;\theta)$ population, $\theta$ unknown.

    $\leadsto$ &nbsp; hypothesis = statement about $\theta$

    $$
    \begin{aligned}
    H_0&=\text{“}\theta=\theta_0\text{”}&&\text{null-hypothesis}\\
    H_1&=\text{“}\theta\neq\theta_0\text{”}&&\text{alternative hypothesis}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; test for $H_0$ against $H_1$

    $$
    =\begin{cases}
    T=u(X_1,\dots,X_n) & \text{statistic}\\
    R\subseteq\mathbb R & \text{rejection region}
    \end{cases}
    $$

    Given data $X_1=x_1,\dots,X_n=x_n$,

    $$
    \begin{aligned}
    t=u(x_1,\dots,x_n)\in R&\quad\Longrightarrow\quad\text{reject }H_0\\
    t=u(x_1,\dots,x_n)\notin R&\quad\Longrightarrow\quad\text{do not reject }H_0
    \end{aligned}
    $$

    $\leadsto$ &nbsp; test design: fix $\alpha$ significance level (tolerance level), choose the region $R_\alpha\subset\mathbb R$

    $$
    \begin{aligned}
    &\bullet\quad\underbrace{P(T\in R_\alpha;\theta=\theta_0)}_{\mathclap{\footnotesize \text{probability of type I error}}}\le\alpha\\[18pt]
    &\bullet\quad\underbrace{P(T\in R_\alpha;\theta\neq\theta_0)}_{\mathclap{\footnotesize 1-\text{probability of type II error}}}\ \text{is as large as possible}
    \end{aligned}
    $$

    **Example (coin).** $X\sim\mathrm{Binom}(1,p)$, $p$ unknown.

    $$
    H_0=\text{“}p=1/2\text{”},\qquad H_1=\text{“}p\neq1/2\text{”}
    $$

    $$
    \leadsto\quad
    Z=\frac{M_n-\overbrace{1/2}^{\mathclap{\footnotesize p\text{ under }H_0}}}{\underbrace{1/2}_{\mathclap{\footnotesize \text{std deviation under }H_0}}/\sqrt n},
    \qquad R_\alpha=\lbrace |z|\ge z_{1-\alpha/2}\rbrace
    $$

    $n=100$, $60$ heads, $40$ tails &nbsp; $\Longrightarrow$ &nbsp; $M_n=0.6$

    $$
    \Longrightarrow\quad Z=2\quad
    \begin{cases}
    2\in R_{5\%}=\lbrace |z|\ge1.96\rbrace & \Longrightarrow\quad\text{reject at }\alpha=5\%\\[4pt]
    2\notin R_{1\%}=\lbrace |z|\ge2.58\rbrace & \Longrightarrow\quad\text{do not reject at }\alpha=1\%
    \end{cases}
    $$

    What is the right significance level? &nbsp; <span class="nw">$\leadsto$ &nbsp; somewhat arbitrary choice</span>

    **In this lecture:**

    $\leadsto$ &nbsp; p-values = measure of how strong the evidence is against $H_0$

    $\leadsto$ &nbsp; $t$-tests = another type of hypothesis test &nbsp; <span class="nw">$\leadsto$ &nbsp; used when $E[X]$ and $\mathrm{Var}(X)$ are both unknown parameters</span>

    **References:** WMS 7.2, 10.6, 10.8

    ## VI.2 &nbsp; p-values and t-tests

    ### ① p-values

    Instead of fixing the significance level $\alpha$, we ask: if $H_0$ is true, how surprising is a given observed value of $T$?

    $\leadsto$ &nbsp; very surprising = strong evidence against $H_0$
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    Given a test statistic $T=u(X_1,\dots,X_n)$ and rejection regions $R_\alpha$, for each $\alpha\in(0,1)$, define the **p-value** of a data set $X_1=x_1,\dots,X_n=x_n$ as

    $$
    p=\min\lbrace \alpha\in(0,1)\mid u(x_1,\dots,x_n)\in R_\alpha\rbrace
    $$

    $\leadsto$ &nbsp; a data set rejects $H_0$ at level $\alpha$ if and only if

    $$
    \underbrace{p}_{\mathclap{\footnotesize \text{computed from data!}}}\le\alpha
    \quad\Longrightarrow\quad\text{no choices involved!}
    $$
    """, "p-value")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; data with small p-value reject $H_0$ even at small significance levels! &nbsp; $\Longrightarrow$ &nbsp; strong evidence against $H_0$!

    **Example ($z$-test for $\mu$).** A data set with $Z=z$ rejects $H_0$ at level $\alpha$

    $$
    \begin{aligned}
    &\Longleftrightarrow\quad|z|\ge z_{1-\alpha/2}\\
    &\Longleftrightarrow\quad\Phi(|z|)\ge1-\alpha/2\\
    &\Longleftrightarrow\quad\alpha\ge2(1-\Phi(|z|))
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo, p_value_sketch):
    mo.hstack([p_value_sketch()], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \Longrightarrow\quad p=2(1-\Phi(|z|))=
    \underbrace{P(|Z|\ge|z|;\mu=\mu_0)}_{\mathclap{\footnotesize \text{probability under } H_0 \text{ of observing data sets with at least as extreme statistic}}}
    $$

    <br>

    **Example (coin).** $n=100$, $60$ heads, $40$ tails.

    $$
    \leadsto\quad z=2\quad\Longrightarrow\quad p=2(1-\Phi(2))\approx4.6\%
    $$

    $$
    \Longrightarrow\quad
    \begin{cases}
    \text{reject “coin is fair” at }\alpha\ge4.6\%\\
    \text{do not reject at }\alpha<4.6\%
    \end{cases}
    $$

    $\Longrightarrow$ &nbsp; if the coin were fair only $4.6\%$ of outcomes of $n=100$ coin flips would give $|Z|\ge2$

    $\Longrightarrow$ &nbsp; if the coin were fair only $4.6\%$ of outcomes of $n=100$ coin flips would speak against “coin is fair” as strongly as this outcome!

    $\leadsto$ &nbsp; our outcome is in the top $4.6\%$ against $H_0$!

    **Remark (important!).** The p-value of a data set is **not** the probability that $H_0$ is true!

    $\leadsto$ &nbsp; $H_0$ is either true or false!

    $$
    \text{This is unknown, }\underbrace{\text{not random}}_{\mathclap{\footnotesize \text{there is no meaning to “probability of } H_0 \text{ is true”!}}}!
    $$

    <br>

    ### ② t-tests

    $X$ with both $E[X]=\mu$ and $\mathrm{Var}(X)=\sigma^2$ unknown.

    $$
    H_0=\text{“}\mu=\mu_0\text{”}\quad\text{vs}\quad H_1=\text{“}\mu\neq\mu_0\text{”}
    $$

    $\leadsto$ &nbsp; $\displaystyle Z=\frac{M_n-\mu_0}{\sigma/\sqrt n}$ depends on $\sigma$ and we have no hypothesis on $\sigma$… &nbsp; $\Longrightarrow$ &nbsp; cannot use $Z$ as a test statistic…

    $\leadsto$ &nbsp; $\displaystyle T=\frac{M_n-\mu_0}{S_n/\sqrt n}$ obtained by replacing $\sigma^2$ by $S_n^2$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $X_1,\dots,X_n\sim\mathcal N(\mu,\sigma^2)$ iid, then

    $$
    T_n=\frac{M_n-\mu}{S_n/\sqrt n}\qquad\text{(Studentized mean)}
    $$

    has distribution $t_{n-1}$ ($t$-distribution with $n-1$ degrees of freedom), independent of $\mu$ and $\sigma^2$.

    $\leadsto$ &nbsp; this has a tabulated cdf similar to the standard normal distribution
    """, "Studentized mean")
    return


@app.cell(hide_code=True)
def _(mo, t_sketch):
    mo.hstack([t_sketch()], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $t_n$ has heavier tails than $\mathcal N(0,1)$ and $t_n\to\mathcal N(0,1)$ as $n\to+\infty$.

    **Example.** For $Z\sim\mathcal N(0,1)$ and $T\sim t_{n-1}$,

    $$
    P(Z<z_{1-\alpha/2})=1-\alpha/2=P(T<t_{n-1,1-\alpha/2})
    $$

    | $\alpha$ | $z_{1-\alpha/2}$ | $t_{30-1,1-\alpha/2}$ | $t_{10-1,1-\alpha/2}$ | $t_{5-1,1-\alpha/2}$ |
    |:--:|:--:|:--:|:--:|:--:|
    | $5\%$ | $1.96$ | $2.05$ | $2.26$ | $2.78$ |
    | $1\%$ | $2.58$ | $2.76$ | $3.25$ | $4.60$ |

    $\leadsto$ &nbsp; $t_{n-1,1-\alpha/2}>z_{1-\alpha/2}$

    $\leadsto$ &nbsp; $t_{n-1,1-\alpha/2}\to z_{1-\alpha/2}$ for $n\to\infty$

    **Example ($t$-test for $\mu$).** $E[X]=\mu$ and $\mathrm{Var}(X)=\sigma^2$ unknown.

    $$
    H_0=\text{“}\mu=\mu_0\text{”}\quad\text{vs}\quad H_1=\text{“}\mu\neq\mu_0\text{”}
    $$

    $$
    T=\frac{M_n-\mu_0}{S_n/\sqrt n},\qquad R_\alpha=\lbrace |t|\ge t_{n-1,1-\alpha/2}\rbrace
    $$

    $\leadsto$ &nbsp; needs stronger evidence than the $z$-test in order to reject $H_0$

    $\leadsto$ &nbsp; doesn't need knowledge about $\sigma^2$!

    ### Practice

    $X=$ lifetime of a battery (in hours) $\sim\mathcal N(\mu,\sigma^2)$. We tested $n=16$ batteries and found

    $$
    M_{16}=38\qquad\text{and}\qquad S_{16}^2=(3.2)^2
    $$

     a) Test $H_0=\text{“}\mu=40\text{”}$ against $H_1=\text{“}\mu\neq40\text{”}$ at significance level $\alpha=5\%$.

     b) Find p-value of the data set. Do you reject $H_0$ at $\alpha=1\%$?

     c) Find a confidence interval for $\mu$ with confidence level $1-\alpha=95\%$.

    **Hint:** $t_{15,0.975}=2.13$ for $\alpha=5\%$; &nbsp; $P(T<2.5)=0.988$ for $T\sim t_{15}$.
    """)
    return


if __name__ == "__main__":
    app.run()

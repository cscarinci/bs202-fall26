import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 21 · Methods of estimation", css_file="bs202.css")

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
    header("Lecture 21","Week 12","Lecture 21 • Methods of estimation")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    $\hat\theta_n$ asymptotically normal with known $\mathrm{SE}(\hat\theta_n)=A_n$ and $\mathrm{Bias}(\hat\theta_n)=B_n$.

    $$
    \Longrightarrow\quad
    [\hat\theta_n-B_n-z_{1-\alpha/2}A_n,\ \hat\theta_n-B_n+z_{1-\alpha/2}A_n]
    $$

    is an approximate CI for $\theta$ at level $1-\alpha$, for large $n$.

    If $A_n$ or $B_n$ are unknown, we must find appropriate estimators! How?

    **In this lecture:** methods to construct estimators

    $\leadsto$ &nbsp; maximum likelihood

    $\leadsto$ &nbsp; method of moments.

    **References:** WMS 9.6, 9.7

    ## V.3 &nbsp; Methods of estimation

    ### ① Maximum likelihood estimators

    **Example (poll).** $X_1,\dots,X_5\sim\mathrm{Binom}(1,p)$ iid, $p$ unknown.

    $$
    \leadsto\quad(X_1,\dots,X_5)(o)=\underbrace{(0,1,1,0,1)}_{\mathclap{\footnotesize \text{data}}},
    \qquad\hat p(o)=M_5(o)=\underbrace{3/5}_{\mathclap{\footnotesize \text{estimate}}}
    $$

    Why is $3/5$ a better estimate than, say, $1/5$?

    $$
    P(X_1=0,X_2=1,X_3=1,X_4=0,X_5=1)=p^3(1-p)^2
    $$

    | $p$ | $0$ | $1/5$ | $2/5$ | $3/5$ | $4/5$ | $1$ |
    |:--:|:--:|:--:|:--:|:--:|:--:|:--:|
    | $p^3(1-p)^2$ | $0$ | $0.5\%$ | $2.3\%$ | $3.5\%$ | $2.0\%$ | $0$ |

    $\leadsto$ &nbsp; $3/5$: estimate which makes the data most probable.
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    Given $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$, and given sample data $X_i=x_i\in\mathbb R$, the **likelihood** of $\theta$ is

    $$
    \begin{aligned}
    L(\underbrace{\theta}_{\footnotesize \text{variable parameter}};\underbrace{x_1,\dots,x_n}_{\footnotesize \text{fixed data}})
    &=\underbrace{f_{X_1\dots X_n}(x_1,\dots,x_n;\theta)}_{\mathclap{\footnotesize \text{joint pmf / pdf}}}\\[14pt]
    &=f_X(x_1;\theta)\cdots f_X(x_n;\theta)\qquad\text{(iid)}
    \end{aligned}
    $$

    Likelihood of $\theta$ parametrized by the observed data = probability (density) of the observed data parametrized by $\theta$.
    """, "Likelihood")
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    The **maximum likelihood estimator** of $\theta$ is a statistic

    $$
    \hat\theta_n^{\mathrm{MLE}}=u(X_1,\dots,X_n)
    $$

    where $u(x_1,\dots,x_n)$ (maximum likelihood estimate for $\theta$) is a value of $\theta$ which maximizes the likelihood $L(\theta;x_1,\dots,x_n)$.
    """, "Maximum likelihood estimator")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** Assuming $L(\theta;x_1,\dots,x_n)$ is strictly positive and sufficiently smooth in $\theta$,

    $$
    L(\theta;x_1,\dots,x_n)\quad\text{and}\quad
    \ell(\theta;x_1,\dots,x_n)=\ln L(\theta;x_1,\dots,x_n)
    $$

    have the same points of maxima and minima!

    $$
    \leadsto\quad\ell(\theta;x_1,\dots,x_n)=\sum_{i=1}^n\ln f_X(x_i;\theta)
    \qquad\text{easier to maximize!}
    $$

    **Recall.** Given $\ell:I\subseteq\mathbb R\to\mathbb R$, $C^2$-smooth, find maximum by solving $\ell'(\theta)=0$, with $\ell''(\theta)<0$ (or use boundary values of $\theta$).

    **Example (poll).** $X_1,\dots,X_n\sim\mathrm{Binom}(1,p)$ iid, $p$ unknown.

    $$
    \leadsto\quad L(p;x_1,\dots,x_n)=p^{\sum_{i=1}^n x_i}(1-p)^{n-\sum_{i=1}^n x_i}
    $$

    For $0<p<1$,

    $$
    \leadsto\quad\ell(p;x_1,\dots,x_n)
    =\ln(p)\sum_{i=1}^n x_i+\ln(1-p)\left(n-\sum_{i=1}^n x_i\right)
    $$

    <span class="chain">$\displaystyle \ell'(p)=\frac1p\sum_{i=1}^n x_i-\frac1{1-p}\left(n-\sum_{i=1}^n x_i\right)=0$ $\displaystyle \Longleftrightarrow\quad(1-p)\sum_{i=1}^n x_i-p\left(n-\sum_{i=1}^n x_i\right)=0$ $\displaystyle \Longleftrightarrow\quad p=\frac1n\sum_{i=1}^n x_i$</span>

    $$
    \ell''(p)=-\frac1{p^2}\sum_{i=1}^n x_i
    -\frac1{(1-p)^2}\left(n-\sum_{i=1}^n x_i\right)<0,
    \qquad0<p<1
    $$

    $\Longrightarrow$ &nbsp; maximum likelihood estimator for $p$:

    $$
    \hat p_n^{\mathrm{MLE}}=\frac1n\sum_{i=1}^n X_i=M_n
    $$

    If $n=5$ and $\sum_{i=1}^5x_i=3$, then $\hat p_5^{\mathrm{MLE}}=3/5$.

    **Example (midterm).** $X\sim \mathcal{N}(\mu,\sigma^2)$, $\mu$ unknown, $\sigma^2>0$ known; $X_1=x_1,\dots,X_n=x_n$.

    $$
    \leadsto\quad L(\mu;x_1,\dots,x_n)
    =\left(\frac1{\sqrt{2\pi}\sigma}\right)^n
    \exp\left(-\frac12\sum_{i=1}^n\left(\frac{x_i-\mu}{\sigma}\right)^2\right)
    $$

    $$
    \leadsto\quad\ell(\mu;x_1,\dots,x_n)
    =-n\ln(\sqrt{2\pi}\sigma)-\frac12\sum_{i=1}^n\left(\frac{x_i-\mu}{\sigma}\right)^2
    $$

    $$
    \ell'(\mu)=\sum_{i=1}^n\frac{x_i-\mu}{\sigma^2}=0
    \quad\Longleftrightarrow\quad n\mu=\sum_{i=1}^n x_i
    $$

    $$
    \ell''(\mu)=-\frac n{\sigma^2}<0\qquad\forall\,\mu
    $$

    $\Longrightarrow$ &nbsp; maximum likelihood estimate for $\mu$:

    $$
    u(x_1,\dots,x_n)=\frac1n\sum_{i=1}^n x_i
    $$

    $\Longrightarrow$ &nbsp; maximum likelihood estimator for $\mu$:

    $$
    \hat\mu_n^{\mathrm{MLE}}=\frac1n\sum_{i=1}^n X_i=M_n
    $$

    If $X_1=30$, $X_2=54$, $X_3=62$, $X_4=78$,

    $$
    \Longrightarrow\quad\hat\mu_4^{\mathrm{MLE}}=56=\frac14(30+54+62+78)
    $$

    has the largest likelihood amongst all values of $\mu$.

    **Remark.** Here maximizing $\ell(\mu)$ is the same as minimizing $\sum_{i=1}^n(x_i-\mu)^2$.

    $\Longrightarrow$ &nbsp; $M_n$ is the estimator with least squared errors &nbsp; $\leadsto$ &nbsp; least squares estimator.

    ### ② Method of moments estimators
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    $X_1,\dots,X_n\sim f_X$ iid with unknown parameter $\theta$.

    The **method of moments estimator** for $\theta$ is a statistic $\hat\theta_n^{\mathrm{MoM}}=u(X_1,\dots,X_n)$, where $u(x_1,\dots,x_n)$ is a value of $\theta$ which solves

    $$
    \underbrace{E[X^k]}_{\footnotesize \text{function of }\theta}
    =\underbrace{\frac1n\sum_{i=1}^n x_i^k}_{\footnotesize \text{determined by data}}
    $$

    One equation per unknown parameter (lowest $k$'s that work).
    """, "Method of moments estimator")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example (poll).** $X\sim\mathrm{Binom}(1,p)$ &nbsp; $\leadsto$ &nbsp; $E[X]=p$.

    $$
    \Longrightarrow\quad\hat p_n^{\mathrm{MoM}}=\frac1n\sum_{i=1}^n X_i=M_n
    $$

    **Example (midterm).** $X\sim \mathcal{N}(\mu,\sigma^2)$, $\sigma^2$ also unknown.

    $$
    \leadsto\quad E[X]=\mu,\qquad E[X^2]=\sigma^2+\mu^2
    $$

    $$
    \Longrightarrow\quad
    \hat\mu_n^{\mathrm{MoM}}=\frac1n\sum_{i=1}^n X_i=M_n,
    \qquad
    \widehat{\sigma^2}_n^{\mathrm{MoM}}=\frac1n\sum_{i=1}^n X_i^2-(\hat\mu_n^{\mathrm{MoM}})^2
    =\hat\sigma_n^2\quad\text{(biased)}
    $$

    $\leadsto$ &nbsp; same as MLE with no calculus!

    **Example.** $X\sim\mathrm{Unif}(0,\theta)$, $\theta>0$ unknown.

    $$
    \leadsto\quad f_X(x;\theta)=\frac1\theta,\quad x\in[0,\theta]
    $$

    $$
    \Longrightarrow\quad E[X]=\int_0^\theta x\frac1\theta\,dx
    =\left[\frac{x^2}{2}\frac1\theta\right]_0^\theta=\frac\theta2
    $$

    $$
    \Longrightarrow\quad\frac{\hat\theta_n^{\mathrm{MoM}}}{2}=\frac1n\sum_{i=1}^n X_i
    \quad\Longrightarrow\quad\hat\theta_n^{\mathrm{MoM}}=2M_n
    $$

    $$
    X_1=1,\ X_2=1,\ X_3=2,\ X_4=6
    \quad\Longrightarrow\quad\hat\theta_4^{\mathrm{MoM}}=\underbrace{5}_{\footnotesize \text{estimate}}
    <\underbrace{6}_{\footnotesize \text{observed}}
    $$

    $\leadsto$ &nbsp; MoM estimates can sometimes be incoherent with the actual data!

    MLE:

    $$
    L(\theta;x_1,\dots,x_n)=
    \begin{cases}
    (1/\theta)^n&\text{if }\max(x_1,\dots,x_n)\in[0,\theta],\\
    0&\text{otherwise}
    \end{cases}
    $$

    For $\theta>\max_i x_i>0$,

    $$
    L'(\theta)=-n\theta^{-n-1}<0
    $$

    $\Longrightarrow$ &nbsp; $L(\theta)$ has its maximum at the boundary

    $$
    \Longrightarrow\quad\hat\theta_n^{\mathrm{MLE}}=\max(X_1,\dots,X_n)
    $$

    If $X_1=1$, $X_2=1$, $X_3=2$, $X_4=6$, then $\hat\theta_4^{\mathrm{MLE}}=6$.

    $\leadsto$ &nbsp; smallest $\theta$ which makes the data possible!

    **Remark.** Many times MLE and MoM give the same estimator, but not always!

    MLE: always coherent with the data and usually the most accurate, but requires calculus…

    MoM: usually easier to compute, but sometimes incoherent with the data…

    ### Practice

    Let $X_1,\dots,X_n\sim\operatorname{Beta}(\theta,1)$ iid, $\theta>0$ unknown.

    $$
    \leadsto\quad f_X(x;\theta)=\theta x^{\theta-1},\quad x\in(0,1)
    $$

     a) Find the MLE estimator for $\theta$.

     b) Find the MoM estimator for $\theta$ (1st moment).

     c) Compute both estimates for $X_1=0.5$, $X_2=0.5$, $X_3=0.8$, $X_4=0.2$.

    **Hint:** $\ln(0.04)\approx-3.22$.
    """)
    return


if __name__ == "__main__":
    app.run()

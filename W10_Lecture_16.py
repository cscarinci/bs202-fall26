import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 16 · Random samples and the law of large numbers", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math
    from fractions import Fraction

    import marimo as mo
    import matplotlib
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Figure, Fraction, math, mo


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

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

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        from matplotlib.figure import Figure as _Figure

        fig = _Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, RED, arrow, blank, corollary, definition, header, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 16", "Week 10", "Lecture 16 • Random samples and the law of large numbers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - joint expectation &nbsp; $E[u(X, Y)]$
    - covariance and correlation &nbsp; $\mathrm{Cov}(X, Y) = \sigma_{X,Y}$, &nbsp; $\rho_{X,Y} = \dfrac{\sigma_{X,Y}}{\sigma_X\, \sigma_Y}$
    - $X, Y$ **independent** measurements on the same experiment

        <span class="chain">$\displaystyle \leadsto \quad f_{X,Y}(x, y) = f_X(x)\, f_Y(y)$ $\displaystyle \quad \Longrightarrow \quad E[u(X)\, v(Y)] = E[u(X)]\, E[v(Y)]$ $\displaystyle \quad \Longrightarrow \quad \mathrm{Var}(aX + bY) = a^2\, \mathrm{Var}(X) + b^2\, \mathrm{Var}(Y)$</span>

    **In this lecture:** $n$ measurements of the same quantity across independent repetitions of an experiment &nbsp; <span class="nw">$\leadsto$ &nbsp; random</span> sample from a population &nbsp; <span class="nw">$\leadsto$ &nbsp; the</span> law of large numbers

    **References:** WMS 5.8, 6.5, 7.1
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## IV.3 &nbsp; Random samples and the law of large numbers

    ### Independent and identically distributed random variables
    """
            ),
            definition(
                r"""
    A collection of $n$ random variables $X_1, \dots, X_n : S \longrightarrow \mathbb{R}$ on $(S, \mathcal{E}, P)$ is called

    - **independent** if
        $$
        f_{X_1, \dots, X_n}(x_1, \dots, x_n) = f_{X_1}(x_1) \cdots f_{X_n}(x_n)
        $$
    - **identically distributed** if
        $$
        f_{X_i}(x) = f_{X_j}(x) \qquad \forall\, i, j
        $$
    """,
                "Independent and identically distributed random variables",
            ),
            mo.md(
                r"""
    For $X_1, \dots, X_n$ independent and identically distributed, with $f_{X_i} = f$, we write &nbsp; $\boldsymbol{X_1, \dots, X_n \sim f}$ **iid**.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(corollary, mo, theorem):
    mo.vstack(
        gap=1.5,
        items=[
            theorem(
                r"""
    Given $X_1, \dots, X_n : S \longrightarrow \mathbb{R}$ and $a_1, \dots, a_n \in \mathbb{R}$

    - $E[a_1 X_1 + \dots + a_n X_n] = a_1 E[X_1] + \dots + a_n E[X_n]$

    If $X_1, \dots, X_n$ are independent, then

    - $E[u_1(X_1) \cdots u_n(X_n)] = E[u_1(X_1)] \cdots E[u_n(X_n)]$
    - $\mathrm{Var}(a_1 X_1 + \dots + a_n X_n) = a_1^2\, \mathrm{Var}(X_1) + \dots + a_n^2\, \mathrm{Var}(X_n)$
    - $m_{X_1 + \dots + X_n}(t) = m_{X_1}(t) \cdots m_{X_n}(t)$
    """,
                "Sums and products of random variables",
            ),
            mo.md(
                r"""
    **Proof** (for the mgf).

    $$
    E\big[e^{t(X_1 + \dots + X_n)}\big] = E\big[e^{tX_1} \cdots e^{tX_n}\big] = E\big[e^{tX_1}\big] \cdots E\big[e^{tX_n}\big] \tag*{$\square$}
    $$
    """
            ),
            theorem(
                r"""
    $X_1, \dots, X_n$ are identically distributed if and only if $m_{X_1}(t) = \dots = m_{X_n}(t)$ near $t = 0$.
    """,
                "Identically distributed if and only if the same mgf",
            ),
            corollary(
                r"""
    If $X_1, \dots, X_n \sim f$ iid with mgf $m(t)$, then

    $$
    m_{X_1 + \dots + X_n}(t) = \big(m(t)\big)^n
    $$
    """,
                "Mgf of a sum of iid random variables",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Example** (Customers arrive independently following $\mathrm{Pois}(\lambda)$).

    - $Y_i$ = time of arrival of the $i$th customer
    - $X_i$ = waiting time between the $(i-1)$th and the $i$th customer &nbsp; <span class="nw">$\leadsto$ &nbsp; with</span> $X_1 = Y_1$

    $$
    \Longrightarrow \qquad X_1, \dots, X_n \sim \mathrm{Exp}(\lambda) \text{ iid}, \qquad Y_i \sim \mathrm{Gamma}(i, \lambda)
    $$

    and &nbsp; $X_1 + \dots + X_n = Y_n$

    <span class="chain">$\displaystyle \Longrightarrow \qquad m_{X_1 + \dots + X_n}(t) = \big(\text{mgf of } \mathrm{Exp}(\lambda)\big)^n = \left(\frac{\lambda}{\lambda - t}\right)^n$ $\displaystyle = \text{mgf of } \mathrm{Gamma}(n, \lambda) = m_{Y_n}(t)$</span>

    $$
    \therefore \quad X_1, \dots, X_n \sim \mathrm{Exp}(\lambda) \text{ iid} \ \Longrightarrow \ X_1 + \dots + X_n \sim \mathrm{Gamma}(n, \lambda) \ !
    $$
    """
            ),
            theorem(
                r"""
    Similarly

    $$
    \begin{aligned}
    X_1, \dots, X_n \sim \mathrm{Binom}(1, p) \text{ iid} \ &\Longrightarrow \ X_1 + \dots + X_n \sim \mathrm{Binom}(n, p) \\
    &\phantom{\Longrightarrow} \ \ (\text{also for } \mathrm{NBinom}) \\[8pt]
    X_1, \dots, X_n \sim \mathrm{Pois}(\lambda) \text{ iid} \ &\Longrightarrow \ X_1 + \dots + X_n \sim \mathrm{Pois}(n\lambda) \\[8pt]
    X_1, \dots, X_n \sim \mathcal{N}(\mu, \sigma^2) \text{ iid} \ &\Longrightarrow \ X_1 + \dots + X_n \sim \mathcal{N}(n\mu, n\sigma^2)
    \end{aligned}
    $$
    """,
                "Sums of iid binomial, Poisson and normal random variables",
            ),
            mo.md(
                r"""
    **Remark.** So far, $X_1, \dots, X_n$ are **different measurements** on a single random experiment $(S, \mathcal{E}, P)$ &nbsp; <span class="nw">$\leadsto$ &nbsp; identically</span> distributed does not mean same measurement

    Now, we want to consider the same measurement on independent repetitions of the experiment.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Random samples"""),
            definition(
                r"""
    Given a random variable $X : S \longrightarrow \mathbb{R}$, a **random sample** from the population $X$ is a collection of random variables

    $$
    X_1, \dots, X_n : S^n \longrightarrow \mathbb{R}
    $$

    on $S^n = S \times \dots \times S$ ($n$ independent repetitions: $P(A_1 \times \dots \times A_n) = P(A_1) \cdots P(A_n)$), with $X_i(o_1, \dots, o_n) = X(o_i)$ (the measurement of $X$ on the $i$th repetition)
    """,
                "Random sample",
            ),
            mo.md(
                r"""
    $$
    \Longrightarrow \qquad X_1, \dots, X_n \sim f_X \text{ iid} \ !
    $$
    """
            ),
            definition(
                r"""
    A **statistic** about $X : S \longrightarrow \mathbb{R}$ is a function $u(X_1, \dots, X_n)$ of a random sample from $X$, which summarizes information about the sample.

    - $\leadsto$ &nbsp; $T = u(X_1, \dots, X_n) : S^n \longrightarrow \mathbb{R}$ is also a random variable on $S^n$
    - $\leadsto$ &nbsp; $f_T : \mathbb{R} \longrightarrow \mathbb{R}$ is called a **sampling distribution**

        $\leadsto$ &nbsp; used to infer properties of a population $X$ from observed data &nbsp; $X_1 = x_1, \dots, X_n = x_n$
    """,
                "Statistic and sampling distribution",
            ),
            mo.md(
                r"""
    **Example** (Special statistics).

    $$
    \begin{aligned}
    M_n &= \frac{X_1 + \dots + X_n}{n} = \frac{1}{n} \sum_{i=1}^{n} X_i && \text{sample mean} \\[10pt]
    S_n^2 &= \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - M_n)^2 && \text{sample variance} \\[10pt]
    G_n &= \frac{1}{n} \sum_{i=1}^{n} \left( \frac{X_i - M_n}{S_n} \right)^3 && \text{sample skewness}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example** (Roll a fair die). &nbsp; $S = \{1, 2, 3, 4, 5, 6\}$

    $$
    X : S \longrightarrow \mathbb{R}, \qquad X(k) = \begin{cases} 1, & k = 6 \\ 0, & k \neq 6 \end{cases}
    $$

    fair &nbsp; <span class="nw">$\leadsto$ &nbsp; $P(\{k\}) = \dfrac{1}{6}$</span> &nbsp; <span class="nw">$\forall\, k \in S$ &nbsp; $\Longrightarrow$</span>

    <span class="chain">$\displaystyle f_X(x) = P(X = x) = \begin{cases} \dfrac{1}{6}, & x = 1 \\[8pt] \dfrac{5}{6}, & x = 0 \end{cases}$ $\displaystyle = \binom{1}{x} \left(\frac{1}{6}\right)^x \left(\frac{5}{6}\right)^{1 - x} = \mathrm{Binom}(1, 1/6)(x)$</span>

    Roll a fair die twice (independently): &nbsp; $X_1, X_2 : S \times S \longrightarrow \mathbb{R}$

    $$
    \begin{aligned}
    X_1(k_1, k_2) &= X(k_1) = \begin{cases} 1, & k_1 = 6 \\ 0, & k_1 \neq 6 \end{cases} \\[8pt]
    X_2(k_1, k_2) &= X(k_2) = \begin{cases} 1, & k_2 = 6 \\ 0, & k_2 \neq 6 \end{cases}
    \end{aligned}
    $$

    fair, independent &nbsp; <span class="nw">$\leadsto$ &nbsp; $P(\{(k_1, k_2)\}) = \dfrac{1}{36} = P(\{k_1\})\, P(\{k_2\})$</span>

    <span class="chain">$\displaystyle \Longrightarrow \qquad f_{X_1}(x) = P(X_1 = x) = \mathrm{Binom}(1, 1/6)(x),$ $\displaystyle \quad f_{X_2}(x) = P(X_2 = x) = \mathrm{Binom}(1, 1/6)(x)$</span>

    $\leadsto$ &nbsp; $X_1, X_2 \sim \mathrm{Binom}(1, 1/6)$ iid

    $T = X_1 + X_2 : S \times S \longrightarrow \mathbb{R}$

    $$
    T(k_1, k_2) = X(k_1) + X(k_2) = \begin{cases} 2, & k_1 = 6,\ k_2 = 6 \\ 1, & k_1 = 6,\ k_2 \neq 6 \ \text{ or } \ k_1 \neq 6,\ k_2 = 6 \\ 0, & k_1 \neq 6,\ k_2 \neq 6 \end{cases}
    $$

    $$
    \Longrightarrow \qquad f_T(2) = \frac{1}{36}, \qquad f_T(1) = \frac{10}{36}, \qquad f_T(0) = \frac{25}{36}
    $$

    $\leadsto$ &nbsp; $T \sim \mathrm{Binom}(2, 1/6)$
    """)
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### The sample mean and the law of large numbers"""),
            theorem(
                r"""
    Given a random sample $X_1, \dots, X_n$ from a population $X$ with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2$

    $$
    \begin{aligned}
    E[M_n] &= E\left[\frac{1}{n}(X_1 + \dots + X_n)\right] = \frac{1}{n}\, n\mu = \mu \\[6pt]
    \mathrm{Var}(M_n) &= \mathrm{Var}\left(\frac{1}{n}(X_1 + \dots + X_n)\right) = \frac{1}{n^2}\, n\sigma^2 = \frac{1}{n}\, \sigma^2
    \end{aligned}
    $$

    Moreover, for any error threshold $\varepsilon > 0$,

    $$
    P(|M_n - \mu| \geq \varepsilon) \leq \frac{1}{n} \frac{\sigma^2}{\varepsilon^2} \longrightarrow 0 \quad \text{as } n \to \infty
    $$

    $\leadsto$ &nbsp; the probability that the sample mean is far away from the population mean goes to zero as we take large samples

    $\leadsto$ &nbsp; **the Law of Large Numbers**
    """,
                "Mean and variance of the sample mean, and the law of large numbers",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    l_n = mo.ui.slider(1, 200, 1, value=10, label="$n$", show_value=True)
    return (l_n,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, Fraction, GREY, RED, l_n, math, mo, table):
    # M_n for n rolls of the fair die of the example (X = 1 on a six): n M_n ~ Binom(n, 1/6), so M_n takes the values k/n
    _n = l_n.value
    _p, _eps = Fraction(1, 6), Fraction(1, 10)
    _mu, _var = _p, _p * (1 - _p)
    _pmf = [math.comb(_n, _k) * float(_p) ** _k * float(1 - _p) ** (_n - _k) for _k in range(_n + 1)]
    _far = [abs(Fraction(_k, _n) - _mu) >= _eps for _k in range(_n + 1)]  # exact, so that a value at mu +- eps counts as far
    _P = sum(_f for _f, _o in zip(_pmf, _far) if _o)
    _bound = float(_var / (_n * _eps**2))

    _fig = Figure(figsize=(5.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _top = 1.25 * max(_pmf)
    for _x in (float(_mu - _eps), float(_mu + _eps)):
        _ax.plot([_x, _x], [0, _top], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _lw = 2.4 if _n <= 60 else 1.4
    for _k in range(_n + 1):
        _ax.plot([_k / _n, _k / _n], [0, _pmf[_k]], color=RED if _far[_k] else BLUE, lw=_lw, solid_capstyle="butt")
    _ax.text(0.97, 0.92 * _top, r"$|m - \mu| \geq \varepsilon$", color=RED, fontsize=13, ha="right", va="top")
    _ax.set_xlim(-0.03, 1.03)
    _ax.set_ylim(0, _top)
    _ax.set_xticks([float(_mu - _eps), float(_mu), float(_mu + _eps), 1], [r"$\mu - \varepsilon$", r"$\mu$", r"$\mu + \varepsilon$", "$1$"])
    _ax.yaxis.set_major_formatter(lambda _v, _pos: f"{_v:g}")
    _ax.set_xlabel("$m$")
    _ax.set_ylabel("$f_{M_n}(m)$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(r"$M_n$ for $n$ rolls of a fair die ($X = 1$ on a six): &nbsp; $\mu = \dfrac{1}{6}$, &nbsp; $\sigma^2 = \dfrac{5}{36}$, &nbsp; $\varepsilon = 0.1$"),
            mo.hstack([l_n], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$P(\lvert M_n - \mu \rvert \geq \varepsilon)$", rf"${_P:.3g}$" if _P < 0.01 else rf"${_P:.3f}$"),
                    (r"$\dfrac{1}{n} \dfrac{\sigma^2}{\varepsilon^2}$", rf"${_bound:.3f}$"),
                ]
            ),
            _fig,
        ]
    )
    return

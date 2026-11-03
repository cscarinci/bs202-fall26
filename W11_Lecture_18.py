import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 18 · Estimators: bias, standard error and consistency", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

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

    return BLUE, GREEN, GREY, HALF, RED, arrow, definition, header, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 18", "Week 11", "Lecture 18 • Estimators: bias, standard error and consistency")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Random samples and statistics &nbsp; <span class="nw">$\leadsto$ &nbsp; law of large numbers and central limit theorem</span>

    $X_1, \dots, X_n \sim f_X$ iid with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2$

    $$
    \Longrightarrow \qquad M_n = \frac{1}{n} \sum_{i=1}^{n} X_i \quad \text{has} \quad E[M_n] = \mu, \quad \mathrm{Var}(M_n) = \frac{\sigma^2}{n}
    $$

    and

    $$
    \begin{aligned}
    & \forall\, \varepsilon > 0, && P(\underbrace{|M_n - \mu|}_{\mathclap{\footnotesize \text{error of estimation}}} \geq \varepsilon) \leq \frac{1}{n}\, \frac{\sigma^2}{\varepsilon^2} \longrightarrow 0 \quad \text{as } n \to +\infty \\[3.4em]
    & \forall\, z \in \mathbb{R}, && P\Bigg( \underbrace{\frac{M_n - \mu}{\sigma / \sqrt{n}}}_{\mathclap{\footnotesize \text{standardized mean } Z_n}} \leq z \Bigg) = F_{Z_n}(z) \longrightarrow \Phi(z) \quad \text{as } n \to +\infty
    \end{aligned}
    $$

    **In this lecture:** how good is $M_n$ as an estimator of $\mu$? &nbsp; <span class="nw">$\leadsto$ &nbsp; bias, standard error, mean squared error</span> <span class="nw">and consistency of an estimator</span>

    **References:** WMS 8.2–8.4, 9.3
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## V.1 &nbsp; Estimators: bias, standard error and consistency

    ### Estimators and bias
    """
            ),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ with an unknown parameter $\theta$ (e.g. $\mu, \sigma^2, \gamma, \dots$), <span class="nw">an **estimator** for $\theta$ is any statistic</span>

    $$
    \hat{\theta}_n = u(X_1, \dots, X_n) : S \times \cdots \times S \longrightarrow \mathbb{R}
    $$

    used to estimate $\theta$ from observed values of $X_i$.

    If $X_i(o) = x_i$, then $\hat{\theta}_n(o) = u(x_1, \dots, x_n)$ is **an estimate of** $\boldsymbol{\theta}$ &nbsp; <span class="nw">$\leadsto$ &nbsp; a guess for its value</span>
    """,
                "Estimator and estimate",
            ),
            definition(
                r"""
    We call $\hat{\theta}_n$ an **unbiased estimator** for $\theta$ if

    $$
    \mathrm{Bias}(\hat{\theta}_n) = E[\hat{\theta}_n] - \theta = 0
    $$
    """,
                "Unbiased estimator",
            ),
        ],
        gap=1.5,
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    $$
    \begin{aligned}
    M_n &= \frac{1}{n} \sum_{i=1}^{n} X_i && \text{is an unbiased estimator for } \mu \\[14pt]
    S_n^2 &= \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - M_n)^2 && \text{is unbiased for } \sigma^2 \\[14pt]
    G_n &= \frac{1}{n} \sum_{i=1}^{n} \left( \frac{X_i - M_n}{S_n} \right)^{\!3} && \text{in general is biased for } \gamma
    \end{aligned}
    $$

    $\leadsto$ &nbsp; $E[G_n]$ usually depends on higher moments
    """,
                "Bias of the sample mean, sample variance and sample skewness",
            ),
            mo.md(
                r"""
    **Proof** (for $S_n^2$). &nbsp; $X_1, \dots, X_n \sim f_X$ iid

    $$
    \sum_{i=1}^{n} (X_i - M_n)^2 = \sum_{i=1}^{n} (X_i^2 - 2 M_n X_i + M_n^2) = \sum_{i=1}^{n} X_i^2 - n M_n^2
    $$

    <span class="chain">$\displaystyle \Longrightarrow \qquad E\left[ \sum_{i=1}^{n} (X_i - M_n)^2 \right] = \sum_{i=1}^{n} E[X_i^2] - n\, E[M_n^2]$ $\displaystyle = \sum_{i=1}^{n} \left( \mathrm{Var}(X_i) + E[X_i]^2 \right) - n\, \mathrm{Var}(M_n) - n\, E[M_n]^2$ $\displaystyle = n\sigma^2 + n\mu^2 - n\, \frac{\sigma^2}{n} - n\mu^2$ $\displaystyle = (n - 1)\, \sigma^2$</span>

    <span class="chain">$\displaystyle \Longrightarrow \qquad \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - M_n)^2 \quad \text{is an unbiased estimator for } \sigma^2$ $\displaystyle \qquad \text{not } \frac{1}{n} \sum_{i=1}^{n} (X_i - M_n)^2\,!$ <span class="qed">$\square$</span></span>
    """
            ).style(display="block"),
        ],
        gap=1.5,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** If we define $\hat{\sigma}_n^2 = \dfrac{1}{n} \displaystyle\sum_{i=1}^{n} (X_i - M_n)^2$

    $$
    \begin{alignat*}{2}
    \Longrightarrow \qquad && E[\hat{\sigma}_n^2] &= \frac{n - 1}{n}\, E[S_n^2] = \frac{n - 1}{n}\, \sigma^2 \\[14pt]
    \Longrightarrow \qquad && \mathrm{Bias}(\hat{\sigma}_n^2) &= \frac{n - 1}{n}\, \sigma^2 - \sigma^2 = -\frac{1}{n}\, \sigma^2
    \end{alignat*}
    $$

    $\leadsto$ &nbsp; sometimes we call <span class="nw">$\hat{\sigma}_n^2$ the biased sample variance</span> <span class="nw">and $S_n^2$ the unbiased sample variance</span>

    $\leadsto$ &nbsp; <span class="nw">estimates from a biased estimator</span> <span class="nw">are expected to differ from the true value of the parameter</span>

    $\leadsto$ &nbsp; $\mathrm{Bias}(\hat{\theta}_n)$ measures the expected estimate error
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### Standard error"""),
            definition(
                r"""
    Given an estimator $\hat{\theta}_n$ for a parameter $\theta$, the **standard error** of $\hat{\theta}_n$ is

    $$
    \mathrm{SE}(\hat{\theta}_n) = \sqrt{\mathrm{Var}(\hat{\theta}_n)}
    $$
    """,
                "Standard error",
            ),
            mo.md(
                r"""
    **Example** (Is a die fair?). &nbsp; $X$ = result of one roll, &nbsp; <span class="nw">$X_1, \dots, X_5 \sim f_X$ iid, &nbsp; size $n = 5$</span>

    $$
    \text{fair} \quad \Longrightarrow \quad \mu = 3.5, \quad \sigma^2 = \frac{35}{12} \quad \Longrightarrow \quad \mathrm{SE}(M_5) = \sqrt{\frac{1}{5}\, \frac{35}{12}} \approx 0.76
    $$

    <span class="chain">$\displaystyle o = (2, 5, 3, 6, 4) \quad \Longrightarrow \quad M_5(o) = \frac{2 + 5 + 3 + 6 + 4}{5} = 4$ $\displaystyle \quad \Longrightarrow \quad |M_5(o) - 3.5| = 0.5 \approx 0.66\, \mathrm{SE}(M_5) \qquad \text{not bad!}$</span>

    <span class="chain">$\displaystyle \tilde{o} = (6, 5, 6, 6, 5) \quad \Longrightarrow \quad M_5(\tilde{o}) = \frac{6 + 5 + 6 + 6 + 5}{5} = 5.6$ $\displaystyle \quad \Longrightarrow \quad |M_5(\tilde{o}) - 3.5| \approx 2.75\, \mathrm{SE}(M_5) \qquad \text{suspicious!}$</span>
    """
            ).style(display="block"),
        ],
        gap=1.5,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    d_n = mo.ui.slider(steps=[5, 10, 15, 20, 30, 50, 100], value=5, label="$n$", show_value=True)
    return (d_n,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, RED, d_n, math, mo, np, table):
    _n = d_n.value
    # pmf of M_n for a fair die: X_1 + ... + X_n by repeated convolution, M_n takes the values k / n, k = n, ..., 6n
    _p = np.array([1.0])
    for _ in range(_n):
        _p = np.convolve(_p, np.full(6, 1 / 6))
    _k = np.arange(_n, 6 * _n + 1)
    _m = _k / _n
    _se = math.sqrt(35 / (12 * _n))
    _seen = (_k == 4 * _n) | (5 * _k == 28 * _n)  # M_n = 4 and M_n = 5.6 (n is a multiple of 5)
    _top = float(_p.max()) * 1.32
    _few = len(_k) <= 80

    def _pct(q):
        """A probability as on the page (51%, 0.6%): relation and percentage; below 0.01% only that bound."""
        v = 100 * q
        if v >= 9.95:
            return rf"\approx {v:.0f}\%"
        if v >= 0.01:
            return rf"\approx {v:.2g}\%"
        return r"< 0.01\%"

    _fig = Figure(figsize=(HALF + 0.6, 2.4), layout="constrained")
    _ax = _fig.subplots()
    _ax.axvline(3.5, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
    for _mask, _color in ((~_seen, BLUE), (_seen, RED)):
        _ax.vlines(_m[_mask], 0, _p[_mask], color=_color, lw=1.2 if _few else 0.8, zorder=3)
        if _few:
            _ax.plot(_m[_mask], _p[_mask], "o", color=_color, ms=3, zorder=4)
    for _x, _name in ((4, r"$M_5(o)$"), (5.6, r"$M_5(\tilde{o})$")):
        _h = float(_p[np.isclose(_m, _x)][0])
        _ax.plot(_x, _h, "o", color=RED, ms=5, zorder=5, clip_on=False)
        # the name just above its own dot (at n = 5 the page's M_5(o), M_5(o~)); 4 sits right of it, clear of the taller bars on its left
        _ax.text(_x + (0.06 if _x == 4 else 0) - (0.13 if _x == 4 and _n == 5 else 0), _h + 0.03 * _top, _name if _n == 5 else f"${_x:g}$", color=RED, fontsize=12, ha="left" if _x == 4 else "center", va="bottom")
    _ax.text(3.45, _top * 0.97, r"$\mu = 3.5$", color="black", fontsize=12, ha="right", va="top")
    # the name of f_{M_n} on its left flank at half height, moving with the bars
    _ax.annotate(r"$f_{M_n}$", (3.5 - 1.18 * _se, 0.5 * float(_p.max())), textcoords="offset points", xytext=(-6, 0), color=BLUE, fontsize=12, ha="right", va="center")
    _ax.set_xlim(0.6, 6.4)
    _ax.set_ylim(0, _top)
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks([])
    _ax.set_xlabel("$m$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _rows = [(r"$\mathrm{SE}(M_n) = \sqrt{\dfrac{1}{n}\, \dfrac{35}{12}}$", rf"${_se:.2f}$")]
    for _x in (4, 5.6):
        # at n = 5 the page's own values (0.66 from SE rounded to 0.76, 2.75 from the exact SE); otherwise exact
        _kk = {4: 0.66, 5.6: 2.75}[_x] if _n == 5 else abs(_x - 3.5) / _se
        _rows.append((rf"$\lvert {_x:g} - 3.5 \rvert$", rf"${_kk:.2f}\, \mathrm{{SE}}(M_n)$, &nbsp; $2(1 - \Phi({_kk:.2f})) {_pct(math.erfc(_kk / math.sqrt(2)))}$"))

    mo.vstack([mo.hstack([d_n], justify="start", gap=2, wrap=True), table(_rows), _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** For $n$ large, by the central limit theorem

    $$
    P(|M_n - \mu| \geq k\, \mathrm{SE}(M_n)) = P(|Z_n| \geq k) \approx 2(1 - \Phi(k))
    $$

    $$
    2(1 - \Phi(0.66)) \approx 51\%, \qquad 2(1 - \Phi(2.75)) \approx 0.6\%\,!
    $$

    $\leadsto$ &nbsp; $\mathrm{SE}(\hat{\theta}_n)$ measures the typical error range <span class="nw">(but only for unbiased estimators!)</span>
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, RED, arrow, definition, mo):
    # the sketch beside the definition: theta, E[theta_n] and theta_n at the corners of a right triangle
    _fig = Figure(figsize=(HALF, 1.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-0.9, 4.3)
    _ax.set_ylim(-0.75, 2.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _t, _e, _h = (0, 0), (3, 0), (3, 2)
    arrow(_ax, _t, _e, RED)
    arrow(_ax, _e, _h, BLUE)
    arrow(_ax, _t, _h, GREEN)
    for _pt in (_t, _e, _h):
        _ax.plot(*_pt, "o", color="black", ms=3, zorder=5)
    _ax.text(-0.12, 0, r"$\theta$", fontsize=13, ha="right", va="center")
    _ax.text(3.12, -0.08, r"$E[\hat{\theta}_n]$", fontsize=13, ha="left", va="top")
    _ax.text(3.0, 2.12, r"$\hat{\theta}_n$", fontsize=13, ha="center", va="bottom")
    _ax.text(1.5, -0.12, r"$|\mathrm{Bias}|$", color=RED, fontsize=13, ha="center", va="top")
    _ax.text(3.12, 1.0, r"$\mathrm{SE}$", color=BLUE, fontsize=13, ha="left", va="center")
    _ax.text(1.35, 1.12, r"$\sqrt{\mathrm{MSE}}$", color=GREEN, fontsize=13, ha="right", va="bottom")

    mo.vstack(
        [
            mo.md(r"""### Mean squared error"""),
            definition(
                r"""
    The **mean squared error** of $\hat{\theta}_n$ is

    $$
    \begin{aligned}
    \mathrm{MSE}(\hat{\theta}_n) &= E[(\hat{\theta}_n - \theta)^2] \\[14pt]
    &= E[\hat{\theta}_n^2] - 2\theta\, E[\hat{\theta}_n] + \theta^2 \\[14pt]
    &= \mathrm{Var}(\hat{\theta}_n) + E[\hat{\theta}_n]^2 - 2\theta\, E[\hat{\theta}_n] + \theta^2 \\[14pt]
    &= \mathrm{Var}(\hat{\theta}_n) + (E[\hat{\theta}_n] - \theta)^2 \\[14pt]
    &= \mathrm{SE}(\hat{\theta}_n)^2 + \mathrm{Bias}(\hat{\theta}_n)^2
    \end{aligned}
    $$
    """,
                "Mean squared error",
            ),
            _fig,
            mo.md(
                r"""
    $\leadsto$ &nbsp; $\mathrm{MSE}(\hat{\theta}_n)$ measures the expected squared error <span class="nw">= the square of the typical error range</span> <span class="nw">(for any estimator!)</span>

    **Remark.** &nbsp; $E[(\hat{\theta}_n - E[\hat{\theta}_n])(E[\hat{\theta}_n] - \theta)] = 0$

    $$
    \Longrightarrow \qquad E[(\hat{\theta}_n - \theta)^2] = E[(\hat{\theta}_n - E[\hat{\theta}_n])^2] + E[(E[\hat{\theta}_n] - \theta)^2]
    $$

    $\leadsto$ &nbsp; another Pythagoras!
    """
            ).style(display="block"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Consistency"""),
            definition(
                r"""
    An estimator $\hat{\theta}_n$ for $\theta$ is **consistent** if

    $$
    \forall\, \varepsilon > 0 \qquad P(|\hat{\theta}_n - \theta| \geq \varepsilon) \longrightarrow 0 \qquad \text{as } n \to +\infty
    $$
    """,
                "Consistent estimator",
            ),
            theorem(
                r"""
    If $\mathrm{Bias}(\hat{\theta}_n) \to 0$ and $\mathrm{SE}(\hat{\theta}_n) \to 0$ as $n \to +\infty$, then $\hat{\theta}_n$ is consistent for $\theta$.
    """,
                "Vanishing bias and standard error give consistency",
            ),
            mo.md(
                r"""
    **Proof** (similar to the law of large numbers).

    <span class="chain">$\displaystyle \mathrm{MSE}(\hat{\theta}_n) = \int_{-\infty}^{\infty} (t - \theta)^2 f_{\hat{\theta}_n}(t)\, dt$ $\displaystyle \geq \int_{|t - \theta| \geq \varepsilon} (t - \theta)^2 f_{\hat{\theta}_n}(t)\, dt$ $\displaystyle \geq \varepsilon^2 \int_{|t - \theta| \geq \varepsilon} f_{\hat{\theta}_n}(t)\, dt = \varepsilon^2\, P(|\hat{\theta}_n - \theta| \geq \varepsilon)$</span>

    $$
    \Longrightarrow \qquad P(|\hat{\theta}_n - \theta| \geq \varepsilon) \leq \frac{\mathrm{SE}(\hat{\theta}_n)^2 + \mathrm{Bias}(\hat{\theta}_n)^2}{\varepsilon^2} \tag*{$\square$}
    $$
    """
            ).style(display="block"),
            theorem(
                r"""
    For any continuous function $g : \mathbb{R} \longrightarrow \mathbb{R}$, <span class="nw">if $\hat{\theta}_n$ is a consistent estimator for $\theta$,</span> <span class="nw">then $g(\hat{\theta}_n)$ is a consistent estimator for $g(\theta)$!</span>
    """,
                "Continuous functions of consistent estimators",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $S_n^2$ is a consistent estimator for $\sigma^2$ &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; $\sqrt{S_n^2}$ is a consistent estimator for $\sigma$</span>
    """
            ),
        ],
        gap=1.5,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Practice

    Let $X_1, \dots, X_n \sim \mathrm{Binom}(1, p)$ iid,

    $$
    M_n = \frac{1}{n} \sum_{i=1}^{n} X_i, \qquad \hat{\sigma}_n^2 = \frac{1}{n} \sum_{i=1}^{n} (X_i - M_n)^2
    $$

    (a) Find the bias of $M_n (1 - M_n)$ as an estimator for $pq$.

    (b) Is $M_n (1 - M_n)$ a consistent estimator for $pq$?

    (c) Prove that $\hat{\sigma}_n^2 = M_n (1 - M_n)$.
    """)
    return


if __name__ == "__main__":
    app.run()

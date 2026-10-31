import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 17 · The central limit theorem", css_file="bs202.css")


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

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, GREEN, GREY, HALF, RED, arrow, definition, header, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 17", "Week 10", "Lecture 17 • The central limit theorem")
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Given a random variable $X : S \longrightarrow \mathbb{R}$, a random sample of size $n$ from the population $X$ is

    $$
    X_1, \dots, X_n : \underbrace{S \times \cdots \times S}_{\mathclap{\text{with independent probability measures}}} \longrightarrow \mathbb{R}, \qquad X_i(o_1, \dots, o_n) = X(o_i)
    $$

    $\leadsto$ &nbsp; probability of products is the product of probabilities

    $$
    \Longrightarrow \qquad X_1, \dots, X_n \sim f_X \quad \text{iid}
    $$

    A statistic is a random variable $T = u(X_1, \dots, X_n) : S \times \cdots \times S \longrightarrow \mathbb{R}$, and the sampling distribution of $T$ is $f_T : \mathbb{R} \longrightarrow \mathbb{R}$

    **Example.**

    $$
    \begin{aligned}
    M_n &= \frac{1}{n} \sum_{i=1}^{n} X_i && \text{sample mean} \\[14pt]
    S_n^2 &= \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - M_n)^2 && \text{sample variance} \\[14pt]
    G_n &= \frac{1}{n} \sum_{i=1}^{n} \left( \frac{X_i - M_n}{S_n} \right)^{\!3} && \text{sample skewness}
    \end{aligned}
    $$
    """
            ),
            theorem(
                r"""
    If $E[X] = \mu$ and $\mathrm{Var}(X) = \sigma^2$

    $$
    \Longrightarrow \qquad E[M_n] = \mu \qquad \text{and} \qquad \mathrm{Var}(M_n) = \frac{\sigma^2}{n}
    $$

    (**Law of Large Numbers**) &nbsp; $\forall\, \varepsilon > 0$

    $$
    P(\underbrace{|M_n - \mu|}_{\mathclap{\text{error of estimation}}} \geq \varepsilon) \leq \frac{1}{n}\, \frac{\sigma^2}{\varepsilon^2} \longrightarrow 0 \qquad \text{as } n \to +\infty
    $$
    """,
                "Mean and variance of the sample mean; law of large numbers",
            ),
            mo.md(r"""$\leadsto$ &nbsp; the sample mean is close to the true mean with high probability for large sample size"""),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Figure, HALF, RED, arrow, mo):
    # the sketch beside the proof: the region |m - mu| >= epsilon of the integral, on the real line
    _fig = Figure(figsize=(HALF, 0.95), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-2.75, 2.75)
    _ax.set_ylim(-0.7, 0.6)
    _ax.axis("off")
    arrow(_ax, (-2.7, 0), (2.7, 0), "black", lw=0.8)
    _ax.plot([-2.6, -1], [0, 0], color=RED, lw=2.6, solid_capstyle="butt")
    _ax.plot([1, 2.45], [0, 0], color=RED, lw=2.6, solid_capstyle="butt")
    for _x, _name in ((-1, r"$\mu - \varepsilon$"), (0, r"$\mu$"), (1, r"$\mu + \varepsilon$")):
        _ax.plot([_x, _x], [-0.1, 0.1], color="black", lw=0.8)
        _ax.text(_x, -0.2, _name, fontsize=12, ha="center", va="top")
    _ax.text(-1.8, 0.14, r"$m \leq \mu - \varepsilon$", color=RED, fontsize=12, ha="center", va="bottom")
    _ax.text(1.72, 0.14, r"$m \geq \mu + \varepsilon$", color=RED, fontsize=12, ha="center", va="bottom")

    mo.vstack(
        [
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    E[M_n] &= E\left[ \frac{1}{n} \sum_{i=1}^{n} X_i \right] = \frac{1}{n} \sum_{i=1}^{n} E[X_i] = \frac{1}{n}\, n\mu \\[14pt]
    \mathrm{Var}(M_n) &= \mathrm{Var}\left( \frac{1}{n} \sum_{i=1}^{n} X_i \right) = \frac{1}{n^2} \sum_{i=1}^{n} \mathrm{Var}(X_i) = \frac{1}{n^2}\, n\sigma^2
    \end{aligned}
    $$

    <span class="chain">$\displaystyle \frac{\sigma^2}{n} = \mathrm{Var}(M_n) = \int_{-\infty}^{\infty} (m - \mu)^2 f_{M_n}(m)\, dm$ $\displaystyle \geq \int_{|m - \mu| \geq \varepsilon} (m - \mu)^2 f_{M_n}(m)\, dm$ $\displaystyle \geq \int_{|m - \mu| \geq \varepsilon} \varepsilon^2 f_{M_n}(m)\, dm = \varepsilon^2\, P(|M_n - \mu| \geq \varepsilon)$</span>
    """
            ),
            _fig,
            mo.md(
                r"""
    $$
    \therefore \qquad P(|M_n - \mu| \geq \varepsilon) \leq \frac{1}{n}\, \frac{\sigma^2}{\varepsilon^2} \qquad \forall\, \varepsilon > 0,\ \forall\, n \geq 1 \tag*{$\square$}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example** (Fair die). &nbsp; $X$ = result &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; $f_X(x) = \dfrac{1}{6}$,</span> &nbsp; $x = 1, 2, \dots, 6$

    <span class="chain">$\displaystyle E[X] = \frac{1}{6} (1 + 2 + 3 + 4 + 5 + 6) = 3.5,$ $\displaystyle \quad E[X^2] = \frac{1}{6} (1 + 4 + 9 + 16 + 25 + 36) = \frac{91}{6}$</span>

    $$
    \Longrightarrow \qquad \mathrm{Var}(X) = E[X^2] - E[X]^2 = \frac{35}{12}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad & P(|M_n - 3.5| \geq 0.5) \leq \frac{1}{n}\, \frac{35}{3} \\[14pt]
    & |M_n - 3.5| \geq 0.5 \iff M_n \leq 3 \text{ or } M_n \geq 4
    \end{aligned}
    $$

    $n = 100$: &nbsp; $P \leq 12\%$ &nbsp;&nbsp;&nbsp; $n = 1000$: &nbsp; $P \leq 1.2\%$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    d_n = mo.ui.slider(steps=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000], value=100, label="$n$", show_value=True)
    return (d_n,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, RED, d_n, mo, np, table):
    _n = d_n.value
    # pmf of X_1 + ... + X_n for n fair dice, by repeated convolution; M_n takes the values k / n, k = n, ..., 6n
    _p = np.array([1.0])
    for _ in range(_n):
        _p = np.convolve(_p, np.full(6, 1 / 6))
    _k = np.arange(_n, 6 * _n + 1)
    _m = _k / _n
    _tail = (_k <= 3 * _n) | (_k >= 4 * _n)  # M_n <= 3 or M_n >= 4, that is |M_n - 3.5| >= 0.5
    _exact = float(_p[_tail].sum())
    _bound = 35 / (3 * _n)

    def _pct(q):
        """A probability as a percentage, as on the page (12%, 1.2%)."""
        v = 100 * q
        if v >= 9.95:
            return rf"{v:.0f}\%"
        if v >= 0.01:
            return rf"{v:.2g}\%"
        e = int(np.floor(np.log10(v)))
        return rf"{v / 10**e:.1f} \cdot 10^{{{e}}}\,\%"

    _few = len(_k) <= 80
    _top = float(_p.max()) * 1.32
    _fig = Figure(figsize=(HALF + 0.6, 2.3), layout="constrained")
    _ax = _fig.subplots()
    for _x in (3, 4):
        _ax.axvline(_x, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
    for _mask, _color in ((~_tail, BLUE), (_tail, RED)):
        _ax.vlines(_m[_mask], 0, _p[_mask], color=_color, lw=1.2 if _few else 0.8, zorder=3)
        if _few:
            _ax.plot(_m[_mask], _p[_mask], "o", color=_color, ms=3, zorder=4)
    _ax.text(3.5, _top * 0.97, r"$f_{M_n}$", color="black", fontsize=12, ha="center", va="top")
    _ax.text(2.9, _top * 0.97, r"$M_n \leq 3$", color=RED, fontsize=12, ha="right", va="top")
    _ax.text(4.1, _top * 0.97, r"$M_n \geq 4$", color=RED, fontsize=12, ha="left", va="top")
    _ax.set_xlim(0.6, 6.4)
    _ax.set_ylim(0, _top)
    _ax.set_xticks(range(1, 7))
    _ax.set_yticks([])
    _ax.set_xlabel("$m$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([d_n], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$P(M_n \leq 3 \text{ or } M_n \geq 4)$", rf"${_pct(_exact)}$"),
                    (r"bound $\dfrac{1}{n}\, \dfrac{35}{3}$", rf"${_pct(_bound)}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **In this lecture:** sampling distribution of $M_n$; the central limit theorem; $\mathrm{Binom}(n, p) \approx \mathcal{N}(np, npq)$ for large $n$

    **References:** WMS 7.2–7.5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## IV.4 &nbsp; The central limit theorem

    ### Sampling distribution of $M_n$ for a normal population

    **Example** (Normal population). &nbsp; $X \sim \mathcal{N}(\mu, \sigma^2)$

    <span class="chain">$\displaystyle \Longrightarrow \qquad f_X(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$ $\displaystyle \quad \Longrightarrow \quad m_X(t) = \exp\!\left( \mu t + \frac{\sigma^2}{2}\, t^2 \right)$</span>

    $X_1, \dots, X_n \sim \mathcal{N}(\mu, \sigma^2)$ iid

    <span class="chain">$\displaystyle \Longrightarrow \qquad m_{X_1 + \cdots + X_n}(t) = (m_X(t))^n = \exp\!\left( n\mu t + n \frac{\sigma^2}{2}\, t^2 \right)$ $\displaystyle \quad \Longrightarrow \quad X_1 + \cdots + X_n \sim \mathcal{N}(n\mu, n\sigma^2)$ $\displaystyle \quad \Longrightarrow \quad M_n = \frac{1}{n} (X_1 + \cdots + X_n) \sim \mathcal{N}\!\left( \mu, \frac{\sigma^2}{n} \right)$</span>

    ($X \sim \mathcal{N}(\mu, \sigma^2) \ \Longrightarrow \ Y = aX + b \sim \mathcal{N}(a\mu + b, a^2\sigma^2)$)

    $\Longrightarrow$ &nbsp; the sample mean of a normal population is normally distributed around the mean, with smaller variance for larger sizes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    v_n = mo.ui.slider(1, 10, 1, value=4, label="$n$", show_value=True)
    return (v_n,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, HALF, math, mo, np, v_n):
    _n = v_n.value
    # x in units of sigma from mu: f_X is the N(0, 1) curve, f_{M_n} the N(0, 1/n) curve (the same scale for both)
    _u = np.linspace(-3.6, 3.6, 721)

    def _phi(v, s):
        return np.exp(-(np.asarray(v, dtype=float) ** 2) / (2 * s**2)) / (s * math.sqrt(2 * math.pi))

    _s = 1 / math.sqrt(_n)
    _fig = Figure(figsize=(HALF + 0.6, 2.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_u, _phi(_u, 1), color=BLUE, lw=1.4, zorder=3)
    _ax.plot(_u, _phi(_u, _s), color=GREEN, lw=1.4, zorder=4)
    _ax.annotate(r"$f_X$", (-1.6, float(_phi(-1.6, 1))), textcoords="offset points", xytext=(-4, 4), color=BLUE, fontsize=12, ha="right", va="bottom")
    # the name of f_{M_n} sits at its half height, on the right flank, and moves with the curve
    _h = math.sqrt(2 * math.log(2)) * _s
    _ax.annotate(r"$f_{M_n}$", (_h, float(_phi(_h, _s))), textcoords="offset points", xytext=(7, 3), color=GREEN, fontsize=12, ha="left", va="bottom")
    _ax.set_xlim(-3.6, 3.6)
    _ax.set_ylim(0, 1.36)
    _ax.set_xticks([-2, -1, 0, 1, 2], [r"$\mu - 2\sigma$", r"$\mu - \sigma$", r"$\mu$", r"$\mu + \sigma$", r"$\mu + 2\sigma$"])
    _ax.set_yticks([])
    _ax.tick_params(labelsize=11)
    for _sp in ("top", "right", "left"):
        _ax.spines[_sp].set_visible(False)

    mo.vstack([mo.hstack([v_n], justify="start", gap=2, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; what about for other populations?

    ### Standardized mean and the central limit theorem
    """
            ),
            definition(
                r"""
    Given $X$ with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2 > 0$ and $X_1, \dots, X_n \sim f_X$ iid, the **standardized mean** is

    $$
    Z_n = \frac{M_n - \mu}{\sigma / \sqrt{n}}
    $$
    """,
                "Standardized mean",
            ),
            theorem(
                r"""
    $$
    E[Z_n] = 0, \qquad \mathrm{Var}(Z_n) = 1
    $$

    (**Central limit theorem**) &nbsp; $\forall\, z \in \mathbb{R}$

    $$
    \underbrace{P(Z_n \leq z)}_{\text{cdf of } Z_n} \longrightarrow \underbrace{\Phi(z)}_{\mathclap{\text{standard normal cdf}}} \qquad \text{as } n \to +\infty
    $$
    """,
                "Mean and variance of the standardized mean; central limit theorem",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; the distribution of the standardized mean approaches the standard normal distribution for large sample sizes **for any population!**

    **Example.** &nbsp; $X \sim \mathrm{Binom}(1, p)$ &nbsp; ($E[X] = p$, $\mathrm{Var}(X) = pq$)

    $X_1, \dots, X_n \sim \mathrm{Binom}(1, p)$ iid

    $$
    \begin{aligned}
    \Longrightarrow \qquad X_1 + \cdots + X_n &\sim \mathrm{Binom}(n, p) \\[14pt]
    X_1 + \cdots + X_n &= n M_n = np + \sqrt{npq}\, Z_n
    \end{aligned}
    $$

    $$
    \text{CLT} \quad \Longrightarrow \quad \mathrm{Binom}(n, p) \approx \mathcal{N}(np, npq) \qquad \text{for large } n\,!
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    b_n = mo.ui.slider(1, 100, 1, value=10, label="$n$", show_value=True)
    return (b_n,)


@app.cell(hide_code=True)
def _(BLUE, Figure, HALF, RED, b_n, math, mo, np):
    _n, _pp = b_n.value, 1 / 6
    _mean, _sd = _n * _pp, math.sqrt(_n * _pp * (1 - _pp))
    _ks = np.arange(_n + 1)
    _pmf = np.array([math.comb(_n, int(_k)) * _pp**_k * (1 - _pp) ** (_n - _k) for _k in _ks])
    # the frame follows the distribution: mean +- 4.5 standard deviations
    _lo, _hi = _mean - 4.5 * _sd, _mean + 4.5 * _sd
    _lo, _hi = min(_lo, _hi - 4), max(_hi, _lo + 4)
    _x = np.linspace(_lo, _hi, 600)
    _pdf = np.exp(-((_x - _mean) ** 2) / (2 * _sd**2)) / (_sd * math.sqrt(2 * math.pi))
    _top = 1.3 * max(float(_pmf.max()), float(_pdf.max()))
    _in = (_ks >= _lo) & (_ks <= _hi)

    _fig = Figure(figsize=(HALF + 0.6, 2.3), layout="constrained")
    _ax = _fig.subplots()
    _ax.vlines(_ks[_in], 0, _pmf[_in], color=BLUE, lw=1.2, zorder=3)
    _ax.plot(_ks[_in], _pmf[_in], "o", color=BLUE, ms=3, zorder=4)
    _ax.plot(_x, _pdf, color=RED, lw=1.4, zorder=5)
    # each name beside its own object: the bars' left flank and the curve's right flank (the frame follows mean +- 4.5 sd)
    _xr = _mean + 1.4 * _sd
    _ax.annotate(r"$\mathcal{N}(np, npq)$", (_xr, math.exp(-0.98) / (_sd * math.sqrt(2 * math.pi))), textcoords="offset points", xytext=(6, 4), color=RED, fontsize=12, ha="left", va="bottom")
    _ax.text(_mean - 1.5 * _sd, 0.8 * float(_pmf.max()), r"$\mathrm{Binom}(n, p)$", color=BLUE, fontsize=12, ha="right", va="center")
    _ax.set_xlim(_lo, _hi)
    _ax.set_ylim(0, _top)
    _ax.xaxis.get_major_locator().set_params(integer=True)
    _ax.set_yticks([])
    _ax.set_xlabel("$x$")
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    mo.vstack([mo.hstack([b_n, mo.md(r"$p = 1/6$")], justify="start", gap=2, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof.** &nbsp; $X_1, \dots, X_n \sim f_X$ iid with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2 > 0$

    ① &nbsp; standardize each measurement $X_i$

    $$
    Y_i = \frac{X_i - \mu}{\sigma}
    $$

    $\Longrightarrow$ &nbsp; $Y_1, \dots, Y_n \sim f_Y$ iid with $E[Y] = 0$, $E[Y^2] = 1$

    $\leadsto$ &nbsp; $E[Y^3] = \gamma_X = \, ?$

    $$
    \text{②} \qquad Z_n = \frac{\dfrac{X_1 + \cdots + X_n}{n} - \mu}{\sigma / \sqrt{n}} = \frac{Y_1 + \cdots + Y_n}{\sqrt{n}}
    $$

    <span class="chain">$\displaystyle \Longrightarrow \qquad m_{Z_n}(t) = E[e^{t Z_n}] = E\Big[ e^{t (Y_1 + \cdots + Y_n)/\sqrt{n}} \Big]$ $\displaystyle = m_{Y_1 + \cdots + Y_n}(t / \sqrt{n}) = \big( m_Y(t / \sqrt{n}) \big)^n$</span>

    $$
    \text{③} \qquad m_Y(s) = E[e^{sY}] = 1 + s\, E[Y] + \frac{s^2}{2}\, E[Y^2] + \frac{s^3}{3!}\, E[Y^3] + \cdots
    $$

    <span class="chain">$\displaystyle \Longrightarrow \qquad m_Y(t / \sqrt{n}) = 1 + \frac{t^2}{2n} + \frac{t^3}{6n\sqrt{n}}\, E[Y^3] + \cdots$ $\displaystyle \quad \Longrightarrow \quad m_{Z_n}(t) = \left( 1 + \frac{t^2}{2n} + \frac{t^3}{6n\sqrt{n}}\, E[Y^3] + \cdots \right)^{\!n}$ $\displaystyle \xrightarrow[n \to \infty]{} e^{t^2/2} = m_Z(t), \qquad Z \sim \mathcal{N}(0, 1)$ <span class="qed">$\square$</span></span>
    """)
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 11 · Expectations for continuous random variables; moment generating functions", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc
    from matplotlib.ticker import FuncFormatter

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, FuncFormatter, math, mo, np


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

    def proposition(body, title=""):
        return _statement("Proposition", title, body)

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def postulate(body, title=""):
        return _statement("Postulate", title, body)

    def note(body):
        """Editorial note of the notebook (not part of the lecture)."""
        return mo.md("**Note.** " + body.strip())

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

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=LIGHT, lw=0.6)
        ax.set_axisbelow(True)

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

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        import numpy as _np

        rng = _np.random.default_rng(seed)
        t = _np.linspace(0, 2 * _np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * _np.cos(k * t + rng.uniform(0, 2 * _np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * _np.cos(t), cy + ry * r * _np.sin(t)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 11", "Week 06", "Lecture 11 • Expectations for continuous random variables; moment generating functions")
    return


@app.cell(hide_code=True)
def _(arrow, math):
    def vector(ax, tail, tip, color, label=None, turn=0, r=15, **kw):
        """Arrow from `tail` to `tip` (a dot when it has zero length), labelled beyond its tip on a white box;
        `turn` (degrees) rotates the label about the tip so that coinciding vectors keep separate labels."""
        dx, dy = tip[0] - tail[0], tip[1] - tail[1]
        if dx == 0 and dy == 0:
            ax.plot(*tip, "o", color=color, ms=4, zorder=4)
            d = math.radians(45 + turn)
        else:
            arrow(ax, tail, tip, color, **kw)
            d = math.atan2(dy, dx) + math.radians(turn)
        if label:
            ax.annotate(label, tip, textcoords="offset points", xytext=(r * math.cos(d), r * math.sin(d)), ha="center", va="center", color=color, fontsize=13, zorder=5, bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    return (vector,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - continuous random variables: &nbsp; $X : S \longrightarrow \mathbb{R}$, &nbsp; $S_X = \mathrm{Im}(X)$ uncountable
    - $\leadsto$ &nbsp; $F_X(x) = P(X \leq x)$ continuous &nbsp; (cdf)
    - $\leadsto$ &nbsp; $f_X(x) = \dfrac{d}{dx} F_X(x)$ &nbsp; (pdf; where the derivative is well-defined; usually, piecewise continuous)
    - **Remark.** For continuous random variables &nbsp; $f_X(x) \neq \underbrace{P(X = x)}_{\footnotesize =\, 0 \ \forall\, x}$

    **In this lecture:** expectations for continuous random variables; moment generating functions

    **References:** WMS 3.9, 4.3, 4.9
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## III.2 &nbsp; Expectations for continuous random variables; moment generating functions

    ### Expectation values
    """
            ),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ continuous random variable and $u : \mathbb{R} \longrightarrow \mathbb{R}$ a single variable function

    <span class="chain">$\displaystyle \underbrace{E[u(X)]}_{\footnotesize \text{expectation value of } u(X)} = \int_{-\infty}^{+\infty} u(x)\, f_X(x)\, dx$ $\displaystyle = \underbrace{\int_{S_X} u(x)\, f_X(x)\, dx}_{\footnotesize f_X(x) \,=\, 0 \ \forall\, x \notin S_X}$</span>
    """,
                "Expectation value",
            ),
            mo.md(r"**Recall:** For discrete random variables &nbsp; $E[u(X)] = \displaystyle\sum_{x \in S_X} u(x)\, f_X(x)$"),
            theorem(
                r"""
    Given $u : \mathbb{R} \longrightarrow \mathbb{R}$, $v : \mathbb{R} \longrightarrow \mathbb{R}$, $a, b, c \in \mathbb{R}$

    $$
    E[a\, u(X) + b\, v(X)] = a\, E[u(X)] + b\, E[v(X)], \qquad E[c] = c
    $$
    """,
                "Linearity of expectation",
            ),
            definition(
                r"""
    For $X : S \longrightarrow \mathbb{R}$ continuous random variable

    <span class="chain">$\displaystyle E[X] = \mu_X$ $\displaystyle = \int_{-\infty}^{\infty} x\, f_X(x)\, dx \quad \text{is the \textbf{mean} of } X$</span>

    <span class="chain">$\displaystyle E[(X - \mu_X)^2] = \mathrm{Var}(X) = \sigma_X^2$ $\displaystyle = \int_{-\infty}^{\infty} (x - \mu_X)^2 f_X(x)\, dx \quad \text{is the \textbf{variance} of } X$</span>

    <span class="chain">$\displaystyle E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = \mathrm{Skew}(X) = \gamma_X$ $\displaystyle = \int_{-\infty}^{\infty} \left( \frac{x - \mu_X}{\sigma_X} \right)^{\!3} f_X(x)\, dx \quad \text{is the \textbf{skewness} of } X$</span>

    More generally,

    $$
    \begin{aligned}
    E[X^k] &= \hat{\mu}_{X,k} && \text{is the } k\text{th \textbf{moment} of } X, \\[4pt]
    E[(X - \mu_X)^k] &= \mu_{X,k} && \text{is the } k\text{th \textbf{central moment} of } X
    \end{aligned}
    $$
    """,
                "Mean, variance, skewness, moments",
            ),
            mo.md(r"**Remark.** Moments and central moments are defined similarly for discrete random variables."),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, math, mo, np, theorem):
    _fig = Figure(figsize=(5.6, 2.7), layout="constrained")
    _ax = _fig.subplots()
    _r = np.linspace(0.04, 5.05, 500)
    _ax.plot(_r, [math.gamma(_v) for _v in _r], color=BLUE, lw=1.4)
    _ax.plot(range(1, 6), [math.factorial(_n - 1) for _n in range(1, 6)], "o", color="black", ms=4, zorder=4)
    _ax.text(2.4, 15.5, r"$\Gamma(r) = \int_0^\infty x^{r-1} e^{-x}\, dx$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.text(3.88, 7.6, r"$\Gamma(n) = (n - 1)!$", fontsize=12, ha="right", va="center")
    _ax.set_xlim(0, 5.3)
    _ax.set_ylim(0, 26)
    _ax.set_xticks(range(0, 6))
    _ax.set_yticks([0, 6, 12, 18, 24])
    _ax.set_xlabel("$r$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            theorem(
                r"""
    Let $X \sim \mathrm{Gamma}(r, \lambda)$ (be a random variable with pdf $\mathrm{Gamma}(r, \lambda)$), then

    $$
    E[X] = \frac{r}{\lambda}, \qquad \mathrm{Var}(X) = \frac{r}{\lambda^2}, \qquad \mathrm{Skew}(X) = \frac{2}{\sqrt{r}}
    $$
    """,
                "Mean, variance and skewness of the Gamma distribution",
            ),
            mo.md(
                r"""
    **Proof** (for mean and variance).

    **1.**

    $$
    \int_{-\infty}^{\infty} f_X(x)\, dx = \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx \ \overset{?}{=} \ 1
    $$

    Integration by parts with $u = (\lambda x)^{r-1}$, $dv = e^{-\lambda x}\, d(\lambda x)$:

    $$
    \int_{0}^{\infty} (\lambda x)^{r-1} e^{-\lambda x}\, d(\lambda x) = \underbrace{-e^{-\lambda x} (\lambda x)^{r-1}\, \Big|_{0}^{\infty}}_{\footnotesize =\, 0} + (r - 1) \int_{0}^{\infty} (\lambda x)^{r-2} e^{-\lambda x}\, d(\lambda x)
    $$

    <span class="chain">$\displaystyle \Longrightarrow \quad \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx$ $\displaystyle = \frac{1}{(r - 1)!} \int_{0}^{\infty} (\lambda x)^{r-1} e^{-\lambda x}\, d(\lambda x)$ $\displaystyle = \frac{1}{(r - 2)!} \int_{0}^{\infty} (\lambda x)^{r-2} e^{-\lambda x}\, d(\lambda x)$ $\displaystyle = \frac{1}{(r - 3)!} \int_{0}^{\infty} (\lambda x)^{r-3} e^{-\lambda x}\, d(\lambda x) = \cdots$ $\displaystyle = \frac{1}{0!} \int_{0}^{\infty} e^{-\lambda x}\, d(\lambda x)$ $\displaystyle = -e^{-\lambda x}\, \Big|_{0}^{\infty} = 0 - (-1) = 1$</span>

    $$
    \leadsto \qquad \boxed{\int_{0}^{\infty} x^{r-1} e^{-x}\, dx = (r - 1)!}
    $$

    $\leadsto$ &nbsp; the left-hand side, $\Gamma(r)$, can be defined for any $r > 0$ &nbsp; (factorials for positive numbers!)
    """
            ),
            _fig,
            mo.md(
                r"""
    **2.**

    <span class="chain">$\displaystyle E[X] = \int_{0}^{\infty} x\, \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx$ $\displaystyle = \frac{1}{(r - 1)!}\, \frac{1}{\lambda} \int_{0}^{\infty} (\lambda x)^r e^{-\lambda x}\, d(\lambda x)$ $\displaystyle = \frac{1}{(r - 1)!}\, \frac{1}{\lambda}\, \Gamma(r + 1)$ $\displaystyle = \frac{r!}{(r - 1)!}\, \frac{1}{\lambda} = \frac{r}{\lambda}$</span>

    **3.**

    $$
    \begin{align*}
    E[X^2] &= \frac{1}{(r - 1)!}\, \frac{1}{\lambda^2}\, \Gamma(r + 2) \\[14pt]
    \mathrm{Var}(X) &= E[X^2] - E[X]^2 = \frac{r (r + 1)}{\lambda^2} - \frac{r^2}{\lambda^2} = \frac{r}{\lambda^2} \tag*{$\square$}
    \end{align*}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    gp_r = mo.ui.slider(1, 10, 1, value=2, label="$r$", show_value=True)
    return (gp_r,)


@app.cell(hide_code=True)
def _(BLUE, Figure, FuncFormatter, GREEN, GREY, LIGHT, gp_r, math, mo, np, table):
    _r, _lam = gp_r.value, 1
    _mu, _sd = _r / _lam, math.sqrt(_r) / _lam
    # one frame for every r (r at most 10: mu + 4 sigma < 23), so that the mean and the spread move
    _lo, _hi, _end = max(0.0, _mu - _sd), _mu + _sd, 24

    def _f(x):
        return _lam**_r * x ** (_r - 1) / math.factorial(_r - 1) * np.exp(-_lam * x)

    _x = np.linspace(0, _end, 500)
    _top = float(_f(_x).max())
    _in = np.linspace(_lo, _hi, 200)

    _fig = Figure(figsize=(5.6, 3.0))
    _ax = _fig.add_axes((0.14, 0.2, 0.83, 0.77))
    _ax.fill_between(_in, 0, _f(_in), color=LIGHT, lw=0)
    for _b in (_lo, _hi):
        _ax.plot([_b, _b], [0, 1.12 * _top], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([_mu, _mu], [0, 1.12 * _top], color=GREEN, lw=1.4, ls=(0, (4, 3)))
    _ax.plot(_x, _f(_x), color=BLUE, lw=1.4)
    # mu_X above its own line; the band named once, just right of its right edge and a row lower: the names never meet for any r
    _ax.annotate(r"$\mu_X$", (_mu, 1.2 * _top), color=GREEN, fontsize=12, ha="center", va="center")
    _ax.annotate(r"$\mu_X \pm \sigma_X$", (_hi, 1.05 * _top), textcoords="offset points", xytext=(4, 0), color=GREY, fontsize=12, ha="left", va="center")
    _ax.set_xlim(0, _end)
    _ax.set_xticks([0, 5, 10, 15, 20])
    _ax.set_ylim(0, 1.3 * _top)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    _ax.yaxis.set_major_formatter(FuncFormatter(lambda _v, _p: f"${_v:g}$"))
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    def _v(x):
        """Exact when a multiple of 1/2, otherwise two decimals."""
        return f"{round(2 * x) / 2 + 0.0:g}" if abs(2 * x - round(2 * x)) < 1e-9 else f"{x:.2f}"

    mo.vstack(
        [
            mo.hstack([gp_r, mo.md(r"$X \sim \mathrm{Gamma}(r, 1)$")], justify="start", align="center", gap=2, wrap=True),
            table(
                [
                    (r"$\mathrm{Skew}(X) = 2/\sqrt{r}$", f"${_v(2 / math.sqrt(_r))}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Moment generating functions"""),
            definition(
                r"""
    For a random variable $X$ (continuous or discrete) the **moment generating function** is the function of a real variable $t$, defined via

    $$
    m_X(t) = E[e^{tX}] \qquad (\text{expectation of exponential of } t \text{ times } X)
    $$

    (finite for $t$ near $0$)
    """,
                "Moment generating function",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $X \sim \mathrm{Binom}(n, p)$

    $$
    m_X(t) = \sum_{x=0}^{n} e^{tx} \binom{n}{x} p^x q^{n-x} = \sum_{x=0}^{n} \binom{n}{x} (p e^t)^x q^{n-x} = (q + p e^t)^n
    $$

    $X \sim \mathrm{Pois}(\lambda)$

    $$
    m_X(t) = \sum_{x=0}^{\infty} e^{tx} e^{-\lambda}\, \frac{\lambda^x}{x!} = \sum_{x=0}^{\infty} e^{-\lambda}\, \frac{(\lambda e^t)^x}{x!} = e^{-\lambda} e^{\lambda e^t} = e^{\lambda (e^t - 1)}
    $$

    $X \sim \mathrm{Gamma}(r, \lambda)$

    <span class="chain">$\displaystyle m_X(t) = \int_{0}^{\infty} e^{tx}\, \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx$ $\displaystyle = \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-(\lambda - t) x}\, dx = \frac{\lambda^r}{(\lambda - t)^r} \qquad \text{for } t < \lambda$</span>
    """
            ),
            theorem(
                r"""
    Given a random variable $X$ with mgf $m_X(t)$, then

    $$
    E[X^k] = \hat{\mu}_{X,k} = \frac{d^k}{dt^k} \Big|_{t=0}\, m_X(t)
    $$

    Also, writing $K_X(t) = \ln(m_X(t))$, we have

    <span class="chain">$\displaystyle K_X(0) = 0,$ $\displaystyle \quad K_X'(0) = E[X],$ $\displaystyle \quad K_X''(0) = \mathrm{Var}(X)$ $\displaystyle \quad \text{and} \quad K_X'''(0) = E[(X - \mu_X)^3]$ $\displaystyle \quad \Longrightarrow \quad \mathrm{Skew}(X) = \frac{K_X'''(0)}{\big( K_X''(0) \big)^{3/2}}$</span>
    """,
                "Moments from the mgf",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $m_X(t) = E[e^{tX}]$

    <span class="chain">$\displaystyle \frac{d}{dt} m_X(t) = \frac{d}{dt} E[e^{tX}]$ $\displaystyle = E\!\left[ \frac{d}{dt} e^{tX} \right]$ $\displaystyle = E[e^{tX} X]$</span>

    <span class="chain">$\displaystyle \frac{d^2}{dt^2} m_X(t) = E[e^{tX} X^2]$ $\displaystyle \qquad \cdots \qquad \frac{d^k}{dt^k} m_X(t) = E[e^{tX} X^k]$ $\displaystyle \quad \Longrightarrow \quad m_X^{(k)}(0) = E[X^k]$</span>

    Similarly,

    <span class="chain">$\displaystyle \frac{d}{dt} K_X(t) = \frac{1}{m_X(t)}\, m_X'(t)$ $\displaystyle \quad \Longrightarrow \quad K_X'(0) = \frac{E[X]}{E[1]} = E[X] \qquad (E[1] = m_X(0) = 1)$</span>

    <span class="chain">$\displaystyle \frac{d^2}{dt^2} K_X(t) = \frac{1}{(m_X(t))^2} \Big[ m_X(t)\, m_X''(t) - \big( m_X'(t) \big)^2 \Big]$ $\displaystyle \quad \Longrightarrow \quad K_X''(0) = E[X^2] - (E[X])^2$</span>

    <span class="chain">$\displaystyle \frac{d^3}{dt^3} K_X(t) = \cdots$ <span class="qed">$\square$</span></span>

    **Remark.** &nbsp; $K_X^{(4)}(0) = E[(X - \mu_X)^4] - 3\, E[(X - \mu_X)^2]^2$ &nbsp; (4th cumulant; not the 4th central moment)

    **Example.** &nbsp; $X \sim \mathrm{Binom}(n, p)$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $m_X(t) = (q + p e^t)^n$,</span> &nbsp; $K_X(t) = \ln(m_X(t)) = n \ln(q + p e^t)$

    <span class="chain">$\displaystyle K_X'(t) = \frac{n}{q + p e^t}\, p e^t$ $\displaystyle \quad \leadsto \quad \mu_X = K_X'(0) = \frac{n}{q + p}\, p = np$</span>

    <span class="chain">$\displaystyle K_X''(t) = \frac{n}{(q + p e^t)^2} \Big( p e^t (q + p e^t) - (p e^t)^2 \Big)$ $\displaystyle = \frac{n p q\, e^t}{(q + p e^t)^2}$ $\displaystyle \quad \leadsto \quad \sigma_X^2 = K_X''(0) = npq$</span>

    <span class="chain">$\displaystyle K_X'''(t) = \frac{n}{(q + p e^t)^3} \Big( pq\, e^t (q + p e^t) - 2 pq\, e^t \cdot p e^t \Big)$ $\displaystyle = \frac{n}{(q + p e^t)^3} \Big( pq\, e^t (q - p e^t) \Big)$ $\displaystyle \quad \leadsto \quad \gamma_X = \frac{K_X'''(0)}{\sigma_X^3} = \frac{npq (q - p)}{(npq)^{3/2}} = \frac{q - p}{\sqrt{npq}}$</span>

    $X \sim \mathrm{Pois}(\lambda)$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $m_X(t) = e^{\lambda (e^t - 1)}$,</span> &nbsp; $K_X(t) = \lambda (e^t - 1)$

    $$
    \begin{aligned}
    K_X'(t) &= \lambda e^t, & \qquad K_X''(t) &= \lambda e^t, & \qquad K_X'''(t) &= \lambda e^t \\[10pt]
    \mu_X &= \lambda, & \qquad \sigma_X^2 &= \lambda, & \qquad \gamma_X &= \frac{\lambda}{(\lambda)^{3/2}} = \frac{1}{\sqrt{\lambda}}
    \end{aligned}
    $$

    $X \sim \mathrm{Gamma}(r, \lambda)$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $m_X(t) = \left( \dfrac{\lambda}{\lambda - t} \right)^{\!r}$,</span> &nbsp; $K_X(t) = r \big( \ln \lambda - \ln(\lambda - t) \big)$

    $$
    \begin{aligned}
    K_X'(t) &= \frac{r}{\lambda - t}, & \quad K_X''(t) &= \frac{r}{(\lambda - t)^2}, & \quad K_X'''(t) &= \frac{2r}{(\lambda - t)^3} \\[14pt]
    \mu_X &= \frac{r}{\lambda}, & \quad \sigma_X^2 &= \frac{r}{\lambda^2}, & \quad \gamma_X &= \frac{2r / \lambda^3}{(r / \lambda^2)^{3/2}} = \frac{2}{\sqrt{r}}
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mg_dist = mo.ui.dropdown(["Binom(n, p)", "Pois(λ)", "Gamma(r, λ)"], value="Binom(n, p)", label="distribution", allow_select_none=False)
    return (mg_dist,)


@app.cell(hide_code=True)
def _(mo):
    # one set of sliders per distribution, each with its own range; every mean is at most 10, so m_X(t) stays visible on -1 <= t <= 1
    mg_bn = mo.ui.slider(1, 10, 1, value=10, label="$n$", show_value=True)
    mg_bp = mo.ui.slider(0.05, 0.95, 0.05, value=0.3, label="$p$", show_value=True)
    mg_pl = mo.ui.slider(0.1, 10, 0.1, value=0.3, label=r"$\lambda$", show_value=True)
    mg_gr = mo.ui.slider(1, 10, 1, value=10, label="$r$", show_value=True)
    mg_gl = mo.ui.slider(1, 5, 0.1, value=2, label=r"$\lambda$", show_value=True)
    return mg_bn, mg_bp, mg_gl, mg_gr, mg_pl


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, FuncFormatter, GREEN, LIGHT, mg_bn, mg_bp, mg_dist, mg_gl, mg_gr, mg_pl, mo, np, table):
    _d = mg_dist.value
    _tmax = 1.0
    if _d.startswith("Binom"):
        _sliders = [mg_bn, mg_bp]
        _a, _b = mg_bn.value, mg_bp.value
        _closed = (r"np", r"npq", r"(q - p)/\sqrt{npq}")

        def _K(t):
            return _a * np.log1p(_b * np.expm1(t))

        _mu, _var, _k3 = _a * _b, _a * _b * (1 - _b), _a * _b * (1 - _b) * (1 - 2 * _b)
    elif _d.startswith("Pois"):
        _sliders = [mg_pl]
        _b = mg_pl.value
        _closed = (r"\lambda", r"\lambda", r"1/\sqrt{\lambda}")

        def _K(t):
            return _b * np.expm1(t)

        _mu, _var, _k3 = _b, _b, _b
    else:
        _sliders = [mg_gr, mg_gl]
        _a, _b = mg_gr.value, mg_gl.value
        _closed = (r"r/\lambda", r"r/\lambda^2", r"2/\sqrt{r}")

        def _K(t):
            return -_a * np.log1p(-t / _b)

        _mu, _var, _k3 = _a / _b, _a / _b**2, 2 * _a / _b**3
        _tmax = min(1.0, 0.8 * _b)  # m_X(t) exists for t < lambda only

    def _v(x):
        """Exact when a multiple of 1/2, otherwise two decimals."""
        return f"{round(2 * x) / 2 + 0.0:g}" if abs(2 * x - round(2 * x)) < 1e-9 else f"{x + 0.0:.2f}"

    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax, _name in ((_left, "$m_X(t)$"), (_right, r"$K_X(t) = \ln m_X(t)$")):
        _ax.axvline(0, color="black", lw=0.8)
        _ax.grid(True, color=LIGHT, lw=0.6)
        _ax.set_axisbelow(True)
        _ax.set_xlim(-1, _tmax)
        _ax.set_xlabel("$t$")
        _ax.set_ylabel(_name)
        _ax.xaxis.set_major_formatter(FuncFormatter(lambda _v, _p: f"${_v:g}$"))
        _ax.yaxis.set_major_formatter(FuncFormatter(lambda _v, _p: f"${_v:g}$"))
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    _rows = [
        (rf"$\mu_X = K_X'(0) = {_closed[0]}$", f"${_v(_mu)}$"),
        (rf"$\sigma_X^2 = K_X''(0) = {_closed[1]}$", f"${_v(_var)}$"),
        (rf"$\gamma_X = K_X'''(0) / \sigma_X^3 = {_closed[2]}$", f"${_v(_k3 / _var**1.5)}$"),
    ]
    _t = np.linspace(-1, _tmax, 300)
    _left.plot(_t, np.exp(_K(_t)), color=BLUE, lw=1.4)
    _left.plot(0, 1, "o", color="black", ms=4, zorder=4)
    # m_X grows very fast for t > 0: the frame stops at 5, so that m_X(0) = 1 and the slope at 0 stay visible
    _left.set_ylim(0, min(1.05 * float(np.exp(_K(_t)).max()), 5))
    _right.plot(_t, _mu * _t, color=GREEN, lw=1.4)
    _right.plot(_t, _K(_t), color=BLUE, lw=1.4)
    _right.plot(0, 0, "o", color="black", ms=4, zorder=4)
    # K_X is convex, so the tangent lies below the curve: the label goes just below the tangent, at t = -1/2
    _right.annotate(r"$t\, K_X'(0)$", (-0.5, -0.5 * _mu), textcoords="offset points", xytext=(4, -6), color=GREEN, fontsize=14, ha="left", va="top")

    mo.vstack(
        [
            mo.hstack([mg_dist, *_sliders], justify="start", gap=2, wrap=True),
            table(_rows),
            _fig,
        ]
    )
    return

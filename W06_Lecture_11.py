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

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np


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
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#1b458f", "#b3261e", "#2e7d32", "#e65100", "#888888", "#cfe3f5"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS202 &bull; {running}</div>
      <div class="bs-title">Introduction to Probability and Mathematical Statistics</div>
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
        One head size and one line weight for every figure, so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>,head_width=0.15,head_length=0.35", "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, check, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 11", "Week 06", "Lecture 11 · Expectations for continuous random variables; moment generating functions")
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
    - **Remark.** For continuous random variables &nbsp; $f_X(x) \neq \underbrace{P(X = x)}_{=\, 0 \ \forall x}$

    **In this lecture:** expectations for continuous random variables; moment generating functions
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.7 &nbsp; Expectations for continuous random variables; moment generating functions

    ### Expectation values
    """
            ),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ continuous random variable and $u : \mathbb{R} \longrightarrow \mathbb{R}$ a single variable function

    $$
    \underbrace{E[u(X)]}_{\text{expectation value of } u(X)} = \int_{-\infty}^{+\infty} u(x)\, f_X(x)\, dx = \int_{S_X} u(x)\, f_X(x)\, dx \qquad (f_X(x) = 0 \ \ \forall\, x \notin S_X)
    $$
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
            mo.md(r"""### Mean, variance, skewness and moments"""),
            definition(
                r"""
    For $X : S \longrightarrow \mathbb{R}$ continuous random variable

    $$
    \begin{aligned}
    E[X] = \mu_X &= \int_{-\infty}^{\infty} x\, f_X(x)\, dx && \text{is the \textbf{mean} of } X \\[4pt]
    E[(X - \mu_X)^2] = \mathrm{Var}(X) = \sigma_X^2 &= \int_{-\infty}^{\infty} (x - \mu_X)^2 f_X(x)\, dx && \text{is the \textbf{variance} of } X \\[4pt]
    E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = \mathrm{Skew}(X) = \gamma_X &= \int_{-\infty}^{\infty} \left( \frac{x - \mu_X}{\sigma_X} \right)^{\!3} f_X(x)\, dx && \text{is the \textbf{skewness} of } X
    \end{aligned}
    $$

    More generally,

    $$
    E[X^k] = \hat{\mu}_{X,k} \quad \text{is the } k\text{th \textbf{moment} of } X, \qquad
    E[(X - \mu_X)^k] = \mu_{X,k} \quad \text{is the } k\text{th \textbf{central moment} of } X
    $$
    """,
                "Mean, variance, skewness, moments",
            ),
            mo.md(r"**Remark.** Moments and central moments are defined similarly for discrete random variables."),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, math, mo, np, theorem):
    _fig = Figure(figsize=(FULL, 2.7), layout="constrained")
    _ax = _fig.subplots()
    _r = np.linspace(0.04, 5.05, 500)
    _ax.plot(_r, [math.gamma(_v) for _v in _r], color=BLUE, lw=1.4)
    _ax.plot(range(1, 6), [math.factorial(_n - 1) for _n in range(1, 6)], "o", color="black", ms=4, zorder=4)
    _ax.text(2.4, 15.5, r"$\Gamma(r) = \int_0^\infty x^{r-1} e^{-x}\, dx$", color=BLUE, fontsize=13, ha="center", va="center")
    _ax.text(4.12, 3.6, r"$\Gamma(n) = (n - 1)!$", fontsize=12, ha="left", va="center")
    _ax.set_xlim(0, 5.3)
    _ax.set_ylim(0, 26)
    _ax.set_xticks(range(0, 6))
    _ax.set_yticks([0, 6, 12, 18, 24])
    _ax.set_xlabel("$r$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(r"""### Mean, variance and skewness of the Gamma distribution"""),
            theorem(
                r"""
    Let $X \sim \mathrm{Gamma}(r, \lambda)$ (be a random variable with pdf $\mathrm{Gamma}(r, \lambda)$), then

    $$
    E[X] = \frac{r}{\lambda}, \qquad \mathrm{Var}(X) = \frac{r}{\lambda^2}, \qquad \mathrm{Skew}(X) = \frac{2}{\sqrt{r}}
    $$
    """,
                "Moments of the Gamma distribution",
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
    \int_{0}^{\infty} (\lambda x)^{r-1} e^{-\lambda x}\, d(\lambda x) = \underbrace{-e^{-\lambda x} (\lambda x)^{r-1}\, \Big|_{0}^{\infty}}_{=\, 0} + (r - 1) \int_{0}^{\infty} (\lambda x)^{r-2} e^{-\lambda x}\, d(\lambda x)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx
    &= \frac{1}{(r - 1)!} \int_{0}^{\infty} (\lambda x)^{r-1} e^{-\lambda x}\, d(\lambda x) = \frac{1}{(r - 2)!} \int_{0}^{\infty} (\lambda x)^{r-2} e^{-\lambda x}\, d(\lambda x) \\[6pt]
    &= \frac{1}{(r - 3)!} \int_{0}^{\infty} (\lambda x)^{r-3} e^{-\lambda x}\, d(\lambda x) = \cdots = \frac{1}{0!} \int_{0}^{\infty} e^{-\lambda x}\, d(\lambda x) \\[6pt]
    &= -e^{-\lambda x}\, \Big|_{0}^{\infty} = 0 - (-1) = 1
    \end{aligned}
    $$

    $$
    \leadsto \quad \boxed{\int_{0}^{\infty} x^{r-1} e^{-x}\, dx = (r - 1)!}
    $$

    $\leadsto$ &nbsp; the left-hand side, $\Gamma(r)$, can be defined for any $r > 0$ &nbsp; (factorials for positive numbers!)
    """
            ),
            _fig,
            mo.md(
                r"""
    **2.**

    $$
    \begin{aligned}
    E[X] &= \int_{0}^{\infty} x\, \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx = \frac{1}{(r - 1)!}\, \frac{1}{\lambda} \int_{0}^{\infty} (\lambda x)^r e^{-\lambda x}\, d(\lambda x) \\[6pt]
    &= \frac{1}{(r - 1)!}\, \frac{1}{\lambda}\, \Gamma(r + 1) = \frac{r!}{(r - 1)!}\, \frac{1}{\lambda} = \frac{r}{\lambda}
    \end{aligned}
    $$

    **3.**

    $$
    \mathrm{Var}(X) = \underbrace{E[X^2]}_{=\, \Gamma(r + 2) / ((r - 1)!\, \lambda^2)} - \ E[X]^2 = \frac{r (r + 1)}{\lambda^2} - \frac{r^2}{\lambda^2} = \frac{r}{\lambda^2} \qquad \square
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
def _(mo):
    gp_lam = mo.ui.slider(0.2, 4, 0.1, value=1, label=r"$\lambda$", show_value=True)
    return (gp_lam,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, gp_lam, gp_r, math, mo, np, table):
    _r, _lam = gp_r.value, gp_lam.value
    _mu, _sd = _r / _lam, math.sqrt(_r) / _lam
    _lo, _hi, _end = max(0.0, _mu - _sd), _mu + _sd, _mu + 4 * _sd

    def _f(x):
        return _lam**_r * x ** (_r - 1) / math.factorial(_r - 1) * np.exp(-_lam * x)

    _x = np.linspace(0, _end, 500)
    _top = float(_f(_x).max())
    _in = np.linspace(_lo, _hi, 200)

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.fill_between(_in, 0, _f(_in), color=LIGHT, lw=0)
    for _b in (_lo, _hi):
        _ax.plot([_b, _b], [0, 1.12 * _top], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([_mu, _mu], [0, 1.12 * _top], color=GREEN, lw=1.4, ls=(0, (4, 3)))
    _ax.plot(_x, _f(_x), color=BLUE, lw=1.4)
    _near = _lo < 0.12 * _end  # the left label goes to the right of its line when there is no room on its left
    _ax.annotate(r"$\mu_X - \sigma_X$", (_lo, 1.2 * _top), textcoords="offset points", xytext=(4 if _near else -2, 0), color=GREY, fontsize=12, ha="left" if _near else "right", va="center")
    _ax.annotate(r"$\mu_X + \sigma_X$", (_hi, 1.2 * _top), textcoords="offset points", xytext=(2, 0), color=GREY, fontsize=12, ha="left", va="center")
    _ax.text(_mu, 1.2 * _top, r"$\mu_X$", color=GREEN, fontsize=12, ha="center", va="center", bbox=_box)
    _ax.set_xlim(0, _end)
    _ax.set_ylim(0, 1.3 * _top)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([gp_r, gp_lam], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$E[X] = r/\lambda$", rf"$\textcolor{{{GREEN}}}{{{_mu:.3f}}}$"),
                    (r"$\mathrm{Var}(X) = r/\lambda^2$", rf"${_r / _lam**2:.3f}$"),
                    (r"$\sigma_X = \sqrt{r}/\lambda$", rf"${_sd:.3f}$"),
                    (r"$\mathrm{Skew}(X) = 2/\sqrt{r}$", rf"${2 / math.sqrt(_r):.3f}$"),
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

    (defined for the $t$ where this expectation is finite; for the moment formulas below we need this on an open interval around $t = 0$)
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

    $$
    m_X(t) = \int_{0}^{\infty} e^{tx}\, \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx = \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-(\lambda - t) x}\, dx = \frac{\lambda^r}{(\lambda - t)^r} \qquad \text{for } t < \lambda
    $$
    """
            ),
            theorem(
                r"""
    Given a random variable $X$ with mgf $m_X(t)$, then

    $$
    E[X^k] = \hat{\mu}_{X,k} = \frac{d^k}{dt^k} \Big|_{t=0}\, m_X(t)
    $$

    Also, writing $K_X(t) = \ln(m_X(t))$, we have

    $$
    K_X(0) = 0, \qquad K_X'(0) = E[X], \qquad K_X''(0) = \mathrm{Var}(X)
    $$

    $$
    \text{and} \quad K_X'''(0) = E[(X - \mu_X)^3] \quad \Longrightarrow \quad \mathrm{Skew}(X) = \frac{K_X'''(0)}{\big( K_X''(0) \big)^{3/2}}
    $$
    """,
                "Moments from the mgf",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $m_X(t) = E[e^{tX}]$

    $$
    \frac{d}{dt} m_X(t) = \frac{d}{dt} E[e^{tX}] = E\!\left[ \frac{d}{dt} e^{tX} \right] = E[e^{tX} X]
    $$

    $$
    \frac{d^2}{dt^2} m_X(t) = E[e^{tX} X^2] \qquad \cdots \qquad \frac{d^k}{dt^k} m_X(t) = E[e^{tX} X^k]
    \qquad \Longrightarrow \qquad m_X^{(k)}(0) = E[X^k]
    $$

    Similarly,

    $$
    \frac{d}{dt} K_X(t) = \frac{1}{m_X(t)}\, m_X'(t) \qquad \Longrightarrow \qquad K_X'(0) = \frac{E[X]}{E[1]}
    $$

    $$
    \frac{d^2}{dt^2} K_X(t) = \frac{1}{(m_X(t))^2} \Big[ m_X(t)\, m_X''(t) - \big( m_X'(t) \big)^2 \Big] \qquad \Longrightarrow \qquad K_X''(0) = E[X^2] - (E[X])^2
    $$

    $$
    \frac{d^3}{dt^3} K_X(t) = \cdots \qquad \square
    $$

    **Remark.** &nbsp; $K_X^{(4)}(0) = E[(X - \mu_X)^4] - 3\, E[(X - \mu_X)^2]^2$ &nbsp; (4th cumulant; not the 4th central moment)

    **Example.** &nbsp; $X \sim \mathrm{Binom}(n, p)$ &nbsp; $\leadsto$ &nbsp; $m_X(t) = (q + p e^t)^n$, &nbsp; $K_X(t) = \ln(m_X(t)) = n \ln(q + p e^t)$

    $$
    K_X'(t) = \frac{n}{q + p e^t}\, p e^t \qquad \leadsto \qquad \mu_X = K_X'(0) = \frac{n}{q + p}\, p = np
    $$

    $$
    K_X''(t) = \frac{n}{(q + p e^t)^2} \Big( p e^t (q + p e^t) - (p e^t)^2 \Big) = \frac{n p q\, e^t}{(q + p e^t)^2} \qquad \leadsto \qquad \sigma_X^2 = K_X''(0) = npq
    $$

    $$
    K_X'''(t) = \frac{n}{(q + p e^t)^3} \Big( pq\, e^t (q + p e^t) - 2 pq\, e^t \cdot p e^t \Big) = \frac{n}{(q + p e^t)^3} \Big( pq\, e^t (q - p e^t) \Big)
    $$

    $$
    \leadsto \quad \gamma_X = \frac{K_X'''(0)}{\sigma_X^3} = \frac{npq (q - p)}{(npq)^{3/2}} = \frac{q - p}{\sqrt{npq}}
    $$

    $X \sim \mathrm{Pois}(\lambda)$ &nbsp; $\leadsto$ &nbsp; $m_X(t) = e^{\lambda (e^t - 1)}$, &nbsp; $K_X(t) = \lambda (e^t - 1)$

    $$
    \begin{aligned}
    K_X'(t) &= \lambda e^t, & K_X''(t) &= \lambda e^t, & K_X'''(t) &= \lambda e^t \\
    \mu_X &= \lambda, & \sigma_X^2 &= \lambda, & \gamma_X &= \frac{\lambda}{(\lambda)^{3/2}} = \frac{1}{\sqrt{\lambda}}
    \end{aligned}
    $$

    $X \sim \mathrm{Gamma}(r, \lambda)$ &nbsp; $\leadsto$ &nbsp; $m_X(t) = \left( \dfrac{\lambda}{\lambda - t} \right)^{\!r}$, &nbsp; $K_X(t) = r \big( \ln \lambda - \ln(\lambda - t) \big)$

    $$
    \begin{aligned}
    K_X'(t) &= \frac{r}{\lambda - t}, & K_X''(t) &= \frac{r}{(\lambda - t)^2}, & K_X'''(t) &= \frac{2r}{(\lambda - t)^3} \\[4pt]
    \mu_X &= \frac{r}{\lambda}, & \sigma_X^2 &= \frac{r}{\lambda^2}, & \gamma_X &= \frac{2r / \lambda^3}{(r / \lambda^2)^{3/2}} = \frac{2}{\sqrt{r}}
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
    mg_a = mo.ui.slider(1, 30, 1, value=10, label="$n$ / $r$", show_value=True)
    return (mg_a,)


@app.cell(hide_code=True)
def _(mo):
    mg_b = mo.ui.slider(0.1, 5, 0.1, value=0.3, label=r"$p$ / $\lambda$", show_value=True)
    return (mg_b,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, LIGHT, math, mg_a, mg_b, mg_dist, mo, np, table):
    _d, _a, _b = mg_dist.value, mg_a.value, mg_b.value
    _need, _scale, _tmax = None, 1.0, 1.0
    if _d.startswith("Binom"):
        _formula = rf"$(q + p e^t)^n, \quad n = {_a}, \ p = {_b:g}$"
        _closed = (r"np", r"npq", r"npq\,(q - p)")
        if _b > 1:
            _need = r"need $p \leq 1$"
        else:

            def _K(t):
                return _a * np.log1p(_b * np.expm1(t))

            _mu, _var, _k3 = _a * _b, _a * _b * (1 - _b), _a * _b * (1 - _b) * (1 - 2 * _b)
    elif _d.startswith("Pois"):
        _formula = rf"$e^{{\lambda (e^t - 1)}}, \quad \lambda = {_b:g}$"
        _closed = (r"\lambda", r"\lambda", r"\lambda")

        def _K(t):
            return _b * np.expm1(t)

        _mu, _var, _k3 = _b, _b, _b
    else:
        _formula = rf"$\left( \dfrac{{\lambda}}{{\lambda - t}} \right)^{{\!r}}, \quad r = {_a}, \ \lambda = {_b:g}$"
        _closed = (r"r/\lambda", r"r/\lambda^2", r"2r/\lambda^3")

        def _K(t):
            return -_a * np.log1p(-t / _b)

        _mu, _var, _k3 = _a / _b, _a / _b**2, 2 * _a / _b**3
        _scale, _tmax = min(1.0, _b), min(1.0, 0.8 * _b)  # m_X(t) exists for t < lambda only

    def _n(x):
        """Four decimals, rounding half up after eight significant digits (ties and near-ties go up, so that both columns round alike)."""
        x = float(f"{x:.8g}")
        return f"{math.copysign(math.floor(abs(x) * 1e4 + 0.5 + 1e-3) / 1e4, x) + 0.0:.4f}"

    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax, _name in ((_left, "$m_X(t)$"), (_right, r"$K_X(t) = \ln m_X(t)$")):
        _ax.axvline(0, color="black", lw=0.8)
        _ax.grid(True, color=LIGHT, lw=0.6)
        _ax.set_axisbelow(True)
        _ax.set_xlim(-1, _tmax)
        _ax.set_xlabel("$t$")
        _ax.set_ylabel(_name)
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    if _need:
        _rows = [(rf"$K_X'(0) = \mu_X = {_closed[0]}$", _need), (rf"$K_X''(0) = \sigma_X^2 = {_closed[1]}$", _need), (rf"$K_X'''(0) = E[(X - \mu_X)^3] = {_closed[2]}$", _need), (r"$\gamma_X = K_X'''(0) / K_X''(0)^{3/2}$", _need)]
        for _ax in (_left, _right):
            _ax.set_ylim(0, 1)
            _ax.set_yticks([])
    else:
        # central differences of K_X at 0, exact to the digits shown
        _h = 3e-3 * _scale
        _k = {_i: float(_K(_i * _h)) for _i in (-3, -2, -1, 0, 1, 2, 3)}
        _K1 = (_k[-2] - 8 * _k[-1] + 8 * _k[1] - _k[2]) / (12 * _h)
        _K2 = (-_k[-2] + 16 * _k[-1] - 30 * _k[0] + 16 * _k[1] - _k[2]) / (12 * _h**2)
        _K3 = (_k[-3] - 8 * _k[-2] + 13 * _k[-1] - 13 * _k[1] + 8 * _k[2] - _k[3]) / (8 * _h**3)
        _skew = (rf"${_n(_K3 / _K2**1.5)}$ &nbsp; (closed form: ${_n(_k3 / _var**1.5)}$)") if _var > 0 else r"need $\sigma_X^2 > 0$"
        _rows = [
            (rf"$K_X'(0) = \mu_X$", rf"$\textcolor{{{GREEN}}}{{{_n(_K1)}}}$ &nbsp; (closed form: ${_closed[0]} = {_n(_mu)}$)"),
            (rf"$K_X''(0) = \sigma_X^2$", rf"${_n(_K2)}$ &nbsp; (closed form: ${_closed[1]} = {_n(_var)}$)"),
            (rf"$K_X'''(0) = E[(X - \mu_X)^3]$", rf"${_n(_K3)}$ &nbsp; (closed form: ${_closed[2]} = {_n(_k3)}$)"),
            (r"$\gamma_X = K_X'''(0) / K_X''(0)^{3/2}$", _skew),
        ]
        _t = np.linspace(-1, _tmax, 300)
        _left.plot(_t, np.exp(_K(_t)), color=BLUE, lw=1.4)
        _right.plot(_t, _mu * _t, color=GREEN, lw=1.4)
        _right.plot(_t, _K(_t), color=BLUE, lw=1.4)
        _right.plot(0, 0, "o", color="black", ms=4, zorder=4)
        _right.annotate(r"$t\, K_X'(0)$", (1, 0), xycoords="axes fraction", textcoords="offset points", xytext=(-4, 4), color=GREEN, fontsize=12, ha="right", va="bottom", bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"})

    mo.vstack(
        [
            mo.hstack([mg_dist, mg_a, mg_b], justify="start", gap=2, wrap=True),
            table([(r"$m_X(t)$", _formula)] + _rows),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - for a continuous random variable, $E[u(X)] = \int_{-\infty}^{\infty} u(x)\, f_X(x)\, dx$; it is linear, and $E[c] = c$
    - mean $\mu_X = E[X]$, variance $\sigma_X^2 = E[(X - \mu_X)^2]$, skewness $\gamma_X = E\big[\big((X - \mu_X)/\sigma_X\big)^3\big]$; $k$th moment $E[X^k]$ and $k$th central moment $E[(X - \mu_X)^k]$
    - $X \sim \mathrm{Gamma}(r, \lambda)$: &nbsp; $E[X] = r/\lambda$, $\mathrm{Var}(X) = r/\lambda^2$, $\mathrm{Skew}(X) = 2/\sqrt{r}$ &nbsp; (using $\Gamma(r) = (r - 1)!$)
    - moment generating function $m_X(t) = E[e^{tX}]$: &nbsp; $E[X^k] = m_X^{(k)}(0)$
    - $K_X(t) = \ln(m_X(t))$: &nbsp; $K_X'(0) = \mu_X$, $K_X''(0) = \sigma_X^2$, $K_X'''(0) = E[(X - \mu_X)^3]$

    **Next:** uniform, beta and Gaussian distributions
    """)
    return


if __name__ == "__main__":
    app.run()

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
    RED, GREEN, BLUE, GREY = "#b3261e", "#2e7d32", "#1b458f", "#888888"

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
        <b>Date</b><span>{date}</span><b>Instructor</b><span>Professor Scarinci</span>
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

    def warning(body):
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 2.2, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=18)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color="#cfe3f5", lw=0.6)
        ax.set_axisbelow(True)

    def check(field, answer):
        """Feedback mark for a numeric answer typed into a text field."""
        s = field.value.strip().replace(",", ".")
        if not s:
            return ""
        try:
            return "✅" if abs(float(s) - answer) < 1e-6 else "❌ try again"
        except ValueError:
            return "⚠️ enter a number"

    return BLUE, GREEN, GREY, RED, arrow, check, definition, header, plane, theorem, warning


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED):
    _PIPS = {
        1: [(2, 2)],
        2: [(1, 1), (3, 3)],
        3: [(1, 1), (2, 2), (3, 3)],
        4: [(1, 1), (1, 3), (3, 1), (3, 3)],
        5: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)],
        6: [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3)],
    }

    def die(n, color=BLUE):
        """A small picture of a die face, for use inside text."""
        dots = "".join(f'<circle cx="{6 * x}" cy="{6 * y}" r="2" fill="{color}"/>' for x, y in _PIPS[n])
        return (
            '<svg viewBox="0 0 24 24" style="display:inline-block;width:1.25em;height:1.25em;vertical-align:-0.25em">'
            f'<rect x="1.5" y="1.5" width="21" height="21" rx="4" fill="none" stroke="{color}" stroke-width="1.6"/>{dots}</svg>'
        )

    def dice(faces, color=BLUE):
        return ", ".join(die(n, color) for n in faces)

    return dice, die


@app.cell(hide_code=True)
def _(arrow):
    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(mo):
    def ask(label, field, answer, tol=1e-6):
        """A labelled answer box with a feedback mark; accepts decimals, decimal commas and percentages."""
        raw = field.value.strip()
        mark = ""
        if raw:
            try:
                value = float(raw.rstrip("%").replace(",", ".")) / (100 if raw.endswith("%") else 1)
                mark = "✅" if abs(value - answer) <= tol else "❌ try again"
            except ValueError:
                mark = "⚠️ enter a number"
        return mo.hstack([mo.md(label), field, mo.md(mark)], justify="start", align="center")

    def box():
        return mo.ui.text(placeholder="?", debounce=True)

    return ask, box


@app.cell(hide_code=True)
def _(header):
    header("Lecture 11", "Week 06", "Lecture 11 · Expectations for continuous random variables; moment generating functions")
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Continuous RVs

    $$
    X : S \longrightarrow \mathbb{R}, \qquad S_X = \mathrm{Im}(X) \ \text{ uncountable}
    $$

    $$
    \leadsto \quad \underbrace{F_X(x)}_{\text{cdf}} = P(X \leq x) \ \text{ continuous}
    \qquad \leadsto \qquad \underbrace{f_X(x)}_{\text{pdf}} = \frac{d}{dx} F_X(x) \quad \left( \begin{array}{c} \text{where the derivative is well-defined} \\ \text{(usually, piecewise continuous)} \end{array} \right)
    $$

    **Remark.** For continuous RVs &nbsp; $f_X(x) \neq \underbrace{P(X = x)}_{=\, 0 \ \forall x}$

    **Today:** Expectations for continuous RVs; Moment generating functions
    """
            ),
            definition(
                r"""
    Given $X : S \longrightarrow \mathbb{R}$ continuous RV and $u : \mathbb{R} \longrightarrow \mathbb{R}$ a single variable function

    $$
    \underbrace{E[u(X)]}_{\text{expectation value of } u(X)} = \int_{-\infty}^{+\infty} u(x)\, f_X(x)\, dx = \int_{S_X} u(x)\, f_X(x)\, dx \qquad (f_X(x) = 0 \ \ \forall\, x \notin S_X)
    $$
    """
            ),
            mo.md(r"**Recall:** For discrete RVs &nbsp; $E[u(X)] = \displaystyle\sum_{x \in S_X} u(x)\, f_X(x)$"),
            theorem(
                r"""
    Given $u : \mathbb{R} \longrightarrow \mathbb{R}$, $v : \mathbb{R} \longrightarrow \mathbb{R}$, $a, b, c \in \mathbb{R}$

    $$
    E[a\, u(X) + b\, v(X)] = a\, E[u(X)] + b\, E[v(X)], \qquad E[c] = c
    $$
    """
            ),
            definition(
                r"""
    For $X : S \longrightarrow \mathbb{R}$ continuous RV

    $$
    E[X] = \mu_X = \int_{-\infty}^{\infty} x\, f_X(x)\, dx \qquad \text{is the \textbf{mean} of } X
    $$

    $$
    E[(X - \mu_X)^2] = \mathrm{Var}(X) = \sigma_X^2 = \int_{-\infty}^{\infty} (x - \mu_X)^2 f_X(x)\, dx \qquad \text{is the \textbf{variance} of } X
    $$

    $$
    E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = \mathrm{Skew}(X) = \gamma_X = \int_{-\infty}^{\infty} \left( \frac{x - \mu_X}{\sigma_X} \right)^{\!3} f_X(x)\, dx \qquad \text{is the \textbf{skewness} of } X
    $$

    More generally,

    $$
    E[X^k] = \hat{\mu}_{X,k} \quad \text{is the } k\text{th \textbf{moment} of } X, \qquad
    E[(X - \mu_X)^k] = \mu_{X,k} \quad \text{is the } k\text{th \textbf{central moment} of } X
    $$
    """
            ),
            mo.md(r"**Remark.** Moments and central moments are defined similarly for discrete RVs."),
            theorem(
                r"""
    Let $X \sim \mathrm{Gamma}(r, \lambda)$, i.e. a RV with pdf $\mathrm{Gamma}(r, \lambda)$. Then

    $$
    E[X] = \frac{r}{\lambda}, \qquad \mathrm{Var}(X) = \frac{r}{\lambda^2}, \qquad \mathrm{Skew}(X) = \frac{2}{\sqrt{r}}
    $$
    """
            ),
            mo.md(
                r"""
    **Proof** (for mean and variance).

    **1.**

    $$
    \int_{-\infty}^{\infty} f_X(x)\, dx = \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx \ \overset{?}{=} \ 1
    $$

    Side computation (integration by parts with $u = (\lambda x)^{r-1}$, $dv = e^{-\lambda x}\, d(\lambda x)$):

    $$
    \int_{0}^{\infty} (\lambda x)^{r-1} e^{-\lambda x}\, d(\lambda x) = \underbrace{-e^{-\lambda x} (\lambda x)^{r-1}\, \Big|_{0}^{\infty}}_{0} + (r - 1) \int_{0}^{\infty} (\lambda x)^{r-2} e^{-\lambda x}\, d(\lambda x)
    $$

    Using it repeatedly:

    $$
    \begin{aligned}
    \int_{0}^{\infty} \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx
    &= \frac{1}{(r - 1)!} \int_{0}^{\infty} (\lambda x)^{r-1} e^{-\lambda x}\, d(\lambda x) = \frac{1}{(r - 2)!} \int_{0}^{\infty} (\lambda x)^{r-2} e^{-\lambda x}\, d(\lambda x) = \frac{1}{(r - 3)!} \int_{0}^{\infty} (\lambda x)^{r-3} e^{-\lambda x}\, d(\lambda x) \\[6pt]
    &= \cdots = \frac{1}{0!} \int_{0}^{\infty} e^{-\lambda x}\, d(\lambda x) = -e^{-\lambda x}\, \Big|_{0}^{\infty} = 0 - (-1) = 1
    \end{aligned}
    $$

    $$
    \leadsto \quad \boxed{\int_{0}^{\infty} x^{r-1} e^{-x}\, dx = (r - 1)!}
    $$

    $\Gamma(r)$ can be defined for any $r > 0$! &nbsp; $\leadsto$ &nbsp; factorials for positive numbers!
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, math, mo, np):
    _fig = Figure(figsize=(5.0, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _r = np.linspace(0.05, 5, 400)
    _ax.plot(_r, [math.gamma(v) for v in _r], color=BLUE, lw=1.4, label=r"$\Gamma(r) = \int_0^\infty x^{r-1} e^{-x}\, dx$")
    _ax.plot(range(1, 6), [math.factorial(n - 1) for n in range(1, 6)], "o", color=RED, ms=5, label="$(n - 1)!$")
    _ax.set_ylim(0, 25)
    _ax.set_xlabel("$r$")
    _ax.legend(frameon=False, fontsize=10)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    mo.hstack([_fig, mo.md(r"e.g. $\Gamma(\tfrac{1}{2}) = \sqrt{\pi}$, &nbsp; $\Gamma(r + 1) = r\, \Gamma(r)$ for every $r > 0$")], widths=[3, 2], gap=2, align="center", wrap=True)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **2.**

    $$
    E[X] = \int_{0}^{\infty} x\, \frac{\lambda^r x^{r-1}}{(r - 1)!}\, e^{-\lambda x}\, dx = \frac{1}{(r - 1)!}\, \frac{1}{\lambda} \int_{0}^{\infty} (\lambda x)^r e^{-\lambda x}\, d(\lambda x)
    = \frac{1}{(r - 1)!}\, \frac{1}{\lambda}\, \Gamma(r + 1) = \frac{r!}{(r - 1)!}\, \frac{1}{\lambda} = \frac{r}{\lambda}
    $$

    **3.**

    $$
    \mathrm{Var}(X) = E[X^2] - E[X]^2 = \frac{1}{(r - 1)!}\, \frac{1}{\lambda^2}\, \Gamma(r + 2) - \frac{r^2}{\lambda^2} = \frac{r (r + 1)}{\lambda^2} - \frac{r^2}{\lambda^2} = \frac{r}{\lambda^2}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    gp_r = mo.ui.slider(1, 10, 1, value=2, label="$r$", show_value=True)
    gp_lam = mo.ui.slider(0.2, 4, 0.1, value=1, label=r"$\lambda$", show_value=True)
    return gp_lam, gp_r


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, gp_lam, gp_r, math, mo, np):
    _r, _lam = gp_r.value, gp_lam.value
    _mu, _sd = _r / _lam, math.sqrt(_r) / _lam
    _x = np.linspace(0, _mu + 4 * _sd, 400)
    _pdf = _lam**_r * _x ** (_r - 1) / math.factorial(_r - 1) * np.exp(-_lam * _x)
    _fig = Figure(figsize=(6.4, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_x, _pdf, color=BLUE, lw=1.4)
    _ax.axvspan(max(0, _mu - _sd), _mu + _sd, color=RED, alpha=0.1, lw=0)
    _ax.axvline(_mu, color=RED, lw=1.2, ls="--")
    _ax.text(_mu, max(_pdf) * 1.05, r"$\mu_X = r/\lambda$", color=RED, ha="center", fontsize=10)
    _ax.text(_mu + _sd, max(_pdf) * 0.5, r"$\mu_X \pm \sigma_X$", color=RED, fontsize=9, ha="left")
    _ax.set_ylim(0, max(_pdf) * 1.2)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)
    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $E[X] = r/\lambda$ | ${_mu:.4g}$ |",
            rf"| $\mathrm{{Var}}(X) = r/\lambda^2$ | ${_r / _lam**2:.4g}$ |",
            rf"| $\mathrm{{Skew}}(X) = 2/\sqrt{{r}}$ | ${2 / math.sqrt(_r):.4g}$ |",
        ]
    )
    mo.vstack([mo.hstack([gp_r, gp_lam], justify="start", gap=3, wrap=True), mo.hstack([_fig, mo.md(_table)], widths=[3, 2], gap=2, align="center", wrap=True)])
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    For a RV $X$ (continuous or discrete) the **moment generating function** is the function of a real variable $t$, defined via

    $$
    m_X(t) = E[e^{tX}] \qquad (\text{expectation of exponential of } t \text{ times } X)
    $$

    (defined for the $t$ where this expectation is finite; for the moment formulas below we need this on an open interval around $t = 0$)
    """
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
    Given a RV $X$ with mgf $m_X(t)$, then

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
    """
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
    mg_a = mo.ui.slider(1, 30, 1, value=10, label="$n$ / $r$", show_value=True)
    mg_b = mo.ui.slider(0.1, 5, 0.1, value=0.3, label=r"$p$ / $\lambda$", show_value=True)
    return mg_a, mg_b, mg_dist


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, math, mg_a, mg_b, mg_dist, mo, np):
    _d, _a, _b = mg_dist.value, mg_a.value, mg_b.value
    if _d.startswith("Binom"):
        _p = min(_b, 0.99)
        _m = lambda t: (1 - _p + _p * np.exp(t)) ** _a
        _mu, _var, _k3 = _a * _p, _a * _p * (1 - _p), _a * _p * (1 - _p) * (1 - 2 * _p)
        _label, _tmax = rf"$m_X(t) = (q + p e^t)^n$, $n = {_a}$, $p = {_p:g}$", 1.0
        _closed = (r"np", r"npq", r"npq\,(q - p)")
    elif _d.startswith("Pois"):
        _m = lambda t: np.exp(_b * (np.exp(t) - 1))
        _mu, _var, _k3 = _b, _b, _b
        _label, _tmax = rf"$m_X(t) = e^{{\lambda (e^t - 1)}}$, $\lambda = {_b:g}$", 1.0
        _closed = (r"\lambda", r"\lambda", r"\lambda")
    else:
        _m = lambda t: (_b / (_b - t)) ** _a
        _mu, _var, _k3 = _a / _b, _a / _b**2, 2 * _a / _b**3
        _label, _tmax = rf"$m_X(t) = (\lambda / (\lambda - t))^r$, $r = {_a}$, $\lambda = {_b:g}$", min(1.0, 0.8 * _b)
        _closed = (r"r/\lambda", r"r/\lambda^2", r"2r/\lambda^3")

    _K = lambda t: np.log(_m(t))
    _h = 1e-2
    _K1 = (_K(_h) - _K(-_h)) / (2 * _h)
    _K2 = (_K(_h) - 2 * _K(0.0) + _K(-_h)) / _h**2
    _K3 = (_K(2 * _h) - 2 * _K(_h) + 2 * _K(-_h) - _K(-2 * _h)) / (2 * _h**3)

    _t = np.linspace(-1, _tmax, 300)
    _fig = Figure(figsize=(8.0, 3.0), layout="constrained")
    _l, _r = _fig.subplots(1, 2)
    _l.plot(_t, _m(_t), color=BLUE, lw=1.4)
    _l.set_title("mgf  $m_X(t)$", fontsize=12)
    _r.plot(_t, _K(_t), color=RED, lw=1.4)
    _r.plot(_t, _mu * _t, ":", color="#555555", lw=1, label=r"tangent at 0: slope $K_X'(0) = \mu_X$")
    _r.set_title("cgf  $K_X(t) = \\ln m_X(t)$", fontsize=12)
    _r.legend(frameon=False, fontsize=9)
    for _ax in (_l, _r):
        _ax.axvline(0, color="#999999", lw=0.6)
        _ax.set_xlabel("$t$")
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    _table = "\n".join(
        [
            "| | numerically from $K_X$ | closed form |",
            "|:--|--:|--:|",
            rf"| $K_X'(0) = \mu_X$ | ${_K1:.4f}$ | ${_closed[0]} = {_mu:.4f}$ |",
            rf"| $K_X''(0) = \sigma_X^2$ | ${_K2:.4f}$ | ${_closed[1]} = {_var:.4f}$ |",
            rf"| $K_X'''(0) = E[(X - \mu_X)^3]$ | ${_K3:.4f}$ | ${_closed[2]} = {_k3:.4f}$ |",
            rf"| $\gamma_X = K_X'''(0) / K_X''(0)^{{3/2}}$ | ${_K3 / _K2**1.5:.4f}$ | ${_k3 / _var**1.5:.4f}$ |",
        ]
    )
    mo.vstack([mo.hstack([mg_dist, mg_a, mg_b], justify="start", gap=3, wrap=True), mo.md(_label), _fig, mo.md(_table)])
    return


if __name__ == "__main__":
    app.run()

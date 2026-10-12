import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 12 · Uniform, beta and Gaussian distributions", css_file="bs202.css")


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
    #   BLUE   the primary object (the particle, the point, the chosen vector)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (velocity, relative velocity, tangent vector)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (equator, light cone, inertial comparison)
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
    header("Lecture 12", "Week 06", "Lecture 12 · Uniform, beta and Gaussian distributions")
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
def _(mo):
    mo.md(r"""
    ## Last time

    - moments and the mgf: &nbsp; $m_X(t) = E[e^{tX}]$, &nbsp; $K_X(t) = \ln(m_X(t))$ (cumulant generating function)

        $$
        \Longrightarrow \quad \begin{cases}
        E[X^k] = \dfrac{d^k}{dt^k} \Big|_{t=0}\, m_X(t) \\[10pt]
        E[(X - \mu_X)^k] = \dfrac{d^k}{dt^k} \Big|_{t=0}\, K_X(t) \qquad (\text{for } k = 2, 3)
        \end{cases}
        $$

    **Today:** families of continuous random variables &nbsp; $\leadsto$ &nbsp; uniform, beta, Gaussian, chi-squared
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, HALF, arrow, blank, definition, mo, theorem):
    _fig, _ax = blank(HALF, 1.8, (-1.0, 4.3), (-0.6, 2.05))
    arrow(_ax, (-0.3, 0), (4.2, 0), "black", lw=0.9)
    arrow(_ax, (0, -0.2), (0, 1.95), "black", lw=0.9)
    _ax.plot([1, 1], [0, 1.2], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([3, 3], [0, 1.2], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([1, 3], [1.2, 1.2], color=BLUE, lw=1.4)
    _ax.plot([-0.07, 0.07], [1.2, 1.2], color="black", lw=0.9)
    _ax.text(-0.18, 1.2, r"$\frac{1}{b-a}$", ha="right", va="center", fontsize=15)
    _ax.text(1, -0.14, "$a$", ha="center", va="top", fontsize=13)
    _ax.text(3, -0.14, "$b$", ha="center", va="top", fontsize=13)
    _ax.text(4.2, -0.14, "$y$", ha="center", va="top", fontsize=13)

    mo.vstack(
        [
            mo.md(
                r"""
    ## II.8 &nbsp; Uniform, beta and Gaussian distributions

    ### The uniform distribution
    """
            ),
            definition(
                r"""
    A **uniform model** is a random experiment that

    1. consists of a single occurrence along $(a, b)$
    2. the probability of occurrence in any subinterval is proportional to its length (all are equally likely)
    3. measures the position of the occurrence
    """,
                "Uniform model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; a bakery is open from 9AM to 9PM; assuming sales are equally likely at any time

    $$
    Y = \text{clock time of a sale} \ (9 = \text{9AM}) \quad \leadsto \quad S_Y = (9, 21)
    $$

    $$
    \Longrightarrow \quad P(Y \leq y) = \frac{y - 9}{21 - 9} = \frac{y - 9}{12}
    \qquad \Longrightarrow \quad f_Y(y) = \frac{1}{12}, \quad y \in (9, 21)
    $$
    """
            ),
            definition(
                r"""
    A random variable $Y$ has **uniform distribution** over $[a, b]$ if its pdf is

    $$
    \underbrace{f_Y(y)}_{\mathrm{Unif}(a, b)(y)} = \begin{cases} \dfrac{1}{b - a}, & y \in (a, b) \\[8pt] 0, & y \notin (a, b) \end{cases}
    $$
    """,
                "Uniform distribution",
            ),
            theorem(
                r"""
    Given $Y \sim \mathrm{Unif}(a, b)$

    $$
    E[Y] = \int_a^b y\, \frac{1}{b - a}\, dy = \frac{y^2 / 2}{b - a}\, \Big|_a^b = \frac{1}{2}\, \frac{b^2 - a^2}{b - a} = \frac{a + b}{2}
    $$

    $$
    \mathrm{Var}(Y) = \frac{(b - a)^2}{12}, \qquad \mathrm{Skew}(Y) = 0
    $$
    """,
                "Mean, variance and skewness of the uniform distribution",
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### The beta distribution"""),
            definition(
                r"""
    A **beta model** is a random experiment that

    1. consists of a fixed number $n$ of occurrences along a unit interval $(0, 1)$
    2. each occurrence being independent and following a uniform model on $(0, 1)$
    3. measure the position $Y$ of the $r$th occurrence
    """,
                "Beta model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; a bakery sells 10 cakes in one shift; &nbsp; $Y$ = time (in “shifts”) until sale of the 3rd cake &nbsp; (assuming sales are equally likely at any time)

    $$
    \Longrightarrow \quad S_Y = (0, 1), \qquad f_Y(y) = \ ?
    $$

    Let $X = \#(\text{cakes sold in } y \text{ shifts})$, &nbsp; $y \in (0, 1)$

    (2) $\Longrightarrow$ each sale happens in $(0, y)$ with probability $y$ &nbsp; $\Longrightarrow$ &nbsp; $X \sim \mathrm{Binom}(10, y)$

    $$
    \Longrightarrow \quad P(Y \leq y) = P(X \geq 3) = \sum_{x=3}^{10} \binom{10}{x} y^x (1 - y)^{10-x}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad f_Y(y) &= \frac{d}{dy} \left[ \sum_{x=3}^{10} \binom{10}{x} y^x (1 - y)^{10-x} \right] \\[4pt]
    &= \sum_{x=3}^{10} \underbrace{\binom{10}{x} x}_{10 \binom{9}{x-1}}\, y^{x-1} (1 - y)^{10-x} - \sum_{x=3}^{9} \underbrace{\binom{10}{x} (10 - x)}_{10 \binom{9}{x},\ x \neq 10}\, y^x (1 - y)^{9-x} \\[4pt]
    &= 10 \left[ \sum_{x=3}^{10} \binom{9}{x - 1} y^{x-1} (1 - y)^{10-x} - \sum_{x=3}^{9} \binom{9}{x} y^x (1 - y)^{9-x} \right] \\[4pt]
    &= 10 \left[ \sum_{\tilde{x}=2}^{9} \binom{9}{\tilde{x}} y^{\tilde{x}} (1 - y)^{9-\tilde{x}} - \sum_{x=3}^{9} \binom{9}{x} y^x (1 - y)^{9-x} \right] \\[4pt]
    &= 10 \binom{9}{2} y^2 (1 - y)^7 = n \binom{n - 1}{r - 1} y^{r-1} (1 - y)^{n-r}, \qquad y \in (0, 1)
    \end{aligned}
    $$

    **Remark.** $r$ = target occurrence counting from the start; &nbsp; $n - r + 1$ = target occurrence counting from the end
    """
            ),
            definition(
                r"""
    A random variable $Y$ has a **beta distribution** with parameters $\alpha$ and $\beta$ if its pdf is

    $$
    \underbrace{f_Y(y)}_{\mathrm{Beta}(\alpha, \beta)(y)} = \frac{(\alpha + \beta - 1)!}{(\alpha - 1)!\,(\beta - 1)!}\, y^{\alpha-1} (1 - y)^{\beta-1}, \qquad y \in (0, 1) \qquad (\alpha, \beta > 0)
    $$

    ($\alpha = r$: counting from start; &nbsp; $\beta = n - r + 1$: counting from end)
    """,
                "Beta distribution",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    b_n = mo.ui.slider(1, 30, 1, value=10, label="$n$", show_value=True)
    return (b_n,)


@app.cell(hide_code=True)
def _(mo):
    b_r = mo.ui.slider(1, 30, 1, value=3, label="$r$", show_value=True)
    return (b_r,)


@app.cell(hide_code=True)
def _(mo):
    b_y = mo.ui.slider(0, 1, 0.01, value=0.25, label="$y$", show_value=True)
    return (b_y,)


@app.cell(hide_code=True)
def _(mo):
    b_redo = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Repeat")
    return (b_redo,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, LIGHT, b_n, b_r, b_redo, b_y, math, mo, np, table):
    _n, _r, _y0 = b_n.value, b_r.value, b_y.value
    _ok = _r <= _n
    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}

    # Simulation of the beta model: n uniform points per run, the r-th from the left
    _rng = np.random.default_rng(1212 + b_redo.value)
    _runs, _rows = 10000, 10
    _pts = np.sort(_rng.random((_runs, _n)), axis=1)

    _fig = Figure(figsize=(FULL, 5.0), layout="constrained")
    _top, _bot = _fig.subplots(2, 1, height_ratios=[1, 1.4])
    for _k in range(_rows):
        _top.plot(_pts[_k], np.full(_n, -_k), "|", color="black", ms=8, mew=1.0)
        if _ok:
            _top.plot(_pts[_k, _r - 1], -_k, "o", mfc="none", mec=BLUE, ms=9, mew=1.4)
    _top.axvline(_y0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    _top.annotate("$y$", (_y0, 1), xycoords=("data", "axes fraction"), textcoords="offset points", xytext=(0, 3), ha="center", va="bottom", fontsize=13, color=GREY, annotation_clip=False)
    _top.set_xlim(0, 1)
    _top.set_ylim(-_rows + 0.4, 0.6)
    _top.set_yticks(-np.arange(_rows), np.arange(1, _rows + 1), fontsize=10)
    _top.set_ylabel("run")

    if _ok:
        _c = _n * math.comb(_n - 1, _r - 1)
        _y = np.linspace(0, 1, 400)
        _pdf = _c * _y ** (_r - 1) * (1 - _y) ** (_n - _r)
        _cdf = sum(math.comb(_n, x) * _y0**x * (1 - _y0) ** (_n - x) for x in range(_r, _n + 1))
        _Y = _pts[:, _r - 1]
        _counts, _edges = np.histogram(_Y, bins=np.linspace(0, 1, 51), density=True)
        _m = _y <= _y0
        _bot.fill_between(_y[_m], _pdf[_m], color=LIGHT, lw=0)
        _bot.plot([_y0, _y0], [0, _c * _y0 ** (_r - 1) * (1 - _y0) ** (_n - _r)], color=GREY, lw=1.0)
        _bot.stairs(_counts, _edges, color=GREY, lw=0.9)
        _bot.plot(_y, _pdf, color=BLUE, lw=1.4)
        _bot.set_ylim(0, 1.35 * max(_pdf.max(), _counts.max()))
        # the two labels sit in the upper corner that the curve leaves free
        _x, _ha = (0.985, "right") if 2 * _r <= _n + 1 else (0.015, "left")
        _bot.text(_x, 0.96, rf"$\mathrm{{Beta}}({_r}, {_n - _r + 1})$", color=BLUE, fontsize=12, ha=_ha, va="top", transform=_bot.transAxes, bbox=_box)
        _bot.text(_x, 0.83, rf"$Y$ in {_runs:,} runs", color=GREY, fontsize=12, ha=_ha, va="top", transform=_bot.transAxes, bbox=_box)
        _values = [
            rf"$\textcolor{{{BLUE}}}{{\mathrm{{Beta}}({_r}, {_n - _r + 1})}}$",
            rf"${_cdf:.4f}$",
            rf"${(_Y <= _y0).mean():.4f}$",
            rf"${_r / (_n + 1):.4f}$",
            rf"${_r * (_n - _r + 1) / ((_n + 1) ** 2 * (_n + 2)):.5f}$",
        ]
    else:
        _bot.set_ylim(0, 1)
        _bot.text(0.5, 0.5, r"need $r \leq n$", fontsize=13, ha="center", va="center")
        _values = [r"need $r \leq n$"] * 5
    _bot.set_xlim(0, 1)
    _bot.set_xlabel("$y$")
    for _ax in (_top, _bot):
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

    _labels = [
        r"$Y \sim \mathrm{Beta}(r, n - r + 1)$ &nbsp; (the $r$th of $n$ uniform points, ringed in the first 10 runs)",
        r"$P(Y \le y) = P(X \ge r)$, &nbsp; $X \sim \mathrm{Binom}(n, y)$",
        rf"fraction of the {_runs:,} runs with $Y \le y$",
        r"$E[Y] = r/(n + 1)$",
        r"$\mathrm{Var}(Y) = r (n - r + 1) / ((n + 1)^2 (n + 2))$",
    ]
    mo.vstack(
        [
            mo.hstack([b_n, b_r, b_y, b_redo], justify="start", gap=2, wrap=True),
            table(list(zip(_labels, _values))),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** bakery sells 10 cakes in 12 hours (one shift)

    $$
    P(\text{sells 1st cake within 2 hours from opening}) = \ ?
    $$

    $Y$ = time (measured in “shifts”) until sales of 1st cake $\sim \mathrm{Beta}(1, 10)$

    $$
    \Longrightarrow \quad f_Y(y) = \frac{10!}{0!\, 9!}\, y^0 (1 - y)^9 = 10 (1 - y)^9
    $$

    1 shift $= 12$ hours, so 2 hours $= \tfrac{1}{6}$ shifts:

    $$
    \Longrightarrow \quad P(Y \leq \tfrac{1}{6}) = \int_0^{1/6} 10 (1 - y)^9\, dy = -(1 - y)^{10}\, \Big|_0^{1/6} = 1 - (1 - \tfrac{1}{6})^{10} \approx 0.84
    $$

    (with $\tfrac{1}{12}$ in place of $\tfrac{1}{6}$: $\approx 0.58$; &nbsp; with $\tfrac{0.5}{12}$: $\approx 0.35$)

    **Remark.** If $\tilde{Y}$ is the location of the $r$th point out of $n$ in $(a, b)$

    $$
    \Longrightarrow \quad f_{\tilde{Y}}(\tilde{y}) = \frac{1}{b - a}\, \mathrm{Beta}(r, n - r + 1)\!\left( \frac{\tilde{y} - a}{b - a} \right)
    $$
    """
            ),
            theorem(
                r"""
    Given $Y \sim \mathrm{Beta}(\alpha, \beta)$ &nbsp; ($\alpha = r$, $\beta = n - r + 1$)

    $$
    \begin{aligned}
    E[Y] &= \frac{\alpha}{\alpha + \beta} = \frac{r}{n + 1} \\[6pt]
    \mathrm{Var}(Y) &= \frac{\alpha \beta}{(\alpha + \beta)^2 (\alpha + \beta + 1)} = \frac{r (n - r + 1)}{(n + 1)^2 (n + 2)} \\[6pt]
    \mathrm{Skew}(Y) &= \frac{2 (\beta - \alpha) \sqrt{\alpha + \beta + 1}}{(\alpha + \beta + 2) \sqrt{\alpha \beta}} = \frac{2 (n + 1 - 2r) \sqrt{n + 2}}{(n + 3) \sqrt{r (n - r + 1)}}
    \end{aligned}
    $$
    """,
                "Mean, variance and skewness of the beta distribution",
            ),
            mo.md(
                r"""
    **Remark.** &nbsp; $\mathrm{Unif}(a, b)(y) = \dfrac{1}{b - a}\, \mathrm{Beta}(1, 1)\!\left( \dfrac{y - a}{b - a} \right)$

    ### The Gaussian distribution
    """
            ),
            definition(
                r"""
    A **Gaussian model** is a random experiment that

    1. consists of a large number $n \to \infty$ of occurrences along a large interval of radius $\ell \to \infty$, with fixed center $\mu$ and a fixed ratio $\ell^2 / n = \sigma^2$
    2. the location of each occurrence being independent and following a uniform distribution on $(\mu - \ell, \mu + \ell)$
    3. measures the location $X$ of the middle occurrence $m = \tfrac{n + 1}{2}$ (we can assume $n$ is odd) in the limit $n \to \infty$ (with $\ell^2 / n = \sigma^2$)
    """,
                "Gaussian model",
            ),
            mo.md(
                r"""
    Assuming $n = 2m - 1$, &nbsp; $X$ = location of the $m$th occurrence

    $$
    \Longrightarrow \quad U = \frac{X - (\mu - \ell)}{2\ell} \sim \mathrm{Beta}(m, m)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad f_X(x) &= \lim_{m \to \infty} \frac{1}{2\ell}\, \mathrm{Beta}(m, m)\!\left( \frac{1}{2} + \frac{x - \mu}{2\ell} \right) \qquad (\text{with } \ell^2 / n = \sigma^2) \\[6pt]
    &= \lim_{m \to \infty} \frac{1}{2\ell}\, \frac{(2m - 1)!}{(m - 1)!\,(m - 1)!} \left( \frac{1}{2} + \frac{x - \mu}{2\ell} \right)^{\!m-1} \left( \frac{1}{2} - \frac{x - \mu}{2\ell} \right)^{\!m-1} \\[6pt]
    &= \lim_{m \to \infty} \underbrace{\frac{1}{2\ell}\, m \binom{2m - 1}{m - 1} \frac{1}{4^{m-1}}}_{\textstyle \longrightarrow\ \frac{1}{\sqrt{2\pi\sigma^2}}}\ \underbrace{\left( 1 - \frac{(x - \mu)^2}{\ell^2} \right)^{\!m-1}}_{\textstyle \longrightarrow\ \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)} \\[6pt]
    &= \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    g_m = mo.ui.slider(1, 60, 1, value=2, label="$m$", show_value=True)
    return (g_m,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, RED, g_m, math, mo, np, table):
    _m = g_m.value
    _n = 2 * _m - 1
    _l = math.sqrt(_n)  # mu = 0, sigma^2 = 1
    _x = np.linspace(-4, 4, 801)
    _u = 0.5 + _x / (2 * _l)
    _inside = (_u > 0) & (_u < 1)
    _logc = math.lgamma(2 * _m) - 2 * math.lgamma(_m)
    _beta = np.zeros_like(_x)
    _beta[_inside] = np.exp(_logc + (_m - 1) * np.log(_u[_inside]) + (_m - 1) * np.log(1 - _u[_inside])) / (2 * _l)

    _box = {"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none"}
    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_x, np.exp(-(_x**2) / 2) / math.sqrt(2 * math.pi), color=RED, lw=1.4)
    _ax.plot(_x, _beta, color=BLUE, lw=1.4)
    _ax.text(-3.9, 0.6, r"$\dfrac{1}{2\ell}\, \mathrm{Beta}(m, m)\left( \dfrac{1}{2} + \dfrac{x}{2\ell} \right)$", color=BLUE, fontsize=13, ha="left", va="top", bbox=_box)
    _ax.text(3.9, 0.58, r"$\mathcal{N}(0, 1)(x)$", color=RED, fontsize=13, ha="right", va="top", bbox=_box)
    _ax.set_xlim(-4, 4)
    _ax.set_ylim(0, 0.62)
    _ax.set_xlabel("$x$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([g_m], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\mu, \ \sigma^2$", r"$0, \ 1$"),
                    (r"$n = 2m - 1$", rf"${_n}$"),
                    (r"$\ell = \sqrt{n \sigma^2}$", rf"${_l:.2f}$"),
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
            definition(
                r"""
    A random variable $X$ has **Gaussian** (Normal) **distribution** with mean $\mu$ and variance $\sigma^2$ if its pdf is

    $$
    \underbrace{f_X(x)}_{\mathcal{N}(\mu, \sigma^2)(x)} = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(x - \mu)^2}{2\sigma^2} \right), \qquad x \in (-\infty, +\infty)
    $$
    """,
                "Gaussian distribution",
            ),
            theorem(
                r"""
    $X \sim \mathcal{N}(\mu, \sigma^2)$

    $$
    E[X] = \mu, \qquad \mathrm{Var}(X) = \sigma^2, \qquad \mathrm{Skew}(X) = 0
    $$
    """,
                "Mean, variance and skewness of the Gaussian distribution",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(box):
    answers = tuple(box() for _ in range(6))
    return (answers,)


@app.cell(hide_code=True)
def _(answers, ask, mo):
    _c1, _e1, _v1, _c2, _e2, _v2 = answers
    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    Let $X$ have pdf $f_X(x) = \begin{cases} c\, x\, e^{-2x}, & x \in (0, +\infty) \\ 0, & x \notin (0, +\infty) \end{cases}$

    Find $c$, $E[X]$ and $\mathrm{Var}(X)$.
    """
            ),
            ask("$c =$", _c1, 4),
            ask("$E[X] =$", _e1, 1),
            ask(r"$\mathrm{Var}(X) =$", _v1, 0.5),
            mo.md(
                r"""
    ### Question 2

    Let $Y$ have pdf $f_Y(y) = \begin{cases} c\, y (1 - y)^2, & y \in (0, 1) \\ 0, & y \notin (0, 1) \end{cases}$

    Find $c$, $E[Y]$ and $\mathrm{Var}(Y)$.
    """
            ),
            ask("$c =$", _c2, 12),
            ask("$E[Y] =$", _e2, 0.4, 0.0005),
            ask(r"$\mathrm{Var}(Y) =$", _v2, 0.04, 0.0005),
            mo.md(
                r"""
    ### Question 3

    Let $Z \sim \mathcal{N}(0, 1)$, &nbsp; $f_Z(z) = \dfrac{1}{\sqrt{2\pi}}\, e^{-z^2/2}$, $z \in \mathbb{R}$

    Show that $m_Z(t) = e^{t^2/2}$, use $K_Z(t) = \ln(m_Z(t))$ to compute $E[Z]$, $\mathrm{Var}(Z)$, $\mathrm{Skew}(Z)$.

    Hint: &nbsp; $tz - \dfrac{z^2}{2} = \dfrac{t^2}{2} - \dfrac{(z - t)^2}{2}$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - uniform model (a single occurrence along $(a, b)$, all positions equally likely): $\mathrm{Unif}(a, b)(y) = \dfrac{1}{b - a}$ on $(a, b)$, with $E[Y] = \dfrac{a + b}{2}$, $\mathrm{Var}(Y) = \dfrac{(b - a)^2}{12}$, $\mathrm{Skew}(Y) = 0$
    - beta model (position of the $r$th of $n$ independent uniform occurrences along $(0, 1)$): $\mathrm{Beta}(\alpha, \beta)(y) = \dfrac{(\alpha + \beta - 1)!}{(\alpha - 1)!\,(\beta - 1)!}\, y^{\alpha-1} (1 - y)^{\beta-1}$ with $\alpha = r$, $\beta = n - r + 1$, and $E[Y] = \dfrac{\alpha}{\alpha + \beta}$
    - Gaussian model (middle occurrence of $n \to \infty$ uniform occurrences along $(\mu - \ell, \mu + \ell)$ with $\ell^2 / n = \sigma^2$): $\mathcal{N}(\mu, \sigma^2)(x) = \dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$, with $E[X] = \mu$, $\mathrm{Var}(X) = \sigma^2$, $\mathrm{Skew}(X) = 0$

    **Next:** the standard normal distribution; functions of random variables; quantiles
    """)
    return


if __name__ == "__main__":
    app.run()

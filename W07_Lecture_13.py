import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 13 · The standard normal distribution; functions of random variables; quantiles", css_file="bs202.css")


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
    header("Lecture 13", "Week 07", "Lecture 13 · The standard normal distribution; functions of random variables; quantiles")
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

    Families of continuous random variables

    - $\mathrm{Unif}(a, b)$, pdf $\dfrac{1}{b - a}$ &nbsp; $\leadsto$ &nbsp; measures position of occurrence in $(a, b)$, assuming probability $P((c, d)) = \dfrac{d - c}{b - a}$ for $(c, d) \subset (a, b)$
    - $\mathrm{Beta}(\alpha, \beta)$, pdf $\dfrac{(\alpha + \beta - 1)!}{(\alpha - 1)!\,(\beta - 1)!}\, x^{\alpha-1} (1 - x)^{\beta-1}$ &nbsp; $\leadsto$ &nbsp; measures position of the $\alpha$th occurrence in $(0, 1)$, out of $\alpha + \beta - 1$ uniform and independent total occurrences
    - $\mathcal{N}(\mu, \sigma^2)$, pdf $\dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$ &nbsp; $\leadsto$ &nbsp; measures position of middle occurrence in $(\mu - \ell, \mu + \ell)$, out of $n$ uniform and independent total occurrences, where $\ell \to +\infty$, $n = 2m - 1 \to +\infty$ with $\ell^2 / n = \sigma^2$ fixed
    - for $n = 2m - 1$, the middle is $\tfrac{n + 1}{2} = m$; &nbsp; $X$ = position of the $m$th occurrence on $(\mu - \ell, \mu + \ell)$

        $$
        \begin{aligned}
        \Longrightarrow \qquad f_X(x) &= \frac{1}{2\ell}\, \mathrm{Beta}(m, m)\Big( \underbrace{\frac{x - \mu + \ell}{2\ell}}_{\in\, (0, 1) \text{ if } x \,\in\, (\mu - \ell,\, \mu + \ell)} \Big) \\[6pt]
        &= \frac{1}{2\ell}\, \frac{(2m - 1)!}{(m - 1)!\,(m - 1)!} \left( \frac{x - \mu + \ell}{2\ell} \right)^{\!m-1} \left( 1 - \frac{x - \mu + \ell}{2\ell} \right)^{\!m-1} \\[6pt]
        &= \underbrace{\frac{1}{2\ell}\, m \binom{2m - 1}{m - 1} \frac{1}{4^{m-1}}}_{\textstyle \longrightarrow\ \frac{1}{\sqrt{2\pi\sigma^2}}}\ \underbrace{\left( 1 - \frac{(x - \mu)^2}{\ell^2} \right)^{\!m-1}}_{\textstyle \longrightarrow\ \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)}
        \end{aligned}
        $$

    **In this lecture:** the standard normal distribution; functions of random variables; quantiles
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.9 &nbsp; The standard normal distribution; functions of random variables; quantiles

    ### The standard normal distribution
    """
            ),
            theorem(
                r"""
    $X \sim \mathcal{N}(\mu, \sigma^2)$

    $$
    E[X] = \mu, \qquad \mathrm{Var}(X) = \sigma^2, \qquad \mathrm{Skew}(X) = 0
    $$

    $$
    \leadsto \qquad m_X(t) = E[e^{tX}] = \exp\!\left( \mu t + \sigma^2 \frac{t^2}{2} \right) \qquad (\text{proved below})
    $$
    """,
                "Moments of the normal distribution",
            ),
            definition(
                r"""
    $$
    Z \sim \mathcal{N}(0, 1) \qquad \Longrightarrow \qquad f_Z(z) = \frac{1}{\sqrt{2\pi}} \exp\!\left( -\frac{z^2}{2} \right)
    $$

    $$
    \Longrightarrow \qquad \underbrace{F_Z(z)}_{P(Z \leq z)} = \int_{-\infty}^{z} \frac{1}{\sqrt{2\pi}} \exp\!\left( -\frac{w^2}{2} \right) dw = \Phi(z) \qquad \text{standard normal cdf}
    $$

    (no simple formula, but its values are well-known)
    """,
                "The standard normal distribution",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    z_val = mo.ui.slider(-3.5, 3.5, 0.05, value=1, label="$z$", show_value=True)
    return (z_val,)


@app.cell(hide_code=True)
def _(mo):
    z_a = mo.ui.slider(-3.5, 3.5, 0.05, value=-1, label="$a$", show_value=True)
    return (z_a,)


@app.cell(hide_code=True)
def _(mo):
    z_b = mo.ui.slider(-3.5, 3.5, 0.05, value=1, label="$b$", show_value=True)
    return (z_b,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, math, mo, np, table, z_a, z_b, z_val):
    def _Phi(v):
        return 0.5 * (1 + math.erf(v / math.sqrt(2)))

    def _pdf(v):
        return np.exp(-(np.asarray(v, dtype=float) ** 2) / 2) / math.sqrt(2 * math.pi)

    _z, _a, _b = z_val.value, z_a.value, z_b.value
    _fz = float(_pdf(_z))
    _w = np.linspace(-6.5, 6.5, 500)

    _fig = Figure(figsize=(FULL, 2.5), layout="constrained")
    _left, _right = _fig.subplots(1, 2)
    for _ax in (_left, _right):
        _ax.set_xlim(-6.5, 6.5)
        _ax.set_ylim(0, 0.52)
        _ax.set_yticks([])
        _ax.set_xticks(range(-4, 5, 2))
        _ax.tick_params(labelsize=12)
        for _s in ("top", "right", "left"):
            _ax.spines[_s].set_visible(False)

    # left: Phi(z) as the area below z
    _wz = np.linspace(-6.5, _z, 300)
    _left.fill_between(_wz, _pdf(_wz), color=LIGHT, lw=0)
    _left.plot([_z, _z], [0, _fz], color=GREY, lw=1.0)
    _left.plot(_w, _pdf(_w), color=BLUE, lw=1.4)
    _left.plot(_z, _fz, "o", color=GREEN, ms=4, zorder=4)
    _left.annotate(r"$(z, f_Z(z))$", (_z, _fz), textcoords="offset points", xytext=(7, 7) if _z >= 0 else (-7, 7), ha="left" if _z >= 0 else "right", va="bottom", color=GREEN, fontsize=12)

    # right: P(a <= Z <= b) as the area between a and b
    if _a <= _b:
        _wab = np.linspace(_a, _b, 300)
        _right.fill_between(_wab, _pdf(_wab), color=LIGHT, lw=0)
        _between = rf"${_Phi(_b) - _Phi(_a):.4f}$"
    else:
        _between = r"need $a \leq b$"
    _right.plot(_w, _pdf(_w), color=BLUE, lw=1.4)
    for _v, _name, _first in ((_a, "$a$", _a <= _b), (_b, "$b$", _a > _b)):
        _right.plot([_v, _v], [0, 0.44], color=GREY, lw=1.0, ls=(0, (4, 3)))
        _right.annotate(_name, (_v, 0.44), textcoords="offset points", xytext=(-2, 3) if _first else (2, 3), ha="right" if _first else "left", va="bottom", fontsize=12)

    mo.vstack(
        [
            mo.hstack([z_val, z_a, z_b], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$f_Z(z)$", rf"$\textcolor{{{GREEN}}}{{{_fz:.4f}}}$"),
                    (r"$\Phi(z)$ &nbsp; (area, left)", rf"${_Phi(_z):.4f}$"),
                    (r"$1 - \Phi(z)$", rf"${1 - _Phi(_z):.4f}$"),
                    (r"$\Phi(-z)$", rf"${_Phi(-_z):.4f}$"),
                    (r"$P(a \leq Z \leq b) = \Phi(b) - \Phi(a)$ &nbsp; (area, right)", _between),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{aligned}
    \leadsto \qquad m_Z(t) = E[e^{tZ}] &= \int_{-\infty}^{\infty} e^{tz} f_Z(z)\, dz = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{tz} e^{-z^2/2}\, dz
    = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{\frac{t^2}{2} - \frac{(z - t)^2}{2}}\, dz \\[6pt]
    &= e^{t^2/2} \int_{-\infty}^{\infty} f_Z(z - t)\, dz = e^{t^2/2}
    \end{aligned}
    $$

    $$
    \leadsto \qquad K_Z(t) = \ln(m_Z(t)) = \frac{t^2}{2}
    $$

    $$
    \Longrightarrow \qquad E[Z] = K_Z'(0) = 0, \qquad \mathrm{Var}(Z) = K_Z''(0) = 1, \qquad \mathrm{Skew}(Z) = \frac{K_Z'''(0)}{\big( K_Z''(0) \big)^{3/2}} = 0
    $$
    """)
    return


@app.cell(hide_code=True)
def _(corollary, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Functions of random variables

    $X : S \longrightarrow \mathbb{R}$ random variable with cdf $F_X : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $u : \mathbb{R} \longrightarrow \mathbb{R}$ single variable function

    $$
    \Longrightarrow \qquad Y = u(X) = u \circ X : S \longrightarrow \mathbb{R} \quad \text{also random variable}
    $$

    If $u$ is **strictly increasing function** (in particular invertible!)

    $$
    \Longrightarrow \qquad F_Y(y) = P(Y \leq y) = P(u(X) \leq y) = P(X \leq u^{-1}(y)) = F_X(u^{-1}(y))
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad f_Y(y) &= \begin{cases}
    F_Y(y) - F_Y(y^-) = F_X(u^{-1}(y)) - F_X(u^{-1}(y^-)) & \text{discrete} \\[8pt]
    \dfrac{d}{dy} F_Y(y) = \dfrac{d}{dy} F_X(u^{-1}(y)) & \text{continuous}
    \end{cases} \\[10pt]
    &= \begin{cases}
    f_X(u^{-1}(y)) \\[8pt]
    \dfrac{d}{dy} u^{-1}(y)\ f_X(u^{-1}(y))
    \end{cases}
    \end{aligned}
    $$

    **Example.** &nbsp; $Y = aX + b$, &nbsp; $a > 0$

    $$
    \Longrightarrow \qquad f_Y(y) = \begin{cases}
    f_X\!\left( \dfrac{y - b}{a} \right) & \text{discrete} \\[10pt]
    \dfrac{1}{a}\, f_X\!\left( \dfrac{y - b}{a} \right) & \text{continuous}
    \end{cases}
    $$
    """
            ),
            theorem(
                r"""
    $Y = aX + b$, &nbsp; $\pm a > 0$

    $$
    \Longrightarrow \qquad m_Y(t) = E[e^{tY}] = E[e^{t(aX + b)}] = E[e^{taX} e^{tb}] = e^{tb}\, m_X(ta)
    $$

    $$
    \Longrightarrow \qquad E[Y] = a\, E[X] + b, \qquad \mathrm{Var}(Y) = a^2\, \mathrm{Var}(X), \qquad \mathrm{Skew}(Y) = \pm\, \mathrm{Skew}(X)
    $$
    """,
                "Linear transformation of a random variable",
            ),
            theorem(
                r"""
    $$
    X \sim \mathcal{N}(\mu, \sigma^2) \qquad \Longleftrightarrow \qquad Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)
    $$
    """,
                "Standardization",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $f_X(x) = \dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$

    $$
    \Longrightarrow \quad f_Z(z) = \frac{\partial}{\partial z} (\mu + \sigma z)\ f_X(\mu + \sigma z) = \sigma\, \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(\mu + \sigma z - \mu)^2}{2\sigma^2} \right) = \frac{1}{\sqrt{2\pi}} \exp\!\left( -\frac{z^2}{2} \right)
    $$

    Converse is the same…

    $$
    f_X(x) = \frac{\partial}{\partial x} \left( \frac{x - \mu}{\sigma} \right) f_Z\!\left( \frac{x - \mu}{\sigma} \right) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(x - \mu)^2}{2\sigma^2} \right) \qquad \square
    $$
    """
            ),
            corollary(
                r"""
    $$
    F_X(x) = P(X \leq x) = P\!\left( Z \leq \frac{x - \mu}{\sigma} \right) = \Phi\!\left( \frac{x - \mu}{\sigma} \right)
    $$

    $\Longrightarrow$ &nbsp; Gaussian cdfs are computed with $\Phi$
    """,
                "Normal cdf",
            ),
            corollary(
                r"""
    $Z \sim \mathcal{N}(0, 1)$ &nbsp; $\leadsto$ &nbsp; $X = \mu + \sigma Z \sim \mathcal{N}(\mu, \sigma^2)$

    $$
    \Longrightarrow \qquad m_X(t) = e^{t\mu}\, m_Z(t\sigma) = e^{t\mu + \frac{t^2}{2} \sigma^2}
    $$

    $$
    Y = aX + b \quad \Longrightarrow \quad m_Y(t) = e^{tb}\, m_X(ta) = e^{t(a\mu + b) + \frac{t^2}{2} a^2 \sigma^2} \quad \Longrightarrow \quad Y \sim \mathcal{N}(a\mu + b,\ a^2\sigma^2)
    $$

    (if $m_{Y_1}(t) = m_{Y_2}(t)$ around $t = 0$, then $Y_1$ and $Y_2$ have the same distribution!)

    $\Longrightarrow$ &nbsp; linear transformations of normal random variables are still normal random variables!
    """,
                "Linear transformations of normal random variables",
            ),
            mo.md(
                r"""
    **Example.** Midterm exam was too hard… with scores $X \sim \mathcal{N}(50, 20^2)$

    Grading scheme was designed based on $\mathcal{N}(75, 15^2)$:

    | | A | B | C | D | F |
    |:--|:-:|:-:|:-:|:-:|:-:|
    | $Y$ | $\geq 90$ | $\geq 75$ | $\geq 60$ | $\geq 50$ | |

    How can the instructor give fairer grades?

    $$
    Y = aX + b \sim \mathcal{N}(75, 15^2) \qquad \Longleftrightarrow \qquad \begin{cases} 75 = a\, 50 + b \\ 15^2 = a^2\, 20^2 \end{cases} \qquad \Longleftrightarrow \qquad \begin{cases} a = 3/4 \\ b = 37.5 \end{cases}
    $$

    $\mathcal{N}(50, 20^2)$ &nbsp; (to get same % of As, Bs, Cs, Ds, Fs):

    | | A | B | C | D | F |
    |:--|:-:|:-:|:-:|:-:|:-:|
    | $X$ | $\geq 70$ | $\geq 50$ | $\geq 30$ | $\geq 16.7$ | |

    $$
    P(X \geq 90) = 1 - P(X \leq 90) = 1 - \Phi\!\left( \frac{90 - 50}{20} \right) = 1 - \underbrace{\Phi(2)}_{\text{tabled}} \approx 1 - 0.977 = 2.3\% \ \text{ get A}
    $$

    $$
    \begin{aligned}
    P(X \geq 70) &= P\!\left( \frac{Y - b}{a} \geq 70 \right) = P(Y \geq 90) = 1 - P(Y \leq 90) = 1 - \Phi\!\left( \frac{90 - 75}{15} \right) \\
    &= 1 - \underbrace{\Phi(1)}_{\text{tabled}} \approx 1 - 0.841 = 15.9\% \ \text{ get A}
    \end{aligned}
    $$

    | $z$ | 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | $\Phi(z)$ | 0.5 | 0.691 | 0.841 | 0.933 | 0.977 | 0.994 | 0.999 |
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, LIGHT, mo, np):
    _fig = Figure(figsize=(HALF, 2.0), layout="constrained")
    _ax = _fig.subplots()
    _w = np.linspace(-3.5, 3.5, 400)
    _f = np.exp(-(_w**2) / 2) / np.sqrt(2 * np.pi)
    _c = 1.2
    _fc = float(np.exp(-(_c**2) / 2) / np.sqrt(2 * np.pi))
    _ax.fill_between(_w[_w <= -_c], _f[_w <= -_c], color=LIGHT, lw=0)
    _ax.fill_between(_w[_w >= _c], _f[_w >= _c], color=LIGHT, lw=0)
    for _v in (-_c, _c):
        _ax.plot([_v, _v], [0, _fc], color=GREY, lw=1.0)
    _ax.plot(_w, _f, color=BLUE, lw=1.4)
    _ax.text(-2.5, 0.2, r"$\Phi(z)$", fontsize=12, ha="center")
    _ax.text(2.45, 0.2, r"$1 - \Phi(w)$", fontsize=12, ha="center")
    _ax.set_xticks([-_c, 0, _c], ["$z$", "$0$", "$w$"])
    _ax.tick_params(labelsize=12)
    _ax.set_yticks([])
    _ax.set_xlim(-3.5, 3.5)
    _ax.set_ylim(0, 0.45)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            _fig,
            mo.md(
                r"""
    $$
    \text{symmetry} \qquad \Longrightarrow \qquad \Phi(-z) = 1 - \Phi(z)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    cut = mo.ui.slider(0, 100, 1, value=70, label="cutoff $x$ (on the scores $X$)", show_value=True)
    return (cut,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, LIGHT, RED, cut, math, mo, np, table):
    def _Phi(v):
        return 0.5 * (1 + math.erf(v / math.sqrt(2)))

    def _pdf(x, mu, s):
        return np.exp(-((np.asarray(x, dtype=float) - mu) ** 2) / (2 * s**2)) / math.sqrt(2 * math.pi * s**2)

    def _share(cuts, mu, sd):
        _F = [_Phi((v - mu) / sd) for v in cuts]
        return [1 - _F[0]] + [_F[i - 1] - _F[i] for i in range(1, 4)] + [_F[3]]

    _c = cut.value
    _y = 0.75 * _c + 37.5
    _x = np.linspace(-10, 120, 500)

    _fig = Figure(figsize=(FULL, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _xc = np.linspace(_c, 120, 300)
    _ax.fill_between(_xc, _pdf(_xc, 50, 20), color=LIGHT, lw=0)
    _ax.plot([_c, _c], [0, 0.031], color=GREY, lw=1.0, ls=(0, (4, 3)))
    _ax.plot(_x, _pdf(_x, 50, 20), color=BLUE, lw=1.4)
    _ax.plot(_x, _pdf(_x, 75, 15), color=RED, lw=1.4)
    _ax.text(_c, 0.0318, "$x$", fontsize=12, ha="center", va="bottom")
    _ax.text(36, 0.0375, r"$X \sim \mathcal{N}(50, 20^2)$", color=BLUE, fontsize=12, ha="center", va="center")
    _ax.text(88, 0.0375, r"$Y \sim \mathcal{N}(75, 15^2)$", color=RED, fontsize=12, ha="center", va="center")
    _ax.set_xlim(-10, 120)
    _ax.set_ylim(0, 0.041)
    _ax.set_yticks([])
    _ax.tick_params(labelsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _cuts_y = [90, 75, 60, 50]
    _cuts_x = [(v - 37.5) / 0.75 for v in _cuts_y]
    _grades = "\n".join(
        [
            "| grade | A | B | C | D | F |",
            "|:--|--:|--:|--:|--:|--:|",
            r"| cutoff on $Y \sim \mathcal{N}(75, 15^2)$ | " + " | ".join(rf"$\geq {v}$" for v in _cuts_y) + " | |",
            "| share | " + " | ".join(rf"${100 * v:.1f}\%$" for v in _share(_cuts_y, 75, 15)) + " |",
            r"| cutoff on $X \sim \mathcal{N}(50, 20^2)$ | " + " | ".join(rf"$\geq {v:.3g}$" for v in _cuts_x) + " | |",
            "| share | " + " | ".join(rf"${100 * v:.1f}\%$" for v in _share(_cuts_x, 50, 20)) + " |",
        ]
    )
    mo.vstack(
        [
            mo.hstack([cut], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$y = \tfrac{3}{4} x + 37.5$", rf"${_y:.2f}$"),
                    (r"$P(X \geq x) = 1 - \Phi\big( (x - 50)/20 \big)$ &nbsp; (area)", rf"$\textcolor{{{BLUE}}}{{{100 * (1 - _Phi((_c - 50) / 20)):.1f}\%}}$"),
                    (r"$P(Y \geq y) = 1 - \Phi\big( (y - 75)/15 \big)$", rf"$\textcolor{{{RED}}}{{{100 * (1 - _Phi((_y - 75) / 15)):.1f}\%}}$"),
                ]
            ),
            _fig,
            mo.md(_grades),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Quantiles"""),
            definition(
                r"""
    Given $X$ continuous random variable, with $f_X(x) > 0$ ($F_X$ strictly increasing), and given $p \in (0, 1)$, the **$p$-quantile** of $X$ is the number $q_p \in \mathbb{R}$ such that

    $$
    F_X(q_p) = \int_{-\infty}^{q_p} f_X(x)\, dx = P(X \leq q_p) = p
    $$

    $\leadsto$ &nbsp; a fraction $p$ of the probability is below the $p$-quantile &nbsp; (median $= q_{1/2}$, &nbsp; $k$th percentile $q_{k/100}$)
    """,
                "Quantile",
            ),
            mo.md(
                r"""
    For $Z \sim \mathcal{N}(0, 1)$ we write $z_p$ such that $\Phi(z_p) = p$

    | $p$ | 0.5 | 0.75 | 0.80 | 0.90 | 0.95 | 0.975 | 0.99 | 0.995 |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | $z_p$ | 0 | 0.674 | 0.842 | 1.282 | 1.645 | 1.960 | 2.326 | 2.576 |

    $$
    \Phi(-z) = 1 - \Phi(z) \qquad \Longrightarrow \qquad -z_p = z_{1-p}
    $$
    """
            ),
            theorem(
                r"""
    $$
    X \sim \mathcal{N}(\mu, \sigma^2) \qquad \Longrightarrow \qquad q_p(X) = \mu + \sigma z_p
    $$
    """,
                "Quantiles of the normal distribution",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    q_p = mo.ui.slider(0.01, 0.99, 0.005, value=0.95, label="$p$", show_value=True)
    return (q_p,)


@app.cell(hide_code=True)
def _(mo):
    q_mu = mo.ui.slider(-50, 150, 1, value=50, label=r"$\mu$", show_value=True)
    return (q_mu,)


@app.cell(hide_code=True)
def _(mo):
    q_sd = mo.ui.slider(1, 40, 0.5, value=20, label=r"$\sigma$", show_value=True)
    return (q_sd,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, LIGHT, math, mo, np, q_mu, q_p, q_sd, table):
    def _Phi(v):
        return 0.5 * (1 + math.erf(v / math.sqrt(2)))

    _p, _mu, _sd = q_p.value, q_mu.value, q_sd.value
    # z_p by bisection on Phi
    _lo, _hi = -6.0, 6.0
    for _k in range(60):
        _mid = (_lo + _hi) / 2
        _lo, _hi = (_mid, _hi) if _Phi(_mid) < _p else (_lo, _mid)
    _zp = (_lo + _hi) / 2
    _qp = _mu + _sd * _zp

    def _pdf(x):
        return np.exp(-((np.asarray(x, dtype=float) - _mu) ** 2) / (2 * _sd**2)) / math.sqrt(2 * math.pi * _sd**2)

    _x = np.linspace(_mu - 4 * _sd, _mu + 4 * _sd, 500)
    _top = float(_pdf(_mu))
    _fig = Figure(figsize=(FULL, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _xq = np.linspace(_x[0], _qp, 300)
    _ax.fill_between(_xq, _pdf(_xq), color=LIGHT, lw=0)
    _ax.plot(_x, _pdf(_x), color=BLUE, lw=1.4)
    _ax.plot([_qp, _qp], [0, 1.08 * _top], color=GREEN, lw=1.2, ls=(0, (4, 3)))
    _ax.text(_qp, 1.1 * _top, "$q_p$", color=GREEN, ha="center", va="bottom", fontsize=12)
    _ax.set_xlim(_x[0], _x[-1])
    _ax.set_ylim(0, 1.3 * _top)
    _ax.set_yticks([])
    _ax.tick_params(labelsize=12)
    _ax.set_xlabel("$x$", fontsize=12)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([q_p, q_mu, q_sd], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$z_p$ &nbsp; ($\Phi(z_p) = p$)", rf"${_zp + 0.0:.4f}$"),
                    (r"$q_p(X) = \mu + \sigma z_p$", rf"$\textcolor{{{GREEN}}}{{{_qp + 0.0:.3f}}}$"),
                    (r"$P(X \leq q_p)$ &nbsp; (area)", rf"${_Phi((_qp - _mu) / _sd):.4f}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - standard normal $Z \sim \mathcal{N}(0, 1)$: &nbsp; cdf $\Phi(z) = P(Z \leq z)$ (no simple formula, tabled), $\Phi(-z) = 1 - \Phi(z)$, &nbsp; $m_Z(t) = e^{t^2/2}$ &nbsp; $\Longrightarrow$ &nbsp; $E[Z] = 0$, $\mathrm{Var}(Z) = 1$, $\mathrm{Skew}(Z) = 0$
    - $Y = u(X)$ with $u$ strictly increasing: &nbsp; $F_Y(y) = F_X(u^{-1}(y))$ and, for $X$ continuous, $f_Y(y) \,{=}\, \tfrac{d}{dy} u^{-1}(y)\ f_X(u^{-1}(y))$
    - $Y = aX + b$: &nbsp; $m_Y(t) = e^{tb}\, m_X(ta)$ &nbsp; $\Longrightarrow$ &nbsp; $E[Y] = a\, E[X] + b$, $\mathrm{Var}(Y) = a^2\, \mathrm{Var}(X)$
    - $X \sim \mathcal{N}(\mu, \sigma^2)$ if and only if $Z = \dfrac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)$ &nbsp; $\Longrightarrow$ &nbsp; $F_X(x) = \Phi\!\left( \dfrac{x - \mu}{\sigma} \right)$; linear transformations of normal random variables are still normal: $aX + b \sim \mathcal{N}(a\mu + b,\ a^2\sigma^2)$
    - $p$-quantile: $F_X(q_p) = p$; &nbsp; for the normal distribution $q_p(X) = \mu + \sigma z_p$ with $\Phi(z_p) = p$
    """)
    return


if __name__ == "__main__":
    app.run()

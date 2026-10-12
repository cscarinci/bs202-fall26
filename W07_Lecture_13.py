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
    header("Lecture 13", "Week 07", "Lecture 13 · The standard normal distribution; functions of random variables; quantiles")
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Families of continuous RV

    - $\mathrm{Unif}(a, b) = \dfrac{1}{b - a}$ &nbsp; $\leadsto$ &nbsp; measures position of occurrence in $(a, b)$, assuming probability $P((c, d)) = \dfrac{d - c}{b - a}$ for $(c, d) \subset (a, b)$

    - $\mathrm{Beta}(\alpha, \beta) = \dfrac{(\alpha + \beta - 1)!}{(\alpha - 1)!\,(\beta - 1)!}\, x^{\alpha-1} (1 - x)^{\beta-1}$ &nbsp; $\leadsto$ &nbsp; measures position of $\alpha$ occurrence in $(0, 1)$, out of $\alpha + \beta - 1$ uniform and independent total occurrences

    - $\mathcal{N}(\mu, \sigma^2) = \dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$ &nbsp; $\leadsto$ &nbsp; measures position of middle occurrence in $(\mu - \ell, \mu + \ell)$, out of $n$ uniform and independent total occurrences, where $\ell \to +\infty$, $n = 2m - 1 \to +\infty$ with $\ell^2 / n = \sigma^2$ fixed

    For $n = 2m - 1$, the middle is $\tfrac{n + 1}{2} = m$; &nbsp; $X$ = position of $m$ occurrence on $(\mu - \ell, \mu + \ell)$

    $$
    \begin{aligned}
    \Longrightarrow \quad f_X(x) &= \frac{1}{2\ell}\, \mathrm{Beta}(m, m)\Big( \underbrace{\frac{x - \mu + \ell}{2\ell}}_{u \,\in\, (0, 1) \text{ if } x \,\in\, (\mu - \ell, \mu + \ell)} \Big) \\[6pt]
    &= \frac{1}{2\ell}\, \frac{(2m - 1)!}{(m - 1)!\,(m - 1)!} \left( \frac{x - \mu + \ell}{2\ell} \right)^{\!m-1} \left( 1 - \frac{x - \mu + \ell}{2\ell} \right)^{\!m-1} \\[6pt]
    &= \underbrace{\frac{1}{2\ell}\, m \binom{2m - 1}{m - 1} \frac{1}{4^{m-1}}}_{\textstyle \longrightarrow\ \frac{1}{\sqrt{2\pi\sigma^2}}}\ \underbrace{\left( 1 - \frac{(x - \mu)^2}{\ell^2} \right)^{\!m-1}}_{\textstyle \longrightarrow\ \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)}
    \end{aligned}
    $$
    """
            ),
            theorem(
                r"""
    $X \sim \mathcal{N}(\mu, \sigma^2)$

    $$
    E[X] = \mu, \qquad \mathrm{Var}(X) = \sigma^2, \qquad \mathrm{Skew}(X) = 0
    $$

    $$
    \leadsto \quad m_X(t) = E[e^{tX}] = \exp\!\left( \mu t + \sigma^2 \frac{t^2}{2} \right) \qquad (\text{will prove later!})
    $$
    """
            ),
            definition(
                r"""
    $$
    Z \sim \mathcal{N}(0, 1) \quad \Longrightarrow \quad f_Z(z) = \frac{1}{\sqrt{2\pi}} \exp\!\left( -\frac{z^2}{2} \right)
    $$

    $$
    \Longrightarrow \quad \underbrace{F_Z(z)}_{P(Z \leq z)} = \int_{-\infty}^{z} \frac{1}{\sqrt{2\pi}} \exp\!\left( -\frac{w^2}{2} \right) dw = \Phi(z) \qquad \text{standard normal cdf}
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
    z_a = mo.ui.slider(-3.5, 3.5, 0.05, value=-1, label="$a$", show_value=True)
    z_b = mo.ui.slider(-3.5, 3.5, 0.05, value=1, label="$b$", show_value=True)
    return z_a, z_b, z_val


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, math, mo, np, z_a, z_b, z_val):
    OCHRE = "#9a6b1f"
    _z = z_val.value
    _a, _b = sorted((z_a.value, z_b.value))
    _Phi = lambda v: 0.5 * (1 + math.erf(v / math.sqrt(2)))
    _phi = _Phi(_z)
    _w = np.linspace(-4, 4, 500)
    _f = np.exp(-(_w**2) / 2) / math.sqrt(2 * math.pi)

    _fig = Figure(figsize=(6.2, 2.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_w, _f, color=RED, lw=1.8)
    _m = _w <= _z
    _ax.fill_between(_w[_m], _f[_m], color=OCHRE, alpha=0.35, lw=0)
    _ab = (_w >= _a) & (_w <= _b)
    _ax.fill_between(_w[_ab], _f[_ab], facecolor="none", edgecolor=BLUE, hatch="///", lw=0)
    _fz = math.exp(-(_z**2) / 2) / math.sqrt(2 * math.pi)
    _ax.plot([_z, _z], [0, _fz], ":", color=GREEN, lw=1.3)
    _ax.plot(_z, _fz, "o", color=GREEN, ms=5)
    _ax.axhline(0, color="black", lw=0.8)
    _ax.axvline(0, color="black", lw=0.8)
    _ax.set_xlim(-4, 4)
    _ax.set_ylim(0, 0.45)
    _ax.set_yticks([])
    _ax.set_xlabel("$z$")
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $f_Z(z)$ | ${_fz:.4f}$ |",
            rf"| $\textcolor{{{OCHRE}}}{{\Phi(z)}}$ (shaded) | ${_phi:.4f}$ |",
            rf"| $1 - \Phi(z)$ | ${1 - _phi:.4f}$ |",
            rf"| $\Phi(-z)$ | ${_Phi(-_z):.4f}$ |",
            rf"| $\textcolor{{{BLUE}}}{{P(a \le Z \le b) = \Phi(b) - \Phi(a)}}$ (hatched) | ${_Phi(_b) - _Phi(_a):.4f}$ |",
        ]
    )
    mo.vstack([mo.hstack([z_val, z_a, z_b], justify="start", gap=3, wrap=True), mo.hstack([_fig, mo.md(_table)], widths=[3, 2], gap=2, align="center", wrap=True)])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, mo, np, theorem):
    _sym = Figure(figsize=(3.6, 2.2), layout="constrained")
    _sx = _sym.subplots()
    _w = np.linspace(-3.5, 3.5, 400)
    _f = np.exp(-(_w**2) / 2) / np.sqrt(2 * np.pi)
    _sx.plot(_w, _f, color=GREEN, lw=1.5)
    _sx.fill_between(_w[_w <= -1.2], _f[_w <= -1.2], facecolor="none", edgecolor=RED, hatch="///", lw=0)
    _sx.fill_between(_w[_w >= 1.2], _f[_w >= 1.2], facecolor="none", edgecolor=BLUE, hatch="\\\\\\", lw=0)
    _sx.text(-2.6, 0.17, r"$\Phi(z)$", color=RED, fontsize=12, ha="center")
    _sx.text(2.6, 0.17, r"$1 - \Phi(w)$", color=BLUE, fontsize=12, ha="center")
    _sx.set_xticks([-1.2, 1.2], ["$z$", "$w$"])
    _sx.set_yticks([])
    _sx.axhline(0, color="black", lw=0.8)
    _sx.axvline(0, color="black", lw=0.8)
    _sx.set_xlim(-3.5, 3.5)
    _sx.set_ylim(0, 0.45)
    for _s in ("top", "right", "left"):
        _sx.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.md(
                r"""
    $$
    \begin{aligned}
    \leadsto \quad m_Z(t) = E[e^{tZ}] &= \int_{-\infty}^{\infty} e^{tz} f_Z(z)\, dz = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{tz} e^{-z^2/2}\, dz \\[6pt]
    &= \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{\frac{t^2}{2} - \frac{(z - t)^2}{2}}\, dz = e^{t^2/2} \int_{-\infty}^{\infty} f_Z(z - t)\, dz = e^{t^2/2}
    \end{aligned}
    $$

    $$
    \leadsto \quad K_Z(t) = \ln(m_Z(t)) = \frac{t^2}{2}
    $$

    $$
    \Longrightarrow \quad E[Z] = K_Z'(0) = 0, \qquad \mathrm{Var}(Z) = K_Z''(0) = 1, \qquad \mathrm{Skew}(Z) = \frac{K_Z'''(0)}{\big( K_Z''(0) \big)^{3/2}} = 0
    $$

    ## Functions of RVs

    $X : S \longrightarrow \mathbb{R}$ RV with cdf $F_X : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $u : \mathbb{R} \longrightarrow \mathbb{R}$ single variable function

    $$
    \Longrightarrow \quad Y = u(X) = u \circ X : S \longrightarrow \mathbb{R} \quad \text{also RV}
    $$

    If $u$ is *strictly increasing function* (in particular invertible!)

    $$
    \Longrightarrow \quad F_Y(y) = P(Y \leq y) = P(u(X) \leq y) = P(X \leq u^{-1}(y)) = F_X(u^{-1}(y))
    $$

    $$
    \Longrightarrow \quad f_Y(y) = \begin{cases}
    F_Y(y) - F_Y(y^-) = F_X(u^{-1}(y)) - F_X(u^{-1}(y^-)) & \text{discrete} \\[8pt]
    \dfrac{d}{dy} F_Y(y) = \dfrac{d}{dy} F_X(u^{-1}(y)) & \text{continuous}
    \end{cases}
    \ = \ \begin{cases}
    f_X(u^{-1}(y)) \\[8pt]
    \dfrac{d}{dy} u^{-1}(y)\ f_X(u^{-1}(y))
    \end{cases}
    $$

    **Example.** &nbsp; $Y = aX + b$, &nbsp; $a > 0$

    $$
    \Longrightarrow \quad f_Y(y) = \begin{cases}
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
    \Longrightarrow \quad m_Y(t) = E[e^{tY}] = E[e^{t(aX + b)}] = E[e^{taX} e^{tb}] = e^{tb}\, m_X(ta)
    $$

    $$
    \Longrightarrow \quad E[Y] = a\, E[X] + b, \qquad \mathrm{Var}(Y) = a^2\, \mathrm{Var}(X), \qquad \mathrm{Skew}(Y) = \pm\, \mathrm{Skew}(X)
    $$
    """
            ),
            theorem(
                r"""
    $$
    X \sim \mathcal{N}(\mu, \sigma^2) \quad \Longleftrightarrow \quad Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)
    $$
    """
            ),
            mo.md(
                r"""
    $$
    f_X(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad f_Z(z) &= \frac{\partial}{\partial z} (\mu + \sigma z)\ f_X(\mu + \sigma z) = \sigma\, \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(\mu + \sigma z - \mu)^2}{2\sigma^2} \right) = \frac{1}{\sqrt{2\pi}} \exp\!\left( -\frac{z^2}{2} \right)
    \end{aligned}
    $$

    Converse is the same…

    $$
    f_X(x) = \frac{\partial}{\partial x} \left( \frac{x - \mu}{\sigma} \right) f_Z\!\left( \frac{x - \mu}{\sigma} \right) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left( -\frac{(x - \mu)^2}{2\sigma^2} \right) \qquad \square
    $$

    **Corollary.**

    $$
    F_X(x) = P(X \leq x) = P\!\left( Z \leq \frac{x - \mu}{\sigma} \right) = \Phi\!\left( \frac{x - \mu}{\sigma} \right)
    $$

    $\Longrightarrow$ &nbsp; Gaussian cdfs are computed with $\Phi$

    **Corollary.** &nbsp; $Z \sim \mathcal{N}(0, 1)$ &nbsp; $\leadsto$ &nbsp; $X = \mu + \sigma Z \sim \mathcal{N}(\mu, \sigma^2)$

    $$
    \Longrightarrow \quad m_X(t) = e^{t\mu}\, m_Z(t\sigma) = e^{t\mu + \frac{t^2}{2} \sigma^2}
    $$

    $$
    Y = aX + b \quad \Longrightarrow \quad m_Y(t) = e^{tb}\, m_X(ta) = e^{t(a\mu + b) + \frac{t^2}{2} a^2 \sigma^2}
    $$

    $$
    \Longrightarrow \quad Y \sim \mathcal{N}(a\mu + b,\ a^2\sigma^2)
    $$

    (if $m_{Y_1}(t) = m_{Y_2}(t)$ around $t = 0$, then $Y_1$ and $Y_2$ have the same distribution!)

    $\Longrightarrow$ &nbsp; linear transformations of normal RVs are still normal RVs!

    **Example.** Midterm exam was too hard… with scores $X \sim \mathcal{N}(50, 20^2)$

    Grading scheme was designed based on $\mathcal{N}(75, 15^2)$:

    | | A | B | C | D | F |
    |:--|:-:|:-:|:-:|:-:|:-:|
    | $Y$ | $\geq 90$ | $\geq 75$ | $\geq 60$ | $\geq 50$ | |

    How can the instructor give fairer grades?

    $$
    Y = aX + b \sim \mathcal{N}(75, 15^2) \quad \Longleftrightarrow \quad \begin{cases} 75 = a\, 50 + b \\ 15^2 = a^2\, 20^2 \end{cases} \quad \Longleftrightarrow \quad \begin{cases} a = 3/4 \\ b = 37.5 \end{cases}
    $$

    $\mathcal{N}(50, 20^2)$:

    | | A | B | C | D | F |
    |:--|:-:|:-:|:-:|:-:|:-:|
    | $X$ | $\geq 70$ | $\geq 50$ | $\geq 30$ | $\geq 16.7$ | |

    (to get same % of As, Bs, Cs, Ds, Fs)

    $$
    P(X \geq 90) = 1 - P(X \leq 90) = 1 - \Phi\!\left( \frac{90 - 50}{20} \right) = 1 - \Phi(2) \approx 1 - 0.977 = 2.3\% \ \text{ get A} \qquad (\Phi(2): \text{tabled})
    $$

    $$
    \begin{aligned}
    P(X \geq 70) &= P\!\left( \frac{Y - b}{a} \geq 70 \right) = P(Y \geq 90) = 1 - P(Y \leq 90) \\
    &= 1 - \Phi\!\left( \frac{90 - 75}{15} \right) = 1 - \Phi(1) \approx 1 - 0.841 = 15.9\% \ \text{ get A} \qquad (\Phi(1): \text{tabled})
    \end{aligned}
    $$

    | $z$ | 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | $\Phi(z)$ | 0.5 | 0.691 | 0.841 | 0.933 | 0.977 | 0.994 | 0.999 |

    """
            ),
            mo.hstack([_sym, mo.md(r"$$\text{symmetry} \quad \Longrightarrow \quad \Phi(-z) = 1 - \Phi(z)$$")], widths=[2, 3], gap=2, align="center", wrap=True),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    cut = mo.ui.slider(0, 100, 1, value=70, label="cutoff $x$ (on the scores $X$)", show_value=True)
    return (cut,)


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, cut, math, mo, np):
    _c = cut.value
    _Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
    _x = np.linspace(-10, 120, 500)
    _pdf = lambda x, mu, s: np.exp(-((x - mu) ** 2) / (2 * s**2)) / math.sqrt(2 * math.pi * s**2)

    _fig = Figure(figsize=(7.0, 2.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_x, _pdf(_x, 50, 20), color=RED, lw=1.8, label=r"$X \sim \mathcal{N}(50, 20^2)$")
    _ax.plot(_x, _pdf(_x, 75, 15), color=BLUE, lw=1.4, label=r"$Y \sim \mathcal{N}(75, 15^2)$")
    _m = _x >= _c
    _ax.fill_between(_x[_m], _pdf(_x[_m], 50, 20), color=RED, alpha=0.3, lw=0)
    _ax.axvline(_c, color="#555555", lw=1, ls="--")
    _ax.set_xlim(-10, 120)
    _ax.set_ylim(0, 0.04)
    _ax.set_yticks([])
    _ax.legend(frameon=False, fontsize=11, loc="upper left", ncols=2)
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _y = 0.75 * _c + 37.5
    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $y = \tfrac{{3}}{{4}} x + 37.5$ | ${_y:g}$ |",
            rf"| $P(X \geq x) = 1 - \Phi\big( (x - 50)/20 \big)$ | ${100 * (1 - _Phi((_c - 50) / 20)):.1f}\%$ |",
            rf"| $P(Y \geq y) = 1 - \Phi\big( (y - 75)/15 \big)$ | ${100 * (1 - _Phi((_y - 75) / 15)):.1f}\%$ |",
        ]
    )
    _cuts_y = [90, 75, 60, 50]
    _cuts_x = [(v - 37.5) / 0.75 for v in _cuts_y]
    _share = lambda cuts, mu, sd: [1 - _Phi((cuts[0] - mu) / sd)] + [_Phi((cuts[i - 1] - mu) / sd) - _Phi((cuts[i] - mu) / sd) for i in range(1, 4)] + [_Phi((cuts[3] - mu) / sd)]
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
    mo.vstack([cut, mo.md(_table), _fig, mo.md(_grades)])
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    Given $X$ continuous RV, with $f_X(x) > 0$ ($F_X$ strictly increasing), and given $p \in (0, 1)$, the **$p$-quantile** of $X$ is the number $q_p \in \mathbb{R}$ s.t.

    $$
    F_X(q_p) = \int_{-\infty}^{q_p} f_X(x)\, dx = P(X \leq q_p) = p
    $$

    A fraction $p$ of the probability is below the $p$-quantile &nbsp; (median $= q_{1/2}$, &nbsp; $k$th percentile $q_{k/100}$)
    """
            ),
            mo.md(
                r"""
    For $Z \sim \mathcal{N}(0, 1)$ we write $z_p$ s.t. $\Phi(z_p) = p$

    | $p$ | 0.5 | 0.75 | 0.80 | 0.90 | 0.95 | 0.975 | 0.99 | 0.995 |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | $z_p$ | 0 | 0.674 | 0.842 | 1.282 | 1.645 | 1.960 | 2.326 | 2.576 |

    $$
    \Phi(-z) = 1 - \Phi(z) \quad \Longrightarrow \quad -z_p = z_{1-p}
    $$
    """
            ),
            theorem(
                r"""
    $$
    X \sim \mathcal{N}(\mu, \sigma^2) \quad \Longrightarrow \quad q_p(X) = \mu + \sigma z_p
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    q_p = mo.ui.slider(0.01, 0.99, 0.005, value=0.95, label="$p$", show_value=True)
    q_mu = mo.ui.slider(-50, 150, 1, value=50, label=r"$\mu$", show_value=True)
    q_sd = mo.ui.slider(1, 40, 0.5, value=20, label=r"$\sigma$", show_value=True)
    return q_mu, q_p, q_sd


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, math, mo, np, q_mu, q_p, q_sd):
    _p, _mu, _sd = q_p.value, q_mu.value, q_sd.value
    _Phi = lambda v: 0.5 * (1 + math.erf(v / math.sqrt(2)))
    # z_p by bisection on Phi
    _lo, _hi = -6.0, 6.0
    for _ in range(60):
        _mid = (_lo + _hi) / 2
        _lo, _hi = (_mid, _hi) if _Phi(_mid) < _p else (_lo, _mid)
    _zp = (_lo + _hi) / 2
    _qp = _mu + _sd * _zp

    _x = np.linspace(_mu - 4 * _sd, _mu + 4 * _sd, 500)
    _f = np.exp(-((_x - _mu) ** 2) / (2 * _sd**2)) / math.sqrt(2 * math.pi * _sd**2)
    _fig = Figure(figsize=(7.0, 2.9), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_x, _f, color=RED, lw=1.8)
    _m = _x <= _qp
    _ax.fill_between(_x[_m], _f[_m], color=BLUE, alpha=0.25, lw=0)
    _ax.axvline(_qp, color=BLUE, lw=1.2, ls="--")
    _ax.text(_qp, max(_f) * 1.05, "$q_p$", color=BLUE, ha="center", fontsize=12)
    _ax.set_xlim(_x[0], _x[-1])
    _ax.set_ylim(0, max(_f) * 1.2)
    _ax.set_yticks([])
    _ax.set_xlabel("$x$")
    for _s in ("top", "right", "left"):
        _ax.spines[_s].set_visible(False)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $z_p$ &nbsp; ($\Phi(z_p) = p$) | ${_zp:.4f}$ |",
            rf"| $q_p(X) = \mu + \sigma z_p$ | ${_qp:.3f}$ |",
            rf"| $P(X \le q_p)$ (shaded) | ${_Phi((_qp - _mu) / _sd):.4f}$ |",
        ]
    )
    mo.vstack([mo.hstack([q_p, q_mu, q_sd], justify="start", gap=3, wrap=True), mo.hstack([_fig, mo.md(_table)], widths=[3, 2], gap=2, align="center", wrap=True)])
    return


if __name__ == "__main__":
    app.run()

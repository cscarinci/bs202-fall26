import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 13 · Standard normal, functions of random variables, quantiles", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(13, "Standard normal, functions of random variables, quantiles")
    return


@app.cell(hide_code=True)
def _(math, np):
    # Helpers of this lecture: the normal pdf and cdf, and the bare axes of a 1D density sketch

    def normal_pdf(x, mu=0.0, sd=1.0):
        """The pdf of N(mu, sd^2) at x (a number or an array)."""
        return np.exp(-((np.asarray(x, dtype=float) - mu) ** 2) / (2 * sd**2)) / math.sqrt(2 * math.pi * sd**2)

    def Phi(z):
        """The standard normal cdf."""
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    def density_axes(ax):
        """A density sketch: no y axis, only the x axis with its ticks."""
        ax.set_yticks([])
        ax.tick_params(labelsize=12)
        ax.spines["left"].set_visible(False)

    return Phi, density_axes, normal_pdf


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    z_val = lk.slider(-3, 3, step=0.05, value=1, label="$z$")
    cut = lk.slider(0, 100, step=1, value=70, label="$x$")
    q_p = lk.slider(0.01, 0.995, step=0.005, value=0.95, label="$p$")
    return cut, q_p, z_val


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(
            r"• &nbsp; $\mk{\mathrm{Unif}(a, b)}$ &nbsp; $\leadsto$ &nbsp; measures position of occurrence in $(a, b)$,",
            r"$\mathrm{Unif}(a, b) = \dfrac{1}{b - a}$",
        ),
        r"<span class='lk-ghost'>• &nbsp; $\mathrm{Unif}(a, b)$ &nbsp; $\leadsto$ &nbsp; </span>assuming probability $P((c, d)) = {\large\tfrac{d - c}{b - a}}$ for $(c, d) \subseteq (a, b)$",
        lk.gap(),
        lk.aside(
            r"• &nbsp; $\mk{\mathrm{Beta}(\alpha, \beta)}$ &nbsp; $\leadsto$ &nbsp; measures position of $\alpha$ occurrence in $(0, 1)$,",
            r"$\mathrm{Beta}(\alpha, \beta) = \dfrac{(\alpha + \beta - 1)!}{(\alpha - 1)! \, (\beta - 1)!} \, x^{\alpha - 1} (1 - x)^{\beta - 1}$",
        ),
        r"<span class='lk-ghost'>• &nbsp; $\mathrm{Beta}(\alpha, \beta)$ &nbsp; $\leadsto$ &nbsp; </span>out of $\alpha + \beta - 1$ uniform and independent total occurrences",
        lk.gap(),
        lk.aside(
            r"• &nbsp; $\mk{\mathcal{N}(\mu, \sigma^2)}$ &nbsp; $\leadsto$ &nbsp; measures position of middle occurrence in $(\mu - \ell, \mu + \ell)$,",
            r"$\mathcal{N}(\mu, \sigma^2) = \dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$",
        ),
        r"""
        <span class='lk-ghost'>• &nbsp; $\mathcal{N}(\mu, \sigma^2)$ &nbsp; $\leadsto$ &nbsp; </span>out of $n$ uniform and independent total occurrences

        <span class='lk-ghost'>• &nbsp; $\mathcal{N}(\mu, \sigma^2)$ &nbsp; $\leadsto$ &nbsp; </span>where $\ell \to +\infty$, $n = 2m - 1 \to +\infty$ with $\ell^2 / n = \sigma^2$ fixed
        """,
        lk.gap(),
        r"""
        For $n = 2m - 1$, the middle is ${\large\tfrac{n + 1}{2}} = m$

        > $X$ = position of $m$ occurrence on $(\mu - \ell, \mu + \ell)$
        """,
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \Longrightarrow \quad f_X(x) &= \frac{1}{2\ell} \, \mathrm{Beta}(m, m) \left( \mk{\frac{x - \mu + \ell}{2\ell}} \right)\\[4pt]
            &= \frac{1}{2\ell} \, \frac{(2m - 1)!}{(m - 1)! \, (m - 1)!} \left( \frac{x - \mu + \ell}{2\ell} \right)^{m - 1} \left( 1 - \frac{x - \mu + \ell}{2\ell} \right)^{m - 1}\\[4pt]
            &= \underbrace{\frac{1}{2\ell} \, m \binom{2m - 1}{m - 1} \frac{1}{4^{m - 1}}}_{\textstyle \longrightarrow {\large\tfrac{1}{\sqrt{2\pi\sigma^2}}}} \, \underbrace{\left( 1 - \frac{(x - \mu)^2}{\ell^2} \right)^{m - 1}}_{\textstyle \longrightarrow \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)}
            \end{aligned}
            $$
            """,
            [(1, r"$= u \in (0, 1)$ if $x \in (\mu - \ell, \mu + \ell)$")],
            rows=3,
        ),
        topic="Families of continuous random variables",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("WMS 4.2, 4.5, 6.3–6.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard normal
    # section
    lk.section("The standard normal distribution")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard normal
    # theorem: mean, variance and skewness of the normal distribution
    lk.theorem(
        [
            r"""
            $X \sim \mathcal{N}(\mu, \sigma^2)$

            $$
            E[X] = \mu, \qquad \mathrm{Var}(X) = \sigma^2, \qquad \mathrm{Skew}(X) = 0
            $$
            """,
            lk.aside(
                r"$\leadsto$ &nbsp; $m_X(t) = E[e^{tX}] = \exp\left( \mu t + \sigma^2 \frac{t^2}{2} \right)$",
                "will prove later!",
            ),
        ],
        label="thm-normal-moments",
    )
    return


@app.cell(hide_code=True)
def _(Figure, density_axes, lk, normal_pdf, np, z_val):
    # module: standard normal
    # definition: standard normal distribution
    # the bell curve, the point z with the value f_Z(z), and Phi(z) as the area left of z
    _z = z_val.value
    _fz = float(normal_pdf(_z))
    _w = np.linspace(-4, 4, 500)
    _fig = Figure(figsize=(5.6, 2.5), layout="constrained")
    _ax = _fig.subplots()
    _wz = np.linspace(-4, _z, 300)
    _ax.fill_between(_wz, normal_pdf(_wz), color=lk.LIGHT, lw=0)
    _ax.plot([_z, _z], [0, _fz], color=lk.GREY, lw=1.0)
    _ax.plot(_w, normal_pdf(_w), color=lk.BLUE, lw=1.4)
    _ax.plot(_z, _fz, "o", color=lk.GREEN, ms=4, zorder=4)
    _ax.annotate(r"$f_Z(z)$", (_z, _fz), textcoords="offset points", xytext=(26 * max(-1.0, min(1.0, _z / 0.6)), 7), ha="center", va="bottom", color=lk.GREEN, fontsize=12)
    _ax.text(-3.9, 0.2, r"$F_Z(z) = \Phi(z)$", fontsize=12, ha="left", va="bottom")
    _ax.set_xlim(-4, 4)
    _ax.set_ylim(0, 0.5)
    _ax.set_xticks(range(-3, 4))
    _ax.set_xlabel("$z$")
    density_axes(_ax)
    lk.definition(
        [
            r"$Z \sim \mathcal{N}(0, 1)$ &nbsp; $\Longrightarrow$ &nbsp; $f_Z(z) = \frac{1}{\sqrt{2\pi}} \exp(-z^2 / 2)$",
            lk.aside(
                r"> <span class='lk-ghost'>$Z \sim \mathcal{N}(0, 1)$ &nbsp; </span>$\Longrightarrow$ &nbsp; $\displaystyle \mk{F_Z(z)} = \int_{-\infty}^{z} \frac{1}{\sqrt{2\pi}} \exp(-w^2 / 2) \, dw = \Phi(z)$",
                r"$F_Z(z) = P(Z \leq z)$, standard normal cdf<br>(no simple formula, but its values are well-known)",
            ),
            lk.interactive(_fig, controls=[z_val]),
        ],
        title="the standard normal distribution",
        label="def-standard-normal",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: standard normal
    # prose: mgf, cgf and moments of Z
    lk.prose(
        r"""
        $$
        \begin{aligned}
        \leadsto \quad m_Z(t) = E[e^{tZ}] &= \int_{-\infty}^{\infty} e^{tz} f_Z(z) \, dz\\[4pt]
        &= \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{tz} e^{-z^2 / 2} \, dz = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{t^2 / 2 - (z - t)^2 / 2} \, dz\\[4pt]
        &= e^{t^2 / 2} \int_{-\infty}^{\infty} f_Z(z - t) \, dz = e^{t^2 / 2}
        \end{aligned}
        $$

        $\leadsto$ &nbsp; $K_Z(t) = \ln(m_Z(t)) = t^2 / 2$

        > $\Longrightarrow$ &nbsp; $E[Z] = K_Z'(0) = 0$, &nbsp; $\mathrm{Var}(Z) = K_Z''(0) = 1$, &nbsp; $\mathrm{Skew}(Z) = \dfrac{K_Z'''(0)}{(K_Z''(0))^{3/2}} = 0$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # section
    lk.section("Functions of random variables")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # prose: Y = u(X), its cdf and its pmf/pdf for u strictly increasing
    lk.prose(
        r"""
        $X : S \longrightarrow \mathbb{R}$ random variable with cdf $F_X : \mathbb{R} \longrightarrow \mathbb{R}$

        $u : \mathbb{R} \longrightarrow \mathbb{R}$ single variable function

        > $\Longrightarrow$ &nbsp; $Y = u(X) = u \circ X : S \longrightarrow \mathbb{R}$ also random variable
        """,
        lk.gap(),
        lk.aside(
            r"If $u$ is <span class='lk-mark'>strictly increasing function</span>",
            "in particular invertible!",
        ),
        r"""
        > $\Longrightarrow$ &nbsp; $F_Y(y) = P(Y \leq y) = P(u(X) \leq y) = P(X \leq u^{-1}(y)) = F_X(u^{-1}(y))$

        > $\Longrightarrow$ &nbsp; $f_Y(y) = \begin{cases} F_Y(y) - F_Y(y^-) = F_X(u^{-1}(y)) - F_X(u^{-1}(y^-)) & \text{discrete}\\[6pt] \dfrac{d}{dy} F_Y(y) = \dfrac{d}{dy} F_X(u^{-1}(y)) & \text{continuous} \end{cases}$

        > <span class='lk-ghost'>$\Longrightarrow$ &nbsp; $f_Y(y)$ </span>$= \begin{cases} f_X(u^{-1}(y))\\[6pt] \dfrac{d}{dy} u^{-1}(y) \, f_X(u^{-1}(y)) \end{cases}$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # example: linear function
    lk.example(
        r"""
        $Y = aX + b$, $a > 0$

        > $\Longrightarrow$ &nbsp; $f_Y(y) = \begin{cases} f_X\left( \dfrac{y - b}{a} \right) & \text{discrete}\\[8pt] \dfrac{1}{a} \, f_X\left( \dfrac{y - b}{a} \right) & \text{continuous} \end{cases}$
        """,
        label="ex-linear",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # theorem: mgf and moments of Y = aX + b
    lk.theorem(
        r"""
        $Y = aX + b$, $\pm a > 0$

        > $\Longrightarrow$ &nbsp; $m_Y(t) = E[e^{tY}] = E[e^{t(aX + b)}] = E[e^{taX} e^{tb}] = e^{tb} \, m_X(ta)$

        > $\Longrightarrow$ &nbsp; $E[Y] = a E[X] + b$, &nbsp; $\mathrm{Var}(Y) = a^2 \, \mathrm{Var}(X)$, &nbsp; $\mathrm{Skew}(Y) = \pm \, \mathrm{Skew}(X)$
        """,
        label="thm-linear",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # theorem: standardization
    lk.theorem(
        r"""
        $$
        X \sim \mathcal{N}(\mu, \sigma^2) \quad \Longleftrightarrow \quad Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)
        $$
        """,
        label="thm-standardization",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # proof: standardization
    lk.proof(
        r"""
        $f_X(x) = \dfrac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\dfrac{(x - \mu)^2}{2\sigma^2} \right)$

        > $$
        > \begin{aligned}
        > \Longrightarrow \quad f_Z(z) &= \frac{\partial}{\partial z} (\mu + \sigma z) \, f_X(\mu + \sigma z)\\[4pt]
        > &= \sigma \, \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(\mu + \sigma z - \mu)^2}{2\sigma^2} \right) = \frac{1}{\sqrt{2\pi}} \exp(-z^2 / 2)
        > \end{aligned}
        > $$

        Converse is the same…

        > $$
        > \begin{aligned}
        > f_X(x) &= \frac{\partial}{\partial x} \left( \frac{x - \mu}{\sigma} \right) f_Z\left( \frac{x - \mu}{\sigma} \right)\\[4pt]
        > &= \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
        > \end{aligned}
        > $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # corollary: normal cdfs from Phi
    lk.corollary(
        r"""
        $F_X(x) = P(X \leq x) = P\left( Z \leq \dfrac{x - \mu}{\sigma} \right) = \Phi\left( \dfrac{x - \mu}{\sigma} \right)$

        > $\Longrightarrow$ &nbsp; Gaussian cdfs are computed with $\Phi$
        """,
        label="cor-normal-cdf",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: functions of random variables
    # corollary: linear transformations of normal random variables
    lk.corollary(
        [
            r"""
            $Z \sim \mathcal{N}(0, 1)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $X = \mu + \sigma Z \sim \mathcal{N}(\mu, \sigma^2)$

            > $\Longrightarrow$ &nbsp; $m_X(t) = e^{t\mu} \, m_Z(t\sigma) = e^{t\mu + \frac{t^2}{2} \sigma^2}$

            $Y = aX + b$ &nbsp; $\Longrightarrow$ &nbsp; $m_Y(t) = e^{tb} \, m_X(ta) = e^{t(a\mu + b) + \frac{t^2}{2} a^2 \sigma^2}$
            """,
            lk.aside(
                r"> <span class='lk-ghost'>$Y = aX + b$ &nbsp; </span>$\Longrightarrow$ &nbsp; $Y \sim \mathcal{N}(a\mu + b, a^2 \sigma^2)$",
                r"$\begin{array}{c} \text{if } m_{Y_1}(t) = m_{Y_2}(t) \text{ around } t = 0 \\[2pt] \Downarrow \\[2pt] Y_1 \text{ and } Y_2 \text{ have the same distribution} \end{array}$",
            ),
            r"""
            > <span class='lk-ghost'>$Y = aX + b$ &nbsp; </span>$\Longrightarrow$ &nbsp; linear transformations of normal random variables

            > <span class='lk-ghost'>$Y = aX + b$ &nbsp; $\Longrightarrow$ &nbsp; </span>are still normal random variables!
            """,
        ],
        label="cor-linear-normal",
    )
    return


@app.cell(hide_code=True)
def _(Figure, cut, density_axes, lk, normal_pdf, np):
    # module: functions of random variables
    # example: fairer grades
    # the scores X ~ N(50, 20^2) (blue) and the scale Y = (3/4) X + 37.5 ~ N(75, 15^2) (red); the tail of X beyond the
    # cutoff x (shaded) has the same area as the tail of Y beyond the matching cutoff y (hatched); x chosen with the
    # slider
    _c = cut.value
    _y = 0.75 * _c + 37.5
    _x = np.linspace(-10, 120, 500)
    _fig = Figure(figsize=(5.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _xc = np.linspace(_c, 120, 300)
    _ax.fill_between(_xc, normal_pdf(_xc, 50, 20), color=lk.LIGHT, lw=0)
    _yc = np.linspace(min(_y, 120), 120, 300)
    _ax.fill_between(_yc, normal_pdf(_yc, 75, 15), facecolor="none", edgecolor=lk.RED, hatch="////", lw=0)
    _ax.plot([_c, _c], [0, 0.031], color=lk.BLUE, lw=1.0, ls=(0, (4, 3)))
    _ax.plot([_y, _y], [0, 0.031], color=lk.RED, lw=1.0, ls=(0, (4, 3)))
    _ax.text(_c, 0.0318, "$x$", color=lk.BLUE, fontsize=12, ha="center", va="bottom")
    _ax.text(_y, 0.0318, "$y$", color=lk.RED, fontsize=12, ha="center", va="bottom")
    _ax.plot(_x, normal_pdf(_x, 50, 20), color=lk.BLUE, lw=1.4)
    _ax.plot(_x, normal_pdf(_x, 75, 15), color=lk.RED, lw=1.4)
    _ax.text(20, 0.04, r"$X \sim \mathcal{N}(50, 20^2)$", color=lk.BLUE, fontsize=12, ha="center", va="center")
    _ax.text(104, 0.04, r"$Y \sim \mathcal{N}(75, 15^2)$", color=lk.RED, fontsize=12, ha="center", va="center")
    _ax.set_xlim(-10, 120)
    _ax.set_ylim(0, 0.043)
    density_axes(_ax)
    lk.example(
        [
            r"""
            Midterm exam was too hard… with scores $X \sim \mathcal{N}(50, 20^2)$

            Grading scheme was designed based on

            | | A | B | C | D | F |
            |:--|:--:|:--:|:--:|:--:|:--:|
            | $Y \sim \mathcal{N}(75, 15^2)$ | $\geq 90$ | $\geq 75$ | $\geq 60$ | $\geq 50$ | |

            How can the instructor give fairer grades?

            $Y = aX + b \sim \mathcal{N}(75, 15^2)$

            > $\Longleftrightarrow$ &nbsp; $\begin{cases} 75 = a \, 50 + b\\ 15^2 = a^2 \, 20^2 \end{cases}$ &nbsp; $\Longleftrightarrow$ &nbsp; $\begin{cases} a = 3/4\\ b = 37.5 \end{cases}$

            | | A | B | C | D | F |
            |:--|:--:|:--:|:--:|:--:|:--:|
            | $X \sim \mathcal{N}(50, 20^2)$ | $\geq 70$ | $\geq 50$ | $\geq 30$ | $\geq 16.7$ | |

            $\leadsto$ &nbsp; to get same % of As, Bs, Cs, Ds, Fs
            """,
            lk.gap(),
            lk.aside(
                r"""
                $$
                \begin{aligned}
                P(X \geq 90) &= 1 - P(X \leq 90) = 1 - \Phi\left( \frac{90 - 50}{20} \right)\\[4pt]
                &= 1 - \mk{\Phi(2)} \approx 1 - 0.977 = 2.3\% \text{ get A}
                \end{aligned}
                $$
                """,
                r"$\Phi(2)$ tabled",
                at="last",
            ),
            r"""
            $$
            \begin{aligned}
            P(X \geq 70) &= P\left( \frac{Y - b}{a} \geq 70 \right) = P(Y \geq 90)\\[4pt]
            &= 1 - P(Y \leq 90) = 1 - \Phi\left( \frac{90 - 75}{15} \right)\\[4pt]
            &= 1 - \Phi(1) \approx 1 - 0.841 = 15.9\% \text{ get A}
            \end{aligned}
            $$

            | $z$ | $0$ | $0.5$ | $1$ | $1.5$ | $2$ | $2.5$ | $3$ |
            |:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
            | $\Phi(z)$ | $0.5$ | $0.691$ | $0.841$ | $0.933$ | $0.977$ | $0.994$ | $0.999$ |
            """,
            lk.interactive(_fig, controls=[cut]),
        ],
        label="ex-grades",
    )
    return


@app.cell(hide_code=True)
def _(Figure, density_axes, lk, normal_pdf, np):
    # module: functions of random variables
    # prose: symmetry of Phi
    # Phi(z) as the area left of z, 1 - Phi(w) as the area right of w
    _fig = Figure(figsize=(3.6, 2.0), layout="constrained")
    _ax = _fig.subplots()
    _w = np.linspace(-3.5, 3.5, 400)
    _f = normal_pdf(_w)
    _c = 1.2
    _fc = float(normal_pdf(_c))
    _ax.fill_between(_w[_w <= -_c], _f[_w <= -_c], color=lk.LIGHT, lw=0)
    _ax.fill_between(_w[_w >= _c], _f[_w >= _c], color=lk.LIGHT, lw=0)
    for _v in (-_c, _c):
        _ax.plot([_v, _v], [0, _fc], color=lk.GREY, lw=1.0)
    _ax.plot(_w, _f, color=lk.BLUE, lw=1.4)
    _ax.text(-2.5, 0.2, r"$\Phi(z)$", fontsize=12, ha="center")
    _ax.text(2.45, 0.2, r"$1 - \Phi(w)$", fontsize=12, ha="center")
    _ax.set_xticks([-_c, 0, _c], ["$z$", "$0$", "$w$"])
    _ax.set_xlim(-3.5, 3.5)
    _ax.set_ylim(0, 0.45)
    density_axes(_ax)
    lk.prose(r"symmetry &nbsp; $\Longrightarrow$ &nbsp; $\Phi(-z) = 1 - \Phi(z)$", lk.figure(_fig))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quantiles
    # section
    lk.section("Quantiles")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quantiles
    # definition: p-quantile
    lk.definition(
        [
            lk.aside(
                r"Given $X$ continuous random variable, with $\mk{f_X(x) > 0}$, and given $p \in (0, 1)$,",
                r"$F_X$ strictly increasing",
            ),
            r"the **$p$-quantile** of $X$ is the number $q_p \in \mathbb{R}$ such that",
            r"""
            $$
            F_X(q_p) = \int_{-\infty}^{q_p} f_X(x) \, dx = P(X \leq q_p) = p
            $$
            """,
            lk.aside(
                r"$\leadsto$ &nbsp; a fraction $p$ of the probability is below the $p$-quantile",
                r"median $= q_{1/2}$, &nbsp; $k$th percentile $q_{k/100}$",
            ),
        ],
        label="def-quantile",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: quantiles
    # prose: quantiles of the standard normal
    lk.prose(
        r"""
        For $Z \sim \mathcal{N}(0, 1)$ we write $z_p$ such that $\Phi(z_p) = p$

        | $p$ | $0.5$ | $0.75$ | $0.80$ | $0.90$ | $0.95$ | $0.975$ | $0.99$ | $0.995$ |
        |:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
        | $z_p$ | $0$ | $0.674$ | $0.842$ | $1.282$ | $1.645$ | $1.960$ | $2.326$ | $2.576$ |

        $\Phi(-z) = 1 - \Phi(z)$ &nbsp; $\Longrightarrow$ &nbsp; $-z_p = z_{1-p}$
        """
    )
    return


@app.cell(hide_code=True)
def _(Figure, Phi, density_axes, lk, normal_pdf, np, q_p):
    # module: quantiles
    # theorem: quantiles of the normal distribution
    # the quantile q_p of X ~ N(50, 20^2): the area left of it is p; p chosen with the slider
    _p, _mu, _sd = q_p.value, 50, 20
    _lo, _hi = -6.0, 6.0
    for _k in range(60):  # z_p by bisection on Phi
        _mid = (_lo + _hi) / 2
        _lo, _hi = (_mid, _hi) if Phi(_mid) < _p else (_lo, _mid)
    _qp = _mu + _sd * (_lo + _hi) / 2
    _x = np.linspace(_mu - 4 * _sd, _mu + 4 * _sd, 500)
    _top = float(normal_pdf(_mu, _mu, _sd))
    _fig = Figure(figsize=(5.6, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _xq = np.linspace(_x[0], _qp, 300)
    _ax.fill_between(_xq, normal_pdf(_xq, _mu, _sd), color=lk.LIGHT, lw=0)
    _ax.plot(_x, normal_pdf(_x, _mu, _sd), color=lk.BLUE, lw=1.4)
    _ax.plot([_qp, _qp], [0, 1.08 * _top], color=lk.GREEN, lw=1.2, ls=(0, (4, 3)))
    _ax.text(_qp, 1.1 * _top, "$q_p$", color=lk.GREEN, ha="center", va="bottom", fontsize=12)
    _ax.text(_x[-1], 1.1 * _top, r"$X \sim \mathcal{N}(50, 20^2)$", color=lk.BLUE, ha="right", va="bottom", fontsize=12)
    _ax.set_xlim(_x[0], _x[-1])
    _ax.set_ylim(0, 1.3 * _top)
    _ax.set_xlabel("$x$")
    density_axes(_ax)
    lk.theorem(
        [
            r"""
            $$
            X \sim \mathcal{N}(\mu, \sigma^2) \quad \Longrightarrow \quad q_p(X) = \mu + \sigma z_p
            $$
            """,
            lk.interactive(_fig, controls=[q_p]),
        ],
        label="thm-normal-quantiles",
    )
    return


if __name__ == "__main__":
    app.run()

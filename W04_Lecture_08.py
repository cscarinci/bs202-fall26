import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 08 · Poisson models", css_file="bs202.css")


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
    header("Lecture 08", "Week 04", "Lecture 08 · Poisson models")
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
def _(math):
    def pois_pmf(m, x):
        """Pois(m)(x), computed through logarithms so that large m, x do not overflow."""
        return math.exp(-m + x * math.log(m) - math.lgamma(x + 1))

    def binom_pmf(n, p, x):
        """B(n, p)(x), zero outside 0 <= x <= n."""
        return math.comb(n, x) * p**x * (1 - p) ** (n - x) if 0 <= x <= n else 0.0

    def stems(ax, xs, ps, color, shift=0.0):
        """pmf plot: thin vertical stems with a dot."""
        _at = [x + shift for x in xs]
        ax.vlines(_at, 0, ps, color=color, lw=1.0)
        ax.plot(_at, ps, "o", color=color, ms=3.5 if len(xs) <= 60 else 2.0)

    def pmf_axis(ax, top):
        """Axis of a pmf plot, with head room for the labels of the two series."""
        ax.set_ylim(0, 1.25 * top)
        ax.set_xlabel("$x$")
        ax.xaxis.get_major_locator().set_params(integer=True)
        for _s in ("top", "right"):
            ax.spines[_s].set_visible(False)

    return binom_pmf, pmf_axis, pois_pmf, stems


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - binomial: &nbsp; $B(n, p)(x) = \dbinom{n}{x} p^x q^{n-x}, \quad 0 \leq x \leq n$
    - negative binomial: &nbsp; $NB(r, p)(y) = \dbinom{y - 1}{r - 1} p^r q^{y-r}, \quad y \geq r$
    - hypergeometric:

        $$
        \begin{gathered}
        HG(N, K, n)(x) = \frac{\dbinom{n}{x} \dbinom{N - n}{K - x}}{\dbinom{N}{K}} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}, \\[6pt]
        \max(0, n + K - N) \leq x \leq \min(n, K)
        \end{gathered}
        $$

    - negative hypergeometric:

        $$
        NHG(N, K, r)(y) = \frac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}} = \frac{K}{N}\, \frac{\dbinom{K - 1}{r - 1} \dbinom{N - K}{y - r}}{\dbinom{N - 1}{y - 1}}, \qquad r \leq y \leq N - K + r
        $$

    **In this lecture:** Poisson and gamma models

    **References:** WMS 3.8
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.5 &nbsp; Poisson models

    ### The Poisson model
    """
            ),
            definition(
                r"""
    A **Poisson model** is a random experiment that

    1. consists of occurrences along a continuous interval, with the number of occurrences in disjoint subintervals being independent of one another
    2. the average rate of occurrences is a constant $\lambda > 0$, and for small subintervals of length $h$ we have:

        $$
        P\left(\substack{\text{exactly one} \\ \text{occurrence}}\right) \approx \lambda h, \qquad P\left(\substack{\text{two or more} \\ \text{occurrences}}\right) \approx 0.
        $$

    3. measures the number $X$ of occurrences in a fixed interval of length $t$
    """,
                "Poisson model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; emails arrive with average rate $\lambda = 3$ per day; &nbsp; $X = \#(\text{emails in 7 days})$ &nbsp; $\Longrightarrow$ &nbsp; $S_X = \{0, 1, 2, \dots\}$

    To compute $f_X$

    (i) split $[0, t]$ into $n$ subintervals of length $h = t/n$

    (ii) for large $n$, each subinterval has 0 or 1 occurrence, with

    $$
    P(\text{exactly 1 occurrence}) \approx \lambda t/n, \qquad P(\text{no occurrences}) \approx 1 - \lambda t/n
    $$

    (iii) by assumption each subinterval is independent

    $\therefore$ &nbsp; we can think of our Poisson model as a sequence of identical independent **trials** (occurrences in each subinterval), each with one of two possible outcomes with

    $$
    P(\text{“success”}) \approx \lambda t/n, \qquad P(\text{“failure”}) \approx 1 - \lambda t/n \qquad (\text{“success”: occurrence})
    $$

    where we are measuring the number $X$ of “successes” in $n$ trials!

    $$
    \Longrightarrow \qquad f_X(x) \approx B(n, \lambda t/n)(x) \qquad (\text{for large } n)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad f_X(x) &= \lim_{n \to \infty} \binom{n}{x} \left( \frac{\lambda t}{n} \right)^{\!x} \left( 1 - \frac{\lambda t}{n} \right)^{\!n-x} \\[6pt]
    &= \lim_{n \to \infty} \underbrace{\frac{n (n - 1) \cdots (n - x + 1)}{n^x}}_{\approx\, 1}\, \frac{(\lambda t)^x}{x!} \left( 1 - \frac{\lambda t}{n} \right)^{\!n} \underbrace{\left( 1 - \frac{\lambda t}{n} \right)^{\!-x}}_{\approx\, 1} \\[6pt]
    &= \frac{(\lambda t)^x}{x!} \underbrace{\lim_{n \to \infty} \left( 1 - \frac{\lambda t}{n} \right)^{\!n}}_{e^{-\lambda t}} = e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} \qquad x = 0, 1, 2, \dots
    \end{aligned}
    $$

    ### The Poisson distribution
    """
            ),
            definition(
                r"""
    A random variable $X$ is said to have a **Poisson distribution** with rate $\lambda$ over an interval of length $t$ if its pmf is

    $$
    \underbrace{f_X(x)}_{\mathrm{Pois}(\lambda t)(x)} = \begin{cases} e^{-\lambda t}\, \dfrac{(\lambda t)^x}{x!}, & x = 0, 1, 2, \dots \\[8pt] 0, & x \neq 0, 1, 2, \dots \end{cases}
    \qquad (\lambda t: \text{single parameter})
    $$
    """,
                "Poisson distribution",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    lam_t = mo.ui.slider(0.5, 20, 0.5, value=2, label=r"$\lambda t$", show_value=True)
    n_sub = mo.ui.slider(1, 200, 1, value=10, label="$n$ (subintervals)", show_value=True)
    px = mo.ui.slider(0, 40, 1, value=0, label="$x$", show_value=True)
    p_redo = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Repeat")
    return lam_t, n_sub, p_redo, px


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, RED, binom_pmf, lam_t, math, mo, n_sub, np, p_redo, pmf_axis, pois_pmf, px, stems, table):
    _m, _n, _x = lam_t.value, n_sub.value, px.value
    _top = max(int(_m + 4 * math.sqrt(_m) + 4), _x + 1)
    _xs = list(range(_top + 1))
    _pois = [pois_pmf(_m, _k) for _k in _xs]
    _p = _m / _n
    _need = r"need $n \geq \lambda t$"

    _fig = Figure(figsize=(FULL, 4.0), layout="constrained")
    _ax, _tl = _fig.subplots(2, 1, height_ratios=[3, 1])
    _peak = max(_pois)
    if _p <= 1:
        _bin = [binom_pmf(_n, _p, _k) for _k in _xs]
        _peak = max(_peak, max(_bin))
        stems(_ax, _xs, _pois, BLUE, -0.12)
        stems(_ax, _xs, _bin, RED, 0.12)
        _bx = rf"$\textcolor{{{RED}}}{{{100 * _bin[_x]:.2f}\%}}$"
    else:
        stems(_ax, _xs, _pois, BLUE, -0.12)
        _bx = _need
    _ax.plot(_x - 0.12, _pois[_x], "o", color="black", mfc="none", ms=8, mew=1.0)
    pmf_axis(_ax, _peak)
    _ax.text(0.99, 0.99, r"$\mathrm{Pois}(\lambda t)$", color=BLUE, fontsize=12, ha="right", va="top", transform=_ax.transAxes)
    if _p <= 1:
        _ax.text(0.80, 0.99, r"$B(n, \lambda t/n)$", color=RED, fontsize=12, ha="right", va="top", transform=_ax.transAxes)

    # One realisation of the construction: n subintervals, each with an occurrence with probability λt/n
    _tl.set_xlim(-0.03, 1.03)
    _tl.set_ylim(-1.6, 1)
    _tl.axis("off")
    _tl.plot([0, 1], [0, 0], color="black", lw=0.9)
    _tl.vlines([_k / _n for _k in range(_n + 1)], -0.35, 0.35, color=GREY, lw=0.6)
    _tl.text(0, -0.6, "$0$", fontsize=12, ha="center", va="top")
    _tl.text(1, -0.6, "$t$", fontsize=12, ha="center", va="top")
    if _p <= 1:
        _rng = np.random.default_rng(808 + p_redo.value)
        _hits = np.nonzero(_rng.random(_n) < _p)[0]
        _tl.plot((_hits + 0.5) / _n, np.zeros(len(_hits)), "o", color="black", ms=4 if _n <= 100 else 2.5, zorder=4)
        _count = f"${len(_hits)}$"
    else:
        _count = _need

    _le = sum(pois_pmf(_m, _k) for _k in range(_x + 1))
    _ge = 1 - sum(pois_pmf(_m, _k) for _k in range(_x))
    mo.vstack(
        [
            mo.hstack([lam_t, px, n_sub, p_redo], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\mathrm{Pois}(\lambda t)(x) = e^{-\lambda t} (\lambda t)^x / x!$", rf"$\textcolor{{{BLUE}}}{{{100 * _pois[_x]:.2f}\%}}$"),
                    (r"$B(n, \lambda t/n)(x)$", _bx),
                    (r"$P(X \leq x)$", rf"${100 * _le:.2f}\%$"),
                    (r"$P(X \geq x)$", rf"${100 * abs(_ge):.2f}\%$"),
                    (r"$\lambda t/n$", rf"${_p:.3f}$"),
                    (r"occurrences in one run of the experiment with $n$ subintervals", _count),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    **Example.** In Hyeonpung, there is an average of 2 car accidents per month. What is more likely this month?

    $A$ = there will be no accidents; &nbsp; $B$ = there will be 3 or more accidents

    $\leadsto$ &nbsp; $X = \#(\text{accidents in one month})$

    $$
    P(X = 0) = e^{-2} \approx 13.5\%
    $$

    $$
    P(X \geq 3) = 1 - P(X < 3) = 1 - e^{-2} - e^{-2} \cdot 2 - e^{-2} \cdot \frac{4}{2!} = 1 - 5 e^{-2} \approx 32.3\%
    $$

    ### Mean, variance and skewness
    """
            ),
            theorem(
                r"""
    $X$ a Poisson random variable with rate $\lambda$ over a period $t$

    $$
    E[X] = \lambda t, \qquad \mathrm{Var}(X) = \lambda t, \qquad \mathrm{Skew}(X) = \frac{1}{\sqrt{\lambda t}}
    $$
    """,
                "Mean, variance and skewness of a Poisson random variable",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    E[X] = \sum_{x=0}^{\infty} x\, e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = \sum_{x=1}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{(x - 1)!}
    = \underbrace{\sum_{x-1=0}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^{x-1}}{(x - 1)!}}_{=\, 1} \cdot (\lambda t)
    $$

    $$
    \begin{aligned}
    \mathrm{Var}(X) &= E[X(X - 1)] + E[X] - E[X]^2 = \sum_{x=0}^{\infty} x (x - 1)\, e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} + \lambda t - (\lambda t)^2 \\[6pt]
    &= \underbrace{\sum_{x-2=0}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^{x-2}}{(x - 2)!}}_{1}\, (\lambda t)^2 + \lambda t - (\lambda t)^2 = \lambda t
    \end{aligned}
    $$

    $$
    \mathrm{Skew}(X) = E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = E\!\left[ \left( \frac{X - \lambda t}{\sqrt{\lambda t}} \right)^{\!3} \right] = \sum_{x=0}^{\infty} \left( \frac{x - \lambda t}{\sqrt{\lambda t}} \right)^{\!3} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = \cdots
    $$

    (we will learn later a simpler way…) $\square$

    ### Poisson approximation of the binomial

    **Remark.** $\mathrm{Pois}(\lambda t)$ is also useful as an approximation for $B(n, p)$ for large $n$, small $p$, with $\lambda t = np$

    $$
    B(n, p)(x) \approx \mathrm{Pois}(np)(x)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    an = mo.ui.slider(1, 500, 1, value=100, label="$n$", show_value=True)
    ap = mo.ui.slider(0.005, 0.95, 0.005, value=0.02, label="$p$", show_value=True)
    return an, ap


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, RED, an, ap, binom_pmf, math, mo, pmf_axis, pois_pmf, stems, table):
    _n, _p = an.value, ap.value
    _m = _n * _p
    _lo = max(0, int(_m - 4 * math.sqrt(_m) - 4))
    _top = int(_m + 4 * math.sqrt(_m) + 4)
    _xs = list(range(_lo, _top + 1))
    _bin = [binom_pmf(_n, _p, _k) for _k in _xs]
    _pois = [pois_pmf(_m, _k) for _k in _xs]
    _err = max(abs(binom_pmf(_n, _p, _k) - pois_pmf(_m, _k)) for _k in range(max(_n, _top) + 1))

    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax = _fig.subplots()
    stems(_ax, _xs, _bin, RED, 0.12)
    stems(_ax, _xs, _pois, BLUE, -0.12)
    pmf_axis(_ax, max(max(_bin), max(_pois)))
    _ax.text(0.99, 0.99, r"$\mathrm{Pois}(np)$", color=BLUE, fontsize=12, ha="right", va="top", transform=_ax.transAxes)
    _ax.text(0.83, 0.99, r"$B(n, p)$", color=RED, fontsize=12, ha="right", va="top", transform=_ax.transAxes)

    mo.vstack(
        [
            mo.hstack([an, ap], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$np$", rf"${_m:.3f}$"),
                    (r"$\max_x \lvert B(n, p)(x) - \mathrm{Pois}(np)(x) \rvert$", rf"${_err:.5f}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### The gamma model"""),
            definition(
                r"""
    A **gamma model** is a random experiment that

    1. consists of occurrences along a continuous interval, with the number of occurrences in disjoint subintervals being independent of one another
    2. the average rate of occurrences is a constant $\lambda > 0$, and for small subintervals of length $h$ we have:

        $$
        P\left(\substack{\text{exactly one} \\ \text{occurrence}}\right) \approx \lambda h, \qquad P\left(\substack{\text{two or more} \\ \text{occurrences}}\right) \approx 0.
        $$

    3. measures the length $Y$ until a fixed number $r$ of occurrences is achieved
    """,
                "Gamma model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; emails arriving at an average rate $\lambda = 3$ per day; &nbsp; $Y$ = time until the 2nd email (not necessarily an integer)

    $$
    S_Y = (0, \infty) \qquad (\text{not discrete!})
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(box):
    answers = tuple(box() for _ in range(6))
    pmf_answers = tuple(box() for _ in range(4))
    return answers, pmf_answers


@app.cell(hide_code=True)
def _(answers, ask, math, mo, pmf_answers):
    _e, _v, _n0, _n2, _y4, _z4 = answers
    mo.vstack(
        [
            mo.md(
                r"""
    ## Practice

    ### Question 1

    A box contains 5 red, 4 blue, 3 green balls. Select 3 without replacement, and let $X = \#(\text{red balls out of 3})$.

    (a) What is the pmf of $X$?
    """
            ),
            *[ask(rf"$f_X({_x}) =$", _f, _v, 0.005) for _x, _f, _v in zip(range(4), pmf_answers, (35 / 220, 105 / 220, 70 / 220, 10 / 220))],
            mo.md(r"(b) Find $E[X]$ and $\mathrm{Var}(X)$."),
            ask(r"$E[X] =$", _e, 1.25, 0.005),
            ask(r"$\mathrm{Var}(X) =$", _v, 3 * (5 / 12) * (7 / 12) * (9 / 11), 0.005),
            mo.md(
                r"""
    (c) If we allow replacement, what is the pmf?

    ### Question 2

    Defects occur along a cable according to a Poisson model with rate 0.5 per meter. Let $N = \#(\text{defects in the first 4 meters})$.

    (a) What is the pmf of $N$? What is its state space?

    (b) Find $P(N = 0)$ and $P(N \geq 2)$.
    """
            ),
            ask(r"$P(N = 0) =$", _n0, math.exp(-2), 0.005),
            ask(r"$P(N \geq 2) =$", _n2, 1 - 3 * math.exp(-2), 0.005),
            mo.md(
                r"""
    ### Question 3

    For the same cable above, let $Y$ = distance until 1st defect, $Z$ = distance until 2nd defect.

    (a) Express $\{Y > 4\}$ and $\{Z > 4\}$ as events involving $N$.

    (b) Find $P(\{Y > 4\})$ and $P(\{Z > 4\})$.
    """
            ),
            ask(r"$P(\{Y > 4\}) =$", _y4, math.exp(-2), 0.005),
            ask(r"$P(\{Z > 4\}) =$", _z4, 3 * math.exp(-2), 0.005),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - a Poisson model: independent occurrences along a continuous interval at a constant average rate $\lambda > 0$; $X$ = number of occurrences in a fixed interval of length $t$, $S_X = \{0, 1, 2, \dots\}$
    - splitting $[0, t]$ into $n$ subintervals gives $f_X(x) \approx B(n, \lambda t/n)(x)$, and in the limit $n \to \infty$:

        $$
        \mathrm{Pois}(\lambda t)(x) = e^{-\lambda t}\, \frac{(\lambda t)^x}{x!}, \qquad x = 0, 1, 2, \dots
        $$
    - $E[X] = \lambda t$, &nbsp; $\mathrm{Var}(X) = \lambda t$, &nbsp; $\mathrm{Skew}(X) = \dfrac{1}{\sqrt{\lambda t}}$
    - for large $n$, small $p$: &nbsp; $B(n, p)(x) \approx \mathrm{Pois}(np)(x)$
    - a gamma model measures instead the length $Y$ until the $r$-th occurrence, $S_Y = (0, \infty)$ (not discrete)

    **Next:** continuous random variables; gamma and exponential distributions
    """)
    return


if __name__ == "__main__":
    app.run()

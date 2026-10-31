import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 07 · Hypergeometric and negative hypergeometric models", css_file="bs202.css")


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
    header("Lecture 07", "Week 04", "Lecture 07 • Hypergeometric and negative hypergeometric models")
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
def _(Figure):
    def pmf_axes(xlabel, h=3.0):
        """A full-width figure with one axis for pmf plots: integer ticks, no top/right spines."""
        from matplotlib.ticker import FuncFormatter, MaxNLocator

        fig = Figure(figsize=(5.6, h), layout="constrained")
        ax = fig.subplots()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:g}$"))
        ax.set_xlabel(xlabel)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        return fig, ax

    def stems(ax, xs, ps, color, dx=0.0, dots=None):
        """A pmf as thin vertical stems with a dot, shifted sideways by `dx` to sit next to a second pmf;
        on a long range (more than 60 values) the stems would merge, so only the dots are drawn."""
        if (len(xs) > 60) if dots is None else dots:
            ax.plot(xs, ps, "o", color=color, ms=2.2)
        else:
            pos = [x + dx for x in xs]
            ax.vlines(pos, 0, ps, color=color, lw=1.0)
            ax.plot(pos, ps, "o", color=color, ms=3.5)

    return pmf_axes, stems


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - **Binomial models** &nbsp; <span class="nw">$\leadsto$ &nbsp; count</span> number of “successes” in a fixed number of trials

        <span class="chain">$\displaystyle S = \{\, c_1 c_2 \cdots c_n \mid c_i = H \text{ or } T \,\} \quad (n: \text{number of trials}),$ $\displaystyle \quad \underbrace{P(\{H\}) = p}_{\footnotesize \text{success}},$ $\displaystyle \quad \underbrace{P(\{T\}) = 1 - p = q}_{\footnotesize \text{failure}}$</span>

        <span class="chain">$\displaystyle P(\underbrace{c_1 c_2 \cdots c_n}_{\footnotesize r\ H\text{s}}) = p^r (1 - p)^{n-r} = p^r q^{n-r},$ $\displaystyle \quad X(c_1 c_2 \cdots c_n) = \#(H \text{ in } n \text{ trials})$</span>

        $$
        \Longrightarrow \qquad \underbrace{f_X(x)}_{\mathclap{\footnotesize B(n, p)(x)}\vphantom{\footnotesize B(n, p)(x)}} = \begin{cases} \dbinom{n}{x} p^x q^{n-x}, & \text{for } x = \underbrace{0, 1, 2, \dots, n}_{\footnotesize S_X} \\[8pt] 0, & \text{otherwise} \end{cases}
        $$

        ($\dbinom{n}{x}$: # combinations of $x$ objects in $n$ positions)

    - **Negative binomial models** &nbsp; <span class="nw">$\leadsto$ &nbsp; count</span> number of trials until a fixed target of successes is achieved

        $$
        \begin{aligned}
        S = \{\, c_1 \cdots c_{n-1} c_n \mid\ & n \geq r \ (n \text{ allowed to vary!}),\ c_n = H, \\
        & c_i = H \text{ or } T \text{ for } 1 \leq i \leq n - 1, \\
        & \text{and } \#(H \text{ in } c_1 \cdots c_{n-1}) = r - 1 \,\}
        \end{aligned}
        $$

        <span class="chain">$\displaystyle P(\underbrace{c_1 \cdots c_{n-1}}_{\footnotesize r - 1\ H\text{s}} \underbrace{c_n}_{\mathrlap{\footnotesize \text{always } = H}\vphantom{\footnotesize \text{always } = H}}) = p^r q^{n-r},$ $\displaystyle \quad Y(c_1 \cdots c_{n-1} c_n) = \#(\text{trials until } r\ H)$</span>

        $$
        \Longrightarrow \qquad \underbrace{f_Y(y)}_{\mathclap{\footnotesize NB(r, p)(y)}\vphantom{\footnotesize NB(r, p)(y)}} = \begin{cases} \dbinom{y - 1}{r - 1} p^r q^{y-r}, & \text{for } y = \underbrace{r, r + 1, \dots}_{\footnotesize S_Y} \\[8pt] 0, & \text{otherwise} \end{cases}
        $$

        ($\dbinom{y-1}{r-1}$: # combinations of $r - 1$ objects in $y - 1$ positions)
    """
            ),
            theorem(
                r"""
    $X$ binomial random variable with bias $p$ on $n$ trials, &nbsp; $Y$ negative binomial random variable with bias $p$ and target $r$

    $$
    \begin{aligned}
    E[X] &= \mu_X = np, & \qquad E[Y] &= \mu_Y = \frac{r}{p} \\[1.6em]
    \mathrm{Var}(X) &= \sigma_X^2 = npq, & \qquad \mathrm{Var}(Y) &= \sigma_Y^2 = \frac{rq}{p^2} \\[1.6em]
    \mathrm{Skew}(X) &= \gamma_X = \frac{q - p}{\sqrt{npq}}, & \qquad \mathrm{Skew}(Y) &= \gamma_Y = \frac{1 + q}{\sqrt{rq}}
    \end{aligned}
    $$
    """,
                "Mean, variance and skewness",
            ),
            mo.md(r"""**In this lecture:** hypergeometric and negative hypergeometric models

            **References:** WMS 3.7""").style({"display": "block"}),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.4 &nbsp; Hypergeometric and negative hypergeometric models

    ### Hypergeometric models
    """
            ),
            definition(
                r"""
    A **hypergeometric model** is an experiment that

    1. consists of a sequence of trials (not independent!)
    2. each single trial has one of two outcomes, with exactly $K$ possible “successes” and $N - K$ possible “failures” in total, with all combinations of the $K$ possible successes among the $N$ possible trials being equally likely
    3. measures the number $X$ of “successes” in a fixed number $n$ of trials
    """,
                "Hypergeometric model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; draw colored coins from a bag with $K$ red coins and $N - K$ blue coins and without replacing the coins; count $X = \#(\text{red coins in } n \text{ draws})$

    <span class="chain">$\displaystyle S = \{\, c_1 c_2 \cdots c_n \mid c_i = R \text{ or } B,\ i = 1, \dots, n \,\},$ $\displaystyle \quad S_X = \{0, 1, \dots, n\} \quad (\text{if } n \leq K \text{ and } n \leq N - K)$</span>

    $$
    P(\{c_1 c_2 \cdots c_n\}) = \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}} \qquad \text{if } X(c_1 c_2 \cdots c_n) = x
    $$

    $\leadsto$ &nbsp; $N = 5$, $K = 3$, $n = 3$:

    <span class="chain">$\displaystyle P(\{RBB\}) = \frac{3}{5} \cdot \frac{2}{4} \cdot \frac{1}{3} = \frac{\dbinom{5-3}{3-1}}{\dbinom{5}{3}} = \frac{1}{\dfrac{5!}{2!\,3!}},$ $\displaystyle \quad P(\{BRR\}) = \frac{2}{5} \cdot \frac{3}{4} \cdot \frac{2}{3} = \frac{\dbinom{5-3}{3-2}}{\dbinom{5}{3}} = \frac{2!}{\dfrac{5!}{2!\,3!}}$</span>

    $\leadsto$ &nbsp; $N = 9$, $K = 5$, $n = 4$:

    $$
    P(\{BBBR\}) = \frac{\dbinom{5}{4}}{\dbinom{9}{5}} = \frac{4}{9} \cdot \frac{3}{8} \cdot \frac{2}{7} \cdot \frac{5}{6}
    $$

    <span class="chain">$\displaystyle f_X(x) = \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}} \times \#(\text{outcomes with } x\ R\text{s})$ $\displaystyle = \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}} \times \dbinom{n}{x}$ $\displaystyle = \frac{\dbinom{n}{x} \dbinom{N - n}{K - x}}{\dbinom{N}{K}}$ $\displaystyle = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}$</span>
    """
            ),
            definition(
                r"""
    A random variable $X$ is said to have a **hypergeometric distribution** if its pmf is

    <span class="chain">$\displaystyle \underbrace{f_X(x)}_{\mathclap{\footnotesize HG(N, K, n)(x)}\vphantom{\footnotesize HG(N, K, n)(x)}} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}},$ $\displaystyle \quad \text{for } x \in \mathbb{Z},\ 0 \leq x \leq K \text{ and } 0 \leq n - x \leq N - K$</span>

    (and $f_X(x) = 0$ otherwise).
    """,
                "Hypergeometric distribution",
            ),
            mo.md(
                r"""
    **Example.** A factory produced 1000 devices, 50 defective. We check a sample of 100 distinct devices. Probability of 7 defective objects in the sample?

    <span class="chain">$\displaystyle X = \#(\text{of defective objects in a sample of } 100)$ $\displaystyle \quad \leadsto \quad HG(1000, 50, 100)(x) = \frac{\dbinom{50}{x} \dbinom{1000 - 50}{100 - x}}{\dbinom{1000}{100}} = f_X(x)$ $\displaystyle \quad \leadsto \quad f_X(7) \approx 11\%,$ $\displaystyle \quad f_X(5) \approx 19\%,$ $\displaystyle \quad f_X(3) \approx 14\%$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(r"""### Negative hypergeometric models"""),
            definition(
                r"""
    A **negative hypergeometric model** is an experiment that

    1. consists of a sequence of trials
    2. each single trial has one of two outcomes, with exactly $K$ possible “successes” and $N - K$ possible “failures” in total, with all combinations of the $K$ possible successes among the $N$ possible trials being equally likely
    3. measures the number $Y$ of trials until a fixed number $r$ of “successes” is achieved

    <span class="chain">$\displaystyle S_Y = \{r, r + 1, \dots, N - K + r\} \quad (r \leq K),$ $\displaystyle \quad \underbrace{f_Y(y)}_{\mathclap{\footnotesize NHG(N, K, r)(y)}\vphantom{\footnotesize NHG(N, K, r)(y)}} = \frac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}}$</span>
    """,
                "Negative hypergeometric model",
            ),
            mo.md(
                r"""
    **Remark.**

    | | replacement allowed | replacement not allowed |
    |:--|:-:|:-:|
    | # successes in $n$ trials | Binomial | Hypergeometric |
    | # trials until $r$ successes | Negative binomial | Negative hypergeometric |

    ### Mean and variance
    """
            ),
            theorem(
                r"""
    For $X$ a hypergeometric random variable, &nbsp; $Y$ a negative hypergeometric random variable

    $$
    \begin{aligned}
    E[X] &= n \frac{K}{N}, & \qquad \mathrm{Var}(X) &= n \frac{K}{N} \left( 1 - \frac{K}{N} \right) \frac{N - n}{N - 1} \\[2em]
    E[Y] &= r\, \frac{N + 1}{K + 1}, & \qquad \mathrm{Var}(Y) &= \frac{r (N + 1)(N - K)(K + 1 - r)}{(K + 1)^2 (K + 2)}
    \end{aligned}
    $$
    """,
                "Mean and variance",
            ),
            mo.md(
                r"""
    $$
    E[X] = np \quad \text{if } p = \frac{K}{N}, \qquad \mathrm{Var}(X) = np(1 - p) \times \underbrace{\frac{N - n}{N - 1}}_{\mathclap{\footnotesize \begin{matrix}\text{finite population} \\ \text{correction term}\end{matrix}}\vphantom{\footnotesize \begin{matrix}\text{finite population} \\ \text{correction term}\end{matrix}}}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    hN = mo.ui.slider(10, 1000, 10, value=1000, label="$N$", show_value=True)
    hK = mo.ui.slider(1, 200, 1, value=50, label="$K$", show_value=True)
    hn = mo.ui.slider(1, 200, 1, value=100, label="$n$", show_value=True)
    return hK, hN, hn


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, hK, hN, hn, math, mo, pmf_axes, stems, table):
    _N, _K, _n = hN.value, hK.value, hn.value
    _fig, _ax = pmf_axes("$x$")
    _ax.text(0, 1.03, "$HG(N, K, n)$", color=BLUE, fontsize=12, ha="left", va="bottom", transform=_ax.transAxes)
    _ax.text(1, 1.03, "$B(n, p)$,  $p = K/N$", color=RED, fontsize=12, ha="right", va="bottom", transform=_ax.transAxes)
    _ok = _K <= _N and _n <= _N
    if _ok:
        _p = _K / _N
        _lo, _hi = max(0, _n - (_N - _K)), min(_K, _n)
        _total = math.comb(_N, _n)
        # both pmfs on the full range x = 0, ..., n; HG is zero outside its support
        _xs = list(range(_n + 1))
        _hg = [math.comb(_K, _i) * math.comb(_N - _K, _n - _i) / _total if _lo <= _i <= _hi else 0.0 for _i in _xs]
        _bi = [math.comb(_n, _i) * _p**_i * (1 - _p) ** (_n - _i) for _i in _xs]
        _keep = [_i for _i in _xs if _hg[_i] > 5e-4 or _bi[_i] > 5e-4]
        _a, _b = _keep[0], _keep[-1]
        _mean = _n * _p
        _top = max(max(_hg), max(_bi))
        # HG is drawn only on S_X: no zero dots along the axis
        _on = [_i for _i in range(_a, _b + 1) if _lo <= _i <= _hi]
        _dots = _b - _a + 1 > 60
        stems(_ax, _on, [_hg[_i] for _i in _on], BLUE, -0.15, _dots)
        stems(_ax, _xs[_a : _b + 1], _bi[_a : _b + 1], RED, 0.15, _dots)
        _ax.set_xlim(min(_a, _mean) - 1, max(_b, _mean) + 1)
        _ax.set_ylim(0, 1.3 * _top)
        _ax.plot([_mean, _mean], [0, 1.06 * _top], color=GREEN, lw=1.0, ls=(0, (4, 3)))
        _ax.text(_mean, 1.12 * _top, "$nK/N = np$", color=GREEN, fontsize=12, ha="center", va="bottom")
        _c = (_N - _n) / (_N - 1)
        _fpc = rf"${_c:g}$" if (100 * (_N - _n)) % (_N - 1) == 0 else rf"${_c:.2f}$"
        _out = table([(r"finite population correction $(N - n)/(N - 1)$", _fpc)])
    else:
        _out = mo.md(r"need $K \leq N$ and $n \leq N$")

    mo.vstack(
        [
            mo.hstack([hN, hK, hn], justify="start", gap=2, wrap=True),
            _out,
        ]
        + ([_fig] if _ok else [])
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Proof.** Similar trick as for binomial

    $$
    x \binom{K}{x} = K \binom{K - 1}{x - 1}, \qquad y \binom{y - 1}{r - 1} = r \binom{y}{r}
    $$

    together with the binomial coefficient identity

    $$
    \binom{N}{n} = \sum_{\mathclap{\footnotesize \begin{matrix} 0 \leq x \leq K \\ 0 \leq n - x \leq N - K \end{matrix}}} \binom{K}{x} \binom{N - K}{n - x}
    $$

    $\leadsto$ &nbsp; $(1 + t)^N = (1 + t)^K (1 + t)^{N-K}$

    <span class="chain">$\displaystyle \sum_{n} \binom{N}{n} t^{N-n} = \sum_{x} \binom{K}{x} t^{K-x} \cdot \sum_{\ell} \binom{N - K}{\ell} t^{N-K-\ell}$ $\displaystyle = \sum_{x} \sum_{\ell} \binom{K}{x} \binom{N - K}{\ell} t^{N-x-\ell}$ $\displaystyle = \sum_{n} \Big[ \sum_{x} \binom{K}{x} \binom{N - K}{n - x} \Big] t^{N-n} \quad (x + \ell = n)$</span>

    and compare the coefficients of $t^{N-n}$ on both sides. <span class=qed>$\square$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    gN = mo.ui.slider(2, 200, 1, value=30, label="$N$", show_value=True)
    gK = mo.ui.slider(1, 60, 1, value=10, label="$K$", show_value=True)
    gr = mo.ui.slider(1, 20, 1, value=3, label="$r$", show_value=True)
    return gK, gN, gr


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, gK, gN, gr, math, mo, pmf_axes, stems):
    _N, _K, _r = gN.value, gK.value, gr.value
    _fig, _ax = pmf_axes("$y$")
    _ax.text(0, 1.03, "$NHG(N, K, r)$", color=BLUE, fontsize=12, ha="left", va="bottom", transform=_ax.transAxes)
    _ax.text(1, 1.03, "$NB(r, p)$,  $p = K/N$", color=RED, fontsize=12, ha="right", va="bottom", transform=_ax.transAxes)
    _ok = _K <= _N and _r <= _K
    if _ok:
        _p = _K / _N
        _total = math.comb(_N, _K)
        _last = _N - _K + _r

        def _nb(y):
            return math.comb(y - 1, _r - 1) * _p**_r * (1 - _p) ** (y - _r)

        # NHG lives on r, ..., N - K + r; NB has no upper end: continue until it is negligible
        _ys = list(range(_r, _last + 1))
        while _nb(_ys[-1] + 1) > 5e-4 or _ys[-1] + 1 < _r / _p:
            _ys.append(_ys[-1] + 1)
        _nhg = [math.comb(_y - 1, _r - 1) * math.comb(_N - _y, _K - _r) / _total if _y <= _last else 0.0 for _y in _ys]
        _nbs = [_nb(_y) for _y in _ys]
        _keep = [_i for _i in range(len(_ys)) if _nhg[_i] > 5e-4 or _nbs[_i] > 5e-4] or list(range(len(_ys)))
        _a, _b = _keep[0], _keep[-1]
        _mean = _r * (_N + 1) / (_K + 1)
        _top = max(max(_nhg), max(_nbs))
        # NHG is drawn only on S_Y = {r, ..., N - K + r}: no zero dots along the axis
        _on = [_i for _i in range(_a, _b + 1) if _ys[_i] <= _last]
        _dots = _b - _a + 1 > 60
        stems(_ax, [_ys[_i] for _i in _on], [_nhg[_i] for _i in _on], BLUE, -0.15, _dots)
        stems(_ax, _ys[_a : _b + 1], _nbs[_a : _b + 1], RED, 0.15, _dots)
        _ax.set_xlim(min(_ys[_a], _mean) - 1, max(_ys[_b], _mean) + 1)
        _ax.set_ylim(0, 1.3 * _top)
        _ax.plot([_mean, _mean], [0, 1.06 * _top], color=GREEN, lw=1.0, ls=(0, (4, 3)))
        _ax.text(_mean, 1.12 * _top, "$r(N+1)/(K+1)$", color=GREEN, fontsize=12, ha="center", va="bottom")

    # an invalid setting shows the message alone
    mo.vstack(
        [
            mo.hstack([gN, gK, gr], justify="start", gap=2, wrap=True),
            _fig if _ok else mo.md(r"need $K \leq N$ and $r \leq K$"),
        ]
    )
    return

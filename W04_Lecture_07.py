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
    header("Lecture 07", "Week 04", "Lecture 07 · Hypergeometric and negative hypergeometric models")
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
        from matplotlib.ticker import MaxNLocator

        fig = Figure(figsize=(7.4, h), layout="constrained")
        ax = fig.subplots()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel(xlabel)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        return fig, ax

    def stems(ax, xs, ps, color, dx=0.0):
        """A pmf as thin vertical stems with a dot, shifted sideways by `dx` to sit next to a second pmf;
        on a long range (more than 60 values) the stems would merge, so only the dots are drawn."""
        if len(xs) > 60:
            ax.plot(xs, ps, "o", color=color, ms=2.2)
        else:
            pos = [x + dx for x in xs]
            ax.vlines(pos, 0, ps, color=color, lw=1.0)
            ax.plot(pos, ps, "o", color=color, ms=3.5)

    def span(a, b):
        r"""The set of integers {a, ..., b} in LaTeX."""
        return rf"\{{{a}\}}" if a == b else rf"\{{{a}, {b}\}}" if b == a + 1 else rf"\{{{a}, \dots, {b}\}}"

    return pmf_axes, span, stems


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - **Binomial models** &nbsp; $\leadsto$ &nbsp; count number of “successes” in a fixed number of trials

        $$
        S = \{\, c_1 c_2 \cdots c_n \mid c_i = H \text{ or } T \,\} \quad (n: \text{number of trials}), \qquad
        \underbrace{P(\{H\}) = p}_{\text{success}}, \quad \underbrace{P(\{T\}) = 1 - p = q}_{\text{failure}}
        $$

        $$
        P(\underbrace{c_1 c_2 \cdots c_n}_{r\ H\text{s}}) = p^r (1 - p)^{n-r} = p^r q^{n-r}, \qquad X(c_1 c_2 \cdots c_n) = \#(H \text{ in } n \text{ trials})
        $$

        $$
        \Longrightarrow \qquad \underbrace{f_X(x)}_{B(n, p)(x)} = \begin{cases} \dbinom{n}{x} p^x q^{n-x}, & \text{for } x = \underbrace{0, 1, 2, \dots, n}_{S_X} \\[8pt] 0, & \text{otherwise} \end{cases}
        $$

        ($\tbinom{n}{x}$: # combinations of $x$ objects in $n$ positions)

    - **Negative binomial models** &nbsp; $\leadsto$ &nbsp; count number of trials until a fixed target of successes is achieved

        $$
        \begin{aligned}
        S = \{\, c_1 \cdots c_{n-1} c_n \mid\ & n \geq r \ (n \text{ allowed to vary!}),\ c_n = H,\ c_i = H \text{ or } T \text{ for } 1 \leq i \leq n - 1, \\
        & \text{and } \#(H \text{ in } c_1 \cdots c_{n-1}) = r - 1 \,\}
        \end{aligned}
        $$

        $$
        P(\underbrace{c_1 \cdots c_{n-1}}_{r - 1\ H\text{s}} \underbrace{c_n}_{\text{always } = H}) = p^r q^{n-r}, \qquad Y(c_1 \cdots c_{n-1} c_n) = \#(\text{trials until } r\ H)
        $$

        $$
        \Longrightarrow \qquad \underbrace{f_Y(y)}_{NB(r, p)(y)} = \begin{cases} \dbinom{y - 1}{r - 1} p^r q^{y-r}, & \text{for } y = \underbrace{r, r + 1, \dots}_{S_Y} \\[8pt] 0, & \text{otherwise} \end{cases}
        $$

        ($\tbinom{y-1}{r-1}$: # combinations of $r - 1$ objects in $y - 1$ positions)
    """
            ),
            theorem(
                r"""
    $X$ binomial random variable with bias $p$ on $n$ trials, &nbsp; $Y$ negative binomial random variable with bias $p$ and target $r$

    $$
    \begin{aligned}
    E[X] &= \mu_X = np, & E[Y] &= \mu_Y = \frac{r}{p} \\[4pt]
    \mathrm{Var}(X) &= \sigma_X^2 = npq, & \mathrm{Var}(Y) &= \sigma_Y^2 = \frac{rq}{p^2} \\[4pt]
    \mathrm{Skew}(X) &= \gamma_X = \frac{q - p}{\sqrt{npq}}, & \mathrm{Skew}(Y) &= \gamma_Y = \frac{1 + q}{\sqrt{rq}}
    \end{aligned}
    $$
    """,
                "Mean, variance and skewness",
            ),
            mo.md(r"**In this lecture:** hypergeometric and negative hypergeometric models"),
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

    $$
    S = \{\, c_1 c_2 \cdots c_n \mid c_i = R \text{ or } B,\ i = 1, \dots, n \,\}, \qquad S_X = \{0, 1, \dots, n\} \quad (\text{if } n \leq K \text{ and } n \leq N - K)
    $$

    $$
    P(\{c_1 c_2 \cdots c_n\}) = \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}} \qquad \text{if } X(c_1 c_2 \cdots c_n) = x
    $$

    $\leadsto$ &nbsp; $N = 5$, $K = 3$, $n = 3$:

    $$
    P(\{RBB\}) = \frac{3}{5} \cdot \frac{2}{4} \cdot \frac{1}{3} = \frac{\binom{5-3}{3-1}}{\binom{5}{3}} = \frac{1}{\frac{5!}{2!\,3!}},
    \qquad
    P(\{BRR\}) = \frac{2}{5} \cdot \frac{3}{4} \cdot \frac{2}{3} = \frac{\binom{5-3}{3-2}}{\binom{5}{3}} = \frac{2!}{\frac{5!}{2!\,3!}}
    $$

    $\leadsto$ &nbsp; $N = 9$, $K = 5$, $n = 4$:

    $$
    P(\{BBBR\}) = \frac{\binom{5}{4}}{\binom{9}{5}} = \frac{4}{9} \cdot \frac{3}{8} \cdot \frac{2}{7} \cdot \frac{5}{6}
    $$

    $$
    f_X(x) = \frac{\dbinom{N - n}{K - x}}{\dbinom{N}{K}} \times \underbrace{\#(\text{outcomes with } x\ R\text{s})}_{\binom{n}{x}}
    = \frac{\dbinom{n}{x} \dbinom{N - n}{K - x}}{\dbinom{N}{K}} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}
    $$
    """
            ),
            definition(
                r"""
    A random variable $X$ is said to have a **hypergeometric distribution** if its pmf is

    $$
    \underbrace{f_X(x)}_{HG(N, K, n)(x)} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}, \qquad \text{for } x \in \mathbb{Z},\ 0 \leq x \leq K \text{ and } 0 \leq n - x \leq N - K
    $$

    (and $f_X(x) = 0$ otherwise).
    """,
                "Hypergeometric distribution",
            ),
            mo.md(
                r"""
    **Example.** A factory produced 1000 devices, 50 defective. We check a sample of 100 distinct devices. Probability of 7 defective objects in the sample?

    $$
    X = \#\left(\substack{\text{of defective objects} \\ \text{in a sample of 100}}\right) \qquad \leadsto \qquad HG(1000, 50, 100)(x) = \frac{\dbinom{50}{x} \dbinom{1000 - 50}{100 - x}}{\dbinom{1000}{100}} = f_X(x)
    $$

    $$
    \leadsto \qquad f_X(7) \approx 11\%, \qquad f_X(5) \approx 19\%, \qquad f_X(3) \approx 14\%
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
    hx = mo.ui.slider(0, 200, 1, value=7, label="$x$", show_value=True)
    return hK, hN, hn, hx


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, hK, hN, hn, hx, math, mo, pmf_axes, span, stems, table):
    _N, _K, _n, _x = hN.value, hK.value, hn.value, hx.value
    _fig, _ax = pmf_axes("$x$")
    _ax.text(0, 1.03, "$HG(N, K, n)$", color=BLUE, fontsize=12, ha="left", va="bottom", transform=_ax.transAxes)
    _ax.text(1, 1.03, "$B(n, p)$,  $p = K/N$", color=RED, fontsize=12, ha="right", va="bottom", transform=_ax.transAxes)
    if _K <= _N and _n <= _N:
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
        stems(_ax, _xs[_a : _b + 1], _hg[_a : _b + 1], BLUE, -0.15)
        stems(_ax, _xs[_a : _b + 1], _bi[_a : _b + 1], RED, 0.15)
        _ax.set_xlim(min(_a, _mean) - 1, max(_b, _mean) + 1)
        _ax.set_ylim(0, 1.3 * _top)
        _ax.plot([_mean, _mean], [0, 1.06 * _top], color=GREEN, lw=1.0, ls=(0, (4, 3)))
        _ax.text(_mean, 1.12 * _top, "$nK/N = np$", color=GREEN, fontsize=12, ha="center", va="bottom")
        _in = _lo <= _x <= _hi
        _rows = [
            rf"${span(_lo, _hi)}$",
            rf"$\textcolor{{{BLUE}}}{{{100 * (_hg[_x] if _in else 0.0):.2f}\%}}$" + ("" if _in else r" &nbsp; ($x \notin S_X$)"),
            rf"$\textcolor{{{RED}}}{{{100 * (_bi[_x] if _x <= _n else 0.0):.2f}\%}}$" + ("" if _x <= _n else r" &nbsp; ($x > n$)"),
            rf"$\textcolor{{{GREEN}}}{{{_mean:.2f}}}$",
            rf"${(_N - _n) / (_N - 1):.4f}$",
            rf"${span(_a, _b)}$",
        ]
    else:
        _ax.set_xlim(-1, 11)
        _ax.set_ylim(0, 1)
        _rows = [r"need $K \leq N$ and $n \leq N$"] * 6

    mo.vstack(
        [
            mo.hstack([hN, hK, hn, hx], justify="start", gap=2, wrap=True),
            table(
                list(
                    zip(
                        [
                            r"$S_X$",
                            r"$HG(N, K, n)(x)$",
                            r"$B(n, K/N)(x)$",
                            r"$E[X] = nK/N$",
                            r"$\mathrm{Var}(X) / npq = (N - n)/(N - 1)$",
                            r"plotted: $x$ with a pmf value $> 0.0005$",
                        ],
                        _rows,
                    )
                )
            ),
            _fig,
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

    $$
    S_Y = \{r, r + 1, \dots, N - K + r\} \quad (r \leq K), \qquad \underbrace{f_Y(y)}_{NHG(N, K, r)(y)} = \frac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}}
    $$
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
    E[X] &= n \frac{K}{N}, & \mathrm{Var}(X) &= n \frac{K}{N} \left( 1 - \frac{K}{N} \right) \frac{N - n}{N - 1} \\[6pt]
    E[Y] &= r\, \frac{N + 1}{K + 1}, & \mathrm{Var}(Y) &= \frac{r (N + 1)(N - K)(K + 1 - r)}{(K + 1)^2 (K + 2)}
    \end{aligned}
    $$
    """,
                "Mean and variance",
            ),
            mo.md(
                r"""
    $$
    E[X] = np \quad \text{if } p = \frac{K}{N}, \qquad \mathrm{Var}(X) = np(1 - p) \times \underbrace{\frac{N - n}{N - 1}}_{\text{finite population correction term}}
    $$

    **Proof.** Similar trick as for binomial

    $$
    x \binom{K}{x} = K \binom{K - 1}{x - 1}, \qquad y \binom{y - 1}{r - 1} = r \binom{y}{r}
    $$

    together with the binomial coefficient identity

    $$
    \binom{N}{n} = \sum_{\substack{0 \leq x \leq K \\ 0 \leq n - x \leq N - K}} \binom{K}{x} \binom{N - K}{n - x}
    $$

    $\leadsto$ &nbsp; $(1 + t)^N = (1 + t)^K (1 + t)^{N-K}$

    $$
    \begin{aligned}
    \sum_{n} \binom{N}{n} t^{N-n} &= \sum_{x} \binom{K}{x} t^{K-x} \cdot \sum_{\ell} \binom{N - K}{\ell} t^{N-K-\ell}
    = \sum_{x} \sum_{\ell} \binom{K}{x} \binom{N - K}{\ell} t^{N-x-\ell} \\
    &\overset{x + \ell = n}{=} \sum_{n} \Big[ \sum_{x} \binom{K}{x} \binom{N - K}{n - x} \Big] t^{N-n}
    \end{aligned}
    $$

    and compare the coefficients of $t^{N-n}$ on both sides. $\square$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    gN = mo.ui.slider(2, 200, 1, value=30, label="$N$", show_value=True)
    gK = mo.ui.slider(1, 200, 1, value=10, label="$K$", show_value=True)
    gr = mo.ui.slider(1, 50, 1, value=3, label="$r$", show_value=True)
    return gK, gN, gr


@app.cell(hide_code=True)
def _(BLUE, GREEN, RED, gK, gN, gr, math, mo, pmf_axes, span, stems, table):
    _N, _K, _r = gN.value, gK.value, gr.value
    _fig, _ax = pmf_axes("$y$")
    _ax.text(0, 1.03, "$NHG(N, K, r)$", color=BLUE, fontsize=12, ha="left", va="bottom", transform=_ax.transAxes)
    _ax.text(1, 1.03, "$NB(r, p)$,  $p = K/N$", color=RED, fontsize=12, ha="right", va="bottom", transform=_ax.transAxes)
    if _K <= _N and _r <= _K:
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
        stems(_ax, _ys[_a : _b + 1], _nhg[_a : _b + 1], BLUE, -0.15)
        stems(_ax, _ys[_a : _b + 1], _nbs[_a : _b + 1], RED, 0.15)
        _ax.set_xlim(min(_ys[_a], _mean) - 1, max(_ys[_b], _mean) + 1)
        _ax.set_ylim(0, 1.3 * _top)
        _ax.plot([_mean, _mean], [0, 1.06 * _top], color=GREEN, lw=1.0, ls=(0, (4, 3)))
        _ax.text(_mean, 1.12 * _top, "$r(N+1)/(K+1)$", color=GREEN, fontsize=12, ha="center", va="bottom")
        _rows = [
            rf"${span(_r, _last)}$",
            rf"$\textcolor{{{GREEN}}}{{{_mean:.2f}}}$",
            rf"$\textcolor{{{RED}}}{{{_r / _p:.2f}}}$",
            rf"${span(_ys[_a], _ys[_b])}$",
        ]
    else:
        _ax.set_xlim(-1, 11)
        _ax.set_ylim(0, 1)
        _rows = [r"need $K \leq N$ and $r \leq K$"] * 4

    mo.vstack(
        [
            mo.hstack([gN, gK, gr], justify="start", gap=2, wrap=True),
            table(
                list(
                    zip(
                        [
                            r"$S_Y = \{r, \dots, N - K + r\}$",
                            r"$E[Y] = r(N + 1)/(K + 1)$",
                            r"$r/p$ (negative binomial mean)",
                            r"plotted: $y$ with a pmf value $> 0.0005$",
                        ],
                        _rows,
                    )
                )
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - hypergeometric model: draws without replacement from $K$ “successes” and $N - K$ “failures”, count the number $X$ of successes in $n$ trials: &nbsp; $HG(N, K, n)(x) = \binom{K}{x} \binom{N - K}{n - x} \big/ \binom{N}{n}$
    - negative hypergeometric model: count the number $Y$ of trials until $r$ successes: &nbsp; $NHG(N, K, r)(y) = \binom{y - 1}{r - 1} \binom{N - y}{K - r} \big/ \binom{N}{K}$
    - replacement allowed versus not allowed: binomial $\leftrightarrow$ hypergeometric, negative binomial $\leftrightarrow$ negative hypergeometric
    - $E[X] = n \tfrac{K}{N} = np$ and $\mathrm{Var}(X) = np(1 - p) \times \tfrac{N - n}{N - 1}$ (finite population correction term) for $p = \tfrac{K}{N}$; &nbsp; $E[Y] = r\, \tfrac{N + 1}{K + 1}$

    **Next:** Poisson models
    """)
    return


if __name__ == "__main__":
    app.run()

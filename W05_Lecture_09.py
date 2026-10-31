import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 09 · Continuous random variables; gamma and exponential distributions", css_file="bs202.css")


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
    header("Lecture 09", "Week 05", "Lecture 09 • Continuous random variables; gamma and exponential distributions")
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

    - Poisson and gamma models
    - $X = \#(\text{occurrences in fixed interval } [0, t])$

        (constant average rate $\lambda$; independent for disjoint intervals)

        <span class="chain">$\displaystyle S_X = \{0, 1, 2, \dots\},$ $\displaystyle \quad f_X(x) = e^{-\lambda t}\, \frac{(\lambda t)^x}{x!}$ $\displaystyle \quad \leadsto \quad \sum_{x=0}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = e^{-\lambda t} e^{\lambda t} = 1$</span>

    - $Y$ = length of interval until $r$ occurrences

        $$
        S_Y = (0, +\infty) \qquad \text{continuous (not countable)}
        $$

    **In this lecture:** random variables with continuous state spaces

    **References:** WMS 4.1, 4.2, 4.6
    """)
    return


@app.cell(hide_code=True)
def _(corollary, definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## III.1 &nbsp; Continuous random variables; gamma and exponential distributions

    ### Continuous random variables

    **Recall:** $X : S \longrightarrow \mathbb{R}$ is a discrete random variable if $S_X = \mathrm{Im}(X)$ is countable

    <span class="chain">$\displaystyle \leadsto \quad P_X(A) = P(X \in A) = \sum_{x \in A \cap S_X} \underbrace{f_X(x)}_{\mathclap{\footnotesize \text{pmf: } P(X = x)}}$ $\displaystyle \quad \leadsto \quad \underbrace{F_X(x)}_{\footnotesize \text{cdf}} = P(X \leq x) = \sum_{y \in (-\infty, x] \cap S_X} f_X(y)$ $\displaystyle \quad \Longrightarrow \quad f_X(x) = F_X(x) - F_X(x^-)$</span>

    ($x^-$ = first element in $S_X$ smaller than $x$; $F_X(x^-) = P(X < x)$)
    """
            ),
            definition(
                r"""
    A random variable $X : S \longrightarrow \mathbb{R}$ is **continuous** if

    - $S_X$ is uncountable
    - there exists $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ continuous (cdf) such that

        $$
        P(X \leq x) = F_X(x)
        $$

        (does not follow from the assumption on $S_X$ only!)
    """,
                "Continuous random variable, via the cdf",
            ),
            corollary(
                r"""
    $X$ continuous random variable &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; $P(X = x) = 0 \quad \forall\, x \in \mathbb{R}$!</span> &nbsp; (no&nbsp;notion&nbsp;of&nbsp;pmf)

    $$
    \Longrightarrow \qquad P(a \leq X \leq b) = F_X(b) - F_X(a)
    $$
    """,
                "Single values have probability zero",
            ),
            definition(
                r"""
    A random variable $X : S \longrightarrow \mathbb{R}$ is **continuous** if

    - $S_X$ is uncountable
    - there exists $f_X : \mathbb{R} \longrightarrow \mathbb{R}$ integrable (pdf:&nbsp;probability&nbsp;density&nbsp;function) such that

        $$
        P(a \leq X \leq b) = \int_a^b f_X(x)\, dx = F_X(b) - F_X(a)
        $$
    """,
                "Continuous random variable, via the pdf",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ must satisfy

    - $F_X(x_1) \leq F_X(x_2) \quad \forall\, x_1 \leq x_2$
    - $\displaystyle\lim_{x \to -\infty} F_X(x) = 0$, &nbsp; $\displaystyle\lim_{x \to +\infty} F_X(x) = 1$

    $\leadsto$ &nbsp; $f_X$ must satisfy

    - $f_X(x) \geq 0 \quad \forall\, x \in \mathbb{R}$
    - $\displaystyle\int_{-\infty}^{+\infty} f_X(x)\, dx = 1$

    $$
    \begin{align*}
    \text{Given } F_X \ & \Longrightarrow \ f_X(x) = \frac{d}{dx} F_X(x) \\[14pt]
    \text{Given } f_X \ & \Longrightarrow \ F_X(x) = \int_{-\infty}^{x} f_X(u)\, du
    \end{align*}
    $$

    ### The gamma distribution

    **Example.** Given $X$ a Poisson random variable with average rate $\lambda$ over an interval $[0, t]$, the corresponding Gamma random variable $Y$ with average rate $\lambda$ and occurrence target $r$ is a continuous random variable!

    **Proof.** Note that

    <span class="chain">$\displaystyle \underbrace{P(X \geq r)}_{\footnotesize \begin{matrix} \text{at least } r \text{ occurrences} \\ \text{before length } t \end{matrix}} = \underbrace{P(Y \leq t)}_{\footnotesize \begin{matrix} \text{less than length } t \\ \text{until } r \text{ occurrences} \end{matrix}}$ $\displaystyle \quad \Longrightarrow \quad \sum_{x=r}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = P(Y \leq t) = F_Y(t)$</span>

    <span class="chain">$\displaystyle \Longrightarrow \quad f_Y(t) = \frac{d}{dt} \left( \sum_{x=r}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} \right)$ $\displaystyle = \sum_{x=r}^{\infty} \lambda e^{-\lambda t} \left( -\frac{(\lambda t)^x}{x!} + \frac{(\lambda t)^{x-1}}{(x - 1)!} \right)$ $\displaystyle = \lambda e^{-\lambda t} \left[ \sum_{x=r}^{\infty} \frac{(\lambda t)^{x-1}}{(x - 1)!} - \sum_{x=r}^{\infty} \frac{(\lambda t)^x}{x!} \right]$ $\displaystyle = \lambda e^{-\lambda t}\, \frac{(\lambda t)^{r-1}}{(r - 1)!} = \underbrace{\frac{\lambda^r t^{r-1}}{(r - 1)!}\, e^{-\lambda t}}_{\footnotesize \mathrm{Gamma}(r, \lambda)(t)}$ <span class="qed">$\square$</span></span>

    **Remark.** Similar derivations of $NB(r, p)$ from $B(n, p)$ and $NHG(N, K, r)$ from $HG(N, K, n)$ are possible!

    $$
    \underbrace{P(X_n \geq r)}_{\footnotesize \text{at least } r\ H\text{s in } n \text{ flips}} = \underbrace{P(Y_r \leq n)}_{\footnotesize \text{at most } n \text{ flips until } r\ H\text{s}}
    $$
    """
            ),
            definition(
                r"""
    A continuous random variable $Y : S \longrightarrow \mathbb{R}$ is said to have a **gamma distribution** with rate $\lambda$ and target $r$ if its pdf is

    $$
    f_Y(y) = \begin{cases} \dfrac{\lambda^r y^{r-1}}{(r - 1)!}\, e^{-\lambda y}, & y \in (0, +\infty) \\[8pt] 0, & y \notin (0, +\infty) \end{cases}
    $$
    """,
                "Gamma distribution",
            ),
        ],
        gap=1.5,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    g_lam = mo.ui.slider(1, 4, 0.1, value=1, label=r"$\lambda$", show_value=True)
    g_a = mo.ui.slider(0, 10, 0.1, value=0, label="$a$", show_value=True)
    g_b = mo.ui.slider(0, 10, 0.1, value=3, label="$b$", show_value=True)
    g_r = mo.ui.slider(1, 3, 1, value=2, label="$r$", show_value=True)
    return g_a, g_b, g_lam, g_r


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, g_a, g_b, g_lam, g_r, math, mo, np, table):
    _lam, _r, _a, _b = g_lam.value, g_r.value, g_a.value, g_b.value

    def _pdf(y, r):
        return _lam**r * y ** (r - 1) / math.factorial(r - 1) * np.exp(-_lam * y)

    def _tail(t, r):
        return sum(np.exp(-_lam * t) * (_lam * t) ** k / math.factorial(k) for k in range(r))

    def _cdf(t, r):
        return 1 - _tail(t, r)

    # the frame reaches at least 10 and at least the 99.5 % point of the chosen r
    _grid = np.linspace(0, 200, 4001)
    _xmax = max(10.0, float(np.ceil(_grid[np.argmax(_cdf(_grid, _r) >= 0.995)])))
    _y = np.linspace(0, _xmax, 500)
    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax, _cx = _fig.subplots(1, 2)

    # pdf: the curves r = 1, 2, 3 of the board for reference, the chosen r in blue with P(a <= Y <= b) as an area
    if _a <= _b:
        _yy = np.linspace(_a, _b, 200)
        _ax.fill_between(_yy, _pdf(_yy, _r), color=LIGHT, lw=0)
    for _x, _name, _ha in ((_a, "$a$", "right" if _a <= _b else "left"), (_b, "$b$", "left" if _a <= _b else "right")):
        _ax.axvline(_x, color=GREY, lw=1.0, ls=(0, (4, 3)))
        _ax.annotate(_name, (_x, 1.0), xycoords=("data", "axes fraction"), textcoords="offset points", xytext=(-2 if _ha == "right" else 2, 3), ha=_ha, va="bottom", fontsize=12, annotation_clip=False)
    _spot = {1: (0.3, (5, 0), "center"), 2: (1.2, (3, 3), "bottom"), 3: (3.5, (3, 3), "bottom")}  # (lambda x, offset, va): a free spot beside each curve
    for _k in sorted({1, 2, 3, _r}):
        _col = BLUE if _k == _r else GREY
        _ax.plot(_y, _pdf(_y, _k), color=_col, lw=1.4 if _k == _r else 1.0, zorder=3 if _k == _r else 2)
        _x = _spot[_k][0] / _lam
        _ax.annotate(f"$r = {_k}$", (_x, float(_pdf(_x, _k))), textcoords="offset points", xytext=_spot[_k][1], ha="left", va=_spot[_k][2], color=_col, fontsize=12, zorder=5, annotation_clip=False)
    _ax.set_xlim(0, _xmax)
    _ax.set_ylim(0, 1.05 * _lam)
    _ax.set_xlabel("$y$")
    _ax.set_ylabel("$f_Y(y)$")

    # cdf of the chosen r: the same probability as a difference of two values
    _Fa, _Fb = float(_cdf(_a, _r)), float(_cdf(_b, _r))
    _P = float(_tail(_a, _r) - _tail(_b, _r))

    def _fmt(v):
        if v >= 0.01 or v == 0:
            return f"{v:.2f}" if v else "0"
        if v >= 1e-4:
            return f"{v:.{1 - math.floor(math.log10(v))}f}"
        _e = math.floor(math.log10(v))
        return rf"{v / 10**_e:.1f} \times 10^{{{_e}}}"

    _cx.plot(_y, _cdf(_y, _r), color=BLUE, lw=1.4)
    for _x, _F in ((_a, _Fa), (_b, _Fb)):
        _cx.plot([_x, _x, 0], [0, _F, _F], color=GREY, lw=1.0, ls=(0, (4, 3)))
    if _a <= _b:
        _cx.plot([0, 0], [_Fa, _Fb], color=GREEN, lw=3.5, solid_capstyle="butt", clip_on=False, zorder=4)
    _cx.set_xlim(0, _xmax)
    _cx.set_ylim(0, 1.05)
    _cx.set_xlabel("$y$")
    _cx.set_ylabel("$F_Y(y)$")
    for _axx in (_ax, _cx):
        for _s in ("top", "right"):
            _axx.spines[_s].set_visible(False)
        _axx.xaxis.set_major_formatter(lambda v, _p: f"{v:g}")
        _axx.yaxis.set_major_formatter(lambda v, _p: f"{v:g}")

    mo.vstack(
        [
            mo.hstack([g_lam, g_r, g_a, g_b], justify="start", gap=2, wrap=True),
        ]
        + ([table([(r"$P(a \leq Y \leq b) = F_Y(b) - F_Y(a)$", rf"${_fmt(_P)}$")]), _fig] if _a <= _b else [mo.md(r"need $a \leq b$")])
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### The exponential distribution

    **Example.** Hyeonpung has 2 car accidents per month

    $$
    P(\text{1 car accident in less than } \underbrace{\text{10 days}}_{\mathclap{\footnotesize 1/3 \text{ months}}}) = \ ?
    $$

    $\leadsto$ &nbsp; $Y$ = time until 1 accident

    <span class="chain">$\displaystyle \Longrightarrow \quad f_Y(y) = \lambda e^{-\lambda y}$ $\displaystyle \quad \leadsto \quad \mathrm{Gamma}(1, \lambda) = \mathrm{Exp}(\lambda) \quad \text{(exponential distribution)}$</span>

    <span class="chain">$\displaystyle \underbrace{P(Y \leq 1/3)}_{\footnotesize F_Y(1/3)} = \int_{0}^{1/3} \lambda e^{-\lambda y}\, dy$ $\displaystyle = -e^{-\lambda y}\, \Big|_{0}^{1/3} = 1 - e^{-\lambda/3} = 1 - e^{-2/3} \approx 48.7\%$</span>

    $$
    P(\text{1 car accident in the 10 days after 20 days without accidents}) = \ ?
    $$

    <span class="chain">$\displaystyle P(Y \leq 1 \mid Y > 2/3) = \frac{P(2/3 < Y \leq 1)}{P(2/3 < Y)} = \frac{F_Y(1) - F_Y(2/3)}{1 - F_Y(2/3)}$ $\displaystyle = \frac{(1 - e^{-\lambda}) - (1 - e^{-2\lambda/3})}{1 - (1 - e^{-2\lambda/3})}$ $\displaystyle = \frac{e^{-2\lambda/3} - e^{-\lambda}}{e^{-2\lambda/3}} = 1 - e^{-\lambda/3} = 1 - e^{-2/3} \approx 48.7\%$</span>
    """
            ),
            theorem(
                r"""
    The exponential distribution (gamma with $r = 1$) has no memory!

    If $Y \sim \mathrm{Exp}(\lambda)$ &nbsp; ($Y$ has $f_Y(y) = \mathrm{Exp}(\lambda)(y)$) &nbsp; then

    $$
    P(Y \leq s + t \mid Y > s) = P(Y \leq t)
    $$

    (how long we have already waited does not change how long we still have to wait until the next occurrence)
    """,
                "The exponential distribution is memoryless",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    m_lam = mo.ui.slider(0.1, 2, 0.1, value=2, label=r"$\lambda$", show_value=True)
    m_s = mo.ui.slider(steps=[round(k / 30, 4) for k in range(0, 31)], value=0.6667, label="$s$", show_value=True)
    m_t = mo.ui.slider(steps=[round(k / 30, 4) for k in range(1, 31)], value=0.3333, label="$t$", show_value=True)
    return m_lam, m_s, m_t


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, LIGHT, m_lam, m_s, m_t, mo, np):
    _l, _s, _t = m_lam.value, m_s.value, m_t.value
    _f = lambda y: _l * np.exp(-_l * y)

    _fig = Figure(figsize=(5.6, 2.9), layout="constrained")
    _ax = _fig.subplots()
    _hi = max(1.4 * (_s + _t) + 0.3, min(6 / _l, 3 * (_s + _t)))  # the frame follows s + t
    _top = 1.5 * _l
    _yy = np.linspace(0, _t, 100)
    _ax.fill_between(_yy, _f(_yy), color=LIGHT, lw=0)
    # (s, s + t] gets its own blue hatch, so that it stays distinct from (0, t] also when the two overlap (t > s)
    _yy = np.linspace(_s, _s + _t, 100)
    _ax.fill_between(_yy, _f(_yy), facecolor="none", edgecolor=BLUE, hatch="\\\\\\", lw=0)
    _yy = np.linspace(_s, _hi, 200)
    _ax.fill_between(_yy, _f(_yy), facecolor="none", edgecolor=GREY, hatch="///", lw=0)
    for _x in (_t, _s, _s + _t):
        _ax.plot([_x, _x], [0, _f(_x)], color=GREY, lw=1.0)
    _y = np.linspace(0, _hi, 400)
    _ax.plot(_y, _f(_y), color=BLUE, lw=1.4)

    # area labels above the curve, stacked so that they never meet (u = one point in data units, roughly)
    _u = _top / 150
    _x1, _x2, _x3 = _t / 2, _s + _t / 2, _s + _t + 0.08 * _hi
    _y1, _y2, _y3 = (_f(_x) + 3 * _u for _x in (_x1, _x2, _x3))
    _y2 = max(_y2, _y3 + 18 * _u)
    _y1 = max(_y1, _y2 + 18 * _u)
    for _x, _yv, _name, _c in ((_x1, _y1, r"$P(Y \leq t)$", "black"), (_x2, _y2, r"$P(s < Y \leq s + t)$", BLUE), (_x3, _y3, r"$P(Y > s)$", GREY)):
        _ax.annotate(_name, (_x, _yv), textcoords="offset points", xytext=(4, 0), ha="left", va="bottom", fontsize=12, color=_c)

    # the marks 0, t and s, s + t on two rows, so that they stay apart for every s and t
    for _x, _name, _row, _ha in ((0, "$0$", 0, "right"), (_t, "$t$", 0, "left"), (_s, "$s$", 1, "right"), (_s + _t, "$s + t$", 1, "left")):
        _ax.annotate(_name, (_x, 0), xycoords=("data", "axes fraction"), textcoords="offset points", xytext=(-1 if _ha == "right" else 1, -5 - 16 * _row), ha=_ha, va="top", fontsize=12, annotation_clip=False)
    _ax.set_xlim(0, _hi)
    _ax.set_ylim(0, _top)
    _ax.set_xticks([])
    _ax.set_ylabel("$f_Y(y)$")
    _ax.yaxis.set_major_formatter(lambda v, _p: "" if v == 0 else f"{v:g}")
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)

    mo.vstack(
        [
            mo.hstack([m_lam, m_s, m_t], justify="start", gap=2, wrap=True),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** LED lightbulbs have failure rate of $\lambda = 0.2$ per year following an exponential model (approximately)

    $\Longrightarrow$ &nbsp; the probability of a failure in the next 3 months is independent of how long ago you bought the lightbulb!

    $$
    P(Y \leq s + 1/4 \mid Y > s) = P(Y \leq 1/4) = 1 - e^{-\lambda/4} \approx 0.05
    $$

    **Remark.** The negative binomial distribution with target $r = 1$ is also memoryless! &nbsp; $NB(1, p) = \mathrm{Geom}(p)$ is called the geometric distribution.
    """)
    return


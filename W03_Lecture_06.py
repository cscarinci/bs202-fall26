import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 06 · Binomial and negative binomial models", css_file="bs202.css")


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
    header("Lecture 06", "Week 03", "Lecture 06 · Binomial and negative binomial models")
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

    - probability spaces &nbsp; $(S, \mathcal{E}, P)$
    - random variables &nbsp; $X : S \longrightarrow \mathbb{R}$
    - probability distributions &nbsp; $f_X : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $x \longmapsto P(X = x)$
    - expectation &nbsp; $E[u(X)] = \displaystyle\sum_{x \in S_X} u(x)\, f_X(x)$

    **In this lecture:** probabilistic models (specific pmfs) &nbsp; $\leadsto$ &nbsp; binomial and negative binomial &nbsp; (WMS 3.4, 3.6)
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## II.3 &nbsp; Binomial and negative binomial models

    ### The binomial model
    """
            ),
            definition(
                r"""
    A **binomial model** is a random experiment that

    1. consists of a sequence of identical independent trials
    2. each single trial has one of **two outcomes** with probabilities $P(\text{“success”}) = p$, $P(\text{“failure”}) = 1 - p = q$
    3. measures the number $X$ of “successes” in a fixed number $n$ of trials
    """,
                "Binomial model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; toss a coin with bias $p = P(\{H\})$ (“success”) $n$ independent times; count $X = \#(\text{heads on } n \text{ trials})$

    $$
    S = \{\, (c_1, c_2, \dots, c_n) \mid c_i = H \text{ or } T \,\}, \qquad S_X = \{0, 1, 2, \dots, n\}
    $$

    $$
    \begin{aligned}
    P(\{(c_1, c_2, \dots, c_n)\}) &= \underbrace{P(\{c_1\})}_{\substack{p \text{ if } c_1 = H \\ q \text{ if } c_1 = T}}\ \underbrace{P(\{c_2\})}_{\substack{p \text{ if } c_2 = H \\ q \text{ if } c_2 = T}} \cdots \underbrace{P(\{c_n\})}_{\substack{p \text{ if } c_n = H \\ q \text{ if } c_n = T}} \\[6pt]
    &= \underbrace{p^k q^{n-k}}_{\substack{\text{probability of one specific} \\ \text{outcome with } k \text{ heads}}} \quad \text{if } X(c_1, c_2, \dots, c_n) = k \qquad (\text{if } k \in S_X)
    \end{aligned}
    $$

    $$
    f_X(x) = p^x q^{n-x} \times \underbrace{\#(\text{outcomes with } x \text{ heads})}_{\binom{n}{x}} = \binom{n}{x} p^x q^{n-x}
    $$
    """
            ),
            definition(
                r"""
    A random variable $X$ is said to have a **binomial distribution** on $n$ trials with bias $p$ if its pmf is

    $$
    f_X(x) = \binom{n}{x} p^x (1 - p)^{n-x} \qquad \text{for } x = 0, 1, 2, \dots, n \quad (\text{and } f_X(x) = 0 \text{ otherwise})
    $$
    """,
                "Binomial distribution",
            ),
            mo.md(
                r"""
    **Remark.**

    $$
    \sum_{x=0}^{n} f_X(x) = \sum_{x=0}^{n} \binom{n}{x} p^x (1 - p)^{n-x} = (p + 1 - p)^n = (1)^n = 1 = P(X \in \{0, 1, 2, \dots, n\})
    $$

    **Example.** 30% of patients recover without treatment. What is the probability that 9 out of 10 patients will recover without treatment?

    $$
    \begin{aligned}
    X &= \#(\text{recovering patients out of } 10) && (n = 10) \\[4pt]
    0.3 &= P(\text{one patient recovers}) = p && (\text{one patient out of one})
    \end{aligned}
    $$

    $$
    \Longrightarrow \qquad f_X(9) = \binom{10}{9} (0.3)^9 (0.7)^{10 - 9} \approx 0.01\%
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    bn = mo.ui.slider(1, 40, 1, value=10, label="$n$", show_value=True)
    bp = mo.ui.slider(0.01, 0.99, 0.01, value=0.3, label="$p$", show_value=True)
    bx = mo.ui.slider(0, 40, 1, value=9, label="$x$", show_value=True)
    b_reps = mo.ui.slider(10, 2000, 10, value=200, label="repetitions of the experiment", show_value=True)
    b_redo = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Repeat")
    return b_redo, b_reps, bn, bp, bx


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, LIGHT, RED, b_redo, b_reps, bn, bp, bx, math, mo, np, table):
    _n, _p, _x = bn.value, bp.value, bx.value
    _xs = list(range(_n + 1))
    _pmf = [math.comb(_n, _k) * _p**_k * (1 - _p) ** (_n - _k) for _k in _xs]
    _in_support = _x <= _n

    # Simulation: toss n coins, count heads, repeat
    _rng = np.random.default_rng(606 + b_redo.value)
    _N = b_reps.value
    _heads = (_rng.random((_N, _n)) < _p).sum(axis=1)
    _freq = np.bincount(_heads, minlength=_n + 1) / _N

    _fx = _pmf[_x] if _in_support else 0.0
    _le = min(1.0, sum(_pmf[: _x + 1])) if _in_support else 1.0  # min() guards against rounding only
    _ge = min(1.0, sum(_pmf[_x:])) if _in_support else 0.0
    _rel = float(_freq[_x]) if _in_support else 0.0

    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _top = max(max(_pmf), float(_freq.max())) * 1.15
    _ax.axvspan(_x - 0.5, _x + 0.5, color=LIGHT, lw=0, zorder=0)  # the chosen x
    _ax.plot([_n * _p] * 2, [0, _top], color=GREEN, lw=1.2, ls=(0, (4, 3)), zorder=1)
    _ax.text(_n * _p, _top, "$np$", color=GREEN, fontsize=12, ha="center", va="bottom", clip_on=False)
    _ax.vlines(_xs, 0, _pmf, color=BLUE, lw=1.2, zorder=3)
    _ax.plot(_xs, _pmf, "o", color=BLUE, ms=3.5, zorder=4)
    _ax.plot(_xs, _freq, "o", mfc="none", mec=RED, ms=6.5, mew=1.1, zorder=5)
    _right = max(_n, _x)  # the frame follows the chosen x, also outside the support
    _ax.set_xlim(-0.7, _right + 0.7)
    _ax.set_ylim(0, _top)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    if _right <= 20:
        _ax.set_xticks(range(_right + 1))
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([bn, bp, bx], justify="start", gap=2, wrap=True),
            mo.hstack([b_reps, b_redo], justify="start", gap=2, align="center", wrap=True),
            table(
                [
                    (rf"$x \in S_X = \{{0, 1, \dots, {_n}\}}$", "yes" if _in_support else "no"),
                    (r"$f_X(x) = \binom{n}{x} p^x q^{n-x}$", rf"$\textcolor{{{BLUE}}}{{{100 * _fx:.3f}\%}}$"),
                    (rf"relative frequency of $X = x$ in ${_N}$ repetitions", rf"$\textcolor{{{RED}}}{{{100 * _rel:.3f}\%}}$"),
                    (r"$P(X \leq x)$", rf"${100 * _le:.3f}\%$"),
                    (r"$P(X \geq x)$", rf"${100 * _ge:.3f}\%$"),
                    (r"$np$", rf"$\textcolor{{{GREEN}}}{{{_n * _p:.2f}}}$"),
                    (r"$npq$", rf"${_n * _p * (1 - _p):.2f}$"),
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
            mo.md(r"""### Mean and variance of a binomial random variable"""),
            theorem(
                r"""
    Let $X$ be a binomial random variable on $n$ trials with bias $p$. Then

    $$
    \mu_X = E[X] = np, \qquad \sigma_X^2 = \mathrm{Var}(X) = npq
    $$
    """,
                "Mean and variance of the binomial distribution",
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    E[X] &= \sum_{x=0}^{n} x \binom{n}{x} p^x q^{n-x} = \sum_{x=0}^{n} x\, \frac{n!}{x!\,(n - x)!}\, p^x q^{n-x} = \sum_{x=1}^{n} \frac{n!}{(x - 1)!\,(n - x)!}\, p^x q^{n-x} \\[6pt]
    &= np \underbrace{\sum_{x-1=0}^{n-1} \frac{(n - 1)!}{(x - 1)!\,(n - 1 - x + 1)!}\, p^{x-1} q^{n-1-x+1}}_{(p + q)^{n-1} \,=\, 1}
    \end{aligned}
    $$

    $$
    \mathrm{Var}(X) = E[X^2] - \underbrace{E[X]^2}_{(np)^2} \qquad \leadsto \qquad E[X^2] = E[X(X - 1)] + E[X]
    $$

    $$
    \begin{aligned}
    \leadsto \qquad E[X(X - 1)] &= \sum_{x=0}^{n} x (x - 1)\, \frac{n!}{x!\,(n - x)!}\, p^x q^{n-x} \\[6pt]
    &= \sum_{x=2}^{n} \frac{n (n - 1) (n - 2)!}{(x - 2)!\,(n - 2 - x + 2)!}\, p^2 p^{x-2} q^{n-x} \\[6pt]
    &= n (n - 1) p^2 \underbrace{\sum_{x-2=0}^{n-2} \frac{(n - 2)!}{(x - 2)!\,(n - 2 - x + 2)!}\, p^{x-2} q^{n-x}}_{(p + q)^{n-2} \,=\, 1}
    \end{aligned}
    $$

    $$
    \Longrightarrow \qquad E[X(X - 1)] = n (n - 1) p^2
    \qquad \Longrightarrow \qquad E[X^2] = E[X(X - 1)] + E[X] = n (n - 1) p^2 + np
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad \mathrm{Var}(X) &= E[X^2] - E[X]^2 = n (n - 1) p^2 + np - (np)^2 \\
    &= -np^2 + np = np (1 - p) = npq \qquad \square
    \end{aligned}
    $$

    ### The negative binomial model
    """
            ),
            definition(
                r"""
    A **negative binomial model** is an experiment that

    1. consists of a sequence of identical independent trials
    2. each single trial has one of **two outcomes** with probabilities $P(\text{“success”}) = p$, $P(\text{“failure”}) = 1 - p = q$
    3. measures the number $Y$ of trials until a fixed number $r$ of “successes”
    """,
                "Negative binomial model",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; toss a coin with bias $p = P(\{H\})$ until $r$ heads are achieved; count $Y = \#(\text{tosses until } r \text{ heads})$

    $$
    \begin{aligned}
    S &= \{\, (c_1, \dots, c_k) \mid c_i = H \text{ or } T \text{ with } c_k = H \text{ and } r - 1 \text{ other } c_i = H \text{ for } 1 \leq i < k \,\} \qquad (\Longrightarrow \ k \geq r) \\[4pt]
    S_Y &= \{r, r + 1, r + 2, \dots\}
    \end{aligned}
    $$

    $$
    P(\{(\underbrace{c_1, \dots, c_{k-1}}_{\text{exactly } r - 1\ H\text{s}}, \underbrace{c_k}_{H})\}) = p^r q^{k-r} \quad \text{if } Y(c_1, \dots, c_k) = k
    $$

    $$
    f_Y(y) = p^r q^{y-r} \underbrace{\#(\text{outcomes with } y \text{ trials})}_{\binom{y-1}{r-1}} = \binom{y - 1}{r - 1} p^r q^{y-r}
    $$
    """
            ),
            definition(
                r"""
    A random variable $Y$ is said to have a **negative binomial distribution** with target $r$ and bias $p$ if its pmf is

    $$
    f_Y(y) = \binom{y - 1}{r - 1} p^r q^{y-r} \qquad \text{for } y = r, r + 1, r + 2, \dots
    $$
    """,
                "Negative binomial distribution",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    nr = mo.ui.slider(1, 10, 1, value=3, label="$r$", show_value=True)
    np_ = mo.ui.slider(0.05, 0.95, 0.01, value=0.4, label="$p$", show_value=True)
    ny = mo.ui.slider(1, 60, 1, value=5, label="$y$", show_value=True)
    return np_, nr, ny


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, LIGHT, math, mo, np_, nr, ny, table):
    _r, _p, _y = nr.value, np_.value, ny.value

    def _f(y):
        return math.comb(y - 1, _r - 1) * _p**_r * (1 - _p) ** (y - _r) if y >= _r else 0.0

    # The support is infinite: the frame runs until 99.5 % of the mass is inside, and at least until the chosen y
    _ys, _pmf, _mass = [], [], 0.0
    while _mass < 0.995 or _r + len(_ys) <= _y:
        _ys.append(_r + len(_ys))
        _pmf.append(_f(_ys[-1]))
        _mass += _pmf[-1]
    _mass = min(1.0, _mass)  # guards against rounding only
    _in_support = _y >= _r
    _le = min(1.0, sum(_pmf[: _y - _r + 1])) if _in_support else 0.0

    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _top = max(_pmf) * 1.15
    _many = len(_ys) > 80
    _ax.axvspan(_y - 0.5, _y + 0.5, color=LIGHT, lw=0, zorder=0)  # the chosen y
    _ax.plot([_r / _p] * 2, [0, _top], color=GREEN, lw=1.2, ls=(0, (4, 3)), zorder=1)
    _ax.text(_r / _p, _top, "$r/p$", color=GREEN, fontsize=12, ha="center", va="bottom", clip_on=False)
    _ax.vlines(_ys, 0, _pmf, color=BLUE, lw=0.8 if _many else 1.2, zorder=3)
    _ax.plot(_ys, _pmf, "o", color=BLUE, ms=2 if _many else 3.5, zorder=4)
    _left = min(_r, _y)
    _ax.set_xlim(_left - 0.7, _ys[-1] + 0.7)
    _ax.set_ylim(0, _top)
    _ax.set_xlabel("$y$")
    _ax.set_ylabel("$f_Y(y)$")
    if _ys[-1] - _left <= 20:
        _ax.set_xticks(range(_left, _ys[-1] + 1))
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    if _in_support:
        _value = rf"$\binom{{{_y - 1}}}{{{_r - 1}}} ({_p:.2f})^{{{_r}}} ({1 - _p:.2f})^{{{_y - _r}}} = \textcolor{{{BLUE}}}{{{100 * _f(_y):.3f}\%}}$"
    else:
        _value = rf"$\textcolor{{{BLUE}}}{{{0:.3f}\%}}$"
    mo.vstack(
        [
            mo.hstack([nr, np_, ny], justify="start", gap=2, wrap=True),
            table(
                [
                    (rf"$y \in S_Y = \{{{_r}, {_r + 1}, {_r + 2}, \dots\}}$", "yes" if _in_support else "no"),
                    (r"$f_Y(y) = \binom{y-1}{r-1} p^r q^{y-r}$", _value),
                    (r"$P(Y \leq y)$", rf"${100 * _le:.3f}\%$"),
                    (r"$r/p$", rf"$\textcolor{{{GREEN}}}{{{_r / _p:.3f}}}$"),
                    (rf"mass inside the frame, $P(Y \leq {_ys[-1]})$", rf"${100 * _mass:.3f}\%$"),
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

    - **binomial model**: $n$ identical independent trials with two outcomes, $P(\text{“success”}) = p$, $P(\text{“failure”}) = q = 1 - p$; $X$ = number of “successes” &nbsp; $\Longrightarrow$ &nbsp; $f_X(x) = \binom{n}{x} p^x q^{n-x}$ for $x = 0, 1, 2, \dots, n$
    - $\sum_{x=0}^{n} f_X(x) = (p + 1 - p)^n = 1$
    - a binomial random variable has $\mu_X = np$ and $\sigma_X^2 = npq$ &nbsp; (via $E[X^2] = E[X(X - 1)] + E[X]$)
    - **negative binomial model**: same trials; $Y$ = number of trials until a fixed number $r$ of “successes” &nbsp; $\Longrightarrow$ &nbsp; $f_Y(y) = \binom{y-1}{r-1} p^r q^{y-r}$ for $y = r, r + 1, r + 2, \dots$

    **Next:** hypergeometric and negative hypergeometric models
    """)
    return


if __name__ == "__main__":
    app.run()

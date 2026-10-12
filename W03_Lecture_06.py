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
    header("Lecture 06", "Week 03", "Lecture 06 · Binomial and negative binomial models")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## So far

    | | |
    |:--|:--|
    | Probability Spaces | $(S, \mathcal{E}, P)$ |
    | Random Variables | $X : S \longrightarrow \mathbb{R}$ |
    | Probability distributions | $f_X : \mathbb{R} \longrightarrow \mathbb{R}$, &nbsp; $x \longmapsto P(X = x)$ |
    | Expectation | $E[u(X)] = \displaystyle\sum_{x \in S_X} u(x)\, f_X(x)$ |

    **Today:** Probabilistic models (specific pmfs) &nbsp; $\leadsto$ &nbsp; Binomial, geometric, Poisson, … &nbsp; (WMS 3.4 – 3.8)
    """
            ),
            definition(
                r"""
    A **binomial model** is a random experiment that

    1. consists of a sequence of identical independent trials
    2. each single trial has one of *two outcomes* with probabilities $P(\text{“success”}) = p$, $P(\text{“failure”}) = 1 - p = q$
    3. measures the number $X$ of “successes” in a fixed number $n$ of trials
    """
            ),
            mo.md(
                r"""
    Toss a coin with bias $p = P(\{H\})$ (“success”) $n$ independent times; count $X = \#(\text{heads on } n \text{ trials})$

    $$
    S = \{\, (c_1, c_2, \dots, c_n) \mid c_i = H \text{ or } T \,\}, \qquad S_X = \{0, 1, 2, \dots, n\}
    $$

    $$
    \begin{aligned}
    P(\{(c_1, c_2, \dots, c_n)\}) &= \underbrace{P(\{c_1\})}_{\substack{p \text{ if } c_1 = H \\ q \text{ if } c_1 = T}}\ \underbrace{P(\{c_2\})}_{\substack{p \text{ if } c_2 = H \\ q \text{ if } c_2 = T}} \cdots \underbrace{P(\{c_n\})}_{\substack{p \text{ if } c_n = H \\ q \text{ if } c_n = T}} \\[6pt]
    &= \underbrace{p^k q^{n-k}}_{\text{probability of one specific outcome with } k \text{ heads}} \quad \text{if } X(c_1, c_2, \dots, c_n) = k \qquad (\text{if } k \in S_X)
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
    """
            ),
            mo.md(
                r"""
    **Remark.**

    $$
    \sum_{x=0}^{n} f_X(x) = \sum_{x=0}^{n} \binom{n}{x} p^x (1 - p)^{n-x} = (p + 1 - p)^n = (1)^n = 1 = P(X \in \{0, 1, 2, \dots, n\})
    $$

    **Example.** 30% of patients recover without treatment. What is the probability that 9 out of 10 patients will recover without treatment?

    $X = \#(\text{recovering patients out of } 10)$ &nbsp; ($n = 10$), &nbsp; $0.3 = P(\text{one patient recovers}) = p$ &nbsp; (one patient out of one)

    $$
    \Longrightarrow \quad f_X(9) = \binom{10}{9} (0.3)^9 (0.7)^{10 - 9} \approx 0.01\%
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
def _(Figure, RED, b_redo, b_reps, bn, bp, bx, math, mo, np):
    _n, _p, _x = bn.value, bp.value, bx.value
    _xs = list(range(_n + 1))
    _pmf = [math.comb(_n, _k) * _p**_k * (1 - _p) ** (_n - _k) for _k in _xs]
    _in_support = _x <= _n

    # Simulation: toss n coins, count heads, repeat
    _rng = np.random.default_rng(606 + b_redo.value)
    _N = b_reps.value
    _heads = (_rng.random((_N, _n)) < _p).sum(axis=1)
    _freq = np.bincount(_heads, minlength=_n + 1) / _N

    _fig = Figure(figsize=(7.4, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.bar(_xs, _pmf, width=0.7, color=["#1b458f" if (_k == _x and _in_support) else RED for _k in _xs], alpha=0.75, label="$f_X(x)$")
    _ax.plot(_xs, _freq, "o", color="black", ms=4, label=f"relative frequency ({_N} repetitions)")
    _ax.axvline(_n * _p, color="#555555", lw=1, ls="--")
    _ax.text(_n * _p, max(_pmf) * 1.08, "$np$", ha="center", fontsize=11, color="#555555")
    _ax.set_ylim(0, max(max(_pmf), _freq.max()) * 1.25)
    _ax.set_xlabel("$x$")
    _ax.set_ylabel("$f_X(x)$")
    _ax.legend(loc="upper right", fontsize=9, frameon=False)
    if _n <= 20:
        _ax.set_xticks(_xs)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    if _in_support:
        _le = sum(_pmf[: _x + 1])
        _text = "\n".join(
            [
                "| | |",
                "|:--|--:|",
                rf"| $f_X(x) = \binom{{n}}{{x}} p^x q^{{n-x}}$ | ${100 * _pmf[_x]:.3g}\%$ |",
                rf"| $P(X \le x)$ | ${100 * _le:.3g}\%$ |",
                rf"| $P(X \ge x)$ | ${100 * (1 - _le + _pmf[_x]):.3g}\%$ |",
                rf"| $np$ | ${_n * _p:.3g}$ |",
                rf"| $npq$ | ${_n * _p * (1 - _p):.3g}$ |",
            ]
        )
    else:
        _text = rf"$x = {_x} \notin S_X = \{{0, 1, \dots, {_n}\}}$ &nbsp; $\Longrightarrow$ &nbsp; $f_X({_x}) = 0$"
    mo.vstack(
        [
            mo.hstack([bn, bp, bx], justify="start", gap=3, wrap=True),
            mo.md(_text),
            mo.hstack([b_reps, b_redo], justify="start", gap=2, align="center", wrap=True),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Let $X$ be a binomial RV on $n$ trials with bias $p$. Then

    $$
    \mu_X = E[X] = np, \qquad \sigma_X^2 = \mathrm{Var}(X) = npq
    $$
    """
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    E[X] &= \sum_{x=0}^{n} x \binom{n}{x} p^x q^{n-x} = \sum_{x=0}^{n} x\, \frac{n!}{x!\,(n - x)!}\, p^x q^{n-x} \\[6pt]
    &= \sum_{x=1}^{n} \frac{n!}{(x - 1)!\,(n - x)!}\, p^x q^{n-x} = np \underbrace{\sum_{x-1=0}^{n-1} \frac{(n - 1)!}{(x - 1)!\,(n - 1 - x + 1)!}\, p^{x-1} q^{n-1-x+1}}_{(p + q)^{n-1} \,=\, 1}
    \end{aligned}
    $$

    $$
    \mathrm{Var}(X) = E[X^2] - \underbrace{E[X]^2}_{(np)^2} \qquad \leadsto \qquad E[X^2] = E[X(X - 1)] + E[X]
    $$

    $$
    \begin{aligned}
    \leadsto \quad E[X(X - 1)] &= \sum_{x=0}^{n} x (x - 1)\, \frac{n!}{x!\,(n - x)!}\, p^x q^{n-x} = \sum_{x=2}^{n} \frac{n (n - 1) (n - 2)!}{(x - 2)!\,(n - 2 - x + 2)!}\, p^2 p^{x-2} q^{n-x} \\[6pt]
    &= n (n - 1) p^2 \underbrace{\sum_{x-2=0}^{n-2} \frac{(n - 2)!}{(x - 2)!\,(n - 2 - x + 2)!}\, p^{x-2} q^{n-x}}_{(p + q)^{n-2} \,=\, 1}
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad E[X(X - 1)] = n (n - 1) p^2
    \qquad \Longrightarrow \qquad E[X^2] = E[X(X - 1)] + E[X] = n (n - 1) p^2 + np
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad \mathrm{Var}(X) &= E[X^2] - E[X]^2 \\
    &= n (n - 1) p^2 + np - (np)^2 \\
    &= -np^2 + np = np (1 - p) = npq \qquad \square
    \end{aligned}
    $$
    """
            ),
            definition(
                r"""
    A **negative binomial model** is an experiment that

    1. consists of a sequence of identical independent trials
    2. each single trial has one of *two outcomes* with probabilities $P(\text{“success”}) = p$, $P(\text{“failure”}) = 1 - p = q$
    3. measures the number $Y$ of trials until a fixed number $r$ of “successes”
    """
            ),
            mo.md(
                r"""
    Toss a coin with bias $p = P(\{H\})$ until $r$ heads are achieved; count $Y = \#(\text{tosses until } r \text{ heads})$

    $$
    S = \{\, (c_1, \dots, c_k) \mid c_i = H \text{ or } T \text{ with } c_k = H \text{ and } r - 1 \text{ other } c_i = H \text{ for } 1 \leq i < k \,\} \qquad (\Longrightarrow \ k \geq r)
    $$

    $$
    S_Y = \{r, r + 1, r + 2, \dots\}
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
    """
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
def _(Figure, RED, math, mo, np_, nr, ny):
    _r, _p, _y = nr.value, np_.value, ny.value
    _f = lambda y: math.comb(y - 1, _r - 1) * _p**_r * (1 - _p) ** (y - _r) if y >= _r else 0.0
    # Plot until the cumulative mass reaches 99.5 %
    _ys, _pmf, _mass = [], [], 0.0
    _top = _r
    while _mass < 0.995 and _top < 400:
        _ys.append(_top)
        _pmf.append(_f(_top))
        _mass += _pmf[-1]
        _top += 1

    _fig = Figure(figsize=(7.4, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.bar(_ys, _pmf, width=0.7, color=["#1b458f" if _k == _y else RED for _k in _ys], alpha=0.75)
    _ax.axvline(_r / _p, color="#555555", lw=1, ls="--")
    _ax.text(_r / _p, max(_pmf) * 1.08, "$r/p$", ha="center", fontsize=11, color="#555555")
    _ax.set_ylim(0, max(_pmf) * 1.25)
    _ax.set_xlabel("$y$")
    _ax.set_ylabel("$f_Y(y)$")
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    if _y >= _r:
        _text = rf"$f_Y({_y}) = \binom{{{_y - 1}}}{{{_r - 1}}} ({_p:g})^{{{_r}}} ({1 - _p:g})^{{{_y - _r}}} \approx {100 * _f(_y):.3g}\%$"
    else:
        _text = rf"$y = {_y} < r = {_r}$ &nbsp; $\Longrightarrow$ &nbsp; $y \notin S_Y$, &nbsp; $f_Y({_y}) = 0$"
    mo.vstack([mo.hstack([nr, np_, ny], justify="start", gap=3, wrap=True), mo.md(_text), _fig])
    return


if __name__ == "__main__":
    app.run()

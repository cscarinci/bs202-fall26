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
    header("Lecture 07", "Week 04", "Lecture 07 · Hypergeometric and negative hypergeometric models")
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    **Binomial models** &nbsp; $\leadsto$ &nbsp; count number of “successes” in a fixed number of trials

    $$
    S = \{\, c_1 c_2 \cdots c_n \mid c_i = H \text{ or } T \,\} \qquad (n: \text{number of trials})
    $$

    success with $P(\{H\}) = p$, &nbsp; failure with $P(\{T\}) = 1 - p = q$

    $$
    P(\underbrace{c_1 c_2 \cdots c_n}_{r\ H\text{s}}) = p^r (1 - p)^{n-r} = p^r q^{n-r}, \qquad X(c_1 c_2 \cdots c_n) = \#(H \text{ in } n \text{ trials})
    $$

    $$
    \Longrightarrow \quad \underbrace{f_X(x)}_{B(n, p)(x)} = \begin{cases} \dbinom{n}{x} p^x q^{n-x}, & \text{for } x = \underbrace{0, 1, 2, \dots, n}_{S_X} \\[8pt] 0, & \text{otherwise} \end{cases}
    $$

    ($\tbinom{n}{x}$: # combinations of $x$ objects in $n$ positions)

    **Negative binomial models** &nbsp; $\leadsto$ &nbsp; count number of trials until a fixed target of successes is achieved

    $$
    \begin{aligned}
    S = \{\, c_1 \cdots c_{n-1} c_n \mid\ & n \geq r,\ c_n = H,\ c_i = H \text{ or } T \text{ for } 1 \leq i \leq n - 1, \\
    & \text{and } \#(H \text{ in } c_1 \cdots c_{n-1}) = r - 1 \,\}
    \end{aligned}
    $$

    ($n$ allowed to vary!)

    $$
    P(\underbrace{c_1 \cdots c_{n-1}}_{r - 1\ H\text{s}} \underbrace{c_n}_{\text{always } = H}) = p^r q^{n-r}, \qquad Y(c_1 \cdots c_{n-1} c_n) = \#(\text{trials until } r\ H)
    $$

    $$
    \Longrightarrow \quad \underbrace{f_Y(y)}_{NB(r, p)(y)} = \begin{cases} \dbinom{y - 1}{r - 1} p^r q^{y-r}, & \text{for } y = \underbrace{r, r + 1, \dots}_{S_Y} \\[8pt] 0, & \text{otherwise} \end{cases}
    $$

    ($\tbinom{y-1}{r-1}$: # combinations of $r - 1$ objects in $y - 1$ positions)
    """
            ),
            theorem(
                r"""
    $X$ binomial RV with bias $p$ on $n$ trials, &nbsp; $Y$ negative binomial RV with bias $p$ and target $r$

    $$
    \begin{aligned}
    E[X] &= \mu_X = np, & E[Y] &= \mu_Y = \frac{r}{p} \\[4pt]
    \mathrm{Var}(X) &= \sigma_X^2 = npq, & \mathrm{Var}(Y) &= \sigma_Y^2 = \frac{rq}{p^2} \\[4pt]
    \mathrm{Skew}(X) &= \gamma_X = \frac{q - p}{\sqrt{npq}}, & \mathrm{Skew}(Y) &= \gamma_Y = \frac{1 + q}{\sqrt{rq}}
    \end{aligned}
    $$
    """
            ),
            mo.md(r"**Today:** Hypergeometric & negative hypergeometric models"),
            definition(
                r"""
    A **hypergeometric model** is an experiment that

    1. consists of a sequence of trials (not independent!)
    2. each single trial has one of two outcomes, with exactly $K$ possible “successes” and $N - K$ possible “failures” in total, with all combinations of the $K$ possible successes among the $N$ possible trials being equally likely
    3. measures the number $X$ of “successes” in a fixed number $n$ of trials
    """
            ),
            mo.md(
                r"""
    Draw colored coins from a bag with $K$ red coins and $N - K$ blue coins and without replacing the coins; count $X = \#(\text{red coins in } n \text{ draws})$

    $$
    S = \{\, c_1 c_2 \cdots c_n \mid c_i = R \text{ or } B,\ i = 1, \dots, n \,\}, \qquad S_X = \{0, 1, \dots, n\} \quad (\text{if } n \leq K \text{ and } n \leq N - K)
    $$

    $$
    P(\{c_1 c_2 \cdots c_n\}) = \frac{\dbinom{N - n}{K - k}}{\dbinom{N}{K}} \quad \text{if } X(c_1 c_2 \cdots c_n) = k
    $$

    $N = 5$, $K = 3$, $n = 3$:

    $$
    P(\{RBB\}) = \frac{3}{5} \cdot \frac{2}{4} \cdot \frac{1}{3} = \frac{\binom{5-3}{3-1}}{\binom{5}{3}} = \frac{1}{\frac{5!}{2!\,3!}},
    \qquad
    P(\{BRR\}) = \frac{2}{5} \cdot \frac{3}{4} \cdot \frac{2}{3} = \frac{\binom{5-3}{3-2}}{\binom{5}{3}} = \frac{2!}{\frac{5!}{2!\,3!}}
    $$

    $N = 9$, $K = 5$, $n = 4$:

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
    A RV $X$ is said to have a **hypergeometric distribution** if its pmf is

    $$
    \underbrace{f_X(x)}_{HG(N, K, n)(x)} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}, \qquad \text{for } x \in \mathbb{Z},\ 0 \leq x \leq K \text{ and } 0 \leq n - x \leq N - K \quad (\text{and } f_X(x) = 0 \text{ otherwise})
    $$
    """
            ),
            mo.md(
                r"""
    **Example.** A factory produced 1000 devices, 50 defective. We check a sample of 100 distinct devices. Probability of 7 defective objects in the sample?

    $$
    X = \#\left(\substack{\text{of defective objects} \\ \text{in a sample of 100}}\right) \qquad \leadsto \qquad HG(1000, 50, 100)(x) = \frac{\dbinom{50}{x} \dbinom{1000 - 50}{100 - x}}{\dbinom{1000}{100}} = f_X(x)
    $$

    $$
    \leadsto \quad f_X(7) \approx 11\%, \qquad f_X(5) \approx 19\%, \qquad f_X(3) \approx 14\%
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
def _(BLUE, Figure, RED, hK, hN, hn, hx, math, mo):
    _N, _K, _n, _x = hN.value, hK.value, hn.value, hx.value
    if _K > _N or _n > _N:
        _out = mo.vstack([mo.hstack([mo.vstack([hN, hK]), mo.vstack([hn, hx])], justify="start", gap=3, wrap=True), mo.md(rf"need $K \le N$ and $n \le N$ &nbsp; (here $N = {_N}$)")])
    else:
        _p = _K / _N
        _lo, _hi = max(0, _n - (_N - _K)), min(_K, _n)
        _total = math.comb(_N, _n)
        # Both pmfs on the full range x = 0, ..., n; HG is zero outside its support
        _xs = list(range(_n + 1))
        _hg = [math.comb(_K, x) * math.comb(_N - _K, _n - x) / _total if _lo <= x <= _hi else 0.0 for x in _xs]
        _bi = [math.comb(_n, x) * _p**x * (1 - _p) ** (_n - x) for x in _xs]
        _keep = [i for i in _xs if _hg[i] > 5e-4 or _bi[i] > 5e-4] or _xs
        _a, _b = _keep[0], _keep[-1] + 1
        _fx = _hg[_x] if _x <= _n else 0.0
        _mean = _n * _p
        _fpc = (_N - _n) / (_N - 1) if _N > 1 else 1.0

        _fig = Figure(figsize=(7.4, 3.0), layout="constrained")
        _ax = _fig.subplots()
        _ax.bar(_xs[_a:_b], _hg[_a:_b], width=0.7, color=RED, alpha=0.75, label="$HG(N, K, n)$")
        _ax.plot(_xs[_a:_b], _bi[_a:_b], "o-", color=BLUE, ms=3.5, lw=1, label="$B(n, p)$, $p = K/N$")
        _ax.axvline(_mean, color="#555555", lw=1, ls="--")
        _ax.text(_mean, max(max(_hg), max(_bi)) * 1.08, "$nK/N = np$", ha="center", fontsize=10, color="#555555")
        _ax.set_ylim(0, max(max(_hg), max(_bi)) * 1.25)
        _ax.set_xlabel("$x$")
        _ax.legend(frameon=False, fontsize=11, loc="upper right")
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

        _table = "\n".join(
            [
                "| | |",
                "|:--|--:|",
                rf"| $HG(N, K, n)(x)$ | ${100 * _fx:.3g}\%$ " + ("" if _lo <= _x <= _hi else rf"&nbsp; ($x \notin S_X = \{{{_lo}, \dots, {_hi}\}}$)") + " |",
                rf"| $B(n, K/N)(x)$ | ${100 * (_bi[_x] if _x <= _n else 0):.3g}\%$ |",
                rf"| $E[X] = nK/N$ | ${_mean:.4g}$ |",
                rf"| $\mathrm{{Var}}(X) / npq = (N - n)/(N - 1)$ | ${_fpc:.4g}$ |",
            ]
        )
        _out = mo.vstack([mo.hstack([mo.vstack([hN, hK]), mo.vstack([hn, hx])], justify="start", gap=3, wrap=True), mo.md(_table), _fig])
    _out
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    A **negative hypergeometric model** is an experiment that

    1. consists of a sequence of trials
    2. each single trial has one of two outcomes with exactly $K$ possible “successes” and $N - K$ possible “failures” in total, with all combinations of the $K$ possible successes among the $N$ possible trials being equally likely
    3. measures the number $Y$ of trials until a fixed number $r$ of “successes” is achieved

    $$
    S_Y = \{r, r + 1, \dots, N - K + r\} \quad (r \leq K), \qquad \underbrace{f_Y(y)}_{NHG(N, K, r)} = \frac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}}
    $$
    """
            ),
            mo.md(
                r"""
    **Remark.**

    | | replacement allowed | replacement not allowed |
    |:--|:-:|:-:|
    | # successes in $n$ trials | Binomial | Hypergeometric |
    | # trials until $r$ successes | Negative binomial | Negative hypergeometric |
    """
            ),
            theorem(
                r"""
    For $X$ a hypergeometric RV, &nbsp; $Y$ a negative hypergeometric RV

    $$
    \begin{aligned}
    E[X] &= n \frac{K}{N}, & \mathrm{Var}(X) &= n \frac{K}{N} \left( 1 - \frac{K}{N} \right) \frac{N - n}{N - 1} \\[6pt]
    E[Y] &= r\, \frac{N + 1}{K + 1}, & \mathrm{Var}(Y) &= \frac{r (N + 1)(N - K)(K + 1 - r)}{(K + 1)^2 (K + 2)}
    \end{aligned}
    $$
    """
            ),
            mo.md(
                r"""
    $E[X] = np$ if $p = \tfrac{K}{N}$; &nbsp; $\mathrm{Var}(X) = np(1 - p) \times \underbrace{\dfrac{N - n}{N - 1}}_{\text{finite population correction term}}$

    **Proof.** Similar trick as for binomial

    $$
    x \binom{K}{x} = K \binom{K - 1}{x - 1}, \qquad y \binom{y - 1}{r - 1} = r \binom{y}{r}
    $$

    together with the binomial coefficient identity

    $$
    \binom{N}{n} = \sum_{\substack{0 \leq x \leq K \\ 0 \leq n - x \leq N - K}} \binom{K}{x} \binom{N - K}{n - x}
    $$

    $$
    (1 + t)^N = (1 + t)^K (1 + t)^{N-K}
    $$

    $$
    \begin{aligned}
    \sum_{n} \binom{N}{n} t^{N-n} &= \sum_{k} \binom{K}{k} t^{K-k} \cdot \sum_{\ell} \binom{N - K}{\ell} t^{N-K-\ell} \\
    &= \sum_{k} \sum_{\ell} \binom{K}{k} \binom{N - K}{\ell} t^{N-k-\ell} \overset{k + \ell = n}{=} \sum_{n} \Big[ \sum_{x} \binom{K}{x} \binom{N - K}{n - x} \Big] t^{N-n}
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
def _(BLUE, Figure, RED, gK, gN, gr, math, mo):
    _N, _K, _r = gN.value, gK.value, gr.value
    if _K > _N or _r > _K:
        _out = mo.vstack([mo.hstack([gN, gK, gr], justify="start", gap=3, wrap=True), mo.md(rf"need $K \le N$ and $r \le K$ &nbsp; (here $N = {_N}$, $K = {_K}$)")])
    else:
        _p = _K / _N
        _total = math.comb(_N, _K)
        _ys = list(range(_r, _N - _K + _r + 1))
        _nhg = [math.comb(y - 1, _r - 1) * math.comb(_N - y, _K - _r) / _total for y in _ys]
        _nb = [math.comb(y - 1, _r - 1) * _p**_r * (1 - _p) ** (y - _r) for y in _ys]
        _keep = [i for i in range(len(_ys)) if _nhg[i] > 5e-4 or _nb[i] > 5e-4] or list(range(len(_ys)))
        _a, _b = _keep[0], _keep[-1] + 1
        _mean = _r * (_N + 1) / (_K + 1)

        _fig = Figure(figsize=(7.4, 3.0), layout="constrained")
        _ax = _fig.subplots()
        _ax.bar(_ys[_a:_b], _nhg[_a:_b], width=0.7, color=RED, alpha=0.75, label="$NHG(N, K, r)$")
        _ax.plot(_ys[_a:_b], _nb[_a:_b], "o-", color=BLUE, ms=3.5, lw=1, label="$NB(r, p)$, $p = K/N$")
        _ax.axvline(_mean, color="#555555", lw=1, ls="--")
        _ax.text(_mean, max(max(_nhg), max(_nb)) * 1.08, "$r(N+1)/(K+1)$", ha="center", fontsize=10, color="#555555")
        _ax.set_ylim(0, max(max(_nhg), max(_nb)) * 1.25)
        _ax.set_xlabel("$y$")
        _ax.legend(frameon=False, fontsize=11, loc="upper right")
        for _s in ("top", "right"):
            _ax.spines[_s].set_visible(False)

        _table = "\n".join(
            [
                "| | |",
                "|:--|--:|",
                rf"| $S_Y = \{{r, \dots, N - K + r\}}$ | $\{{{_r}, \dots, {_N - _K + _r}\}}$ |",
                rf"| $E[Y] = r(N + 1)/(K + 1)$ | ${_mean:.4g}$ |",
                rf"| $r/p$ (negative binomial mean) | ${_r / _p:.4g}$ |",
            ]
        )
        _out = mo.vstack([mo.hstack([gN, gK, gr], justify="start", gap=3, wrap=True), mo.md(_table), _fig])
    _out
    return


if __name__ == "__main__":
    app.run()

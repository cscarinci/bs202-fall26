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
    header("Lecture 08", "Week 04", "Lecture 08 · Poisson models")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## So far

    $$
    \begin{aligned}
    B(n, p)(x) &= \binom{n}{x} p^x q^{n-x}, && 0 \leq x \leq n \\[6pt]
    NB(r, p)(y) &= \binom{y - 1}{r - 1} p^r q^{y-r}, && y \geq r \\[6pt]
    HG(N, K, n)(x) &= \frac{\dbinom{n}{x} \dbinom{N - n}{K - x}}{\dbinom{N}{K}} = \frac{\dbinom{K}{x} \dbinom{N - K}{n - x}}{\dbinom{N}{n}}, && \max(0, n + K - N) \leq x \leq \min(n, K) \\[6pt]
    NHG(N, K, r)(y) &= \frac{\dbinom{y - 1}{r - 1} \dbinom{N - y}{K - r}}{\dbinom{N}{K}} = \frac{K}{N}\, \frac{\dbinom{K - 1}{r - 1} \dbinom{N - K}{y - r}}{\dbinom{N - 1}{y - 1}}, && r \leq y \leq N - K + r
    \end{aligned}
    $$

    **Today:** Poisson & Exponential models
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
    """
            ),
            mo.md(
                r"""
    Emails arrive with average rate $\lambda = 3$ per day; &nbsp; $X = \#(\text{emails in 7 days})$ &nbsp; $\Longrightarrow$ &nbsp; $S_X = \{0, 1, 2, \dots\}$

    To compute $f_X$

    (i) split $[0, t]$ into $n$ subintervals of length $h = t/n$

    (ii) for large $n$, each subinterval has 0 or 1 occurrence, with

    $$
    P(\text{exactly 1 occurrence}) \approx \lambda t/n, \qquad P(\text{no occurrences}) \approx 1 - \lambda t/n
    $$

    (iii) by assumption each subinterval is independent

    $\therefore$ &nbsp; we can think of our Poisson model as a sequence of identical independent *trials* (occurrences in each subinterval), each with one of two possible outcomes with

    $$
    P(\text{“success”}) \approx \lambda t/n, \qquad P(\text{“failure”}) \approx 1 - \lambda t/n \qquad (\text{“success”: occurrence})
    $$

    where we are measuring the number $X$ of “successes” in $n$ trials!

    $$
    \Longrightarrow \quad f_X(x) \approx B(n, \lambda t/n)(x) \qquad (\text{for large } n\,!)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad f_X(x) &= \lim_{n \to \infty} \binom{n}{x} \left( \frac{\lambda t}{n} \right)^{\!x} \left( 1 - \frac{\lambda t}{n} \right)^{\!n-x} \\[6pt]
    &= \lim_{n \to \infty} \underbrace{\frac{n (n - 1) \cdots (n - x + 1)}{n^x}}_{\approx\, 1}\, \frac{(\lambda t)^x}{x!} \left( 1 - \frac{\lambda t}{n} \right)^{\!n} \underbrace{\left( 1 - \frac{\lambda t}{n} \right)^{\!-x}}_{\approx\, 1} \\[6pt]
    &= \frac{(\lambda t)^x}{x!} \underbrace{\lim_{n \to \infty} \left( 1 - \frac{\lambda t}{n} \right)^{\!n}}_{e^{-\lambda t}} = e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} \qquad x = 0, 1, 2, \dots
    \end{aligned}
    $$
    """
            ),
            definition(
                r"""
    A RV $X$ is said to have a **Poisson distribution** with rate $\lambda$ over an interval of length $t$ if its pmf is

    $$
    \underbrace{f_X(x)}_{\mathrm{Pois}(\lambda t)(x)} = \begin{cases} e^{-\lambda t}\, \dfrac{(\lambda t)^x}{x!}, & x = 0, 1, 2, \dots \\[8pt] 0, & x \neq 0, 1, 2, \dots \end{cases}
    \qquad (\lambda t: \text{single parameter})
    $$
    """
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
def _(BLUE, Figure, RED, lam_t, math, mo, n_sub, np, p_redo, px):
    _m, _n, _x = lam_t.value, n_sub.value, px.value
    _top = int(_m + 4 * math.sqrt(_m) + 4)
    _xs = list(range(_top + 1))
    _pois = [math.exp(-_m) * _m**x / math.factorial(x) for x in _xs]
    _p = _m / _n

    _fig = Figure(figsize=(7.4, 4.2), layout="constrained")
    _ax, _tl = _fig.subplots(2, 1, height_ratios=[3, 1])
    _ax.bar(_xs, _pois, width=0.7, color=[BLUE if _k == _x else RED for _k in _xs], alpha=0.75, label=r"$\mathrm{Pois}(\lambda t)$")
    if _p <= 1:
        _bin = [math.comb(_n, x) * _p**x * (1 - _p) ** (_n - x) if x <= _n else 0.0 for x in _xs]
        _ax.plot(_xs, _bin, "o-", color=BLUE, ms=3.5, lw=1, label=r"$B(n, \lambda t / n)$")
        _note = rf"$\lambda t / n = {_p:.3g}$"
    else:
        _note = r"$\lambda t / n > 1$: take $n$ larger"
    _ax.set_xlabel("$x$")
    _ax.legend(frameon=False, fontsize=11)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    # One realisation of the construction: n subintervals, each with an occurrence with probability λt/n
    _rng = np.random.default_rng(808 + p_redo.value)
    _hits = np.nonzero(_rng.random(_n) < min(_p, 1))[0]
    for _k in range(_n + 1):
        _tl.axvline(_k / _n, color="#cccccc", lw=0.6)
    _tl.plot((_hits + 0.5) / _n, np.zeros(len(_hits)), "|", color=RED, ms=14, mew=2)
    _tl.set_xlim(0, 1)
    _tl.set_yticks([])
    _tl.set_xticks([0, 1], ["$0$", "$t$"])
    _tl.set_title(rf"one trial of the experiment: $n = {_n}$ subintervals, {len(_hits)} occurrences", fontsize=10)
    for _s in ("top", "right", "left"):
        _tl.spines[_s].set_visible(False)

    _px = math.exp(-_m) * _m**_x / math.factorial(_x)
    _le = sum(_pois[: _x + 1]) if _x <= _top else 1.0
    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $\mathrm{{Pois}}(\lambda t)(x) = e^{{-\lambda t}} (\lambda t)^x / x!$ | ${100 * _px:.3g}\%$ |",
            rf"| $P(X \le x)$ | ${100 * _le:.3g}\%$ |",
            rf"| $P(X \ge x)$ | ${100 * (1 - _le + _px):.3g}\%$ |",
        ]
    )
    mo.vstack(
        [
            mo.hstack([lam_t, px], justify="start", gap=3, wrap=True),
            mo.md(_table),
            mo.hstack([n_sub, mo.md(_note), p_redo], justify="start", gap=3, align="center", wrap=True),
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

    $X = \#(\text{accidents in one month})$

    $$
    P(X = 0) = e^{-2} \approx 13.5\%
    $$

    $$
    P(X \geq 3) = 1 - P(X < 3) = 1 - e^{-2} - e^{-2} \cdot 2 - e^{-2} \cdot \frac{4}{2!} = 1 - 5 e^{-2} \approx 32.3\%
    $$
    """
            ),
            theorem(
                r"""
    $X$ a Poisson RV with rate $\lambda$ over a period $t$

    $$
    E[X] = \lambda t, \qquad \mathrm{Var}(X) = \lambda t, \qquad \mathrm{Skew}(X) = \frac{1}{\sqrt{\lambda t}}
    $$
    """
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
    \mathrm{Var}(X) &= E[X(X - 1)] + E[X] - E[X]^2 \\
    &= \sum_{x=0}^{\infty} x (x - 1)\, e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} + \lambda t - (\lambda t)^2 \\
    &= \underbrace{\sum_{x-2=0}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^{x-2}}{(x - 2)!}}_{1}\, (\lambda t)^2 + \lambda t - (\lambda t)^2 = \lambda t
    \end{aligned}
    $$

    $$
    \mathrm{Skew}(X) = E\!\left[ \left( \frac{X - \mu_X}{\sigma_X} \right)^{\!3} \right] = E\!\left[ \left( \frac{X - \lambda t}{\sqrt{\lambda t}} \right)^{\!3} \right] = \sum_{x=0}^{\infty} \left( \frac{x - \lambda t}{\sqrt{\lambda t}} \right)^{\!3} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = \cdots
    $$

    (we will learn later a simpler way…)

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
def _(BLUE, Figure, RED, an, ap, math, mo):
    _n, _p = an.value, ap.value
    _m = _n * _p
    _top = min(_n, int(_m + 4 * math.sqrt(_m) + 4))
    _xs = list(range(_top + 1))
    _bin = [math.comb(_n, x) * _p**x * (1 - _p) ** (_n - x) for x in _xs]
    _pois = [math.exp(-_m) * _m**x / math.factorial(x) for x in _xs]
    _err = max(abs(a - b) for a, b in zip(_bin, _pois))

    _fig = Figure(figsize=(7.4, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.bar(_xs, _bin, width=0.7, color=RED, alpha=0.75, label="$B(n, p)$")
    _ax.plot(_xs, _pois, "o-", color=BLUE, ms=3.5, lw=1, label=r"$\mathrm{Pois}(np)$")
    _ax.set_xlabel("$x$")
    _ax.legend(frameon=False, fontsize=11)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    mo.vstack(
        [
            mo.hstack([an, ap], justify="start", gap=3, wrap=True),
            mo.md(rf"$np = {_m:.3g}$, &nbsp;&nbsp; $\max_x \lvert B(n, p)(x) - \mathrm{{Pois}}(np)(x) \rvert = {_err:.3g}$"),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    A **gamma model** is a random experiment that

    1. consists of occurrences along a continuous interval, with the number of occurrences in disjoint subintervals being independent of one another
    2. the average rate of occurrences is a constant $\lambda > 0$, and for small subintervals of length $h$ we have:

        $$
        P\left(\substack{\text{exactly one} \\ \text{occurrence}}\right) \approx \lambda h, \qquad P\left(\substack{\text{two or more} \\ \text{occurrences}}\right) \approx 0.
        $$

    3. measures the length $Y$ until a fixed number $r$ of occurrences is achieved
    """
            ),
            mo.md(
                r"""
    Emails arriving at an average rate $\lambda = 3$ per day; &nbsp; $Y$ = time until the 2nd email (not necessarily an integer)

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


if __name__ == "__main__":
    app.run()

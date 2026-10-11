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
    header("Lecture 09", "Week 05", "Lecture 09 · Continuous random variables; gamma and exponential distributions")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    Poisson & gamma models

    $X = \#(\text{occurrences in fixed interval } [0, t])$ &nbsp; — constant average rate $\lambda$; independent for disjoint intervals

    $$
    S_X = \{0, 1, 2, \dots\}, \qquad f_X(x) = e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} \qquad \leadsto \quad \sum_{x=0}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = e^{-\lambda t} e^{\lambda t} = 1
    $$

    $Y$ = length of interval until $r$ occurrences

    $$
    S_Y = (0, +\infty) \qquad \text{continuous (not countable)}
    $$

    **Today:** RVs with continuous state spaces

    **Recall:** $X : S \longrightarrow \mathbb{R}$ discrete RV if $S_X = \mathrm{Im}(X)$ is countable

    $$
    \leadsto \quad P_X(A) = P(X \in A) = \sum_{x \in A \cap S_X} \underbrace{f_X(x)}_{\text{pmf: } P(X = x)}
    $$

    $$
    \leadsto \quad \underbrace{F_X(x)}_{\text{cdf}} = P(X \leq x) = \sum_{y \in (-\infty, x] \cap S_X} f_X(y)
    \qquad \Longrightarrow \qquad f_X(x) = F_X(x) - F_X(x^-) \quad (F_X(x^-) = P(X < x): \text{value of } F_X \text{ just before } x)
    $$
    """
            ),
            definition(
                r"""
    A RV $X : S \longrightarrow \mathbb{R}$ is **continuous** if

    - $S_X$ is uncountable
    - there exists $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ continuous (cdf) s.t.

        $$
        P(X \leq x) = F_X(x)
        $$

        (does not follow from the assumption on $S_X$ only!)
    """
            ),
            mo.md(
                r"""
    **Corollary.** $X$ continuous RV &nbsp; $\Longrightarrow$ &nbsp; $P(X = x) = 0 \quad \forall\, x \in \mathbb{R}$! &nbsp; (no notion of pmf)

    $$
    \Longrightarrow \quad P(a \leq X \leq b) = F_X(b) - F_X(a)
    $$
    """
            ),
            definition(
                r"""
    A RV $X : S \longrightarrow \mathbb{R}$ is **continuous** if

    - $S_X$ is uncountable
    - there exists $f_X : \mathbb{R} \longrightarrow \mathbb{R}$ integrable (pdf: prob. density function) s.t.

        $$
        P(a \leq X \leq b) = \int_a^b f_X(x)\, dx = F_X(b) - F_X(a)
        $$
    """
            ),
            mo.md(
                r"""
    In this course, continuous RVs are those with a pdf; continuity of the cdf then follows from $F_X(x) = \int_{-\infty}^{x} f_X(u)\, du$.

    $F_X : \mathbb{R} \longrightarrow \mathbb{R}$ must satisfy

    - $F_X(x_1) \leq F_X(x_2) \quad \forall\, x_1 \leq x_2$
    - $\displaystyle\lim_{x \to -\infty} F_X(x) = 0$, &nbsp; $\displaystyle\lim_{x \to +\infty} F_X(x) = 1$

    $f_X$ must satisfy

    - $f_X(x) \geq 0 \quad \forall\, x \in \mathbb{R}$
    - $\displaystyle\int_{-\infty}^{+\infty} f_X(x)\, dx = 1$

    $$
    \text{Given } F_X \ \Longrightarrow \ f_X(x) = \frac{d}{dx} F_X(x), \qquad \qquad \text{Given } f_X \ \Longrightarrow \ F_X(x) = \int_{-\infty}^{x} f_X(u)\, du
    $$

    **Example.** Given $X$ a Poisson RV with avg. rate $\lambda$ over an interval $[0, t]$, the corresponding Gamma RV $Y$ with avg. rate $\lambda$ and occurrence target $r$ is a continuous RV!

    **Proof.** Note that

    $$
    \underbrace{P(X \geq r)}_{\text{at least } r \text{ occurrences before length } t} = \underbrace{P(Y \leq t)}_{\text{less than length } t \text{ until } r \text{ occurrences}}
    $$

    $$
    \Longrightarrow \quad \sum_{x=r}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} = P(Y \leq t) = F_Y(t)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad f_Y(t) = \frac{d}{dt} \left( \sum_{x=r}^{\infty} e^{-\lambda t}\, \frac{(\lambda t)^x}{x!} \right)
    &= \sum_{x=r}^{\infty} \lambda e^{-\lambda t} \left( -\frac{(\lambda t)^x}{x!} + \frac{(\lambda t)^{x-1}}{(x - 1)!} \right) = \lambda e^{-\lambda t} \left[ \sum_{x=r}^{\infty} \frac{(\lambda t)^{x-1}}{(x - 1)!} - \sum_{x=r}^{\infty} \frac{(\lambda t)^x}{x!} \right] \\[6pt]
    &= \lambda e^{-\lambda t}\, \frac{(\lambda t)^{r-1}}{(r - 1)!} = \underbrace{\frac{\lambda^r t^{r-1}}{(r - 1)!}\, e^{-\lambda t}}_{\mathrm{Gamma}(r, \lambda)(t)}
    \end{aligned}
    $$

    **Remark.** Similar derivations of $NB(r, p)$ from $B(n, p)$ and $NHG(N, K, r)$ from $HG(N, K, n)$ are possible!

    $$
    \underbrace{P(X_n \geq r)}_{\text{at least } r\ H\text{s in } n \text{ flips}} = \underbrace{P(Y_r \leq n)}_{\text{at most } n \text{ flips until } r\ H\text{s}}
    $$
    """
            ),
            definition(
                r"""
    A continuous RV $Y : S \longrightarrow \mathbb{R}$ is said to have a **gamma distribution** with rate $\lambda$ and target $r$ if its pdf is

    $$
    f_Y(y) = \begin{cases} \dfrac{\lambda^r y^{r-1}}{(r - 1)!}\, e^{-\lambda y}, & y \in (0, +\infty) \\[8pt] 0, & y \notin (0, +\infty) \end{cases}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    g_lam = mo.ui.slider(0.2, 4, 0.1, value=1, label=r"$\lambda$", show_value=True)
    g_a = mo.ui.slider(0, 10, 0.1, value=0, label="$a$", show_value=True)
    g_b = mo.ui.slider(0, 10, 0.1, value=2, label="$b$", show_value=True)
    g_r = mo.ui.slider(1, 6, 1, value=2, label="$r$ (shaded)", show_value=True)
    g_t = mo.ui.slider(0.1, 10, 0.1, value=2, label="$t$", show_value=True)
    return g_a, g_b, g_lam, g_r, g_t


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, g_a, g_b, g_lam, g_r, g_t, math, mo, np):
    _lam, _r, _t = g_lam.value, g_r.value, g_t.value
    _a, _b = sorted((g_a.value, g_b.value))

    def _pdf(y, r):
        return _lam**r * y ** (r - 1) / math.factorial(r - 1) * np.exp(-_lam * y)

    def _cdf(t, r):
        return 1 - sum(np.exp(-_lam * t) * (_lam * t) ** k / math.factorial(k) for k in range(r))

    _y = np.linspace(0, 10, 500)
    _fig = Figure(figsize=(9.0, 3.2), layout="constrained")
    _ax, _cx = _fig.subplots(1, 2)
    for _k, _col in ((1, RED), (2, BLUE), (3, "black")):
        _ax.plot(_y, _pdf(_y, _k), color=_col, lw=1.3, label=f"$r = {_k}$")
    if _r > 3:
        _ax.plot(_y, _pdf(_y, _r), color="#9a6b1f", lw=1.3, label=f"$r = {_r}$")
    _yy = np.linspace(_a, _b, 200)
    _ax.fill_between(_yy, _pdf(_yy, _r), color="#9a6b1f", alpha=0.3, lw=0)
    _ax.set_xlim(0, 10)
    _ax.set_ylim(0, None)
    _ax.set_xlabel("$y$")
    _ax.set_title("pdf  $f_Y(y)$", fontsize=12)
    _ax.legend(frameon=False, fontsize=10)
    _cx.plot(_y, _cdf(_y, _r), color="#9a6b1f", lw=1.5)
    _Fa, _Fb = float(_cdf(_a, _r)), float(_cdf(_b, _r))
    _cx.plot([_a, _a, 0], [0, _Fa, _Fa], ":", color="#9a6b1f", lw=1)
    _cx.plot([_b, _b, 0], [0, _Fb, _Fb], ":", color="#9a6b1f", lw=1)
    _cx.annotate("", xy=(0.3, _Fb), xytext=(0.3, _Fa), arrowprops={"arrowstyle": "<->", "color": "#9a6b1f", "lw": 1.2})
    _cx.set_xlim(0, 10)
    _cx.set_ylim(0, 1.05)
    _cx.set_xlabel("$y$")
    _cx.set_title(f"cdf  $F_Y(y)$,  $r = {_r}$", fontsize=12)
    for _axx in (_ax, _cx):
        for _s in ("top", "right"):
            _axx.spines[_s].set_visible(False)

    _pois_tail = 1 - sum(math.exp(-_lam * _t) * (_lam * _t) ** k / math.factorial(k) for k in range(_r))
    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $P(a \le Y \le b) = F_Y(b) - F_Y(a)$ | ${_Fb - _Fa:.4f}$ |",
            rf"| $P(X \ge r) = \sum_{{x \ge r}} \mathrm{{Pois}}(\lambda t)(x)$ | ${_pois_tail:.4f}$ |",
            rf"| $P(Y \le t) = F_Y(t)$ | ${float(_cdf(_t, _r)):.4f}$ |",
        ]
    )
    mo.vstack(
        [
            mo.hstack([g_lam, g_r, g_a, g_b, g_t], justify="start", gap=2, wrap=True),
            mo.md(_table),
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
    **Example.** Hyeonpung has 2 car accidents per month

    $$
    P(\text{1 car accident in less than } \underbrace{\text{10 days}}_{1/3 \text{ months}}) = \ ?
    $$

    $Y$ = time until 1 accident

    $$
    \Longrightarrow \quad f_Y(y) = \lambda e^{-\lambda y} \qquad \leadsto \quad \mathrm{Gamma}(1, \lambda) = \mathrm{Exp}(\lambda) \quad \text{exponential distribution}
    $$

    $$
    \underbrace{P(Y \leq \tfrac{1}{3})}_{F_Y(1/3)} = \int_{0}^{1/3} \lambda e^{-\lambda y}\, dy = -e^{-\lambda y}\, \Big|_{0}^{1/3} = 1 - e^{-\lambda/3} = 1 - e^{-2/3} \approx 48.6\%
    $$

    $$
    P\left(\substack{\text{1 car accident in the 10 days after} \\ \text{20 days without accidents}}\right) = \ ?
    $$

    $$
    \begin{aligned}
    &= P(Y \leq 1 \mid Y > \tfrac{2}{3}) = \frac{P(\tfrac{2}{3} < Y \leq 1)}{P(\tfrac{2}{3} < Y)} = \frac{F_Y(1) - F_Y(\tfrac{2}{3})}{1 - F_Y(\tfrac{2}{3})} \\[6pt]
    &= \frac{(1 - e^{-\lambda}) - (1 - e^{-2\lambda/3})}{1 - (1 - e^{-2\lambda/3})} = \frac{e^{-2\lambda/3} - e^{-\lambda}}{e^{-2\lambda/3}} = 1 - e^{-\lambda/3} = 1 - e^{-2/3} \approx 48.6\%
    \end{aligned}
    $$
    """
            ),
            theorem(
                r"""
    The exponential distribution (gamma with $r = 1$) has no memory!

    If $Y \sim \mathrm{Exp}(\lambda)$ &nbsp; ($Y$ has $f_Y(y) = \mathrm{Exp}(\lambda)(y)$) &nbsp; then

    $$
    P(Y \leq s + t \mid Y > s) = P(Y \leq t)
    $$
    """
            ),
            mo.md(
                r"""
    How long we have already waited does not change how long we still have to wait until the next occurrence.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    m_lam = mo.ui.slider(0.1, 4, 0.1, value=2, label=r"$\lambda$", show_value=True)
    m_s = mo.ui.slider(0, 3, 0.05, value=0.65, label="$s$ (already waited)", show_value=True)
    m_t = mo.ui.slider(0.05, 3, 0.05, value=0.35, label="$t$", show_value=True)
    return m_lam, m_s, m_t


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, m_lam, m_s, m_t, math, mo, np):
    _l, _s, _t = m_lam.value, m_s.value, m_t.value
    _F = lambda y: 1 - math.exp(-_l * y)
    _cond = (_F(_s + _t) - _F(_s)) / (1 - _F(_s))

    _fig = Figure(figsize=(7.4, 2.8), layout="constrained")
    _ax = _fig.subplots()
    _hi = max(6 / _l, _s + _t + 0.5)
    _y = np.linspace(0, _hi, 400)
    _pdf = _l * np.exp(-_l * _y)
    _ax.plot(_y, _pdf, color="black", lw=1.3)
    _y1 = np.linspace(0, _t, 100)
    _ax.fill_between(_y1, _l * np.exp(-_l * _y1), color=BLUE, alpha=0.25, lw=0, label=rf"$P(Y \leq t)$")
    _y2 = np.linspace(_s, _s + _t, 100)
    _ax.fill_between(_y2, _l * np.exp(-_l * _y2), color=RED, alpha=0.35, lw=0, label=rf"$P(s < Y \leq s + t)$")
    _y3 = np.linspace(_s, _hi, 200)
    _ax.fill_between(_y3, _l * np.exp(-_l * _y3), facecolor="none", edgecolor=RED, hatch="///", lw=0, alpha=0.5, label=r"$P(Y > s)$")
    _ax.set_xlim(0, _hi)
    _ax.set_ylim(0, _l * 1.1)
    _ax.set_xticks([0, _t, _s, _s + _t], ["$0$", "$t$", "$s$", "$s + t$"])
    _ax.set_ylabel("$f_Y(y)$")
    _ax.legend(frameon=False, fontsize=10)
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $P(Y \leq s + t \mid Y > s) = \dfrac{{F_Y(s + t) - F_Y(s)}}{{1 - F_Y(s)}}$ | ${_cond:.4f}$ |",
            rf"| $P(Y \leq t) = F_Y(t) = 1 - e^{{-\lambda t}}$ | ${_F(_t):.4f}$ |",
        ]
    )
    mo.vstack([mo.hstack([m_lam, m_s, m_t], justify="start", gap=3, wrap=True), mo.md(_table), mo.md("red area divided by hatched area equals the blue area:"), _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** LED lightbulbs have failure rate of $\lambda = 0.2$ per year following an exponential model (approximately)

    $\Longrightarrow$ &nbsp; the probability of a failure in the next 3 months is independent of how long ago you bought the lightbulb!

    $$
    P(Y \leq s + \tfrac{1}{4} \mid Y > s) = P(Y \leq \tfrac{1}{4}) = 1 - e^{-\lambda/4} \approx 0.05
    $$

    **Remark.** The negative binomial distribution with target $r = 1$ is also memoryless! &nbsp; $NB(1, p) = \mathrm{Geom}(p)$ is called the geometric distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    q_p = mo.ui.slider(0.05, 0.95, 0.05, value=0.3, label="$p$", show_value=True)
    q_s = mo.ui.slider(0, 20, 1, value=4, label="$s$ (flips already made)", show_value=True)
    q_t = mo.ui.slider(1, 20, 1, value=3, label="$t$", show_value=True)
    return q_p, q_s, q_t


@app.cell(hide_code=True)
def _(mo, q_p, q_s, q_t):
    _p, _s, _t = q_p.value, q_s.value, q_t.value
    _F = lambda y: 1 - (1 - _p) ** y  # P(Y <= y) for Y ~ Geom(p), y = 0, 1, 2, ...
    _cond = (_F(_s + _t) - _F(_s)) / (1 - _F(_s))
    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $P(Y \leq s + t \mid Y > s)$ | ${_cond:.4f}$ |",
            rf"| $P(Y \leq t) = 1 - (1 - p)^t$ | ${_F(_t):.4f}$ |",
        ]
    )
    mo.vstack([mo.md(r"Check for $Y \sim \mathrm{Geom}(p)$ (number of flips until the first $H$):"), mo.hstack([q_p, q_s, q_t], justify="start", gap=3, wrap=True), mo.md(_table)])
    return


if __name__ == "__main__":
    app.run()

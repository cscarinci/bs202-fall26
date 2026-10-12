import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Guided Practice 1", css_file="bs202.css")


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
    header("Guided Practice 1", "Week 05", "Guided Practice 1")
    return


@app.cell(hide_code=True)
def _(math, np):
    # ---- Probability models used below ---------------------------------
    def binomial_pmf(x, n, p):
        return math.comb(n, x) * p**x * (1 - p) ** (n - x) if 0 <= x <= n else 0.0

    def neg_binomial_pmf(y, r, p):
        return math.comb(y - 1, r - 1) * p**r * (1 - p) ** (y - r) if y >= r else 0.0

    def hypergeometric_pmf(x, N, K, n):
        return math.comb(K, x) * math.comb(N - K, n - x) / math.comb(N, n) if max(0, n - N + K) <= x <= min(K, n) else 0.0

    def neg_hypergeometric_pmf(y, N, K, r):
        return math.comb(y - 1, r - 1) * math.comb(N - y, K - r) / math.comb(N, K) if r <= y <= N - K + r else 0.0

    def poisson_pmf(x, mean):
        return math.exp(-mean + x * math.log(mean) - math.lgamma(x + 1)) if x >= 0 and mean > 0 else float(x == 0)

    def seat_open_probability(t, seats, rate):
        return sum(poisson_pmf(k, rate * t) for k in range(seats))

    def posterior(prevalence, sensitivity, specificity):
        a, b = prevalence * sensitivity, (1 - prevalence) * (1 - specificity)
        return a / (a + b)

    def population_grid(ax, groups, per_square, N=50):
        """groups: four (count, colour, label). The first two fill a block in the top-left corner;
        the rest fill the remaining cells in reading order. One square = per_square people."""
        from matplotlib.colors import to_rgb

        q = [int(round(n / per_square)) for n, _, _ in groups]
        w = max(1, int(np.ceil((q[0] + q[1]) / N)))
        h = int(np.ceil((q[0] + q[1]) / w))
        idx = np.full((N, N), -1)
        for k, (r, c) in enumerate([(r, c) for r in range(h) for c in range(w)][: q[0] + q[1]]):
            idx[r, c] = 0 if k < q[0] else 1
        rest = [(r, c) for r in range(N) for c in range(N) if idx[r, c] < 0]
        for k, (r, c) in enumerate(rest):
            idx[r, c] = 2 if k < q[2] else 3
        rgb = np.array([to_rgb(colour) for _, colour, _ in groups])[idx]
        ax.imshow(rgb, interpolation="nearest", extent=(0, N, N, 0))
        ax.set_xticks(np.arange(0, N + 1), minor=True)
        ax.set_yticks(np.arange(0, N + 1), minor=True)
        ax.grid(which="minor", color="white", lw=0.4)
        ax.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
        for sp in ax.spines.values():
            sp.set_visible(False)
        for i, (n, colour, label) in enumerate(groups):
            ax.text(N + 1.5, 3 + 4 * i, f"{n:,}  {label}", color=colour, fontsize=10, va="center")
        ax.set_xlim(0, N + 30)
        ax.set_ylim(N + 2, -1)
        ax.set_aspect("equal")

    return binomial_pmf, hypergeometric_pmf, neg_binomial_pmf, neg_hypergeometric_pmf, poisson_pmf, population_grid, posterior, seat_open_probability


@app.cell(hide_code=True)
def _(box):
    q1_boxes = tuple(box() for _ in range(6))
    return (q1_boxes,)


@app.cell(hide_code=True)
def _(ask, mo, posterior, q1_boxes):
    _a, _b1, _b2, _b3, _c, _d = q1_boxes
    mo.vstack(
        [
            mo.md(
                r"""
    ## Question 1

    A disease has prevalence $P(I) = 0.01$, and a test for this disease has sensitivity $P(+ \mid I) = 0.80$ and specificity $P(- \mid I^c) = 0.95$, where $I$ is the event that a randomly chosen person is infected and $+$ the event that the test is positive.

    (a) Find the probability that a person who tests positive is infected, $P(I \mid +)$.
    """
            ),
            ask(r"$P(I \mid +) =$", _a, posterior(0.01, 0.80, 0.95), 0.002),
            mo.md(
                r"""
    (b) Find $P(I \mid +)$ when we increase (i) the prevalence to $0.05$; (ii) the sensitivity to $0.84$; (iii) the specificity to $0.99$. Assume the other two values are kept as in (a).
    """
            ),
            ask(r"(i) $P(I \mid +) =$", _b1, posterior(0.05, 0.80, 0.95), 0.002),
            ask(r"(ii) $P(I \mid +) =$", _b2, posterior(0.01, 0.84, 0.95), 0.002),
            ask(r"(iii) $P(I \mid +) =$", _b3, posterior(0.01, 0.80, 0.99), 0.002),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    t_pop = mo.ui.slider(1000, 100000, 1000, value=10000, label="population", show_value=True)
    t_prev = mo.ui.slider(0.001, 0.5, 0.001, value=0.01, label="prevalence $P(I)$", show_value=True)
    t_sens = mo.ui.slider(0.5, 1.0, 0.01, value=0.80, label="sensitivity", show_value=True)
    t_spec = mo.ui.slider(0.80, 1.0, 0.005, value=0.95, label="specificity", show_value=True)
    t_step = mo.ui.slider(0.01, 0.2, 0.01, value=0.04, label="step", show_value=True)
    return t_pop, t_prev, t_sens, t_spec, t_step


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, mo, population_grid, posterior, t_pop, t_prev, t_sens, t_spec, t_step):
    ORANGE = "#e5a23b"
    _pop, _step = t_pop.value, t_step.value
    _N = 50
    _per = _pop / _N**2
    _base = dict(prevalence=t_prev.value, sensitivity=t_sens.value, specificity=t_spec.value)
    _fig = Figure(figsize=(8.4, 4 * 5.4), layout="constrained")
    _rows = []
    for _ax, _changed in zip(_fig.subplots(4, 1), [None, "prevalence", "sensitivity", "specificity"]):
        _s = dict(_base)
        if _changed:
            _s[_changed] = min(1, _s[_changed] + _step)
        _ninf = _s["prevalence"] * _pop
        _tp, _fn = round(_ninf * _s["sensitivity"]), round(_ninf * (1 - _s["sensitivity"]))
        _fp = round((_pop - _ninf) * (1 - _s["specificity"]))
        _tn = _pop - _tp - _fn - _fp
        population_grid(_ax, [(_tp, RED, "infected, positive"), (_fn, ORANGE, "infected, negative"), (_fp, BLUE, "not infected, positive"), (_tn, GREY, "not infected, negative")], _per, _N)
        _ax.set_title(("base scenario" if not _changed else f"{_changed} + {_step:g}") + f":  P(I) = {_s['prevalence']:g},  sens {_s['sensitivity']:.2f},  spec {_s['specificity']:.3g}", fontsize=10, loc="left")
        _ax.text(0, _N + 1.5, f"positive: {_tp:,} infected + {_fp:,} not = {_tp + _fp:,}      $P(I \\mid +) = {_tp / (_tp + _fp):.3f}$", fontsize=10, va="top")
        _rows.append((_changed or "base scenario", _s, _tp, _fp))
    _fig.suptitle(f"population {_pop:,}, one square = {_per:g} people", fontsize=10, color="grey")
    _table = "\n".join(
        ["| scenario | $P(I)$ | sens | spec | TP | FP | $P(I \\mid +)$ from counts | exact |", "|:--|--:|--:|--:|--:|--:|--:|--:|"]
        + [rf"| {_k} | ${_s['prevalence']:.3f}$ | ${_s['sensitivity']:.2f}$ | ${_s['specificity']:.3f}$ | ${_tp:,}$ | ${_fp:,}$ | ${_tp / (_tp + _fp):.3f}$ | ${posterior(**_s):.4f}$ |".replace(",", r"\,") for _k, _s, _tp, _fp in _rows]
    )
    mo.accordion({"Simulation [cell 1]": mo.vstack([mo.hstack([t_pop, t_prev, t_sens, t_spec, t_step], justify="start", gap=2, wrap=True), mo.md(_table), _fig])})
    return


@app.cell(hide_code=True)
def _(ask, mo, posterior, q1_boxes):
    _c = q1_boxes[4]
    mo.vstack([mo.md(r"(c) Find the maximum $P(I \mid +)$ when only the sensitivity can change."), ask(r"$\max P(I \mid +) =$", _c, posterior(0.01, 1.0, 0.95), 0.002)])
    return


@app.cell(hide_code=True)
def _(mo):
    c_prev = mo.ui.slider(0.001, 0.5, 0.001, value=0.01, label="prevalence $P(I)$", show_value=True)
    c_sens = mo.ui.slider(0.5, 1.0, 0.01, value=0.80, label="sensitivity", show_value=True)
    c_spec = mo.ui.slider(0.80, 1.0, 0.005, value=0.95, label="specificity", show_value=True)
    c_step = mo.ui.slider(0.01, 0.2, 0.01, value=0.04, label="step", show_value=True)
    return c_prev, c_sens, c_spec, c_step


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, c_prev, c_sens, c_spec, c_step, mo, np, posterior):
    _base = dict(prevalence=c_prev.value, sensitivity=c_sens.value, specificity=c_spec.value)
    _step = c_step.value
    _cfig = Figure(figsize=(9.6, 2.8), layout="constrained")
    _grids = [("prevalence", np.logspace(-3, np.log10(0.6), 300)), ("sensitivity", np.linspace(0.5, 1, 300)), ("specificity", np.linspace(0.90, 1, 300))]
    for _ax, (_name, _grid) in zip(_cfig.subplots(1, 3), _grids):
        _ax.plot(_grid, [posterior(**{**_base, _name: v}) for v in _grid], color=BLUE, lw=1.4)
        _ax.plot([_base[_name]], [posterior(**_base)], "o", color="black", ms=5, label="base scenario")
        _v = min(1, _base[_name] + _step)
        _ax.plot([_v], [posterior(**{**_base, _name: _v})], "o", color=RED, ms=5, label=f"{_name} + {_step:g}")
        _ax.set_xlabel(_name)
        _ax.set_ylim(0, 1)
        _ax.set_ylabel(r"$P(I \mid +)$")
        _ax.legend(fontsize=8, frameon=False)
        if _name == "prevalence":
            _ax.set_xscale("log")
        for _sp in ("top", "right"):
            _ax.spines[_sp].set_visible(False)
    _cfig.suptitle(r"$P(I \mid +)$ against one input, the other two held at the base values", fontsize=10)
    mo.accordion({"Simulation [cell 2]": mo.vstack([mo.hstack([c_prev, c_sens, c_spec, c_step], justify="start", gap=2, wrap=True), _cfig])})
    return


@app.cell(hide_code=True)
def _(ask, mo, q1_boxes):
    _d = q1_boxes[5]
    mo.vstack([mo.md(r"(d) Find $P(I \mid +, +)$ for two tests independent given infection status."), ask(r"$P(I \mid +, +) =$", _d, 0.01 * 0.8**2 / (0.01 * 0.8**2 + 0.99 * 0.05**2), 0.002)])
    return


@app.cell(hide_code=True)
def _(mo):
    d_pop = mo.ui.slider(1000, 100000, 1000, value=10000, label="population", show_value=True)
    d_prev = mo.ui.slider(0.001, 0.5, 0.001, value=0.01, label="prevalence $P(I)$", show_value=True)
    d_sens = mo.ui.slider(0.5, 1.0, 0.01, value=0.80, label="sensitivity", show_value=True)
    d_spec = mo.ui.slider(0.80, 1.0, 0.005, value=0.95, label="specificity", show_value=True)
    return d_pop, d_prev, d_sens, d_spec


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, d_pop, d_prev, d_sens, d_spec, mo, np, population_grid):
    _ORANGE = "#e5a23b"
    _pop = d_pop.value
    _N = 50
    _per = _pop / _N**2
    _prev, _sens, _spec = d_prev.value, d_sens.value, d_spec.value
    _ninf = round(_prev * _pop)
    _nnot = _pop - _ninf
    _tfig = Figure(figsize=(8.4, 2 * 5.4), layout="constrained")
    for _ax, _tests in zip(_tfig.subplots(2, 1), (1, 2)):
        _tp = round(_ninf * _sens**_tests)
        _fp = round(_nnot * (1 - _spec) ** _tests)
        _word = "positive" if _tests == 1 else "positive twice"
        population_grid(_ax, [(_tp, RED, f"infected, {_word}"), (_ninf - _tp, _ORANGE, f"infected, not {_word}"), (_fp, BLUE, f"not infected, {_word}"), (_nnot - _fp, GREY, f"not infected, not {_word}")], _per, _N)
        _ax.set_title(f"{_tests} test{'s' if _tests > 1 else ''}:  P(I) = {_prev:g},  sens {_sens:.2f},  spec {_spec:.3g}", fontsize=10, loc="left")
        _ax.text(0, _N + 1.5, f"{_word}: {_tp:,} + {_fp:,} = {_tp + _fp:,}      $P(I \\mid {'+' if _tests == 1 else '+,+'}) = {_tp / (_tp + _fp):.3f}$", fontsize=10, va="top")
    _tfig.suptitle(f"population {_pop:,}, one square = {_per:g} people", fontsize=10, color="grey")
    _lines = ["| results | $P(\\text{results} \\mid I)$ | $P(\\text{results} \\mid I^c)$ | from the counts | exact |", "|:--|--:|--:|--:|--:|"]
    for _res in ("+", "++", "+-", "+++"):
        _a = float(np.prod([_sens if c == "+" else 1 - _sens for c in _res]))
        _b = float(np.prod([1 - _spec if c == "+" else _spec for c in _res]))
        _tp_, _fp_ = round(_ninf * _a), round(_nnot * _b)
        _lines.append(rf"| ${_res}$ | ${_a:.4f}$ | ${_b:.6f}$ | ${_tp_ / (_tp_ + _fp_) if _tp_ + _fp_ else float('nan'):.4f}$ | ${_prev * _a / (_prev * _a + (1 - _prev) * _b):.4f}$ |")
    mo.accordion(
        {
            "Simulation [cell 3]": mo.vstack([mo.hstack([d_pop, d_prev, d_sens, d_spec], justify="start", gap=2, wrap=True), mo.md("\n".join(_lines)), _tfig]),
            "Solution": mo.md(
                r"""
    (a) $P(I \mid +) = \dfrac{0.01 \times 0.8}{0.01 \times 0.8 + 0.99 \times 0.05} = \dfrac{0.008}{0.008 + 0.0495} \approx 0.139$: 80 true and 495 false positives among 10 000.

    (b) (i) $400 / (400 + 475) \approx 0.457$; (ii) $84 / (84 + 495) \approx 0.145$; (iii) $80 / (80 + 99) \approx 0.447$. The sensitivity acts on the 100 infected, the specificity on the 9 900 healthy.

    (c) At sensitivity 1: $100 / (100 + 495) \approx 0.168$.

    (d) $\dfrac{0.01 \times 0.8^2}{0.01 \times 0.8^2 + 0.99 \times 0.05^2} = \dfrac{0.0064}{0.008875} \approx 0.721$.
    """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(box, mo):
    q2_boxes = tuple(box() for _ in range(10))
    q2_sentence = mo.ui.text_area(placeholder="your one-sentence explanation for (d)", rows=2, full_width=True)
    return q2_boxes, q2_sentence


@app.cell(hide_code=True)
def _(ask, binomial_pmf, hypergeometric_pmf, math, mo, neg_binomial_pmf, neg_hypergeometric_pmf, q2_boxes, q2_sentence):
    _ea, _va, _ya, _eb, _vb, _yb, _pxa, _pya, _pxb, _pyb = q2_boxes
    _PXA = 1 - sum(binomial_pmf(x, 10, 0.2) for x in range(2))
    _PYA = sum(neg_binomial_pmf(y, 2, 0.2) for y in range(2, 11))
    _PXB = 1 - sum(hypergeometric_pmf(x, 20, 4, 10) for x in range(2))
    _PYB = sum(neg_hypergeometric_pmf(y, 20, 4, 2) for y in range(2, 11))
    mo.vstack(
        [
            mo.md(
                r"""
    ## Question 2

    A playlist contains $N = 20$ songs, $K = 4$ by one artist. Player A selects each song independently at random from the whole playlist; songs can repeat. Player B plays the songs in a random order; each song only once. Let $X$ count the number of songs by the artist among the first 10 songs played, and $Y$ the number of songs played up to and including the second song by the artist. Answer for both players.

    (a) Calculate $E[X]$, $\mathrm{Var}(X)$ and $E[Y]$.
    """
            ),
            mo.hstack([ask(r"player A: $E[X] =$", _ea, 2.0, 0.005), ask(r"$\mathrm{Var}(X) =$", _va, 1.6, 0.005), ask(r"$E[Y] =$", _ya, 10.0, 0.005)], justify="start", gap=2, wrap=True),
            mo.hstack([ask(r"player B: $E[X] =$", _eb, 2.0, 0.005), ask(r"$\mathrm{Var}(X) =$", _vb, 1.6 * 10 / 19, 0.005), ask(r"$E[Y] =$", _yb, 8.4, 0.005)], justify="start", gap=2, wrap=True),
            mo.md(r"(b) Find $P(X \geq 2)$ and $P(Y \leq 10)$."),
            mo.hstack([ask(r"player A: $P(X \geq 2) =$", _pxa, _PXA, 0.002), ask(r"$P(Y \leq 10) =$", _pya, _PYA, 0.002)], justify="start", gap=2, wrap=True),
            mo.hstack([ask(r"player B: $P(X \geq 2) =$", _pxb, _PXB, 0.002), ask(r"$P(Y \leq 10) =$", _pyb, _PYB, 0.002)], justify="start", gap=2, wrap=True),
            mo.md(
                r"""
    (c) Identify the runs with $X \geq 2$ and those with $Y \leq 10$.

    (d) Compare $P(X = 0)$, $P(X \geq 4)$ and $P(Y > 15)$. Explain in one sentence.
    """
            ),
            q2_sentence,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    s_songs = mo.ui.slider(5, 100, 1, value=20, label="songs $N$", show_value=True)
    s_art = mo.ui.slider(1, 20, 1, value=4, label="by the artist $K$", show_value=True)
    s_played = mo.ui.slider(1, 50, 1, value=10, label="played $n$", show_value=True)
    s_target = mo.ui.slider(1, 10, 1, value=2, label="target $r$", show_value=True)
    s_runs = mo.ui.dropdown({"10": 10, "100": 100, "10 000": 10000}, value="10 000", label="runs shown in the histograms", allow_select_none=False)
    s_seed = mo.ui.number(value=2029, label="seed", step=1)
    return s_art, s_played, s_runs, s_seed, s_songs, s_target


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, RED, binomial_pmf, hypergeometric_pmf, mo, neg_binomial_pmf, neg_hypergeometric_pmf, np, s_art, s_played, s_runs, s_seed, s_songs, s_target):
    _N, _K, _n, _r = s_songs.value, s_art.value, s_played.value, s_target.value
    _m, _total = int(s_runs.value), 10000
    if _K > _N or _n > _N or _r > _K:
        _out = mo.accordion({"Simulation [cell 4]": mo.vstack([mo.hstack([s_songs, s_art, s_played, s_target, s_runs, s_seed], justify="start", gap=2, wrap=True), mo.md(rf"need $K \le N$, $n \le N$ and $r \le K$")])})
    else:
        _p = _K / _N
        _rng = np.random.default_rng(int(s_seed.value))
        # player B: a random order of the playlist; player A: independent draws with probability p
        _seqB = _rng.random((_total, _N)).argsort(axis=1) < _K
        _seqA = _rng.random((_total, 4 * _N)) < _p
        while np.any(_seqA.sum(axis=1) < _r):
            _seqA = np.concatenate((_seqA, _rng.random((_total, 2 * _N)) < _p), axis=1)

        def _measure(seq):
            X = seq[:, :_n].sum(axis=1)
            return X, (np.cumsum(seq, axis=1) >= _r).argmax(axis=1) + 1

        _XA, _YA = _measure(_seqA)
        _XB, _YB = _measure(_seqB)
        _col = {"A": (BLUE, "#8fa8e8"), "B": (RED, "#f0b4a0")}
        _STRIP, _ROWS = max(40, int(np.ceil(1.5 * _n / 10) * 10)), 12

        # --- strips: the first 12 runs of each player
        _sfig = Figure(figsize=(9.6, 2 * (0.3 * _ROWS + 0.8)), layout="constrained")
        for _ax, _name, _seq in zip(_sfig.subplots(2, 1, sharex=True), ("A", "B"), (_seqA, _seqB)):
            for _row in range(_ROWS):
                _s = _seq[_row][:_STRIP]
                _X = int(_seq[_row][:_n].sum())
                _Y = int(np.flatnonzero(_seq[_row])[_r - 1] + 1)
                _ax.scatter(np.arange(1, len(_s) + 1), np.full(len(_s), -_row), s=20, c=np.where(_s, GREEN, "#dddddd"), marker="s", linewidths=0)
                if _Y <= _STRIP:
                    _ax.plot(_Y, -_row, "o", mfc="none", mec=_col[_name][0], ms=8, mew=1.4)
                _ax.text(1.005, -_row, f"X = {_X:<3d} Y = {_Y}", transform=_ax.get_yaxis_transform(), va="center", fontsize=8)
            _ax.axvspan(0.5, min(_n, _STRIP) + 0.5, color="#fff2b0", zorder=0)
            _ax.set_ylabel(f"player {_name}")
            _ax.set_xlim(0.5, _STRIP + 0.5)
            _ax.set_ylim(-_ROWS + 0.4, 0.6)
            _ax.set_yticks(-np.arange(_ROWS), np.arange(1, _ROWS + 1))
            for _sp in ("top", "right"):
                _ax.spines[_sp].set_visible(False)
        _sfig.axes[1].set_xlabel(f"song (first {_STRIP} of each run)")
        _sfig.suptitle("green: a song by the artist;  yellow: the songs counted in X;  ring: the song counted by Y", fontsize=10)

        # --- histograms over many runs vs the exact pmfs
        _pmfs = {
            "A": (lambda x: binomial_pmf(x, _n, _p), lambda y: neg_binomial_pmf(y, _r, _p), f"B({_n}, {_p:g})", f"NB({_r}, {_p:g})"),
            "B": (lambda x: hypergeometric_pmf(x, _N, _K, _n), lambda y: neg_hypergeometric_pmf(y, _N, _K, _r), f"HG({_N}, {_K}, {_n})", f"NHG({_N}, {_K}, {_r})"),
        }
        _YMAX = int(np.ceil(np.quantile(np.concatenate([_YA, _YB]), 0.995) / 10) * 10)
        _hfig = Figure(figsize=(9.6, 3.2), layout="constrained")
        _hx, _hy = _hfig.subplots(1, 2)
        _xs = np.arange(0, _n + 1)
        _ys = np.arange(_r, _YMAX + 1)
        for _k, (_name, _X, _Y) in enumerate((("A", _XA, _YA), ("B", _XB, _YB))):
            _dark, _light = _col[_name]
            _hx.bar(_xs + (_k - 0.5) * 0.4, [(_X[:_m] == x).mean() for x in _xs], width=0.4, color=_light, label=f"player {_name}, {_m:,} runs")
            _hx.plot(_xs, [_pmfs[_name][0](int(x)) for x in _xs], "o", color=_dark, ms=4, label=_pmfs[_name][2])
            _hy.bar(_ys + (_k - 0.5) * 0.4, [(_Y[:_m] == y).mean() for y in _ys], width=0.4, color=_light, label=f"player {_name}, {_m:,} runs")
            _hy.plot(_ys, [_pmfs[_name][1](int(y)) for y in _ys], "o", color=_dark, ms=4, label=_pmfs[_name][3])
        _hx.set_xlabel("$X$")
        _hy.set_xlabel("$Y$")
        _hx.set_ylabel("fraction of runs")
        for _ax in (_hx, _hy):
            _ax.legend(fontsize=8, frameon=False)
            for _sp in ("top", "right"):
                _ax.spines[_sp].set_visible(False)

        # --- table: simulated vs exact
        _exact = {"A": (_n * _p, _n * _p * (1 - _p), _r / _p), "B": (_n * _p, _n * _p * (1 - _p) * (_N - _n) / (_N - 1), _r * (_N + 1) / (_K + 1))}
        _lo_x = max(0, int(np.floor(_n * _p - 1.5 * np.sqrt(_n * _p * (1 - _p)))))
        _hi_x = int(np.ceil(_n * _p + 1.5 * np.sqrt(_n * _p * (1 - _p))))
        _tail_y = int(round((_r / _p + np.sqrt(_r * (1 - _p)) / _p) / 5) * 5)
        _heads = [("X = 0" if _lo_x == 0 else f"X ≤ {_lo_x}"), f"X ≥ {_hi_x}", f"X ≥ {_r}", f"Y ≤ {_n}", f"Y > {_tail_y}"]
        _lines = ["| first " + f"{_m:,}" + " runs | mean X | var X | mean Y | " + " | ".join(_heads) + " |", "|:--|--:|--:|--:|" + "--:|" * len(_heads)]
        for _name, _X, _Y in (("A", _XA, _YA), ("B", _XB, _YB)):
            _EX, _VX, _EY = _exact[_name]
            _Xm, _Ym = _X[:_m], _Y[:_m]
            _fx, _fy = _pmfs[_name][0], _pmfs[_name][1]
            _sim = [(_Xm <= _lo_x).mean(), (_Xm >= _hi_x).mean(), (_Xm >= _r).mean(), (_Ym <= _n).mean(), (_Ym > _tail_y).mean()]
            _exa = [sum(_fx(x) for x in range(0, _lo_x + 1)), sum(_fx(x) for x in range(_hi_x, _n + 1)), sum(_fx(x) for x in range(_r, _n + 1)), sum(_fy(y) for y in range(_r, _n + 1)), 1 - sum(_fy(y) for y in range(_r, _tail_y + 1))]
            _lines.append(f"| player {_name}, simulated | {_Xm.mean():.3f} | {_Xm.var():.3f} | {_Ym.mean():.3f} | " + " | ".join(f"{v:.4f}" for v in _sim) + " |")
            _lines.append(f"| player {_name}, exact | {_EX:.3f} | {_VX:.3f} | {_EY:.3f} | " + " | ".join(f"{v:.4f}" for v in _exa) + " |")
        _table = "\n".join(_lines)

        # --- player B, run 1: probability that the next song is by the artist
        _seq = _seqB[0][:_n]
        _before = np.r_[0, np.cumsum(_seq)[:-1]]
        _next = (_K - _before) / (_N - np.arange(_n))
        _nxt = "\n".join(
            [
                "| song | " + " | ".join(str(j) for j in range(1, _n + 1)) + " |",
                "|:--|" + "--:|" * _n,
                "| artist? | " + " | ".join("A" if s else "·" for s in _seq) + " |",
                "| player B, $P$(next is by the artist) | " + " | ".join(f"{q:.3f}" for q in _next) + " |",
                "| player A | " + " | ".join(f"{_p:.3f}" for _ in range(_n)) + " |",
            ]
        )

        _out = mo.accordion(
            {
                "Simulation [cell 4]": mo.vstack(
                    [
                        mo.hstack([s_songs, s_art, s_played, s_target, s_runs, s_seed], justify="start", gap=2, wrap=True),
                        _sfig,
                        _hfig,
                        mo.md(_table),
                        mo.md(_nxt),
                    ]
                ),
            }
        )
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"(e) Compare the distributions of $X$ for $N = 40$, $200$, $2000$, with $K/N = 0.2$.")
    return


@app.cell(hide_code=True)
def _(mo):
    z_sizes = mo.ui.text(value="20, 40, 200, 2000", label="playlist sizes $N$", full_width=False)
    z_played = mo.ui.slider(1, 50, 1, value=10, label="played $n$", show_value=True)
    z_frac = mo.ui.slider(0.05, 0.95, 0.05, value=0.2, label="fraction by the artist $K/N$", show_value=True)
    z_seed = mo.ui.number(value=2029, label="seed", step=1)
    return z_frac, z_played, z_seed, z_sizes


@app.cell(hide_code=True)
def _(BLUE, Figure, RED, binomial_pmf, hypergeometric_pmf, mo, np, z_frac, z_played, z_seed, z_sizes):
    _sizes = [int(v) for v in z_sizes.value.replace(";", ",").split(",") if v.strip().isdigit()]
    _n, _p, _reps = z_played.value, z_frac.value, 10000
    _sizes = [N for N in _sizes if N >= _n and round(N * _p) >= 1]
    if not _sizes:
        _out = mo.accordion({"Simulation [cell 5]": mo.vstack([mo.hstack([z_sizes, z_played, z_frac, z_seed], justify="start", gap=2, wrap=True), mo.md("enter playlist sizes $N \\ge n$, separated by commas")])})
    else:
        _rng = np.random.default_rng(int(z_seed.value))
        _counts = {N: (_rng.binomial(_n, _p, size=_reps), _rng.hypergeometric(round(N * _p), N - round(N * _p), _n, size=_reps)) for N in _sizes}
        _fig = Figure(figsize=(2.4 * len(_sizes), 3.0), layout="constrained")
        _axes = np.atleast_1d(_fig.subplots(1, len(_sizes), sharey=True))
        _xs = np.arange(0, _n + 1)
        _rows = ["| songs $N$ | var X, player A | exact $B$ | var X, player B | exact $HG$ |", "|--:|--:|--:|--:|--:|"]
        for _ax, _Nn in zip(_axes, _sizes):
            _Kk = round(_Nn * _p)
            for _k, (_name, _vals, _pmf, _dark, _light) in enumerate(
                (("A", _counts[_Nn][0], lambda x: binomial_pmf(x, _n, _p), BLUE, "#8fa8e8"), ("B", _counts[_Nn][1], lambda x, N=_Nn, K=_Kk: hypergeometric_pmf(x, N, K, _n), RED, "#f0b4a0"))
            ):
                _ax.bar(_xs + (_k - 0.5) * 0.4, [(_vals == x).mean() for x in _xs], width=0.4, color=_light, label=f"player {_name}")
                _ax.plot(_xs, [_pmf(int(x)) for x in _xs], "o", color=_dark, ms=3.5)
            _ax.set_title(f"{_Nn:,} songs", fontsize=10)
            _ax.set_xlabel("$X$")
            _ax.legend(fontsize=7, frameon=False)
            for _sp in ("top", "right"):
                _ax.spines[_sp].set_visible(False)
            _rows.append(f"| {_Nn:,} | {_counts[_Nn][0].var():.3f} | {_n * _p * (1 - _p):.3f} | {_counts[_Nn][1].var():.3f} | {_n * _p * (1 - _p) * (_Nn - _n) / (_Nn - 1):.3f} |")
        _axes[0].set_ylabel("fraction of runs")
        _out = mo.accordion(
            {
                "Simulation [cell 5]": mo.vstack(
                    [
                        mo.hstack([z_sizes, z_played, z_frac, z_seed], justify="start", gap=2, wrap=True),
                        _fig,
                        mo.md("\n".join(_rows)),
                    ]
                ),
                "Solution": mo.md(
                r"""
    (a) Player A: $X \sim B(10, 0.2)$, $E[X] = 2$, $\mathrm{Var}(X) = 1.6$; $Y \sim NB(2, 0.2)$, $E[Y] = 10$. Player B: $X \sim HG(20, 4, 10)$, $E[X] = 2$, $\mathrm{Var}(X) = 1.6 \cdot 10/19 \approx 0.842$; $Y \sim NHG(20, 4, 2)$, $E[Y] = 2 \cdot 21/5 = 8.4$.

    (b) Player A: $P(X \geq 2) = 1 - 0.8^{10} - 10 (0.2) 0.8^9 \approx 0.624$ and $P(Y \leq 10) = \sum_{y=2}^{10} (y - 1)(0.2)^2 (0.8)^{y-2} \approx 0.624$. Player B: $P(X \geq 2) = 1 - \big[\binom{16}{10} + 4 \binom{16}{9}\big] / \binom{20}{10} \approx 0.709$ and $P(Y \leq 10) \approx 0.709$. The same event: the second song by the artist plays by song 10 exactly when at least two of the first ten are by the artist.

    (c) The same runs, for the same reason.

    (d) Player A in all three: $P(X = 0)$ is $0.107$ against $0.043$, $P(X \geq 4)$ is $0.121$ against $0.043$, and $P(Y > 15) = 0.8^{15} + 15 (0.2) 0.8^{14} \approx 0.167$ against $\big[\binom{16}{15} + 4 \binom{16}{14}\big] / \binom{20}{15} \approx 0.032$ — at most one song by the artist among the first 15: one run in six against one in thirty. Under player B each song by the artist lowers the chance of the next one ($4/20 \to 3/19$) and each other song raises it ($4/20 \to 4/19$); under player A it is $0.2$ always.

    (e) $\mathrm{Var}(X)$ under player B: $0.842$, $1.231$, $1.528$, $1.593$, against $1.6$. By 2 000 songs, selecting ten songs hardly changes the artist's share of the remaining playlist, so the two distributions become nearly equal.
    """
                ),
            }
        )
    _out
    return


@app.cell(hide_code=True)
def _(box, mo):
    q3_boxes = tuple(box() for _ in range(6))
    q3_sentence = mo.ui.text_area(placeholder="your answer to (b): the two events in terms of R(t) and T(60)", rows=2, full_width=True)
    return q3_boxes, q3_sentence


@app.cell(hide_code=True)
def _(ask, math, mo, q3_boxes, q3_sentence, seat_open_probability):
    _r0, _et1, _et60, _p20, _p30, _p40 = q3_boxes
    mo.vstack(
        [
            mo.md(
                r"""
    ## Question 3

    A course has 60 seats. After registration opens, requests arrive following a Poisson model at rate 2 per second. Let $R(t)$ be the number of requests in the first $t$ seconds and $T(r)$ be the time of the $r$-th request. The course fills at $T(60)$.

    (a) Find $P(R(1) = 0)$, $E[T(1)]$ and $E[T(60)]$.
    """
            ),
            mo.hstack([ask(r"$P(R(1) = 0) =$", _r0, math.exp(-2), 0.002), ask(r"$E[T(1)] =$", _et1, 0.5, 0.005), ask(r"$E[T(60)] =$", _et60, 30.0, 0.005)], justify="start", gap=2, wrap=True),
            mo.md(r"(b) Express “a seat is still open at time $t$” using $R(t)$, and using $T(60)$."),
            q3_sentence,
            mo.md(r"(c) Find the mean and standard deviation of $T(60)$ from 10 000 simulated openings. Compare with (a)."),
            mo.md(r"(d) Find the probability that a seat is still open at 20, 30 and 40 seconds."),
            mo.hstack(
                [ask(r"$t = 20$:", _p20, seat_open_probability(20, 60, 2), 0.005), ask(r"$t = 30$:", _p30, seat_open_probability(30, 60, 2), 0.005), ask(r"$t = 40$:", _p40, seat_open_probability(40, 60, 2), 0.005)],
                justify="start",
                gap=2,
                wrap=True,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    a_rate = mo.ui.slider(0.2, 10, 0.1, value=2.0, label="rate (per second)", show_value=True)
    a_seats = mo.ui.slider(1, 200, 1, value=60, label="seats", show_value=True)
    a_cut = mo.ui.slider(1, 120, 1, value=30, label="time cutoff $t$ (s)", show_value=True)
    a_seed = mo.ui.number(value=2029, label="seed", step=1)
    return a_cut, a_rate, a_seats, a_seed


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, a_cut, a_rate, a_seats, a_seed, mo, np, seat_open_probability):
    _rate, _seats, _tcut = a_rate.value, a_seats.value, float(a_cut.value)
    _runs = 10000
    _span = max(_tcut, 1.5 * _seats / _rate)
    _rng = np.random.default_rng(int(a_seed.value))
    # millisecond slots, a request with probability rate/1000 in each: the gaps are geometric (≈ exponential)
    _slots = 1000
    _cols = max(_seats, int(_rate * _span + 4 * np.sqrt(_rate * _span) + 20))
    _arr = _rng.geometric(_rate / _slots, size=(_runs, _cols)).cumsum(axis=1)
    while np.any(_arr[:, -1] <= _span * _slots):
        _arr = np.concatenate((_arr, _arr[:, -1, None] + _rng.geometric(_rate / _slots, size=(_runs, 32)).cumsum(axis=1)), axis=1)
    _T = _arr[:, _seats - 1] / _slots
    _TMAX = float(np.ceil(max(_tcut * 1.1, np.quantile(_T, 0.999)) / 5) * 5)
    _Rcut = (_arr <= round(_tcut * _slots)).sum(axis=1)
    _open = _Rcut < _seats

    # --- timelines of 15 openings
    _tfig = Figure(figsize=(9.6, 4.2), layout="constrained")
    _ax = _tfig.subplots()
    for _row in range(15):
        _c = BLUE if _open[_row] else GREY
        _vis = _arr[_row] / _slots
        _vis = _vis[_vis <= _TMAX]
        _ax.hlines(-_row, 0, _TMAX, color=_c, alpha=0.3, lw=1)
        _ax.scatter(_vis, np.full(len(_vis), -_row), color=_c, s=6)
        if _T[_row] <= _TMAX:
            _ax.plot(_T[_row], -_row, "*", color=RED, ms=10)
        _ax.text(1.01, -_row, f"R(t) = {_Rcut[_row]}", transform=_ax.get_yaxis_transform(), va="center", fontsize=8, color=_c)
    _ax.axvline(_tcut, color="black", ls="--", lw=1)
    _ax.text(_tcut, 1.2, f"t = {_tcut:g}", ha="center", fontsize=9)
    _ax.set_yticks(-np.arange(15), np.arange(1, 16))
    _ax.set_xlabel("seconds after opening")
    _ax.set_ylabel("opening")
    _ax.set_xlim(0, _TMAX)
    _ax.set_ylim(-14.7, 2)
    _ax.set_title(f"rate {_rate:g} per second, {_seats} seats;  dots: requests;  star: request {_seats}", fontsize=10, loc="left")
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)

    # --- histogram of T(seats) and the open-seat curve
    _hfig = Figure(figsize=(9.6, 3.2), layout="constrained")
    _h, _o = _hfig.subplots(1, 2)
    _bins = np.linspace(0, _TMAX, 61)
    _h.hist(_T[_T <= _TMAX], bins=_bins, weights=np.full((_T <= _TMAX).sum(), 1 / len(_T)), color="#c5cfe6")
    _h.axvline(_T.mean(), color=RED, lw=1.2, label=f"mean {_T.mean():.2f} s")
    _h.set_xlabel(f"$T({_seats})$, seconds until the course is full")
    _h.set_ylabel("fraction of openings")
    _h.set_xlim(0, _TMAX)
    _h.legend(fontsize=8, frameon=False)
    _grid = np.linspace(0, _TMAX, 300)
    _o.plot(_grid, [(_T > t).mean() for t in _grid], color="#c5cfe6", lw=4, label=f"fraction of openings with $T({_seats}) > t$")
    _o.plot(_grid, [seat_open_probability(t, _seats, _rate) for t in _grid], color=BLUE, lw=1.3, label=f"$P(R(t) < {_seats})$")
    _o.axvline(_tcut, color="black", ls="--", lw=1)
    _o.set_xlabel("$t$, seconds after opening")
    _o.set_ylabel("probability a seat is still open")
    _o.set_xlim(0, _TMAX)
    _o.set_ylim(0, 1.02)
    _o.legend(fontsize=8, frameon=False)
    for _ax in (_h, _o):
        for _sp in ("top", "right"):
            _ax.spines[_sp].set_visible(False)

    _rows = [
        f"| {_runs:,} simulated openings, rate {_rate:g} per second, {_seats} seats | simulated | exact |",
        "|:--|--:|--:|",
        f"| mean of $T({_seats})$ | {_T.mean():.3f} | {_seats / _rate:.3f} |",
        f"| standard deviation of $T({_seats})$ | {_T.std():.3f} | {np.sqrt(_seats) / _rate:.3f} |",
    ] + [f"| seat open at $t = {t:g}$ | {(_T > t).mean():.4f} | {seat_open_probability(t, _seats, _rate):.4f} |" for t in sorted({_tcut, 20.0, 30.0, 40.0})]

    mo.accordion(
        {
            "Simulation [cell 6]": mo.vstack(
                [
                    mo.hstack([a_rate, a_seats, a_cut, a_seed], justify="start", gap=2, wrap=True),
                    _tfig,
                    _hfig,
                    mo.md("\n".join(_rows)),
                ]
            ),
            "Solution": mo.md(
                r"""
    (a) $R(1) \sim \mathrm{Pois}(2)$: $P(R(1) = 0) = e^{-2} \approx 0.135$. One request per half second on average: $E[T(1)] = 1/2$ s and $E[T(60)] = 60/2 = 30$ s.

    (b) $\{R(t) < 60\} = \{T(60) > t\}$: fewer than 60 requests by time $t$ exactly when the 60th request comes after $t$.

    (c) Simulated mean $30.0$ s; standard deviation $3.8$ s ($T(60) \sim \mathrm{Gamma}(60, 2)$, variance $60/4$).

    (d) $P(R(t) < 60)$ with $R(t) \sim \mathrm{Pois}(2t)$: $0.998$ at $t = 20$, $0.483$ at $t = 30$, $0.009$ at $t = 40$.
    """
            ),
        }
    )
    return


if __name__ == "__main__":
    app.run()

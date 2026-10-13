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
    header("Guided Practice 1", "Week 05", "Guided Practice 1")
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
        return mo.hstack([mo.md(label).style({"white-space": "nowrap"}), field, mo.md(mark).style({"white-space": "nowrap"})], justify="start", align="center").style({"flex": "0 0 auto"})

    def box():
        return mo.ui.text(placeholder="?", debounce=True)

    return ask, box


@app.cell(hide_code=True)
def _(math, np):
    from matplotlib.ticker import MaxNLocator

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
        from matplotlib.patches import Rectangle

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
        # each group is labelled next to the grid: a square of its colour, its count, its name
        for i, (n, colour, label) in enumerate(groups):
            y = 3 + 7.5 * i
            ax.add_patch(Rectangle((N + 2, y - 1.1), 2.2, 2.2, facecolor=colour, edgecolor="black", lw=0.5))
            ax.text(N + 5.5, y, f"{n:,}", fontsize=12, va="center")
            ax.text(N + 5.5, y + 3.2, label, fontsize=12, va="center")
        ax.set_xlim(0, N + 36)
        ax.set_ylim(N + 5, -0.5)
        ax.set_aspect("equal")

    return MaxNLocator, binomial_pmf, hypergeometric_pmf, neg_binomial_pmf, neg_hypergeometric_pmf, population_grid, posterior, seat_open_probability


@app.cell(hide_code=True)
def _(box, mo):
    q1_boxes = mo.ui.array([box() for _ in range(6)])
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
def _(BLUE, FULL, Figure, LIGHT, ORANGE, RED, mo, population_grid, posterior, t_pop, t_prev, t_sens, t_spec, t_step):
    _pop, _step = t_pop.value, t_step.value
    _N = 50
    _per = _pop / _N**2
    _base = dict(prevalence=t_prev.value, sensitivity=t_sens.value, specificity=t_spec.value)
    _fig = Figure(figsize=(FULL, 4 * 4.85), layout="constrained")
    _cols = []
    for _ax, _changed in zip(_fig.subplots(4, 1), [None, "prevalence", "sensitivity", "specificity"]):
        _s = dict(_base)
        _capped = False
        if _changed:
            _capped = _s[_changed] + _step > 1
            _s[_changed] = min(1, _s[_changed] + _step)
        # whole people, as in cell 3: the infected are split into positive and negative
        _ninf = round(_s["prevalence"] * _pop)
        _tp = round(_ninf * _s["sensitivity"])
        _fn = _ninf - _tp
        _fp = round((_pop - _ninf) * (1 - _s["specificity"]))
        _tn = _pop - _tp - _fn - _fp
        population_grid(_ax, [(_tp, BLUE, "infected, positive"), (_fn, ORANGE, "infected, negative"), (_fp, RED, "not infected, positive"), (_tn, LIGHT, "not infected, negative")], _per, _N)
        _ratio = f"{_tp / (_tp + _fp):.3f}" if _tp + _fp else None
        _ax.set_title("base scenario" if not _changed else f"{_changed} + step", fontsize=13, loc="left")
        _ax.text(0, _N + 1.5, f"positive: {_tp:,} infected + {_fp:,} not infected = {_tp + _fp:,}" + (f",   $P(I \\mid +) = {_ratio}$" if _ratio else ""), fontsize=12, va="top")
        _cols.append((_s, _changed if _capped else None, _tp, _fp, _ratio))

    def _num(text):
        return "$" + text.replace(",", r"\,") + "$"

    def _input(col, name, digits):
        return _num(f"{col[0][name]:.{digits}f}") + (" (maximum)" if col[1] == name else "")

    _lines = ["| | base scenario | prevalence + step | sensitivity + step | specificity + step |", "|:--|--:|--:|--:|--:|"]
    for _label, _cell in [
        ("prevalence $P(I)$", lambda c: _input(c, "prevalence", 3)),
        ("sensitivity $P(+ \\mid I)$", lambda c: _input(c, "sensitivity", 2)),
        ("specificity $P(- \\mid I^c)$", lambda c: _input(c, "specificity", 3)),
        ("infected, positive", lambda c: rf"$\textcolor{{{BLUE}}}{{" + f"{c[2]:,}".replace(",", r"\,") + "}$"),
        ("not infected, positive", lambda c: rf"$\textcolor{{{RED}}}{{" + f"{c[3]:,}".replace(",", r"\,") + "}$"),
        ("$P(I \\mid +)$ from the counts", lambda c: _num(c[4]) if c[4] else "need a positive test"),
        ("$P(I \\mid +)$ exact", lambda c: _num(f"{posterior(**c[0]):.4f}") if c[0]["sensitivity"] > 0 or c[0]["specificity"] < 1 else "need a positive test"),
    ]:
        _lines.append(f"| {_label} | " + " | ".join(_cell(c) for c in _cols) + " |")
    mo.accordion(
        {
            "Simulation [cell 1]": mo.vstack(
                [
                    mo.hstack([t_pop, t_prev, t_sens, t_spec, t_step], justify="start", gap=2, wrap=True),
                    mo.md("Population $" + f"{_pop:,}".replace(",", r"\,") + f"$, one square = ${_per:g}$ people."),
                    mo.md("\n".join(_lines)),
                    _fig,
                ]
            )
        }
    )
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
def _(BLUE, FULL, Figure, RED, c_prev, c_sens, c_spec, c_step, mo, np, posterior, table):
    _base = dict(prevalence=c_prev.value, sensitivity=c_sens.value, specificity=c_spec.value)
    _step = c_step.value

    def _post(**kw):
        _s = {**_base, **kw}
        return posterior(**_s) if _s["sensitivity"] > 0 or _s["specificity"] < 1 else float("nan")

    _cfig = Figure(figsize=(FULL, 2.7), layout="constrained")
    _cfig.get_layout_engine().set(wspace=0.08)
    _grids = [("prevalence", np.logspace(-3, np.log10(0.7), 300)), ("sensitivity", np.linspace(0.5, 1, 300)), ("specificity", np.linspace(0.80, 1, 300))]
    _rows = [("base scenario (black point)", f"$P(I \\mid +) = {_post():.4f}$")]
    for _ax, (_name, _grid) in zip(_cfig.subplots(1, 3, sharey=True), _grids):
        _ax.plot(_grid, [_post(**{_name: v}) for v in _grid], color=BLUE, lw=1.4)
        _v = min(1, _base[_name] + _step)
        _ax.plot([_v], [_post(**{_name: _v})], "o", color=RED, ms=5, zorder=4)
        _ax.plot([_base[_name]], [_post()], "o", color="black", ms=5, zorder=5)
        _ax.set_xlabel(_name, fontsize=13)
        _ax.set_ylim(0, 1.02)
        _ax.tick_params(labelsize=11)
        if _name == "prevalence":
            _ax.set_xscale("log")
            _ax.set_ylabel(r"$P(I \mid +)$", fontsize=13)
        for _sp in ("top", "right"):
            _ax.spines[_sp].set_visible(False)
        _rows.append((f"{_name} + step: {_name} ${_v:.3f}$" + (" (maximum)" if _base[_name] + _step > 1 else "") + " (red point)", rf"$\textcolor{{{RED}}}{{P(I \mid +) = {_post(**{_name: _v}):.4f}}}$"))
    mo.accordion({"Simulation [cell 2]": mo.vstack([mo.hstack([c_prev, c_sens, c_spec, c_step], justify="start", gap=2, wrap=True), table(_rows), _cfig])})
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
def _(BLUE, FULL, Figure, LIGHT, ORANGE, RED, d_pop, d_prev, d_sens, d_spec, mo, np, population_grid):
    _pop = d_pop.value
    _N = 50
    _per = _pop / _N**2
    _prev, _sens, _spec = d_prev.value, d_sens.value, d_spec.value
    _ninf = round(_prev * _pop)
    _nnot = _pop - _ninf
    _tfig = Figure(figsize=(FULL, 2 * 4.85), layout="constrained")
    for _ax, _tests in zip(_tfig.subplots(2, 1), (1, 2)):
        _tp = round(_ninf * _sens**_tests)
        _fp = round(_nnot * (1 - _spec) ** _tests)
        _word = "positive" if _tests == 1 else "positive twice"
        population_grid(_ax, [(_tp, BLUE, f"infected, {_word}"), (_ninf - _tp, ORANGE, f"infected, not {_word}"), (_fp, RED, f"not infected, {_word}"), (_nnot - _fp, LIGHT, f"not infected, not {_word}")], _per, _N)
        _ax.set_title("1 test" if _tests == 1 else "2 tests", fontsize=13, loc="left")
        _ax.text(0, _N + 1.5, f"{_word}: {_tp:,} infected + {_fp:,} not infected = {_tp + _fp:,}" + (f",   $P(I \\mid {'+' if _tests == 1 else '+,+'}) = {_tp / (_tp + _fp):.3f}$" if _tp + _fp else ""), fontsize=12, va="top")
    _lines = ["| results | $P(\\text{results} \\mid I)$ | $P(\\text{results} \\mid I^c)$ | $P(I \\mid \\text{results})$ from the counts | exact |", "|:--|--:|--:|--:|--:|"]
    for _res in ("+", "++", "+-", "+++"):
        _a = float(np.prod([_sens if c == "+" else 1 - _sens for c in _res]))
        _b = float(np.prod([1 - _spec if c == "+" else _spec for c in _res]))
        _tp_, _fp_ = round(_ninf * _a), round(_nnot * _b)
        _counts = f"${_tp_ / (_tp_ + _fp_):.4f}$" if _tp_ + _fp_ else "need a person with these results"
        _exact = f"${_prev * _a / (_prev * _a + (1 - _prev) * _b):.4f}$" if _a + _b > 0 else "need possible results"
        _lines.append(rf"| ${', '.join(_res)}$ | ${_a:.4f}$ | ${_b:.6f}$ | {_counts} | {_exact} |")
    mo.accordion(
        {
            "Simulation [cell 3]": mo.vstack(
                [
                    mo.hstack([d_pop, d_prev, d_sens, d_spec], justify="start", gap=2, wrap=True),
                    mo.md("Population $" + f"{_pop:,}".replace(",", r"\,") + "$ ($" + f"{_ninf:,}".replace(",", r"\,") + f"$ infected), one square = ${_per:g}$ people."),
                    mo.md("\n".join(_lines)),
                    _tfig,
                ]
            ),
            "Solution": mo.md(
                r"""
    (a) $P(I \mid +) = \dfrac{0.01 \times 0.8}{0.01 \times 0.8 + 0.99 \times 0.05} = \dfrac{0.008}{0.008 + 0.0495} \approx 0.139$: 80 true and 495 false positives among $10\,000$.

    (b) (i) $400 / (400 + 475) \approx 0.457$; (ii) $84 / (84 + 495) \approx 0.145$; (iii) $80 / (80 + 99) \approx 0.447$. The sensitivity acts on the 100 infected, the specificity on the $9\,900$ healthy.

    (c) At sensitivity 1: $100 / (100 + 495) \approx 0.168$.

    (d) $\dfrac{0.01 \times 0.8^2}{0.01 \times 0.8^2 + 0.99 \times 0.05^2} = \dfrac{0.0064}{0.008875} \approx 0.721$.
    """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(box, mo):
    q2_boxes = mo.ui.array([box() for _ in range(10)])
    q2_sentence = mo.ui.text_area(placeholder="your one-sentence explanation for (d)", rows=2, full_width=True)
    return q2_boxes, q2_sentence


@app.cell(hide_code=True)
def _(ask, binomial_pmf, hypergeometric_pmf, mo, neg_binomial_pmf, neg_hypergeometric_pmf, q2_boxes, q2_sentence):
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
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, MaxNLocator, RED, binomial_pmf, hypergeometric_pmf, mo, neg_binomial_pmf, neg_hypergeometric_pmf, np, s_art, s_played, s_runs, s_seed, s_songs, s_target, table):
    _N, _K, _n, _r = s_songs.value, s_art.value, s_played.value, s_target.value
    _m, _total = int(s_runs.value), 10000
    _controls = mo.hstack([s_songs, s_art, s_played, s_target, s_runs, s_seed], justify="start", gap=2, wrap=True)
    if _K > _N or _n > _N or _r > _K:
        _out = mo.accordion({"Simulation [cell 4]": mo.vstack([_controls, table([("simulation", r"need $K \le N$, $n \le N$ and $r \le K$")])])})
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
        _col = {"A": BLUE, "B": RED}
        _STRIP, _ROWS = max(40, int(np.ceil(1.5 * _n / 10) * 10)), 12

        # --- strips: the first 12 runs of each player
        _sfig = Figure(figsize=(FULL, 2 * (0.25 * _ROWS + 0.75)), layout="constrained")
        for _ax, _name, _seq in zip(_sfig.subplots(2, 1, sharex=True), ("A", "B"), (_seqA, _seqB)):
            for _row in range(_ROWS):
                _s = _seq[_row][:_STRIP]
                _X = int(_seq[_row][:_n].sum())
                _Y = int(np.flatnonzero(_seq[_row])[_r - 1] + 1)
                _pos = np.arange(1, len(_s) + 1)
                _ax.scatter(_pos[~_s], np.full((~_s).sum(), -_row), s=16, marker="s", facecolors="white", edgecolors=GREY, linewidths=0.5, zorder=2)
                _ax.scatter(_pos[_s], np.full(_s.sum(), -_row), s=16, marker="s", color=_col[_name], linewidths=0.5, zorder=2)
                if _Y <= _STRIP:
                    _ax.plot(_Y, -_row, "o", mfc="none", mec=GREEN, ms=8.5, mew=1.4, zorder=3)
                _ax.text(1.012, -_row, f"$X = {_X}$", transform=_ax.get_yaxis_transform(), va="center", fontsize=11)
                _ax.text(1.115, -_row, f"$Y = {_Y}$", transform=_ax.get_yaxis_transform(), va="center", fontsize=11)
            _ax.axvspan(0.5, min(_n, _STRIP) + 0.5, color=LIGHT, lw=0, zorder=0)
            _ax.set_ylabel(f"player {_name}", fontsize=13)
            _ax.set_xlim(0.5, _STRIP + 0.5)
            _ax.set_ylim(-_ROWS + 0.4, 0.6)
            _ax.set_yticks(-np.arange(_ROWS), np.arange(1, _ROWS + 1))
            _ax.tick_params(labelsize=10)
            for _sp in ("top", "right"):
                _ax.spines[_sp].set_visible(False)
        _sfig.axes[1].set_xlabel(f"song (first {_STRIP} of each run)", fontsize=13)

        # --- histograms over many runs vs the exact pmfs
        _pmfs = {
            "A": (lambda x: binomial_pmf(x, _n, _p), lambda y: neg_binomial_pmf(y, _r, _p), rf"\mathrm{{B}}({_n}, {_p:.3g})", rf"\mathrm{{NB}}({_r}, {_p:.3g})"),
            "B": (lambda x: hypergeometric_pmf(x, _N, _K, _n), lambda y: neg_hypergeometric_pmf(y, _N, _K, _r), rf"\mathrm{{HG}}({_N}, {_K}, {_n})", rf"\mathrm{{NHG}}({_N}, {_K}, {_r})"),
        }
        # the frame of the Y histogram follows the simulated data: every run is drawn
        _YMAX = int(max(_YA.max(), _YB.max()))
        _hfig = Figure(figsize=(FULL, 5.0), layout="constrained")
        _hx, _hy = _hfig.subplots(2, 1)
        _xs = np.arange(0, _n + 1)
        _ys = np.arange(_r, _YMAX + 1)
        _wide = len(_ys) > 120
        for _k, (_name, _X, _Y) in enumerate((("A", _XA, _YA), ("B", _XB, _YB))):
            _off = (_k - 0.5) * 0.4
            _hx.bar(_xs + _off, np.bincount(_X[:_m], minlength=_n + 1) / _m, width=0.4, color=LIGHT, edgecolor=_col[_name], lw=0.8)
            _freq = np.bincount(_Y[:_m], minlength=_YMAX + 1)[_r:] / _m
            if _wide:
                # too many values of Y for separate bars: the outline of the histogram, the pmf as dots
                _hy.stairs(_freq, np.arange(_r - 0.5, _YMAX + 1), color=_col[_name], lw=0.7)
            else:
                _hy.bar(_ys + _off, _freq, width=0.4, color=LIGHT, edgecolor=_col[_name], lw=0.8)
            for _ax, _grid, _f in ((_hx, _xs, _pmfs[_name][0]), (_hy, _ys, _pmfs[_name][1])):
                _vals = [_f(int(v)) for v in _grid]
                if _ax is _hy and _wide:
                    _ax.plot(_grid, _vals, "o", color=_col[_name], ms=1.5)
                else:
                    _ax.vlines(_grid + _off, 0, _vals, color=_col[_name], lw=0.9)
                    _ax.plot(_grid + _off, _vals, "o", color=_col[_name], ms=3.5 if len(_grid) < 40 else 2.5)
            _hx.text(0.84 + 0.16 * _k, 1.03, f"player {_name}", color=_col[_name], fontsize=12, ha="right", va="bottom", transform=_hx.transAxes)
        _hx.set_xlabel("$X$", fontsize=13)
        _hy.set_xlabel("$Y$", fontsize=13)
        _hx.set_xlim(-0.6, _n + 0.6)
        _hy.set_xlim(_r - 0.6, max(_YMAX, _r + 4) + 0.6)
        for _ax in (_hx, _hy):
            _ax.set_ylabel("fraction of runs", fontsize=13)
            _ax.tick_params(labelsize=11)
            _ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            for _sp in ("top", "right"):
                _ax.spines[_sp].set_visible(False)

        # --- table: simulated vs exact
        _exact = {"A": (_n * _p, _n * _p * (1 - _p), _r / _p), "B": (_n * _p, _n * _p * (1 - _p) * (_N - _n) / (_N - 1), _r * (_N + 1) / (_K + 1))}
        _lo_x = max(0, int(np.floor(_n * _p - 1.5 * np.sqrt(_n * _p * (1 - _p)))))
        _hi_x = int(np.ceil(_n * _p + 1.5 * np.sqrt(_n * _p * (1 - _p))))
        _tail_y = int(round((_r / _p + np.sqrt(_r * (1 - _p)) / _p) / 5) * 5)
        _labels = ["distribution of $X$", "distribution of $Y$", "mean of $X$", "variance of $X$", "mean of $Y$", "$P(X = 0)$" if _lo_x == 0 else rf"$P(X \leq {_lo_x})$", rf"$P(X \geq {_hi_x})$", rf"$P(X \geq {_r})$", rf"$P(Y \leq {_n})$", rf"$P(Y > {_tail_y})$"]
        _columns = []
        for _name, _X, _Y in (("A", _XA, _YA), ("B", _XB, _YB)):
            _EX, _VX, _EY = _exact[_name]
            _Xm, _Ym = _X[:_m], _Y[:_m]
            _fx, _fy = _pmfs[_name][0], _pmfs[_name][1]
            _sim = [(_Xm <= _lo_x).mean(), (_Xm >= _hi_x).mean(), (_Xm >= _r).mean(), (_Ym <= _n).mean(), (_Ym > _tail_y).mean()]
            _exa = [sum(_fx(x) for x in range(0, _lo_x + 1)), sum(_fx(x) for x in range(_hi_x, _n + 1)), sum(_fx(x) for x in range(_r, _n + 1)), sum(_fy(y) for y in range(_r, _n + 1)), 1 - sum(_fy(y) for y in range(_r, _tail_y + 1))]
            _columns.append(["", ""] + [f"${v:.3f}$" for v in (_Xm.mean(), _Xm.var(), _Ym.mean())] + [f"${abs(v):.4f}$" for v in _sim])
            _columns.append([f"${_pmfs[_name][2]}$", f"${_pmfs[_name][3]}$"] + [f"${v:.3f}$" for v in (_EX, _VX, _EY)] + [f"${abs(round(v, 4)):.4f}$" for v in _exa])
        _A, _B = rf"$\textcolor{{{BLUE}}}{{\text{{player A}}}}$", rf"$\textcolor{{{RED}}}{{\text{{player B}}}}$"
        _mtxt = f"{_m:,}".replace(",", r"\,")
        _lines = [f"| first ${_mtxt}$ runs | {_A}, simulated | {_A}, exact | {_B}, simulated | {_B}, exact |", "|:--|--:|--:|--:|--:|"]
        _lines += [f"| {_label} | " + " | ".join(c[i] for c in _columns) + " |" for i, _label in enumerate(_labels)]
        _table = "\n".join(_lines)

        # --- player B, run 1: probability that the next song is by the artist (ten songs per block)
        _seq = _seqB[0][:_n]
        _before = np.r_[0, np.cumsum(_seq)[:-1]]
        _next = (_K - _before) / (_N - np.arange(_n))
        _nlines = ["| player B, run 1 |" + " |" * 10, "|:--|" + "--:|" * 10]
        for _start in range(0, _n, 10):
            _js = list(range(_start, min(_start + 10, _n)))
            _pad = [""] * (10 - len(_js))
            _nlines.append("| **song** | " + " | ".join([f"**{j + 1}**" for j in _js] + _pad) + " |")
            _nlines.append("| by the artist? | " + " | ".join([r"$\bullet$" if _seq[j] else r"$\cdot$" for j in _js] + _pad) + " |")
            _nlines.append("| $P$(next is by the artist), player B | " + " | ".join([f"${_next[j]:.3f}$" for j in _js] + _pad) + " |")
            _nlines.append("| $P$(next is by the artist), player A | " + " | ".join([f"${_p:.3f}$" for _ in _js] + _pad) + " |")
        _nxt = "\n".join(_nlines)

        _out = mo.accordion(
            {
                "Simulation [cell 4]": mo.vstack(
                    [
                        _controls,
                        mo.md(_table),
                        mo.md("The first 12 runs of each player. Filled square: a song by the artist; shaded: the songs counted in $X$; ring: the song counted by $Y$."),
                        _sfig,
                        mo.md("Bars: the fraction of the runs shown; stems: the exact pmf." + (" For $Y$: the outline of the bars and the pmf as dots." if _wide else "")),
                        _hfig,
                        mo.md(_nxt),
                    ]
                ),
            }
        )
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (e) Compare the distributions of $X$ for $N = 20$, $40$, $200$, $2000$, with $K/N = 0.2$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    z_sizes = mo.ui.text(value="20, 40, 200, 2000", label="playlist sizes $N$", full_width=False)
    z_played = mo.ui.slider(1, 50, 1, value=10, label="played $n$", show_value=True)
    z_frac = mo.ui.slider(0.05, 0.95, 0.05, value=0.2, label="fraction by the artist $K/N$", show_value=True)
    z_seed = mo.ui.number(value=2029, label="seed", step=1)
    return z_frac, z_played, z_seed, z_sizes


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, LIGHT, MaxNLocator, RED, binomial_pmf, hypergeometric_pmf, mo, np, z_frac, z_played, z_seed, z_sizes):
    _n, _p, _reps = z_played.value, z_frac.value, 10000
    _tokens = list(dict.fromkeys(v.strip() for v in z_sizes.value.replace(";", ",").split(",") if v.strip()))
    _sizes = [int(v) for v in _tokens if v.isdigit() and int(v) >= _n and round(int(v) * _p) >= 1]
    _A, _B = rf"$\textcolor{{{BLUE}}}{{\text{{player A}}}}$", rf"$\textcolor{{{RED}}}{{\text{{player B}}}}$"
    _rows = [f"| songs $N$ | by the artist $K$ | variance of $X$: {_A}, simulated | {_A}, exact | {_B}, simulated | {_B}, exact |", "|--:|--:|--:|--:|--:|--:|"]
    _parts = [mo.hstack([z_sizes, z_played, z_frac, z_seed], justify="start", gap=2, wrap=True)]
    _fig = None
    if _sizes:
        _rng = np.random.default_rng(int(z_seed.value))
        _counts = {N: (_rng.binomial(_n, round(N * _p) / N, size=_reps), _rng.hypergeometric(round(N * _p), N - round(N * _p), _n, size=_reps)) for N in _sizes}
        _ncols = min(len(_sizes), 4)
        _nrows = -(-len(_sizes) // _ncols)
        _fig = Figure(figsize=(FULL, 2.9 * _nrows), layout="constrained")
        _fig.get_layout_engine().set(wspace=0.06)
        _axes = np.atleast_1d(_fig.subplots(_nrows, _ncols, sharey=True, squeeze=False)).ravel()
        _xs = np.arange(0, _n + 1)
        for _ax in _axes[len(_sizes) :]:
            _ax.axis("off")
        for _i, (_ax, _Nn) in enumerate(zip(_axes, _sizes)):
            _Kk = round(_Nn * _p)
            for _k, (_vals, _pmf, _colour) in enumerate(((_counts[_Nn][0], lambda x, N=_Nn, K=_Kk: binomial_pmf(x, _n, K / N), BLUE), (_counts[_Nn][1], lambda x, N=_Nn, K=_Kk: hypergeometric_pmf(x, N, K, _n), RED))):
                _off = (_k - 0.5) * 0.4
                _exact = [_pmf(int(x)) for x in _xs]
                _ax.bar(_xs + _off, np.bincount(_vals, minlength=_n + 1) / _reps, width=0.4, color=LIGHT, edgecolor=_colour, lw=0.7)
                _ax.vlines(_xs + _off, 0, _exact, color=_colour, lw=0.9)
                _ax.plot(_xs + _off, _exact, "o", color=_colour, ms=3)
            _ax.set_xlabel(f"$X$,  $N = {_Nn}$", fontsize=13)
            _ax.set_xlim(-0.6, _n + 0.6)
            _ax.tick_params(labelsize=11)
            _ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            for _sp in ("top", "right"):
                _ax.spines[_sp].set_visible(False)
            if _i % _ncols == 0:
                _ax.set_ylabel("fraction of runs", fontsize=13)
        _axes[_ncols - 1].text(1.0, 1.03, "player B", color=RED, fontsize=12, ha="right", va="bottom", transform=_axes[_ncols - 1].transAxes)
        _axes[0].text(0.0, 1.03, "player A", color=BLUE, fontsize=12, ha="left", va="bottom", transform=_axes[0].transAxes)
    for _v in _tokens:
        if not _v.isdigit():
            _rows.append(f"| {_v} | | need a whole number | | | |")
        elif int(_v) not in _sizes:
            _rows.append(f"| ${int(_v)}$ | ${round(int(_v) * _p)}$ | need $N \\geq n$ and $K \\geq 1$ | | | |")
        else:
            _Nn, _Kk = int(_v), round(int(_v) * _p)
            _q = _Kk / _Nn
            _rows.append(f"| ${_Nn}$ | ${_Kk}$ | ${_counts[_Nn][0].var():.3f}$ | ${_n * _q * (1 - _q):.3f}$ | ${_counts[_Nn][1].var():.3f}$ | ${_n * _q * (1 - _q) * (_Nn - _n) / max(_Nn - 1, 1):.3f}$ |")
    if not _tokens:
        _rows.append("| need playlist sizes $N \\geq n$, separated by commas | | | | | |")
    _parts.append(mo.md("\n".join(_rows)))
    if _fig is not None:
        _parts += [mo.md("Bars: the fraction of $10\\,000$ runs; stems: the exact pmf."), _fig]
    mo.accordion(
        {
            "Simulation [cell 5]": mo.vstack(_parts),
            "Solution": mo.md(
                r"""
    (a) Player A: ${X \sim \mathrm{B}(10, 0.2)}$, $E[X] = 2$, $\mathrm{Var}(X) = 1.6$; ${Y \sim \mathrm{NB}(2, 0.2)}$, $E[Y] = 10$. Player B: ${X \sim \mathrm{HG}(20, 4, 10)}$, $E[X] = 2$, $\mathrm{Var}(X) = 1.6 \cdot 10/19 \approx 0.842$; ${Y \sim \mathrm{NHG}(20, 4, 2)}$, $E[Y] = 2 \cdot 21/5 = 8.4$.

    (b) Player A: $P(X \geq 2) = 1 - 0.8^{10} - 10 (0.2) 0.8^9 \approx 0.624$ and $P(Y \leq 10) = \sum_{y=2}^{10} (y - 1)(0.2)^2 (0.8)^{y-2} \approx 0.624$. Player B: $P(X \geq 2) = 1 - \big[\binom{16}{10} + 4 \binom{16}{9}\big] / \binom{20}{10} \approx 0.709$ and $P(Y \leq 10) \approx 0.709$. The same event: the second song by the artist plays by song 10 exactly when at least two of the first ten are by the artist.

    (c) The same runs, for the same reason.

    (d) Player A in all three: $P(X = 0)$ is $0.107$ against $0.043$, $P(X \geq 4)$ is $0.121$ against $0.043$, and $P(Y > 15) = 0.8^{15} + 15 (0.2) 0.8^{14} \approx 0.167$ against $\big[\binom{16}{15} + 4 \binom{16}{14}\big] / \binom{20}{15} \approx 0.032$, at most one song by the artist among the first 15: one run in six against one in thirty. Under player B each song by the artist lowers the chance of the next one $(4/20 \to 3/19)$ and each other song raises it $(4/20 \to 4/19)$; under player A it is $0.2$ always.

    (e) $\mathrm{Var}(X)$ under player B: $0.842$, $1.231$, $1.528$, $1.593$, against $1.6$. By $2\,000$ songs, selecting ten songs hardly changes the artist's share of the remaining playlist, so the two distributions become nearly equal.
    """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(box, mo):
    q3_boxes = mo.ui.array([box() for _ in range(6)])
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
            mo.md(r"(c) Find the mean and standard deviation of $T(60)$ from $10\,000$ simulated openings. Compare with (a)."),
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
def _(BLUE, FULL, Figure, GREEN, GREY, LIGHT, a_cut, a_rate, a_seats, a_seed, mo, np, seat_open_probability):
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
    # the frame follows the simulated data: every opening is drawn
    _TMAX = float(np.ceil(max(_tcut * 1.1, _T.max()) / 5) * 5)
    _Rcut = (_arr <= round(_tcut * _slots)).sum(axis=1)
    _open = _Rcut < _seats

    # --- timelines of 15 openings (their requests continued up to the right edge of the frame)
    _show = _arr[:15]
    while np.any(_show[:, -1] <= _TMAX * _slots):
        _show = np.concatenate((_show, _show[:, -1, None] + _rng.geometric(_rate / _slots, size=(15, 64)).cumsum(axis=1)), axis=1)
    _tfig = Figure(figsize=(FULL, 4.2), layout="constrained")
    _ax = _tfig.subplots()
    for _row in range(15):
        _c = BLUE if _open[_row] else GREY
        _vis = _show[_row] / _slots
        _vis = _vis[_vis <= _TMAX]
        _ax.hlines(-_row, 0, _TMAX, color=LIGHT, lw=1, zorder=1)
        _ax.scatter(_vis, np.full(len(_vis), -_row), color=_c, s=5, zorder=2)
        _ax.plot(_T[_row], -_row, "|", color=GREEN, ms=13, mew=2, zorder=3)
        _ax.text(1.012, -_row, f"$R(t) = {_Rcut[_row]}$", transform=_ax.get_yaxis_transform(), va="center", fontsize=11)
    _ax.axvline(_tcut, color=GREY, ls=(0, (4, 3)), lw=1, zorder=1)
    _ax.text(_tcut, 1.02, f"$t = {_tcut:g}$", ha="center", va="bottom", fontsize=12, transform=_ax.get_xaxis_transform())
    _ax.set_yticks(-np.arange(15), np.arange(1, 16))
    _ax.set_xlabel("seconds after opening", fontsize=13)
    _ax.set_ylabel("opening", fontsize=13)
    _ax.set_xlim(0, _TMAX)
    _ax.set_ylim(-14.7, 0.7)
    _ax.tick_params(labelsize=11)
    for _sp in ("top", "right"):
        _ax.spines[_sp].set_visible(False)

    # --- histogram of T(seats) and the open-seat curve
    _hfig = Figure(figsize=(FULL, 5.0), layout="constrained")
    _h, _o = _hfig.subplots(2, 1, sharex=True)
    _bins = np.linspace(0, _TMAX, 61)
    _h.hist(_T, bins=_bins, weights=np.full(len(_T), 1 / len(_T)), color=LIGHT, edgecolor=BLUE, lw=0.7)
    _h.axvline(_T.mean(), color=GREEN, lw=1.4)
    _h.text(_T.mean(), 1.02, "mean", color=GREEN, ha="center", va="bottom", fontsize=12, transform=_h.get_xaxis_transform())
    _h.set_ylabel("fraction of openings", fontsize=13)
    _grid = np.linspace(0, _TMAX, 300)
    _o.plot(_grid, [seat_open_probability(t, _seats, _rate) for t in _grid], color=BLUE, lw=1.4)
    _dots = np.linspace(0, _TMAX, 41)
    _o.plot(_dots, [(_T > t).mean() for t in _dots], "o", color="black", ms=3)
    _o.axvline(_tcut, color=GREY, ls=(0, (4, 3)), lw=1)
    _o.text(_tcut, 1.02, f"$t = {_tcut:g}$", ha="center", va="bottom", fontsize=12, transform=_o.get_xaxis_transform())
    _o.set_xlabel("seconds after opening", fontsize=13)
    _o.set_ylabel("seat still open", fontsize=13)
    _o.set_xlim(0, _TMAX)
    _o.set_ylim(0, 1.04)
    for _ax in (_h, _o):
        _ax.tick_params(labelsize=11)
        for _sp in ("top", "right"):
            _ax.spines[_sp].set_visible(False)

    _rows = [
        f"| ${_runs:,}$ simulated openings | simulated | exact |".replace(",", r"\,"),
        "|:--|--:|--:|",
        f"| mean of $T({_seats})$ | ${_T.mean():.3f}$ | ${_seats / _rate:.3f}$ |",
        f"| standard deviation of $T({_seats})$ | ${_T.std():.3f}$ | ${np.sqrt(_seats) / _rate:.3f}$ |",
        f"| seat open at the cutoff $t = {_tcut:g}$ | ${(_T > _tcut).mean():.4f}$ | ${seat_open_probability(_tcut, _seats, _rate):.4f}$ |",
    ] + [f"| seat open at $t = {t:g}$ | ${(_T > t).mean():.4f}$ | ${seat_open_probability(t, _seats, _rate):.4f}$ |" for t in (20.0, 30.0, 40.0)]

    mo.accordion(
        {
            "Simulation [cell 6]": mo.vstack(
                [
                    mo.hstack([a_rate, a_seats, a_cut, a_seed], justify="start", gap=2, wrap=True),
                    mo.md("\n".join(_rows)),
                    mo.md(f"The first 15 openings. Dots: requests (grey rows: the course is full by the cutoff $t$); bar: request ${_seats}$, at time $T({_seats})$."),
                    _tfig,
                    mo.md(f"Above: the simulated values of $T({_seats})$. Below, curve: $P(R(t) < {_seats})$; dots: the fraction of openings with $T({_seats}) > t$."),
                    _hfig,
                ]
            ),
            "Solution": mo.md(
                r"""
    (a) $R(1) \sim \mathrm{Pois}(2)$: $P(R(1) = 0) = e^{-2} \approx 0.135$. One request per half second on average: $E[T(1)] = 1/2$ s and $E[T(60)] = 60/2 = 30$ s.

    (b) $\{R(t) < 60\} = \{T(60) > t\}$: fewer than 60 requests by time $t$ exactly when the 60th request comes after $t$.

    (c) Simulated mean $\approx 30$ s; standard deviation $\approx 3.9$ s ($T(60) \sim \mathrm{Gamma}(60, 2)$, variance $60/4$).

    (d) $P(R(t) < 60)$ with $R(t) \sim \mathrm{Pois}(2t)$: $0.998$ at $t = 20$, $0.483$ at $t = 30$, $0.009$ at $t = 40$.
    """
            ),
        }
    )
    return


if __name__ == "__main__":
    app.run()

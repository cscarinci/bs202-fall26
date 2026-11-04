import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BS202 · Lecture 19 · Guided Practice 2", css_file="bs202.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.ticker import MaxNLocator

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Figure, MaxNLocator, math, mo, np


@app.cell(hide_code=True)
def _(mo):
    # Palette with fixed roles, as in the lecture notebooks:
    #   BLUE   the primary object (dots, curve)
    #   RED    dots and bars whose error is too large
    #   LIGHT  the band of allowed errors and the bars inside it
    #   GREY   reference lines
    BLUE, RED, PINK, LIGHT, GREY = "#3f5f8f", "#a8554c", "#e6c7c3", "#e3ebf4", "#9a9a9a"
    WIDTH = 7.4
    POLLS = [0, 1, 2, 3, 10, 50, 100, 500, 1000]

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

    # the normal distribution, with numpy only
    _erfc = np.vectorize(math.erfc)

    def norm_sf(z):
        """P(Z > z) for Z ~ N(0, 1)."""
        return 0.5 * _erfc(np.asarray(z) / math.sqrt(2))

    def norm_pdf(x, mu, sd):
        return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))

    def plain_axes(ax):
        ax.tick_params(labelsize=11)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    def thin(n):
        """A number with a thin space between thousands, as in the text."""
        return f"{n:,}".replace(",", r"\,")

    def repeat_button():
        return mo.ui.button(label="Repeat", value=0, on_click=lambda v: v + 1)

    def percent(slider):
        """A slider of percentages, with its value written as a percentage at its end."""
        return mo.hstack([slider, mo.md(f"{slider.value:g}%").style({"font-size": "0.8rem", "color": "#6b7280"})], justify="start", gap=0.5, align="center")

    return BLUE, GREY, LIGHT, PINK, POLLS, RED, WIDTH, header, norm_pdf, norm_sf, percent, plain_axes, repeat_button, thin


@app.cell(hide_code=True)
def _(header):
    header("Guided Practice 2", "Week 11", "Guided Practice 2")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1

    A poll asks $n$ voters, chosen at random, whether they support candidate A. Let $p$ be the true (unknown) fraction of all voters who support A, and let $X_i$ be the answer of the $i$-th voter:

    $$
    X_i = \begin{cases} 1 & \text{if the } i\text{-th voter supports A,} \\ 0 & \text{otherwise.} \end{cases}
    $$

    Define $\hat p_X = \frac1n(X_1 + \dots + X_n)$, the fraction of polled voters that support A, and its error of estimation $|\hat p_X - p|$.

    **(a)** For a poll of $n = 1\,000$ voters, the error is at most $3.1\%$ with probability at least $0.95$. How many voters must a poll ask so that the error is at most $1.55\%$ with probability at least $0.95$? Write down a guess.
    """)
    return


@app.cell(hide_code=True)
def _(POLLS, mo, repeat_button):
    s1_p = mo.ui.slider(5, 95, 1, value=30, label="$p$")
    s1_n = mo.ui.number(start=100, stop=25000, step=1, value=1000, label="$n$")
    s1_e = mo.ui.radio(options={"3.1%": 3.1, "1.55%": 1.55}, value="3.1%", label=r"$\varepsilon$", inline=True)
    s1_k = mo.ui.slider(steps=POLLS, value=0, label="number of polls", show_value=True)
    s1_r = repeat_button()
    return s1_e, s1_k, s1_n, s1_p, s1_r


@app.cell(hide_code=True)
def _(fig1, mo, percent, s1_e, s1_k, s1_n, s1_p, s1_r):
    mo.accordion({"Simulation 1": mo.vstack([mo.vstack([mo.md(r"""Each dot is one poll of $n$ voters. A dot is red when $|\hat p_X - p| > \varepsilon$."""), mo.hstack([percent(s1_p), s1_n, s1_e], justify="start", gap=2), mo.hstack([s1_k, s1_r], justify="start", gap=2)]), fig1])})
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, MaxNLocator, np, plain_axes, RED, s1_e, s1_k, s1_n, s1_p, s1_r, thin, WIDTH):
    def _sim1():
        p, n, e, k = s1_p.value, int(s1_n.value), s1_e.value, s1_k.value
        ph = np.random.default_rng(100 + s1_r.value).binomial(n, p / 100, 1000)[:k] / n * 100
        red = np.abs(ph - p) > e + 1e-9
        x = np.arange(1, k + 1)
        half = max(5.0, 4 * np.sqrt(p * (100 - p) / n))
        xmax = max(k, 10)
        fig = Figure(figsize=(WIDTH, 3.4))
        ax = fig.subplots()
        ax.axhspan(p - e, p + e, color=LIGHT, lw=0)
        ax.axhline(p, color="black", lw=1)
        size = 14 if k <= 100 else 5
        ax.scatter(x[~red], ph[~red], s=size, color=BLUE)
        ax.scatter(x[red], ph[red], s=size, color=RED)
        ax.text(xmax * 1.015, p, "$p$", va="center")
        ax.text(xmax * 1.015, p + e, r"$p + \varepsilon$", va="center", fontsize=12)
        ax.text(xmax * 1.015, p - e, r"$p - \varepsilon$", va="center", fontsize=12)
        ax.set_xlim(0, xmax * 1.01)
        # a fraction lies between 0% and 100%
        ax.set_ylim(max(p - half, 0), min(p + half, 100))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("poll")
        ax.set_ylabel(r"$\hat p_X$ (%)")
        plain_axes(ax)
        top = r"$p = %d\%%$, $n = %s$, $\varepsilon = %s\%%$" % (p, thin(n), f"{e:g}")
        if k:
            top += r":  %d of %d polls are red (%.1f%%)" % (red.sum(), k, 100 * red.mean())
        ax.set_title(top, fontsize=12)
        fig.tight_layout()
        return fig

    fig1 = _sim1()
    return (fig1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **(b)** State the distribution of $X_i$, and the sampling distribution of $\hat p_X$.

    **(c)** Use the central limit theorem to write the probability that the error is at most $\varepsilon$ in terms of $n$, $p$ and $\varepsilon$. For which $p$ is this probability smallest?

    CLT: for large $n$,

    $$
    P(Z_n \leq z) \approx \Phi(z), \qquad Z_n = \frac{M_n - \mu}{\sigma/\sqrt n}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo, repeat_button):
    # ==== BEGIN: CLT box, the sample means M_1, ..., M_1000 of one population (added 2026-11-02) ====
    clt_pop = mo.ui.dropdown(options=["Binom(1, p)", "Geom(p)", "Pois(λ)", "Exp(λ)", "N(μ, σ²)"], value="Binom(1, p)", label="population")
    clt_p = mo.ui.slider(5, 95, 1, value=30, label="$p$")
    clt_l = mo.ui.slider(0.5, 5, 0.5, value=2, label=r"$\lambda$", show_value=True)
    clt_m = mo.ui.slider(-5, 5, 0.5, value=0, label=r"$\mu$", show_value=True)
    clt_s = mo.ui.slider(0.5, 3, 0.5, value=1, label=r"$\sigma$", show_value=True)
    clt_ax = mo.ui.radio(options=["Mₙ", "Zₙ"], value="Mₙ", inline=True)
    clt_r = repeat_button()
    return clt_ax, clt_l, clt_m, clt_p, clt_pop, clt_r, clt_s


@app.cell(hide_code=True)
def _(clt_ax, clt_l, clt_m, clt_p, clt_pop, clt_r, clt_s, fig_clt, mo, percent):
    # only the parameter of the chosen population
    _par = {"Binom(1, p)": [percent(clt_p)], "Geom(p)": [percent(clt_p)], "Pois(λ)": [clt_l], "Exp(λ)": [clt_l], "N(μ, σ²)": [clt_m, clt_s]}[clt_pop.value]
    mo.accordion({"CLT": mo.vstack([mo.vstack([mo.md(r"""Each slice is one $n$. The bars show 10 000 sample means, and the line is the exact distribution."""), mo.hstack([clt_pop, *_par, clt_ax, clt_r], justify="start", gap=2, wrap=True)]), fig_clt])})
    return


@app.cell(hide_code=True)
def _(BLUE, clt_ax, clt_l, clt_m, clt_p, clt_pop, clt_r, clt_s, math, mo, np):
    import html as _html
    import json as _json

    # a canvas drawn by hand, so that the picture turns when dragged (double-click resets the view)
    _PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
    html, body { margin: 0; background: #fff; }
    canvas { display: block; width: 100%; height: 520px; cursor: grab; touch-action: none; }
    canvas.drag { cursor: grabbing; }
    </style></head><body><canvas id="c"></canvas><script>
    (() => {
      const S = __DATA__;
      const cv = document.getElementById("c"), g = cv.getContext("2d");
      let store = {};
      try { store = window.parent.__bs202clt || (window.parent.__bs202clt = {}); } catch (e) {}
      const HOME = { az: -60, el: 24 };
      let view = store.view ? { ...store.view } : { ...HOME };
      const N = S.slices.length, BX = 1, BY = 2.2, BZ = 0.75, TOP = 34;
      const X = (x) => ((x - S.lo) / (S.hi - S.lo) - 0.5) * BX;
      const Y = (i) => (i / (N - 1) - 0.5) * BY;
      const Z = (h) => (h / S.top - 0.5) * BZ;
      let W = 0, H = 0, sc = 1, cx = 0, cy = 0;
      function fit() {
        const r = window.devicePixelRatio || 1;
        W = cv.clientWidth; H = cv.clientHeight;
        cv.width = W * r; cv.height = H * r; g.setTransform(r, 0, 0, r, 0, 0);
      }
      // the box, as seen now, fills the canvas with room for the labels
      function frame() {
        sc = 1; cx = 0; cy = 0;
        const q = [];
        for (const x of [-BX / 2, BX / 2]) for (const y of [-BY / 2, BY / 2]) for (const z of [-BZ / 2, BZ / 2]) q.push(proj(x, y, z));
        const xs = q.map((p) => p[0]), ys = q.map((p) => p[1]);
        const bw = Math.max(...xs) - Math.min(...xs), bh = Math.max(...ys) - Math.min(...ys);
        sc = Math.min((W - 120) / bw, (H - TOP - 70) / bh);
        cx = W / 2 - sc * (Math.max(...xs) + Math.min(...xs)) / 2;
        cy = TOP + 10 + (H - TOP - 30) / 2 - sc * (Math.max(...ys) + Math.min(...ys)) / 2;
      }
      // the same projection as matplotlib's view_init(elev, azim)
      function proj(x, y, z) {
        const a = view.az * Math.PI / 180, e = view.el * Math.PI / 180;
        const sx = -x * Math.sin(a) + y * Math.cos(a);
        const sy = -(x * Math.cos(a) + y * Math.sin(a)) * Math.sin(e) + z * Math.cos(e);
        const d = (x * Math.cos(a) + y * Math.sin(a)) * Math.cos(e) + z * Math.sin(e);
        return [cx + sc * sx, cy - sc * sy, d];
      }
      const font = (s, it) => (it ? "italic " : "") + s + "px 'Latin Modern Roman', 'CMU Serif', Georgia, serif";
      function line(pts, c, w) {
        g.beginPath(); pts.forEach((p, i) => { const q = proj(...p); i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1]); });
        g.strokeStyle = c; g.lineWidth = w; g.stroke();
      }
      function text(p, s, size, it) {
        const q = proj(...p); g.fillStyle = "#000"; g.font = font(size, it); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(s, q[0], q[1]);
      }
      function draw() {
        g.clearRect(0, 0, W, H);
        frame();
        g.fillStyle = "#000"; g.font = font(17); g.textAlign = "center"; g.textBaseline = "top"; g.fillText(S.title, W / 2, 6);
        const fl = -BZ / 2, hx = BX / 2, hy = BY / 2;
        // the edges nearer the viewer carry the axes
        const ey = proj(0, -hy, fl)[2] > proj(0, hy, fl)[2] ? -hy : hy;
        const ex = proj(hx, 0, fl)[2] > proj(-hx, 0, fl)[2] ? hx : -hx;
        line([[-hx, ey, fl], [hx, ey, fl]], "#000", 1);
        line([[ex, -hy, fl], [ex, hy, fl]], "#000", 1);
        const out = Math.sign(ey), side = Math.sign(ex);
        for (const [v, s] of S.ticks) {
          line([[X(v), ey, fl], [X(v), ey + out * 0.03, fl]], "#000", 1);
          text([X(v), ey + out * 0.12, fl], s, 13);
        }
        text([0, ey + out * 0.3, fl], S.axis, 17, true);
        S.slices.forEach((s, i) => {
          line([[ex, Y(i), fl], [ex + side * 0.025, Y(i), fl]], "#000", 1);
          text([ex + side * 0.09, Y(i), fl], String(s.n), 13);
        });
        text([ex + side * 0.2, 0, fl], "n", 17, true);
        // the mean of the population, on the floor
        line([[X(S.mu), Y(0), fl], [X(S.mu), Y(N - 1), fl]], "#000", 1);
        // the slices, from the far one to the near one
        const order = S.slices.map((s, i) => i).sort((i, j) => proj(0, Y(i), 0)[2] - proj(0, Y(j), 0)[2]);
        for (const i of order) {
          const s = S.slices[i];
          g.beginPath();
          s.sx.forEach((x, k) => { const q = proj(X(x), Y(i), Z(s.sy[k])); k ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1]); });
          g.closePath(); g.fillStyle = S.light; g.fill();
          // the exact distribution, down to the floor at both ends
          line([[X(s.ex[0]), Y(i), Z(0)], ...s.ex.map((x, k) => [X(x), Y(i), Z(s.ey[k])]), [X(s.ex[s.ex.length - 1]), Y(i), Z(0)]], S.blue, 1.2);
        }
      }
      let pending = false;
      const redraw = () => { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; draw(); }); } };
      let grab = null;
      cv.addEventListener("pointerdown", (e) => { grab = { x: e.clientX, y: e.clientY, ...view }; cv.setPointerCapture(e.pointerId); cv.classList.add("drag"); });
      cv.addEventListener("pointermove", (e) => {
        if (!grab) return;
        view = { az: grab.az - (e.clientX - grab.x) * 0.45, el: Math.max(0, Math.min(89, grab.el + (e.clientY - grab.y) * 0.45)) };
        store.view = { ...view }; redraw();
      });
      const drop = () => { grab = null; cv.classList.remove("drag"); };
      cv.addEventListener("pointerup", drop); cv.addEventListener("pointercancel", drop);
      cv.addEventListener("dblclick", () => { view = { ...HOME }; delete store.view; redraw(); });
      new ResizeObserver(() => { fit(); draw(); }).observe(cv);
      fit(); draw();
    })();
    </script></body></html>"""

    def _sim_clt():
        kind, p, lam, m0, s0 = clt_pop.value, clt_p.value / 100, clt_l.value, clt_m.value, clt_s.value
        standard = clt_ax.value == "Zₙ"
        sizes = [1, 2, 3, 4, 5, 10, 20, 50, 100, 200, 500, 1000]
        samples = 10000
        rng = np.random.default_rng(19 + clt_r.value)
        # mean, standard deviation, window of the axis, and one draw of n values of X
        if kind == "Binom(1, p)":
            mu, sd, lo, hi, title = p, math.sqrt(p * (1 - p)), -0.04, 1.04, "Binom(1, %g)" % p
            draw = lambda m, n: (rng.random((m, n)) < p).sum(axis=1)
            # the sum is Binom(n, p)
            logpmf = lambda k, n: math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log(1 - p)
        elif kind == "Geom(p)":
            mu, sd, title = 1 / p, math.sqrt(1 - p) / p, "Geom(%g)" % p
            lo, hi = 0.5, mu + 4 * sd
            draw = lambda m, n: rng.geometric(p, (m, n)).sum(axis=1)
            # the sum is NB(n, p), the number of trials until the n-th success
            logpmf = lambda k, n: math.lgamma(k) - math.lgamma(n) - math.lgamma(k - n + 1) + n * math.log(p) + (k - n) * math.log(1 - p)
        elif kind == "Pois(λ)":
            mu, sd, title = lam, math.sqrt(lam), "Pois(%g)" % lam
            lo, hi = -0.5, mu + 4 * sd + 0.5
            draw = lambda m, n: rng.poisson(lam, (m, n)).sum(axis=1)
            # the sum is Pois(n lambda)
            logpmf = lambda k, n: -n * lam + k * math.log(n * lam) - math.lgamma(k + 1)
        elif kind == "Exp(λ)":
            mu, sd, lo, hi, title = 1 / lam, 1 / lam, 0, 5 / lam, "Exp(%g)" % lam
            draw = lambda m, n: rng.exponential(1 / lam, (m, n)).sum(axis=1)
            # M_n ~ Gamma(n, n lambda)
            density = lambda x, n: np.where(x > 0, np.exp(n * math.log(n * lam) + (n - 1) * np.log(np.maximum(x, 1e-300)) - n * lam * x - math.lgamma(n)), 0)
        else:
            mu, sd, title = m0, s0, "𝒩(%g, %g²)" % (m0, s0)
            lo, hi = mu - 4 * sd, mu + 4 * sd
            draw = lambda m, n: (m0 + s0 * rng.standard_normal((m, n))).sum(axis=1)
            # M_n ~ N(mu, sigma^2 / n)
            density = lambda x, n: np.sqrt(n / (2 * math.pi)) / sd * np.exp(-n * (x - mu) ** 2 / (2 * sd**2))
        discrete = kind in ("Binom(1, p)", "Geom(p)", "Pois(λ)")

        slices = []
        for n in sizes:
            # the sum of n draws of X, for each of 10 000 samples
            sums = np.concatenate([draw(1000, n) for _ in range(samples // 1000)])
            # the window of M_n on the axis; for the standardized mean, Z_n between -4.5 and 4.5
            se = sd / math.sqrt(n)
            wlo, whi = (mu - 4.5 * se, mu + 4.5 * se) if standard else (lo, hi)
            if discrete:
                # the sum takes whole values k, so M_n takes the values k/n; grp of them share a bar
                kmin = {"Binom(1, p)": 0, "Geom(p)": n, "Pois(λ)": 0}[kind]
                k0 = max(math.ceil(wlo * n - 0.5), kmin)
                k1 = math.floor(whi * n + 0.5)
                if kind == "Binom(1, p)":
                    k1 = min(k1, n)
                grp = max(1, math.ceil((k1 - k0 + 1) / 150))
                nb = (k1 - k0) // grp + 1
                edges = (k0 - 0.5 + grp * np.arange(nb + 1)) / n
                idx = (sums - k0) // grp
                sim = np.bincount(idx[(idx >= 0) & (idx < nb)], minlength=nb) / samples
                # the last bar may reach past the largest value of the sum (n, for Binom); those values have probability 0
                kmax = n if kind == "Binom(1, p)" else math.inf
                exact = np.array([math.exp(logpmf(k, n)) if k <= kmax else 0.0 for k in range(k0, k0 + grp * nb)]).reshape(nb, grp).sum(axis=1)
                width = grp / n
                ex, ey = np.repeat(edges, 2)[1:-1], np.repeat(exact / width, 2)
            else:
                width = (whi - wlo) / 150
                edges = wlo + width * np.arange(151)
                sim = np.histogram(sums / n, bins=edges)[0] / samples
                ex = np.linspace(wlo, whi, 300)
                ey = density(ex, n)
            sx = np.clip(np.repeat(edges, 2), wlo, whi)
            sy = np.concatenate([[0], np.repeat(sim / width, 2), [0]])
            ex = np.clip(ex, wlo, whi)
            if standard:
                # Z_n = (M_n - mu) / (sigma / sqrt(n)); a density in z is se times the density in M_n
                sx, ex, sy, ey = (sx - mu) / se, (ex - mu) / se, sy * se, ey * se
            slices.append({"n": n, "sx": np.round(sx, 5).tolist(), "sy": np.round(sy, 5).tolist(), "ex": np.round(ex, 5).tolist(), "ey": np.round(ey, 5).tolist()})

        xlo, xhi = (-4.5, 4.5) if standard else (lo, hi)
        top = 1.02 * max(max(max(s["sy"]), max(s["ey"])) for s in slices)
        step = [t for t in (0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 25, 50) if (xhi - xlo) / t <= 8][0]
        ticks = [round(t, 6) for t in np.arange(math.ceil(xlo / step) * step, xhi + 1e-9, step)]
        data = {
            "title": "population " + title, "axis": "Zₙ" if standard else "Mₙ", "lo": xlo, "hi": xhi, "top": top,
            "mu": 0 if standard else mu, "ticks": [[t, f"{t:g}".replace("-", "−")] for t in ticks],
            # the bars darker than LIGHT and see-through, so the slices behind show
            "blue": BLUE, "light": "rgba(120, 150, 190, 0.45)", "slices": slices,
        }
        page = _PAGE.replace("__DATA__", _json.dumps(data))
        return mo.Html(f'<iframe srcdoc="{_html.escape(page)}" title="The distribution of the sample mean for n = 1 to 1000; drag to turn" style="display: block; width: 100%; height: 524px; border: 0;"></iframe>')

    fig_clt = _sim_clt()
    # ==== END: CLT box ====
    return (fig_clt,)


@app.cell(hide_code=True)
def _(mo):
    s2_p = mo.ui.slider(5, 95, 1, value=30, label="$p$")
    s2_n = mo.ui.number(start=100, stop=25000, step=1, value=2000, label="$n$")
    return s2_n, s2_p


@app.cell(hide_code=True)
def _(fig2, mo, percent, s2_n, s2_p):
    mo.accordion({"Simulation 2": mo.vstack([mo.vstack([mo.md(r"""The histogram shows 10 000 polls of $n$ voters. The curve is the density of $\mathcal N(p, pq/n)$. A bar is red when $|\hat p_X - p| > 1.55\%$."""), mo.hstack([percent(s2_p), s2_n], justify="start", gap=2)]), fig2])})
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, norm_pdf, norm_sf, np, PINK, s2_n, s2_p, WIDTH):
    def _sim2():
        p, n, e = s2_p.value, int(s2_n.value), 1.55
        sd = np.sqrt(p * (100 - p) / n)
        ph = np.random.default_rng(8).binomial(n, p / 100, 10000) / n * 100
        half = max(6.0, 4 * sd)
        lo, hi = max(p - half, 0), min(p + half, 100)
        step = 100 / n
        width = max(1, round(0.1 / step)) * step
        edges = p - step / 2 + width * np.arange(np.floor(-half / width), np.ceil(half / width) + 1)
        h, ed = np.histogram(ph, bins=edges, density=True)
        mid = (ed[:-1] + ed[1:]) / 2
        
        in_bar, _ = np.histogram(ph, bins=edges)
        red_in_bar, _ = np.histogram(ph[np.abs(ph - p) > e + 1e-9], bins=edges)
        h_red = h * red_in_bar / np.maximum(in_bar, 1)
        fig = Figure(figsize=(WIDTH, 3.4))
        ax = fig.subplots()
        ax.bar(mid, h, width=ed[1] - ed[0], color=LIGHT, edgecolor="white")
        ax.bar(mid, h_red, width=ed[1] - ed[0], color=PINK, edgecolor="white")
        xx = np.linspace(lo, hi, 600)
        f = norm_pdf(xx, p, sd)
        ax.plot(xx, f, color=BLUE, lw=1.8)
        top = max(f.max(), h.max())
        ax.plot([p, p], [0, top * 1.08], color="black", lw=1)
        ax.text(p, top * 1.1, "$p$", ha="center")
        ax.set_xlim(lo, hi)
        ax.set_ylim(0, top * 1.2)
        ax.set_yticks([])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=11)
        ax.set_xlabel(r"$\hat p_X$ (%)")
        red = np.mean(np.abs(ph - p) > e + 1e-9)

        def pct(v):
            """A percentage; a small one with two significant digits, never 0.0%."""
            if v == 0:
                return "0%"
            if v >= 1:
                return "%.1f%%" % v
            k = int(np.floor(np.log10(v)))
            if k >= -3:
                return "%.*f%%" % (1 - k, v)
            m, k = f"{v:.1e}".split("e")
            return r"$%s \times 10^{%d}$%%" % (m, int(k))

        ax.set_title(r"$P(|\hat p_X - p| > %s\%%)$: simulation %s, normal approximation %s" % (f"{e:g}", pct(100 * red), pct(200 * norm_sf(e / sd))), fontsize=12)
        fig.tight_layout()
        return fig

    fig2 = _sim2()
    return (fig2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **(d)** Use (c) to show that, in the normal approximation, for $n = 1\,000$,

    $$
    P(|\hat p_X - p| \leq 3.1\%) \geq 0.95,
    $$

    and find the smallest $n$ for which $P(|\hat p_X - p| \leq 1.55\%) \geq 0.95$. Compare with your guess in (a).

    Reminder: $z_{0.975} = 1.96$, where $\Phi(z_p) = p$.

    **(e)** Use the law of large numbers to find an $n$ for which $P(|\hat p_X - p| \leq 1.55\%) \geq 0.95$. Compare it with the $n$ found in (d).

    LLN: for every $\varepsilon > 0$,

    $$
    P(|M_n - \mu| \geq \varepsilon) \leq \frac{1}{n}\frac{\sigma^2}{\varepsilon^2}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fa_p = mo.ui.slider(5, 95, 1, value=50, label="$p$")
    return (fa_p,)


@app.cell(hide_code=True)
def _(fa_p, figA, mo, percent):
    mo.accordion({"Figure A": mo.vstack([percent(fa_p), figA])})
    return


@app.cell(hide_code=True)
def _(BLUE, fa_p, Figure, GREY, norm_sf, np, plain_axes, RED, WIDTH):
    def _figA():
        p, e = fa_p.value / 100, 0.0155
        pq = p * (1 - p)
        n = np.logspace(2, 5, 400)
        clt = 2 * norm_sf(e * np.sqrt(n) / np.sqrt(pq))
        bound = np.minimum(pq / (n * e**2), 1)
        n_clt = pq * (1.96 / e) ** 2
        n_lln = pq / (0.05 * e**2)
        fig = Figure(figsize=(WIDTH, 3.8))
        ax = fig.subplots()
        ax.plot(n, clt, color=BLUE, lw=1.8)
        ax.plot(n, bound, color=RED, lw=1.8)
        ax.axhline(0.05, color=GREY, lw=1, ls="--")
        ax.text(1.05e5, 0.05, "$0.05$", va="center", fontsize=12)
        # the smallest n of each method, on a row of its own under the ticks
        for x, c in ((n_clt, BLUE), (n_lln, RED)):
            ax.plot([x, x], [0, 0.05], color=c, lw=1, ls=":")
            ax.plot(x, 0.05, "o", color=c, ms=5)
            ax.text(x, -0.19, "$%s$" % f"{int(np.ceil(x)):,}".replace(",", r"\,"), ha="center", va="top", fontsize=11, color=c)
        # each name sits beside its own curve, at a fixed place
        ax.text(108, 0.08, "central limit\ntheorem", color=BLUE, fontsize=12, va="bottom", linespacing=1.1)
        n_half = pq / (0.5 * e**2)
        ax.text(n_half * 1.25, 0.5, "law of large numbers bound", color=RED, fontsize=12, va="center")
        ax.set_xscale("log")
        ax.set_xlim(100, 1e5)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("$n$", labelpad=30)
        ax.set_ylabel(r"$P(|\hat p_X - p| > 1.55\%)$", fontsize=13)
        plain_axes(ax)
        ax.set_title(r"$p = %d\%%$" % fa_p.value, fontsize=12)
        fig.tight_layout()
        return fig

    figA = _figA()
    return (figA,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2

    Voters are now chosen at random from a subgroup in which a fraction $r \neq p$ supports A. Let $Y_i = 1$ if the $i$-th voter supports A, and $Y_i = 0$ otherwise. The poll estimates $p$ by $\hat p_Y = \frac1n (Y_1 + \dots + Y_n)$.

    **(a)** For the poll of $1\,000$ voters in Question 1, the error $|\hat p_X - p|$ is at most $3.1\%$ with probability at least $0.95$. What is the probability that the error $|\hat p_Y - p|$ is at most $3.1\%$ when $r = p + 2\%$ and when $r = p + 4\%$, for $n = 1\,000$? Write down a guess.

    **(b)** Find the bias, the standard error and the mean squared error of $\hat p_Y$, and the limit of the mean squared error as $n \to \infty$.
    """)
    return


@app.cell(hide_code=True)
def _(POLLS, mo, repeat_button):
    s3_p = mo.ui.slider(5, 95, 1, value=30, label="$p$")
    s3_b = mo.ui.slider(0, 5, 1, value=2, label="$r - p$")
    s3_n = mo.ui.number(start=100, stop=1000000, step=1, value=1000, label="$n$")
    s3_k = mo.ui.slider(steps=POLLS, value=0, label="number of polls", show_value=True)
    s3_r = repeat_button()
    return s3_b, s3_k, s3_n, s3_p, s3_r


@app.cell(hide_code=True)
def _(fig3, mo, percent, s3_b, s3_k, s3_n, s3_p, s3_r):
    mo.accordion({"Simulation 3": mo.vstack([mo.vstack([mo.md(r"""Each dot is one poll of $n$ voters from the subgroup. A dot is red when $|\hat p_Y - p| > 3.1\%$."""), mo.hstack([percent(s3_p), percent(s3_b), s3_n], justify="start", gap=2), mo.hstack([s3_k, s3_r], justify="start", gap=2)]), fig3])})
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, MaxNLocator, np, plain_axes, RED, s3_b, s3_k, s3_n, s3_p, s3_r, thin, WIDTH):
    def _sim3():
        p, b, n, k, e = s3_p.value, s3_b.value, int(s3_n.value), s3_k.value, 3.1
        r = p + b
        ph = np.random.default_rng(300 + s3_r.value).binomial(n, r / 100, 1000)[:k] / n * 100
        red = np.abs(ph - p) > e + 1e-9
        x = np.arange(1, k + 1)
        spread = 4 * np.sqrt(r * (100 - r) / n)
        xmax = max(k, 10)
        fig = Figure(figsize=(WIDTH, 3.6))
        ax = fig.subplots()
        ax.axhspan(p - e, p + e, color=LIGHT, lw=0)
        ax.axhline(p, color="black", lw=1)
        ax.axhline(r, color="black", lw=1, ls="--")
        size = 14 if k <= 100 else 5
        ax.scatter(x[~red], ph[~red], s=size, color=BLUE)
        ax.scatter(x[red], ph[red], s=size, color=RED)
        # the names centred in one column right of the plot; one name when the two lines coincide
        names = [(p + e, r"$p + 3.1\%$", 12), (p - e, r"$p - 3.1\%$", 12)]
        names += [(p, "$r = p$", 14)] if b == 0 else [(r, "$r$", 14), (p, "$p$", 14)]
        for y, name, size in names:
            ax.annotate(name, (1, y), xycoords=ax.get_yaxis_transform(), xytext=(27, 0), textcoords="offset points", ha="center", va="center", fontsize=size)
        ax.set_xlim(0, xmax * 1.01)
        # a fraction lies between 0% and 100%
        ax.set_ylim(max(min(p - 6, r - spread), 0), min(max(p + 10, r + spread), 100.5))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("poll")
        ax.set_ylabel(r"$\hat p_Y$ (%)")
        plain_axes(ax)
        top = r"$p = %d\%%$, $r = %d\%%$, $n = %s$" % (p, r, thin(n))
        if k:
            top += r":  %d of %d polls are red (%.1f%%)" % (red.sum(), k, 100 * red.mean())
        ax.set_title(top, fontsize=12)
        fig.tight_layout()
        return fig

    fig3 = _sim3()
    return (fig3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **(c)** Find the limit of $P(|\hat p_Y - p| \leq 3.1\%)$ as $n \to \infty$, when $r = p + 2\%$ and when $r = p + 4\%$. Is $\hat p_Y$ consistent for $p$?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fb_b = mo.ui.slider(0, 5, 1, value=2, label="$r - p$")
    return (fb_b,)


@app.cell(hide_code=True)
def _(fb_b, figB, mo, percent):
    mo.accordion({"Figure B": mo.vstack([percent(fb_b), figB])})
    return


@app.cell(hide_code=True)
def _(BLUE, fb_b, Figure, GREY, np, plain_axes, RED, WIDTH):
    def _figB():
        p, b = 0.30, fb_b.value / 100
        r = p + b
        n = np.logspace(2, 6, 400)
        mse_y = r * (1 - r) / n + b**2
        mse_x = p * (1 - p) / n
        fig = Figure(figsize=(WIDTH, 3.8))
        ax = fig.subplots()
        ax.plot(n, mse_y, color=BLUE, lw=1.8)
        # dashed and on top, so it stays visible where the two curves meet (r = p)
        ax.plot(n, mse_x, color=RED, lw=1.8, ls=(0, (5, 3)), zorder=3)
        if b > 0:
            ax.axhline(b**2, color=GREY, lw=1.2, ls="--")
            ax.text(1.2e6, b**2, "$(r - p)^2$", va="center", fontsize=12)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(100, 1e6)
        ax.set_ylim(1e-7, 4 * mse_y[0])
        ax.text(2e4, 1.9 * (r * (1 - r) / 2e4 + b**2), r"$\mathrm{MSE}(\hat p_Y)$", color=BLUE, fontsize=12)
        ax.text(1.3e5, 2.6 * p * (1 - p) / 1.3e5, r"$\mathrm{MSE}(\hat p_X)$", color=RED, fontsize=12)
        ax.set_xlabel("$n$")
        ax.set_ylabel("mean squared error")
        plain_axes(ax)
        ax.set_title(r"$p = %d\%%$, $r = %d\%%$" % (round(100 * p), round(100 * r)), fontsize=12)
        fig.tight_layout()
        return fig

    figB = _figB()
    return (figB,)


@app.cell(hide_code=True)
def _(figC, mo):
    mo.accordion({"Figure C": figC})
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, norm_sf, np, plain_axes, RED, WIDTH):
    def _figC():
        p, e = 0.30, 0.031
        n = np.logspace(2, 6, 400)

        def inside(r):
            """P(|p_Y - p| <= e), with the normal approximation."""
            sd = np.sqrt(r * (1 - r) / n)
            return norm_sf((p - e - r) / sd) - norm_sf((p + e - r) / sd)

        fig = Figure(figsize=(WIDTH, 3.8))
        ax = fig.subplots()
        # the unbiased poll, dashed and on top
        ax.plot(n, inside(p), color=GREY, lw=1.6, ls="--", zorder=3)
        ax.plot(n, inside(p + 0.02), color=BLUE, lw=1.8)
        ax.plot(n, inside(p + 0.04), color=RED, lw=1.8)
        ax.text(2e3, 1.02, r"$r = p$", color=GREY, fontsize=12, ha="left", va="bottom")
        ax.text(1.5e3, 0.80, r"$r = p + 2\%$", color=BLUE, fontsize=12, ha="left", va="top")
        ax.text(2.5e3, 0.30, r"$r = p + 4\%$", color=RED, fontsize=12, ha="left", va="bottom")
        ax.set_xscale("log")
        ax.set_xlim(100, 1e6)
        ax.set_ylim(0, 1.12)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.set_xlabel("$n$")
        ax.set_ylabel(r"$P(|\hat p_Y - p| \leq 3.1\%)$", fontsize=13)
        plain_axes(ax)
        ax.set_title(r"$p = 30\%$", fontsize=12)
        fig.tight_layout()
        return fig

    figC = _figC()
    return (figC,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3

    The poll of Question 1 runs a second time after a certain period. Between the two polls, the true fraction of all voters who support A might have changed from $p$ to $p'$. The change $d = p' - p$ can be estimated with two methods:

    1. Two independent groups of $n$ voters are asked, one in each poll.
    2. The same $n$ voters are asked in both polls.

    Let $U_i$ and $V_i$ be the answers of the $i$-th voter in the first and in the second poll with method 1, and $\tilde U_i$ and $\tilde V_i$ with method 2. Each answer is $1$ if the voter supports A, and $0$ otherwise. The answers $U_i$ and $V_i$ are independent, while the joint pmf of $(\tilde U_i, \tilde V_i)$ is

    $$
    \def\arraystretch{1.5}
    \begin{array}{c|cc}
     & \quad \tilde V_i = 0 \quad & \quad \tilde V_i = 1 \quad \\ \hline
    \tilde U_i = 0 & 1 - p - b & b \\
    \tilde U_i = 1 & a & p - a
    \end{array}
    $$

    and the change is estimated by

    $$
    \hat d_{U,V} = \frac1n (V_1 + \dots + V_n) - \frac1n (U_1 + \dots + U_n) \quad \text{(method 1)},
    $$

    $$
    \hat d_{\tilde U, \tilde V} = \frac1n (\tilde V_1 + \dots + \tilde V_n) - \frac1n (\tilde U_1 + \dots + \tilde U_n) \quad \text{(method 2)}.
    $$

    **(a)** Let $p = 30\%$, $a = 1\%$, $b = 4\%$ and $n = 1\,000$. Which estimator of $d$ has the smaller standard error, and how many times smaller is it? Write down a guess.

    **(b)** Find $\mathrm{Cov}(U_i, V_i)$ and $\mathrm{Cov}(\tilde U_i, \tilde V_i)$, and the bias and the standard error of $\hat d_{U,V}$ and of $\hat d_{\tilde U, \tilde V}$.
    """)
    return


@app.cell(hide_code=True)
def _(POLLS, mo, repeat_button):
    s4_p = mo.ui.slider(5, 95, 1, value=30, label="$p$")
    s4_a = mo.ui.slider(0, 30, 1, value=1, label="$a$")
    s4_b = mo.ui.slider(0, 30, 1, value=4, label="$b$")
    s4_n = mo.ui.number(start=100, stop=100000, step=1, value=1000, label="$n$")
    s4_k = mo.ui.slider(steps=POLLS, value=0, label="number of runs", show_value=True)
    s4_r = repeat_button()
    return s4_a, s4_b, s4_k, s4_n, s4_p, s4_r


@app.cell(hide_code=True)
def _(fig4, mo, percent, s4_a, s4_b, s4_k, s4_n, s4_p, s4_r):
    mo.accordion({"Simulation 4": mo.vstack([mo.vstack([mo.md(r"""Each dot is the estimate of $d$ from one run of both polls, with $n$ voters in each poll."""), mo.hstack([percent(s4_p), percent(s4_a), percent(s4_b), s4_n], justify="start", gap=2, wrap=True), mo.hstack([s4_k, s4_r], justify="start", gap=2)]), fig4])})
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, MaxNLocator, mo, np, plain_axes, s4_a, s4_b, s4_k, s4_n, s4_p, s4_r, thin):
    def _sim4():
        p, a, b, n, k = s4_p.value / 100, s4_a.value / 100, s4_b.value / 100, int(s4_n.value), s4_k.value
        if s4_a.value > s4_p.value or s4_b.value > 100 - s4_p.value:
            return mo.md(r"$a$ must be at most $p$, and $b$ at most $1 - p$.")
        p2, d = p - a + b, b - a
        rng = np.random.default_rng(400 + s4_r.value)
        d1 = (rng.binomial(n, p2, 1000) - rng.binomial(n, p, 1000))[:k] / n * 100
        c = rng.multinomial(n, [a, b, 1 - a - b], size=1000)[:k]
        d2 = (c[:, 1] - c[:, 0]) / n * 100
        x = np.arange(1, k + 1)
        half = max(8.0, 4 * 100 * np.sqrt((p * (1 - p) + p2 * (1 - p2)) / n))
        xmax = max(k, 10)
        size = 14 if k <= 100 else 5
        fig = Figure(figsize=(9.6, 3.9))
        axs = fig.subplots(1, 2, sharey=True)
        panels = ((axs[0], d1, r"$\hat d_{U,V}$ (%)", "method 1"), (axs[1], d2, r"$\hat d_{\tilde U,\tilde V}$ (%)", "method 2"))
        for ax, dh, label, name in panels:
            ax.axhline(100 * d, color="black", lw=1)
            ax.scatter(x, dh, s=size, color=BLUE)
            ax.text(xmax * 1.015, 100 * d, "$d$", va="center")
            ax.set_xlim(0, xmax * 1.01)
            ax.set_ylim(100 * d - half, 100 * d + half)
            ax.set_xlabel("run")
            ax.set_ylabel(label)
            ax.yaxis.set_tick_params(labelleft=True)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plain_axes(ax)
            title = name
            if k >= 2:
                title += ": standard deviation of the dots %.2f%%" % dh.std(ddof=1)
            ax.set_title(title, fontsize=12)
        top = r"$p = %d\%%$, $a = %d\%%$, $b = %d\%%$, $n = %s$" % (s4_p.value, s4_a.value, s4_b.value, thin(n))
        if k:
            top += ", %d run%s" % (k, "" if k == 1 else "s")
        fig.suptitle(top, fontsize=12)
        fig.tight_layout()
        return fig

    fig4 = _sim4()
    return (fig4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **(c)** Answer the question in (a), and compare with your guess. For which $a$ and $b$ does $\hat d_{\tilde U, \tilde V}$ have the smaller standard error?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # p stops at 90%, so that p + d < 100% and every setting has a curve
    fd_p = mo.ui.slider(5, 90, 1, value=30, label="$p$")
    fd_d = mo.ui.slider(0, 5, 1, value=3, label="$d$")
    return fd_d, fd_p


@app.cell(hide_code=True)
def _(fd_d, fd_p, figD, mo, percent):
    mo.accordion({"Figure D": mo.vstack([mo.hstack([percent(fd_p), percent(fd_d)], justify="start", gap=2), figD])})
    return


@app.cell(hide_code=True)
def _(BLUE, fd_d, fd_p, Figure, GREY, np, plain_axes, RED, thin, WIDTH):
    def _figD():
        p, d, n = fd_p.value / 100, fd_d.value / 100, 1000
        p2 = p + d
        amax = min(p, 1 - p2)
        a = np.linspace(0, amax, 400)
        se1 = np.full_like(a, np.sqrt((p * (1 - p) + p2 * (1 - p2)) / n))
        se2 = np.sqrt((2 * a + d - d**2) / n)
        a0 = p * (1 - p2)
        fig = Figure(figsize=(WIDTH, 3.8))
        ax = fig.subplots()
        ax.plot(100 * a, 100 * se1, color=RED, lw=1.8)
        ax.plot(100 * a, 100 * se2, color=BLUE, lw=1.8)
        if a0 <= amax:
            ax.plot([100 * a0] * 2, [0, 100 * se1[0]], color=GREY, lw=1, ls="--")
            ax.text(100 * a0 - 0.5 * amax / 0.3, 100 * se1[0] * 1.04, r"$\mathrm{Cov}(\tilde U_i, \tilde V_i) = 0$", ha="right", va="bottom", fontsize=12)
        # the flat curve is named at its left end, away from the crossing
        ax.text(100 * amax * 0.01, 100 * se1[0] * 1.04, r"$\mathrm{SE}(\hat d_{U,V})$", color=RED, va="bottom", fontsize=12)
        ax.text(100 * amax * 1.01, 100 * se2[-1], r"$\mathrm{SE}(\hat d_{\tilde U,\tilde V})$", color=BLUE, va="center", fontsize=12)
        ax.set_xlim(0, 100 * amax)
        ax.set_ylim(0, 100 * max(se1[0], se2[-1]) * 1.25)
        ax.set_xlabel("$a$ (%)")
        ax.set_ylabel("standard error (%)")
        plain_axes(ax)
        ax.set_title(r"$p = %d\%%$, $d = b - a = %d\%%$, $n = %s$" % (fd_p.value, fd_d.value, thin(n)), fontsize=12)
        fig.tight_layout()
        return fig

    figD = _figD()
    return (figD,)


if __name__ == "__main__":
    app.run()

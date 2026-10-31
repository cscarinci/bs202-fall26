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

    return BLUE, GREY, LIGHT, PINK, POLLS, RED, WIDTH, header, norm_pdf, norm_sf, plain_axes, repeat_button, thin


@app.cell(hide_code=True)
def _(header):
    header("Guided Practice 2 (draft)", "Week 11", "Guided Practice 2 (draft)")
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

    (a) For a poll of $n = 1\,000$ voters, the error is at most $3.1\%$ with probability at least $0.95$. How many voters must a poll ask so that the error is at most $1.55\%$ with probability at least $0.95$? Write down a guess.
    """)
    return


@app.cell(hide_code=True)
def _(POLLS, mo, repeat_button):
    s1_p = mo.ui.slider(5, 95, 1, value=30, label="$p$ (%)", show_value=True)
    s1_n = mo.ui.number(start=100, stop=25000, step=1, value=1000, label="$n$")
    s1_e = mo.ui.radio(options={"3.1%": 3.1, "1.55%": 1.55}, value="3.1%", label=r"$\varepsilon$", inline=True)
    s1_k = mo.ui.slider(steps=POLLS, value=0, label="number of polls", show_value=True)
    s1_r = repeat_button()
    return s1_e, s1_k, s1_n, s1_p, s1_r


@app.cell(hide_code=True)
def _(mo):
    show1 = mo.ui.button(label="Show simulation 1", value=False, on_click=lambda _: True)
    return (show1,)


@app.cell(hide_code=True)
def _(mo, s1_e, s1_k, s1_n, s1_p, s1_r, show1):
    # the simulation stays hidden until its button is clicked
    show1 if not show1.value else mo.vstack([mo.md(r"""*Simulation 1.* Each dot is the $\hat p_X$ of one poll of $n$ voters. A dot is red when its error $|\hat p_X - p|$ is larger than $\varepsilon$. The fraction of red dots estimates $P(|\hat p_X - p| > \varepsilon)$."""), mo.hstack([s1_p, s1_n, s1_e], justify="start", gap=2), mo.hstack([s1_k, s1_r], justify="start", gap=2)])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, RED, WIDTH, np, plain_axes, s1_e, s1_k, s1_n, s1_p, s1_r, show1, thin):
    def _sim1():
        p, n, e, k = s1_p.value, int(s1_n.value), s1_e.value, s1_k.value
        ph = np.random.default_rng(100 + s1_r.value).binomial(n, p / 100, 1000)[:k] / n * 100
        red = np.abs(ph - p) > e
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
        ax.set_ylim(p - half, p + half)
        ax.set_xlabel("poll")
        ax.set_ylabel(r"$\hat p_X$ (%)")
        plain_axes(ax)
        top = r"$p = %d\%%$, $n = %s$, $\varepsilon = %s\%%$" % (p, thin(n), f"{e:g}")
        if k:
            top += r":  %d of %d polls are red (%.0f%%)" % (red.sum(), k, 100 * red.mean())
        ax.set_title(top, fontsize=12)
        fig.tight_layout()
        return fig

    _sim1() if show1.value else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (b) State the distribution of $X_i$, and the sampling distribution of $\hat p_X$.

    (c) Use the central limit theorem to write the probability that the error is at most $\varepsilon$ in terms of $n$, $p$ and $\varepsilon$. For which $p$ is this probability smallest?

    CLT: for large $n$,

    $$
    P(Z_n \leq z) \approx \Phi(z), \qquad Z_n = \frac{M_n - \mu}{\sigma/\sqrt n}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    s2_p = mo.ui.slider(5, 95, 1, value=30, label="$p$ (%)", show_value=True)
    s2_n = mo.ui.number(start=100, stop=25000, step=1, value=2000, label="$n$")
    return s2_n, s2_p


@app.cell(hide_code=True)
def _(mo):
    show2 = mo.ui.button(label="Show simulation 2", value=False, on_click=lambda _: True)
    return (show2,)


@app.cell(hide_code=True)
def _(mo, s2_n, s2_p, show2):
    # the simulation stays hidden until its button is clicked
    show2 if not show2.value else mo.vstack([mo.md(r"""*Simulation 2.* The histogram shows $\hat p_X$ for 10 000 polls of $n$ voters each. The curve is the density of $\mathcal N(p, pq/n)$. A bar is red when $|\hat p_X - p| > 1.55\%$."""), mo.hstack([s2_p, s2_n], justify="start", gap=2)])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, PINK, WIDTH, norm_pdf, norm_sf, np, s2_n, s2_p, show2, thin):
    def _sim2():
        p, n, e = s2_p.value, int(s2_n.value), 1.55
        sd = np.sqrt(p * (100 - p) / n)
        ph = np.random.default_rng(8).binomial(n, p / 100, 10000) / n * 100
        half = max(6.0, 4 * sd)
        lo, hi = p - half, p + half
        step = 100 / n
        width = max(1, round(0.1 / step)) * step
        edges = p - step / 2 + width * np.arange(np.floor(-half / width), np.ceil(half / width) + 1)
        h, ed = np.histogram(ph, bins=edges, density=True)
        mid = (ed[:-1] + ed[1:]) / 2
        fig = Figure(figsize=(WIDTH, 3.4))
        ax = fig.subplots()
        ax.bar(mid, h, width=ed[1] - ed[0], color=[PINK if abs(m - p) > e else LIGHT for m in mid], edgecolor="white")
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
        ax.set_title(r"$p = %d\%%$, $n = %s$:  %.1f%% of the polls are red.  Same area under the curve: %.1f%%" % (p, thin(n), 100 * red, 200 * norm_sf(e / sd)), fontsize=12)
        fig.tight_layout()
        return fig

    _sim2() if show2.value else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (d) Use (c) to prove that for $n = 1\,000$,

    $$
    P(|\hat p_X - p| \leq 3.1\%) \geq 0.95,
    $$

    and find the smallest $n$ for which $P(|\hat p_X - p| \leq 1.55\%) \geq 0.95$. Compare with your guess in (a).

    Reminder: $z_{0.975} = 1.96$.

    (e) Use the law of large numbers to find an $n$ for which $P(|\hat p_X - p| \leq 1.55\%) \geq 0.95$. Compare it with the $n$ found in (d).

    LLN: for every $\varepsilon > 0$,

    $$
    P(|M_n - \mu| \geq \varepsilon) \leq \frac{1}{n}\frac{\sigma^2}{\varepsilon^2}.
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fa_p = mo.ui.slider(5, 95, 1, value=50, label="$p$ (%)", show_value=True)
    return (fa_p,)


@app.cell(hide_code=True)
def _(mo):
    showA = mo.ui.button(label="Show figure A", value=False, on_click=lambda _: True)
    return (showA,)


@app.cell(hide_code=True)
def _(fa_p, showA):
    # the figure stays hidden until its button is clicked
    showA if not showA.value else fa_p
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, WIDTH, fa_p, norm_sf, np, plain_axes, showA):
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
        for x, c, shown in ((n_clt, BLUE, round(n_clt, -1 if n_clt < 1e4 else -2)), (n_lln, RED, np.ceil(n_lln))):
            ax.plot([x, x], [0, 0.05], color=c, lw=1, ls=":")
            ax.plot(x, 0.05, "o", color=c, ms=5)
            ax.text(x, -0.07, "$%s$" % f"{int(shown):,}".replace(",", r"\,"), ha="center", va="top", fontsize=11, color=c)
        # each name sits beside its own curve
        clt_1000 = 2 * norm_sf(e * np.sqrt(1000) / np.sqrt(pq))
        ax.text(200, max(0.12, clt_1000 - 0.08), "central limit theorem", color=BLUE, fontsize=12, va="top")
        n_half = pq / (0.5 * e**2)
        ax.text(n_half * 1.25, 0.5, "law of large numbers bound", color=RED, fontsize=12, va="center")
        ax.set_xscale("log")
        ax.set_xlim(100, 1e5)
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("$n$", labelpad=14)
        ax.set_ylabel(r"$P(|\hat p_X - p| > 1.55\%)$", fontsize=13)
        plain_axes(ax)
        ax.set_title(r"$p = %d\%%$" % fa_p.value, fontsize=12)
        fig.tight_layout()
        return fig

    _figA() if showA.value else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2

    Voters are now chosen at random from a subgroup in which a fraction $r \neq p$ supports A. Let $Y_i = 1$ if the $i$-th voter supports A, and $Y_i = 0$ otherwise. The poll estimates $p$ by $\hat p_Y = \frac1n (Y_1 + \dots + Y_n)$.

    (a) For the poll of $1\,000$ voters in Question 1, the error $|\hat p_X - p|$ is at most $3.1\%$ with probability at least $0.95$. What is the probability that the error $|\hat p_Y - p|$ is at most $3.1\%$ when $r = p + 2\%$ and when $r = p + 4\%$, for $n = 1\,000$? Write down a guess.

    (b) Find the bias, the standard error and the mean squared error of $\hat p_Y$, and the limit of the mean squared error as $n \to \infty$.
    """)
    return


@app.cell(hide_code=True)
def _(POLLS, mo, repeat_button):
    s3_p = mo.ui.slider(5, 95, 1, value=30, label="$p$ (%)", show_value=True)
    s3_b = mo.ui.slider(0, 5, 1, value=2, label="$r - p$ (%)", show_value=True)
    s3_n = mo.ui.number(start=100, stop=1000000, step=1, value=1000, label="$n$")
    s3_k = mo.ui.slider(steps=POLLS, value=0, label="number of polls", show_value=True)
    s3_r = repeat_button()
    return s3_b, s3_k, s3_n, s3_p, s3_r


@app.cell(hide_code=True)
def _(mo):
    show3 = mo.ui.button(label="Show simulation 3", value=False, on_click=lambda _: True)
    return (show3,)


@app.cell(hide_code=True)
def _(mo, s3_b, s3_k, s3_n, s3_p, s3_r, show3):
    # the simulation stays hidden until its button is clicked
    show3 if not show3.value else mo.vstack([mo.md(r"""*Simulation 3.* Each dot is the $\hat p_Y$ of one poll of $n$ voters from the subgroup. A dot is red when its error $|\hat p_Y - p|$ is larger than $3.1\%$. The fraction of red dots estimates $P(|\hat p_Y - p| > 3.1\%)$. The dashed line is at $r$."""), mo.hstack([s3_p, s3_b, s3_n], justify="start", gap=2), mo.hstack([s3_k, s3_r], justify="start", gap=2)])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, LIGHT, RED, WIDTH, np, plain_axes, s3_b, s3_k, s3_n, s3_p, s3_r, show3, thin):
    def _sim3():
        p, b, n, k, e = s3_p.value, s3_b.value, int(s3_n.value), s3_k.value, 3.1
        r = p + b
        ph = np.random.default_rng(300 + s3_r.value).binomial(n, r / 100, 1000)[:k] / n * 100
        red = np.abs(ph - p) > e
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
        ax.text(xmax * 1.015, p, "$p$", va="center")
        ax.text(xmax * 1.015, r, "$r$", va="center")
        ax.text(xmax * 1.015, p + e, r"$p + 3.1\%$", va="center", fontsize=12)
        ax.text(xmax * 1.015, p - e, r"$p - 3.1\%$", va="center", fontsize=12)
        ax.set_xlim(0, xmax * 1.01)
        ax.set_ylim(min(p - 6, r - spread), max(p + 10, r + spread))
        ax.set_xlabel("poll")
        ax.set_ylabel(r"$\hat p_Y$ (%)")
        plain_axes(ax)
        top = r"$p = %d\%%$, $r = %d\%%$, $n = %s$" % (p, r, thin(n))
        if k:
            top += r":  %d of %d polls are red (%.0f%%)" % (red.sum(), k, 100 * red.mean())
        ax.set_title(top, fontsize=12)
        fig.tight_layout()
        return fig

    _sim3() if show3.value else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (c) Find the limit of $P(|\hat p_Y - p| \leq 3.1\%)$ as $n \to \infty$, when $r = p + 2\%$ and when $r = p + 4\%$. Is $\hat p_Y$ consistent for $p$?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fb_b = mo.ui.slider(0, 5, 1, value=2, label="$r - p$ (%)", show_value=True)
    return (fb_b,)


@app.cell(hide_code=True)
def _(mo):
    showB = mo.ui.button(label="Show figure B", value=False, on_click=lambda _: True)
    return (showB,)


@app.cell(hide_code=True)
def _(fb_b, showB):
    # the figure stays hidden until its button is clicked
    showB if not showB.value else fb_b
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, WIDTH, fb_b, np, plain_axes, showB):
    def _figB():
        p, b = 0.30, fb_b.value / 100
        r = p + b
        n = np.logspace(2, 6, 400)
        mse_y = r * (1 - r) / n + b**2
        mse_x = p * (1 - p) / n
        fig = Figure(figsize=(WIDTH, 3.8))
        ax = fig.subplots()
        ax.plot(n, mse_y, color=BLUE, lw=1.8)
        ax.plot(n, mse_x, color=RED, lw=1.8)
        if b > 0:
            ax.axhline(b**2, color=GREY, lw=1.2, ls="--")
            ax.text(1.2e6, b**2, "$(r - p)^2$", va="center", fontsize=12)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(100, 1e6)
        ax.set_ylim(1e-7, 4 * mse_y[0])
        ax.text(2e4, 1.8 * mse_y[-1], r"$\mathrm{MSE}(\hat p_Y)$", color=BLUE, fontsize=12)
        ax.text(1.3e5, 2.6 * p * (1 - p) / 1.3e5, r"$\mathrm{MSE}(\hat p_X)$", color=RED, fontsize=12)
        ax.set_xlabel("$n$")
        ax.set_ylabel("mean squared error")
        plain_axes(ax)
        ax.set_title(r"$p = %d\%%$, $r = %d\%%$" % (round(100 * p), round(100 * r)), fontsize=12)
        fig.tight_layout()
        return fig

    _figB() if showB.value else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3

    The poll of Question 1 runs a second time after a certain period. Between the two polls, the true fraction of all voters who support A might have changed from $p$ to $p'$. The change $d = p' - p$ can be estimated with two methods:

    1. Two independent groups of $n$ voters are asked, one in each poll.
    2. The same $n$ voters are asked in both polls.

    Let $U_i$ and $V_i$ be the answers of the $i$-th voter in the first and in the second poll with method 1, and $\tilde U_i$ and $\tilde V_i$ with method 2. Each answer is $1$ if the voter supports A, and $0$ otherwise. The answers $U_i$ and $V_i$ are independent, the joint pmf of $(\tilde U_i, \tilde V_i)$ is

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

    (a) Let $p = 30\%$, $a = 1\%$, $b = 4\%$ and $n = 1\,000$. Which estimator of $d$ has the smaller standard error, and how many times smaller is it? Write down a guess.

    (b) Find $\mathrm{Cov}(U_i, V_i)$ and $\mathrm{Cov}(\tilde U_i, \tilde V_i)$, and the bias and the standard error of $\hat d_{U,V}$ and of $\hat d_{\tilde U, \tilde V}$.
    """)
    return


@app.cell(hide_code=True)
def _(POLLS, mo, repeat_button):
    s4_p = mo.ui.slider(5, 95, 1, value=30, label="$p$ (%)", show_value=True)
    s4_a = mo.ui.slider(0, 30, 1, value=1, label="$a$ (%)", show_value=True)
    s4_b = mo.ui.slider(0, 30, 1, value=4, label="$b$ (%)", show_value=True)
    s4_n = mo.ui.number(start=100, stop=100000, step=1, value=1000, label="$n$")
    s4_k = mo.ui.slider(steps=POLLS, value=0, label="number of runs", show_value=True)
    s4_r = repeat_button()
    return s4_a, s4_b, s4_k, s4_n, s4_p, s4_r


@app.cell(hide_code=True)
def _(mo):
    show4 = mo.ui.button(label="Show simulation 4", value=False, on_click=lambda _: True)
    return (show4,)


@app.cell(hide_code=True)
def _(mo, s4_a, s4_b, s4_k, s4_n, s4_p, s4_r, show4):
    # the simulation stays hidden until its button is clicked
    show4 if not show4.value else mo.vstack([mo.md(r"""*Simulation 4.* Each dot is the estimate of $d$ from one run of both polls, with $n$ voters in each poll. The left panel uses method 1, and the right panel uses method 2. The solid line is at $d$. The standard deviation of the dots estimates the standard error of the estimator."""), mo.hstack([s4_p, s4_a, s4_b, s4_n], justify="start", gap=2), mo.hstack([s4_k, s4_r], justify="start", gap=2)])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, MaxNLocator, mo, np, plain_axes, s4_a, s4_b, s4_k, s4_n, s4_p, s4_r, show4, thin):
    def _sim4():
        p, a, b, n, k = s4_p.value / 100, s4_a.value / 100, s4_b.value / 100, int(s4_n.value), s4_k.value
        if a > p or b > 1 - p:
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

    _sim4() if show4.value else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (c) Answer the question in (a), and compare with your guess. For which $a$ and $b$ does $\hat d_{\tilde U, \tilde V}$ have the smaller standard error?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fc_p = mo.ui.slider(5, 95, 1, value=30, label="$p$ (%)", show_value=True)
    fc_d = mo.ui.slider(0, 5, 1, value=3, label="$d$ (%)", show_value=True)
    fc_n = mo.ui.number(start=100, stop=100000, step=1, value=1000, label="$n$")
    return fc_d, fc_n, fc_p


@app.cell(hide_code=True)
def _(mo):
    showC = mo.ui.button(label="Show figure C", value=False, on_click=lambda _: True)
    return (showC,)


@app.cell(hide_code=True)
def _(fc_d, fc_n, fc_p, mo, showC):
    # the figure stays hidden until its button is clicked
    showC if not showC.value else mo.hstack([fc_p, fc_d, fc_n], justify="start", gap=2)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, WIDTH, fc_d, fc_n, fc_p, mo, np, plain_axes, showC, thin):
    def _figC():
        p, d, n = fc_p.value / 100, fc_d.value / 100, int(fc_n.value)
        p2 = p + d
        if p2 > 1:
            return mo.md(r"$p + d$ must be at most $1$.")
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
            ax.text(100 * a0 - 0.5, 100 * se1[0] * 1.04, r"$\mathrm{Cov}(\tilde U_i, \tilde V_i) = 0$", ha="right", va="bottom", fontsize=12)
        ax.text(100 * amax * 1.01, 100 * se1[-1], r"$\mathrm{SE}(\hat d_{U,V})$", color=RED, va="center", fontsize=12)
        ax.text(100 * amax * 1.01, 100 * se2[-1], r"$\mathrm{SE}(\hat d_{\tilde U,\tilde V})$", color=BLUE, va="center", fontsize=12)
        ax.set_xlim(0, 100 * amax)
        ax.set_ylim(0, 100 * max(se1[0], se2[-1]) * 1.25)
        ax.set_xlabel("$a$ (%)")
        ax.set_ylabel("standard error (%)")
        plain_axes(ax)
        ax.set_title(r"$p = %d\%%$, $d = b - a = %d\%%$, $n = %s$" % (fc_p.value, fc_d.value, thin(n)), fontsize=12)
        fig.tight_layout()
        return fig

    _figC() if showC.value else None
    return


if __name__ == "__main__":
    app.run()

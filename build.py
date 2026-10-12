"""Build the BS202 course site: one browser-run page per lecture, plus an index.

Usage:  python build.py        (writes ./site)
Preview: python -m http.server --directory site
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
SITE = HERE / "site"

PARTS = [  # (name, first lecture, last lecture); ranges after part II are tentative
    ("I. Probability spaces and counting methods", 1, 3),
    ("II. Random variables and their distributions", 4, 13),
    ("III. Joint distributions and independence", 14, 16),
    ("IV. Random samples and sampling distributions", 17, 19),
    ("V. Estimation and hypothesis testing", 20, 25),
    ("VI. Simple linear regression", 26, 28),
]

TITLES = {  # lecture number -> title shown on the index
    1: "Probability basics",
    2: "Properties of probability; counting methods",
    3: "Conditioning, independence, and Bayes' rule",
    4: "Random variables",
    5: "Discrete random variables: pmf, cdf, expectation",
    6: "Binomial and negative binomial models",
    7: "Hypergeometric and negative hypergeometric models",
    8: "Poisson models",
    9: "Continuous random variables; gamma and exponential distributions",
    10: "Guided practice 1",
    11: "Expectations for continuous random variables; moment generating functions",
    12: "Uniform, beta and Gaussian distributions",
    13: "The standard normal distribution; functions of random variables; quantiles",
}

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BS202 Introduction to Probability and Mathematical Statistics</title>
<style>
  body {{ font-family: "Latin Modern Roman", "CMU Serif", Georgia, serif; color: #111; background: #fff;
         max-width: 46rem; margin: 0 auto; padding: 2rem 1rem; font-size: 1.1rem; line-height: 1.5; }}
  .title {{ color: #1b458f; font-weight: 700; font-size: 1.9rem; text-align: center; margin: 1rem 0 .3rem; }}
  .inst {{ color: #1b458f; text-align: center; font-size: 1.2rem; }}
  .meta {{ display: grid; grid-template-columns: auto 1fr auto 1fr; gap: .5rem 1.5rem; margin: 2rem 0;
          padding: 1rem 1.2rem; text-align: right; border-top: 1px solid #1b458f; border-bottom: 1px solid #1b458f; }}
  .meta b {{ text-align: left; }}
  h2 {{ font-size: 1.2rem; margin: 1.8rem 0 .4rem; }}
  ul {{ list-style: none; padding: 0; margin: 0; }}
  li {{ padding: .15rem 0; }}
  a {{ color: #1b458f; }}
  .none {{ opacity: .55; font-style: italic; }}
</style></head><body>
<div class="title">Introduction to Probability and Mathematical Statistics</div>
<div class="inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
<div class="meta"><b>Document</b><span>Lecture notes</span><b>Course</b><span>BS202a</span>
<b>Lectures</b><span>{count} available</span><b>Instructor</b><span>Professor Scarinci</span></div>
{parts}
</body></html>
"""


NAV_CSS = """<style>
  .bs-nav { position: fixed; left: 1.1rem; bottom: 1.1rem; z-index: 50; display: flex; gap: .35rem;
             font-family: "KaTeX_Main", "Latin Modern Roman", "CMU Serif", Georgia, serif; font-size: .9rem; }
  .bs-nav a { color: #1b458f; text-decoration: none; opacity: .45; padding: .25rem .55rem; border-radius: .3rem;
               background: rgba(255,255,255,.85); border: 1px solid rgba(27,69,143,.25); transition: opacity .15s; }
  .bs-nav a:hover { opacity: 1; }
  #root { padding-bottom: 3.5rem; }
  @media print { .bs-nav { display: none; } }
</style>"""


def nav_html(number, numbers):
    """Subtle previous / index / next links for the page of lecture `number`."""
    links = []
    if number - 1 in numbers:
        links.append(f'<a href="../Lecture_{number - 1:02d}/" title="Lecture {number - 1:02d}">&larr; {number - 1:02d}</a>')
    links.append('<a href="../" title="All lectures">Index</a>')
    if number + 1 in numbers:
        links.append(f'<a href="../Lecture_{number + 1:02d}/" title="Lecture {number + 1:02d}">{number + 1:02d} &rarr;</a>')
    return NAV_CSS + '<nav class="bs-nav">' + "".join(links) + "</nav>"


def main():
    notebooks = {}
    for path in sorted(HERE.glob("W*_Lecture_*.py")):
        number = int(re.search(r"Lecture_(\d+)", path.stem).group(1))
        notebooks[number] = path

    for number, path in notebooks.items():
        print(f"exporting {path.name}")
        subprocess.run(
            ["marimo", "export", "html-wasm", str(path), "-o", str(SITE / f"Lecture_{number:02d}"), "--mode", "run", "-f"],
            check=True,
            cwd=HERE,
        )

    for number in notebooks:  # previous / next navigation, injected into each exported page
        page = SITE / f"Lecture_{number:02d}" / "index.html"
        html = re.sub(r'<nav class="bs-nav">.*?</nav>', "", page.read_text(encoding="utf-8"), flags=re.S)
        html = html.replace("</body>", nav_html(number, notebooks) + "</body>", 1)
        page.write_text(html, encoding="utf-8")

    sections = []
    for name, first, last in PARTS:
        items = [
            f'<li><a href="Lecture_{n:02d}/">Lecture {n:02d}</a> &mdash; {TITLES.get(n, "")}</li>'
            for n in range(first, last + 1)
            if n in notebooks
        ]
        body = "<ul>" + "".join(items) + "</ul>" if items else '<div class="none">not yet available</div>'
        sections.append(f"<h2>{name}</h2>{body}")

    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(PAGE.format(count=len(notebooks), parts="\n".join(sections)), encoding="utf-8")
    (SITE / ".nojekyll").write_text("")
    print(f"wrote {SITE / 'index.html'}")


if __name__ == "__main__":
    main()

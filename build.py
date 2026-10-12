"""Build the BS202 course site: one browser-run page per lecture, plus an index.

Usage:  python build.py        (writes ./site)
Preview: python -m http.server --directory site
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SITE = HERE / "site"

PARTS = [  # (name, first lecture, last lecture)
    ("Lectures", 1, 28),
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


def main():
    notebooks = {}
    for path in sorted(HERE.glob("W*_Lecture_*.py")):
        number = int(re.search(r"Lecture_(\d+)", path.stem).group(1))
        notebooks[number] = path

    for number, path in notebooks.items():
        print(f"exporting {path.name}")
        subprocess.run(
            [sys.executable, "-m", "marimo", "export", "html-wasm", str(path), "-o", str(SITE / path.stem), "--mode", "run", "-f"],
            check=True,
            cwd=HERE,
        )

    sections = []
    for name, first, last in PARTS:
        items = [
            f'<li><a href="{notebooks[n].stem}/">Lecture {n:02d}</a> &mdash; {TITLES.get(n, "")}</li>'
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

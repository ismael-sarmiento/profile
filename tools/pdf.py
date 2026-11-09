#!/usr/bin/env python3
"""Writes the downloadable PDFs of IsProfile with headless Chrome, from the locally served site (css/print.css):

  ismael-sarmiento-cv.pdf           Spanish, light   (/profile/?pdf)
  ismael-sarmiento-cv-en.pdf        English, light   (/profile/?lang=en&pdf)
  ismael-sarmiento-cv-dark.pdf      Spanish, dark    (/profile/?pdf=dark)
  ismael-sarmiento-cv-en-dark.pdf   English, dark    (/profile/?lang=en&pdf=dark)

?pdf opens every "read more" and skips the intro (js/app.js, /assets/ds/intro.js); the PDF links of the page pick the
file of the language and theme shown (js/pdf.js). Run it after tools/build.py, with a folder
that has the portada at the root and this repository in profile/ served locally (the design system lives in /assets/ds/):

    python3 tools/pdf.py [http://127.0.0.1:8777/]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8777/').rstrip('/')

for name, query in (('ismael-sarmiento-cv.pdf', '?pdf'), ('ismael-sarmiento-cv-en.pdf', '?lang=en&pdf'),
                    ('ismael-sarmiento-cv-dark.pdf', '?pdf=dark'), ('ismael-sarmiento-cv-en-dark.pdf', '?lang=en&pdf=dark')):
    out = ROOT / name
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--hide-scrollbars',
                    '--virtual-time-budget=15000', f'--print-to-pdf={out}', f'{BASE}/profile/{query}'],
                   check=True, capture_output=True)
    print(f'wrote {out.name} ({out.stat().st_size // 1024} KB)')

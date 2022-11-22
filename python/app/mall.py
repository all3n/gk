import os
from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter
from PyPDF2 import PdfReader, PdfWriter
import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import sys


def merge(ifiles, out):
    pfm = PdfMerger()
    for f in ifiles:
        pfm.append(f)
    with open(out, 'wb') as of:
        pfm.write(of)

def main():
    for i in tqdm(os.listdir(".")):
        merge(i)

"""
python -m app.mall a1.pdf a2.pdf out.pdf
"""
if __main__ == '__main__':
    i, o = sys.argv[1:-1], sys.argv[-1]
    merge(i, o)

import os
from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter
from PyPDF2 import PdfReader, PdfWriter
import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tqdm import tqdm
import sys
import json



def add_page_numgers(pdf_path, newpath, start = 0, title = ""):
    """
    Add page numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    """
    tmp = "__tmp.pdf"

    n = 0
    writer = PdfWriter()
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        n = len(reader.pages)

        # create new PDF with page numbers
        create_page_pdf(n, tmp, start, title)

        with open(tmp, "rb") as ftmp:
            number_pdf = PdfReader(ftmp)
            # iterarte pages
            for p in range(n):
                page = reader.pages[p]
                number_layer = number_pdf.pages[p]
                # merge number page with actual page
                page.merge_page(number_layer)
                writer.add_page(page)

            # write result
            if len(writer.pages) > 0:
                with open(newpath, "wb") as f:
                    writer.write(f)
        os.remove(tmp)
    return n

def create_page_pdf(num, tmp, start = 0, title = ""):
    title = title.replace(".pdf", "").replace('"','')
    '''create tmp pdf that only include page number'''
    fonts_dir = os.environ["FONTS_DIR"]
    pdfmetrics.registerFont(
        TTFont('msyh', os.path.join(fonts_dir, 'microsoft-ya-hei.ttf')))
    c = canvas.Canvas(tmp)
    for i in range(num):
        c.setFont('msyh', 10)
        c.drawString((104)*mm, (4)*mm, str(start + i + 1))
        c.drawString((44)*mm, (9)*mm, title)
        c.showPage()
    c.save()


def merge(input_dir, output, tmp_dir):
    pfm = PdfMerger()
    start = 0
    outline = []
    jf = os.path.join(input_dir, "file.json")
    if os.path.exists(jf):
        with open(jf, "r") as f:
            info = json.loads(f.read())
            input_files = info["files"]
    else:
            input_files = sorted(os.listdir(input_dir))
    if os.path.isdir(input_dir):
        name=os.path.basename(input_dir)
        for f in tqdm(input_files, desc = name):
            tf = os.path.join(input_dir, f)
            try:
                t_out = os.path.join(tmp_dir, f)
                outline.append((f, start + 1))
                n = add_page_numgers(tf, t_out, start, f)
                start += n
                with open(t_out, "rb") as f:
                    pfm.append(f)
                os.remove(t_out)
            except PyPDF2.errors.PdfReadError as e:
                print(e, tf)

        with open(output, 'wb') as of:
            for (title, p) in outline:
                pfm.add_outline_item(title, p)
            pfm.write(of)


"""
merge pdf and add page number and info
"""
def main():
    input_dir=sys.argv[1]
    output = sys.argv[2]
    tmp_dir = sys.argv[3]
    merge(input_dir, output, tmp_dir)

main()

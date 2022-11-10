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
    pdfmetrics.registerFont(
        TTFont('msyh', './microsoft-ya-hei.ttf'))
    c = canvas.Canvas(tmp)
    for i in range(num):
        c.setFont('msyh', 10)
        c.drawString((104)*mm, (4)*mm, str(start + i + 1))
        c.drawString((44)*mm, (9)*mm, title)
        c.showPage()
    c.save()


def merge(i):
    tmp_dir = "tmp"
    pfm = PdfMerger()
    start = 0
    outline = []
    if os.path.isdir(i):
        for f in tqdm(sorted(os.listdir(i)), desc = i):
            tf = os.path.join(i, f)
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
    
        with open('merge_%s.pdf' % (i), 'wb') as of:
            for (title, p) in outline:
                pfm.add_outline_item(title, p)
            pfm.write(of)


def main():
    for i in tqdm(os.listdir(".")):
        merge(i)
#main()
#merge('hx')
#for i in sorted(os.listdir('hx')):
#    print(i)
merge(sys.argv[1])

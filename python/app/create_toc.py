import os
import sys
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.frames import Frame
from reportlab.platypus.tables import Table
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import cm
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_dir = os.environ["FONTS_DIR"]

pdfmetrics.registerFont(
        TTFont('msyh', os.path.join(font_dir, 'microsoft-ya-hei.ttf')))


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')])
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))



styles = getSampleStyleSheet()
nc = ParagraphStyle(name='Normal_CENTER',
                          parent=styles['Normal'],
                          fontName='msyh',
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontSize=33,
                          leading=33,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          )

title_style = styles['Heading1']
title_style.alignment = 1
title_style.fontName = 'msyh'

bd = PS(name = 'body',
fontSize = 14,
leading = 16, fontName = 'msyh')




toc = sys.argv[1]
title = sys.argv[2]
output = sys.argv[3]
story = []
story.append(Paragraph('<font size="33">%s</font>' % title, title_style))
story.append(PageBreak())
with open(toc, "r") as f:
    i = 1
    for line in f:
        a,b = line.strip().split()
        a = a.replace("\"", "").replace("立即下载：","").replace(".pdf", "")
        b = str(int(b) - 1)
        print(a, b)
        story.append(Paragraph('%d:%10s ---- %-10s' % (i, a,b), bd))
        i += 1

doc = MyDocTemplate(output)
doc.multiBuild(story)

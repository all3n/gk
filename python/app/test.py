import os
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.platypus.tables import Table
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.graphics.charts.textlabels import _text2Path

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

pt = PS(name = 'title', fontName = 'msyh',
fontSize = 24,
leading = 16)

h1 = PS(name = 'Heading1', fontName = 'msyh',
fontSize = 14,
leading = 16)
h2 = PS(name = 'Heading2',
fontSize = 12,
leading = 14)
# Build story.
story = []
toc = TableOfContents()
# For conciseness we use the same styles for headings and TOC entries
toc.levelStyles = [h1, h2]
#story.append(toc)
#story.append(PageBreak())
#story.append(Paragraph('First heading', h1))
#story.append(Paragraph('Text in first heading', PS('body')))
#story.append(Paragraph('First sub heading', h2))
#story.append(Paragraph('Text in first sub heading', PS('body')))
#story.append(PageBreak())
#story.append(Paragraph('Second sub heading', h2))
#story.append(Paragraph('Text in second sub heading', PS('body')))
#story.append(Paragraph('Last heading', h1))

#p=_text2Path('a min')



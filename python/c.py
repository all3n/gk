from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Spacer, SimpleDocTemplate, Table
import datetime

# 注册字体
msyh = "msyh"
msyhbd = "msyhbd"
song = "simsun"
pdfmetrics.registerFont(TTFont(song, "./simsun.ttc"))
pdfmetrics.registerFont(TTFont(msyh, "./microsoft-ya-hei.ttf"))
pdfmetrics.registerFont(TTFont(msyhbd, "./microsoft-ya-hei.ttf"))

PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]

def myFirstPage(c: Canvas, doc):
    c.saveState()
    # 设置填充色
    c.setFillColor(colors.orange)
    # 设置字体大小
    c.setFont(msyhbd, 30)
    # 绘制居中标题文本
    DrawPageInfo(c)
    drawUserInfoTable(c, 100, 100)
    c.drawCentredString(300, PAGE_HEIGHT - 80, "test")
    c.restoreState()

def DrawPageInfo(c: Canvas, date=datetime.date.today()):
    """绘制页脚"""
    # 设置边框颜色
    c.setStrokeColor(colors.dimgrey)
    # 绘制线条
    c.line(30, PAGE_HEIGHT - 790, 570, PAGE_HEIGHT - 790)
    # 绘制页脚文字
    c.setFont(song, 8)
    c.setFillColor(colors.black)
    d = date.strftime("%Y-%m-%d")
    c.drawString(30, PAGE_HEIGHT - 810, f"生成日期：{d}")

def drawUserInfoTable(c: Canvas, x, y):
    data = [["1", "df"],
            ["2", "fda"],
            ["3", "男"],
            ["3", 175],
            ["4", 65],
            ["5", 20]]
    t = Table(data, style={
        ("FONT", (0, 0), (-1, -1), msyhbd, 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ('ALIGN', (1, 0), (1, -1), 'CENTER')
    })
    t._argW[1] = 200
    t.wrapOn(c, 0, 0)
    t.drawOn(c, x, y)


def myLaterPages(c: Canvas, doc):
    c.saveState()
    c.restoreState()


# 创建文档
doc = SimpleDocTemplate("output/pdftest.pdf")
Story = [Spacer(1, 2 * inch)]
# 保存文档
doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

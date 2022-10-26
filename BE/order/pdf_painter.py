import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


def draw_centered_text(canvas: Canvas, x: float, y: float, text: str):
    lines = text.splitlines()

    widths = [pdfmetrics.stringWidth(line, canvas._fontname, canvas._fontsize) for line in lines]

    width = max(widths)

    text_obj = canvas.beginText(x, y)

    for line, w in zip(lines, widths):
        offset = (width - w) / 2
        text_obj.setXPos(offset)
        text_obj.textLine(line)
        text_obj.setXPos(-offset)

    canvas.drawText(text_obj)


def draw_image(canvas: Canvas, x: float, y: float, img: ImageReader, size_factor: float = 1):
    w, h = img.getSize()

    w *= size_factor
    h *= size_factor

    canvas.drawImage(img, x, canvas._pagesize[1] - h - y, w, h)


def draw_images(canvas: Canvas, h: float, x0: float, img_logo: ImageReader, img_help: ImageReader):
    canvas.saveState()
    canvas.transform(1, 0, 0, -1, 0, h)

    logo_x, logo_y = 175, 90
    logo_size_factor = 0.75
    draw_image(canvas, logo_x + x0, logo_y, img_logo, logo_size_factor)

    help_size_factor = 0.40
    draw_image(canvas, logo_x + img_logo.getSize()[0] * logo_size_factor - img_help.getSize()[0] * help_size_factor + x0, 480, img_help, help_size_factor)

    canvas.restoreState()

    lw, lh = img_logo.getSize()

    return (logo_x, logo_y), (lw * logo_size_factor, lh * logo_size_factor)


def format_phone_number(phone: str):
    clean = re.sub(r'[^0-9]+', '', phone)

    length = len(clean)

    if length == 10 or length == 12:
        tail = f'{clean[-7:-4]} {clean[-4:-2]} {clean[-2:]}'
        if length == 12:
            return f'+{clean[:3]} {clean[-9:-7]} {tail}'
        else:
            return f'({clean[0]}{clean[-9:-7]}) {tail}'
    else:
        return phone


class FormFieldPainter:
    def __init__(self, canvas: Canvas, title_x: float, first_line_x: float, later_lines_x: float, lines_end_x: float, leading: float, lines_offset: float, font: str, font_size: float):
        self.canvas = canvas
        self.title_x = title_x
        self.x0 = first_line_x
        self.x1 = later_lines_x
        self.x2 = lines_end_x
        self.leading = leading
        self.lines_offset = lines_offset
        self.style = ParagraphStyle('FormFieldText', fontName=font, fontSize=font_size,
                                    leading=leading, firstLineIndent=first_line_x - later_lines_x)

        self.font = font, font_size

        face = pdfmetrics.getFont(font).face

        self.font_h = (face.ascent - face.descent) * font_size / 1_000

    def draw(self, name: str, y: float, lines_count: int, text: str):
        self.canvas.setFont(*self.font)
        self.canvas.drawString(self.title_x, y, name)

        p = Paragraph(text, self.style)
        w, h = p.wrap(self.x2 - self.x0, availHeight=None)
        p.drawOn(self.canvas, self.x1, y + self.leading - h)

        y += self.lines_offset

        self.canvas.line(self.x0, y, self.x2, y)

        for i in range(lines_count - 1):
            y += self.leading
            self.canvas.line(self.x1, y, self.x2, y)


class ReportPainter:
    def __init__(self, file, img_logo: ImageReader, img_help: ImageReader):
        self.canvas = Canvas(file, (pagesize := A4[::-1]), bottomup=0)
        self.pagesize = pagesize

        self.img_logo = img_logo
        self.img_help = img_help

        self.canvas.setTitle('Замовлення')

        bk = 'BayraktarKharkiv'
        self.canvas.setAuthor(bk)
        self.canvas.setCreator(bk)
        self.canvas.setProducer(bk)

        self.font_franklin_i = 'Franklin Italic'
        self.font_corsiva = 'Corsiva'

        pdfmetrics.registerFont(TTFont(self.font_franklin_i, 'assets/framdit.ttf'))
        pdfmetrics.registerFont(TTFont(self.font_corsiva, 'assets/Mtcorsva.ttf'))

        self.font_size_big = 30
        self.font_size_medium = 16

        self.page = 1

    def __enter__(self):
        return self

    def draw_report(self, order_number: str, district: str, contact: str, phone_number: str, address: str, people: int, comment: str):
        canvas = self.canvas
        w, h = self.pagesize

        w /= 2

        font_main = self.font_franklin_i
        font_glory = self.font_corsiva

        font_size_big = 21
        font_size_medium = 11

        if self.page % 2:
            if self.page > 1:
                canvas.showPage()

            x0 = 0
        else:
            x0 = w

        font_franklin_i_face = pdfmetrics.getFont(font_main).face
        font_franklin_i_big_h = (font_franklin_i_face.ascent - font_franklin_i_face.descent) * font_size_big / 1_000
        font_franklin_i_medium_h = (font_franklin_i_face.ascent - font_franklin_i_face.descent) * font_size_medium / 1_000

        logo_pos, logo_size = draw_images(canvas, h, x0, self.img_logo, self.img_help)

        canvas.setFont(font_main, 13)
        canvas.drawCentredString(logo_pos[0] + logo_size[0] / 2 + x0, logo_pos[1] + logo_size[1], "ВО «БАЙРАКТАР ХАРКІВ»")

        x = 20 + x0

        canvas.setFont(font_main, font_size_medium)
        canvas.drawString(x, logo_pos[1] + logo_size[1] / 2, "ЗАКАЗ")
        canvas.drawString(x, logo_pos[1] + logo_size[1] / 2 + font_franklin_i_medium_h, f'№{order_number}')

        # TODO escape XML
        ff_painter = FormFieldPainter(canvas, x, 135 + x0, 160 + x0, w - 35 + x0, font_franklin_i_big_h * 1.1, 2, font_main,
                                      font_size_big)

        ff_painter.draw("РАЙОН", 65, 1, district)
        ff_painter.draw("КОНТАКТ", 235, 2, f'{contact}<br/>{format_phone_number(phone_number)}')
        ff_painter.draw("АДРЕСА", 300, 2, address)
        ff_painter.draw("ЛЮДЕЙ", 365, 1, str(people))
        ff_painter.draw("КОМЕНТАР", 430 - ff_painter.leading, 3, comment)

        canvas.setFont(font_main, font_size_medium)
        draw_centered_text(canvas, x, 460, "Пишіть нам:\nу дірект Інстаграму\n@bayraktar.kharkiv\n"
                                           "в Телеграм\n@bayraktarkharkiv\n\n"
                                           "Телефон гарячої лінії\n+380 96 268 64 58")

        canvas.setFont(font_glory, font_size_big)
        canvas.drawCentredString(w / 2 + x0, h - 15, 'СЛАВА УКРАЇНІ')

        self.page += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.canvas.save()

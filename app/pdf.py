from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import qrcode



start = {"rapport": (84, 842 - 218), "date": (48, 842 - 237), "auteur": (10, 842 - (279 + 17)),
         "victime": (10, 842 - (349 + 17)), "enquete": (81, 842 - 416), "remarque_enquete": (8, 842 - 480),
         "remarque_photo": (401, 842 - 660)}


def main_pdf(value, path, dest = "report.pdf"):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    for k in start:
        if k == "remarque_photo":
            list_phrase = value[k]
            for i,f in enumerate(list_phrase):
                can.drawString(start[k][0], start[k][1]-(i*12), f)
        else:
            can.drawString(start[k][0], start[k][1],value[k] )
    can.drawInlineImage(path[1], 211, 842 - 567, height=365, width=365)
    can.drawInlineImage(path[0], 213, 842 - 803, height=170, width=170)
    can.drawInlineImage(path[2], 515, 842 - (6+70), height=70, width=70)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open("police.pdf", "rb"))
    output = PdfWriter()
    output.add_metadata(
        {
            "/Author": "Group ZERO",
        }
    )
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    output_stream = open(dest, "wb")
    output.write(output_stream)
    output_stream.close()

def make_qr(id):
    img = qrcode.make(f"BLABLABLA LIEN vers la database avec l'id : {id}")
    img.save('qr_code.png')



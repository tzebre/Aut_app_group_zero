from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import uuid
import random
import string

def rdm_le(x, bool):
    if bool:
        return random.choice(string.ascii_uppercase)[:x]
    else:
        return random.choice(string.ascii_lowercase)[:x]

start = {"rapport" : (82, 842-218), "date" : (46, 842-237), "auteur":(10, 842-(279+17)), "victime":(10, 842-(349+17)), "enquete":(81, 842-415),"remarque_enquete":(8, 842-480),"remarque_photo":(401, 842-660)}
value = {"rapport" : f"{rdm_le(1,True)}{str(uuid.uuid4())[:3]}{rdm_le(1,False)}{str(uuid.uuid4())[:4]}", "date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "auteur": "JACKIE ricard", "victime":"QUENTIN DUVERT", "enquete":"XXXXX","remarque_enquete":"blablablabla","remarque_photo":"blablablabla"}
def set_value(what, val):
    value[what] = val

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=A4)
for k in start:
    can.drawString(start[k][0], start[k][1], value[k])

can.drawInlineImage("etst.png", 211,842-567, height=365, width=365)
can.drawInlineImage("etst.png", 214,842-803, height=170, width=170)
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader(open("police.pdf", "rb"))
output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
output_stream = open("destination.pdf", "wb")
output.write(output_stream)
output_stream.close()
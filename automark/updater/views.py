from django.shortcuts import render
from django.core.files.storage import default_storage
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from pandas.io.parsers import read_csv
from email.mime.image import MIMEImage
from PIL import Image, ImageDraw, ImageFont
# Create your views here.

def index(request):
    return render(request, "input.html")


def main(request):
    names = str(request.POST['names'])
    emails = str(request.POST['emails'])
    marks = str(request.POST['marks'])
    names = names.split("\r\n")
    emails = emails.split("\r\n")
    marks = marks.split("\r\n")

    email = str(request.POST['email'])
    password = str(request.POST['password'])
    course = str(request.POST['course'])
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = emails
    

    fnt = ImageFont.truetype('Garamond.ttf', 40) 
    fnt2 = ImageFont.truetype('Garamond.ttf', 18)
    fnt3 = ImageFont.truetype('Garamond.ttf', 24)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    for i in range(len(names)):
        message = f"""Dear {names[i]} and Parent/Guardian,

    Attached please find your {course} Final Mark for Quadmester 4 of the 2020-21 academic year.
    It has been completed in accordance with Ministry of Education directives.
    """

        msg = MIMEMultipart()
        template = Image.open('Report_Card.jpg')
        displayNames = ImageDraw.Draw(template)
        displayNames.text((100, 140), names[i], font=fnt, fill=(0, 0, 0), anchor = 'mm')
        displayNames.text((107, 248), course, font=fnt3, fill=(0,0,0), anchor = 'mm')
        displayNames.text((263, 253), str(marks[i]), font=fnt2, fill = (0,0,0), anchor = 'mm')
        name = 'Report_Card ' + str(names[i]) + '.png'
        template.save(name, 'PNG')
        
        with open(name, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)
        msg['Subject'] = "Final Mark"
        # Attach the message to the MIMEMultipart object
        msg.attach(MIMEText(message, 'plain'))
        text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
        server.sendmail(email, str(emails[i]), text)
        print('done',emails[i])
        
    server.close
    return render(request, "result.html")
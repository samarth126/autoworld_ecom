
# Importing Required Module
from reportlab.pdfgen import canvas
from datetime import date

today = date.today()

def pdff(response,c_name,o_id,pd,total,phone,qnt):
    # orer_id,product_name, qunatity, T_price
    # Creating Canvas
    c = canvas.Canvas(response,pagesize=(200,250),bottomup=0)

    # Logo Section
    # Setting th origin to (10,40)
    c.translate(10,40)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    c.drawImage(".\static\img\logo.png",0,0,width=50,height=30)

    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10,-40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold",10)
    # Inserting the name of the company
    c.drawCentredString(125,20,"BHARAT AUTOWORLD")
    # For under lining the title
    c.line(70,22,180,22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold",5)
    c.drawCentredString(125,30," 279, Transport Nagar, ")
    c.drawCentredString(125,35,"Indore, Madhya Pradesh 452014")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold",6)
    c.drawCentredString(125,42,"GSTIN :23GXZPS7573E1ZJ")

    # Line Seprating the page header from the body
    c.line(5,45,195,45)

    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold",8)
    c.drawCentredString(100,55,"TAX-INVOICE")

    # This Block Consist of Costumer Details
    c.roundRect(15,63,170,40,10,stroke=1,fill=0)
    c.setFont("Times-Bold",5)

    c.drawRightString(70,70,"ORDER ID :")
    c.drawRightString(105,70, str(o_id) )

    c.drawRightString(70,80,"DATE :")
    c.drawRightString(105,80,str(today))

    c.drawRightString(70,90,"CUSTOMER NAME :")
    c.drawRightString(105,90,c_name)

    c.drawRightString(70,100,"PHONE No. :")
    c.drawRightString(105,100,str(phone))

    # This Block Consist of Item Description
    c.roundRect(15,108,170,130,10,stroke=1,fill=0)
    c.line(15,120,185,120)

    c.drawCentredString(25,118,"SR No.")
    c.drawCentredString(25,130,"1")


    c.drawCentredString(75,118,"GOODS DESCRIPTION")
    x=130
    for i in pd:
        c.drawCentredString(75,x,str(i))
        x=x+10

    c.drawCentredString(125,118,"RATE")
    c.drawCentredString(125,130,"--")

    c.drawCentredString(148,118,"QTY")
    c.drawCentredString(148,130,str(qnt))

    c.drawCentredString(173,118,"TOTAL")
    c.drawCentredString(173,130,str(total))

    # Drawing table for Item Description
    c.line(15,210,185,210)
    c.line(35,108,35,220)
    c.line(115,108,115,220)
    c.line(135,108,135,220)
    c.line(160,108,160,220)

    # Declaration and Signature
    c.line(15,220,185,220)
    c.line(100,220,100,238)
    c.drawString(20,225,"We declare that above mentioned")
    c.drawString(20,230,"information is true.")
    c.drawString(20,235,"(This is system generated invoice)")
    c.drawRightString(180,235,"Authorised Signatory")

    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()
    return response
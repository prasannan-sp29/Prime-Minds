from django.shortcuts import render,redirect
from pagesapp.forms import reg_form
from pagesapp.models import register_user
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


# Create your views here.

def index(request):
    
    if request.method=='POST':
        form = reg_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['fullname']
            form.save()

            return redirect('user_view',name)
    else:
        form = reg_form()
    return render(request,'register.html',{'form':form})

def user_view(request,name):
    data = register_user.objects.all()
    return render(request,'view.html',{'data':data,'name':name})


# def download_pdf(request):
#     users = register_user.objects.all()

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="user_list.pdf"'

#     p = canvas.Canvas(response, pagesize=letter)

#     p.drawString(300, 700, 'User List')

#     data = [["Full Name", "Username"]]
#     for user in users:
#         data.append([user.fullname, user.username])

#     table = Table(data)
#     table_style = TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
#     ])
#     table.setStyle(table_style)

#     # table_width, table_height = table.wrap(1400, 1600)
#     # table.drawOn(p, (letter[0] - table_width) / 2, 600 - table_height)

#     table.wrapOn(p,600,800)
#     table.drawOn(p,250,550)


#     p.showPage()
#     p.save()

#     return response

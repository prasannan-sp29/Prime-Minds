import io
import logging
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .forms import *

# Configure logging
logger = logging.getLogger(__name__)

def generate_pdf(data):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Name: {data['name']}")
    p.drawString(100, 730, f"Email: {data['email']}")
    p.drawString(100, 710, f"Message: {data['message']}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def my_form_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            if request.GET.get('download'):
                logger.info("Data received successfully!")
                # Generate the PDF
                pdf_buffer = generate_pdf(form.cleaned_data)
                return FileResponse(pdf_buffer, as_attachment=True, filename='form_data.pdf')
            else:
                # Handle the normal form submission here
                # pass
                form.save()
    else:
        form = MyForm()
    return render(request, 'my_form_template.html', {'form': form})


def create_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food_item_list')  # Redirect to a list of food items or another appropriate view
    else:
        form = FoodItemForm()

    return render(request, 'create_food_item.html', {'form': form})
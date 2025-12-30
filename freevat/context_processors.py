from .models import Category, Format, Software

# Umožní přístup k datům z databáze ve všech šablonách
def global_data(request):
    return {
        'categories': Category.objects.all().order_by('name'),
        'formats': Format.objects.all().order_by('name'),
        'software_list': Software.objects.all().order_by('name'),
    }

from .models import Category, Format, Software

# Umožní přístup k datům z databáze ve všech šablonách
def global_data(request):
    return {
        "categories": Category.objects.all(),
        "formats": Format.objects.all(),
        "software_list": Software.objects.all(),
    }

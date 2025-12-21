from .models import Category


# Zpřístupnění všech kategorií ve všech šablonách
def categories_processor(request):
    return {'categories': Category.objects.all().order_by('name')}

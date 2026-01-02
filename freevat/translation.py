from modeltranslation.translator import register, TranslationOptions
from .models import Category

# Pro překlad kategorií
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
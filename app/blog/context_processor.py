from .models import Category

def category_navbar(request):
    return {
        "category": Category.objects.filter(status=True)
    }
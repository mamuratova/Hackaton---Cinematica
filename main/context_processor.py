from .models import Genre


def get_category(request):
    categories = Genre.objects.all()
    return {'categories': categories}


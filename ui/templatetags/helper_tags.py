from django import template

register = template.Library()

@register.filter(is_safe=True)
def hash(h, key):
    return h[key]

@register.filter(is_safe=True)
def s(items):
    items = [str(i) for i in items]
    return ', '.join(items)

movie_categories = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                      'Fantasy', 'Film_Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci_Fi', 'Thriller', 'War',
                      'Western', 'unknown']

@register.filter(is_safe=True)
def get_movie_categories(items):
    categories = []
    items = items.objects.all()
    items = list(items)
    print(items)
    print(items)
    for i in movie_categories:
        if items[i]==1:
            categories.append(i)

    return ', '.join(categories)
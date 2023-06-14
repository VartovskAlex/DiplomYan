# для отоброжения разделов в навбаре (в base.html)
from app.models import Section

def navbar(request):
    sections = Section.objects.all() # берем все разделы
    return {'navbar_sections': sections} # помещаем в словарь


# https://ustimov.org/posts/18/ - гайд
from django.template.response import TemplateResponse


def demo_home(request):
    return TemplateResponse(template="demo/home.html", request=request)

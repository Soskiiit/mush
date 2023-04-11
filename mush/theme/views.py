from django.views.generic.base import TemplateView


class BaseView(TemplateView):
    template_name = 'theme/test-form.html'

from django.views.generic.base import TemplateView


class ItemEditView(TemplateView):
    template_name = 'catalog/item-edit.html'


class ItemDetailsView(TemplateView):
    template_name = 'catalog/item-details.html'

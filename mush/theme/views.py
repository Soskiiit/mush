from django.views.generic.base import TemplateView


is_model_ready = 1
is_user_the_owner = 1


class ItemEditView(TemplateView):
    template_name = 'catalog/item-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For debug purposes only
        local_context = {
            'model_ready': is_model_ready,
            'is_user_the_owner': is_user_the_owner,
        }
        context.update(local_context)
        return context


class ItemDetailsView(TemplateView):
    template_name = 'catalog/item-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For debug purposes only
        local_context = {
            'model_ready': is_model_ready,
            'is_user_the_owner': is_user_the_owner,
        }
        context.update(local_context)
        return context

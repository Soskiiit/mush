from django.views.generic.base import TemplateView


is_model_ready = 1
is_user_the_owner = 1


class ProfileView(TemplateView):
    template_name = 'users/profile.html'


class SignupView(TemplateView):
    template_name = 'theme/test-form.html'


class MyProjectsView(TemplateView):
    template_name = 'catalog/my-projects.html'


class CatalogView(TemplateView):
    template_name = 'catalog/index.html'


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

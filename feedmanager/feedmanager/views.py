from django.views import generic

from feeds.models import Feed


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_list'] = Feed.objects.all()
        return context

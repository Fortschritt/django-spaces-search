from django.apps import AppConfig
from django.core.urlresolvers import reverse_lazy
from django.db.models import Model, Q
from django.views.generic.edit import FormView
from spaces.models import SpacePluginRegistry

from .forms import SearchForm

"""
die plugins krieg ich ja aus der registry.
"""

class ContextMixin(object):
    """
        Adds 
        * The name of this plugin
    """
    def get_context_data(self, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['plugin_selected'] = 'search'
        return context


class SearchView(ContextMixin, FormView):
    template_name = "spaces_search/search.html"
    form_class = SearchForm
    success_url = reverse_lazy("spaces_search:search")
    search_results = None

    def form_valid(self, form, **kwargs):
        search_terms = form.cleaned_data["search_terms"]
        context = self.get_context_data(form=form, **kwargs)
        context["results"] = self.search(search_terms)
        return self.render_to_response(context)

    def search(self, search_terms):
        """ the actual database searching """
        search_terms = search_terms.split(" ")
        plugins = SpacePluginRegistry.get_plugins()
        results = []
        space = self.request.SPACE
        for plugin in plugins:
            if plugin.searchable_fields is None:
                continue
            model, fields = plugin.searchable_fields
            complete_query = None
            for term in search_terms:
                partial_query = None
                for field_name in fields:
                    q = Q(**{"%s__icontains" % field_name: term})
                    if partial_query is None:
                        partial_query = q
                    else:
                        partial_query = partial_query | q
            if complete_query is None:
                complete_query = partial_query
            else:
                complete_query = complete_query & partial_query
            if complete_query is not None:
                partial_result = model.objects.in_space(space).filter(complete_query)
                results.append({'plugin': plugin, 'queryset': partial_result})
        prepared_results = []
        for item in results:
            for result in item['queryset']:
                obj = {
                    'title': result,
                    'link': result.get_absolute_url(),
                    'plugin': item['plugin']
                }
                prepared_results.append(obj)

        return prepared_results


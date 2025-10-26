# marathon_analytics/views.py

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result

import math
import plotly
import plotly.graph_objs as go

class ResultsListView(ListView):
    '''View to display marathon results.'''

    model = Result
    template_name = 'marathon_analytics/results.html'
    context_object_name = 'results'
    paginate_by = 25 # how many records per page

    def get_queryset(self):
        '''limit the result query (for now).'''
        results = super().get_queryset()
        # return results[:25] # slice to only return

        # look for URL parameters to filter by:
        if 'city' in self.request.GET:
            city = self.request.GET['city']

            if city:
                results = results.filter(city=city)

        return results
    
class ResultDetailView(DetailView):
    '''Display the results for a single runner.'''

    model = Result
    context_object_name = 'r' # short for runner
    template_name = 'marathon_analytics/result_detail.html'

    def get_context_data(self, **kwargs):
        '''Provide context variables for template.'''
        context = super().get_context_data()
        r = context['r']

        # create a graph of first half/second half time as pie chart
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second

        x = ['first_half_seconds', 'second_half_seconds']
        y = [first_half_seconds, second_half_seconds]

        fig = go.Pie(labels=x, values=y)
        title_text = 'Half Marathon Splits (in seconds)'

        graph_div_splits = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text},
                                                auto_open=False,
                                                output_type="div")
        
        context["graph_div_splits"] = graph_div_splits

        # create a bar chart with count of runners passed/passed by
        x = [f'Runners Passed by {r.first_name}',
             f'Runners who Passed {r.first_name}'] 
        y = [r.get_runners_passed(),
                  r.get_runners_passed_by()]
        print(Result.objects.all())
        print(f"y: {y}")

        
        fig2 = go.Bar(x=x, y=y)
        title_text = "Runners Passed/Passed By"
        graph_div_passed = plotly.offline.plot({"data": [fig2],
                                                "layout_title_text": title_text},
                                                auto_open=False,
                                                output_type="div")

        context['graph_div_passed'] = graph_div_passed
        return context
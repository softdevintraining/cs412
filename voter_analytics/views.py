# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/31/2025
# Description: Views file which handles requests to voter_analytics/

from django.shortcuts import render

from django.views.generic import ListView, DetailView
from . models import Voter
from datetime import date
import urllib.parse

import math
import plotly
import plotly.graph_objs as go

# Create your views here.

class ShowVotersView(ListView):
    model = Voter
    template_name = "voter_analytics/show_all_voters.html"
    context_object_name = "voters"

    paginate_by = 100 # determine the amount of voter records to show per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        # creates a distinct QuerySet of all possible parties
        unique_parties = Voter.objects.values_list( 
            'party_affiliation', flat=True).distinct()
        
        # creates a distinct QuerySet of all possible voter scores
        unique_scores = sorted(Voter.objects.values_list( 
            'voter_score', flat=True).distinct())
        
        # creates a QuerySet housing all date of birth attributes
        dates = list(Voter.objects.values_list('date_of_birth', flat=True))
        sorted_dates = []

        # creates a list containing the unique years of birth of the voters
        for d in range(0, len(dates)):
            dates[d] = dates[d].year
            if dates[d] not in sorted_dates:
                sorted_dates.append(dates[d])
            else:
                continue

        sorted_dates = sorted(sorted_dates) # sorts them

        # putting these values into context
        context["parties"] = unique_parties
        context["scores"] = unique_scores
        context["dates"] = sorted_dates
        context["address"] = ""
 
        return context

    def get_queryset(self):
        '''Defines the query set context that is used by our template.'''
        voters = super().get_queryset()

        # Look for URL parameters to filter by if they exist
        if 'party' in self.request.GET:
            party_affiliation = self.request.GET['party']
            if party_affiliation:
                if (len(party_affiliation) != 2):
                    voters = voters.filter(party_affiliation=party_affiliation.strip()+" ")
                else:
                    voters = voters.filter(party_affiliation=party_affiliation)

        if 'min_dob' in self.request.GET:
            min_year = self.request.GET['min_dob']
            if min_year:
                min_date = date(int(min_year), 1, 1)
                voters = voters.filter(date_of_birth__gte=min_date)

        if 'max_dob' in self.request.GET:
            max_year = self.request.GET['max_dob']
            if max_year:
                max_date = date(int(max_year), 12, 31)
                voters = voters.filter(date_of_birth__lte=max_date)

        if 'score' in self.request.GET:
            score = self.request.GET['score']
            if score:
                voters = voters.filter(voter_score=int(score))

        if 'v20state' in self.request.GET:
            voted = self.request.GET['v20state']
            if voted == 'TRUE':
                voters = voters.filter(v20state="TRUE")
        
        if 'v21town' in self.request.GET:
            voted = self.request.GET['v21town']
            if voted == 'TRUE':
                voters = voters.filter(v21town="TRUE")
        
        if 'v21primary' in self.request.GET:
            voted = self.request.GET['v21primary']
            if voted == 'TRUE':
                voters = voters.filter(v21primary="TRUE")
        
        if 'v22general' in self.request.GET:
            voted = self.request.GET['v22general']
            if voted == 'TRUE':
                voters = voters.filter(v22general="TRUE")
        
        if 'v23town' in self.request.GET:
            voted = self.request.GET['v23town']
            if voted == 'TRUE':
                voters = voters.filter(v23town="TRUE")

        return voters

class VoterDetailView(DetailView):
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        voter = self.get_object()
        address = f"{voter.street_number} {voter.street_name} #{voter.apartment_number}, Newton, MA" 

        context["address"] = urllib.parse.quote(address, safe='')
        return context

    def get_object(self, queryset = ...):
        '''Return the Voter object we are currently viewing.'''
        return Voter.objects.get(pk=self.kwargs['pk'])
    
class ShowGraphsView(ListView):
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_context_data(self, **kwargs):
        '''Define the context for this view.'''
        context = super().get_context_data()

        # grab voters in context, with searches applied if there is one
        voters = self.get_queryset() 

        # this is used to display sample size in our graphs
        num_objects = len(voters.all())

        years = []
        num_born_this_year = []
        
        # Define context variables for our search form
        unique_parties = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context["parties"] = unique_parties

        represented_parties = voters.values_list('party_affiliation', flat=True).distinct()
        party_members = [] 

        unique_scores = sorted(Voter.objects.values_list('voter_score', flat=True).distinct())
        context["scores"] = unique_scores
        
        dates = list(Voter.objects.values_list('date_of_birth', flat=True))
        sorted_dates = []

        for d in range(0, len(dates)):
            dates[d] = dates[d].year
            if dates[d] not in sorted_dates:
                sorted_dates.append(dates[d])
            else:
                continue

        sorted_dates = sorted(sorted_dates)

        context["dates"] = sorted_dates

        # Grab party affiliations of voters resulting from the search
        for p in represented_parties:
            party_members.append(len(voters.filter(party_affiliation=p)))

        # Grab number of voters from the serach that voted in each election
        election_labels = [ 
            'v20state', 
            'v21town', 
            'v21primary', 
            'v22general', 
            'v23town', 
        ]
        election_count = [
            len(voters.filter(v20state="TRUE")),
            len(voters.filter(v21town="TRUE")),
            len(voters.filter(v21primary="TRUE")),
            len(voters.filter(v22general="TRUE")),
            len(voters.filter(v23town="TRUE")),
        ]

        # create a list of the unique years of birth of voters from the search
        dates = list(voters.values_list('date_of_birth', flat=True))
        for d in range(0, len(dates)):
            dates[d] = dates[d].year
            if dates[d] not in years:
                years.append(dates[d])
            else:
                continue

        years = sorted(years) # sort these years
        
        # Grab the number of voters born in each year in the above list
        for y in years:
            min = date(int(y), 1, 1)
            max = date(int(y), 12, 31)
            num_born_this_year.append(
                len(voters.filter(
                    date_of_birth__gte=min,
                    date_of_birth__lte=max
                )))
            
        # Create graphs to display year, party, and election distribution info
        # and put them into context to be displayed in the template
        fig = go.Bar(x=years, y=num_born_this_year)
        title_text = f'Voter distribution by Year of Birth n={num_objects}'

        graph_year_distribution = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text},
                                                auto_open=False,
                                                output_type="div")
        
        context['graph_year_distribution'] = graph_year_distribution

        fig = go.Pie(labels=list(represented_parties), values=party_members)
        title_text = f'Voter distribution by Party Affiliation n={num_objects}'

        graph_party_affiliation = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text},
                                                auto_open=False,
                                                output_type="div")
        
        context['graph_party_affiliation'] = graph_party_affiliation

        fig = go.Bar(x=election_labels, y=election_count)
        title_text = f'Vote Count by Election n={num_objects}'

        graph_election_count = plotly.offline.plot({"data": [fig],
                                                "layout_title_text": title_text},
                                                auto_open=False,
                                                output_type="div")
        
        context['graph_election_count'] = graph_election_count

        return context
    
    def get_queryset(self):
        '''Defines the query set context that is used by our template.'''
        voters = super().get_queryset()

        # Look for URL parameters to filter by if they exist
        if 'party' in self.request.GET:
            party_affiliation = self.request.GET['party']
            if party_affiliation:
                if (len(party_affiliation) != 2):
                    voters = voters.filter(party_affiliation=party_affiliation.strip()+" ")
                else:
                    voters = voters.filter(party_affiliation=party_affiliation)

        if 'min_dob' in self.request.GET:
            min_year = self.request.GET['min_dob']
            if min_year:
                min_date = date(int(min_year), 1, 1)
                voters = voters.filter(date_of_birth__gte=min_date)

        if 'max_dob' in self.request.GET:
            max_year = self.request.GET['max_dob']
            if max_year:
                max_date = date(int(max_year), 12, 31)
                voters = voters.filter(date_of_birth__lte=max_date)

        if 'score' in self.request.GET:
            score = self.request.GET['score']            
            if score:
                voters = voters.filter(voter_score=int(score))

        if 'v20state' in self.request.GET:
            voted = self.request.GET['v20state']
            if voted == 'TRUE':
                voters = voters.filter(v20state="TRUE")
        
        if 'v21town' in self.request.GET:
            voted = self.request.GET['v21town']
            if voted == 'TRUE':
                voters = voters.filter(v21town="TRUE")
        
        if 'v21primary' in self.request.GET:
            voted = self.request.GET['v21primary']
            if voted == 'TRUE':
                voters = voters.filter(v21primary="TRUE")
        
        if 'v22general' in self.request.GET:
            voted = self.request.GET['v22general']
            if voted == 'TRUE':
                voters = voters.filter(v22general="TRUE")
        
        if 'v23town' in self.request.GET:
            voted = self.request.GET['v23town']
            if voted == 'TRUE':
                voters = voters.filter(v23town="TRUE")

        return voters
# blog/views.py
# views for the blog applicaiton
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse

import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display a single article.'''

    model = Article
    template_name = "blog/article.html"
    context_object_name ="article" # note the singular variable name

class RandomArticleView(DetailView):
    '''Display a single article selected at randnom.'''
    model = Article
    template_name = "blog/article.html"
    context_object_name ="article" # note the singular variable name

    # methods
    def get_object(self):
        '''return one instance of the Article object selected at random'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article

# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm

    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''Override the default method to add some debug infomration.'''

        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        return super().form_valid(form)

class CreateCommentView(CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # create and return a URL
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variabels for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # find/add the article to the context dictionary
        context['article'] = article
        return context

    def form_valid(self, form, request):
        '''This method handles the form submission and save the
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''

        print(form.cleaned_data)
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateArticleView(UpdateView):
    '''View class to handle update of an article based on its PK.'''
    
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
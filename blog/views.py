# blog/views.py
# views for the blog applicaiton
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## for auth
from django.contrib.auth.forms import UserCreationForm ## for creating a new user
from django.contrib.auth.models import User

import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the disaptch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in')

        return super().dispatch(request, *args, **kwargs)

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
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm

    template_name = "blog/create_article_form.html"

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        return reverse('login')

    def form_valid(self, form):
        '''Override the default method to add some debug infomration.'''

        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        # find the logged in user 
        user = self.request.user
        print(f'CreateArticleView.form_valid(): {user}')
        
        # attach this user to the form instance (to the article object)
        form.instance.user = user

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

class DeleteCommentView(DeleteView):
    '''View class to delete a comment on an Article.'''

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        '''Return the URL to redirect to after a succesful delete.'''

        # find the PK for this comment
        pk = self.kwargs['pk']
        # find the Comment object:
        comment = Comment.objects.get(pk=pk)

        # find the PK of the article
        article = comment.article

        return reverse('article', kwargs={'pk':article.pk})
    
class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new user.'''
    template_name = "blog/register.html"
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''The url to redirect to after creating a new user.'''
        return reverse('login')
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.models import User
from django.views.generic import (
                                View,
                                ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView
                                )   

from .models import Post, PostView, Category 

from .forms import CommentForm, PostForm

class BlogSearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if not query:
            queryset = Post.objects.none()
        else:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) 
        ).distinct()

        context = {
            'queryset': queryset
        }
        return render(request, 'blog/BlogSearchResult.html', context)

class Dashboard(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_dashboard_items'] = Post.objects.filter(
                                            author=self.request.user).order_by(
                                            '-date_posted')
        return context
 

class BlogPostListView(ListView):
    model = Post
    template_name = 'blog/Baseblog.html' 
    context_object_name = 'posts' 
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BlogPostListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the categories__title and categories__title__count
        context['category_list'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        context['most_recent'] = Post.objects.order_by('?')[:4]
        context['mainblog'] = 'active'

        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_related_post.html' 
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_related_post.html'
    context_object_name = 'ByCategorysPost' 
    paginate_by = 8

    def get_queryset(self):
        self.category = get_object_or_404(Category, title=self.kwargs.get('title'))
        return Post.objects.filter(categories__title=self.category)
    
    def get_context_data(self, **kwargs):
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        context['category_list'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        context['most_recent'] = Post.objects.order_by('?')[:4]
        return context

class BlogPostDetailView(DetailView):
    model = Post
    template_name = "blog/blog_post_detail.html"
    form = CommentForm()
    query_pk_and_slug = True


    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        context['category_list'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        context['most_recent'] = Post.objects.order_by('-date_posted')[:4]
        context['form'] = self.form        
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk,
                'slug': post.slug
            }))
     
 
class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'categories', 'thumbnail', 'content']
    form_class = PostForm
    template_name = "blog/blog_new_post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'categories', 'thumbnail', 'content']
    template_name = "blog/blog_new_post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        # check to make sure that the current user is author of the post 
        if self.request.user == post.author:
            return True
        return False


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/dashboard/'
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        # check to make sure that the current user is author of the post 
        if self.request.user == post.author:
            return True
        return False
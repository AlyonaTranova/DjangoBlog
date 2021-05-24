from django.views import View, generic

from .models import Post, Comment
from django.views.generic import TemplateView

from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib import messages

from .models import Post
from .forms import PostForm, CommentForm

from .models import Post, Comment


class Main(View):
    template_name = 'blog/main_page.html'

    def get(self, request):
        return render(request, self.template_name)


class PostListView(generic.ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['commentform'] = CommentForm()
        return context

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments_form = CommentForm(request.POST)
        new_comment = None
        if comments_form.is_valid():
            new_comment = comments_form.save(commit=False)
            new_comment.news = post
            new_comment.save()
            return HttpResponseRedirect(str(post.pk))
        return render(request, 'blog/post_detail.html')

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.increment_view_count()
        return item


class PostFormView(View):

    def get(self, request):
        news_form = PostForm()
        return render(request, 'blog/register.html', context={'news_form': news_form})

    def post(self, request):
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            Post.objects.create(**post_form.cleaned_data)
            messages.add_message(request, messages.INFO, 'Пост создан')
            return HttpResponseRedirect('register')
        return render(request, 'blog/register.html', context={'post_form': post_form})


class PostEditFormView(View):
    def get(self, request, profile_id):
        post = Post.objects.get(id=profile_id)
        post_form = PostForm(instance=post)
        messages.add_message(request, messages.INFO, 'Пост отредактирован')
        return render(request, 'blog/edit.html', context={'post_form': post_form, 'profile_id': profile_id})

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.increment_view_count()
        return item


class About(View):
    template_name = 'blog/about.html'

    def get(self, request):
        return render(request, self.template_name)

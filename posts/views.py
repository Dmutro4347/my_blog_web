from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Post, Category, Comment


# def index(request):
#     newest_post = Post.objects.latest('created_at')
#     posts = Post.objects.order_by('-created_at')[1:]
#     categories = Category.objects.all()
#     return render(request, "main/index.html", {"posts": posts, "newest_post": newest_post, "categories": categories})
#
#
# def post_detail(request, slug):
#     post = Post.objects.get(slug=slug)
#     categories = Category.objects.all()
#     comments = Comment.objects.filter(post=post)
#
#     paginator = Paginator(comments, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     if request.method == "POST":
#         comment_text = request.POST.get('text')
#         Comment.objects.create(content=comment_text, post=post, author=request.user)
#     return render(request, "posts/post.html", {"post": post, "categories": categories, "comments": comments})
#
#
# def category_detail(request, slug):
#     category = Category.objects.get(slug=slug)
#     posts = Post.objects.filter(category=category).order_by('-created_at')
#     categories = Category.objects.all()
#
#     return render(request, "posts/category_posts.html", {"posts": posts, "category": category, "categories": categories})

class CommonDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context


class IndexView(CommonDataMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "main/index.html"
    paginate_by = 3
    ordering = ["-created_at"]

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")[1:]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["newest_post"] = Post.objects.all().latest("created_at")

        return context


class PostDetailView(CommonDataMixin, DetailView):
    model = Post
    slug_field = "slug"
    context_object_name = 'post'
    template_name = "posts/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.get_object())

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_text = request.POST.get('text')
        if comment_text:
            Comment.objects.create(
                content=comment_text,
                post=self.object,
                author=request.user
            )
        return redirect('post_detail', slug=self.object.slug)


class CategoryDetailView(CommonDataMixin, ListView):
    model = Post
    template_name = "posts/category_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context



# Create your views here.from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from .filters import NewsFilter
from .forms import PostForm
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from NewsPaper.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import login_required



class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news/news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['numPost'] = len(Post.objects.all())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

class NewsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'

class PostAdd(CreateView):
    template_name = 'news/add.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter.py'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostEdit(UpdateView):
    template_name = 'news/edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    template_name = 'new/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'


class PostCategory(ListView):
    model = Post
    template_name = 'post_category.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        cat = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCategory=cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        context['category'] = category
        return context


@login_required
def subscribe_to_category(request: object, pk: object) -> object:
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject='Уведомление о подписке',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)

    return redirect('/sign')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from .models import Post, Subscription, Category
from .forms import NewsForm, ArticleForm
from .filters import ProductFilter



class NewsList(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

        
    
class NewsDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'news'

    
    
class NewsCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'News_edit.html'
    
    def form_valid(self, form):
        product = form.save(commit=False)
        product.category_type = 'NW'
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'News_edit.html'
    
    
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    
class ArticleCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ArticleForm
    model = Post
    template_name = 'News_edit.html'
    
    def form_valid(self, form):
        product = form.save(commit=False)
        product.category_type = 'AR'
        return super().form_valid(form)
    
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
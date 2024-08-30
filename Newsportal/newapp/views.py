from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import NewsForm, ArticleForm
from .filters import ProductFilter
from django.urls import reverse_lazy


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

    
    
class NewsCreate(CreateView):
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
    
class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'News_edit.html'
    
    def form_valid(self, form):
        product = form.save(commit=False)
        product.category_type = 'AR'
        return super().form_valid(form)
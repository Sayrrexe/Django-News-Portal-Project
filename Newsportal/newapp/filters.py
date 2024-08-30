from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from django.forms import DateInput
from .models import Post, Category


class ProductFilter(FilterSet):
    post_category = ModelChoiceFilter(queryset=Category.objects.all(), label='Категория')
    date_creation = DateFilter(
            field_name='date_creation',
            lookup_expr='gte',
            label='Дата после',
            widget=DateInput(attrs={'type': 'date'}))
    class Meta:
       model = Post
       fields = {
           # поиск по названию
           'title': ['icontains'],
        }
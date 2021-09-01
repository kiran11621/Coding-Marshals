import django_filters 
from django_filters import CharFilter

from .models import QuestionMake

# for applying problem_list filter
class ProblemsFilter(django_filters.FilterSet):

    tags=CharFilter(field_name="tags",lookup_expr='icontains',label="Tags")
    problem_name=CharFilter(field_name="problem_name",lookup_expr='icontains',label='Problem')
    difficulty=CharFilter(field_name="difficulty",lookup_expr='icontains',label="Diffculty")
    class Meta:
        model = QuestionMake
        fields = ['problem_name','tags','difficulty']
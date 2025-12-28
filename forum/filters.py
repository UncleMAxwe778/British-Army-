import django_filters
from django.db.models import Q

class PrivateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='by_name_filter')

    def by_name_filter(self, queryset, name, value):
        if value:
            value = value.strip()
            return queryset.filter(
                Q(first_name_private__icontains=value) |
                Q(last_name_private__icontains=value))
        else:
            return queryset.none()
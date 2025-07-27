from django_filters import rest_framework as filters
from .models import Message


class MessageFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte')
    end_date = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte')
    conversation = filters.NumberFilter(field_name='conversation__id')
    sender = filters.NumberFilter(field_name='sender__id')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date']

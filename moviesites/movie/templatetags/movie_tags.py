from django import template
from django.db.models.aggregates import Count

from ..models import MGenre

register = template.Library()


@register.simple_tag
def get_tags():
	return MGenre.objects.annotate(num_posts=Count('id')).filter(num_posts__gt=0)
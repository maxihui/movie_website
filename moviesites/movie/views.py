from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import MInformation,MGenre
# Create your views here.


class IndexView(ListView):
	model = MInformation
	template_name = 'movie/index.html'
	context_object_name = 'info_list'
	paginate_by = 12  # 设置每页个数

	def get_context_data(self, *, object_list=None, **kwargs):
		"""
		重写获取内容数据方法，添加分页操作
		"""

		context = super().get_context_data(object_list=None, **kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		paginate_data = self.paginate_data(paginator, page, is_paginated)
		context.update(paginate_data)
		return context

	def paginate_data(self, paginator, page, is_paginated):
		"""
		根据配置信息，编写分页逻辑
		is_paginated 判断是否分页
		page 获取页面数量
		paginator 获取页面信息
		"""
		if not is_paginated:
		    return {}
		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		page_num = page.number
		total_page = paginator.num_pages
		page_range = paginator.page_range

		if page_num == 1:
			right = page_range[page_num:page_num + 2]
			if right[-1] < total_page - 1:
				right_has_more = True
			if right[-1] < total_page:
				last = True
		elif page_num == total_page:
			left = page_range[(page_num - 3) if (page_num - 3) > 0 else 0:page_num - 1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			right = page_range[page_num:page_num + 2]
			if right[-1] < total_page - 1:
				right_has_more = True
			if right[-1] < total_page:
				last = True
			left = page_range[(page_num - 3) if (page_num - 3) > 0 else 0:page_num - 1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		data = {
			'left': left,
			'left_has_more': left_has_more,
			'right': right,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}
		return data


class PostDetailView(DetailView):
	model = MInformation
	template_name = 'movie/detail.html'
	context_object_name = 'info'


class TagView(IndexView):
	model = MInformation
	template_name = 'movie/index.html'
	context_object_name = 'info_list'

	def get_queryset(self):
		tag = get_object_or_404(MGenre, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(mtype=tag)
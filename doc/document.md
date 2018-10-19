###  开发文档

1. 搭建环境

	```
	mkdir movie_web
	cd movie_web
	python -m venv myvenv
	myvenv\Scripts\activate
	pip install django==2.0.9
	```

2. 创建项目

	django-admin startproject moviesite

3. 修改配置

	```
	moviesite/settings.py
	LANGUAGE_CODE = 'zh-hans' # 中文语言
	TIME_ZONE = 'Asia/Shanghai'  # 添加时区
	```

4. 运行测试

	python manage.py runserver

5. 添加应用
	
	```
	django-admin startapp movie
	moviesite/settings.py
	INSTALLED_APPS = (
		'movie'
	)
	`# python manage.py runserver`
	```


6. 添加数据库
	
	```
	moviesite/settings.py
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	        'HOST': 'localhost',
	        'PORT': '3306',
	        'NAME': 'imdb',
	        'USER': 'root',
	        'PASSWORD': '12345678',
	    }
	}
	---
	movie/models.py
	---
	python manage.py makemigrations
	python manage.py migrate
	```

7. 添加后台应用

	```
	movie/admin.py
	from django.contrib import admin
	from .models import MInformation, MGenre
	#
	`# Register your models here.`
	class MinformationAdmin(admin.ModelAdmin):
		list_display = ['title', 'sorce', 'id', 'img', 'summary']
	#
	admin.site.register(MInformation, MinformationAdmin)
	admin.site.register(MGenre)
	---
	python manage.py createsuperuser
	```

8. 添加视图

	```
	movie/views.py 
	movie/urls.py 
	movie/template/movie/index.html
	movie/template/movie/detail.html
	movie/static/movie/css/movie.css
	movie/static/movie/js
	movie/static/movie/image
	---
	moviesite/settings.py 
	TEMPLATES = [
	    {
	    	...
	        'DIRS': [os.path.join(BASE_DIR, 'templates')],
	    	...
	    },
	]
	#
	STATIC_URL = '/static/'
	#
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 添加静态文件路径
	```

9. 添加自定义模板

	```
	movie/templatetags/movie_tags.py
	movie/templatetags/__init__.py
	```

10. 提交代码

	```
	需要在github上先建立一个空项目，获取代码提交地址address
	git init
	git add --all .
	git commit -m 'first commit'
	git remote add origin address
	git pull --rebase origin master # 创建项目时如果添加了readme需要添加这条命令，因为本地没有readme文件
	git push -u origin master
	```

11. 再次提交

	```
		git status # 查看状态
		git add --all .
		git status # 查看状态
		git commit -m "changed the html for the site"
		git push
	```

12. 服务器下载代码，并部署环境

	```
	mkdir movie.plumcandy.site # 创建项目文件 
	cd movie.plumcandy.site
	git clone address 
	virtualenv --python=python3.4 myvenv # 创建虚拟环境 
	source bin myvenv/bin/activate # 进入虚拟环境
	deactivate # 退出虚拟环境
	pip install django==1.8 # django 
	pip install pymysql # 数据库支持
	pip install gunicorn # 自动部署
	```

13. 数据库支持

	```
	# 由于ubantu不能直接支持MySQLdb,需要用pymysql中转
	moviesites/__init__.py
	import pymysql
	pymysql.install_as_MySQLdb()
	```

14. 添加域名解析

	使用的域名必须经过解析才能够正常使用

15. 配置服务

	```
	/etc/nginx/sites-available/movie.plumcandy.site 
	server {
	    charset utf-8;
	    listen 80;
	    server_name movie.plumcandy.site;
	    root /home/maxhi/sites/movie.plumcandy.site/movie_sites/moviesites/movie/templates/movie;
	    index index.html index.htm;
	    location /static {
	        alias /home/maxhi/sites/movie.plumcandy.site/movie_sites/moviesites/static;
	    }
	    location / {
	        proxy_set_header Host $host;
	        proxy_pass http://unix:/tmp/movie.plumcandy.site.socket;
	    }
	}
	```

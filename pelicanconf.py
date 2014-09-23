#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'zhang liyong'
SITENAME = u"Lyon's Blog"
RELATIVE_URLS = True
SITEURL = 'http://zhangliyong.github.io'

TIMEZONE = 'Asia/Shanghai'

USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_DATE = 'fs'
FEED_DOMAIN = 'http://zhangliyong.github.io'
FEED_ALL_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

THEME = "../pelican-elegant"


ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'

PLUGIN_PATHS = ["../pelican-plugins"]
PLUGINS = ['pelican_gist', 'sitemap', 'neighbors', 'extract_toc', 'tipue_search']
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
DIRECT_TEMPLATES = (('index', 'tags', 'archives', 'search', '404'))
STATIC_PATHS = ['theme/images', 'images']
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}


DEFAULT_LANG = u'en'

GITHUB_URL = 'https://github.com/zhangliyong/'
DISQUS_SITENAME = "lyonhappyblog"
GOOGLE_ANALYTICS = 'UA-48307158-1'

# Blogroll
LINKS = (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
         ('Python.org', 'http://python.org'),
         ('Jinja2', 'http://jinja.pocoo.org'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('Twitter', 'https://twitter.com/zhangliyong'),
    ('Github', 'https://github.com/zhangliyong'),
    ('Email', 'mailto:lyzhang87@gmail.com'),
)

DEFAULT_PAGINATION = 10


LANDING_PAGE_ABOUT = {
    "title": "I'm a software engineer, mainly focus on web backend",
    "details": u'''
软件攻城师一位，主要从事 Web 后端开发，常用语言为 Python，也有一定 JAVA, C的基础，主要涉及到Linux系统知识，Nginx, MongoDB, redis等，个人对函数编程及Linux系统知识感兴趣。热爱生活。平时喜欢读书，种类比较杂。

<br />
<br />
Contact:
<pre>
{
    Name: Zhang Liyong, 
    Github: <a href="https://github.com/zhangliyong">zhangliyong</a>,
    Twitter: <a href="https://twitter.com/zhangliyong">@zhangliyong</a>,
    E-mail: lyzhang87 at gmail,
}</pre>
    ''',
}

PROJECTS = [
    {
        'name': 'dash-docsets',
        'url': 'https://github.com/zhangliyong/dash-docsets',
        'description': 'Generate docsets for dash on MacOSX'
    },
]

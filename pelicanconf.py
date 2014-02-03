#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'zhang liyong'
SITENAME = u"Lyon's Blog"
RELATIVE_URLS = True
SITEURL = 'http://zhangliyong.github.io'

TIMEZONE = 'Europe/Paris'

USE_FOLDER_AS_CATEGORY = True
DEFAULT_DATE = 'fs'
DEFAULT_CATEGORY = 'misc'
FEED_DOMAIN = 'http://zhangliyong.github.io'
FEED_ALL_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

static_PATHS = ['images']

THEME = "pelican-elegant-1.3"

DEFAULT_LANG = u'en'

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

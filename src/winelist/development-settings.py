# -*- coding: utf-8 -*-
""" DEVELOPMENT SETTINGS """

try:
    from settings import *
except ImportError as e:
    pass

""" import all prod setting except this """ 

DEBUG = True

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}
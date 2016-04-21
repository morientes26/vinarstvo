# -*- coding: utf-8 -*-
from fabric.api import local


def test(module="inventory"):
	""" run unit tests """
	suffix = ".tests"
	local("./manage.py test "+module+suffix)


def bootsrap():
	""" setup application, download frontend dependences """
	""" it is importent to have installed 'npm' """
	local("sudo npm install -g bower")
	local("./manage.py bower_install")


def localization():
	""" build localization en, sk """
	local("./manage.py makemessages -l sk")
	local("./manage.py makemessages -l en")
	local("./manage.py compilemessages -l sk")
	local("./manage.py compilemessages -l en")


def migrate():
	""" make migrations and run migrations """
	local("./manage.py makemigrations")
	local("./manage.py migrate")


def run():
	""" run on local development server """
	local("./manage.py runserver")


def run_gn():
	""" run on local production server """
	local("gunicorn winelist.wsgi")


#def create_virtualenv_remote():
#    """ setup virtualenv on remote host """
#    require('virtualenv_root', provided_by=('staging', 'production'))
#    args = '--clear --distribute'
#    run('virtualenv %s %s' % (args, env.virtualenv_root))
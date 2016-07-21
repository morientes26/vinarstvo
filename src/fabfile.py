# -*- coding: utf-8 -*-
import os
import subprocess
from fabric.api import local, run, env, put

# host setting
env.hosts = ['winary.tpsoft.sk']
env.user = "root"
#env.password =

# application setting
app_port = 8000


def health():
	""" Ping production server """
	print('pinging server: ' + env.hosts[0])
	run("ps -ef|grep " + str(app_port))


def install():
	""" setup application, download frontend dependences """
	if not is_app_installed("nodejs"):
		local("sudo apt-get install nodejs")
	if not is_app_installed("npm"):
		local("sudo apt-get install npm")
	if not is_app_installed("bower"):
		local("sudo npm install -g bower")
	local("./manage.py bower_install")


def test(module="inventory"):
	""" run unit tests """
	suffix = ".tests"
	local("./manage.py test "+module+suffix + " --settings=winelist.development-settings")


def localization():
	""" build localization en, sk """
	local("./manage.py makemessages -l sk --settings=winelist.development-settings")
	local("./manage.py makemessages -l en --settings=winelist.development-settings")
	local("./manage.py compilemessages -l sk --settings=winelist.development-settings")
	local("./manage.py compilemessages -l en --settings=winelist.development-settings")


def static():
	""" build localization en, sk """
	local("./manage.py collectstatic")


def migrate():
	""" make migrations and run migrations """
	local("./manage.py makemigrations --settings=winelist.development-settings")
	local("./manage.py migrate --settings=winelist.development-settings")


def run_server():
	""" run on local development server """
	local("echo '\n--- DEVELOPMENT MODE ---\n'")
	local("./manage.py runserver 0.0.0.0:8888 --settings=winelist.development-settings")


def run_gn_server():
	""" run on local production server """
	local("echo '\n--- PRODUCTION MODE ---\n'")
	local("gunicorn winelist.wsgi")


def is_app_installed(app):
	try:
		subprocess.call([app])
		return True
	except OSError as e:
		if e.errno == os.errno.ENOENT:
			print(app + " has to be installed")
		else:
			print("Something else went wrong while trying to run `%s`", app)
		return False


#def create_virtualenv_remote():
#    """ setup virtualenv on remote host """
#    require('virtualenv_root', provided_by=('staging', 'production'))
#    args = '--clear --distribute'
#    run('virtualenv %s %s' % (args, env.virtualenv_root))

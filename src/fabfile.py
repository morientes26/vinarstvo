# -*- coding: utf-8 -*-
import os
import subprocess
from fabric.api import local, run, env, put, sudo, cd
from time import gmtime, strftime
import winelist

# host setting
env.hosts = ['winary.tpsoft.sk']
env.user = "root"
env.password = "Tekvica82"

# application setting
app_port = 8000
app_name = "winary"
#app_path = "/data/winary/"
app_path = "/data/backups/test"
app_backup = "/data/backups/"

#app_local_path = "/home/morientes/Work/tp-soft/winecart/"   
app_local_path = "/home/morientes/Work/tp-soft/winecart"  


def health():
	""" Ping production server """
	print('pinging server: ' + env.hosts[0])
	run("ps -ef|grep " + str(app_port))
	run("systemctl status dev-appserver.service")


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


def deploy_to_test():
	# Stop test server
	#stop_test_server()

	# Create backup
	#datestring = strftime("%Y%m%d%H%M%S", gmtime())
	#path = app_backup + datestring
	#sudo("mkdir " + path)
	#with cd(path):
	#	run("echo 'backup version: " + winelist.__version__ + "' > backup.info")
	#	run("tar zcvf "+ app_name + ".tar.gz " + app_path)

	# Deploy to server
	#run("rsync -a " + app_local_path +" " + env.user + "@" + env.hosts[0] + ":" + app_path + "/")
	put(app_local_path, app_path, mode=774)
	run("chown -R django:django "+app_path)	

	# Start test server
	#start_test_server()


def start_test_server():
	run("systemctl start dev-appserver.service")

def stop_test_server():
	run("systemctl stop dev-appserver.service")
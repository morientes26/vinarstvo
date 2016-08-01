# -*- coding: utf-8 -*-
import os
import subprocess
from fabric.api import local, run, env, put, sudo, cd, get
from time import gmtime, strftime
import winelist, os

# host setting
env.hosts = ['winary.tpsoft.sk']
env.user = "root"
env.password = "Tekvica82"

# application setting
app_port = 8000
app_name = "winary"
app_path = "/data/winary/"
app_backup = "/data/backups/"
tmp = "/tmp/"

base_path = os.path.dirname(os.path.realpath(__file__))

app_local_path = "./"
local_tmp = "/tmp/" 


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
	local(base_path+"/manage.py bower_install")


def test(module="inventory"):
	""" run unit tests """
	suffix = ".tests"
	local(base_path +"/manage.py test "+module+suffix + " --settings=winelist.development-settings")


def localization():
	""" build localization en, sk """
	local(base_path + "/manage.py makemessages -l sk --settings=winelist.development-settings")
	local(base_path + "/manage.py makemessages -l en --settings=winelist.development-settings")
	local(base_path + "/manage.py compilemessages -l sk --settings=winelist.development-settings")
	local(base_path + "/manage.py compilemessages -l en --settings=winelist.development-settings")


def static():
	""" build localization en, sk """
	local(base_path + "/manage.py collectstatic")


def migrate():
	""" make migrations and run migrations """
	local(base_path + "/manage.py makemigrations --settings=winelist.development-settings")
	local(base_path + "/manage.py migrate --settings=winelist.development-settings")


def run_server():
	""" run on local development server """
	local("echo '\n--- DEVELOPMENT MODE ---\n'")
	local(base_path + "/manage.py runserver 0.0.0.0:8000 --settings=winelist.development-settings")


def run_gn_server():
	""" run on local production server """
	local("echo '\n--- PRODUCTION MODE ---\n'")
	local("gunicorn winelist.wsgi")


def logging(message, filename):
	run("echo $(date) " + message + " >> " + filename)

def deploy_to_test():
	datestring = strftime("%Y%m%d%H%M%S", gmtime())
	path = app_backup + datestring
	sudo("mkdir " + path)
	log = path+"/deploy.log"

	logging('Start deploying process', log)

	# Create backup
	with cd(path):
		run("echo 'backup version: " + winelist.__version__ + "' > backup.info")
		run("tar zcvf "+ app_name + ".tar.gz " + app_path)
	logging('Created backup', log)

	# Prepare release
	with cd(app_local_path):
		local("git archive --format=tar --prefix="+app_name+"/ HEAD | (cd "+local_tmp+" && tar xf -)")
	logging('Release prepared', log)

	# Deploy to server
	put(local_tmp + app_name, tmp)	

	# Stop test server
	stop_test_server()
	logging('Stop application server', log)

	run("yes | cp -rf "+tmp + app_name+ "/* " + app_path)
	
	run("chmod -R 774 " + app_path)
	run("chown -R django:django " + app_path)

	logging('Release deployed', log)

	with cd(app_path):
		run("virtualenv env")
		run("source env/bin/activate")
		run("pip install -r requirements.txt")
	logging('Application environments initialized', log)

	# Start test server
	start_test_server()
	logging('Server is running', log)
	
	logging('End deploying process', log)


def start_test_server():
	run("systemctl start dev-appserver.service")

def stop_test_server():
	run("systemctl stop dev-appserver.service")

def download_test_db():
	get(app_path + "db.sqlite3", "../backup/db.sqlite3")
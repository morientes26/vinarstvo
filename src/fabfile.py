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
app_path = "/data/winary/"
app_backup = "/data/backups/"
tmp = "/tmp/"

#app_local_path = "/home/morientes/Work/tp-soft/winecart/"   
app_local_path = "/home/morientes/Work/tp-soft/winecart"  
release_local_tmp = "/home/morientes/Work/tp-soft/release_tmp" 


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
		local("git archive --format=tar --prefix="+app_name+"/ HEAD | (cd "+release_local_tmp+" && tar xf -)")
	logging('Release prepared', log)

	# Deploy to server
	put(release_local_tmp + "/" + app_name, tmp)
	run("chmod -R 774 "+tmp)
	run("chown -R django:django "+tmp)	

	# Stop test server
	#stop_test_server()
	#logging('Stop application server', log)

	#run("yes | cp -rf "+tmp + app_name+ "/winelist/ "+app_path)
	run("yes | cp -rf "+tmp + app_name+ "/winelist/ /data/backups/test/winary/")

	logging('Release deployed', log)

	#with cd(app_path):
	with cd("/data/backups/test/winary/"):
		run("virtualenv env")
		run("source env/bin/activate")
		run("pip install -r requirements.txt")
	logging('Application environments initialized', log)

	# Start test server
	#start_test_server()
	#logging('Server is running', log)
	
	logging('End deploying process', log)


def start_test_server():
	run("systemctl start dev-appserver.service")

def stop_test_server():
	run("systemctl stop dev-appserver.service")
from fabric.api import local

def test(module="inventory"):
	""" run unit tests """
	suffix = ".tests"
	local("./manage.py test "+module+suffix)

def bootsrap():
	""" setup application, download frontend dependences """
	print("not implemented yet")


def run():
	""" run develop server """
	local("./manage.py runserver")

def create_virtualenv_remote():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--clear --distribute'
    run('virtualenv %s %s' % (args, env.virtualenv_root))
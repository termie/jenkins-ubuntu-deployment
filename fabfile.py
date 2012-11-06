
import fabric
from fabric.api import run, cd, env, sudo

env.hosts = ['ec2-184-73-4-10.compute-1.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = '/home/alan/awspem/projectfixup.pem'


def setup_machine():
    run('wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -')
    sudo('sudo sh -c "echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list"')
    sudo('apt-get update')
    sudo('apt-get -y install jenkins')
    sudo('apt-get -y install git')
    sudo('apt-get -y install python-pip')
    sudo('pip install pip --upgrade')
    sudo('pip install virtualenv')

def setup_apache():
    sudo('apt-get -y install apache2')
    sudo('a2enmod proxy')
    sudo('a2enmod proxy_http')
    sudo('a2enmod vhost_alias')
    sudo('a2dissite default')

def setup_basic_auth_user(username):
    run('htpasswd -c /etc/apache2/passwords %s' % username)

def upload_config(username=''):
    if username:
        fabric.operations.put('apache.config.basic_auth', '/etc/apache2/sites-available/jenkins')
    else:
        fabric.operations.put('apache.config', '/etc/apache2/sites-available/jenkins')
    sudo('chown www-data:www-data /etc/apache2/sites-available/jenkins')
    sudo('chmod 766 /etc/apache2/sites-available/jenkins')


def enable_apache_site():
    sudo('a2ensite jenkins')
    sudo('/etc/init.d/apache2 restart')


def deploy_jenkins(auth_username=''):
    setup_machine()
    setup_apache()
    if auth_username:
        setup_basic_auth_user(auth_username)
    enable_apache_site()



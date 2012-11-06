import fabric
from fabric.api import run, cd, env, sudo

# ADD YOUR JENKINS CI SERVER HOST HERE
env.hosts = ['']

# SET YOUR JENKINS CI SERVER (ROOT-ACCESS) USERNAME HERE
env.user = 'ubuntu'

# SET YOUR KEYFILE NAME HERE (your key-pair name .pem file for ec2 instances)
env.key_filename = ''


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
    sudo('htpasswd -c /etc/apache2/passwords %s' % username)

def get_config_path(suffix):
    import os
    return os.path.join(os.getcwd(), suffix)

def upload_config(username=''):
    if username:
        localpath = get_config_path('apache.config.basic_auth')
        fabric.operations.put(localpath, '/etc/apache2/sites-available/jenkins', use_sudo=True)
    else:
        localpath = get_config_path('apache.config')
        fabric.operations.put('apache.config', '/etc/apache2/sites-available/jenkins', use_sudo=True)
    sudo('chown root:root /etc/apache2/sites-available/jenkins')
    sudo('chmod 644 /etc/apache2/sites-available/jenkins')


def enable_apache_site():
    sudo('a2ensite jenkins')
    sudo('/etc/init.d/apache2 restart')


def setup_ssh_keys():
    sudo('ssh-keygen -t rsa', user='jenkins')
    run('echo "your deploy key:"')
    sudo('cat /var/lib/jenkins/.ssh/id_rsa.pub')


def deploy_jenkins(auth_username=''):
    setup_machine()
    setup_apache()
    if auth_username:
        setup_basic_auth_user(auth_username)
    upload_config(auth_username)
    enable_apache_site()
    setup_ssh_keys()


def test_clone_repo(repourl=''):
    if not repourl:
        print 'Specify a repository url'
        return
    
    path = '/var/lib/jenkins/test_clone'
    sudo('rm -Rf %s' % path)
    sudo('mkdir %s' % path, user='jenkins')
    sudo('chown jenkins:nogroup %s' % path)
    sudo('cd %s; git clone %s' % (path, repourl), user='jenkins')
    sudo('rm -Rf %s' % path)



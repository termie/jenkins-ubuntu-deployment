# jenkins-ubuntu-deployment


### Overview:

A simple fabric () script that deploys and sets up a Jenkins continuous integration server with one line.


### Installation:

```
git clone git@github.com:ailling/jenkins-ubuntu-deployment.git
cd jenkins-ubuntu-deployment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Deploy Jenkins

With basic http auth:
```
fab deploy_jenkins:auth_username="your username"
```

Note: you'll be prompted for a password for this basic http auth user.

With no authorization:
```
fab deploy_jenkins
```


### Deployment keys

This script will generate private/public keypairs for the 'jenkins' user on the machine you setup. Make
sure to just accept the defaults (by hitting enter) and it'll create public key ~/.ssh/id_rsa.pub


The public key will be displayed at the end of the script; copy and paste this key into the deployment
keys of your Git server (in Github, go to your project's Admin section on the right and click on 'Deploy keys', add a new key)


### Test ability to clone

Your jenkins server will need your known_hosts file populated with the server details where your git reository is located.
You can either uploda your own known_hosts file or run the clone test and type "yes" when prompted:

```
fab test_clone_repo:repourl="your git repoistory url" # e.g., git@github.com:username/project.git
```


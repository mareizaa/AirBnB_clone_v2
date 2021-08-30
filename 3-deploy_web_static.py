#!/usr/bin/python3
'''Generates a .tgz archive from the contents of the web_static'''
from fabric.api import local
from datetime import datetime
from fabric.api import run, put, env
from os import path

env.user = "ubuntu"
env.hosts = ['34.138.145.79', '18.207.128.190']


def do_pack():
    '''Generates a .tgz archive from the contents of the web_static'''
    try:
        name = datetime.now().strftime('%Y%m%d%H%M%S')
        name_file = "versions/web_static_{}.tgz".format(name)
        local('mkdir -p versions')
        print('Packing web_static to {}'.format(name_file))
        local('tar -cvzf {} web_static'.format(name_file))
        return name_file
    except:
        return None


def do_deploy(archive_path):
    '''
    Distributes an archive to your web servers,
    using the function do_deploy
    '''
    if path.exists(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name_file = file.split(".")[0]

    try:
        path_f = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path_f, name_file))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file, path_f, name_file))
        run('rm /tmp/{}'.format(file))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path_f, name_file))
        run('rm -rf {}{}/web_static'.format(path_f, name_file))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path_f, name_file))
        print("New version deployed")
        return True
    except:
        return None


def deploy():
    """
    creates and distributes an archive to your web servers,
    using the function deploy
    """
    path_file = do_pack()
    if path_file is None:
        return False
    return do_deploy(path_file)

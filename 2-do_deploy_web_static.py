#!/usr/bin/python3
'''Generates a .tgz archive from the contents of the web_static'''
from fabric.api import run, put, env
from os import path

env.user = "ubuntu"
env.hosts = ['34.138.145.79', '18.207.128.190']


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

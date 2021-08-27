#!/usr/bin/python3
'''Generates a .tgz archive from the contents of the web_static'''
from fabric.api import local
from datetime import datetime


def do_pack():
    '''Generates a .tgz archive from the contents of the web_static'''
    try:
        name = datetime.now().strftime('%Y%m%d%H%M%S')
        name_file = "versions/web_static_{}.tgz".format(name)
        local('mkdir -p versions')
        print('Packing web_static to {}'.format(name_file))
        local('tar -cvzf {} web_static'.format(name_file))
    except:
        None

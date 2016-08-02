# -*- coding: utf-8 -*-
import os, time, socket
import ConfigParser
class env:
    pass
def valid_ip(address):
    """
    #从配置文件中获取配置
    """
    return True
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

config = ConfigParser.ConfigParser()    
with open(r'config.ini') as fd:
    config.readfp(fd)

env.user=config.get("env","user").strip(" \n\r\t")
env.password=config.get("env","password").strip(" \n\r\t")
env.project_dev_source=config.get("env","project_dev_source").strip(" \n\r\t")
env.project_tar_source=config.get("env","project_tar_source").strip(" \n\r\t")
env.project_pack_name=config.get("env","project_pack_name").strip(" \n\r\t")
env.deploy_project_root=config.get("env","deploy_project_root").strip(" \n\r\t")
env.deploy_release_dir=config.get("env","deploy_release_dir").strip(" \n\r\t")
env.deploy_current_dir=config.get("env","deploy_current_dir").strip(" \n\r\t")
env.deploy_version=time.strftime("%Y%m%d") + config.get("env","deploy_version").strip(" \n\r\t")  
env.hosts=[IP for IP in config.get("env","hosts").strip(" \n\r\t").split(',') if valid_ip(IP)]

env.deploy_full_path=os.path.join(env.deploy_project_root, env.deploy_release_dir, env.deploy_version)
print env.user
print env.password
print env.project_dev_source
print env.project_tar_source
print env.project_pack_name
print env.deploy_project_root
print env.deploy_release_dir
print env.deploy_current_dir
print env.deploy_release_dir
print env.deploy_version
print env.hosts
print env.deploy_full_path

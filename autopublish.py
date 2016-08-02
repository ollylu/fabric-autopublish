# -*- coding: utf-8 -*-
'''
Created on 2016/8/1
  

auto publish script
  
@author: ollylu
'''

import os, time, re
import ConfigParser
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user='root'                #生产集群机器用户
env.hosts=[]                   #生产集群机器IP列表
env.password=''                #生产集群机器密码
env.project_dev_source = ''    #开发机项目主目录 如：/data/dev/Lwebadmin
env.project_tar_source = ''    #开发机项目压缩包存储目录 如：/data/dev/releases
env.project_pack_name = ''     #项目压缩包名前缀, 如：release 文件名为release.tar.gz
env.deploy_project_root = ''   #项目生产环境主目录 如：/data/www/Lwebadmin
env.deploy_release_dir = ''    #项目发布目录,位于主目录下面 如：releases
env.deploy_current_dir = ''    #对外服务的当前版本,软链接 如：current
env.deploy_version=''          #版本号 如 20160517v9.0.1


def valid_ip(address):
    """
    #只对IP有效性 做最基本检查
    """
    pieces = address.split('.')
    
    if len(pieces) != 4: 
       return False
    try: 
       return all(0<=int(p)<256 for p in pieces)
       
    except ValueError: 
       return False
    
@runs_once
def get_config_form_config_ini():
    """
    #从配置文件中获取配置
    """
    
    config = ConfigParser.ConfigParser()    
    with open(os.path.join(os.path.dirname(__file__),'config.ini'),'r') as fd:
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
    
    if len(env.hosts)<1:
       abort("Aborting can not get host ip from config.ini")
       
    if not os.path.isdir(env.project_dev_source):
       abort("Aborting project_dev_source not such dir!")
       
#在入口函数之前，获取配置，填充env
get_config_form_config_ini()
   
@runs_once
def input_versionid():
    """
    #获得用户输入的版本号,以便做版本回滚操作
    """
    return prompt("please input project rollback version ID:",default="")
    

@task
@runs_once
def tar_source():
    """
    #打包本地项目主目录,并将压缩包存储到本地压缩包目录
    """
    print yellow("Creating source package...")
    local("mkdir -p %s" % env.project_tar_source)
    with lcd(env.project_dev_source):
        local("tar -czf %s.tar.gz ." % os.path.join(env.project_tar_source, env.project_pack_name))
    
    print green("Creating source package success！")
    

@task
def put_package():
    """
    #上传任务函数
    """
    print yellow("Start put package...")
    
    #创建版本目录
    with settings(warn_only=True):
        run("mkdir -p %s" % env.deploy_project_root)
        
        with cd(env.deploy_project_root): 
            run("mkdir -p %s" % os.path.join(env.deploy_project_root, env.deploy_release_dir)) 
            
        with cd(os.path.join(env.deploy_project_root, env.deploy_release_dir)):       
            run("mkdir -p %s" % env.deploy_version)     
    
    #上传项目压缩包至此目录
    with settings(warn_only=True):
        print green(env.deploy_full_path)
        result = put(os.path.join(env.project_tar_source, env.project_pack_name) +".tar.gz", env.deploy_full_path)
    
    if result.failed and no("put file failed, Continue[Y/N]？"):
        abort("Aborting file put task！")
    
    #成功解压后删除压缩包
    with cd(env.deploy_full_path):
        run("tar -zxvf %s.tar.gz >/dev/null  2>&1" % env.project_pack_name)
        run("rm -rf %s.tar.gz" % env.project_pack_name)
    
    print green("Put & untar package success！")

@task
def make_symlink():
    """
    #为当前版本目录做软链接
    """
    print yellow("update current symlink")
    
    #删除软链接,重新创建并指定软链源目录,新版本生效
    with settings(warn_only=True):    
        run("rm -rf %s" % os.path.join(env.deploy_project_root, env.deploy_current_dir) )
        run("ln -s %s %s" % (env.deploy_full_path, \
                             os.path.join(env.deploy_project_root, env.deploy_current_dir)) )
        
    print green("make symlink success！")

@task
def rollback():
    """
    #版本回滚任务函数
    """
    #读取配置文件
    get_config_form_config_ini()
    
    print yellow("rollback project version")
    
    #获得用户输入的回滚版本号
    versionid= input_versionid()   
    if versionid=='':
        abort("Project version ID error,abort！")
        
    env.deploy_full_path=os.path.join(env.deploy_project_root, \
                                      env.deploy_release_dir,  \
                                      versionid)
    
    #删除软链接,重新创建并指定软链源目录,新版本生效
    run("rm -rf %s" % os.path.join(env.deploy_project_root, env.deploy_current_dir) )
    run("ln -s %s %s" % (env.deploy_full_path, os.path.join(env.deploy_project_root, env.deploy_current_dir)) )
    
    print green("rollback success！")

@task
def go():
    """
    #自动化版本发布入口函数
    """
    tar_source()
    put_package()
    make_symlink() 

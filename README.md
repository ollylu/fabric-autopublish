# 基于fabric 的自动化发布应用

##应用场景
autopublish.py 初步实现了一个通用性较强的代码发布管理功能，支持快速部署与回滚，无论发布还是回滚，
都可以通过切换current的软链来实现，比较灵活。
[](https://github.com/ollylu/fabric-autopublish/blob/master/autopublish.png)

## 安装与配置

autopublish.py依赖第三方Fabric包的支持,我们可以通过
pip很方便的安装Fabric，只需要一条命令^_^,
```
pip install fabric

```
校验安装结果，如果导入模块没有提示异常，则说明安装成功：
```
# python
Python 2.6.6 （r266：84292， Jul 10 2013， 22：48：45） 
[GCC 4.4.7 20120313 （Red Hat 4.4.7-3）] on linux2
Type "help"， "copyright"， "credits" or "license" for more information.
>>> import fabric
>>> 
```
将源码下载到代码分发服务器的任意目录下：
```
root@ubuntu:/data/autopublish/fabric-install-and-use# ll
total 244
drwxr-xr-x 3 root root   4096 Aug  2 06:22 ./
drwxr-xr-x 3 root root   4096 Aug  2 04:10 ../
-rw-r--r-- 1 root root 213237 Aug  2 04:11 autopublish.png
-rw-r--r-- 1 root root   6064 Aug  2 05:50 autopublish.py
-rw-r--r-- 1 root root    663 Aug  2 04:11 config.ini
drwxr-xr-x 8 root root   4096 Aug  2 05:50 .git/
-rw-r--r-- 1 root root    546 Aug  2 04:11 README.md
```
配置config.ini文件，样例如下
```
    [env]

    生产集群机器用户
    user = root

    生产集群机器列表逗号分割
    hosts = 192.168.57.133, 192.168.57.131, 192.168.57.130

    生产集群机器密码
    password = ollylu

    开发机项目主目录
    project_dev_source = /data/dev/Lwebadmin

    开发机项目压缩包存储目录
    project_tar_source = /data/dev/releases

    项目压缩包名前缀,文件名为release.tar.gz
    project_pack_name = release

    项目生产环境主目录
    deploy_project_root = /data/www/Lwebadmin

    项目发布目录,位于主目录下面
    deploy_release_dir = releases

    对外服务的当前版本,软链接
    deploy_current_dir = current

    版本号
    deploy_version=v9.0.1

执行发布
```
fab -f autopublish.py go
```

发布回滚
```
fab -f autopublish.py rollback
```

## 代码实现说明



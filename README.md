# fabric的安装与应用

## 安装

Fabric依赖第三方的setuptools、Crypto、paramiko包的支持,但我们可以通过
pip很方便解决包依赖的问题^_^,只需要一条命令
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

## 应用

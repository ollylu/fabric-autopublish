# 基于fabric 的自动化发布应用

##应用场景
autopublish.py 初步实现了一个通用性较强的代码发布管理功能，支持快速部署与回滚，无论发布还是回滚，
都可以通过切换current的软链来实现，比较灵活。
[](https://github.com/ollylu/fabric-autopublish/blob/master/autopublish.png)

## 安装与配置

依赖第三方Fabric包的支持,我们可以通过
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

## 应用

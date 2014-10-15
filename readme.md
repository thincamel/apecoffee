说明
===

##### 99Party 采用Flask框架(Jinjia2)

##### 需要安装的依赖Flask插件
参见 requirements.txt

##### 工程说明
* 99Party工程目录，包含：config.py（全局配置）、run.py（运行程序）、app.db（应用数据库SQLite）。`其他一些用于数据库升降级，暂不需要`
* app子目录，参考Flask，包含：static（静态文件）、templates（Jinjia模版）、\__init\__.py、以及对应MVC模式相应的几个Python文件
* db_repository子目录，`用于数据库升降级，暂不需要`

#####
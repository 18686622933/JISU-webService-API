# JISU-webService-API
web Service接口

dataSource.py ：访问数据库的类方法  
DataItem.py   ：数据应用  
RESTful-API.py：API引擎

使用方法：  
1、在DataItem.py文件的 "items"中增加新得 应用名称、中文名称、字段注释、以及sql查询语句  
2、在DataItem.py文件中增加与"items"中应用名称一致且首字母大写的类，内容完全复制前面的类即可 
3、在RESTful-API.py文件中"配置路由"位置使用api.add_resource()增加新得路由，
第一个参数与DataItem.py文件中中的类名称一致，路由中的参数<code>不可更改


说明：  
目前数据均取自一个库，即为dataSource.py中select()函数中配置的'中心库'，  
如想取多个库，可以新增连接参数，或配置新的函数

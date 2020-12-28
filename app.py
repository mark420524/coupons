#! /usr/bin/python
# encoding:utf-8

# 导入Tornado模块
import tornado.ioloop #核心IO循环模块
import tornado.httpserver #异步非阻塞HTTP服务器模块
import tornado.web #Web框架模块
import tornado.options #解析终端参数模块

#从终端模块中导出define模块用于读取参数，导出options模块用于设置默认参数
from tornado.options import define, options
from handler.goods import GoodsHandler
from utils import config
# 定义端口用于指定HTTP服务监听的端口
# 如果命令行中带有port同名参数则会称为全局tornado.options的属性，若没有则使用define定义。
define("port", type=int, default=10324, help="run on the given port")
conf = config.init()
conf = config.get_yaml()

# 创建路由表
urls = [(r"/goods", GoodsHandler,dict(conf=conf))]

# 定义服务器
def main():
    # 解析命令行参数
    tornado.options.parse_command_line()
    # 创建应用实例
    app = tornado.web.Application(urls)
    # 监听端口
    app.listen(options.port)
    # 创建IOLoop实例并启动
    tornado.ioloop.IOLoop.current().start()

# 应用运行入口，解析命令行参数
if __name__ == "__main__":
    # 启动服务器
    main()

# coding=utf-8

"""

"""

from untils import config

def run():
    conf = config.init()
    if not conf:  # 如果 conf，表示配置文件出错。
        print('程序中止...')
        return
    print(config.copy())

if __name__ == '__main__':
    run()

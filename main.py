# coding=utf-8

"""

"""

from utils import config
from coupon.jd import jingfen_query
from coupon.tb import tb_share_text
from coupon.tb import  tb_search_goods
from utils.type import isString

conf = config.init()
def jd_job_task(page_no, page_size):

    conf = config.get_yaml()
    conf = conf.get('jingdong')
    if not conf.get('is_open'):
        return
    if conf.get('app_key') =='' or conf.get('app_secret') =='' or conf.get('site_id') =='' or conf.get('suo_im') =='':
        return
    chat_groups = conf.get('chat_groups')
    app_key = conf.get('app_key')
    app_secret = conf.get('app_secret')
    site_id = conf.get('site_id')
    suo_im = conf.get('suo_im')
    for chat_group in chat_groups:
        kwargs={'group_material_id': chat_group['group_material_id'],
                'app_key': app_key, 'secret_key': app_secret, 'site_id': site_id, 'suo_mi_token': suo_im,'page_no':page_no, 'page_size': page_size}
        jingfen_query(**kwargs)

def tb_job(page_no, page_size):
    conf = config.get_yaml()
    conf = conf.get('taobao')
    if not conf.get('is_open'):
        return
    if conf.get('app_key') =='' or conf.get('app_secret') =='' or conf.get('adzone_id') =='' :
        return
    
    group_material_id = conf.get('group_material_id')
    app_key = conf.get('app_key')
    app_secret = conf.get('app_secret')
    adzone_id = conf.get('adzone_id')
    kwargs={'material_id': group_material_id,
                'app_key': app_key, 'app_secret': app_secret, 'adzone_id': adzone_id,'page_no':page_no, 'page_size': page_size}
    tb_share_text(**kwargs)


def tb_search_job(page_no, page_size):
    conf = config.get_yaml()
    conf = conf.get('taobao')
    if not conf.get('is_open'):
        return
    if conf.get('app_key') =='' or conf.get('app_secret') =='' or conf.get('adzone_id') =='' :
        return
    
    group_material_id = conf.get('group_material_id')
    app_key = conf.get('app_key')
    app_secret = conf.get('app_secret')
    adzone_id = conf.get('adzone_id')
    kwargs={'material_id': '',
                'app_key': app_key, 'app_secret': app_secret, 'adzone_id': adzone_id,'page_no':page_no, 'page_size': page_size,
                 'goods_sort':'', 'goods_platform':'', 'q':'内衣'}
    info = tb_search_goods(**kwargs)

def run(goods_type):
    if not conf:  # 如果 conf，表示配置文件出错。
        print('程序中止...')
        return 'error conf'
    print(page_no)
    print(page_size)
    #jd_job_task()
    return 'ok'

if __name__ == '__main__':
    print(tb_search_job(1, 1))

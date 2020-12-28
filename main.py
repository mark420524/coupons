# coding=utf-8

"""

"""

from utils import config
from coupon.jd import jingfen_query
from coupon.tb import tb_share_text
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

def run(goods_type):
    if not conf:  # 如果 conf，表示配置文件出错。
        print('程序中止...')
        return 'error conf'
    print(page_no)
    print(page_size)
    #jd_job_task()
    return 'ok'

if __name__ == '__main__':
    run(1)

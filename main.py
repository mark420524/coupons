# coding=utf-8

"""

"""

from utils import config
from coupon.jd import jingfen_query



def jd_job_task(scheduler):

    conf = config.get_yaml()
    conf = conf.get('jingdong')
    if not conf.get('is_open'):
        return

    if conf.get('app_key') =='' or conf.get('app_secret') =='' or conf.get('site_id') =='' or conf.get('suo_im') =='':
        return

    app_key = conf.get('app_key')
    app_secret = conf.get('app_secret')
    site_id = conf.get('site_id')
    suo_im = conf.get('suo_im')
    kwargs={'group_name': chat_group['group_name'], 'group_material_id': chat_group['group_material_id'],
                                  'app_key': app_key, 'secret_key': app_secret, 'site_id': site_id, 'suo_mi_token': suo_im}
    print(kwargs)
def run():
    conf = config.init()
    if not conf:  # 如果 conf，表示配置文件出错。
        print('程序中止...')
        return
    print(config.copy())

if __name__ == '__main__':
    run()

import tornado.web
import tornado.escape
import logging
from coupon.jd import jingfen_query
from coupon.tb import tb_share_text
from enums.goods_enum import GoodsEnum
logger = logging.getLogger(__name__)

class GoodsHandler(tornado.web.RequestHandler):
    def initialize(self, conf):

        self.conf = conf 

    def get(self):
        page_no = self.get_query_argument('page')
        page_size = self.get_query_argument('size')
        goods_type = self.get_query_argument('type')
        logging.info('query params, page_no:%s,page_size:%s,goods_type:%s', page_no, page_size, goods_type)
        try:
            c = GoodsEnum(str(goods_type))
        except ValueError:
            c = 0
         
        if c == GoodsEnum.JD:
            info = self.get_jd()
        elif c == GoodsEnum.PDD:
            info = []
            print('pdd')
        elif c == GoodsEnum.TB:
            info = self.tb_job(page_no, page_size)
        self.write_json(info)

    def get_jd(self, page_no, page_size):
        conf = self.conf.get('jingdong')
        
        if not conf.get('is_open'):
            return
        if conf.get('app_key') =='' or conf.get('app_secret') =='' or conf.get('site_id') =='' or conf.get('suo_im') =='':
            return
        group_material_id = conf.get('group_material_id')
        app_key = conf.get('app_key')
        app_secret = conf.get('app_secret')
        site_id = conf.get('site_id')
        suo_im = conf.get('suo_im')
        info = []
        kwargs={'group_material_id': group_material_id,
                'app_key': app_key, 'secret_key': app_secret, 'site_id': site_id, 'suo_mi_token': suo_im,'page_no':page_no, 'page_size': page_size}
        info=jingfen_query(**kwargs)
        return info
    
    def tb_job(self, page_no, page_size):
        
        conf = self.conf.get('taobao')
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
        
        return tb_share_text(**kwargs)

    def write_json(self, info):
        self.set_header('Content-Type', 'application/json')
        self.write(tornado.escape.json_encode(info))




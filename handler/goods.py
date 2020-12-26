import tornado.web
import tornado.escape
import logging
from coupon.jd import jingfen_query

logger = logging.getLogger(__name__)

class GoodsHandler(tornado.web.RequestHandler):
    def initialize(self, conf):

        self.conf = conf 

    def get(self):
        page_no = self.get_query_argument('page')
        page_size = self.get_query_argument('size')
        goods_type = self.get_query_argument('type')
        logging.info('query params, page_no:%s,page_size:%s,goods_type:%s', page_no, page_size, goods_type)
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
        self.write_json(info)

    def write_json(self, info):
        self.set_header('Content-Type', 'application/json')
        self.write(tornado.escape.json_encode(info))




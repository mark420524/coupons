import time
import json
import random

from utils.tb_top_api import TbApiClient
from utils.common import save_pic

def tb_share_text( material_id: str, app_key, app_secret, adzone_id, page_no, page_size):
    '''

    :param group_name:
    :param material_id:
    :return:
    '''
    info = []
    try:
        material_id = str(random.choices(material_id.split(','))[0])
        #print(material_id)
        time.sleep(random.randint(1, 5))
        tb_client = TbApiClient(app_key=app_key, secret_key=app_secret, adzone_id=adzone_id)
        res = tb_client.taobao_tbk_dg_optimus_material(material_id, page_no, page_size)
        json_data = json.loads(res)['tbk_dg_optimus_material_response']['result_list']['map_data']
        count = 0
        folder = 'taobao'
        for item in json_data:
            count += 1
            coupon_amount = 0
            coupon_share_url = ""
            title = ""
            if str(item).find("coupon_share_url") > -1:
                coupon_share_url = "https:" + item['coupon_share_url']
                coupon_amount = item['coupon_amount']
                pict_url = "https:" + str(item['pict_url'])
                title = item['title']
                item_id = item['item_id']
                filename = save_pic(pict_url, item_id, folder)
                zk_final_price = item['zk_final_price']
                reserve_price = item['reserve_price']
                text = f'''{tb_client.taobao_tbk_tpwd_create(title, coupon_share_url)}'''
            else:
                click_url = "https:" + item['click_url']
                coupon_share_url = click_url
                title = item['title']
                item_id = item['item_id']
                pict_url = "https:" + str(item['pict_url'])
                filename = save_pic(pict_url, item_id, folder)
                zk_final_price = item['zk_final_price']
                reserve_price = item['reserve_price']
                text = f'''{tb_client.taobao_tbk_tpwd_create(title, coupon_share_url)}'''
            item_info = {
        	'price':reserve_price,'lowest_price':zk_final_price,
        	'duanzhi':coupon_share_url,'short_desc':text, 
        	'imageUrl':pict_url, 'sku_name':title}
            info.append(item_info)
    
    except Exception as e:
        print(e)
        #tb_share_text(material_id, app_key, app_secret, adzone_id, page_no, page_size)
    return info



def tb_search_goods( material_id: str, app_key, app_secret, adzone_id, page_no, page_size, goods_sort, goods_platform, q):
    '''

    :param group_name:
    :param material_id:
    :return:
    '''
    info = []
    try:
        material_id = str(random.choices(material_id.split(','))[0])
        #print(material_id)
        time.sleep(random.randint(1, 5))
        tb_client = TbApiClient(app_key=app_key, secret_key=app_secret, adzone_id=adzone_id)
        res = tb_client.taobao_tbk_material_optional(material_id, q, goods_sort, goods_platform, page_no, page_size)
        json_data = res
        
        count = 0
        folder = 'taobao'
        for item in json_data:
            count += 1
            coupon_amount = 0
            coupon_share_url = ""
            title = ""
            if str(item).find("coupon_share_url") > -1:
                coupon_share_url = "https:" + item['coupon_share_url']
                coupon_amount = item['coupon_amount']
                pict_url =  item['pict_url'] 
                title = item['title']
                item_id = item['item_id']
                filename = save_pic(pict_url, item_id, folder)
                zk_final_price = item['zk_final_price']
                reserve_price = item['reserve_price']
                text = f'''{tb_client.taobao_tbk_tpwd_create(title, coupon_share_url)}'''
            else:
                click_url =  item['item_url']
                coupon_share_url = click_url
                title = item['title']
                item_id = item['item_id']
                pict_url =  item['pict_url'] 
                filename = save_pic(pict_url, item_id, folder)
                zk_final_price = item['zk_final_price']
                reserve_price = item['reserve_price']
                text = f'''{tb_client.taobao_tbk_tpwd_create(title, coupon_share_url)}'''
            item_info = {
        	'price':reserve_price,'lowest_price':zk_final_price,
        	'duanzhi':coupon_share_url,'short_desc':text, 
        	'imageUrl':pict_url, 'sku_name':title}
            info.append(item_info)
    
    except Exception as e:
        print(e)
        #tb_share_text(material_id, app_key, app_secret, adzone_id, page_no, page_size)
    return info

if __name__ == '__main__':
    print(f'''tb function''')

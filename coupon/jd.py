'''
用suo_mi短址的原因是因为京东使用短址的api需要申请，申请的门槛我放到这里：

a)      流量稳定且具备一定推广规模的联盟会员，无违规行为，接受业绩考核。

b)      会员申请标准：开通后两个月内的月订单量>3万单 或 月点击量>30万次

c)      如开通后2个自然月内如无返回数据，或月订单量达不到要求的，联盟平台将可以关闭高级权限。


就上面第二条是我未来所期待的，所以折中选了个其他短址的
'''

import random
import time
import json
from utils.jd_api import JdApiClient
from utils.suo_im import Suo_mi
from utils.common import save_pic, del_pic

def jingfen_query( group_material_id:str, app_key:str, secret_key:str, site_id:str, suo_mi_token:str,page_no:int,page_size:int):
    ''' 方法效率不咋地，不管了
    https://union.jd.com/openplatform/api/10421
    :return:
    '''
    info = []
    try:

        client = JdApiClient(app_key=app_key, secret_key=secret_key)
        resp = client.call("jd.union.open.goods.jingfen.query",
                           {"goodsReq":
                                {"sort": "desc",
                                 "pageSize": page_size,
                                 "pageIndex": page_no,
                                 "eliteId": group_material_id
                                 }})
    except Exception as e:
        print(e)
        #jingfen_query( group_material_id, app_key, secret_key, site_id, suo_mi_token)
    # pprint.pprint(json.loads(resp.json()['jd_union_open_goods_jingfen_query_response']['result']))
    for data in json.loads(resp.json()['jd_union_open_goods_jingfen_query_response']['result'])['data']:
        sku_name = data['skuName']   ## 商品全名
        sku_id = data['skuId']     ## 商品 sku
        material_url = f'''http://{(data['materialUrl'])}''' ## 商品url

        couponInfos = data['couponInfo'] ## 优惠券列表
        imageInfo = data['imageInfo']
        imageObj = imageInfo['imageList'][0]
        # 查找最优优惠券
        coupon_link = ""
        discount = 0
        share_text = ""
        lowest_price_type = data['priceInfo']['lowestPriceType']  ## 什么类型
        is_coupon = False
        for couponInfo in couponInfos['couponList']:
            if 'isBest' in couponInfo:
                if int(couponInfo['isBest']) == 1:
                    discount = couponInfo['discount']  ## 优惠券额度
                    coupon_link = couponInfo['link']  ## 优惠券领取地址
                    is_coupon = True
            else:
                discount = couponInfo['discount']  ## 优惠券额度
                coupon_link = couponInfo['link']  ## 优惠券领取地址
                is_coupon = True
                
        if is_coupon: # 如果有券
            if lowest_price_type == 3:  # 秒杀
                price = data['seckillInfo']['seckillOriPrice'] # 原价
                lowest_price = data['priceInfo']['lowestCouponPrice'] # 秒杀价
                duanzhi = tb_share_text(app_key, secret_key, material_url, coupon_link, site_id, suo_mi_token)
                share_text = f'''【秒杀】{sku_name}\n——————————\n  【原价】¥{price}\n 【券后秒杀价】¥{lowest_price}\n抢购地址：{duanzhi}'''
                short_desc = f'''【秒杀】\n——————————\n  【原价】¥{price}\n 【券后秒杀价】¥{lowest_price}\n抢购地址：{duanzhi}'''
            elif lowest_price_type == 2: # 拼购
                price = data['priceInfo']['price']  # 原价
                lowest_price = data['priceInfo']['lowestCouponPrice']  # 用券拼购
                duanzhi = tb_share_text(app_key, secret_key, material_url, coupon_link, site_id, suo_mi_token)
                share_text = f'''【拼购】{sku_name}\n——————————\n  【原价】¥{price}\n 【券后拼购价】¥{lowest_price}\n抢购地址：{duanzhi}'''
                short_desc = f'''【拼购】\n——————————\n  【原价】¥{price}\n 【券后拼购价】¥{lowest_price}\n抢购地址：{duanzhi}'''
            else:
                price = data['priceInfo']['price'] ## 商品价格
                lowest_price = data['priceInfo']['lowestCouponPrice']
                duanzhi = tb_share_text(app_key, secret_key, material_url, coupon_link, site_id, suo_mi_token)
                share_text = f'''【京东】{sku_name}\n——————————\n  【爆款价】¥{price}\n 【用卷价】¥{lowest_price}\n抢购地址：{duanzhi}'''
                short_desc = f'''【京东】\n——————————\n  【爆款价】¥{price}\n 【用卷价】¥{lowest_price}\n抢购地址：{duanzhi}'''


        else: ## 如果没有券
            if lowest_price_type == 3:  # 秒杀
                price = data['seckillInfo']['seckillOriPrice']  # 原价
                lowest_price = data['seckillInfo']['seckillPrice']  # 秒杀价
                duanzhi = tb_share_text(app_key, secret_key, material_url, coupon_link, site_id, suo_mi_token)
                share_text = f'''【秒杀】{sku_name}\n——————————\n  【原价】¥{price}\n 【秒杀价】¥{lowest_price}\n抢购地址：{duanzhi}'''
                short_desc = f'''【秒杀】\n——————————\n  【原价】¥{price}\n 【秒杀价】¥{lowest_price}\n抢购地址：{duanzhi}'''

            elif lowest_price_type == 2:  # 拼购
                price = data['priceInfo']['price']  # 原价
                lowest_price = data['priceInfo']['lowestPrice']  # 用券拼购
                duanzhi = tb_share_text(app_key, secret_key, material_url, coupon_link, site_id, suo_mi_token)
                share_text = f'''【拼购】{sku_name}\n——————————\n  【原价】¥{price}\n 【拼购价】¥{lowest_price}\n抢购地址：{duanzhi}'''
                short_desc = f'''【拼购】\n——————————\n  【原价】¥{price}\n 【拼购价】¥{lowest_price}\n抢购地址：{duanzhi}'''
            else:
                price = data['priceInfo']['price']
                lowest_price = price
                # 得到短址
                duanzhi = tb_share_text(app_key, secret_key, material_url, coupon_link, site_id, suo_mi_token)
                share_text = f'''【京东】{sku_name}\n——————————\n 【爆款价】¥{lowest_price}\n抢购地址：{duanzhi}'''
                short_desc = f'''【京东】\n——————————\n 【爆款价】¥{lowest_price}\n抢购地址：{duanzhi}'''
        item_info = {
        	'price':price,'lowest_price':lowest_price,
        	'duanzhi':duanzhi,'short_desc':short_desc, 
        	'imageUrl':imageObj['url'], 'sku_name':sku_name}
        info.append(item_info)
    return info

def tb_share_text(app_key, secret_key, material_url, coupon_url, site_id, suo_mi_token):
    '''
    :param material_url: 物料的url
    :param coupon_url:  优惠券的url
    :param site_id:  网站id
    :param suo_mi_token: suo_mi网站的token
    :return: string ，返回一个suo_mi的短址
    '''
    #rint(f'''{app_key}''')
    ##print(f'''{secret_key}''')
    #print(f'''{material_url}''')
    #print(f'''{coupon_url}''')
    #print(f'''{site_id}''')
    #print(f'''{suo_mi_token}''')
    client = JdApiClient(app_key=app_key, secret_key=secret_key)
    if coupon_url == "":
        resp = client.call("jd.union.open.promotion.common.get",
                           {"promotionCodeReq":
                                {
                                 "siteId": site_id,
                                 "materialId": material_url
                                 }})
    else:
        resp = client.call("jd.union.open.promotion.common.get",
                           {"promotionCodeReq":
                                {
                                 "siteId": site_id,
                                 "materialId": material_url,
                                 "couponUrl": coupon_url
                                 }})
    try:
        x = json.loads(resp.json()['jd_union_open_promotion_common_get_response']['result'])['data']['clickURL']
    except Exception as e:
        print(f'''转码异常：{resp.json()}\n material_url: {material_url} \n coupon_url: {coupon_url}''')
        x = material_url
    # 直接返回短址
    url = x
    #print(url)
    #c = Suo_mi(app_key=suo_mi_token).get_short_url(url)
    return url

if __name__ == '__main__':
    pass
    # jingfen_query()

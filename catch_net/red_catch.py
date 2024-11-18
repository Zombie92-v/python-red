from catch_net import extract_request_headers_and_body
from DriverManage import singleDriver
import json

'''
{
    "username": "Alice",
    "avatar": "https://sns-avatar-qc.xhscdn.com/avatar/62bd17578aee9196052f8693.jpg?imageView2/2/w/120/format/jpg",
    "comment": "这真是一个很棒的体验！",
    "comment_pic": "https://sns-webpic-qc.xhscdn.com/202411170130/21f33bb91eaed0a34584932a8a06f243/comment/1040g2h031a5ohikmmm005n85141k1860a1adp3g!nc_n_webp_mw_1",
    "like": '4.2万',
}
'''


def commnts(url, target_url='/comment/page', filter=lambda h: 'json' in h.get("content-type")):
    driver = singleDriver.getDriver()
    target_url, json_response = extract_request_headers_and_body(driver=driver, target_url_part=target_url,
                                                                 url=url, timeout=60,
                                                                 filter=filter)
    print("目标请求的 URL：", target_url)
    res_list = []
    response = json.loads(json.dumps(json_response, indent=4, ensure_ascii=False))
    for i in response['data']['comments']:
        obj = {
            'username': i['user_info']['nickname'],
            'avatar': i['user_info']['image'],
            'comment': i['content'],
            'comment_pic': i.get('pictures', [{}])[0].get('url_pre', None) if i.get('pictures', []) else None,
            'like': i['like_count']
        }
        # 过滤作者
        if 'is_author' in i.get('show_tags', []):
            print('作者')
            continue
        res_list.append(obj)
    return res_list


if __name__ == '__main__':
    url = "https://www.xiaohongshu.com/explore/67346883000000001b010cfa?xsec_token=ABheASSYPcqzFhsmuUywUjdTz_Xmu0ftMnDmC_p-7gFg8=&xsec_source=pc_collect"  # 替换为目标网页 URL
    res_list = commnts(url=url)
    print(len(res_list))
    pass

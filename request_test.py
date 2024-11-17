import requests

url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page'
params = {
    'note_id': '67346883000000001b010cfa',
    'cursor': '',
    'top_comment_id': '',
    'image_formats': 'jpg,webp,avif',
    'xsec_token': 'ABheASSYPcqzFhsmuUywUjdTz_Xmu0ftMnDmC_p-7gFg8%3D'
}

headers = {
    'cookie': 'abRequestId=7f001fb3-cf8e-54c1-998f-0d6022a26f3b; a1=191f67af17301me7b393wx9me9qopbexl41avhqyf50000428339; webId=5c1b17a92634dc2d59ed938113feacf0; gid=yjyiKW0iKS1dyjyiKW0iy4xAWq8y6dWDqjqEyviCj6djA028lUDdCh8884JYqqj8yd4fifJS; web_session=0400698fbab3b3565f2f846a1a354b7413c447; webBuild=4.43.0; xsecappid=xhs-pc-web; unread={%22ub%22:%226736193e000000001a01eb38%22%2C%22ue%22:%226736cd0d000000001b0103e4%22%2C%22uc%22:23}; acw_tc=0a50882717317652632938269ef148166b7e1d5b5c93e3372cc0a7a6d25e23; websectiga=cffd9dcea65962b05ab048ac76962acee933d26157113bb213105a116241fa6c; sec_poison_id=f69e9ff5-f6f5-4f10-99ce-735a814e2e5a',
    'x-s': 'XYW_eyJzaWduU3ZuIjoiNTUiLCJzaWduVHlwZSI6IngyIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6IjdiNTRiOWEzOTJlMmY0MzYzZWFkYmI3MGNlZDQ2ZDdjYjE0MjgxNmNiN2FhNjI4Yzk3NWZmN2UwNGZiZmY0MTE4ODhkZGM1Y2I3MTBlZjQ4OWVmODZkYTk2ZDdlYjk4N2JkYjlkZWRiNDZmYmM4YjY2NGRkODRkZTljM2EwZTk2ZTAwMDg5ZmY3YTY1ODdhNWYyM2JiNzJlMDYyNmRkZWJlY2VmYjI0MTZlOTdkN2UzMjZhZmE4ODhjMzQwNTgwZWQ5OTQzMzFkNmE1YjcwYjVlZmU4MDUzNmJmNGMwNDNiNGNlMTg2ZjgzMWU2ZmM1MmI2NjQ5Zjc2YjRhMDVmN2Q2MGQyZDhlY2VmYzA4ZTYwNTIyYmE1ZDdhNzE2NzAyMWJlNzg1OTRmYzVlNmRiZWU2NDIyODM3NDdjNzI0YThmYTVlZGI1OTQ0ZjFhMTk5NjNjZmE0OTE2ZGYwODZmOGI2ODVmYjk4MjUwNWUyZTM5YzMxZTVhMzA5NWIzZmM1ZjVkZjhlZDFmMzY1NTRlZjU4Zjk5NDViNzU5ZjIzOTMyIn0',
    'x-s-common': '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',
    'origin': 'https://www.xiaohongshu.com',
    'sec-ch-ua': '"Google Chrome";v="118", "Not A Brand";v="99", "Chromium";v="118"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-t': '1731767048263',
    "Host": "www.xiaohongshu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1114.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
}

response = requests.get(url, params=params, headers=headers)

print(response)

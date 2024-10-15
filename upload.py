import os
import requests
import tempfile
from urllib.parse import urlparse

def download_and_upload_to_smms(resource_url: str, smms_token: str) -> str:
    """
    下载线上资源并上传到 SM.MS 图床，返回 SM.MS 的 URL。

    :param resource_url: 线上资源的URL，例如图片或视频的链接。
    :param smms_token: SM.MS 的 API Token。
    :return: 上传到 SM.MS 后的资源URL。
    :raises: Exception 如果下载或上传失败。
    """
    try:
        # 发送GET请求下载资源，使用stream=True处理大文件
        with requests.get(resource_url, stream=True) as response:
            response.raise_for_status()  # 检查请求是否成功

            # 解析URL获取文件名，如果无法获取则使用默认名称
            parsed_url = urlparse(resource_url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = 'uploaded_file'

            # 创建临时文件保存下载的资源
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                temp_file_path = tmp_file.name

        # 上传到 SM.MS
        with open(temp_file_path, 'rb') as image_file:
            headers = {'Authorization': smms_token}
            files = {'smfile': image_file}
            upload_response = requests.post('https://sm.ms/api/v2/upload', headers=headers, files=files)
            upload_response.raise_for_status()  # 检查上传请求是否成功
            json_response = upload_response.json()
            if not json_response.get('success'):
                raise Exception(f"SM.MS 上传失败: {json_response.get('message')}")

            smms_url = json_response['data']['url']

        # 删除临时文件
        os.remove(temp_file_path)

        return smms_url

    except requests.RequestException as e:
        raise Exception(f"下载或上传过程中发生网络错误: {e}")
    except Exception as e:
        raise Exception(f"下载或上传过程中发生错误: {e}")

# 使用示例
if __name__ == "__main__":
    # 替换为你要下载的资源URL
    resource_url = "https://sns-video-al.xhscdn.com/stream/110/259/01e7066362a542e4010370039270f4cf25_259.mp4"

    # 替换为你的SM.MS API Token
    smms_token = "BW50KlMTqojE31YyxAwZ36oV3cNpvxxt"

    try:
        smms_url = download_and_upload_to_smms(resource_url, smms_token)
        print(f"资源已上传到SM.MS: {smms_url}")
    except Exception as e:
        print(f"发生错误: {e}")

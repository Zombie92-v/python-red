import os
import requests
from urllib.parse import urlparse
from tqdm import tqdm
from pathlib import Path
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_old_files(directory: Path, max_files: int):
    """
    检查目录中的文件数量，并在超过指定数量时删除最早创建的文件。
    """
    files = list(directory.glob("*"))
    if len(files) > max_files:
        # 按文件创建时间排序
        files.sort(key=lambda f: f.stat().st_ctime)
        # 删除最早的文件
        for file_to_delete in files[:len(files) - max_files]:
            logger.info(f"删除旧文件: {file_to_delete}")
            file_to_delete.unlink()

def download_resource_with_progress(url, save_dir='downloads', chunk_size=8192):
    """
    下载指定 URL 的资源并保存到本地，显示进度条。

    :param url: 资源的 URL，例如 MP4 文件的链接。
    :param save_dir: 保存资源的本地目录。默认为 'downloads'。
    :param chunk_size: 每次下载的块大小（字节）。默认为 8192（8KB）。
    :return: 下载后文件的本地路径。
    :raises: Exception 如果下载失败或 URL 无效。
    """
    try:
        # 解析 URL 获取文件名
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            raise ValueError("无法从 URL 中提取文件名。")

        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)

        # 发送 GET 请求，流式下载
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # 检查请求是否成功

            # 获取总大小（如果服务器提供）
            total_size = int(response.headers.get('content-length', 0))
            block_size = chunk_size
            t = tqdm(total=total_size, unit='iB', unit_scale=True)

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        file.write(chunk)
                        t.update(len(chunk))
            t.close()

        if total_size != 0 and t.n != total_size:
            print("警告: 下载过程中出现问题，下载的文件可能不完整。")
            raise Exception("下载不完整。")

        print(f"下载完成: {file_path}")
        cleanup_old_files(Path(save_dir),200)
        return f"/file/{filename}"

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        raise
    except Exception as e:
        print(f"下载失败: {e}")
        raise

if __name__ == '__main__':
    print(download_resource_with_progress(url="https://sns-video-al.xhscdn.com/stream/110/258/01e6e5dfee9cd1e80103700191f1f32340_258.mp4#devtools_no_referrer"))
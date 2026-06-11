import os
import json
import base64
import mimetypes
import requests
import concurrent.futures
import webbrowser
from pathlib import Path

# ==================== 全局配置 ====================
# API_KEY = os.getenv("AGNES_API_KEY", "YOUR_AGNES_API_KEY")
API_KEY = "wk-JLIt1hBlc3NX8gH2cXEPY8Oc9BbLU3fgdsgnxhtrjoMuLJWe"
BASE_URL = "https://apihub.agnes-ai.com/v1"  # 官方接口地址
JSON_CONFIG_PATH = "C:\\program1\\project\\Front\\typora-img\\image_generate\\batch_tasks.json"        # JSON 任务配置文件路径

# 并发控制变量（轻度并发，建议设置为 2 ~ 5 之间，避免请求频率过高触发 API 限制）
MAX_WORKERS = 10
# ==================================================


def file_to_base64_uri(file_path: str) -> str:
    """
    读取本地图片文件并将其转化为 Data URI Base64 格式
    此格式可直接通过 API 发送，无需将本地图片上传至公网服务器
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"本地文件未找到: {file_path}")

    # 自动探测文件 MIME 类型 (例如 image/png, image/jpeg)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "image/png"  # 默认降级格式

    with open(file_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{b64_data}"


def download_image(url: str, save_path: str, log_prefix: str) -> bool:
    """下载生成的图片并保存到本地"""
    try:
        response = requests.get(url, timeout=300)
        response.raise_for_status()

        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"{log_prefix} 👉 [成功] 图片已保存至: {save_path}")
        return True
    except Exception as e:
        print(f"{log_prefix} ❌ [错误] 图片下载失败: {e}")
        return False


def process_single_task(task: dict, headers: dict) -> str | None:
    """
    执行单个生图任务
    在独立线程中运行，保证多任务并发执行
    成功时返回 output_path，失败返回 None
    """
    task_id = task.get("task_id", "Unknown")
    task_type = task.get("type", "text_to_image")
    prompt = task.get("prompt")
    size = task.get("size", "1024x1024")
    output_path = task.get("output_path", f"./output_{task_id}.png")

    log_prefix = f"[{task_id}]"

    # 自动匹配最佳模型
    model = task.get("model")
    if not model:
        if task_type == "text_to_image":
            model = "agnes-image-2.1-flash"  # 文生图
        elif task_type == "image_to_image":
            model = "agnes-image-2.0-flash"  # 图生图

    print(f"{log_prefix} 🚀 任务启动 | 类型: {task_type} | 模型: {model} | 分辨率: {size}")

    # 构建通用 payload
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size
    }

    # 针对图生图，本地读取并转成 base64 传入
    if task_type == "image_to_image":
        local_image_path = task.get("local_image_path")
        if not local_image_path:
            print(f"{log_prefix} ❌ [失败] 图生图任务必须提供本地图片路径 'local_image_path'。")
            return

        try:
            # 转换为 Data URI
            base64_uri = file_to_base64_uri(local_image_path)
            # 注入至 extra_body.image 中
            payload["extra_body"] = {
                "image": [base64_uri]
            }
        except Exception as e:
            print(f"{log_prefix} ❌ [本地错误] 读取本地图片失败: {e}")
            return

    endpoint = f"{BASE_URL}/images/generations"

    try:
        # 发送 API 请求 (增加较大超时以防生图排队时间较长)
        response = requests.post(endpoint, headers=headers, json=payload, timeout=300)

        if response.status_code != 200:
            print(f"{log_prefix} ❌ [API错误] HTTP {response.status_code}\n详情: {response.text}")
            return

        res_json = response.json()
        image_list = res_json.get("data", [])

        if image_list and len(image_list) > 0:
            generated_url = image_list[0].get("url")
            if generated_url:
                print(f"{log_prefix} 🎨 图像已由 Agnes 生成成功，正在下载中...")
                if download_image(generated_url, output_path, log_prefix):
                    return output_path
            else:
                print(f"{log_prefix} ❌ [解析错误] 返回结构正常，但没有找到图片 URL")
        else:
            print(f"{log_prefix} ❌ [响应异常] 接口返回值未包含预期图像：{res_json}")

    except requests.exceptions.RequestException as e:
        print(f"{log_prefix} ❌ [网络错误] 请求 API 失败: {e}")
    except Exception as e:
        print(f"{log_prefix} ❌ [未知异常] 执行过程中出错: {e}")


def generate_html_gallery(image_paths: list[str], output_html: str):
    """将成功生成的图片列表写入一个 HTML 页面并打开"""
    cards = []
    for path in image_paths:
        abs_path = os.path.abspath(path)
        filename = os.path.basename(abs_path)
        # 用 file:// 协议直接引用本地图片
        file_uri = Path(abs_path).as_uri()
        cards.append(f"""    <div class="card">
      <img src="{file_uri}" alt="{filename}" loading="lazy" onclick="window.open('{file_uri}')">
      <div class="info">
        <div class="filename">{filename}</div>
        <div class="filepath">{abs_path}</div>
      </div>
    </div>""")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 图片生成结果 - 共 {len(image_paths)} 张</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, 'Segoe UI', sans-serif; background: #f5f5f5; padding: 30px; }}
h1 {{ font-size: 24px; margin-bottom: 20px; color: #333; }}
h1 span {{ font-weight: normal; font-size: 16px; color: #888; }}
.gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
.card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); transition: transform 0.15s; }}
.card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.12); }}
.card img {{ width: 100%; height: 280px; object-fit: cover; display: block; cursor: pointer; }}
.card .info {{ padding: 12px 16px; }}
.card .filename {{ font-size: 14px; font-weight: 600; color: #222; word-break: break-all; }}
.card .filepath {{ font-size: 11px; color: #999; word-break: break-all; margin-top: 4px; }}
</style>
</head>
<body>
<h1>AI 图片生成结果 <span>共 {len(image_paths)} 张</span></h1>
<div class="gallery">
{chr(10).join(cards)}
</div>
</body>
</html>"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)

    abs_html = os.path.abspath(output_html)
    print(f"\n📄 HTML 页面已生成: {abs_html}")
    # webbrowser.open(Path(abs_html).as_uri())


def run_batch_concurrency(config_path: str):
    """主并发控制函数"""
    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"🌟 批量并发任务开始运行。最大并发任务数 (MAX_WORKERS) 已设置为: {MAX_WORKERS}")

    # 采用线程池（ThreadPoolExecutor）对 I/O 密集型的网络请求进行并发调度
    successful_images = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        futures = {executor.submit(process_single_task, task, headers): task for task in tasks}

        # 观察并等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            task = futures[future]
            task_id = task.get("task_id", "Unknown")
            try:
                result = future.result()  # 触发可能产生的未捕获线程异常
                if result:
                    successful_images.append(result)
            except Exception as e:
                print(f"❌ [{task_id}] 线程执行期间产生致命故障: {e}")

    print(f"\n✨ 并发任务队列处理完毕，成功生成了 {len(successful_images)} 张图片。")

    if successful_images:
        successful_images.sort()
        html_path = os.path.join(os.path.dirname(config_path), "image_gallery.html")
        generate_html_gallery(successful_images, html_path)


if __name__ == "__main__":
    if API_KEY == "YOUR_AGNES_API_KEY":
        print("⚠️ 请确认你已经在全局配置区修改了 API_KEY 变量。")
    else:
        run_batch_concurrency(JSON_CONFIG_PATH)
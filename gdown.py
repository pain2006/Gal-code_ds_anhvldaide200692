import os
import requests
import time
from urllib.parse import urlparse, parse_qs

def get_drive_id(url):
    try:
        parsed = urlparse(url)
        if 'drive.google.com' not in parsed.netloc:
            return None
        path_parts = parsed.path.split('/')
        if 'folders' in path_parts:
            return path_parts[-1].split('?')[0]
        elif 'file' in path_parts and 'd' in path_parts:
            return path_parts[path_parts.index('d') + 1].split('?')[0]
        elif 'open' in parsed.path:
            qs = parse_qs(parsed.query)
            return qs.get('id', [None])[0]
        return None
    except Exception as e:
        print(f"Lỗi phân tích URL {url}: {e}")
        return None

def is_folder_url(url):
    return 'folders' in url or 'folderview' in url

def download_file(drive_id, output_path):
    try:
        url = f"https://drive.google.com/uc?export=download&id={drive_id}"
        session = requests.Session()
        response = session.get(url, stream=True)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break
        if token:
            url = f"https://drive.google.com/uc?export=download&confirm={token}&id={drive_id}"
            response = session.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Lỗi tải file {drive_id}: {e}")
        return False

try:
    start_time = time.time()
    folder_path = input("Nhập đường dẫn thư mục chứa file txt: ")
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not txt_files:
        print("Không tìm thấy file txt")
        exit()
    txt_path = os.path.join(folder_path, txt_files[0])
    with open(txt_path, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    output_folder = os.path.join(folder_path, 'output')
    os.makedirs(output_folder, exist_ok=True)
    total = len(links)
    for i, link in enumerate(links, 1):
        drive_id = get_drive_id(link)
        if not drive_id:
            print(f"Bỏ qua link không hợp lệ: {link}")
            continue
        try:
            if is_folder_url(link):
                print(f"Không hỗ trợ tải thư mục: {link}. Vui lòng nén thư mục thành ZIP trên Google Drive.")
                continue
            output_path = os.path.join(output_folder, f"file_{i}.png")
            if download_file(drive_id, output_path):
                print(f"Hoàn thành {i}/{total}")
        except Exception as e:
            print(f"Lỗi tải {link}: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Hoàn thành tất cả tác vụ trong {elapsed_time:.2f} giây")
except Exception as e:
    print(f"Lỗi: {e}")
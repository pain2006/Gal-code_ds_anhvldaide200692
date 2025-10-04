import os
from PIL import Image

def create_black_version(img_path, output_path):
    img = Image.open(img_path).convert('RGBA')
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if a > 0:
                img.putpixel((x, y), (0, 0, 0, a))
    img.save(output_path, dpi=(300, 300))

folder_path = input("Enter folder path: ")
output_folder = os.path.join(folder_path, 'output')
os.makedirs(output_folder, exist_ok=True)

for subfolder in os.listdir(folder_path):
    sub_path = os.path.join(folder_path, subfolder)
    if not os.path.isdir(sub_path):
        continue
    file_f = os.path.join(sub_path, 'F.png')
    file_b = os.path.join(sub_path, 'B.png')
    if not os.path.exists(file_f):
        print(f"Missing F.png in {subfolder}")
        continue
    
    # Tạo file S.png từ F.png
    file_s = os.path.join(sub_path, 'S.png')
    create_black_version(file_f, file_s)
    
    # Chuẩn bị danh sách ảnh để dàn trang
    image_files = [file_s, file_f]
    if os.path.exists(file_b):
        image_files.append(file_b)
    
    # Tạo file dàn trang
    images = [Image.open(f).convert('RGBA') for f in image_files]
    widths = [img.width for img in images]
    heights = [img.height for img in images]
    max_width = max(widths)
    total_height = sum(heights)
    combined = Image.new('RGBA', (max_width, total_height))
    y_offset = 0
    for img in images:
        combined.paste(img, (0, y_offset))
        y_offset += img.height
    output_file = os.path.join(output_folder, f"{subfolder}.png")
    combined.save(output_file, dpi=(300, 300))
    print(f"Created {output_file}")
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
    img.save(output_path)

folder_path = input("Enter folder path: ")
output_folder = os.path.join(folder_path, 'output')
os.makedirs(output_folder, exist_ok=True)

for subfolder in os.listdir(folder_path):
    sub_path = os.path.join(folder_path, subfolder)
    if not os.path.isdir(sub_path):
        continue
    file2 = os.path.join(sub_path, '2.png')
    file4 = os.path.join(sub_path, '4.png')
    if not (os.path.exists(file2) and os.path.exists(file4)):
        print(f"Missing files in {subfolder}")
        continue
    file1 = os.path.join(sub_path, '1.png')
    file3 = os.path.join(sub_path, '3.png')
    create_black_version(file2, file1)
    create_black_version(file4, file3)
    images = [Image.open(os.path.join(sub_path, f"{i}.png")) for i in range(1, 5)]
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
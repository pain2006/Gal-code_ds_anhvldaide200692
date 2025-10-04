import os
from PIL import Image

folder_path = input("Enter folder path: ")
output_folder = os.path.join(folder_path, 'output')
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(folder_path):
    if not file.endswith('.png'):
        continue
    parts = file[:-4].split('_')
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        print(f"Invalid format: {file}")
        continue
    name, W_str, H_str = parts
    W, H = int(W_str), int(H_str)
    img_path = os.path.join(folder_path, file)
    img = Image.open(img_path)
    # Preserve original mode (RGBA for transparency, RGB otherwise)
    width, height = img.size
    new_width = width * W
    new_height = height * H
    new_img = Image.new(img.mode, (new_width, new_height))
    for i in range(W):
        for j in range(H):
            new_img.paste(img, (i * width, j * height))
    output_path = os.path.join(output_folder, f"{name}_{W}_{H}_output.png")
    new_img.save(output_path, dpi=(300, 300))
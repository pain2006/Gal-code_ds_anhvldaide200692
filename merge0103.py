import os
from PIL import Image

def rotate_and_combine_images(image1_path, image2_path, output_path):
    """Ghép hai ảnh đã xoay thành một.

    Args:
        image1_path: Đường dẫn đến ảnh thứ nhất.
        image2_path: Đường dẫn đến ảnh thứ hai.
        output_path: Đường dẫn để lưu ảnh kết quả.
    """
    image1 = Image.open(image1_path).rotate(90)
    image2 = Image.open(image2_path).rotate(90)

    # Tính toán kích thước ảnh kết quả (bạn có thể tùy chỉnh)
    width = 19630 
    height = 15529

    new_image = Image.new('RGBA', (width, height),(0,0,0,0))
    new_image.paste(image1, (276, 1060))
    new_image.paste(image2, (9928, 1060))
    new_image.save(output_path, dpi=(300, 300))

if __name__ == "__main__":
    folder_path = input("Nhập đường dẫn đến folder chứa ảnh: ")

    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if len(image_files) < 2:
        print("Folder không chứa đủ 2 ảnh để ghép!")
    else:
        for i in range(0, len(image_files), 2):
            if i + 1 < len(image_files):
                image1_path = os.path.join(folder_path, image_files[i])
                image2_path = os.path.join(folder_path, image_files[i + 1])

                output_file = f"{image_files[i][:-4]}_{image_files[i+1][:-4]}.png"
                output_path = os.path.join(folder_path, output_file)

                rotate_and_combine_images(image1_path, image2_path, output_path)
            else:
                print(f"Ảnh {image_files[i]} không có ảnh ghép cặp.")

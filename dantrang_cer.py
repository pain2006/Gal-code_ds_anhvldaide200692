import os
from PIL import Image

def main():
    # Nhập đường dẫn folder
    folder_path = input("Enter the path to the folder containing PNG designs: ").strip()
    
    # Lấy tên folder để đặt tên file output
    folder_name = os.path.basename(folder_path)
    
    # Tạo folder output
    output_folder = os.path.join(folder_path, "output")
    os.makedirs(output_folder, exist_ok=True)
    
    # Duyệt tất cả file PNG trong folder và subfolders
    designs = []
    for root, dirs, files in os.walk(folder_path):
        if root == output_folder:
            continue  # Bỏ qua folder output
        for file in files:
            if file.lower().endswith('.png'):
                name, ext = os.path.splitext(file)
                parts = name.rsplit('_', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    count = int(parts[1])
                    img_path = os.path.join(root, file)
                    designs.append((img_path, count))
                else:
                    print(f"Warning: File '{file}' does not match the required format 'filename_X.png' (X must be a number).")
    
    # Sắp xếp designs theo đường dẫn để đảm bảo thứ tự nhất quán
    designs.sort(key=lambda x: x[0])
    
    # Kiểm tra kích thước các ảnh
    dimensions = set()
    for img_path, _ in designs:
        img = Image.open(img_path)
        dimensions.add(img.size)
        img.close()
    
    if len(dimensions) > 1:
        print("Error: All PNG files must have the same dimensions.")
        return
    
    if not dimensions:
        print("Error: No valid PNG files found.")
        return
    
    # Kích thước canvas
    canvas_width = 28346
    canvas_height = 5906
    
    # Khởi tạo canvas đầu tiên (mode RGBA với nền transparent)
    current_canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
    
    # Vị trí hiện tại: bắt đầu từ dưới lên
    current_x = 0
    current_y = canvas_height
    max_height_in_row = 0
    
    # Số trang
    page_num = 1
    
    # Duyệt qua từng design và dàn số lượng X
    for img_path, count in designs:
        for _ in range(count):
            # Mở hình ảnh
            img = Image.open(img_path)
            w, h = img.size
            
            # Nếu không vừa vào hàng hiện tại, chuyển sang hàng mới (lên trên)
            if current_x + w > canvas_width:
                current_y -= max_height_in_row
                current_x = 0
                max_height_in_row = 0
            
            # Nếu không vừa vào canvas hiện tại, tạo canvas mới và lưu canvas cũ
            if current_y - h < 0:
                output_path = os.path.join(output_folder, f"{folder_name}_{page_num}.png")
                current_canvas.save(output_path, dpi=(300, 300))
                page_num += 1
                current_canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
                current_x = 0
                current_y = canvas_height
                max_height_in_row = 0
            
            # Dán hình ảnh vào canvas, align bottom
            current_canvas.paste(img, (current_x, current_y - h))
            
            # Cập nhật vị trí và max height của hàng
            current_x += w
            max_height_in_row = max(max_height_in_row, h)
            
            # Đóng hình ảnh để tiết kiệm bộ nhớ
            img.close()
    
    # Lưu canvas cuối cùng nếu có nội dung
    if current_x > 0 or current_y < canvas_height:
        output_path = os.path.join(output_folder, f"{folder_name}_{page_num}.png")
        current_canvas.save(output_path, dpi=(300, 300))
    
    print(f"Dàn trang hoàn tất. Các file output được lưu trong thư mục: {output_folder}")

if __name__ == "__main__":
    main()
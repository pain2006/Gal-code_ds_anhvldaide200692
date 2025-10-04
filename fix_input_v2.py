import os
from PIL import Image
import traceback

def create_black_version(img_path, output_path):
    try:
        img = Image.open(img_path).convert('RGBA')
        width, height = img.size
        for x in range(width):
            for y in range(height):
                r, g, b, a = img.getpixel((x, y))
                if a > 0:
                    img.putpixel((x, y), (0, 0, 0, a))
        img.save(output_path, dpi=(300, 300))
        print(f"Created {output_path}")
    except Exception as e:
        print(f"Error creating black version for {img_path}: {e}")
        traceback.print_exc()

def main():
    try:
        folder_path = input("Enter folder path: ").strip()
        if not os.path.exists(folder_path):
            print(f"Error: Folder {folder_path} does not exist.")
            return
        
        output_folder = os.path.join(folder_path, 'output')
        os.makedirs(output_folder, exist_ok=True)
        print(f"Created output folder: {output_folder}")
        
        processed = False
        png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
        if not png_files:
            print(f"No PNG files found in {folder_path}")
            return
        
        for file in png_files:
            try:
                file_f = os.path.join(folder_path, file)
                file_name = os.path.splitext(file)[0]
                file_s = os.path.join(folder_path, f"{file_name}-S.png")
                print(f"Creating {file_s} from {file_f}")
                create_black_version(file_f, file_s)
                
                # Tạo file dàn trang
                image_files = [file_s, file_f]
                images = []
                for f in image_files:
                    try:
                        images.append(Image.open(f).convert('RGBA'))
                    except Exception as e:
                        print(f"Error opening {f}: {e}")
                        continue
                
                if not images:
                    print(f"No valid images for {file_name}")
                    continue
                
                max_width = max(img.width for img in images)
                total_height = sum(img.height for img in images)
                combined = Image.new('RGBA', (max_width, total_height))
                y_offset = 0
                for img in images:
                    combined.paste(img, (0, y_offset))
                    y_offset += img.height
                output_file = os.path.join(output_folder, f"{file_name}.png")
                combined.save(output_file, dpi=(300, 300))
                print(f"Created layout file: {output_file}")
                processed = True
            
            except Exception as e:
                print(f"Error processing {file}: {e}")
                traceback.print_exc()
        
        if not processed:
            print("No files were processed. Check PNG files.")
    
    except Exception as e:
        print(f"Main error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
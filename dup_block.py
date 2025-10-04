import os, glob, qrcode, openpyxl
from PIL import Image, ImageDraw, ImageFont
from os import path

# load database




path_folder= input("input path here: ")
list_png = glob.glob(path_folder+'/**/*.png', recursive=True)
list_jpg = glob.glob(path_folder+'/**/*.jpg', recursive=True)
list_ds =[]
i= 0
# tao folder file final
path_final = path_folder + "/final"
if os.path.exists(path_final) == False: 
	os.mkdir(path_final)




# lay list design
for p in list_png:
	list_ds.append(p)

for j in list_jpg:
	list_ds.append(j)

for ds in list_ds:
	#detect info product
	ds_name= os.path.splitext(os.path.basename(ds))[0]
	ds_ex=os.path.splitext(os.path.basename(ds))[1]
	dup_quan = ds_name.split("_")[1]  
	ds_x, ds_y,ds_dpi, ds_w_s, ds_h_s, ds_code_sz = 3000,200,300,3500,2500,50   # định vị code, dim standard, code sz
	
	fnt= ImageFont.truetype("arial.ttf",ds_code_sz)
		
	#add code
	print(ds_name," begin render...")
	img = Image.open(ds)
	

	ds_img_mode= img_r.mode  #hệ màu

	d = ImageDraw.Draw(img)
	for j in range(0,dup_quan-1):
		bl= i + j + 1
		d.text((ds_x,ds_y),'Block' + bl,font= fnt, fill=(0,0,0))
		img_r.save(path_final+"/Block "+ bl +ds_ex, dpi=(ds_dpi,ds_dpi))


	i = i+1
	print(i)


	print(ds_name," Done")

	
print("Finish. Good luck have fun:) ")



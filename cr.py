import os, glob, qrcode, openpyxl
from PIL import Image, ImageDraw, ImageFont
from os import path

# load database




path_folder= input("input path here: ")
list_png = glob.glob(path_folder+'/**/*.png', recursive=True)
list_jpg = glob.glob(path_folder+'/**/*.jpg', recursive=True)
list_ds =[]
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
	ds_code = os.path.splitext(os.path.basename(ds))[1]  #product code 
	ds_mode = 3  #modul base code product
	ds_x, ds_y,ds_dpi, ds_w_s, ds_h_s, ds_code_sz = 5400,1400,300,3500,2500,30   # định vị code, dim standard, code sz
	

	fnt= ImageFont.truetype("arial.ttf",ds_code_sz)
		
	#add code
	print(ds_name," begin render...")
	img = Image.open(ds)
	#img_r = img.resize((ds_w_s,ds_h_s))

	ds_img_mode= img_r.mode  #hệ màu

	if ds_mode == 1:  # add code outside
		new = Image.new(ds_img_mode,(ds_w_s,ds_h_s + 70),color=(255,255,255))
		d = ImageDraw.Draw(new)
		d.text((ds_w_s/2,ds_h_s),ds_name,font= fnt, fill=(0,0,0))
		new.paste(img_r,(0,0))
		new.save(path_final+"/"+ds_name+ds_ex, dpi=(ds_dpi,ds_dpi))
	elif ds_mode==2:   # add qrcode 

		# convert cmyk

		
		qr = qrcode.QRCode(
	    version=1,
	    error_correction=qrcode.constants.ERROR_CORRECT_L,
	    box_size=5,
	    border=1,
		)
		qr.add_data(ds_name)
		qr.make(fit=True)
		ds_qr = qr.make_image(fill_color="black", back_color="white")
		# img_r.paste(ds_qr,(ds_x,ds_y))
		# img_r.save(path_final+"/"+ds_name+ds_ex, dpi=(ds_dpi,ds_dpi))

		if ds_img_mode =='RGB':
			ds_cmyk = img_r.convert('CMYK')
			ds_cmyk.paste(ds_qr,(ds_x,ds_y))
			ds_cmyk.save(path_final+"/"+ds_name+".jpg", dpi=(ds_dpi,ds_dpi))
		img_r.paste(ds_qr,(ds_x,ds_y))
		img_r.save(path_final+"/"+ds_name+ds_ex, dpi=(ds_dpi,ds_dpi))

	elif ds_mode==3: #add code text 
		new = Image.new('RGBA',(280,900), color=(0,0,0,0))
		d = ImageDraw.Draw(new)
		d.text((5,5),ds_name,font= fnt, fill=(0,0,0,))
		new_f = new.transpose(Image.FLIP_LEFT_RIGHT)
		img.paste(new_f,(5400,1400))
		img.paste(new_f,(5400,4300))

		img.save(path_final+"/"+ds_name+ds_ex, dpi=(ds_dpi,ds_dpi))


	print(ds_name," Done")

	
print("Finish. Good luck have fun:) ")



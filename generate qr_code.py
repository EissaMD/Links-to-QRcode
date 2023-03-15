import qrcode
from PIL import Image, ImageDraw, ImageFont
import csv
csv_file = "csv\KSA_100S980212140_2000.csv"
bg_w , bg_h = 	1240 , 1754
no_col , no_row = 4, 5
bg_original = Image.new('RGB', (bg_w, bg_h), (255, 255, 255))
csv_file_name = csv_file.split(".")[0].split("\\")[1]
ff = ImageFont.truetype("arial.ttf", 16)
bg = bg_original.copy()
qr_w = int(bg_w/no_col)
qr_h = int(bg_h/no_row)
img_ls = []
no_page=1
current_col= current_row= pos_x= pos_y = counter= 0
with open(csv_file, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        counter+=1
        link = row[0]
        link_no = link.split('c=')[1]
        if current_col == no_col:
            current_col = pos_x = 0
            current_row += 1
            pos_y = pos_y + qr_h
        if current_row == no_row:
            current_col= current_row= pos_x= pos_y= 0
            draw = ImageDraw.Draw(bg)
            draw.text((2, 2), text=csv_file_name, fill='black' , font=ff)
            img_ls.append(bg)
            # bg.save(f'imgs/qrcode_{no_page}.png')
            bg = bg_original.copy()
            no_page+=1
        qr_img = qrcode.make(link).resize((qr_w, qr_h))
        draw = ImageDraw.Draw(qr_img)
        draw.text(((qr_w-95)/2, qr_h-18), text=link_no, fill='black' , font=ff)
        bg.paste(qr_img, (pos_x, pos_y))
        pos_x = pos_x + qr_w
        current_col += 1

if counter//(no_col*no_row) > 0:
    img_ls.append(bg)
    # bg.save(f'imgs/qrcode_{no_page}.png')

img_ls[0].save(
    f"{csv_file_name}.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=img_ls[1:]
)
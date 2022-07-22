from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from keras.models import load_model
from PIL import Image #use PIL
import numpy as np
def NN_interpolation(img,dstH,dstW):
    if img.ndim == 3:
        scrH,scrW,_ = img.shape
        retimg=np.zeros((dstH,dstW,4),dtype=np.uint8)
        for k in range(4):
            for i in range(dstH-1):
                for j in range(dstW-1):
                    scrx = int(i*(scrH/dstH))
                    scry = int(j*(scrW/dstW))
                    retimg[i,j,k]=img[scrx,scry,k]  
    elif img.ndim == 4:
        _,scrH,scrW,_ = img.shape
        retimg=np.zeros((dstH,dstW,4),dtype=np.uint8)
        for k in range(4):
            for i in range(dstH-1):
                for j in range(dstW-1):
                    scrx = int(i*(scrH/dstH))
                    scry = int(j*(scrW/dstW))
                    retimg[i,j,k]=img[1,scrx,scry,k]    
    return retimg
def bilinear_interpolation(img,out_dim):
    src_h, src_w, channel = img.shape
    dst_h, dst_w = out_dim[1], out_dim[0]
    #print ("src_h, src_w = ", src_h, src_w)
    #print ("dst_h, dst_w = ", dst_h, dst_w)#没有必要打印出来
    if src_h == dst_h and src_w == dst_w:
        return img.copy()
    #如果输入大小与原图大小相同，则返回原图
    dst_img = np.zeros((dst_h,dst_w,4),dtype=np.uint8)
    #建立一个预输出的全0图像
    scale_x, scale_y = float(src_w) / dst_w, float(src_h) / dst_h
    for i in range(4):
        for dst_y in range(dst_h):
            for dst_x in range(dst_w):
            
                #使用几何中心对称
                #如果使用直接方式，src_x=dst_x*scale_x
                #scale是比例，通过同比例缩小/放大实现中心对齐
                src_x = (dst_x + 0.5) * scale_x - 0.5
                src_y = (dst_y + 0.5) * scale_y - 0.5
 
                #找到将用于计算插值的点的坐标
                src_x0 = int(np.floor(src_x))
                src_x1 = min(src_x0 + 1 ,src_w - 1)
                src_y0 = int(np.floor(src_y))
                src_y1 = min(src_y0 + 1, src_h - 1)

                # 计算插值
                temp0 = (src_x1 - src_x) * img[src_y0,src_x0,i] + (src_x - src_x0) * img[src_y0,src_x1,i]
                temp1 = (src_x1 - src_x) * img[src_y1,src_x0,i] + (src_x - src_x0) * img[src_y1,src_x1,i]
                dst_img[dst_y,dst_x,i] = int(round((src_y1 - src_y) * temp0 + (src_y - src_y0) * temp1)) #这里改为四舍五入取整
    return dst_img
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        file = request.files['file']
        print("File Received")
        filename = secure_filename(file.filename)
        print(filename)
        dict = ['Abra', 'Aerodactyl', 'Alakazam', 'Alolan Sandslash', 'Arbok', 'Arcanine', 'Articuno', 'Beedrill', 'Bellsprout', 'Blastoise', 'Bulbasaur', 'Butterfree', 'Caterpie', 'Chansey', 'Charizard', 'Charmander', 'Charmeleon', 'Clefable', 'Clefairy', 'Cloyster', 'Cubone', 'Dewgong', 'Diglett', 'Ditto', 'Dodrio', 'Doduo', 'Dragonair', 'Dragonite', 'Dratini', 'Drowzee', 'Dugtrio', 'Eevee', 'Ekans', 'Electabuzz', 'Electrode', 'Exeggcute', 'Exeggutor', 'Farfetchd', 'Fearow', 'Flareon', 'Gastly', 'Gengar', 'Geodude', 'Gloom', 'Golbat', 'Goldeen', 'Golduck', 'Golem', 'Graveler', 'Grimer', 'Growlithe', 'Gyarados', 'Haunter', 'Hitmonchan', 'Hitmonlee', 'Horsea', 'Hypno', 'Ivysaur', 'Jigglypuff', 'Jolteon', 'Jynx', 'Kabuto', 'Kabutops', 'Kadabra', 'Kakuna', 'Kangaskhan', 'Kingler', 'Koffing', 'Krabby', 'Lapras', 'Lickitung', 'Machamp', 'Machoke', 'Machop', 'Magikarp', 'Magmar', 'Magnemite', 'Magneton', 'Mankey', 'Marowak', 'Meowth', 'Metapod', 'Mew', 'Mewtwo', 'Moltres', 'Mr. Mime', 'MrMime', 'Muk', 'Nidoking', 'Nidoqueen', 'NidoranF', 'NidoranM', 'Nidorina', 'Nidorino', 'Ninetales', 'Oddish', 'Omanyte', 'Omastar', 'Onix', 'Paras', 'Parasect', 'Persian', 'Pidgeot', 'Pidgeotto', 'Pidgey', 'Pikachu', 'Pinsir', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Ponyta', 'Porygon', 'Primeape', 'Psyduck', 'Raichu', 'Rapidash', 'Raticate', 'Rattata', 'Rhydon', 'Rhyhorn', 'Sandshrew', 'Sandslash', 'Scyther', 'Seadra', 'Seaking', 'Seel', 'Shellder', 'Slowbro', 'Slowpoke', 'Snorlax', 'Spearow', 'Squirtle', 'Starmie', 'Staryu', 'Tangela', 'Tauros', 'Tentacool', 'Tentacruel', 'Vaporeon', 'Venomoth', 'Venonat', 'Venusaur', 'Victreebel', 'Vileplume', 'Voltorb', 'Vulpix', 'Wartortle', 'Weedle', 'Weepinbell', 'Weezing', 'Wigglytuff', 'Zapdos', 'Zubat']
        file.save("./static/"+filename) #Heroku no need static
        file = open("./static/"+filename,"r") #Heroku no need static
        model = load_model("Pokemon")
        image = Image.open("./static/"+filename)#读取方式为RGB
        image = image.convert("RGBA")                   # 图片转为RGB格式
        #image = np.array(image)[:, :, ::-1]            # 将图片转为numpy格式，并将最后一维通道倒序
        #image = Image.fromarray(np.uint8(image))       # 将numpy转换回PIL的Image对象#这里不要，datagenerator本身即为rgb读取
        #转化为BGR格式
        image = np.asarray(image)
        #image.resize((100,100,3),refcheck = False)
        image = NN_interpolation(image,128,128)#要采用邻近插值
        image = np.asarray(image, dtype="float64")/255 #need to transfer to np to reshape'
        image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2]) #rgb to reshape to 1,100,100,3
        pred= dict[model.predict(image).argmax()]
        return(render_template("index.html", result=str(pred)))
    else:
        return(render_template("index.html", result="WAITING"))
if __name__ == "__main__":
    app.run()

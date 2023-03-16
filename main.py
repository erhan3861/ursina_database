from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import sqlite3

seciliBlok = 1
mode = "level1"

def update():
    global seciliBlok # bir değişkeni bir fonk değiştirmek istiyorsak

    if held_keys["1"]:
        seciliBlok = 1
        print("beyaz küp seçildi")

    if held_keys["2"]:
        seciliBlok = 2
        print("çimen seçildi")

    if held_keys["3"]:
        seciliBlok = 3

    if held_keys["4"]:
        seciliBlok = 4

    if held_keys["5"]:
        seciliBlok = 5

    if held_keys["6"]:
        seciliBlok = 6

class Sky(Entity):
    def __init__(self): # fabrikası
        super().__init__( # super derken Entity sınıfı kastedilir
            parent = scene, # merkez, bağlı olduğu birim
            model = 'sphere', # küre
            texture = 'sky_default', # doku, kaplama
            double_sided = True, # iki taraflı
            scale = 150 # ölçek, büyüklük
        )

class Block(Button):
    def __init__(self, position = (0, 0, 0), texture="grass", zemin = 1): # SETUP KISMI
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            texture = texture,
            color = color.white,
            origin_y = .5,
            highlight_color = color.lime
        )
        self.tus = ""
        self.zemin = zemin

    def input(self, key):
        if self.hovered: # küpün üzerine gelmek
            if key == "right mouse down":
                if seciliBlok == 1:
                    block = Block(position=self.position+mouse.normal, texture="white_cube", zemin=0)
                elif seciliBlok == 2:
                    block = Block(position=self.position+mouse.normal, texture="grass", zemin=0)
                elif seciliBlok == 3:
                    block = Block(position=self.position+mouse.normal, texture="wallpaper.jfif", zemin=0)
                elif seciliBlok == 4:
                    block = Block(position=self.position+mouse.normal, texture="matrix.gif", zemin=0)
                elif seciliBlok == 5:
                    block = Block(position=self.position+mouse.normal, texture="kareli", zemin=0)
                    block.texture_scale = (2,2)
                elif seciliBlok == 6:
                    block = Block(position=self.position+mouse.normal, texture="cam", zemin=0)
                    block.color = color.rgba(255, 255, 255, 50) # a -> alpha = saydamlık

            if key == "left mouse down":
                destroy(self) # yok et
            
            if key in ["x","y","z","e","r","t","b","7","8","9"]:
                 self.tus = key # nesnenin key özelliğini x,y veya z tuşundan birisi yap
                        

    def update(self): # nesneyi günceller  self -> nesneyi gösterir / temsil eder
        if self.hovered: # küpün üzerinde gezinmek
            if self.tus == "x": self.x += (held_keys["+"] - held_keys["-"]) * 0.01 
            elif self.tus == "y": self.y += (held_keys["+"] - held_keys["-"]) * 0.01
            elif self.tus == "z": self.z += (held_keys["+"] - held_keys["-"]) * 0.01
            elif self.tus == "e": self.rotation_x += (held_keys["+"] - held_keys["-"]) * 5
            elif self.tus == "r": self.rotation_y += (held_keys["+"] - held_keys["-"]) * 5
            elif self.tus == "t": self.rotation_z += (held_keys["+"] - held_keys["-"]) * 5
            elif self.tus == "b": self.scale += (held_keys["+"] - held_keys["-"]) * Vec3(0.1, 0.1, 0.1)
            elif self.tus == "7": self.scale_x += (held_keys["+"] - held_keys["-"]) * 0.1
            elif self.tus == "8": self.scale_y += (held_keys["+"] - held_keys["-"]) * 0.1
            elif self.tus == "9": self.scale_z += (held_keys["+"] - held_keys["-"]) * 0.1


# app input fonksiyununu kullanacağınız
def input(key):
    if key == "k": # kayıt kelimesindeki ilk harf
        id = 0
        tablo_name = mode

        # veri tabanı silme işlemleri
        db = sqlite3.connect("veritabani.db")
        imlec = db.cursor()
        imlec.execute("DELETE FROM "+ tablo_name)
        db.commit() # save -> kayıt et
        db.close()

        for entity in scene.entities: # scene -> ekran
            if isinstance(entity, Block): # entity Block sınıfının bir öğesi midir?
                if entity.zemin == 1: # yani zemin ise
                    continue # devam et alttaki kodları çalıştırma
                id += 1
                # buradan sonra veritabanına kayıt işlemi yapılacak
                db = sqlite3.connect("veritabani.db")
                imlec = db.cursor()
                imlec.execute("INSERT INTO "+ tablo_name + "(id, model, x, y, z, texture,\
                              scale_x, scale_y, scale_z, rx, ry, rz)  VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",\
                                (id, str(entity.model), entity.x, entity.y, entity.z, str(entity.texture),\
                                 entity.scale_x, entity.scale_y, entity.scale_z, \
                                    entity.rotation_x, entity.rotation_y, entity.rotation_z)) # kayıt işlemi insert -> yerleştirmek
                db.commit() # KAYDET -> SAVE
                db.close()
    if key == "v": # veri tabanından verileri getir
        setup(mode)
 

app = Ursina(borderless = False) # penceresiz özelliği False -> Pencere koy

db = sqlite3.connect("veritabani.db")
imlec = db.cursor()
imlec.execute("CREATE TABLE IF NOT EXISTS " + mode + "(id INTEGER, model TEXT, x INTEGER, y INTEGER, z INTEGER, \
              texture TEXT, scale_x FLOAT, scale_y FLOAT, scale_z FLOAT, rx INTEGER, ry INTEGER, rz INTEGER )") # yürütmek  SQL sorgusu-> Backend
db.close()


player = FirstPersonController()

sky = Sky()

for x in range(15): # zemin inşa ediliyor
    for z in range(15):
        block = Block(position = (x, 0, z))


block_list = []
def setup(mode): # func definition
    db = sqlite3.connect("veritabani.db")
    imlec = db.cursor() # cursor -> imlec demek
    # block tablosundan bütün verileri çek
    imlec.execute("SELECT * FROM "+ mode) # execute -> uygulamak, yürütmek  * (yıldız) anlamı->all
    block_list = imlec.fetchall() # fetchall -> bütün verileri getir
    print(block_list)
    db.close()

    # shift tab tuşu geri tab tuşudur
    
    # item = (1, 'render/scene/block/cube', 3, 1, 6, 'white_cube.png', 2.1000001430511475, 0.5999999046325684, 1.0, 0, 0, 0) 
    # bu bir tuple nesnesidir
    for item in block_list:
        x = item[2]
        y = item[3]
        z = item[4]
        texture = item[5]
        block = Block(position = (x, y, z), texture = texture, zemin = 0)

        block.model = item[1].split("/")[-1] # model
        # ['render', 'scene', 'block', 'cube'] 
        block.scale = (item[6], item[7], item[8])
        block.rotation = (item[9], item[10], item[11])

mode = "level1"

try:
    setup(mode)
except:
    pass

app.run()

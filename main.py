import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
import random
import math

class PetPet:
    def __init__(self, root, scale = 0.2):
        self.root = root
        self.root.attributes('-topmost', True)  # 总是在顶层
        self.root.attributes('-transparentcolor', 'white')  # 设置透明色
        self.root.overrideredirect(True)  # 隐藏窗口装饰（标题栏、边框）
        
        # 设置窗口大小和位置
        self.width = round(min(root.winfo_screenwidth(), root.winfo_screenheight()) * scale)
        self.height = round(min(root.winfo_screenwidth(), root.winfo_screenheight()) * scale)
        self.root.geometry(f'{self.width}x{self.height}+500+400')
        
        # 创建画布
        self.canvas = Canvas(
            root,
            width = self.width,
            height = self.height,
            bg = 'white',
            highlightthickness = 0
        )
        self.canvas.pack()
        
        # 宠物位置
        # self.x = 50
        # self.y = 50
        # self.vx = random.uniform(-2, 2)
        # self.vy = random.uniform(-2, 2)
        
        # 宠物状态
        # self.pet_emotion = "normal"  # normal, happy, sad
        # self.emotion_timer = 0
        
        # 鼠标拖拽
        # self.drag_data = {"x": 0, "y": 0}
        # self.root.bind("<ButtonPress-1>", self.on_drag_start)
        # self.root.bind("<B1-Motion>", self.on_drag_motion)
        # self.root.bind("<ButtonRelease-1>", self.on_drag_stop)
        
        # 右键菜单（退出）
        # self.root.bind("<Button-3>", lambda e: self.root.quit())
        
        # 开始动画循环
        self.animate()
    
    # def on_drag_start(self, event):
    #     """开始拖拽"""
    #     self.drag_data["x"] = event.x
    #     self.drag_data["y"] = event.y
    #     self.vx = 0
    #     self.vy = 0
    #     self.pet_emotion = "happy"
    #     self.emotion_timer = 30
    
    # def on_drag_motion(self, event):
    #     """拖拽移动"""
    #     dx = event.x_root - self.drag_data["x"]
    #     dy = event.y_root - self.drag_data["y"]
        
    #     x = self.root.winfo_x() + dx
    #     y = self.root.winfo_y() + dy
        
    #     self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')
    #     self.drag_data["x"] = event.x_root
    #     self.drag_data["y"] = event.y_root
    
    # def on_drag_stop(self, event):
    #     """停止拖拽"""
    #     self.vx = random.uniform(-2, 2)
    #     self.vy = random.uniform(-2, 2)
    
    def create_pet_image(self):
        return Image.open(".\\Resources\\1.bmp").resize((self.width, self.height))
        # img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        # draw = ImageDraw.Draw(img)
        
        # # 根据情感绘制不同的表情
        # if self.pet_emotion == "happy":
        #     # 身体 - 圆形，黄色
        #     draw.ellipse([20, 20, 80, 80], fill=(255, 200, 0, 255), outline=(200, 150, 0, 255))
        #     # 眼睛 - 高兴的眼睛
        #     draw.ellipse([35, 35, 45, 45], fill=(0, 0, 0, 255))
        #     draw.ellipse([55, 35, 65, 45], fill=(0, 0, 0, 255))
        #     # 嘴 - 笑脸
        #     draw.arc([35, 40, 65, 65], 0, 180, fill=(0, 0, 0, 255), width=2)
        # elif self.pet_emotion == "sad":
        #     # 身体
        #     draw.ellipse([20, 20, 80, 80], fill=(100, 150, 200, 255), outline=(50, 100, 150, 255))
        #     # 眼睛 - 伤心的眼睛
        #     draw.ellipse([35, 35, 45, 45], fill=(0, 0, 0, 255))
        #     draw.ellipse([55, 35, 65, 45], fill=(0, 0, 0, 255))
        #     # 嘴 - 伤心的嘴
        #     draw.arc([35, 50, 65, 65], 180, 360, fill=(0, 0, 0, 255), width=2)
        # else:  # normal
        #     # 身体 - 圆形，紫色
        #     draw.ellipse([20, 20, 80, 80], fill=(200, 100, 200, 255), outline=(150, 50, 150, 255))
        #     # 眼睛
        #     draw.ellipse([35, 35, 45, 45], fill=(0, 0, 0, 255))
        #     draw.ellipse([55, 35, 65, 45], fill=(0, 0, 0, 255))
        #     # 嘴 - 平静的嘴
        #     draw.line([40, 55, 60, 55], fill=(0, 0, 0, 255), width=2)
        
        # return img
    
    def animate(self):
        img = self.create_pet_image()
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        # self.canvas.create_image(0, 0, image=self.tk_image)
        self.root.after(50, self.animate) # 50 ms 后在此调用自己
        # pass
        # """动画循环"""
        # # 更新位置
        # self.x += self.vx
        # self.y += self.vy
        
        # # 边界碰撞反弹
        # if self.x <= 10 or self.x >= self.width - 10:
        #     self.vx *= -1
        # if self.y <= 10 or self.y >= self.height - 10:
        #     self.vy *= -1
        
        # # 随机改变方向
        # if random.random() < 0.02:
        #     self.vx = random.uniform(-2, 2)
        #     self.vy = random.uniform(-2, 2)
        
        # # 更新情感
        # if self.emotion_timer > 0:
        #     self.emotion_timer -= 1
        # else:
        #     self.pet_emotion = "normal"
        
        # # 清空画布
        # self.canvas.delete("all")
        
        # # 绘制宠物
        # img = self.create_pet_image()
        # self.tk_image = ImageTk.PhotoImage(img)
        # self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        
        # # 继续动画
        # self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PetPet")
    pet = PetPet(root)
    root.mainloop()

import tkinter as tk
from datetime import datetime, timedelta
import math
from PIL import Image, ImageTk

# タイムゾーン差
timezones = {
    "Tokyo": 0,
    "California": -17,
    "Greece": -6
}

# 時計の初期角度設定
clocks = {
    "Tokyo": {'angle': 0},
    "California": {'angle': 120},
    "Greece": {'angle': 240}
}

main_center = (250, 250)  # 大円の中心
orbit_radius = 100        # 大円の半径

root = tk.Tk()
root.title("World Clocks")
canvas = tk.Canvas(root, width=500, height=500, bg="#99713d")
canvas.pack()

# 歯車画像の読み込み
gear_images = {
    "Tokyo": Image.open("gear1.png"),       
    "California": Image.open("gear2.png"),  
    "Greece": Image.open("gear3.png")       
}

# 歯車のサイズ調整（少し大きめに設定）
gear_size = 100
for key in gear_images:
    gear_images[key] = gear_images[key].resize((gear_size, gear_size))
gear_photos = {key: ImageTk.PhotoImage(img) for key, img in gear_images.items()}

def draw_clock_face(name, offset_hours):

    # 時計の角度に基づいて座標を計算
    angle_deg = clocks[name]['angle']
    angle_rad = math.radians(angle_deg)
    cx, cy = main_center
    x = cx + orbit_radius * math.cos(angle_rad)
    y = cy + orbit_radius * math.sin(angle_rad)

    # 現在の時刻（UTC + 日本との時差 + 現地時差）
    now = datetime.utcnow() + timedelta(hours=9 + offset_hours)
    hour = now.hour
    is_pm = hour >= 12

    # 昼/夜で背景色を変更
    face_color = "#E3F5FE" if not is_pm else "#FFDBA3"

    # 時計の外円
    canvas.create_oval(x - 80, y - 80, x + 80, y + 80, fill=face_color, outline="black", width=2)

    # 文字盤
    for i in range(1, 13):
        theta = math.radians(i * 30 - 90)
        tx = x + 60 * math.cos(theta)
        ty = y + 60 * math.sin(theta)

        if name == "Tokyo":
            num = ["壱", "弐", "参", "四", "五", "六", "七", "八", "九", "拾", "拾壱", "拾弐"][i-1]
        elif name == "California":
            num = str(i)
        elif name == "Greece":
            greek_nums = ["I", "II", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ"]
            num = greek_nums[i-1]

        canvas.create_text(tx, ty, text=num, font=("Helvetica", 12))

    # 中心の座標保存
    clocks[name]['draw_x'] = x
    clocks[name]['draw_y'] = y

    # 時計の中心に国名を表示（英語表記、上に25pxずらす、おしゃれなフォント）
    canvas.create_text(x, y - 25, text=name, font=("Courier New", 14, "bold"), fill="black")

def draw_clock_hands(name, offset_hours):
    
    now = datetime.utcnow() + timedelta(hours=9 + offset_hours)
    h, m, s = now.hour % 12, now.minute, now.second

    x = clocks[name]['draw_x']
    y = clocks[name]['draw_y']

    # 時針
    hour_angle = math.radians((h + m / 60) * 30 - 90)
    hx = x + 40 * math.cos(hour_angle)
    hy = y + 40 * math.sin(hour_angle)
    canvas.create_line(x, y, hx, hy, width=4)

    # 分針
    minute_angle = math.radians((m + s / 60) * 6 - 90)
    mx = x + 60 * math.cos(minute_angle)
    my = y + 60 * math.sin(minute_angle)
    canvas.create_line(x, y, mx, my, width=2)

    # 秒針（赤）
    second_angle = math.radians(s * 6 - 90)
    sx = x + 70 * math.cos(second_angle)
    sy = y + 70 * math.sin(second_angle)
    canvas.create_line(x, y, sx, sy, fill="red", width=1)

def update():
    canvas.delete("all")

    # 大円のガイド
    cx, cy = main_center
    canvas.create_oval(cx - orbit_radius, cy - orbit_radius,
                       cx + orbit_radius, cy + orbit_radius,
                       outline="#cc9752", dash=(4, 2))
    canvas.create_image(200, 300, image=gear_photos["Tokyo"], tags="background")
    canvas.create_image(350, 225, image=gear_photos["California"], tags="background")
    canvas.create_image(350, 300, image=gear_photos["Greece"], tags="background")
    canvas.create_image(250, 375, image=gear_photos["California"], tags="background")
    canvas.create_image(270, 250, image=gear_photos["Tokyo"], tags="background")
    canvas.create_image(200, 200, image=gear_photos["Greece"], tags="background")
    canvas.create_image(280, 160, image=gear_photos["Greece"], tags="background")
    canvas.create_image(140, 260, image=gear_photos["California"], tags="background")
    canvas.create_image(340, 390, image=gear_photos["Tokyo"], tags="background")



    for name in clocks:
        draw_clock_face(name, timezones[name])
        draw_clock_hands(name, timezones[name])
        clocks[name]['angle'] = (clocks[name]['angle'] + 0.2) % 360  # 回転速度

    root.after(1000 // 60, update)  # 約60fps

update()
root.mainloop()

#必要なモジュールのインポート
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

main_center = (300, 300) # 大円の中心
orbit_radius = 150  # 大円の半径

root = tk.Tk() # ルートをメインウィンドウに設定
root.title("World Clocks") # ウィンドウの名前を設定
canvas = tk.Canvas(root, width=600, height=600, bg="#deb887") # ウィンドウの大きさと背景色の設定
canvas.pack() # 表示

def draw_clock_face(name, offset_hours):
    # 大円の配置 
    angle_deg = clocks[name]['angle']
    angle_rad = math.radians(angle_deg)
    cx, cy = main_center

    # 小円時計を配置
    x = cx + orbit_radius * math.cos(angle_rad)
    y = cy + orbit_radius * math.sin(angle_rad)

    # 時計の外円線
    canvas.create_oval(x - 80, y - 80, x + 80, y + 80, fill="white", outline="black", width=2)

    # 文字盤（数字）
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

    # 時計の中心
    clocks[name]['draw_x'] = x
    clocks[name]['draw_y'] = y

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

def update():
    canvas.delete("all")

    # 大円のガイド
    cx, cy = main_center
    canvas.create_oval(cx - orbit_radius, cy - orbit_radius,
                       cx + orbit_radius, cy + orbit_radius,
                       outline="gray", dash=(4, 2))

    for name in clocks:
        draw_clock_face(name, timezones[name])
        draw_clock_hands(name, timezones[name])
        clocks[name]['angle'] = (clocks[name]['angle'] + 0.2) % 360  # 回転速度

    root.after(16, update)

update()
root.mainloop()

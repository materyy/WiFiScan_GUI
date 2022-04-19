"""
    这个程序实现在tk窗口中显示 表格 & 时序图
    以无线信号测量软件展示界面的表格为准调试
"""
import tkinter as tk
import numpy as np
import matplotlib
from tkinter import ttk
from tkinter.ttk import Style
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 设置matplotlib中可显示中文
matplotlib.rc("font", family="Microsoft YaHei")

# 创建主窗口
win = tk.Tk()
win.title("WiFiScan")

# 设置窗口LOGO
win.iconphoto(True, tk.PhotoImage(file='lock.png'))
# False:该图像仅使用这个窗口，而不是将来创建的toplevels窗口
# 设置为True：将适用于后来创建的所有toplevels窗口


# 获取屏幕宽高
screen_height = win.winfo_screenheight()
screen_width = win.winfo_screenwidth()
item02_width = int(screen_width/7)
item01_width = int(screen_width/14+0.5)

# 设置窗口出现位置以及大小
# win.geometry("%dx%d+%d+%d" % (screen_width, screen_height, 0, 0))   # 四个参数：width x height +x(窗口距屏幕左侧多少) +y(距屏幕顶端）
win.state("zoomed")    # 也可以实现窗口默认最大化，但zoomed参数只能在Windows使用
win.resizable(False, False)    # 不允许改变窗口大小


# 信道占用次数列表（只有表头&1行数据）
frame1 = tk.Frame(win)
frame1.place(x=0, y=0, width=screen_width, height=50)

# 无线信号具体信息列表显示框架
frame2 = tk.Frame(win)
frame2.place(x=0, y=49, width=screen_width+17, height=220)

# 滚动条--frame2中
scrollBar = tk.Scrollbar(frame2)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

# 创建绘图区域
frame3 = tk.Frame(win)
frame3 = tk.LabelFrame(win, text="RSSI[dBm]信号强度时序图↓", background="#cc9999")
frame3.place(relx=0, rely=0.3, relwidth=1, relheight=0.71)
fig = Figure(figsize=(16, 5), dpi=120)
axs = fig.add_axes([0.06, 0.26, 0.91, 0.6])     # 添加区域，x轴y轴起始点，axes区域宽高

# 创建画布
canvas = FigureCanvasTkAgg(fig, master=frame3)
canvas.draw()

canvas.get_tk_widget().pack()

# 生成x，y的值（函数)
x = np.arange(10)
for i in range(72):
    line, = axs.plot(x, i * x, label='$%i$'%i)


# 绘制图形标题
axs.set_title('RSSI[dBm]信号强度时序图             ')    # 图表顶部 横向显示
# axs.set_ylabel('RSSI[dBm]信号强度时序图')  # y轴 纵向显示

# 设置axs区域位置大小
box = axs.get_position()
axs.set_position([box.x0, box.y0,
                 box.width, box.height*0.98])

# 设置-图例-字体大小
fontP = FontProperties()
fontP.set_size('x-small')

# 设置图例
axs.grid(True)
axs.legend(loc='upper center', bbox_to_anchor=(0.5, -0.101),
           fancybox=True, shadow=True, ncol=20, prop=fontP)


"""
    目前没解决问题：
        1. item.insert()每次插入新的一行都会出现在表格第一行，需要逆序实现？？需要吗？
        2. 定义并绑定Treeview组件的鼠标单击事件---需要将这一行对应的无线信号RSSI信号强度在窗口底部的时序图中加粗显示！！
"""
# Treeview组件，13+1列---Channel|1|2|3|...|13----
tree1 = ttk.Treeview(frame1, columns=('Channel', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'), 
                     show="headings")
# Treeview组件，6列，显示表头，带垂直滚动条---（无线信号具体信息）
tree2 = ttk.Treeview(frame2, columns=('序号', 'MAC地址', 'SSID', 'Channel', 'RSSI', '链路质量', 'BssType'),
                     show="headings", yscrollcommand=scrollBar.set)

# 设置Style
style = Style()
"""
    注意！函数Fixed_map()和方法map()都很重要！！
"""


def fixed_map(option):
    return [elm
            for elm in style.map('Treeview', query_opt=option)
            if elm[:2] != ('!disabled', '!selected')]


style.map('Treeview',
          foreground=fixed_map('foreground'),
          background=fixed_map('background'),
          )


# 设置选中条目的背景色&前景色
style.map('Treeview',
          background=[('selected', '#666666')],    # #00aa00(绿色)
          foreground=[('selected', "#fff0f5")],
          )

# 表格显示(左对齐，纵向填充）
tree1.pack(side=tk.LEFT, fill=tk.Y)
tree2.pack(side=tk.LEFT, fill=tk.Y)


# 定义列
tree1["columns"] = ("Channel", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13")
tree2["columns"] = ("序号", "MAC地址", "SSID", "Channel", "RSSI", "链路质量", "BssType")


"""
    《问题》：
        1.下面设置tree1列，怎样循环操作？ " "中的字符串怎样通过 for i in range(12)的i传入？？
"""
# 设置tree1列，列还不显示
tree1.column("Channel", width=item01_width, anchor="center")
tree1.column("1", width=item01_width)
tree1.column("2", width=item01_width)
tree1.column("3", width=item01_width)
tree1.column("4", width=item01_width)
tree1.column("5", width=item01_width)
tree1.column("6", width=item01_width)
tree1.column("7", width=item01_width)
tree1.column("8", width=item01_width)
tree1.column("9", width=item01_width)
tree1.column("10", width=item01_width)
tree1.column("11", width=item01_width)
tree1.column("12", width=item01_width)
tree1.column("13", width=item01_width)
# 设置表头
tree1.heading("Channel", text="Channel")
tree1.heading("1", text="1")
tree1.heading("2", text="2")
tree1.heading("3", text="3")
tree1.heading("4", text="4")
tree1.heading("5", text="5")
tree1.heading("6", text="6")
tree1.heading("7", text="7")
tree1.heading("8", text="8")
tree1.heading("9", text="9")
tree1.heading("10", text="10")
tree1.heading("11", text="11")
tree1.heading("12", text="12")
tree1.heading("13", text="13")


# 设置tree2列，列还不显示
tree2.column("序号", width=item02_width)
tree2.column("MAC地址", width=item02_width)
tree2.column("SSID", width=item02_width)
tree2.column("Channel", width=item02_width)
tree2.column("RSSI", width=item02_width)
tree2.column("链路质量", width=item02_width)
tree2.column("BssType", width=item02_width)
# 设置表头
tree2.heading("序号", text="seq")  # 这个行数序列可以再添加数据的时候自动生成吗？-----可以用索引吗？？
tree2.heading("MAC地址", text="MAC")
tree2.heading("SSID", text="SSID")
tree2.heading("Channel", text="Channel")
tree2.heading("RSSI", text="RSSI")
tree2.heading("链路质量", text="LinQuality(1~100)")
tree2.heading("BssType", text="BssType")

# Treeview组件与垂直滚动条结合
scrollBar.config(command=tree2.yview)


# tree1添加数据
tree1.insert("", 0, text="line1", values=("number", "3", "6", "0", "0", "0",
                                          "0", "0", "13", "0", "0", "4", "1", "13"))
# tree2添加数据
tree2.insert("", 0, text="line1", values=("1", "1", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line2", values=("2", "2", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line3", values=("3", "3", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line4", values=("4", "4", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line5", values=("5", "5", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line6", values=("6", "6", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line7", values=("7", "7", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line8", values=("8", "8", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line9", values=("9", "9", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line10", values=("10", "10", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line11", values=("11", "11", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line12", values=("12", "12", "3", "4", "5", "3", "55"))
tree2.insert("", 0, text="line12", values=("13", "13", "3", "4", "5", "3", "55"))


win.mainloop()

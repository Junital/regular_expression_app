import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sidebar Example")
        
        self.sidebar = tk.Frame(root, bg="gray", width=150)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)
        
        self.content = tk.Frame(root)
        self.content.pack(fill=tk.BOTH, expand=True)
        
        self.create_sidebar_buttons()
        
        self.page1 = tk.Frame(self.content)
        self.page2 = tk.Frame(self.content)
        
        self.show_page(self.page1)  # 默认显示第一个界面
        
    def create_sidebar_buttons(self):
        button1 = tk.Button(self.sidebar, text="Page 1", command=self.show_page1)
        button2 = tk.Button(self.sidebar, text="Page 2", command=self.show_page2)
        
        button1.pack(fill=tk.X)
        button2.pack(fill=tk.X)
        
    def show_page(self, page):
        for widget in self.content.winfo_children():
            widget.grid_forget()  # 移除之前的页面部件
        
        page.grid(row=0, column=0, sticky="nsew")  # 使用grid布局显示新的页面
        
    def show_page1(self):
        self.show_page(self.page1)
        
    def show_page2(self):
        self.show_page(self.page2)

root = tk.Tk()
app = App(root)
root.mainloop()

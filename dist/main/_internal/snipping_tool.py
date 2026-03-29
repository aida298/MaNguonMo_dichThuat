import tkinter as tk

class SnippingTool:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.coordinates = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=3)

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        self.coordinates = (x1, y1, x2 - x1, y2 - y1)
        self.root.quit()

def get_selection_area():
    root = tk.Tk()
    app = SnippingTool(root)
    root.mainloop()
    coords = app.coordinates
    root.destroy()
    return coords
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import pydot
from PIL import Image, ImageTk
import os

class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mind Map Creator")

        self.graph = pydot.Dot(graph_type='graph')
        self.nodes = {}

        # Layout Frames
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Canvas for Mind Map
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.add_node_button = tk.Button(self.button_frame, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save Mind Map", command=self.save_mind_map)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = tk.Button(self.button_frame, text="Load Mind Map", command=self.load_mind_map)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear Mind Map", command=self.clear_mind_map)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save Mind Map", command=self.save_mind_map)
        file_menu.add_command(label="Load Mind Map", command=self.load_mind_map)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def add_node(self):
        node_name = simpledialog.askstring("Input", "Enter node name:")
        if node_name:
            parent_name = simpledialog.askstring("Input", "Enter parent node name (leave blank for root):")
            self.add_node_to_graph(node_name, parent_name)

    def add_node_to_graph(self, node_name, parent_name):
        new_node = pydot.Node(node_name)
        self.graph.add_node(new_node)
        self.nodes[node_name] = new_node

        if parent_name and parent_name in self.nodes:
            self.graph.add_edge(pydot.Edge(self.nodes[parent_name], new_node))

        self.render_graph()

    def render_graph(self):
        self.graph.write_png('mind_map.png')
        self.display_image('mind_map.png')

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((800, 600))
            self.img = ImageTk.PhotoImage(img)
            self.canvas.delete("all")  # Clear the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to display image: {e}")

    def save_mind_map(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".dot", filetypes=[("DOT Files", "*.dot"), ("All Files", "*.*")])
        if file_path:
            self.graph.write(file_path)
            messagebox.showinfo("Success", f"Mind map saved as {file_path}")

    def load_mind_map(self):
        file_path = filedialog.askopenfilename(filetypes=[("DOT Files", "*.dot"), ("All Files", "*.*")])
        if file_path:
            try:
                self.graph = pydot.graph_from_dot_file(file_path)[0]
                self.nodes = {node.get_name(): node for node in self.graph.get_nodes()}
                self.render_graph()
                messagebox.showinfo("Success", "Mind map loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to load mind map: {e}")

    def clear_mind_map(self):
        self.graph = pydot.Dot(graph_type='graph')
        self.nodes = {}
        self.canvas.delete("all")
        messagebox.showinfo("Success", "Mind map cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = MindMapApp(root)
    root.mainloop()

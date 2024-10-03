import tkinter as tk
from tkinter import simpledialog
import pydot
from PIL import Image, ImageTk
import os

class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mind Map Creator")
        
        self.graph = pydot.Dot(graph_type='graph')
        self.nodes = {}
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.add_node_button = tk.Button(self.root, text="Add Node", command=self.add_node)
        self.add_node_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Mind Map", command=self.save_mind_map)
        self.save_button.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Mind Map", command=self.load_mind_map)
        self.load_button.pack(pady=10)

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
        img = Image.open(image_path)
        img.thumbnail((800, 600))
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def save_mind_map(self):
        self.graph.write('mind_map.dot')
        print("Mind map saved as mind_map.dot")

    def load_mind_map(self):
        # For loading logic, you can implement a method to read from dot file and recreate nodes
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MindMapApp(root)
    root.mainloop()

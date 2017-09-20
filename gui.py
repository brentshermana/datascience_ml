import tkinter as tk

import clustering

import logging

CANVAS_DIM = 500 # px
DOT_RADIUS = 2 # px
COLORS = ['red', 'blue']

class gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.create_widgets()
        self.points = []
        logging.basicConfig(filename="log.log")

    def create_widgets(self):
        self.points_count_label = tk.Label(text="0000")
        self.points_count_label.pack()

        single_link_button = tk.Button(self, text="single link", command=self.run_single_link)
        single_link_button.pack()

        k_means_button = tk.Button(self, text="k means", command=self.run_k_means)
        k_means_button.pack()

        clear_button = tk.Button(self, text="clear", command=self.clear)
        clear_button.pack()

        #canvas:
        self.click_canvas = tk.Canvas(self, width=CANVAS_DIM, height=CANVAS_DIM)
        self.click_canvas.bind("<Button-1>", self.canvas_click)
        self.click_canvas.pack()

    def draw_dot(self, center, color='black'):
        self.click_canvas.create_oval(center[0] - DOT_RADIUS, center[1] - DOT_RADIUS, center[0] + DOT_RADIUS, center[1] + DOT_RADIUS, outline=color)
    def draw_center(self, center, color='black'):
        self.click_canvas.create_oval(center[0] - DOT_RADIUS*5, center[1] - DOT_RADIUS*5, center[0] + DOT_RADIUS*5, center[1] + DOT_RADIUS*5, outline='black', fill=color)
    def canvas_click(self, event):
        point = (event.x, event.y)
        self.points.append( point )
        self.draw_dot(point, 'black')
        self.points_count_label['text'] = str(len(self.points))

    def run_single_link(self):
        print("RUNNING SINGLE LINK")
        print("== Points:")
        print(self.points)
        #for consistency, we'll make the group with the lowest y value the blue one
        clusters = clustering.singlelink(self.points, 2)
        miny = 1000000
        blue_set = None
        for c in clusters:
            for pi in c:
                if self.points[pi][1] < miny:
                    miny = self.points[pi][1]
                    blue_set = c

        # now, draw the colored points:
        self.click_canvas.delete("all")
        for c in clusters:
            color = 'red'
            if (c is blue_set): color = 'blue'
            print("== Group {}".format(color))
            print(c)
            for pi in c:
                self.draw_dot(self.points[pi], color=color)

    def run_k_means(self):
        print("RUNNING KMEANS")
        print("Points")
        print(self.points)
        print("Starting Centers: {}".format([self.points[0], self.points[1]]))
        centers, clusters = clustering.kmeans(self.points, [self.points[0], self.points[1]] )
        # whichever center is lower is the blue center
        blue_center = centers[0]
        if centers[1][1] < centers[0][1]:
            blue_center = centers[1]

        # draw the centers and points
        self.click_canvas.delete("all")
        for center_i, center in enumerate(centers):
            color = None
            if center is blue_center:
                color='blue'
            else:
                color='red'
            print("Cluster {} with center {}".format(color, center))
            print("Cluster Points:")
            print(clusters[center_i])
            self.draw_center(center, color=color)
            for cluster_coord in clusters[center_i]:
                self.draw_dot(cluster_coord, color=color)


    def clear(self):
        logging.debug("== CLEAR ==")
        self.click_canvas.delete("all")
        self.points = []
        self.points_count_label['text'] = len(self.points)

if __name__ == '__main__':
    g = gui()
    g.mainloop()

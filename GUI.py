import tkinter as tk
import tkinter.messagebox as msgb
from random import sample as random_sample
from random import randint as random_int

from Operations import Operations

from Polygon import Polygon
from Point import Point
from Line import Line
from KDTree import KDTree


class GUI():
    def __init__(self):
        self._root = tk.Tk()
        self._root.update_idletasks()
        self._root.attributes('-fullscreen', True)
        geometry = self._root.winfo_geometry()
        xy = geometry.split("x")
        xy[1] = xy[1].split("+")[0]
        self._root.attributes('-fullscreen', False)

        self._root.geometry(
            f'{int(int(xy[0]) * 0.6)}x{int(int(xy[1]) * 0.6)}+{int(int(xy[0]) * 0.2)}+{int(int(xy[1]) * 0.2)}')
        self._root.resizable(False, False)
        # self.master = tk.Frame(self.root, bg="azure")
        self._master = tk.Frame(self._root, bg="honeydew4")
        self._master.grid(sticky="nswe")
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._master.grid_columnconfigure(0, weight=5)
        self._master.grid_columnconfigure(1, weight=25)
        self._master.grid_rowconfigure(0, weight=1)

        self.data = dict({"points": [], "lines": [], "polygons": []})
        self._create_widgets()

    def start(self):
        self._root.mainloop()

    def _create_widgets(self):
        self._root.winfo_toplevel().title("Computational geometry - Krzysztof Garbarz 2021")

        self._menu = tk.Frame(self._master, bg="honeydew4")
        self._menu.grid(column=0, row=0, sticky="nswe")
        self._menu.grid_columnconfigure(0, weight=1, min=250)
        self._menu.grid_rowconfigure(0, weight=1, uniform='row')
        self._menu.grid_rowconfigure(1, weight=1, uniform='row')

        self._window = tk.Frame(self._master, bg="black")
        self._window.grid(column=1, row=0, sticky="nswe")

        self._canvas = tk.Canvas(self._window, bg="azure", cursor="cross", bd=0)

        self._canvas.pack(fill="both", expand=True, padx=(1, 0))
        self._window.pack_propagate(False)

        self._buttons = tk.Frame(self._menu, bg="honeydew4")
        self._buttons.grid(row=0, column=0, sticky="nswe", padx=(5, 5), pady=(5, 0))
        self._buttons.grid_columnconfigure(0, weight=1)
        # self._buttons.grid_rowconfigure(0, weight=1)

        for i in range(0, 7):
            button = tk.Button(self._buttons)
            button.grid(row=i, column=0, sticky="nwe", padx=(5, 5), pady=(5 if i < 4 else 15, 0))

        label = tk.Label(self._menu)
        label.grid(row=1, column=0, sticky="swe", padx=(5, 5), pady=(1, 1))

        self._restore("")

    def _restore(self, ev):
        self._canvas.unbind("<ButtonPress-1>")
        self._canvas.bind("<ButtonPress-1>", self._selector)

        for i, but in enumerate(self._buttons.winfo_children()):
            but.unbind("<ButtonPress-1>")
            if i == 0:
                but.config(text="Add points")
                but.bind("<ButtonPress-1>", self._add_point)
            elif i == 1:
                but.config(text="Generate random points (10)")
                but.bind("<ButtonPress-1>", self._generate_random_points)
            elif i == 2:
                but.config(text="Find convex hull for points in canvas")
                but.bind("<ButtonPress-1>", self._convex_hull)
            elif i == 3:
                but.config(text="Generate KD tree for points in canvas")
                but.bind("<ButtonPress-1>", self._kd_tree)
            elif i == 4:
                but.config(text="Add line")
                but.bind("<ButtonPress-1>", self._add_line)
            elif i == 5:
                but.config(text="Add polygon")
                but.bind("<ButtonPress-1>", self._add_polygon)
            elif i == 6:
                but.config(text="Clear canvas")
                but.bind("<ButtonPress-1>", self._clear)
            but.config(state="normal", relief=tk.RAISED)

        if len(self.data["lines"]) > 0 and isinstance(self.data["lines"][-1], Point):
            del self.data["lines"][-1]

        if len(self.data["polygons"]) > 0 and not isinstance(self.data["polygons"][-1], Polygon):
            del self.data["polygons"][-1]

        self._menu.winfo_children()[1].config(text="Author: Krzysztof Garbarz", fg="black")

    def _selector(self, event):
        selected = None
        for point in self.data["points"]:
            if point.x - 3 <= event.x and point.x + 3 >= event.x and point.y - 3 <= event.y and point.y + 3 >= event.y:
                selected = point
                break

        if not selected:
            for line in self.data["lines"]:
                if (Operations.check_if_point_on_line(Point(event.x, event.y), line)):
                    selected = line
                    break

        if not selected:
            for polygon in self.data["polygons"]:
                if (Operations.is_point_in_polygon(Point(event.x, event.y), polygon.points)):
                    selected = polygon
                    break

        if selected:
            menu = tk.Menu(self._root, tearoff=0)
            if isinstance(selected, Point):
                menu.add_command(label="Find functional equation", command=lambda: self._find_other_point(selected))
                menu.add_command(label="Specify location due to line",
                                 command=lambda: self._find_other_line(selected, 0))
                menu.add_command(label="Specify location due to polygon",
                                 command=lambda: self._find_other_polygon(selected))
            elif isinstance(selected, Line):
                menu.add_command(label="Rotate in relation to point",
                                 command=lambda: self._rotator(selected))
                menu.add_command(label="Find crossing point of lines",
                                 command=lambda: self._find_other_line(selected, 1))
            else:
                if len(selected.points) == 3:
                    menu.add_command(
                        label="Calculate triangle area",
                        command=lambda: msgb.showinfo("Triangle area",
                                                      "Area of selected triangle is equal to " +
                                                      str(Operations.findTriangleArea(selected.points)) + "px"))
            menu.add_separator()
            menu.add_command(label="Remove", command=lambda: self._remover(selected))
            menu.tk_popup(event.x_root, event.y_root)

    def _remover(self, selected):
        if isinstance(selected, Point):
            self.data["points"].remove(selected)
        elif isinstance(selected, Line):
            self.data["lines"].remove(selected)
        else:
            self.data["polygons"].remove(selected)
        self._paint()

    def _add_point(self, ev):
        self._canvas.bind("<ButtonPress-1>", self._create_point)
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")
        ev.widget.config(text=f"-> {ev.widget['text']} <-", state="active")
        ev.widget.bind("<ButtonPress-1>", self._restore)

    def _create_point(self, event):
        _ok = True
        for point in self.data["points"]:
            if point.x - 3 <= event.x and point.x + 3 >= event.x and point.y - 3 <= event.y and point.y + 3 >= event.y:
                _ok = False
            if not _ok:
                break
        if _ok:
            self.data["points"].append(Point(event.x, event.y))
            self._paint()
        else:
            self._menu.winfo_children()[1].config(text="This place is occupied by another point!", fg="firebrick2")

    def _add_line(self, ev):
        self._canvas.bind("<ButtonPress-1>", self._create_line)
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")
        ev.widget.config(text=f"-> {ev.widget['text']} <-", state="active")
        ev.widget.bind("<ButtonPress-1>", self._restore)

    def _create_line(self, event):
        _ok = True

        if len(self.data["lines"]) == 0 or (
                len(self.data["lines"]) > 0 and isinstance(self.data["lines"][-1], Line)):
            self.data["lines"].append(Point(event.x, event.y))
        else:
            self.data["lines"][-1] = Line(self.data["lines"][-1], Point(event.x, event.y))
        self._paint()

    def _add_polygon(self, ev):
        self._canvas.bind("<ButtonPress-1>", self._create_polygon)
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")
        ev.widget.config(text=f"-> {ev.widget['text']} <-", state="active")
        ev.widget.bind("<ButtonPress-1>", self._restore)

    def _create_polygon(self, event):
        if len(self.data["polygons"]) == 0 or (
                len(self.data["polygons"]) > 0 and isinstance(self.data["polygons"][-1], Polygon)):
            self.data["polygons"].append([Point(event.x, event.y)])
            self._paint()
        else:
            _end = False
            if len(self.data["polygons"][-1]) > 2:
                point = self.data["polygons"][-1][0]
                if point.x - 3 <= event.x and point.x + 3 >= event.x and point.y - 3 <= event.y and point.y + 3 >= event.y:
                    _end = True

                if _end:
                    self.data["polygons"][-1] = Polygon(self.data["polygons"][-1])
                    self._paint()
                    return

            for point in self.data["polygons"][-1]:
                if point.x - 3 <= event.x and point.x + 3 >= event.x and point.y - 3 <= event.y and point.y + 3 >= event.y:
                    self._menu.winfo_children()[1].config(text="This place is occupied by another point!",
                                                          fg="firebrick2")
                    _end = True
            if not _end:
                self.data["polygons"][-1].append(Point(event.x, event.y))
                self._paint()

    def _paint(self):
        self._canvas.delete("all")
        self._menu.winfo_children()[1].config(text="Author: Krzysztof Garbarz", fg="black")
        for point in self.data["points"]:
            if point.mark:
                self._canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, outline="limegreen")
            else:
                self._canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3)

        for line in self.data["lines"]:
            if isinstance(line, Line):
                if line.mark:
                    self._canvas.create_line(line.start.x, line.start.y, line.end.x, line.end.y, fill="limegreen")
                else:
                    self._canvas.create_line(line.start.x, line.start.y, line.end.x, line.end.y)
            else:
                self._canvas.create_oval(line.x - 3, line.y - 3, line.x + 3, line.y + 3, outline="firebrick2")

        for polygon in self.data["polygons"]:
            if isinstance(polygon, Polygon):
                for i in range(0, len(polygon.points) - 1):
                    self._canvas.create_line(polygon.points[i].x, polygon.points[i].y,
                                             polygon.points[i + 1].x, polygon.points[i + 1].y)
                self._canvas.create_line(polygon.points[-1].x, polygon.points[-1].y,
                                         polygon.points[0].x, polygon.points[0].y)
            else:
                for i in range(0, len(polygon)):
                    if i != len(polygon) - 1:
                        self._canvas.create_line(polygon[i].x, polygon[i].y,
                                                 polygon[i + 1].x, polygon[i + 1].y, fill="firebrick2")

                    self._canvas.create_oval(polygon[i].x - 3, polygon[i].y - 3,
                                             polygon[i].x + 3, polygon[i].y + 3, outline="firebrick2")

    def _find_other_point(self, point: Point):
        point.mark = True
        self._paint()
        msgb.showinfo("Information", "Please select other point to calculate equation.")
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")

        self._menu.winfo_children()[1].config(text="Select second point to calculate functional equation.", fg="black")
        self._canvas.bind("<ButtonPress-1>", lambda ev: self._point_selector(ev, point))

    def _point_selector(self, event, point1: Point):
        selected = None
        for point2 in self.data["points"]:
            if point2.x - 3 <= event.x and point2.x + 3 >= event.x and point2.y - 3 <= event.y and point2.y + 3 >= event.y:
                selected = point2
                break

        if selected:
            if point1 != point2:
                msgb.showinfo(
                    "Equation", "The equation is: " + Operations.get_line_cartesian_formula(Line(point1, point2)))
                point1.mark = False
                self._paint()
                self._restore(event)
            else:
                msgb.showerror("Warning", "Second point cannot be equal to first one!")

    def _find_other_line(self, point, type: int):
        point.mark = True
        self._paint()
        if type == 0:
            msgb.showinfo("Information", "Please select line to calculate relative position.")
        elif type == 1:
            msgb.showinfo("Information", "Please select second line to calculate crossing point.")
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")

        if type == 0:
            self._menu.winfo_children()[1].config(text="Select line to calculate relative position.", fg="black")
        elif type == 1:
            self._menu.winfo_children()[1].config(text="Select second line to calculate crossing point.", fg="black")
        self._canvas.bind("<ButtonPress-1>", lambda ev: self._line_selector(ev, point, type))

    def _line_selector(self, event, line1, type):
        selected = None
        for line in self.data["lines"]:
            if (Operations.check_if_point_on_line(Point(event.x, event.y), line)):
                selected = line
                break

        if selected:
            if type == 0:
                msgb.showinfo(
                    "Result", "The point is " + (
                        "on right side of line" if Operations.which_side(selected, point) == 1 else (
                            "on left side of line" if Operations.which_side(selected, point) == -1 else "on the line")))
            elif type == 1:
                if line1 != selected:
                    msgb.showinfo(
                        "Result", "The crossing point is " + str(Operations.crossingPointCartesian(line1, selected)) +
                                  "\n\nWARNING! The point may not be a visible crossing point" +
                                  " since its checking for LINE intersection not SEGMENT!")
                else:
                    msgb.showerror("Warning", "Second line cannot be equal to first one!")
            line1.mark = False
            self._paint()
            self._restore(event)

    def _find_other_polygon(self, point):
        point.mark = True
        self._paint()
        msgb.showinfo("Information", "Please select polygon to calculate relative position.")
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")

        self._menu.winfo_children()[1].config(text="Select polygon to calculate relative position.", fg="black")
        self._canvas.bind("<ButtonPress-1>", lambda ev: self._polygon_selector(ev, point))

    def _polygon_selector(self, event, point):
        selected = None
        for polygon in self.data["polygons"]:
            if (Operations.is_point_in_polygon(Point(event.x, event.y), polygon.points)):
                selected = polygon
                break
        if selected:
            msgb.showinfo(
                "Result", "The point is: " + (
                    "inside the polygon" if Operations.is_point_in_polygon(point, selected.points)
                    else "outside the polygon"))
            point.mark = False
            self._paint()
            self._restore(event)

    def _rotator(self, line: Line):
        line.mark = True
        self._paint()
        msgb.showinfo("Information", "Please add point to relate rotation.")
        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")

        self._menu.winfo_children()[1].config(text="Add point to relate rotation.", fg="black")
        self._canvas.bind("<ButtonPress-1>", lambda ev: self._rotation_point(ev, line))

    def _rotation_point(self, event, line):
        from copy import deepcopy
        self._canvas.unbind("<ButtonPress-1>")
        rotation_point = Point(event.x, event.y)
        line_start = deepcopy(line)
        rotation_point.mark = True
        self.data["points"].append(rotation_point)
        self._paint()
        self._canvas.bind('<Motion>', lambda ev: self._motion(ev, line, line_start, rotation_point))
        self._canvas.bind('<ButtonPress-1>', lambda ev: self._motion(ev, line, line_start, rotation_point, True))

    def _motion(self, event, line, rel_line, rotation_point, save=False):
        if save:
            line.mark = False
            del self.data["points"][-1]
            self._canvas.unbind('<Motion>')
            self._restore(event)
            self._paint()
        else:
            n_line = Operations.rotateLine(
                (rotation_point.x - event.x), line.start, line.end, rotation_point)
            ind = self.data["lines"].index(line)
            self.data["lines"][ind].start = n_line.start
            self.data["lines"][ind].end = n_line.end
            self._paint()

    def _generate_random_points(self, event):
        self._root.update()
        w, h = self._canvas.winfo_width() - 5, self._canvas.winfo_height() - 5
        xy: List[List[float]] = [random_sample(range(2, w), 10), random_sample(range(2, h), 10)]

        _ok = True
        for i in range(len(xy[0])):
            for point in self.data["points"]:
                while point.x - 3 <= xy[0][i] and point.x + 3 >= xy[0][i] and \
                        point.y - 3 <= xy[1][i] and point.y + 3 >= xy[1][i]:
                    xy[0][i] = random_int(2, w)
                    xy[1][i] = random_int(2, h)
            self.data["points"].append(Point(xy[0][i], xy[1][i]))

        self._paint()

    def _clear(self, event):
        self.data = dict({"points": [], "lines": [], "polygons": []})
        self._paint()

    def _convex_hull(self, event):
        from copy import deepcopy
        if len(self.data["points"]) < 3:
            msgb.showerror(title="Error", message="Not enough points on canvas.\nYou can use random point generator.")
            self._restore(event)
            return "break"

        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")
        event.widget.config(text=f"-> {event.widget['text']} <-")

        resp: bool = msgb.askokcancel(title="Confirmation",
                                      message="Warning! All lines and polygons created prior to this operation"
                                              " will be permanently deleted. Do you wish to continue?")

        if resp:
            self.data["lines"] = []
            self.data["polygons"] = []

            points: List[Point] = Operations.graham_scan(deepcopy(self.data["points"]))

            for i in range(len(points) - 1):
                self.data["lines"].append(Line(points[i], points[i + 1]))
            self.data["lines"].append(Line(points[-1], points[0]))

        self._paint()
        self._restore(event)
        return "break"

    def _kd_tree(self, event):
        if len(self.data["points"]) < 2:
            msgb.showerror(title="Error", message="Not enough points on canvas.\nYou can use random point generator.")
            self._restore(event)
            return "break"

        for but in self._buttons.winfo_children():
            but.config(state="disable")
            but.unbind("<ButtonPress-1>")
        event.widget.config(text=f"-> {event.widget['text']} <-")

        resp: bool = msgb.askokcancel(title="Confirmation",
                                      message="Warning! All lines and polygons created prior to this operation"
                                              " will be permanently deleted. Do you wish to continue?")
        if resp:
            self.data["lines"] = []
            self.data["polygons"] = []

            kd = KDTree()
            kd.generate(self.data["points"])

            for point in self.data["points"]:
                neighbor = kd.find_nearest_neighbor(point)
                self.data["lines"].append(Line(point, neighbor))

        self._paint()
        self._restore(event)
        return "break"

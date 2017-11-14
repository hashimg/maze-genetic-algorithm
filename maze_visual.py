import turtle


class ScreenPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GridPosition:
    def __init__(self, r, c):
        self.r = r
        self.c = c


class Maze:
    colors = {'C': "red", 'M': "green", 'x': "black", '-': "yellow",
              'mouse': "gray", 'cheese': "gold"}
    square_size = 80

    def __init__(self, values):
        self.row_dim = len(values)
        self.col_dim = len(values[0])
        self.values = values
        self.origin = ScreenPosition(0, 0)
        self.visualized = False
        self.cheese_pos = None
        self.pen_maze = None
        self.InitializeGraphics()
        self.mouse = self.Mouse(self, self.square_size // 3, self.colors['mouse'])
        self.FindStartFinish()

    def Reset(self):
        self.pen_maze.clear()
        self.mouse.Reset()

    def ResetMouse(self):
        self.mouse.Reset()
        self.mouse.Draw()

    def InitializeGraphics(self):
        self.pen_maze = turtle.Turtle()
        screen = self.pen_maze.getscreen()
        screen.setworldcoordinates(0, 0, 1000, 1000)
        self.pen_maze.speed(0)
        turtle.tracer(0, 0)
        self.pen_maze.hideturtle()

    def FindStartFinish(self):
        for r in range(self.row_dim):
            for c in range(self.col_dim):
                if self.values[r][c] == 'C':
                    self.cheese_pos = GridPosition(r, c)
                elif self.values[r][c] == 'M':
                    self.mouse.set_start(r, c)

    def Visualize(self):
        for r in range(self.row_dim):
            for c in range(self.col_dim):
                x, y = self.Convert(r, c)
                self.DrawSquare(x, y, self.colors[self.values[r][c]])
        turtle.update()
        self.mouse.Draw()
        self.DrawCheese()
        self.visualized = True

    def RunMaze(self, moves):
        if not self.visualized: self.Visualize()
        r = self.mouse.start.r
        c = self.mouse.start.c
        for el in moves:
            new_r, new_c = r, c
            if el == 'U':
                new_r += 1
            elif el == 'D':
                new_r -= 1
            elif el == 'R':
                new_c += 1
            elif el == 'L':
                new_c -= 1
            else:
                print('Unrecognized Command')
                return
            if 0 <= new_r and new_r < self.row_dim \
                    and 0 <= new_c and new_c < self.col_dim:
                if self.values[new_r][new_c] in ['M', '-', 'C']:
                    r, c = new_r, new_c
            self.mouse.Move(r, c, True)
            self.mouse.Draw()
            turtle.update()
        if r == self.cheese_pos.r and c == self.cheese_pos.c:
            print('FOUND the CHEESE!')
        else:
            print('No CHEESE :-(')

    def Convert(self, row, col):
        x = self.square_size * col + self.origin.x
        y = self.square_size * row + self.origin.y
        return x, y

    def Center(self, x, y):
        center_x = x + self.square_size // 2
        center_y = y + self.square_size // 2
        return center_x, center_y

    def DrawSquare(self, ll_x, ll_y, color):
        pen = self.pen_maze
        pen.pu()
        pen.goto(ll_x, ll_y)
        pen.begin_fill()
        pen.color(color)
        pen.pd()
        pen.goto(ll_x + self.square_size, ll_y)
        pen.goto(ll_x + self.square_size, ll_y + self.square_size)
        pen.goto(ll_x, ll_y + self.square_size)
        pen.goto(ll_x, ll_y)
        pen.end_fill()

    def DrawCheese(self):

        x, y = self.Convert(self.cheese_pos.r, self.cheese_pos.c)
        x = x + 10
        y = y + 10
        pen = self.pen_maze
        pen.pu()

        def DrawHole(x, y):
            pen.color("black")
            pen.pu()
            pen.goto(x, y)
            pen.pd()
            pen.dot(5)

        # Draw the wedge of cheese
        pen.goto(x, y)
        pen.begin_fill()
        pen.color(self.colors["cheese"])
        pen.pd()
        pen.goto(x + 40, y)
        pen.goto(x + 40, y + 30)
        pen.goto(x, y)
        pen.end_fill()

        # Draw the swiss cheese holes
        DrawHole(x + 20, y + 5)
        DrawHole(x + 30, y + 15)
        DrawHole(x + 35, y + 10)

    class Mouse:
        def __init__(self, maze, size, color):
            self.maze = maze
            self.size_head = size
            self.size_ear = size // 2
            self.color = color
            self.start = None
            self.pos = None
            self.pen = turtle.Turtle()

        def set_start(self, r, c):
            self.start = GridPosition(r, c)
            self.pos = self.start

        def Reset(self):
            self.pen.clear()
            self.pos = self.start

        def Move(self, row, col, visualize):
            self.pen.pu()
            # if want to see line between moves ...
            if visualize:
                x, y = self.maze.Convert(self.pos.r, self.pos.c)
                cx, cy = self.maze.Center(x, y)
                self.pen.goto(cx, cy)
                self.pen.pd()
            # set new position and draw line to show move
            self.pos = GridPosition(row, col)
            x, y = self.maze.Convert(self.pos.r, self.pos.c)
            cx, cy = self.maze.Center(x, y)
            self.pen.goto(cx, cy)

        def Draw(self):
            x, y = self.maze.Convert(self.pos.r, self.pos.c)
            cx, cy = self.maze.Center(x, y)
            # Draw Head
            self.pen.pu()
            self.pen.goto(cx, cy)
            self.pen.color(self.color)
            self.pen.pd()
            self.pen.dot(self.size_head)
            # Draw Left Ear
            self.pen.goto(cx - self.size_head // 2, cy + self.size_head // 2)
            self.pen.dot(self.size_ear)
            # Draw Right Ear
            self.pen.pu()
            self.pen.goto(cx + self.size_head // 2, cy + self.size_head // 2)
            self.pen.dot(self.size_ear)







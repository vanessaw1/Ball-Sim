from tkinter import *
from collections import deque
import math

class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.state("zoomed")
        self.ballStack = deque([])
        self.countVar = StringVar()

        # Begin Constants
        self.DT = 0.1
        self.BALLLIMIT = 25
        self.G = 1
        self.WIDTH = 1600
        self.HEIGHT = 1000
        # End Constants

        self.pack()
        self.createWigets()
        self.moveBalls()

    def createWigets(self):
        # Simulation - Canvas
        self.canvas = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="WHITE")
        self.canvas.grid(row=0, column=0, rowspan=10)
        self.canvas.bind("<Button-1>", self.createBall)  # On clicking the mouse

        # Color Chooser - Label + Radio Buttons
        self.color = Label(self, text="Set Next Ball Color:").grid(row=0, column=1, columnspan=2, sticky=S)
        self.colorVar = StringVar()
        self.cRed = Radiobutton(self, text="Red", variable=self.colorVar, indicatoron=0, value="RED", bg="RED").grid(row=1, column=1, sticky=W+E)
        self.cOrange = Radiobutton(self, text="Orange", variable=self.colorVar, indicatoron=0, value="ORANGE", bg="ORANGE", width=13).grid(row=1, column=2, sticky=W+E)
        self.cYellow = Radiobutton(self, text="Yellow", variable=self.colorVar, indicatoron=0, value="YELLOW", bg="YELLOW").grid(row=2, column=1, sticky=W+E)
        self.cGreen = Radiobutton(self, text="Green", variable=self.colorVar, indicatoron=0, value="GREEN", bg="GREEN").grid(row=2, column=2, sticky=W+E)
        self.cLightBlue = Radiobutton(self, text="Light Blue", variable=self.colorVar, indicatoron=0, value="LIGHT BLUE", bg="LIGHT BLUE").grid(row=3, column=1, sticky=W+E)
        self.cBlue = Radiobutton(self, text="Blue", variable=self.colorVar, indicatoron=0, value="BLUE", bg="BLUE").grid(row=3, column=2, sticky=W+E)
        self.cPurple = Radiobutton(self, text="Purple", variable=self.colorVar, indicatoron=0, value="PURPLE", bg="PURPLE").grid(row=4, column=1, sticky=W+E)
        self.cBlack = Radiobutton(self, text="Black", variable=self.colorVar, indicatoron=0, value="BLACK", bg="BLACK").grid(row=4, column=2, sticky=W+E)
        self.colorVar.set("BLACK")  # Default color on start

        # Ball Radius - Label + Scale
        self.radius_desc = Label(self, text="Set Next Ball Radius:").grid(row=5, column=1)
        self.radius = Scale(self, from_=1, to_=50)
        self.radius.set(20)
        self.radius.grid(row=5, column=2)

        # Set Gravity - Label + Radio Buttons
        self.gravity_desc = Label(self, text="Set Gravity:").grid(row=6, column=1, columnspan=2, sticky=S)
        self.gravityVar = IntVar()
        self.gOn = Radiobutton(self, text="On", variable=self.gravityVar, value=self.G, command=self.switchGravity).grid(row=7, column=1, sticky=N)
        self.gOff = Radiobutton(self, text="Off", variable=self.gravityVar, value=0, command=self.switchGravity).grid(row=7, column=2, sticky=N)
        self.gravityVar.set(0)

        # Remove Last Ball - Button
        self.remove_last = Button(self, text="Remove Last Ball Created", command=self.removeBall)
        self.remove_last.grid(row=8, column=1, columnspan=2)

        # Clear All - Button
        self.clear = Button(self, text="Clear All", command=self.clearCanvas).grid(row=9, column=1, columnspan=2)

        # Ball Count - Label
        self.countVar.set("Ball Count: %i\n[Limit %i]" % (len(self.ballStack), self.BALLLIMIT))
        self.count = Label(self, textvariable=self.countVar, bg="WHITE").grid(row=0, column=0)

    def clearCanvas(self):
        for ball in self.ballStack:
            ball.deleteBall()
        self.ballStack = deque([])
        self.updateBallCount()

    def createBall(self, event):
        self.ballStack.append(ball(self.canvas, event, self.radius.get(), self.DT, self.gravityVar.get(), self.colorVar.get(), self.WIDTH, self.HEIGHT))
        if len(self.ballStack) > self.BALLLIMIT:
            self.ballStack.popleft().deleteBall()
        self.updateBallCount()

    def removeBall(self):
        if len(self.ballStack) == 0:
            pass
        else:
            self.ballStack.pop().deleteBall()
        self.updateBallCount()

    def switchGravity(self):
        for ball in self.ballStack:
            ball.toggleGravity(self.gravityVar.get())

    def updateBallCount(self):
        self.countVar.set("Ball Count: %i\n[Limit %i]" % (len(self.ballStack), self.BALLLIMIT))

    def moveBalls(self):
        for i in range(len(self.ballStack)):
            self.ballStack[i].animation()
            self.ballStack[i].update()
        for i in range(len(self.ballStack)):
            for j in range(i):
                self.ballStack[i].checkCollision(self.ballStack[j])
        self.canvas.after(10, self.moveBalls)

class ball():
    def __init__(self, canvas, event, r, dt, g, color, width, height):
        self.canvas = canvas
        self.x = event.x
        self.y = event.y
        self.r = r
        self.dt = dt
        self.g = g
        self.x_velocity = 5
        self.y_velocity = 5
        self.mass = r

        # Boundaries
        self.floor = height
        self.ceiling = 0
        self.lwall = 0
        self.rwall = width

        self.ballDrawing = canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, outline=color, fill=color)

    def animation(self):
        # y-axis movement
        if self.floor - self.r < self.y or self.y < self.ceiling + self.r:
            self.y_velocity = -self.y_velocity
        else:
            self.y_velocity += self.g * self.dt
        self.y += self.y_velocity

        # x-axis movement
        if self.rwall - self.r < self.x or self.x < self.lwall + self.r:
            self.x_velocity = -self.x_velocity
        self.x += self.x_velocity

    def checkCollision(self, ball2):
        distance = math.sqrt(math.pow(self.x - ball2.x, 2) + math.pow(self.y - ball2.y, 2))
        if distance < self.r + ball2.r:
            tempx1 = (self.x_velocity * (self.mass - ball2.mass) + (2 * ball2.mass * ball2.x_velocity)) / (self.mass + ball2.mass)
            tempy1 = (self.y_velocity * (self.mass - ball2.mass) + (2 * ball2.mass * ball2.y_velocity)) / (self.mass + ball2.mass)
            tempx2 = (ball2.x_velocity * (ball2.mass - self.mass) + (2 * self.mass * self.x_velocity)) / (self.mass + ball2.mass)
            tempy2 = (ball2.y_velocity * (ball2.mass - self.mass) + (2 * self.mass * self.y_velocity)) / (self.mass + ball2.mass)
            self.x_velocity = tempx1
            self.y_velocity = tempy1
            ball2.x_velocity = tempx2
            ball2.y_velocity = tempy2

    def update(self):
        self.canvas.move(self.ballDrawing, self.x_velocity, self.y_velocity)

    def toggleGravity(self, gravValue):
        self.g = gravValue

    def deleteBall(self):
        self.canvas.delete(self.ballDrawing)

root = Tk()
root.title("Ball Simulator")
gui = GUI(master=root)
gui.mainloop()
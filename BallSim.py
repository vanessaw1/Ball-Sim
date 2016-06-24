from tkinter import *
from collections import deque

class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.minsize(width=1920, height=1080)
        master.maxsize(width=1920, height=1080)
        self.ballStack = deque([])
        self.countVar = StringVar()

        # Begin Constants
        self.DT = 0.075  # In seconds - Affects smoothness (0.075)
        self.UPDATETIME = 400  # In milliseconds - Affects animation speed (400)
        self.BALLLIMIT = 20
        self.G = 10
        # End Constants

        self.pack()
        self.createWigets()

    def createWigets(self):
        # Simulation - Canvas
        self.sim = Canvas(self, width=1300, height=1000, bg="WHITE")
        self.sim.grid(row=0, column=0, rowspan=10)
        self.sim.bind("<Button-1>", self.createBall)  # On clicking the mouse

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
        self.gravityVar.set(self.G)

        # Remove Last Ball - Button
        self.remove_last = Button(self, text="Remove Last Ball Created", command=self.removeBall)
        self.remove_last.grid(row=8, column=1, columnspan=2)

        # Clear All - Button
        self.clear = Button(self, text="Clear All", command=self.clearCanvas).grid(row=9, column=1, columnspan=2)

        # Ball Count - Label
        self.countVar.set("Ball Count: %i\n[Limit %i]" % (len(self.ballStack), self.BALLLIMIT))
        self.count = Label(self, textvariable=self.countVar, bg="WHITE").grid(row=0, column=0)

    def clearCanvas(self):
        print("Clearing screen...")
        for ball in self.ballStack:
            ball.deleteBall()
        self.ballStack = deque([])
        self.updateBallCount()
        print("Cleared!")

    def createBall(self, event):
        self.ballStack.append(ball(self.sim, event, self.radius.get(), self.DT, self.gravityVar.get(), self.colorVar.get(), self.UPDATETIME))
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

class ball():
    def __init__(self, canvas, event, r, dt, g, color, updateTime):
        self.x = event.x
        self.y = event.y
        self.canvas = canvas
        self.speedX = 5
        self.speedY = 0
        self.floor = 1000
        self.ceiling = 0
        self.lwall = 0
        self.rwall = 1300
        self.dt = dt
        self.r = r
        self.g = g
        self.updateTime = updateTime

        #print("Ball's position:", event.x, event.y)
        self.ballDrawing = canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, outline=color, fill=color)
        self.animation(self.dt)
        print("Ball Placed:", self.ballDrawing)

    def animation(self, dt):
        self.dt = dt

        # y-axis movement
        if self.ceiling + self.r < self.y < self.floor - self.r:
            self.speedY += self.g * self.dt  # vf = vi + at
        else:
            self.speedY = -self.speedY
        self.y += self.speedY  # Update coordinates
        #print("y: %f,  SpeedY: %f,  dt: %f" % (self.y, self.speedY, self.dt))

        # x-axis movement
        if self.lwall + self.r < self.x < self.rwall - self.r:
            pass
        else:
            self.speedX = -self.speedX
        self.x += self.speedX
        self.canvas.move(self.ballDrawing, self.speedX, self.speedY)
        self.canvas.after(int(self.dt*self.updateTime), self.animation, self.dt)

    def toggleGravity(self, gravValue):
        self.g = gravValue

    def deleteBall(self):
        self.canvas.delete(self.ballDrawing)
        print("Deleted ball", self.ballDrawing)

root = Tk()
root.title("Ball Simulator")
gui = GUI(master=root)
gui.mainloop()

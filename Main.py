import os
import tkinter as tk
from tkinter.constants import END
import pygubu
import matplotlib
import random
import math

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from math import acos, acosh, asin, degrees, sin, cos, radians, sqrt, log, pi

from pygubu import builder
from typing_extensions import IntVar


class Cannon:
    def __init__(self, x0, y0, v, angle):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.x = x0
        self.y = y0

        self.alpha = angle

        self.vx = v * cos(radians(angle))
        X = builder.get_object('ux0')
        X.delete(0, END)
        X.insert(0, round(self.vx, 1))

        self.vy = v * sin(radians(angle))
        Y = builder.get_object('uy0')
        Y.delete(0, END)
        Y.insert(0, round(self.vy, 1))

        self.vm = 0
        self.a = self.alpha

        self.ax = 0
        self.ay = -9.8

        self.time = 0

        self.v0 = sqrt(pow(self.vx, 2) + pow(self.vy, 2))
        self.b = float(self.v0 * sin(radians(self.alpha)) * 2)
        self.t = float((self.b + sqrt(pow(self.b, 2) + 4 * 9.8 * y0 * 2))/(2 * 9.8))
        self.S = float(self.v0 * round(self.t, 2) * cos(radians(self.alpha)))

        self.xarr = [self.x]
        self.yarr = [self.y]

    def updateVx(self, dt):
        self.vx = self.vx + self.ax * dt

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        X = builder.get_object('uxm')
        X.delete(0, END)
        X.insert(0, round(self.vx, 1))

        return self.vx

    def updateVy(self, dt):

        if self.y <= 0.0 or self.vy > (self.v0 * sin(radians(self.alpha))) - (9.8 * self.time):
            self.vy = self.v0 * sin(radians(self.alpha)) - 9.8 * self.time

        else:
            self.vy = self.vy + self.ay * dt


        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        X = builder.get_object('uym')
        X.delete(0, END)
        X.insert(0, round(self.vy, 1))

        return self.vy

    def updateVm(self, dt):
        self.vm = sqrt(pow(self.vx, 2) + pow(self.vy, 2))

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        V = builder.get_object('u_m')
        V.delete(0, END)
        V.insert(0, round(self.vm, 1))

        return self.vm

    def updateAngle(self, dt):
        self.a = int(round(degrees(asin(self.vy / self.vm))))

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        V = builder.get_object('alpha')
        V.delete(0, END)
        V.insert(0, self.a)

        return self.a 

    def updateX(self, dt):
        self.x = (self.x + 0.5 * (self.vx + self.updateVx(dt)) * dt)
        xm = self.S 
        
        if self.x > xm:
            self.x = xm 

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        X = builder.get_object('x_m')
        X.delete(0, END)
        X.insert(0, round(self.x, 1))

        return self.x

    def updateY(self, dt):
        self.y = self.y + 0.5 * (self.vy + self.updateVy(dt)) * dt
        
        if self.y <= 0:
            self.y = 0.0

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        Y = builder.get_object('y_m')
        Y.delete(0, END)
        Y.insert(0, round(self.y))

        return self.y

    def step(self, dt):
        self.xarr.append(self.updateX(dt))
        self.yarr.append(self.updateY(dt))
        self.time = self.time + dt

        self.vm = self.updateVm(self)
        self.a = self.updateAngle(self)

        if self.time > self.t:
            self.time = self.t

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        text = builder.get_object('tm')
        text.delete(0, END)
        text.insert(0, round(self.time, 1))


def makeShoot(x0, y0, velocity, angle):

    cannon = Cannon(x0, y0, velocity, angle)
    dt = 0.05 
    t = 0
    cannon.step(dt)

    while cannon.y >= 0:
        cannon.step(dt)
        t = t + dt
    return (cannon.xarr, cannon.yarr)


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "interface.ui")


class Issue220App:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')


        fcontainer = builder.get_object('frame_3')

        self.figure = fig = Figure(figsize = (5, 4), dpi = 100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master = fcontainer)
        canvas.draw()
        canvas.get_tk_widget().pack(side = 'top', fill = 'both')
        #canvas.get_tk_widget().place(anchor='nw', height=400, relwidth=.70, width=150, y=-30)
        
        self.toolbar = NavigationToolbar2Tk(canvas, fcontainer, pack_toolbar=True)
        self.toolbar.update()
        

        builder.connect_callbacks(self)
        guivars = ('spinvar1','spinvar2', 'spinvar3')
        builder.import_variables(self, guivars)

        self.y = builder.get_object('y0m')
        ay = random.randint(0, 0)
        self.spinvar1.set(ay)

        self.a = builder.get_object('alpha0')
        aa = random.randint(0, 0)
        self.spinvar2.set(aa)

        self.v = builder.get_object('u0')
        av = random.randint(0, 0)
        self.spinvar3.set(av)
        
        self.on_animate_click()

    def on_animate_click(self):
        self.anim_step = 5
        self.dt = 0.1
        self.time = 0

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        
        #Input
        y0 = float(self.y.get())
        alpha = float(self.a.get())
        velocity = float(self.v.get())
        

        self.cannons = [Cannon(0, y0, velocity, alpha)]
        
        self.mainwindow.after(self.anim_step, self.anim)
        
    def anim(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid()

        continue_anim = False

        #Print
        for c in self.cannons:
            if c.y > 0:
                c.step(self.dt)
                print(c.x, c.y)
                continue_anim = True
            elif c.y == 0:
                continue_anim = False

            ax.plot(c.xarr, c.yarr)
        
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        self.canvas.draw()
        
        if continue_anim:
            self.mainwindow.after(self.anim_step, self.anim)


    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = Issue220App()
    app.run()
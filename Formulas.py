import math
from math import cos, sin, radians, sqrt

h = int(input())
v = int(input())
alpha = int(input())

g = float(9.8)

vx = v * cos(radians(alpha))
vy = v * sin(radians(alpha)) 
b = float(v*sin(radians(alpha))*2)
t = float((b + sqrt(pow(b,2)+4*g*h*2))/(2*g))
S = float(v*round(t,2)*cos(radians(alpha)))
H = (pow(v,2)*(sin(radians(alpha)))**2)/(2*g) + h

print("\nvx =", round(vx,1), "\nvy =", round(vy,1), "\nt =", round(t,1), "\nS =", round(S,2), "\nH =", round(H,1))

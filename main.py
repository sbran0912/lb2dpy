import lib2d as l2d
from random import randint
import pyray as pr
import math

b1 = l2d.Box(100, 200, 200, 300)
b2 = l2d.Box(100, 200, 200, 300)
     
pr.init_window(1200, 800, "Hello Raylib")
pr.set_target_fps(60)
while not pr.window_should_close():
   pr.begin_drawing()
   pr.clear_background(pr.WHITE)
   l2d.draw_box(b1, pr.BLACK)
   l2d.draw_box(b2, pr.BLUE)
   b2.rotate(0.02)
   pr.end_drawing()
   pass
pr.close_window()

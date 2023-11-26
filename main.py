import lb2d
from random import randint
from pyray import *

b = lb2d.Box(100, 200, 200, 300)
     
init_window(1200, 800, "Hello Raylib")
set_target_fps(60)
while not window_should_close():
   begin_drawing()
   clear_background(WHITE)
   lb2d.draw_box(b)
   end_drawing()
   pass
close_window()

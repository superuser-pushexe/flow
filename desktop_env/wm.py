from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

def get_window_under_cursor(d):
    pointer = d.screen().root.query_pointer()
    win = pointer.child
    return win

def start_window_manager():
    d = display.Display()
    root = d.screen().root
    root.change_attributes(event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask | X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask)

    drag_window = None
    drag_start = (0, 0)

    while True:
        event = d.next_event()

        if event.type == X.MapRequest:
            win = event.window
            win.map()

        elif event.type == X.ButtonPress and event.detail == 1:
            pointer = root.query_pointer()
            drag_window = get_window_under_cursor(d)
            if drag_window:
                geom = drag_window.get_geometry()
                drag_start = (pointer.root_x - geom.x, pointer.root_y - geom.y)

        elif event.type == X.MotionNotify and drag_window:
            pointer = root.query_pointer()
            new_x = pointer.root_x - drag_start[0]
            new_y = pointer.root_y - drag_start[1]
            drag_window.configure(x=new_x, y=new_y)
            d.sync()

        elif event.type == X.ButtonRelease:
            drag_window = None

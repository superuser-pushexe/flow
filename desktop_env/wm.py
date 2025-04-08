from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

# Global list to track open windows
open_windows = []

def get_window_under_cursor(d):
    pointer = d.screen().root.query_pointer()
    win = pointer.child
    return win

def start_window_manager():
    global open_windows
    d = display.Display()
    root = d.screen().root
    root.change_attributes(event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask | X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask | X.KeyPressMask)

    drag_window = None
    drag_start = (0, 0)
    focused_window = None

    while True:
        event = d.next_event()

        if event.type == X.MapRequest:
            win = event.window
            win.map()
            win.change_attributes(event_mask=X.EnterWindowMask)
            # Get window name (simplified)
            try:
                name = win.get_wm_name() or "Untitled"
            except:
                name = "Untitled"
            open_windows.append({"id": win.id, "name": name})

        elif event.type == X.EnterNotify:
            win = event.window
            if focused_window != win:
                if focused_window:
                    focused_window.configure(border_width=1)
                win.configure(border_width=2)
                focused_window = win
                d.set_input_focus(win, X.RevertToParent, X.CurrentTime)

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
            screen_width = root.get_geometry().width
            if new_x < 50:
                drag_window.configure(x=0, y=0, width=screen_width//2, height=root.get_geometry().height)
                drag_window = None
            elif new_x + drag_window.get_geometry().width > screen_width - 50:
                drag_window.configure(x=screen_width//2, y=0, width=screen_width//2, height=root.get_geometry().height)
                drag_window = None
            else:
                drag_window.configure(x=new_x, y=new_y)
            d.sync()

        elif event.type == X.ButtonRelease:
            drag_window = None

        elif event.type == X.KeyPress:
            keycode = event.detail
            state = event.state
            if keycode == 58 and state & X.Mod1Mask:  # Alt + M
                win = get_window_under_cursor(d)
                if win:
                    win.unmap()
                    open_windows = [w for w in open_windows if w["id"] != win.id]
            elif keycode == 41 and state & X.Mod1Mask:  # Alt + F
                win = get_window_under_cursor(d)
                if win:
                    geom = win.get_geometry()
                    if geom.width == root.get_geometry().width:
                        win.configure(width=800, height=600)
                    else:
                        win.configure(x=0, y=0, width=root.get_geometry().width, height=root.get_geometry().height)

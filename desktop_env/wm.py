from Xlib import X, display

def start_window_manager():
    d = display.Display()
    root = d.screen().root
    root.change_attributes(event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask)
    while True:
        event = d.next_event()
        if event.type == X.MapRequest:
            win = event.window
            win.map()

Title: urwid

最近要写一个mongo current op的管理工具，

http://www.nicosphere.net/urwid-for-python-a-ncurses-library-2541/

https://github.com/intnull/videotop/blob/master/videotop.py




Why can't I select text in an Urwid program?

By default Urwid's MainLoop tells the terminal that it will handle mouse input so it can react to things like selecting widgets with the mouse or activating check boxes.

If you wrote this program and you want to disable Urwid's mouse handling you can set handle_mouse=False when creating your MainLoop or screen object.

Or you can just hold the SHIFT key while clicking and dragging in to get the normal select text/copy behavior.

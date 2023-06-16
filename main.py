from tkinter import Tk, Canvas, Listbox, Frame, Scrollbar

from graph import Graph

from config import *

root = Tk()

root.config(bg=BG_COLOR)
root.option_add('*background', BG_COLOR)

main = Frame(root)
main.pack(expand=1)

canvas = Canvas(
    main,
    width=CANVAS_SIZE,
    height=CANVAS_SIZE,
    highlightthickness=0,
)
canvas.grid(
    column=0, 
    row=0, 
    rowspan=2, 
    padx=PADDING, 
    pady=PADDING,
)

edge_frame = Frame(main)
edge_frame.grid(
    column=1, 
    row=0, 
    padx=PADDING, 
    pady=PADDING
)

edge_scroll_bar = Scrollbar(
    edge_frame,
    bg=BLACK_COLOR,
    activebackground=BLACK_COLOR,
    troughcolor=WHITE_COLOR,
    width=SCROLL_WIDTH,
    bd=0,
)
edge_scroll_bar.pack(
    side='right', 
    fill='both'
)

edge_list = Listbox(
    edge_frame,
    border=0,
    highlightthickness=0,
    selectmode='extended',
    activestyle='none',
    font=FONT,
    width=LIST_WIDTH,
    height=LIST_HEIGHT,
    fg=BLACK_COLOR,
    selectbackground=WHITE_COLOR,
    selectforeground=BLACK_COLOR,
    yscrollcommand=edge_scroll_bar.set,
)
edge_list.pack()
edge_scroll_bar.config(command=edge_list.yview)

d_f_frame = Frame(main)
d_f_frame.grid(
    column=1, 
    row=1, 
    padx=PADDING, 
    pady=PADDING
)

d_f_scroll_bar = Scrollbar(
    d_f_frame,
    bg=BLACK_COLOR,
    activebackground=BLACK_COLOR,
    troughcolor=WHITE_COLOR,
    width=SCROLL_WIDTH,
    orient='horizontal',
    bd=0,
)
d_f_scroll_bar.pack(
    side='bottom', 
    fill='both'
)

d_f_list = Listbox(
    d_f_frame,
    border=0,
    highlightthickness=0,
    selectmode='extended',
    activestyle='none',
    font=FONT,
    width=LIST_WIDTH,
    height=2,
    fg=BLACK_COLOR,
    selectbackground=WHITE_COLOR,
    selectforeground=BLACK_COLOR,
    xscrollcommand=d_f_scroll_bar.set,
)
d_f_list.pack()
d_f_scroll_bar.config(command=d_f_list.xview)

graph = Graph(*Graph.load('graph.txt'), canvas, edge_list, d_f_list)

graph.DFS()

graph.draw()
graph.animate()

root.mainloop()

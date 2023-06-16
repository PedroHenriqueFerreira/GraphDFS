from typing import Any

from tkinter import Canvas, Listbox
from math import radians, sin, cos, hypot

from config import *

class Graph:
    def __init__(
        self,
        V: list[int],
        adj_list: dict[int, list[int]],
        canvas: Canvas,
        edge_list: Listbox,
        d_f_list: Listbox
    ):
        self.V = V
        self.adj_list = adj_list

        self.canvas = canvas
        self.edge_list = edge_list
        self.d_f_list = d_f_list

        self.color = {v: 'white' for v in self.V}

        self.d: dict[int, int] = {}
        self.f: dict[int, int] = {}

        self.edges: list[dict[str, Any]] = []

        self.mark = 0

        self.text_elements: dict[int, int] = {}
        self.circle_elements: dict[int, int] = {}

    def on_d_f_list_select(self, e):
        selection = self.d_f_list.curselection()
        
        for v in self.V:
            self.canvas.itemconfig(self.text_elements[v], text=v)

        if len(selection) == 0:
            return
        
        if len(selection) == 1:
            vector = self.d if selection[0] == 0 else self.f
            
            for v in self.V:
                self.canvas.itemconfig(self.text_elements[v], text=vector[v])
        else:
            for v in self.V:
                self.canvas.itemconfig(self.text_elements[v], text=f'{self.d[v]}/{self.f[v]}')      

    def on_edge_list_select(self, e):
        selection = self.edge_list.curselection()

        self.canvas.lift('circle')
        self.canvas.lift('text')

        self.canvas.itemconfig('text', fill=BG_COLOR)
        self.canvas.itemconfig('circle', fill=BLACK_COLOR)
        self.canvas.itemconfig('line', fill=BLACK_COLOR)

        if len(selection) == 0:
            return

        self.canvas.itemconfig('text', fill=BG_COLOR)
        self.canvas.itemconfig('circle', fill=BG_COLOR)
        self.canvas.itemconfig('line', fill=BG_COLOR)

        for selected in selection:
            edge_info = self.edge_list.get(selected)
            edge: list[int] = [int(i) for i in edge_info.split(':')[0][1:-1].split(', ')]

            line_element = self.edges[selected]['element']

            self.canvas.itemconfig(line_element, fill=BLACK_COLOR)

            for v in edge:
                self.canvas.itemconfig(self.circle_elements[v], fill=BLACK_COLOR)
                self.canvas.itemconfig(self.text_elements[v], fill=BG_COLOR)
                
                self.canvas.lift(self.circle_elements[v])
                self.canvas.lift(self.text_elements[v])

            self.canvas.lift(line_element, 'circle')

    def DFS_visit(self, v: int) -> None:
        self.color[v] = 'gray'

        self.mark += 1
        self.d[v] = self.mark

        if v in self.adj_list:
            for v2 in self.adj_list[v]:
                edge: dict[str, str | int | tuple[int, int]] = { 'value': (v, v2), 'mark': self.mark }
                
                if self.color[v2] == 'white':
                    edge['type'] = 'Árvore'
                    
                elif self.color[v2] == 'gray':
                    edge['type'] = 'Retorno'
                elif self.d[v] < self.f[v2]:
                    edge['type'] = 'Avanço'
                else:
                    edge['type'] = 'Cruzamento'
                
                self.edges.append(edge)
                
                if self.color[v2] == 'white':    
                    self.DFS_visit(v2)

        self.color[v] = 'black'

        self.mark += 1
        self.f[v] = self.mark

    def DFS(self):
        sorted_V = sorted(self.V, key=lambda i: len(self.adj_list.get(i) or []), reverse=True)

        for v in sorted_V:
            if self.color[v] == 'white':
                self.DFS_visit(v)

    @staticmethod
    def load(url: str) -> tuple[list[int], dict[int, list[int]]]:
        V: list[int] = []
        adj_list: dict[int, list[int]] = {}

        with open(url, 'r') as file:
            lines = file.readlines()
            
            n_V = int(lines[0].strip().split()[0])
            
            V = [i for i in range(1, n_V + 1)]
            
            for line in lines[1:]:
                origin, destiny = [int(i) for i in line.strip().split()]

                if origin not in adj_list:
                    adj_list[origin] = []

                adj_list[origin].append(destiny)

        for v in adj_list:
            adj_list[v].sort()

        V.sort()

        return V, adj_list

    def draw(self) -> None:        
        degree_per_item = 360 / len(self.V)

        center_pos = (CANVAS_SIZE - CIRCLE_SIZE) / 2

        for i, v in enumerate(self.V):
            degree = i * degree_per_item

            distance = (CANVAS_SIZE / 2) - CIRCLE_SIZE

            pos_x = center_pos + distance * cos(radians(degree))
            pos_y = center_pos + distance * sin(radians(degree))

            circle_element = self.canvas.create_oval(
                pos_x,
                pos_y,
                pos_x + CIRCLE_SIZE,
                pos_y + CIRCLE_SIZE,
                fill=WHITE_COLOR,
                width=0,
                tags='circle'
            )

            text_element = self.canvas.create_text(
                pos_x + CIRCLE_SIZE / 2,
                pos_y + CIRCLE_SIZE / 2,
                text=v,
                fill=BLACK_COLOR,
                font=FONT,
                tags='text'
            )

            self.circle_elements[v] = circle_element
            self.text_elements[v] = text_element

        for edge in self.edges:
            origin_coords = self.canvas.coords(self.circle_elements[edge['value'][0]])
            destiny_coords = self.canvas.coords(self.circle_elements[edge['value'][1]])

            origin_pos = [(origin_coords[i] + origin_coords[i + 2]) / 2 for i in range(2)]
            destiny_pos = [(destiny_coords[i] + destiny_coords[i + 2]) / 2 for i in range(2)]

            x = (origin_pos[0] + destiny_pos[0]) / 2
            y = (origin_pos[1] + destiny_pos[1]) / 2
            
            x_signal = 1 if x < center_pos else -1
            y_signal = 1 if y > center_pos else -1
            
            distance = hypot(origin_pos[0] - destiny_pos[0], origin_pos[1] - destiny_pos[1])

            # Se a distância é 0, então cria um laço do vértice até ele mesmo
            if distance == 0:
                origin_pos[1] += (CIRCLE_SIZE / 2) * y_signal
                
                destiny_pos = [
                    origin_pos[0],
                    origin_pos[1] + (CIRCLE_SIZE / 2) * y_signal,
                    
                    origin_pos[0] - CIRCLE_SIZE * x_signal,
                    origin_pos[1] + (CIRCLE_SIZE / 2) * y_signal,
                    
                    origin_pos[0] - CIRCLE_SIZE * x_signal,
                    origin_pos[1] - (CIRCLE_SIZE / 2) * y_signal,
                    
                    origin_pos[0] - (CIRCLE_SIZE / 2) * x_signal,
                    origin_pos[1] - (CIRCLE_SIZE / 2) * y_signal
                ]
                
            else:
                # Recuando para a reta ficar apenas tocando as bordas do vértice
                distance_x = ((CIRCLE_SIZE / 2) * (destiny_pos[0] - origin_pos[0])) / distance
                distance_y = ((CIRCLE_SIZE / 2) * (destiny_pos[1] - origin_pos[1])) / distance

                destiny_pos[0] -= distance_x
                destiny_pos[1] -= distance_y

                origin_pos[0] += distance_x
                origin_pos[1] += distance_y

                # Cria uma curva na linha atual e na linha reversa se existir uma linha reversa
                
                reversed_edge_value = tuple(reversed(edge['value']))
                
                if reversed_edge_value in [e['value'] for e in self.edges]:
                    reversed_edge = [
                        edge_value 
                        for edge_value in self.edges 
                        if edge_value['value'] == reversed_edge_value
                    ][0]
                    
                    if 'element' in reversed_edge:
                        curve_pos = [
                            x - (CIRCLE_SIZE / 2) * x_signal, 
                            y + (CIRCLE_SIZE / 2) * y_signal
                        ]

                        self.canvas.coords(
                            reversed_edge['element'],
                            *destiny_pos,
                            *curve_pos,
                            *origin_pos
                        )

                        curve_pos = [
                            x + (CIRCLE_SIZE / 2) * x_signal, 
                            y - (CIRCLE_SIZE / 2) * y_signal
                        ]
                        
                        destiny_pos = [*curve_pos, *destiny_pos]

            line_element = self.canvas.create_line(
                *origin_pos,
                *destiny_pos,
                arrow='last',
                smooth=True,
                width=LINE_WIDTH,
                fill=WHITE_COLOR,
                arrowshape=ARROW_SHAPE,
                tags='line'
            )

            edge['element'] = line_element
            self.canvas.lower(line_element)

    def animate(self, mark: int = 0) -> None:
        if mark > self.mark:
            self.edge_list.bind('<<ListboxSelect>>', self.on_edge_list_select)
            self.d_f_list.bind('<<ListboxSelect>>', self.on_d_f_list_select)
            return

        if mark in self.d.values():
            for v in self.d:
                if self.d[v] == mark:
                    self.canvas.itemconfig(self.circle_elements[v], fill=GRAY_COLOR)
                    self.canvas.itemconfig(self.text_elements[v], fill=BLACK_COLOR)

                    break
        elif mark in self.f.values():
            for v in self.f:
                if self.f[v] == mark:
                    self.canvas.itemconfig(self.circle_elements[v], fill=BLACK_COLOR)
                    self.canvas.itemconfig(self.text_elements[v], fill=BG_COLOR)

                    break

        if mark in [edge['mark'] for edge in self.edges]:
            for edge in self.edges:
                if edge['mark'] == mark:
                    dash: tuple[int, ...] | None = None

                    match edge['type']:
                        case 'Retorno':
                            dash = DOT_CONFIG
                        case 'Avanço':
                            dash = DASH_CONFIG
                        case 'Cruzamento':
                            dash = DOTTED_DASH_CONFIG

                    self.canvas.itemconfig(edge['element'], fill=BLACK_COLOR, dash=dash)
                    self.canvas.lift(edge['element'], 'line')

                    self.edge_list.insert('end', f'{edge["value"]}: {edge["type"]}')                

        d = [self.d[v] if self.d[v] <= mark else 0 for v in self.V]
        f = [self.f[v] if self.f[v] <= mark else 0 for v in self.V]

        self.d_f_list.insert(0, f'Vetor D: {d}')
        self.d_f_list.insert(1, f'Vetor F: {f}')

        self.canvas.after(SPEED, lambda: self.animate(mark + 1))
        
        
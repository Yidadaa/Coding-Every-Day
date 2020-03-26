from tkinter import Frame, Button, Menu, Canvas, Scale, LabelFrame, Label, Listbox
import tkinter as tk
from itertools import product
from time import time
import os
import json

import numpy as np

from .core import GameRunner

class Application(Frame):
  def __init__(self, runner: GameRunner):
    Frame.__init__(self)
    self.runner = runner

    # private state
    self.event_loop_count_ms = 1
    self.t = self.get_timestamp_ms()
    self.is_running = False
    self.max_speed = 20
    self.speed = 1
    self.canvas_width = 640
    self.canvas_height = 400
    self.block_width = 10 # pixels
    self.template_list = []

    # lifecyle functions
    self.load_config()
    self.create_layout()
    self.loop_callback()
    self.update_status_text()

  def run(self):
    self.mainloop()

  def load_config(self):
    '''Load config from ./config
    '''
    root_path = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
    config_path = os.path.join(root_path, 'configs')
    self.template_list = []
    for config_file in os.listdir(config_path):
      file_path = os.path.join(config_path, config_file)
      try:
        content = json.load(open(file_path))
        # check file content
        if 'name' not in content or 'template' not in content\
          or len(content['template']) < 1\
          or len(content['template'][0]) < 1:
          continue
        self.template_list.append(content)
      except:
        print('Failed to load {}.'.format(file_path))

  def create_layout(self):
    '''Makes layout of the application.
    '''
    self.master.geometry('{}x{}'.format(self.canvas_width + 200, self.canvas_height + 120))
    # self.master.resizable(False, False)
    self.master.title('Conway\'s Game of Life')
    self.pack()

    # template list
    self.list_frame = Frame(self)
    self.list_frame.pack(side=tk.LEFT)
    self.frame_title = Canvas(self.list_frame, width=180, height=20)
    self.frame_title.create_text(90, 10, fill='black', text='Template List')
    self.frame_title.pack()
    self.list_box = Listbox(self.list_frame, height=100)
    for item in self.template_list:
      self.list_box.insert(tk.END, item['name'])
    self.list_box.pack(fill=tk.X, expand=tk.YES)
    self.list_box.bind('<<ListboxSelect>>', self.on_template_selected)
    # select the first value as default
    self.list_box.select_set(0)

    # canvas displayer
    self.display_frame = Frame(self)
    self.display_frame.pack(side=tk.RIGHT)
    self.canvas = Canvas(self.display_frame, width=self.canvas_width, height=self.canvas_height, bg='black')
    self.canvas.pack()

    # button group
    self.control_frame = Frame(self.display_frame)
    self.control_frame.pack()
    self.button_group = LabelFrame(self.control_frame, text='Control Buttons')
    self.start_button = Button(self.button_group, text='Start', width=10,
      command=self.on_start_button, state=tk.NORMAL)
    self.pause_button = Button(self.button_group, text='Pause', width=10,
      command=self.on_pause_button, state=tk.DISABLED)
    self.random_button = Button(self.button_group, text='Random', width=10,
      command=self.on_random_button, state=tk.NORMAL)
    for button in [self.start_button, self.pause_button, self.random_button]:
      button.pack(side=tk.LEFT, padx=5, pady=5)
    self.button_group.pack(side=tk.LEFT, padx=2)

    # speed controller
    self.speed_frame = LabelFrame(self.control_frame)
    self.speed_scale = Scale(self.speed_frame, from_=1, to=20, resolution=1, orient=tk.HORIZONTAL, show=0, length=430,
      command=self.on_speed_changed)
    self.speed_scale.set(self.max_speed // 2)
    self.speed_scale.pack(padx=5, pady=(9, 8))
    self.speed_frame.pack(side=tk.LEFT, padx=2)

    # status content
    self.status_frame = LabelFrame(self.display_frame, text='Status')
    self.status_text = Label(self.status_frame, text='', width=self.canvas_width)
    self.status_text.pack(side=tk.LEFT, padx=5)
    self.status_frame.pack(side=tk.LEFT, padx=2)

    # dispatch default template
    self.list_box.event_generate("<<ListboxSelect>>")


  def on_template_selected(self, event):
    '''Renders template to screen.
    '''
    if self.is_running:
      self.on_pause_button() # pause game
    widget = event.widget # type: ListBox
    selected_index = widget.curselection()[0]
    if selected_index >= len(self.template_list): return
    template = np.array(self.template_list[selected_index]['template'], dtype=np.uint8)
    rows, cols = template.shape
    # determine block width
    block_width = self.block_width
    if max(rows, cols) > self.canvas_height: block_width //= 2
    # determine world size
    world_h, world_w = self.canvas_height // block_width, self.canvas_width // block_width
    world_mat = np.zeros((world_h, world_w), dtype=np.uint8)
    # copy template to world
    st_row, st_col = (world_h - rows) // 2, (world_w - cols) // 2
    world_mat[st_row:st_row + rows, st_col:st_col + cols] = template
    self.runner.set_world(world_mat)
    self.render()

  def on_speed_changed(self, speed):
    '''Speed changed callback
    '''
    self.speed = int(speed)
    self.speed_frame.config(text='Speed (1 - {}), Current: {}'.format(self.max_speed, speed))

  def on_start_button(self):
    '''Will be called when start button is clicked.
    '''
    if self.runner.world is None: return
    self.is_running = True
    self.start_button.config(state=tk.DISABLED)
    self.pause_button.config(state=tk.NORMAL)
    self.random_button.config(state=tk.DISABLED)

  def on_random_button(self):
    '''Will be called when random button is clicked.
    '''
    self.start_button.config(state=tk.DISABLED)
    self.pause_button.config(state=tk.DISABLED)
    self.runner.random_init(self.canvas_height // self.block_width,
      self.canvas_width // self.block_width, 0.1)
    self.render()
    self.start_button.config(state=tk.NORMAL)
    self.pause_button.config(state=tk.DISABLED)

  def on_pause_button(self):
    '''Will be called when pause button is clicked.
    '''
    self.is_running = False
    self.start_button.config(state=tk.NORMAL)
    self.pause_button.config(state=tk.DISABLED)
    self.random_button.config(state=tk.NORMAL)

  def get_timestamp_ms(self):
    '''Returns milliseconds from 1970.
    '''
    return time() * 1000

  def loop_callback(self):
    '''This function will be called every ${self.loop_callback} ms.
    '''
    if self.is_running:
      if self.get_timestamp_ms() - self.t >= (self.max_speed - self.speed + 1) * 20:
        self.runner.step()
        self.render()
        self.t = self.get_timestamp_ms()
    self.after(self.event_loop_count_ms, self.loop_callback)

  def update_status_text(self):
    '''Updates status text.
    '''
    self.status_text.config(
      text='Iteration: {:5}\t Live: {:10}\t Dead: {:10}'.format(
        self.runner.t, self.runner.live_count, self.runner.dead_count))

  def render(self):
    '''Renders world to canvas.
    '''
    self.update_status_text()
    rows, cols = self.runner.world.shape
    w, h = self.canvas_width, self.canvas_height
    bh, bw = h // rows, w // cols
    self.canvas.delete(tk.ALL)
    for r, c in product(range(rows), range(cols)):
      if self.runner.world[r, c] < 1: continue
      self.canvas.create_rectangle(c * bw, r * bh, c * bw + bw, r * bh + bh, fill='white')

  def fast_render(self):
    '''Faster version of render function.
    '''
    self.update_status_text()
    rows, cols = self.runner.world.shape
    w, h = self.canvas_width, self.canvas_height
    bh, bw = h // rows, w // cols
    ppm_data = bytes('P5 {} {} 255 '.format(cols, rows), 'utf-8')
    ppm_data += (self.runner.world * 255).astype(np.uint16).tobytes()
    self.image = tk.PhotoImage(width=cols, height=rows, data=ppm_data, format='PPM').zoom(bw, bh)
    self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
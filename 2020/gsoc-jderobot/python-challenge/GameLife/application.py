from tkinter import Frame, Button, Menu, Canvas, Scale, LabelFrame, Label
import tkinter as tk

from .core import GameRunner

class Application(Frame):
  def __init__(self, runner: GameRunner):
    Frame.__init__(self)
    self.runner = runner

    # private state
    self.event_loop_count_ms = 10
    self.t = 0
    self.is_running = False

    # lifecyle functions
    self.create_menu()
    self.create_layout()
    self.loop_callback()

  def run(self):
    self.mainloop()

  def create_menu(self):
    ''' Creates menu bar.
    '''
    self.menu = Menu(self)
    self.menu.add_command(label='Open')
    self.menu.add_command(label='Save')
    self.master.config(menu=self.menu)

  def create_layout(self):
    '''Makes layout of the application.
    '''
    self.master.geometry('640x520')
    self.master.title('Conway\'s Game of Life')
    self.pack()
    Canvas(self, width=640, height=400, bg='black').pack()

    self.control_frame = Frame(self)
    self.control_frame.pack()
    self.button_group = LabelFrame(self.control_frame, text='Control Buttons')
    self.start_button = Button(self.button_group, text='Start', width=10,
      command=self.on_start_button, state=tk.NORMAL)
    self.pause_button = Button(self.button_group, text='Pause', width=10,
      command=self.on_pause_button, state=tk.DISABLED)
    for button in [self.start_button, self.pause_button]: button.pack(side=tk.LEFT, padx=5, pady=5)
    self.button_group.pack(side=tk.LEFT, padx=2)

    self.speed_frame = LabelFrame(self.control_frame, text='Speed (1 - 20), Current: 1')
    Scale(self.speed_frame, from_=1, to=20, resolution=1, orient=tk.HORIZONTAL, show=0, length=430,
      command=self.on_speed_changed).pack(padx=5, pady=(9, 8))
    self.speed_frame.pack(side=tk.LEFT, padx=2)

    self.status_frame = LabelFrame(self, text='Status')
    Label(self.status_frame, text='fsfsdfdd').pack()
    self.status_frame.pack(sid=tk.LEFT, padx=2)

  def on_speed_changed(self, speed):
    '''Speed changed callback
    '''
    self.speed_frame.config(text='Speed (1 - 10), Current: {}'.format(speed))

  def on_start_button(self):
    self.is_running = True
    self.start_button.config(state=tk.DISABLED)
    self.pause_button.config(state=tk.NORMAL)

  def on_pause_button(self):
    self.is_running = False
    self.start_button.config(state=tk.NORMAL)
    self.pause_button.config(state=tk.DISABLED)

  def loop_callback(self):
    if not self.is_running: return
    self.t += 1
    self.after(self.event_loop_count_ms, self.loop_callback)
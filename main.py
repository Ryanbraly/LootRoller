import customtkinter as ctk

from graphics import Window, Lobby
from player import Player

#ctk.deactivate_automatic_dpi_awareness()
ctk.set_appearance_mode("dark")


window = Window()
lobby = Lobby(master=window)


window.mainloop()





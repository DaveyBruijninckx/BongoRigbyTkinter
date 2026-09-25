import tkinter as tk
from pynput import keyboard, mouse
import queue
from PIL import Image, ImageTk  # Voor het laden van afbeeldingen
from time import strftime
import sys
import os

# deze functie zorgt ervoor dat ik de foto's kan vinden :)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller tijdelijke map
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Queue voor thread-safe communicatie
event_queue = queue.Queue()

#checked de value van value
def ProcessEvents():
    while not event_queue.empty():
        value = int(lblValue["text"])
        lblValue["text"] = str(value + 1)

    window.after(10, ProcessEvents)  # blijft checken

window = tk.Tk()

window.attributes("-topmost", True) #zorgt ervoor dat de window altijd boven alles blijft
window.overrideredirect(True) #zorgt ervoor dat de rand weg gaat

BG = "#1e1e2e"
ACCENT = "#ff79c6"
TEXT = "#f8f8f2"

#deze fuctie saved de score
def SaveScore():
    with open("score.txt", "w") as save:
        save.write(lblValue["text"])

#deze functie laad de score
def LoadScore():
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as save:
            data = save.read().strip()
            if data.isdigit():
                return data
    return "0"

#deze functie roept de functies aan waneer het programma gesloten word
def onClose():
    SaveScore()
    window.destroy()

customBar = tk.Frame(window, bg="#2a2a3c", height=30)# maakt de mooie roze bar boven rigby
customBar.grid(row=0, column=0, columnspan=3, sticky="ew")# dit zorgt ervoor dat hij boven de rigby en niet verder dan rigby gaat

closeButton = tk.Button(customBar, text="✕", command=onClose, bg="#2a2a3c", fg=ACCENT, bd=0, font=("Segoe UI", 10))
closeButton.pack(side="right", padx=5, pady=2)

#alles wat te maken heeft met het mooi maken van de app
window.attributes("-transparentcolor", "white")
window.configure(bg=BG)

#laad de jpg van rigby in
idleImg = Image.open(resource_path("rigbyIdle.jpg")).resize((180,180))
hitImg = Image.open(resource_path("rigbyHit.jpg")).resize((180,180))

#verandert jpg naar een tkinter foto
idlePhoto = ImageTk.PhotoImage(idleImg)
hitPhoto = ImageTk.PhotoImage(hitImg)

#maakt een label voor rigby zodat je hem kan zien
rigbyLabel = tk.Label(window, image=idlePhoto, bg=BG)
rigbyLabel.grid(row=1, columnspan=3)

#zet een idle en hit foto
rigbyLabel.idle = idlePhoto
rigbyLabel.hit = hitPhoto

#de functie om te wisselen van plaatje
def PlayAnimation():
    rigbyLabel.config(image=hitPhoto)
    window.after(200, lambda: rigbyLabel.config(image=idlePhoto))

#groote van de window
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure([0, 1, 2], minsize=0, weight=1)

#Dit is de label/counter :)
lblValue = tk.Label(master=window, text=LoadScore(), bg='#2a2a3c', fg=ACCENT, font=("Segoe UI", 10))
lblValue.grid(row=2, column=0)

#de functie om tijd op te nemen
def time():
    klok = strftime('%H:%M:%S')
    labelKlok.config(text=klok)
    labelKlok.after(800, time)

labelKlok = tk.Label(window, bg=BG, fg=ACCENT, font=("Segoe UI", 12))
labelKlok.grid(row=2, column=2)

time()

#de functie om bij de 1 bij de counter op te tellen
def Increase(event=None):
    value = int(lblValue["text"])
    lblValue["text"] = f"{value + 1}"

# set om bij te houden welke toetsen ingedrukt zijn
keysPressed = set()

# Globale keyboard listener
def OnKeyPress(key):
    if key not in keysPressed:
        keysPressed.add(key)
        Increase()
        PlayAnimation()

def OnKeyRelease(key):
    # verwijder key uit set als hij losgelaten wordt
    if key in keysPressed:
        keysPressed.remove(key)

# Globale muis knop listener
def OnClick(x,y, button, pressed):
    if pressed:
        Increase()
        PlayAnimation()

#de keyboard listener zorgt ervoor dat je weet waneer er een keer geklikt word en kan meerdere keren de zelfde toets lezen
keyBoardListener = keyboard.Listener(
    on_press=OnKeyPress,
    on_release=OnKeyRelease
)

#Dit zorgt ervoor dat als ik een input geef met mijn muis dat de counter omhoog gaat
mouseClickListener = mouse.Listener(on_click=OnClick)

keyBoardListener.start() 
mouseClickListener.start()

# Variabelen om positie bij te houden
offsetX = 0
offsetY = 0

# Functie om het bewegen te starten
def StartMove(event):
    global OffsetX, OffsetY
    OffsetX = event.x
    OffsetY = event.y

# Functie om het programma te bewegen over het scherm
def DoMove(event):
    x = window.winfo_pointerx() - OffsetX
    y = window.winfo_pointery() - OffsetY
    window.geometry(f"+{x}+{y}")

# Hier kijkt hij of je hem kan bewegen
rigbyLabel.bind("<Button-1>", StartMove)
rigbyLabel.bind("<B1-Motion>", DoMove)

customBar.bind("<Button-1>", StartMove)
customBar.bind("<B1-Motion>", DoMove)

window.mainloop()
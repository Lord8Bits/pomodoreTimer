from customtkinter import *
import threading
import time


# TODO: add a pause and reset button
# TODO: add GUI effects for the timer
# TODO: add the 5 minutes break time
# TODO: add custom timer
# FIXME: stop concurrent threads from starting causing a conflict

class Pomodoro(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x650')
        self.title('Pomodoro Timer')

        self.timer_running: bool = False
        self.timer_paused: bool = True

        self.grid_system()
        self.timer_label()
        self.buttons()

    def grid_system(self):
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
    
    def timer_label(self):
        FontManager.load_font("assests/MRKMaston-Bold.ttf")
        MRK_font = CTkFont(family="MRK Maston Bold", weight='bold', size=80)
        self.TimeLabel = CTkLabel(self, text='25:00', font=MRK_font)

        self.TimeLabel.grid(row=0, column=0, columnspan=2, pady=(0,10))
    
    def buttons(self):
        self.buttonstart = CTkButton(self, width=50, text="Start",
                                    corner_radius=32, command=self.timer_logic)
        self.buttonstart.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 4))
    
    def timer_logic(self):
        # Starting time is 25min as in the Pomodoro Technique:  
        timestart = 25*60
        # Thread that counts the time:
        counting_worker = threading.Thread(target=self._countdown, args=(timestart,))
        counting_worker.start()

    def _countdown(self, start):
        # Sleeps for 1 second and updates TimeLabel text's timer.
        self.timer_running = True
        while start >= 0 :
            time.sleep(1)
            start -= 1
            self.TimeLabel.configure(text=time.strftime("%M:%S", time.gmtime(start)))
        self.timer_running = False
            
            
app = Pomodoro()
app.mainloop()

from customtkinter import * # type: ignore
import threading
import time


# TODO: add a ringtone when timer ends
# TODO: add GUI effects for the timer
# TODO: add custom timer

class Pomodoro(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x650')
        self.title('Pomodoro Timer')

        self.workTime: float = 2 # 25 min study time
        self.breakTime: float = 5 # 5 min break time

        self.isPaused: bool = False
        self.isRunning: bool = False
        self.isReset: bool = False

        self.grid_system()
        self.timer_label()
        self.buttons()

    def grid_system(self):
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
    
    def timer_label(self):
        FontManager.load_font("assests/MRKMaston-Bold.ttf")
        MRK_font = CTkFont(family="MRK Maston Bold", weight='bold', size=80)
        self.TimeLabel = CTkLabel(self, text=time.strftime("%M:%S", time.gmtime(self.workTime))
                                  , font=MRK_font)

        self.TimeLabel.grid(row=0, column=0, columnspan=2, pady=(0,10))
    
    def buttons(self):
        self.buttonStart = CTkButton(self, width=50, text="Start",
                                    corner_radius=32, command=self.start_logic)
        
        self.buttonStart.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 4))

        self.buttonPause = CTkButton(self, width=50, text="Pause",
                                    corner_radius=32, command=self.pause_logic)
        
        self.buttonPause.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 4))
        
        self.buttonReset = CTkButton(self, width=50, text="Reset",
                                    corner_radius=32, command=self.reset_logic)
        
        self.buttonReset.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 4))
    
    def pause_logic(self):
        if self.isRunning:
            if self.isPaused:
                self.pause_event.set()
                self.isPaused = False
            else:
                self.pause_event.clear()
                self.isPaused = True
    
    
    def start_logic(self):
        if not self.isRunning:
            self.isRunning = True
            self.buttonStart.configure(state=DISABLED)
            # event variable serves for the pause logic:
            self.pause_event = threading.Event()
            self.pause_event.set()
            # Start the countdown thread:
            counting_worker = threading.Thread(target=self._countdown, args=[self.workTime], daemon=True)
            counting_worker.start()

    def reset_logic(self):
        if self.isRunning:
            self.isReset = True
        else:
            self.isReset = False


    def _countdown(self, start: float):
        # Work time logic:
        while start > 0 and not self.isReset:
            self.pause_event.wait()
            time.sleep(0.5)
            start -= 0.5
            self.TimeLabel.configure(text=time.strftime("%M:%S", time.gmtime(start)))
        
        # Break time logic:
        if start <= 0:
            start = self.breakTime # 5 minutes break
            while start > 0 and not self.isReset:
                self.pause_event.wait()
                time.sleep(0.5)
                start -= 0.5
                self.TimeLabel.configure(text=time.strftime("%M:%S", time.gmtime(start)))

        # Reset the button state back to normal and running/reset states as well as the Timer to the initial time.
        self.buttonStart.configure(state=NORMAL)
        self.TimeLabel.configure(text=time.strftime("%M:%S", time.gmtime(self.workTime)))
        
        self.isRunning = False
            
            
app = Pomodoro()
app.mainloop()

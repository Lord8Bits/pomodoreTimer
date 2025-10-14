from customtkinter import * # type: ignore
import threading
import time
import playsound
import random


# TODO: add a ringtone when timer ends
# TODO: add GUI effects for the timer
# TODO: add custom timer

class Pomodoro(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x650')
        self.title('Pomodoro Timer')

        self.work_time: float = 10 # 25 min study time
        self.break_time: float = 10 # 5 min break time

        self.is_running: bool = False
        self.is_reset: bool = False

        self.sound: str = "assests/sounds/bell.mp3"

        self.grid_system()
        self.timer_label()
        self.buttons()
        self.stop_thread()

    def grid_system(self):
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
    
    def timer_label(self):
        FontManager.load_font("assests/fonts/MRKMaston-Bold.ttf")
        MRK_font = CTkFont(family="MRK Maston Bold", weight='bold', size=80)
        self.time_label = CTkLabel(self, text=time.strftime("%M:%S", time.gmtime(self.work_time))
                                  , font=MRK_font)

        self.time_label.grid(row=0, column=0, columnspan=2, pady=(0,10))
    
    def buttons(self):
        self.button_start = CTkButton(self, width=100, text="Start",
                                    corner_radius=32, command=self.start_logic)
        
        self.button_start.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 4))
        
        self.button_reset = CTkButton(self, width=100, text="Reset",
                                    corner_radius=32, command=self.reset_logic)
        
        self.button_reset.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 4))
    
    def fun(self):
        chosen_sound = random.choices(["assests/sounds/bell.mp3", "assests/sounds/tubular_bells.mp3"], weights=[0.9, 0.1], k=1)[0]
        self.sound = chosen_sound
    def start_logic(self):
        if not self.is_running:
            self.is_running = True
            self.button_start.configure(state=DISABLED)
            # Start the countdown thread:
            counting_worker = threading.Thread(target=self._countdown, daemon=True) # Creates new thread for counting
            counting_worker.start()

    def play_sound(self):
        sound_worker = threading.Thread(target=playsound.playsound, args=[self.sound], daemon=True) # Thread for playing sound
        sound_worker.start()

    def reset_logic(self):
        if self.is_running:
            self.is_reset = True
        else:
            self.is_reset = False
        
    def stop_thread(self):
        # Resets the timer to the original value and continues the thread to stop it when isReset is True
        if self.is_reset:
            self.time_label.configure(text=time.strftime("%M:%S", time.gmtime(self.work_time)))

    def _countdown(self):
        # Work time logic:
        while not self.is_reset:
            start = self.work_time + .1
            while start > 0.1 and not self.is_reset:
                time.sleep(0.1)
                start -= 0.1
                self.time_label.configure(text=time.strftime("%M:%S", time.gmtime(start)))
            # Plays Notification Sound:
            self.fun()
            if not self.is_reset: self.play_sound() # Plays a ringtone but doesn't when reset button is pressed
            # Break time logic:
            start = self.break_time + .1 # 5 minutes break
            while start > 0.1 and not self.is_reset:
                time.sleep(0.1)
                start -= 0.1
                self.time_label.configure(text=time.strftime("%M:%S", time.gmtime(start)))
            if not self.is_reset: self.play_sound()


        # Reset the button state back to normal and running/reset states as well as the Timer to the initial time.
        self.button_start.configure(state=NORMAL)
        self.time_label.configure(text=time.strftime("%M:%S", time.gmtime(self.work_time)))
        
        self.is_running = False
        self.is_reset = False
            
            
app = Pomodoro()
app.mainloop()

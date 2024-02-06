import tkinter as tk
import time
from functools import partial
from datetime import datetime
import os 

def opendata():
    '''Import the last actions performed and the previous date'''
    if not os.path.exists('data.txt') or os.path.getsize('data.txt') == 0: #Bestäm data om filen ej finns
        GUI.last_date = 'first time playing!'
        GUI.last_time = time.time()
        GUI.size = 350
        GUI.sequence = ['study ', 'sleep ']
    else:
        with open('data.txt', '+a') as file:
            file.seek(0)
            GUI.last_date = file.readline()
            GUI.last_time = file.readline()
            GUI.size = float(file.readline().strip())
            GUI.sequence = file.readline()
            GUI.sequence += file.readline()
            GUI.sequence = GUI.sequence.splitlines()
    GUI.last_sequence = GUI.sequence   

class GUI:
    '''The tkinter GUI'''
    def __init__(self):
        #Main parts of the GUI system
        self.root = tk.Tk()
        self.root.title('Tamagotchi')

        #Centering the application in the middle of the screen
        self.w = 500 
        self.h = 500 

        self.screen_width = self.root.winfo_screenwidth()  
        self.screen_height = self.root.winfo_screenheight() 
        self.x = (self.screen_width/2) - (self.w/2)
        self.y = (self.screen_height/2) - (self.h/2)

        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        #Time info
        self.time_diff = int(time.time() - float(self.last_time)) 
        self.label = tk.Label(self.root, text = 'Welcome back! \n Last time playing: ' +
                              str(self.last_date) + 'Tamagotchi has been left alone for ' + 
                              str(self.time_diff // (24 * 3600)) + ' days, ' + 
                              str((self.time_diff % (24 * 3600)) // 3600)+ ' hours, ' + 
                              str((self.time_diff % 3600) // 60) + ' minutes and ' + 
                              str(self.time_diff % 60) + ' seconds.')
        self.label.pack()

        #Picture of the Tamagotchi
        self.original_size = 350
        self.canvas = tk.Canvas(self.root, width = self.original_size, height = self.original_size, bg = 'white' )
        self.canvas.pack()
        self.tamagotchi = self.canvas.create_oval(self.original_size-self.size, self.original_size-self.size, self.size, self.size, fill = 'black')

        #Action options
        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        self.btn1 = tk.Button(self.buttonframe, text = 'Sleep', command = partial(action, self, 1)) 
        self.btn1.grid(row=0, column=0, sticky='news') 

        self.btn2 = tk.Button(self.buttonframe, text = 'Party', command = partial(action, self, 2))
        self.btn2.grid(row=0, column=1, sticky='news')

        self.btn3 = tk.Button(self.buttonframe, text = 'Take Exam', command = partial(action, self, 3))
        self.btn3.grid(row=1, column=0, sticky='news')

        self.btn4 = tk.Button(self.buttonframe, text = 'Study', command = partial(action, self, 4))
        self.btn4.grid(row=1, column=1, sticky='news')

        #Binding buttons to key presses
        self.btn1.bind('<Button-1>', partial(button_press, self))
        self.btn2.bind('<Button-1>', partial(button_press, self))
        self.btn3.bind('<Button-1>', partial(button_press, self))
        self.btn4.bind('<Button-1>', partial(button_press, self)) 

        self.buttonframe.pack(fill='x')

        #Feedback for the player
        self.label = tk.Label(self.root, text = 'Good luck!')
        self.label.pack()   

        #Save the data before closing!
        self.root.protocol('WM_DELETE_WINDOW', partial(closing, self))

        #Time since last key press
        self.last_button_press_time = 0

        #Has the action sequence changed?
        self.change = False

        #Recursive function that checks the last three actions performed
        self.root.after(1, lambda: tamagotchi_reacts(self))  
        self.root.after(3000, lambda: inactive(self)) 
        self.root.after(1, lambda: check_for_change(self))
        self.root.after(1, lambda: tamagotchi_color(self))

def inactive(self):
    '''Reaction for inactivity'''
    self.current_time = time.time()

    if self.current_time - self.last_button_press_time > 3:
        self.size = self.size * 0.95 
        self.label.config(text = 'I am bored!')
        tamagotchi_size(self)

    self.root.after(3000, lambda: inactive(self)) 

def tamagotchi_color(self):
    '''Updates the color of Tamagotchi'''
    if self.size >= self.original_size * 0.8:
        self.canvas.itemconfig(self.tamagotchi, fill = '#00FF00')

    elif self.size >= self.original_size * 0.7:
        self.canvas.itemconfig(self.tamagotchi, fill = '#FFFF00')

    elif self.size <= self.original_size * 0.6:
        self.canvas.itemconfig(self.tamagotchi, fill = '#FF0000') 

    self.root.after(1, lambda: tamagotchi_color(self))       

def check_for_change(self):
    '''Checks if there's been a change in the action sequence'''
    if self.last_sequence != self.sequence:
        self.change = True 

    self.root.after(1, lambda: check_for_change(self)) 

def tamagotchi_reacts(self):
    '''Reactions for different sequences of actions'''  
    if len(self.sequence) >= 3 and self.change == True:

        if self.sequence[-3] == self.sequence[-2] and self.sequence[-3] == self.sequence[-1]:
            self.size = self.size * 0.75
            self.label.config(text = 'Mix it up!')
            tamagotchi_size(self) 

        elif self.sequence[-3:] == ['study ', 'exam ', 'party '] or self.sequence[-3:] ==['study ', 'party ', 'sleep ']:     
            self.size = self.size * 1.05
            self.label.config(text = 'Good choice!')
            tamagotchi_size(self) 

        elif self.sequence[-3:] == ['party ', 'exam ', 'study '] or self.sequence[-3:] == ['study ', 'sleep ', 'study ']:     
            self.size = self.size * 0.95 
            self.label.config(text = 'Bad choice!')   
            tamagotchi_size(self)   

        self.change = False         
        self.last_sequence = self.sequence 

    self.root.after(1, lambda: tamagotchi_reacts(self)) 

def tamagotchi_size(self):
    '''Updates the size of Tamagotchi'''
    if self.size > self.original_size:
        self.size = self.original_size

    elif self.size < self.original_size / 2:
        self.size = self.original_size / 2

    self.canvas.coords(self.tamagotchi, (self.original_size-self.size, self.original_size-self.size, self.size, self.size))

def action(self, a):
        '''Action is appended to the list'''
        if a == 1:
            with open('sequence.txt', 'a') as file:
                file.write('\nsleep ')

        elif a == 2:
            with open('sequence.txt', 'a') as file:
                file.write('\nparty ')

        elif a == 3:
            with open('sequence.txt', 'a') as file:
                file.write('\nexam ')

        elif a == 4:        
            with open('sequence.txt', 'a') as file:
                file.write('\nstudy ')

        with open('sequence.txt', 'r') as file:
            self.sequence = file.read().splitlines()  

def button_press(self, event):
    '''Saves time for the last click on one of the buttons'''
    self.last_button_press_time = time.time()

def closing(self):
    '''Saves data in the .txt files'''
    # Get the current timestamp
    timestamp = time.time()
    # Convert timestamp to a datetime object
    date_object = datetime.fromtimestamp(timestamp)
    # Format the datetime object as a string
    formatted_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
    
    with open('data.txt', 'w') as file:
        file.write(str(formatted_date) + '\n') #Date
        file.write(str(time.time()) + '\n') #Date to check how long has gone since the previous execution
        file.write(str(self.size) + '\n') #Tamagotchi's size
        file.write(str(self.sequence[-2]) + '\n' + str(self.sequence[-1])) #The last two actions performed

    self.root.destroy() 

def main():
    '''Main function'''  
    try:   
        opendata()
        gui = GUI()        
        gui.root.mainloop()

    except Exception as e:
        closing(gui)

        root = tk.Tk()
        w = 500 
        h = 50

        screen_width = root.winfo_screenwidth()  
        screen_height = root.winfo_screenheight() 
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        label = tk.Label(root, text = 'An error occured: ' + str(e) + '.')
        label.pack()
        okay = tk.Button(root, text = 'OK', command = root.destroy)
        okay.pack()
        root.mainloop()

if __name__ == '__main__': 
    main()

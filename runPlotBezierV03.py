import tkinter as tk
import plotBezierV03 as pb

root = tk.Tk()

root.geometry("240x220")
root.title('Incremental Integer Bezier')
root.resizable(0, 0)
root.grid_columnconfigure((0, 1), weight=0)
root.attributes('-toolwindow', True)

labels = []
XY = ['X', 'Y']
intlist = []
entryList = []
buttonList = []
buttonText = ['Cubic', 'Alt','Cancel','OK']
buttonState = [False, False, False, False]

def get_entry_fields():
    elist = [entryList[0].get(), entryList[2].get(), entryList[4].get(),
          entryList[1].get(), entryList[3].get(), entryList[5].get()]
    for idx in range(0,6):
        try:
            intlist.append(int(elist[idx]))
        except ValueError:
            intlist.append(0)
            print("\'" + elist[idx] + "##### \' is not an integer #####")
 
def generate_labels():
    for i in range(0, 12, 2):
        ro = i//4
        co = i % 4
        num = str(ro + 1)
        letter = XY[co//2]
        tk.Label(root, text=letter+num).grid(row=ro, column=co, padx=15, pady=5)
        newent = tk.Entry(root, width=5)
        newent.grid(row=ro, column=co + 1, pady=5)
        val2=newent.get()
        entryList.append(newent)

def generate_buttons():
    for idx in range(4):
        ro = idx//2
        co = idx % 2
        newbutton = tk.Button(text=buttonText[idx], width = 5,\
            command = lambda: change_state(idx) )
        newbutton.grid(row=3+ro, column = co + 1, padx=15, pady=5)#, columnspan=2)
        buttonList.append(newbutton)

def toggle_button_state(button,idx):
    if buttonState[idx] == False:
        button.config(relief='sunken', fg = 'red' )
        buttonState[idx] = True
    else:
        button.config(relief='raised', fg = 'black')
        buttonState[idx] = False

def change_state(idx):
    button = buttonList[idx]
    button.config(text = buttonText[idx])
    if idx == 0:
        toggle_button_state(button,0)
    elif idx == 1:
        toggle_button_state(button,1)
    elif idx == 2:
        root.quit()
    else:
        get_entry_fields() 
        X = intlist[:3]
        Y = intlist[3:]
        isCubic = buttonState[0]
        isAlt = buttonState[1]
        if False:    ### reality check
            isCubic = True
            iaAlt = True
            X = [1000, -1000, 2000]
            Y = [5000,  1000, 2000]        
        pb.plotBezier(X,Y,isCubic,isAlt)
        root.quit()

generate_labels()
generate_buttons()
root.mainloop()

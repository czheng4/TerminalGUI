import tkinter as tk
from tkinter import ttk
import subprocess
from tkinter import *
import functools
import json
from lib.tooltip import CreateToolTip 

# name conversion
#Label   lbl lbl_name
#Button  btn btn_submit
#Entry   ent ent_age
#Text    txt txt_notes
#Frame   frm frm_address


def create_canvas(tab):
    canvas = tk.Canvas(tab, width = 770,height = 550, scrollregion = (0, 0, 300, 1000))
    canvas.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(tab, command=canvas.yview)
    scrollbar.pack(side=tk.LEFT, fill='y', expand=True)

    canvas.configure(yscrollcommand = scrollbar.set)

    return canvas


# Tab control class that allows you to add tabs and retrive tabs
class TabControl:
    def __init__(self, window):
        self.window = window
        self.tabs = {}
        self.tab_control = ttk.Notebook(window)

    def addTab(self, name):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=name, sticky="nw")
        self.tabs[name] = tab

    def getTabByName(self, name):
        return self.tabs[name]

    def pack(self, **options):
        self.tab_control.pack(options)

class Terminal:
    def __init__(self, window, tab):
        self.tab = tab
        self.window = window


        self.texts = []       # all the texts
        self.entries = []     # all the command entires to type in



    def enterCallback(self, event, arg):
        print(event, arg)
        out = ""
        ent = self.entries[arg]
        text = self.texts[arg]
        # out = subprocess.check_output(ent.get(), stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        


        try :
            out = subprocess.check_output(ent.get(), stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        except:
            pass

       
        # if (out == ""): out = "Command \"{}\" is not found".format(ent.get())
        text.config(text = out)


        if arg == len(self.texts) - 1: self.newCommand()

        self.tab.update()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas.yview_scroll(3000, "units")



    def bound_to_mousewheel(self, event):
        fp = functools.partial
        self.canvas.bind_all("<Button-5>", fp(self.on_mousewheel, scroll=1))
        self.canvas.bind_all("<Button-4>", fp(self.on_mousewheel, scroll=-1))
       

    def unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def on_mousewheel(self, scroll):
        self.canvas.yview_scroll(int(scroll), "units")


    def on_configure(self, event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


    def render(self):

        canvas = create_canvas(self.tab)
        
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', self.on_configure)

        # --- put frame in canvas ---
        self.frame = tk.Frame(canvas)

        canvas.bind('<Enter>', self.bound_to_mousewheel)
        canvas.bind('<Leave>', self.unbound_to_mousewheel)
        canvas.create_window((600, 0), window=self.frame)
        canvas.pack()
        self.canvas = canvas
        self.newCommand()
        

    def newCommand(self):

        # get row number
        command_id = len(self.texts)
        row=command_id * 2

        # create the new command prompt and new empty text.

        pwd = subprocess.check_output("pwd", shell=True).decode("utf-8")[:-1] + ": "
        tk.Label(master=self.frame, text=pwd, fg="red").grid(column = 0, row = row, padx=5)
        ent = tk.Entry(master=self.frame, width=55)
        ent.grid(column = 1, row = row)
        ent.bind('<Return>', lambda event, command_id=command_id : self.enterCallback(event,command_id))
        text = tk.Label(master=self.frame, text="", justify="left", wraplength=500)
        text.grid(column=0, columnspan=100, row=row + 1, sticky="w", padx=5)

        self.entries.append(ent)
        self.texts.append(text)

class UserCommands:
    
    def __init__(self, window, tab):
        self.tab = tab
        self.window = window


        ## it's an array of array, the first index is the commnad id, the second index is t
        self.all_vars = []
        self.all_flags = []
        self.all_commands_labels = []

        with open('data/commands.json') as f:
            self.all_commands = json.load(f)
       
    def bound_to_mousewheel(self, event):
        fp = functools.partial
        self.canvas.bind_all("<Button-5>", fp(self.on_mousewheel, scroll=1))
        self.canvas.bind_all("<Button-4>", fp(self.on_mousewheel, scroll=-1))
       

    def unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def on_mousewheel(self, scroll):
        self.canvas.yview_scroll(int(scroll), "units")


    def on_configure(self, event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def getCommand(self, id):
        pass


    def sel(self):
        print(self.var.get())
        pass
        # selection = "You selected the option " + str(var.get())
        # label.config(text = selection)


    def print_selection(self):
        pass

    def execute(self, id):

        command = self.all_commands[id]["command_name"]

        for f, var in zip(self.all_flags[id], self.all_vars[id]):
            if f != "" and var.get() != "": command += " " + f + " " + var.get()
            else: command += " " + var.get()



        text = self.all_commands_labels[id]
        text.delete(0, END)
        text.insert(0, command)
        print(command)
        return command

       


    def render(self):


        canvas = create_canvas(self.tab)
        
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', self.on_configure)
        
        # canvas.bind_all("<MouseWheel>", lambda event, canvas=canvas : on_mousewheel(event, canvas))

        # --- put frame in canvas ---
        self.frame = tk.Frame(canvas)

        canvas.bind('<Enter>', self.bound_to_mousewheel)
        canvas.bind('<Leave>', self.unbound_to_mousewheel)
        canvas.create_window((0, 0), window=self.frame)
        canvas.pack()
        self.canvas = canvas

        fp = functools.partial



        row_num = 0
        for count, command in enumerate(self.all_commands):


            command_vars = []
            flags = []

            f =  tk.Frame(self.frame)
            # print(command)
            name = command["command_name"]
            label = tk.Label(f, text = name, font=("Arial", 20)).pack(side = "left", anchor = 'w')
            f.grid(row = row_num, column = 0, sticky="w")
            row_num = row_num + 1


            for name, widget in command["categories"].items():
                flag = ""
                if "argument" in widget: flag = widget["argument"]
                

                f = tk.Frame(self.frame)
                label = tk.Label(f, text = name + ": ")
                label.pack(padx = 10, side = "left", anchor = 'w')


                f.grid(row = row_num, column = 0, sticky="w")
                row_num = row_num + 1

                wtype = widget["widget_type"]
                if wtype == "radio_button":

                    var = tk.StringVar(value=widget["options"][0])
                    command_vars.append(var)
                    flags.append(flag)
                    # f.grid(row = 0, column = 0, sticky = 'w')
                    for option, description in zip(widget["options"], widget["description"]):
                        if wtype == "radio_button":
                            rb = tk.Radiobutton(f, text=option + "  ", variable=var, value=option)
                            rb.pack(side = "left", anchor = tk.W)
                            CreateToolTip(rb, text = description)


                elif wtype == "checkbox":
                    for option, description in zip(widget["options"], widget["description"]):
                        var = tk.StringVar(value="")

                        # if "argument" in widget: 
                        command_vars.append(var)
                        flags.append(flag)
                        cb = tk.Checkbutton(f, text=option + "  ",variable=var, onvalue=option, offvalue="")
                        cb.pack(side = "left", anchor = tk.W)
                        CreateToolTip(cb, text = description)


                elif wtype == "text":
                    ent = tk.Entry(f, width=55)
                    ent.pack(side = "left", anchor = tk.W)
                    command_vars.append(ent)
                    flags.append(flag)
                    CreateToolTip(ent, text = widget["description"])

            f = tk.Frame(self.frame)
            f.grid(row = row_num, column = 0, sticky="w")
            row_num = row_num + 1
            tk.Button(f, text = "Show Command", command = fp(self.execute, id=count)).pack(padx = 10, side = "left", anchor = tk.W)
            label = tk.Entry(f, text = "", width = 70)
            label.pack(padx = 10, side = "left", anchor = tk.W)

            self.all_commands_labels.append(label)
            self.all_vars.append(command_vars)
            self.all_flags.append(flags)
            # self.all_commands_labels = []
                # print(name, widget)
                # for name, widget in category.items():

                #     print(name, widget)


        for var in command_vars:
            if var.get() != "":
                print(var.get())


        # f =  tk.Frame(self.tab)
        # self.var = tk.IntVar(value=1)
        # var = self.var
        # self.var.set(1)


        # f.grid(row = 0, column = 0, sticky = 'w')
        # R1 = tk.Radiobutton(f, text="Option 1", variable=var, value=1,
        #                   command=self.sel)

        # R1.pack( side = "left", anchor = tk.W )

        # R2 = tk.Radiobutton(f, text="Option 2", variable=var, value=2,
        #                   command=self.sel)

        # R2.pack( side = "left", anchor = tk.W)

        # R3 = tk.Radiobutton(f, text="Option 3", variable=var, value=3,
        #                   command=self.sel)

        # R3.pack( side = "left", anchor = tk.W)


        # f = tk.Frame(self.tab)
        # f.grid(row = 1, column = 0, sticky = 'w')
        
        # var1 = tk.IntVar()
        # var2 = tk.IntVar()
        
        # c1 = tk.Checkbutton(f, text='Python',variable=var1, onvalue=1, offvalue=0, command=self.print_selection)
        # c1.pack(side = "left", anchor = tk.W)
        # c2 = tk.Checkbutton(f, text='C++',variable=var2, onvalue=1, offvalue=0, command=self.print_selection)
        # c2.pack(side = "left")


        # f = tk.Frame(self.tab)
        # f.grid(row = 2, column = 0, sticky = 'w')
        # ent = tk.Entry(master=f, width=55)
        # ent.pack(side = "left")





def main():
    window = tk.Tk()
    window.title("Terminal GUI")
    window.geometry("800x500")

    # window.resizable(width=False, height=False)

    style = ttk.Style(window)
    style.theme_use('classic')
    # ttk.Style(window).configure("TLABEL", foreground="red", background="white")

  
    

    tab_control = TabControl(window)
    tab_control.addTab("Terminal")
    tab_control.addTab("User Commands")
    tab_control.addTab("Pipe")
    tab_control.pack(expand=True, fill ="both")

    
    tab1 = tab_control.getTabByName("Terminal")
    tab2 = tab_control.getTabByName("User Commands")
    tab3 = tab_control.getTabByName("Pipe")
    # tab1.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
      
    
    terminal = Terminal(window, tab1)
    terminal.render()


    user_commands = UserCommands(window, tab2)
    user_commands.render()


    ttk.Label(tab3,
              text ="Implement pipe here").pack()
  
    window.mainloop()





if __name__ == "__main__":
    main()

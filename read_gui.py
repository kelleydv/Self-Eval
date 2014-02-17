from tkinter import Tk, Text, Button, Label, Frame, Listbox



class ResponseGui:
    def __init__(self, root):
        optframe = Frame(root)
        optframe.pack(side='right')
        
        txtframe = Frame(root)
        txtframe.pack(side='left')
        
        self.options = Listbox(optframe)
        self.options.pack()
        self.current=None
        self.opt_callbacks=[]
        self.poll()

        self.maintext = Text(txtframe)
        self.maintext.pack()
        

    def update_options(self, options):
        """ Expects a list of name,callback pairs
        """

        self.options.delete(0,'END')
        self.opt_callbacks = []

        for name,func in options:
            self.options.insert(-1,name)
            self.opt_callbacks.append(func)

        return self

    def update_text(self, string):
        self.maintext.insert('1.0',string)
        return self

    def poll(self):
        selection = self.options.curselection()
        if selection != self.current:
            self.current = selection
            print(selection)
            if selection:
                self.opt_callbacks[int(*selection)]()
        self.options.after(200, self.poll)

    

root = Tk()
root.title("Self-Eval Responses")
foo = ResponseGui(root)

options = [('Hi there', lambda:foo.update_text('Hello')), ('Byebye', lambda:foo.update_text('Goodbye'))]


foo.update_options(options)

root.mainloop()

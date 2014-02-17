from tkinter import Tk, Text, Button, Label, Frame, Listbox

class ResponseGui:
    def __init__(self, root):
        optframe = Frame(root)
        optframe.pack(side='right')
        
        txtframe = Frame(root)
        txtframe.pack(side='left')
        
        btnframe = Frame(root)
        btnframe.pack(side='bottom')
        
        self.options = Listbox(optframe)
        self.options.pack()
        self.current=None
        self.opt_callbacks=[]
        self.poll()

        self.maintext = Text(txtframe)
        self.maintext.pack()

        
        self.buttonlabel = Label(btnframe)
        self.buttonlabel.pack()
        self.button = Button(btnframe)
        self.button.pack()
        self.update_button()
        

    def update_options(self, options):
        """ Expects a list of name,callback pairs
        """

        self.options.delete(0,'end')
        self.opt_callbacks = []

        for name,func in options:
            self.options.insert('end',name)
            self.opt_callbacks.append(func)

        return self

    def update_text(self, string):
        self.maintext.delete('0.0', 'end')
        self.maintext.insert('1.0',string)
        return self

    def poll(self):
        selection = self.options.curselection()
        if selection != self.current:
            self.current = selection
            if selection:
                self.opt_callbacks[int(*selection)]()
        self.options.after(200, self.poll)

    def update_button(self, text='Go!', label='Usesless button.', func=lambda:True):
        self.button.config(text=text, command=func)
        self.buttonlabel.config(text=label)
        self.button.pack()
        
    
def main():
    root = Tk()
    root.title("Self-Eval Responses")
    foo = ResponseGui(root)
    
    options = [('Hi there', lambda:foo.update_text('Hello')), ('Byebye', lambda:foo.update_text('Goodbye'))]
    foo.update_options(options)
    
    root.mainloop()

from gui import ResponseGui
from tkinter import Tk
from compass import ResponseReader

root = Tk()
root.title("Self-Eval Responses")
app = ResponseGui(root)

refs = ResponseReader(configFile = 'config.json', update=False)

def main():
    
    def view_recent(date):
        classes = refs.classes(date)
        txt = ''
        for x in classes:
            txt+=str(x)+'\n'
            for r in classes[x]:
                txt+= ''.join(['\t',r[refs.ID_COL],'\n'])
        app.update_text(txt)

        def select_class(): 
            def list_students(class_): 
                def show_response(r): 
                    def write_response(r):

                        with open('responses/'+r[1]+'.txt', 'w+') as f:
                            f.write(txt)

                    txt = ''.join(['\t', r[1], '\n\t', r[3], '\n\t', r[4], '\n\n'])
                    for i,e in enumerate(r[5:]):
                        if e:
                            if len(e) > 20:
                                wordcount = 'wordcount: %d' % len(e.split(' '))
                            else:
                                wordcount = ''
                            txt+=''.join(['****', refs.labels()[i+5], '\n\t', e, '\n', wordcount, '\n\n'])
                    app.update_text(txt)
                    app.update_button(label='Respond to reflection', text='Go', func=lambda r=r:write_response(r))
                
                app.update_text(txt)
                options = [(r[refs.ID_COL],lambda r=r:show_response(r)) for r in class_]
                options.append(('Back', select_class))
                app.update_options(options)
            
            app.update_button()
            app.update_text(txt)
            options = [(x,lambda x=x:list_students(classes[x])) for x in classes]
            options.append(('Back', lambda:view_recent(date)))
            app.update_options(options)

        app.update_options([
            ('Select Class', select_class),
            ('Back', main),
        ])

    
    app.update_options([
        ('View Recent', lambda:view_recent('2/12/2014')),
        ('Quit', root.quit)
    ])

main()



root.mainloop()
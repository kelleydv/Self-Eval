from compass import ResponseReader

foo = ResponseReader(configFile = 'config.json', update = True)

classes = foo.classes('2/12/2014')




for x in classes.keys():
    print(x)
    for r in classes[x]:
        print('\t',r[1])

input()

for x in classes.keys():
    for r in classes[x]:
        foo._clear()
        print('\t', r[1], '\n\t', r[3], '\n\t', r[4], '\n\n')
        for i,e in enumerate(r[5:]):
            if e:
                if len(e) > 20:
                    wordcount = 'wordcount: %d' % len(e.split(' '))
                else:
                    wordcount = ''
                print('****', foo.labels()[i+5], '\n\t', e, '\n', wordcount, '\n\n')
        input()



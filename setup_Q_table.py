import itertools
import csv

#STATES:
#wall left, wall right, wall up, wall down, moving left, moving right, moving up, moving down, food left, food right, food up, food down 

#ACTIONS:
#left, right, up, down
def make_states():
    table = list(itertools.product([False, True], repeat=12)) #wow this is big lol

    #Removing "bad" states for clarity. Might leave in if run into problems later, as they never should show up,
    #but thinking it might be helpful to visual debug somewhat.

    #Doesn't work for some reason, some slip through but I think it should be fine
    #for i in table:
    #    #Can only have one direction it is moving in
   #     if (i[4] == True):
    #        if (i[5] == True or i[6] == True or i[7] == True):
    #            try:
    #                table.remove(i)
    #            except:
     #               pass
    #    if (i[5] == True):
     #       if (i[4] == True or i[6] == True or i[7] == True):
     #           try:
     #               table.remove(i)
    #            except:
    #                pass
    #    if (i[6] == True):
    #        if (i[4] == True or i[5] == True or i[7] == True):
     #           try:
     #               table.remove(i)
     #           except:
     #               pass
     #   if (i[7] == True):
     #       if (i[4] == True or i[5] == True or i[6] == True):
    #            try:
    #                table.remove(i)
    #            except:
    #                pass
     #   
     #   #Removing food is left-and-right and up-and-down
    #    if (i[8] == True and i[9] == True):
    #        try:
     #           table.remove(i)
    #        except:
    #            pass
    #    if (i[10] == True and i[11] == True):
    #        try:
    #            table.remove(i)
    #        except:
    #            pass
    #            
    return table

def make_q_table():
    states = make_states()
    Q_table = {}

    for s in states:
        Q_table[s] = [0, 0, 0, 0]
    
    return Q_table


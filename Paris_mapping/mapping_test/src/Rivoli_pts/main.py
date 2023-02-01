import pandas as pd

def naming_index(index,pos):
    s = "pt" + str(index) +"p" + str(pos)
    return s

def posXandY(x,y,pos):
    x_offset = 0
    y_offset = 0
    if pos == 0 :
        x_offset = -0.5
        y_offset = +0.5
    elif pos == 1 :
        x_offset = +0.5
        y_offset = +0.5
    elif pos == 2 :
        x_offset = -0.5
        y_offset = -0.5
    elif pos == 3 :
        x_offset = +0.5
        y_offset = -0.5

    return '[' + str(x+x_offset) + "," + str(y+y_offset) + ']; '

df = pd.read_csv(r'Points.csv', sep=';') # Points importation

dataCSV = pd.DataFrame(df, columns=['X', 'Y']) # We only want X and Y

f = open("freefem_code.txt", "w") # Creating/Opening file in writing mode


string ="real [int] "

# Points definition
for index, row in dataCSV.iterrows() : # For every rows
   
    for i in range (0,4) :
        string += str(naming_index(index,i)) +"(2)"
        
        if index!=len(dataCSV)-1 or i != 3 : 
            string += ", "

string += ";\n\n"
f.write(string)



# Points coordinates
for index, row in dataCSV.iterrows() : # For every rows
    for i in range (0,4) :
        string = str(naming_index(index,i)) +" = "+ posXandY(row['X'],row['Y'],i) 
        f.write(string)

f.close()



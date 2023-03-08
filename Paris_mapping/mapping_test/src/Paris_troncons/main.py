#dictionarie python : https://www.w3schools.com/python/python_dictionaries.asp
import pandas as pd


def posXandY(x,y,pos):
    global_offset = 0.00005
    x_offset = 0
    y_offset = 0
    if pos == 0 :
        x_offset = -global_offset
        y_offset = -global_offset
    elif pos == 1 :
        x_offset = -global_offset
        y_offset = +global_offset
    elif pos == 2 :
        x_offset = +global_offset
        y_offset = +global_offset
    elif pos == 3 :
        x_offset = +global_offset
        y_offset = -global_offset

    return '[' + str(x+x_offset) + "," + str(y+y_offset) + ']; '

def printBorder(name1, name2, number_of_borders):
    return "border c"+str(number_of_borders) +"(t=0,1){x=(1-t)*"+name1+"[0]+t*"+name2+"[0]; y=(1-t)*"+name1+"[1]+t*"+name2+"[1];}\n"

def writeBorder(f,line, number_of_borders):
    f.write(line)
    number_of_borders = number_of_borders+1
    return number_of_borders

def writeBordersOfPoint(f, number_of_borders,point, left, right, bottom, top):
    if left == 0:
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,0),printPoint4(point,1), number_of_borders),number_of_borders)      
    if right == 0:
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,2),printPoint4(point,3), number_of_borders),number_of_borders)
    if bottom == 0:
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,0),printPoint4(point,3), number_of_borders),number_of_borders)
    if top == 0:
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,1),printPoint4(point,2), number_of_borders),number_of_borders)
    return number_of_borders

def printPoint4(start, index): 
    return start +  'p' + str(index)

def whereIsPInRelationToO(rowO, rowP, left, right, bottom, top):
     #the original point 'O'
    xRow0A = float(rowO.split(',')[0])
    yRow0A = float(rowO.split(',')[1])

    #the point 'P' we want to know if this is on right, left, bottom or top
    xRow1B = float(rowP.split(',')[0])
    yRow1B = float(rowP.split(',')[1])

    aboveD1 = False
    aboveD2 = False
    
    if yRow1B - (xRow1B + (yRow0A-xRow0A))>=0: #line d1 : 
        aboveD1=True
    if yRow1B - (-xRow1B + (yRow0A+xRow0A))>=0: #line d2 : 
        aboveD2=True

    #if top, bottom, right, left
    if aboveD1 and aboveD2 :
        top=top+1
    elif aboveD1 and not aboveD2 :
        left=left+1
    elif not aboveD1 and aboveD2: 
        right=right+1
    else:
        bottom=bottom+1
    return  left, right, bottom, top

df = pd.read_csv(r'arr15.csv', sep=';') # Points importation

dataCSV = pd.DataFrame(df, columns=['A', 'B']) # We only want A and B

f = open("freefem_code.txt", "w") # Creating/Opening file in writing mode



points_array={}
number_of_points = 0

# Points dict definition
for index, row in dataCSV.iterrows() : # For every rows

    if not (row['A'] in points_array) :
        points_array[row['A']] = ["pt" + str(number_of_points), 0]
        number_of_points = number_of_points+1
    
    if not (row['B'] in points_array) :
        points_array[row['B']] = ["pt" + str(number_of_points),0]
        number_of_points = number_of_points+1

string ="real [int] "



#Point def on string
y=0
for x in points_array :
    for i in range (0,4) :
        string +=printPoint4(points_array[x][0],i)  +"(2)"
        if len(points_array)-1 != y or i != 3 :
            string += ", "
    y = y +1

string += ";\n\n"
f.write(string)

#Points coordinates
for x in points_array :
    for i in range (0,4) :
        string =printPoint4(points_array[x][0],i) + " = " + posXandY(float(x.split(',')[0]),float(x.split(',')[1]),i)
        f.write(string)

string = "\n\n"
f.write(string)


number_of_borders = 0
#to know if point is under or above a line : https://fr.moonbooks.org/Articles/Cr%C3%A9er-un-algorithme-pour-v%C3%A9rifier-si-un-point-et-au-dessus-ou-au-dessous-dune-droite/
for index, row0 in dataCSV.iterrows() : # For every lines
    print(str(points_array[row0['A']][0]) + str(" -> ") + str(points_array[row0['B']][0]))


    #for the point A on the line = point O
    if points_array[row0['A']][1] == 0: #if not already marked (already points placed)
        points_array[row0['A']][1] = 1 #we mark it
        left=0
        right=0
        bottom=0
        top=0

        #For every lines, we check if there is the same point on A or B
        #If there is, if this is on A, we check the position of B in relation to A
        #           , if this is on B, we check the position of A in relation to B 
        for index1, row1 in dataCSV.iterrows() : # For every lines
            if index1 != index : #if not same line
                if points_array[row0['A']][0] == points_array[row1['A']][0] :  #if same point on the other line
                    #we check where is B of row 1 (we will call it P) in relation to point A on row 0 (we will call it O)
                    left, right, bottom, top = whereIsPInRelationToO(row0['A'],row1['B'],left,right,bottom,top)
                
                if points_array[row0['A']][0] == points_array[row1['B']][0] :  #if same point on the other line
                    #we check where is A of row 1 (we will call it P) in relation to point A on row 0 (we will call it O)
                    left, right, bottom, top = whereIsPInRelationToO(row0['A'],row1['A'],left,right,bottom,top)
            else :#if same line
                left, right, bottom, top = whereIsPInRelationToO(row0['A'],row1['B'],left,right,bottom,top)

        number_of_borders= writeBordersOfPoint(f, number_of_borders,points_array[row0['A']][0], left, right, bottom, top)
        print('A ' + points_array[row0['A']][0] + ' : ' +str(left) + ',' +str(right) + ',' + str(bottom) + ',' + str(top))

    #for the point B on the line = point O
    if points_array[row0['B']][1] == 0: #if not already marked (already points placed)
        points_array[row0['B']][1] = 1 #we mark it
        left=0
        right=0
        bottom=0
        top=0
        #For every lines, we check if there is the same point on A or B
        #If there is, if this is on A, we check the position of B in relation to A
        #           , if this is on B, we check the position of A in relation to B 
        for index1, row1 in dataCSV.iterrows() : # For every lines
            if index1 != index : #if not same line
                if points_array[row0['B']][0] == points_array[row1['A']][0] :  #if same point on the other line
                    #we check where is B of row 1 (we will call it P) in relation to point A on row 0 (we will call it O)
                    left, right, bottom, top = whereIsPInRelationToO(row0['B'],row1['B'],left,right,bottom,top)
                
                if points_array[row0['B']][0] == points_array[row1['B']][0] :  #if same point on the other line
                    #we check where is A of row 1 (we will call it P) in relation to point A on row 0 (we will call it O)
                    left, right, bottom, top = whereIsPInRelationToO(row0['B'],row1['A'],left,right,bottom,top)
            else :#if same line
                left, right, bottom, top = whereIsPInRelationToO(row0['B'],row1['A'],left,right,bottom,top)

        number_of_borders= writeBordersOfPoint(f, number_of_borders,points_array[row0['B']][0], left, right, bottom, top)
        print('B ' + points_array[row0['B']][0] + ' : ' +str(left) + ',' +str(right) + ',' + str(bottom) + ',' + str(top))
    
    #for border of the line
    left=right=bottom=top=0
    left, right, bottom, top = whereIsPInRelationToO(row0['A'],row0['B'],left,right,bottom,top)

    if left == 1:
        number_of_borders= writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],1),printPoint4(points_array[row0['B']][0],2), number_of_borders), number_of_borders)
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],0),printPoint4(points_array[row0['B']][0],3), number_of_borders), number_of_borders)
    elif right == 1:
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],2),printPoint4(points_array[row0['B']][0],1), number_of_borders), number_of_borders)
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],3),printPoint4(points_array[row0['B']][0],0), number_of_borders), number_of_borders)
    elif top == 1:
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],1),printPoint4(points_array[row0['B']][0],0), number_of_borders), number_of_borders)
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],2),printPoint4(points_array[row0['B']][0],3), number_of_borders), number_of_borders)
    elif bottom == 1:
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],0),printPoint4(points_array[row0['B']][0],1), number_of_borders), number_of_borders)
        number_of_borders=writeBorder(f,printBorder(printPoint4(points_array[row0['A']][0],3),printPoint4(points_array[row0['B']][0],2), number_of_borders), number_of_borders)


#plot borders
string ="\nplot("
for i in range(0,number_of_borders): 
    string+="c"+str(i)+"(1)"
    if i != number_of_borders-1: 
        string+="+"

string +=");"
f.write(string)

#mesh def

string ="\n\nmesh Th = buildmesh("
for i in range(0,number_of_borders): 
    string+="c"+str(i)+"(50)"
    if i != number_of_borders-1: 
        string+="+"

string +=");"
string+="\nplot(Th, ps = \"mesh.eps\");"
f.write(string)


f.close()
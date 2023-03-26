import pandas as pd
import math

#Variables globales

offset = 90

# Si le coefficient directeur de la droite est égal à 0
def posXandY(x,y,pos):
    x_offset = 0
    y_offset = 0
    if pos == 0 :
        x_offset = -offset
        y_offset = -offset
    elif pos == 1 :
        x_offset = -offset
        y_offset = +offset
    elif pos == 2 :
        x_offset = +offset
        y_offset = +offset
    elif pos == 3 :
        x_offset = +offset
        y_offset = -offset
    return '[' + str(x+x_offset) + "," + str(y+y_offset) + ']; '

def printBorder(name1, name2, number_of_borders,sensNormal):
    if sensNormal == True: # name 1 vers name 2
        return "border c"+str(number_of_borders) +"(t=0,1){x=(1-t)*"+name1+"[0]+t*"+name2+"[0]; y=(1-t)*"+name1+"[1]+t*"+name2+"[1];}"
    else : # name 2 vers name 1
        return "border c"+str(number_of_borders) +"(t=0,1){x=(1-t)*"+name2+"[0]+t*"+name1+"[0]; y=(1-t)*"+name2+"[1]+t*"+name1+"[1];}"

def writeBorder(f,line, number_of_borders,comment=None):
    if comment !=None :
        f.write(line+comment+"\n")
    else :
        f.write(line+"\n")
    number_of_borders = number_of_borders+1
    return number_of_borders

def writeBordersOfPoint(f, number_of_borders,point, left, right, bottom, top,borders_coeff):

    if left == 0:
        borders_coeff[number_of_borders] = 6
        comment = "//Border id = 0 (b0) of point pt"+str(point)
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,0),printPoint4(point,1), number_of_borders,False),number_of_borders,comment)      
    if right == 0:
        borders_coeff[number_of_borders] = 6
        comment = "//Border id = 2 (b2) of point pt"+str(point)
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,2),printPoint4(point,3), number_of_borders,False),number_of_borders,comment)
    if bottom == 0:
        borders_coeff[number_of_borders] = 6
        comment = "//Border id = 3 (b3) of point pt"+str(point)
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,0),printPoint4(point,3), number_of_borders,True),number_of_borders,comment)
    if top == 0:
        borders_coeff[number_of_borders] = 6
        comment = "//Border id = 1 (b1) of point pt"+str(point)
        number_of_borders= writeBorder(f,printBorder(printPoint4(point,1),printPoint4(point,2), number_of_borders,False),number_of_borders,comment)
    return number_of_borders

def getCoeffOfLine(x1,y1,x2,y2):
    if x2 == x1:
        return None
    return (y2-y1)/(x2-x1)

def printPoint4(start, index): 
    return "pt"+str(start) +  'p' + str(index)

def whereIsPInRelationToO(A, B,m, left, right, bottom, top):
     #the original point 'O'
    xRow0A = A[0]
    yRow0A = A[1]

    #the point 'P' we want to know if this is on right, left, bottom or top
    xRow1B = B[0]
    yRow1B = B[1]

    aboveD1 = False
    aboveD2 = False

  
    """
    if yRow1B - ((m+1)*xRow1B + (yRow0A-((m+1)*xRow0A)))>=0: #line d1 : 
        aboveD1=True
    if yRow1B - ((m-1)*xRow1B + (yRow0A-((m-1)*xRow0A)))>=0: #line d2 : 
        aboveD2=True
    """
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

df = pd.read_csv(r'stcharles.csv', sep=';') # Points importation

dataCSV = pd.DataFrame(df, columns=['A', 'B']) # We only want A and B

f = open("freefem_code.txt", "w") # Creating/Opening file in writing mode

points_array={}
number_of_points = 0
number_of_edges = 0
edge_array={}

# points_array[coordinate][Edge ID for Points with coeff][Number of adjacent][Marqued]
# edge_array[Id Point 1][Id Point 2][Coeff]
points_array_temp ={}

# On met tous les sommets et tous les arretes dans un tableau
for index, row in dataCSV.iterrows() : # For every rows
    xyA=row['A'].split(',')

    xyA[0] = xyA[0][2:] 
    xyA[1] = xyA[1][3:]

    xyA[0] = xyA[0][:6] + '.' + xyA[0][6:]
    xyA[1] = xyA[1][:6] + '.' + xyA[1][6:]

    xyB=row['B'].split(',')

    xyB[0] = xyB[0][2:] 
    xyB[1] = xyB[1][3:]

    xyB[0] = xyB[0][:6] + '.' + xyB[0][6:]
    xyB[1] = xyB[1][:6] + '.' + xyB[1][6:]

    

    xyAFloat = [float(xyA[0]),float(xyA[1])]
    xyBFloat = [float(xyB[0]),float(xyB[1])]

    idA=-1
    idB=-1

    if not (row['A'] in points_array_temp) :
        points_array_temp[row['A']] = number_of_points
        points_array[number_of_points] = [xyAFloat, -1,0,False]
       
        number_of_points +=1
 
    if not (row['B'] in points_array_temp) :
        points_array_temp[row['B']] = number_of_points
        points_array[number_of_points] = [xyBFloat, -1,0,False]
        idB=number_of_points
        number_of_points +=1

    idA = points_array_temp[row['A']]
    idB = points_array_temp[row['B']]
    edge_array[number_of_edges] = [idA, idB, getCoeffOfLine(xyAFloat[0],xyAFloat[1],xyBFloat[0],xyBFloat[1])]
    number_of_edges +=1

del points_array_temp

# get number of adjacent
for x in edge_array :
    points_array[edge_array[x][0]][2]+=1
    points_array[edge_array[x][1]][2]+=1

string ="real [int] "
#Point def on string
y=0
print("Point: [x,y]")
for x in points_array :
    
    print("pt" + str(x) +": " + str(points_array[x][0]) )
    for i in range (0,4) :
        string +=printPoint4(x,i)  +"(2)"
        if len(points_array)-1 != y or i != 3 :
            string += ", "
    y = y +1

string += ";\n\n"
f.write(string)


# Calcul de la position des quatres points
for x in points_array :
    
    # equation : y=mx+p
    xA = points_array[x][0][0]
    yA = points_array[x][0][1]

    for i in edge_array :
        if edge_array[i][0] == x  or edge_array[i][1] == x :
            m = edge_array[i][2]
            points_array[x][1] = i # Edge Id 
            break
    
    if m == 0 or m == None: #si droite uniquement selon y ou uniquement selon x
        for i in range (0,4) :
            string =printPoint4(x,i) + " = " + str(posXandY(xA,yA,i))
            
            f.write(string) 

    else : 
        p=yA-(m*xA)
        
        #print(str(xA) + " " + str(yA) + " " + str(m) + " " + str(p)) #valeur de la droite passant par A et B

        mAP = -1/m # coeff de la droite perpendiculaire à la droite passant par A
        bAP = yA-mAP*xA #b de la droite perpendiculaire à la droite passant par A

        #print(xA)
        #print(yA)
        print("y=" + str(m) + "x+" + str(p)) #droite  passant par A et B

        #Coeficient directeur des droites y1, y2, y3 et y4
        aY1 = m
        aY2 = m
        aY3=  mAP
        aY4 = mAP

        #Trouver b2 de y1 et y2 selon m et p (b1 de la droite passant par 1 et B)
        b1 = p

        b2Y2 = b1 + offset*math.sqrt(m*m+1)
        b2Y1 = b1 - offset*math.sqrt(m*m+1)

        #print(b2Y2)
        #print(b2Y1)
        #Trouver b2 de y3 et y4 selon mAp et b (bAP) de la droite perpendiculairement à la droite passant par A et B
        b2Y3 = bAP + offset*math.sqrt(mAP*mAP+1)
        b2Y4 = bAP - offset*math.sqrt(mAP*mAP+1)

        #print(b2Y3)
        #print(b2Y4)

        bY1 = p+b2Y1
        bY2 =p+b2Y2
        bY3 = yA-mAP*xA+(b2Y3)
        bY4 = yA-mAP*xA+(b2Y4)
    
        print("y=" + str(m) + "x+" + str(bY1)) #droite  passant par A et B - le coeff y1
        print("y=" + str(m) + "x+" + str(bY2)) #droite  passant par A et B + le coeff y2
        #print("y=" + str(mAP) + "x+" + str(yA-mAP*xA)) #droite perpendiculaire passant par A
        print("y=" + str(mAP) + "x+" + str(bY3)) #droite perpendiculaire passant par A + coeff y3
        print("y=" + str(mAP) + "x+" + str(bY4)) #droite perpendiculaire passant par A - coeff y4

        xA={}
        yA={}

        # Premier point de A
        xA[0] = (bY3-bY1)/(aY1-aY3)
        yA[0] = aY1* xA[0]+bY1
        #print ("E = (" +str(x1A) +", " + str(y1A)+")")
        print(xA[0])
        print(yA[0])
        # Deuxieme point de A
        xA[1] = (bY3-bY2)/(aY2-aY3)
        yA[1] = aY2*xA[1]+bY2
        #print ("C = (" +str(x2A) +", " + str(y2A)+")")

        # Troisieme point de A
        xA[2] = (bY4-bY2)/(aY2-aY4)
        yA[2] = aY2*xA[2]+bY2
        #print ("D = (" +str(x3A) +", " + str(y3A)+")")

        # Quartrieme point de A
        xA[3] = (bY4-bY1)/(aY1-aY4)
        yA[3] = aY1*xA[3]+bY1
        #print ("D = (" +str(x4A) +", " + str(y4A)+")")

        #intervertir 2 et 1
        if m>0:
            tempx2 = xA[2]
            tempy2 = yA[2]
            xA[2] = xA[0]
            yA[2] = yA[0]
            xA[0] = tempx2
            yA[0] = tempy2

        for i in range (0,4) :
            string =printPoint4(x,i) + " = [" + str(xA[i]) + "," + str(yA[i]) + ']; '
            
            f.write(string)

string = "\n\n"
f.write(string)


number_of_borders = 0
borders_coeff ={}
#permet de mettre les bordures


for line in edge_array :
    
    if points_array[edge_array[line][0]][3] == False:
        points_array[edge_array[line][0]][3] = True
        left=right=bottom=top=0

        for line2  in edge_array :
            if line != line2 :
                if edge_array[line2][0] == edge_array[line][0] :
                    left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][0]][0],points_array[edge_array[line2][1]][0],edge_array[line][2],left,right,bottom,top)
                if edge_array[line2][1] == edge_array[line][0] :
                    left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][0]][0],points_array[edge_array[line2][0]][0],edge_array[line][2],left,right,bottom,top)
            else :#if same line
                left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][0]][0],points_array[edge_array[line2][1]][0],edge_array[line][2],left,right,bottom,top)
        #print(str(edge_array[line][0]) + " " +str(left) +" " + str(right) +" "+ str(bottom) +" "+ str(top))
        number_of_borders= writeBordersOfPoint(f, number_of_borders,edge_array[line][0], left, right, bottom, top,borders_coeff)
    
    if points_array[edge_array[line][1]][3] == False:
        points_array[edge_array[line][1]][3] = True
        left=right=bottom=top=0

        for line2  in edge_array :
            if line != line2 :
                if edge_array[line2][0] == edge_array[line][1] :
                    left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][1]][0],points_array[edge_array[line2][1]][0],edge_array[line][2],left,right,bottom,top)
                if edge_array[line2][1] == edge_array[line][1] :
                    left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][1]][0],points_array[edge_array[line2][0]][0],edge_array[line][2],left,right,bottom,top)
            else :#if same line
                left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][1]][0],points_array[edge_array[line2][0]][0],edge_array[line][2],left,right,bottom,top)
        #print(str(edge_array[line][1]) + " " +str(left) +" " + str(right) +" "+ str(bottom) +" "+ str(top))
        number_of_borders= writeBordersOfPoint(f, number_of_borders,edge_array[line][1], left, right, bottom, top,borders_coeff)

    #for border of the line
    left=right=bottom=top=0
    left, right, bottom, top = whereIsPInRelationToO(points_array[edge_array[line][0]][0],points_array[edge_array[line][1]][0],edge_array[line][2],left,right,bottom,top)
    
    if left == 1:
        borders_coeff[number_of_borders] = 60
        number_of_borders= writeBorder(f,printBorder(printPoint4(edge_array[line][0],1),printPoint4(edge_array[line][1],2), number_of_borders,True), number_of_borders)
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],0),printPoint4(edge_array[line][1],3), number_of_borders,False), number_of_borders)
    elif right == 1:
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],2),printPoint4(edge_array[line][1],1), number_of_borders,False), number_of_borders)
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],3),printPoint4(edge_array[line][1],0), number_of_borders,True), number_of_borders)
    elif top == 1:
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],1),printPoint4(edge_array[line][1],0), number_of_borders,False), number_of_borders)
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],2),printPoint4(edge_array[line][1],3), number_of_borders,True), number_of_borders)
    elif bottom == 1:
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],0),printPoint4(edge_array[line][1],1), number_of_borders,True), number_of_borders)
        borders_coeff[number_of_borders] = 60
        number_of_borders=writeBorder(f,printBorder(printPoint4(edge_array[line][0],3),printPoint4(edge_array[line][1],2), number_of_borders,False), number_of_borders)
    
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
    string+="c"+str(i)+"("+str(borders_coeff[i])+")"
    if i != number_of_borders-1: 
        string+="+"

string +=");"
string+="\nplot(Th, ps = \"mesh.eps\");"
f.write(string)

f.close()
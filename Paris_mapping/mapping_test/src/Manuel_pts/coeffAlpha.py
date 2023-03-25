#Code permettant d'avoir le coefficient directeur m2 d'une droite avec un angle 
#alpha par rapport à une autre droite avec coeff directeur m1

#https://www.nagwa.com/fr/explainers/407162748438/
from math import *
m1 = 0.5
alpha = 45

m2 = (m1 -tan(pi/4))/(tan(pi/4)*m1+1)
print(m2)
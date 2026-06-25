import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson #need for integration


nacaairfoil="2412"

angleofattack = 0.0873 # 0.0873 rad= 5 degrees (assumption)

nacalist = []
c = 1         #assumed chord length to be 1

#extracting the max camber, position of max camber, and thickness data from the given naca airfoil

for k in nacaairfoil:
    nacalist.append(k)

maxcamber = (int(nacalist[0]))*c/100
positionofmaxcamber = (int(nacalist[1]))*c/10

maxthicknesslist = nacalist[2] + nacalist[3]
maxthickness = (int(maxthicknesslist))*c/100



listofevenlyspacedX = np.linspace(0,c,100) #this line helps create 100 random points on the chord (x-axis) from the leading edge (0,0) to the trailing edge (1,0)

camberlist=[]
  
"""camber block of code"""

for i in listofevenlyspacedX:  
    
    if maxcamber == 0:
        
        camberlist.append(0)

    elif i <= positionofmaxcamber: #case for if the evenly spaced point on the chord between leading edge and position of max camber
        
        zc_leadingedgetomaxcamber = (maxcamber/(positionofmaxcamber**2)) * (((2*positionofmaxcamber) * (i/c)) - ((i/c)**2)) #known formula
        camberlist.append(zc_leadingedgetomaxcamber) #stores values of camber before position of max camber
        
        
    else: #case for if the evenly spaced point is between the position of max camber and the trailing edge
    
        zc_maxcambertotrailingedge = (maxcamber/((1-positionofmaxcamber)**2))* ((1-(2*positionofmaxcamber)) + ((2*positionofmaxcamber)*(i/c)) - ((i/c)**2)) #known formula
        camberlist.append(zc_maxcambertotrailingedge) #stores values of camber after position of max camber

plt.plot(listofevenlyspacedX, camberlist)
plt.xlabel("Position on chord")
plt.ylabel("Height of camber")
plt.show()

"""
what my code does till now is it picks 100 evenly spaced out points on the chord (x axis) (that goes from 0 (leading edge) to 1 (trailing edge)) 
and at each of those evenly spaced points it tries to calculate the camber. 
It checks if the point is less or more than the position of max camber and uses the appropriate formula. 
Then the program collects all these camber data and plots it against the points at which each camber was calculated #
"""


"""
thickness block of code (thickness in NACA airfoil is measured perpendicular from mean camber line to
the upper and lower surface
"""

thicknesslist=[]

for j in listofevenlyspacedX:
    
    zt = c*((5*maxthickness)*(0.2969*np.sqrt(j/c) - 0.1260*(j/c) - 0.3516*((j/c)**2) + 0.2843*((j/c)**3) - 0.1015*((j/c)**4)))    
    thicknesslist.append(zt)   
    
plt.plot(listofevenlyspacedX, thicknesslist)
plt.xlabel("Position on chord")
plt.ylabel("Half Thickness of the airfoil")
plt.show()

slopelist = []
    

"""
what the thickness loop does is loop through the same 100 evenly spaced points on the chord, 
and at each point, calculate the half-thickness, the perpendicular distance from the camber line out to one surface (upper or lower), 
using the empirical NACA thickness formula. One formula covers the whole chord, no if/else needed, since thickness doesn't have a geometric split like camber does. 
It then plots the points against their thickness values, that's the half-thickness, the real airfoil's full top-to-bottom thickness at any point is twice this value.
"""

    

"""
building the upper surface and the lower surface of airfoil by first getting the slope at each point
on the mean camber line by forward/backward/central finite differencing


we need to do this because our airfoil is curved and we need the thickness (distance between point on mean camber line and
its corresponding line on the curved upper/lower surface). We need to find theta, the angle between the slanted thickness line between
a random point on mean camber line and its corresponding pt on upper/lower surface and a straight line up from that same point
on the mean camber line up to the upper/lower surface

to get the angle at each point on the mean camber line we can simple do arctan of the slope found at that point
"""

for k in range(len(listofevenlyspacedX)): 
    
    if k==0: #checks for leading edge (can only do forward differencing here)
        slope = (camberlist[k+1] - camberlist[k]) / (listofevenlyspacedX[k+1] - listofevenlyspacedX[k])
        slopelist.append(slope)
    
    elif k == len(listofevenlyspacedX)-1: #checks for trailing edge (can only do backward differencing here)
        slope = (camberlist[k] - camberlist[k-1]) / (listofevenlyspacedX[k] - listofevenlyspacedX[k-1])
        slopelist.append(slope)
        
    else: #otherwise normally between leading and trailing edge we can use central differencing
        slope = (camberlist[k+1] - camberlist[k-1]) / (listofevenlyspacedX[k+1] - listofevenlyspacedX[k-1])
        slopelist.append(slope)

"""
theta block of code
"""

thetalist=[]

for m in slopelist:
    theta = np.atan(m)
    thetalist.append(theta)

xulist = []
zulist = []

xllist = []
zllist = []


for k in range(len(listofevenlyspacedX)):

    xu = listofevenlyspacedX[k] - thicknesslist[k]*np.sin(thetalist[k]) #basically xu = x - zsintheta
    zu = camberlist[k] + thicknesslist[k]*np.cos(thetalist[k]) #basically zu = x - 

    xulist.append(xu)
    zulist.append(zu)

    xl = listofevenlyspacedX[k] + thicknesslist[k]*np.sin(thetalist[k])
    zl = camberlist[k] - thicknesslist[k]*np.cos(thetalist[k])

    xllist.append(xl)
    zllist.append(zl)   
    
"""
for every point on the mean camber line, the thickness connecting the x point to its corresponding point on the upper and the lower
surfaces 
"""

plt.plot(xulist, zulist)
plt.plot(xllist, zllist)
plt.axis('equal')
plt.xlabel("X coordinates")
plt.ylabel("Z coordinates")
plt.show()

# everything till here builds the airfoil structure

"""
code from here is for calculating Cl using fourier coefficients A0, A1,...An
and for doing this we need stuff in terms of theta
"""


thetaarray = np.linspace(0, np.pi, 100) #creates 100 angles from 0 to pi 

xconvertedtotheta = (c/2) * (1-np.cos(thetaarray)) #converts those 100 angles to x values


"""
cannot use the same lists as before because they were for a different set of x points and the thetaarray and
xconvertedtotheta list has different x values and angle values

height of camber (zc) stays the same whether x is channged to theta or kept as x
"""


zc_forthetalist=[]

for m in xconvertedtotheta:
      
    if maxcamber==0:
        zc_forthetalist.append(0)
    
    elif m<=positionofmaxcamber:
        zc_fortheta = (maxcamber/(positionofmaxcamber**2)) * (((2*positionofmaxcamber) * (m/c)) - ((m/c)**2))
        zc_forthetalist.append(zc_fortheta)
        
    else:
        zc_fortheta = (maxcamber/((1-positionofmaxcamber)**2))* ((1-(2*positionofmaxcamber)) + ((2*positionofmaxcamber)*(m/c)) - ((m/c)**2))
        zc_forthetalist.append(zc_fortheta)
        
plt.plot(xconvertedtotheta, zc_forthetalist)
plt.xlabel("Chord position (X coordinate) converted to theta")
plt.ylabel("Height of camber")
plt.show()



slopelistfromtheta = []

for k in range(len(xconvertedtotheta)):
    
    if k == 0:
        slope = (zc_forthetalist[k+1] - zc_forthetalist[k]) / (xconvertedtotheta[k+1] - xconvertedtotheta[k])
        slopelistfromtheta.append(slope)
        
    elif k == len(xconvertedtotheta)-1:
        slope = (zc_forthetalist[k] - zc_forthetalist[k-1]) / (xconvertedtotheta[k] - xconvertedtotheta[k-1])
        slopelistfromtheta.append(slope)
        
    else:
        slope = (zc_forthetalist[k+1] - zc_forthetalist[k-1]) / (xconvertedtotheta[k+1] - xconvertedtotheta[k-1])
        slopelistfromtheta.append(slope)

"""
computation of Cl

integration is done using the simpson package

for finding Cl and Cm,c/4 we need A0, A1, and A2

the general formula is An = 2/pi * integral of dz/dx * cos(n theta)*dtheta   from 0 to pi

and A0 = alpha - (1/pi) * integral of dz/dx * dtheta from 0 to pi

dz/dx will be slopelistfromtheta and dtheta will be thetaarray

since thetaarray is already defined to be from 0 to pi, we dont have to worry about the bounds of the integrals 
"""


integral1 = simpson(slopelistfromtheta, thetaarray) #used for A0 

integral2 = simpson((slopelistfromtheta * np.cos(thetaarray) ) , thetaarray) #used for A1

integral3 = simpson((slopelistfromtheta * np.cos(2 * thetaarray) ) , thetaarray) #used for A2

integral4 = simpson((slopelistfromtheta*(np.cos(thetaarray) - 1)) , thetaarray) #used for alpha L=0

A0 = angleofattack - (1/np.pi)*integral1

A1 = (2/np.pi)*integral2

A2 = (2/np.pi)*integral3    
    
"""
Cl = pi * (2*A0 + A1)

Cm,c/4 = pi/4 * (A2 - A1)

to find alphaL=0 you just rearrange the Cl equation and set Cl=0 in it or you can do alphaL=0 = -1/pi * integral of dz/dx * (costheta - 1) from 0 to pi
"""

Cl = (np.pi* ((2*A0) + A1))

Cmcby4 = ((np.pi)/4) * (A2 - A1)

alphaLequals0 = (-1/np.pi) * integral4

print("The lift coefficient = ",Cl)
print("The moment coefficient about the quarter chord point = ",Cmcby4)
print("The zero lift angle of attack = ",alphaLequals0)
     

"""
code below is for calculating delta Cp (pressure distrubution coefficient)

the fourier formula for delta Cp is:
    
delta Cp = 4[A0*(1+costheta)/sintheta + sum of An*sin(n*theta) where n starts from 1 to inf]

we go upto n=2 only because that is sufficient and accurate enough

HOWEVER: we need a new thetaarray because our older one goes from 0 to pi (both included)
and 0 and pi cause delta Cp to go to infinity

So to counter that we define a brand new thetaarray that goes from 0+epsilon to pi-epsilon

a new thetarray will have all changed values than the older thetaarray and that's fine because 
we're calculating delta Cp now which is a whole new thing

we don't have to recalculate A0, A1, and A2 on the new thetaarray cz the answer would almost
be the same as the original one and thus will give a very small error that can be neglected
"""

newthetaarray = np.linspace(0+0.0001 , np.pi - 0.0001, 100)

deltacplist = []

for q in newthetaarray:
    
    deltacp = 4*((A0*(1+np.cos(q))/np.sin(q)) + (A1*np.sin(q)) + (A2*np.sin(2*q)))
    deltacplist.append(deltacp)

plt.plot(newthetaarray, deltacplist)
plt.yscale('log') #used log scale because otherwise it would just show a big spike at theta=0 and then flat line
plt.xlabel("Theta")
plt.ylabel("Delta Cp on the log scale")
plt.show()


"""
following part of code is for getting a dat list with coordinates (x,z) of our airfoil surface (both upper and lower surfaces)
we need to reverse the xulist, zulist, xllist, and zllist because we want the coordinates to go from trailing edge to leading edge

We have to reverse this because almost every airfoil database baked into XFOIL starts from trailing
edge, so we might as well do the same to avoid any crashes or errors
"""

reversedxulist = list(reversed(xulist))
reversedzulist = list(reversed(zulist))



#opening/creating and writing the reversed lists into a dat file using python code

file = open("MyAirfoilCoordinates.dat", "w")

file.write("My Airfoil Coordinates\n")

for g in range(len(reversedxulist)):
    file.write(str(reversedxulist[g]) + " " + str(reversedzulist[g]) + "\n")

for g in range(len(xllist)):
    file.write(str(xllist[g]) + " " + str(zllist[g]) + "\n")

file.close()





    
  


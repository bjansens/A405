import site
import matplotlib.pyplot as plt
import numpy as np
from a405thermo.constants import constants as c
from a405thermo.thermlib import convertTempToSkew, find_theta
from a405skewT.makeSkewII import makeSkewWet


#Carnot heat engine:
#
#dry adiabatic expansion from B to C 
#isothermal compression from C to D (heat flow, Qout,  out of the system)
#dry adiabatic compression from D to C
#note that Qin > Qout so that work done by the system in the carnot cycle = Qin - Qout > 0

pressA=1.e5
tempA=15 + c.Tc
pressC=0.7e5
tempC=5 + c.Tc;
thetaA=find_theta(tempA,pressA)
thetaC=find_theta(tempC,pressC)
thetaB=thetaC
tempB=tempA
term1=(thetaB/tempB)**(c.cpd/c.Rd)
term1=1./term1
pressB=term1*1.e5
tempD=tempC
thetaD=thetaA
term1=(thetaD/tempD)**(c.cpd/c.Rd)
term1=1./term1
pressD=term1*1.e5

plt.close('all')
fig,ax = plt.subplots(1,1)
corners =  [5,30]
ax, skew = makeSkewWet(ax,corners=corners)

xtempA=convertTempToSkew(tempA - c.Tc,pressA*0.01,skew)
xtempB=convertTempToSkew(tempB - c.Tc,pressB*0.01,skew)
xtempC=convertTempToSkew(tempC - c.Tc,pressC*0.01,skew)
xtempD=convertTempToSkew(tempD - c.Tc,pressD*0.01,skew)

ax.text(xtempA,pressA*0.01,'A', fontweight='bold',fontsize= 22, color='b')
ax.text(xtempB,pressB*0.01,'B', fontweight='bold',fontsize= 22,color='b')
ax.text(xtempC,pressC*0.01,'C', fontweight='bold',fontsize= 22,color='b')
ax.text(xtempD,pressD*0.01,'D', fontweight='bold',fontsize= 22, color='b')

xmin = convertTempToSkew(corners[0],pressA*0.01,skew)
xmax = convertTempToSkew(corners[1],pressA*0.01,skew)
ax.axis([xmin, xmax, 1000, 600])
ax.set_title('forward carnot cycle')
plt.show()

#print -dpdf forward_carnot.pdf
#print -dpng -r200 forward_carnot.png

#Carnot refrigerator:

#adiabatic expansion from A to B 
#isothermal expansion from B to C (heat flow in, Qin, to system)
#adiabatic compression from C to D )
#isothermal compression from D to A  heat flow out, Qout, of system)
#note that Qout > Qin so that work done by the system in the carnot cycle = Qin - Qout < 0
#(i.e. work is done on the system)

thetaB=thetaA
tempB=tempC
term1=(thetaB/tempB)**(c.cpd/c.Rd)
term1=1./term1
pressB=term1*1.e5
tempD=tempA
thetaD=thetaC
term1=(thetaD/tempD)**(c.cpd/c.Rd)
term1=1./term1
pressD=term1*1.e5

fig, ax = plt.subplots(1,1)

ax, skew = makeSkewWet(ax,corners = corners)


xtempA=convertTempToSkew(tempA - c.Tc,pressA*0.01,skew)
xtempB=convertTempToSkew(tempB - c.Tc,pressB*0.01,skew)
xtempC=convertTempToSkew(tempC - c.Tc,pressC*0.01,skew)
xtempD=convertTempToSkew(tempD - c.Tc,pressD*0.01,skew)

ax.text(xtempA,pressA*0.01,'A', fontweight='bold',fontsize= 22, color='b')
ax.text(xtempB,pressB*0.01,'B', fontweight='bold',fontsize= 22,color='b')
ax.text(xtempC,pressC*0.01,'C', fontweight='bold',fontsize= 22,color='b')
ax.text(xtempD,pressD*0.01,'D', fontweight='bold',fontsize= 22, color='b')

xmin = convertTempToSkew(corners[0],pressA*0.01,skew)
xmax = convertTempToSkew(corners[1],pressA*0.01,skew)
ax.axis([xmin, xmax, 1000, 600])
ax.set_title('backward carnot cycle')
plt.show()

#print -dpdf backward_carnot.pdf
#print -dpng -r200 backward_carnot.png
#print -depsc  backward_carnot_clip.eps


#Calculate the heat input and output

#exact change in entropy
deltaS=c.cpd*(np.log(thetaC) - np.log(thetaB));
#approx change in entropy
deltaSapprox=c.cpd*(thetaC - thetaB)/thetaC;
#heat input inside the house
qin=tempB*deltaS;
#heat exausted outside the house
qout=tempA*deltaS;
work_done=qin - qout;


out_mesg='\nHeat absorbed during expansion (qin) = %8.3f (J/kg)\n\
Heat expelled during compression (qout) = %8.3f (J/kg)\n\
Work required to complete the cycle (work_done) = %8.3f (J/kg)\n\
(this is also the net energy removed from the room)\n'

print(out_mesg %(qin, qout, work_done))

#check this using enthalpy per the carnot_refrigerator notes

qin_h= c.cpd*(tempC - tempB) - c.Rd*tempB*(np.log(pressC) - np.log(pressB))
qout_h= c.cpd*(tempD - tempA) - c.Rd*tempD*(np.log(pressD) - np.log(pressA))

out_mesg='\nEnthalpy check: heat absorbed during expansion (qin) = %8.3f (J/kg)\n\
Enthalpy check: Heat expelled during compression (qout) = %8.3f (J/kg)\n'

print(out_mesg %(qin, qout))

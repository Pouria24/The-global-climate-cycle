
# In[111]:


# Put your code here
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
import pandas as pd
import numpy as np
import math
get_ipython().run_line_magic('matplotlib', 'inline')
glb = pd.read_csv("GLB.Ts.csv")
co2 = np.loadtxt("co2_mm_mlo.txt", skiprows =72)
glb=glb[['Year','J-D']]
glb=glb[glb['Year']>=1960]
glb['J-D']=glb[['J-D']]/100+14.3
co2 = pd.DataFrame(co2)
co2= co2[[2,4]]

co2=co2.rename(columns={2:"Decimal Date",4:"Interpolated"})
co2=co2[co2['Decimal Date']>=1960]
tempreture= co2['Interpolated']
initialT=tempreture.iloc[0]
p=[]
for i in co2['Interpolated']:
    p.append(14.3+3*np.log2(i/initialT))
plt.plot(glb['Year'],glb['J-D'],label='Air Tempreture')
plt.plot(co2['Decimal Date'],p,label='CO2 concentration')
plt.ylabel('Tempreture')
plt.xlabel('Time')
plt.title('Air Tempreture - CO2 concentration')
plt.legend()
print('3 was good')


# ---
# ## Step 2: Make predictions for the future
# 
# Now, let's go back to our original "very, very simple model" and modify it to make it more sophsticated, and to make some predictions for the future. Consider the following scenarios, and predict global temperature from the current 2000 until the year 2100. **As you did in the pre-class assignment, start with a CO$_2$ concentration of 368 parts per million (ppm) and an average global temperature of 15° C (59° F).**
# 
# 1.  **Baseline model:** A constant 9 gigatons of carbon per year is put into the atmosphere by humans (this is the model you implemented in your pre-class assignment)
# 2.  **Growth model:** The amount of carbon put into the atmosphere actually grows: starting at 7 gigatons/year in 2000, and increasing by 0.1 gigatons/year for every additional year thereafter (to represent increased reliance on fossil fuels).
# 3.  **"Get it under control" model:** The amount of carbon put into the atmosphere starts at 7 gigatons/year in 2000, increases by 0.1 gigatons/year until 2020, and then decreases by 0.1 gigatons/year until 2100.
# 4.  **"Carbon sequestration" model:** The amount of carbon put into the atmosphere starts at 7 gigatons/year in 2000, increases by 0.1 gigatons/year until 2020, and then decreases by 0.5 gigatons/year until it reaches -5 gigatons/year (indicating that we have developed some means of "sequestering" carbon -- in other words, removing it from the atmosphere.
# 5.  **Your own scenario:** Given your thoughts about climate change and humanity's ability to reduce CO$_2$ emission, devise your own scenario!
# 
# Make plots of the global CO$_2$ concentration, average global temperature, and the rate of human carbon emission each year for each of these scenarios, plotted on the same subplot.  Create a key for the plots so we can tell which lines correspond to which scenario!
# 
# Also, in what scenarios do we avoid increasing global temperatues by no more than 2° C from the current temperature?  Experts consider that to be the global temperature increase that will have [catastrophic climate consequences](http://www.pbs.org/newshour/bb/why-2-degrees-celsius-is-climate-changes-magic-number/), and thus is a critical target for climate models.
# 

# In[114]:


# Put your code here
x=[]
co2=[]
t=[]
co2_i = 9
co2_rn= 368
for i in range (100):
    x.append(2000+i)
    co2.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t.append(T)
    co2_rn = co2_rn +co2_i/2.3
co2_gr=[]
t_gr=[]
co2_i=7
co2_rn= 368
for i in range (100):
    co2_gr.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t_gr.append(T)
    co2_rn = co2_rn +co2_i/2.3
    co2_i=co2_i+0.1

co2_co=[]
t_co=[]
co2_i=7
co2_rn= 368
for i in range (100):
    co2_co.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t_co.append(T)
    co2_rn = co2_rn +co2_i/2.3
    if (i<=20):
        co2_i=co2_i+0.1
    else:
        co2_i=co2_i-0.1
co2_s=[]
t_s=[]
for i in range (100):
    co2_s.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t_s.append(T)
    co2_rn = co2_rn +co2_i/2.3
    if (i<=20):
        co2_i=co2_i+0.1
    elif(i>20 and co2_i>-5):
        co2_i=co2_i-0.5
    else:
        co2_i=co2_i
co2_a=[]
t_a=[]
for i in range(100):
    co2_a.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t_a.append(T)
    co2_rn = co2_rn +co2_i/2.3
    if (i<=30):
        co2_i=co2_i+0.7
    else:
        co2_i=co2_i-0.1
plt. figure(figsize=(10,20))
plt.subplot(5,1,1)
plt.plot(x,t,color='green')
plt.ylabel('Tempreture')
plt.xlabel('Time')
plt.title('Tempreture-Baseline')
plt.subplot(5,1,2)
plt.plot(x,t_gr,color='orange')
plt.ylabel('Tempreture')
plt.xlabel('Time')
plt.title('Tempreture-Growth')
plt.subplot(5,1,3)
plt.plot(x,t_co,color='red')
plt.ylabel('Tempreture')
plt.xlabel('Time')
plt.title('Tempreture-Get it under control')
plt.subplot(5,1,4)
plt.plot(x,t_s,color='purple')
plt.ylabel('Tempreture')
plt.xlabel('Time')
plt.title('Tempreture-Carbon sequestration')
plt.subplot(5,1,5)
plt.plot(x,t_a,color='yellow')
plt.ylabel('Tempreture')
plt.xlabel('Time')
plt.title('Tempreture-My own scenario')
plt.tight_layout()


# ## Step 3:  How does this impact sea level?
# 
# One major concern with regards to climate change is that global warming will cause a rise in [sea level](https://climate.nasa.gov/vital-signs/sea-level/), which comes from both melting glaciers and ice caps and from the expansion of water as it warms.  This will have significant consequences for ecosystems and also for humans - most of the Earth's population lives close to the ocean, and increased sea level will increase the dangers from flooding and the impact of hurricanes and cyclones, and will displace huge numbers of people in low-lying countries from their homes.
# 
# A recent paper by [Levermann et al. (2013, PNRAS, 110, 13745)](http://www.pik-potsdam.de/~anders/publications/levermann_clark13.pdf) shows calculations that estimate this effect.  Their best prediction is that, over long time scales, the sea level rise will be approximately 2.3 meters per °C of temperature increase beyond the current value, although this is substantially uncertain (by roughly a factor of two in either direction).  They also caution that this is the **long-term outcome**, with sea level rise trailing the increase in atmospheric CO$_2$ concentration by some time because it will take some time for the oceans to warm up and the Antarctic ice sheet to melt.
# 
# Using the Levermann data, make three estimates per model from Step 2: an "optimistic" model assuming 1 meter of sea level rise per °C of temperature increase beyond the present, a "realistic" model assuming 2 meters of rise per °C of temperature increase, and a "pessimistic" model assuming 4 meters of rise per °C of temperature increase.  Given [this graph of human population distribution by altitude](http://www.radicalcartography.net/index.html?howhigh), how much of the Earth's population might be affected by each of these models?

# In[116]:


# Put your code here
plt. figure(figsize=(7,30))

change11=[]
change12=[]
change13=[]
change21=[]
change22=[]
change23=[]
change31=[]
change32=[]
change33=[]
change41=[]
change42=[]
change43=[]
change51=[]
change52=[]
change53=[]
for i in t:
    change11.append((i-15)*1)
for i in t:
    change12.append((i-15)*2)
for i in t:
    change13.append((i-15)*4)
for i in t_gr:
    change21.append((i-15)*1)
for i in t_gr:
    change22.append((i-15)*2)
for i in t_gr:
    change23.append((i-15)*4)
for i in t_co:
    change31.append((i-15)*1)
for i in t_co:
    change32.append((i-15)*2)
for i in t_co:
    change33.append((i-15)*4)
for i in t_s:
    change41.append((i-15)*1)
for i in t_s:
    change42.append((i-15)*2)
for i in t_s:
    change43.append((i-15)*4)
for i in t_a:
    change51.append((i-15)*1)
for i in t_a:
    change52.append((i-15)*2)
for i in t_a:
    change53.append((i-15)*4)
plt.subplot(15,1,1)
plt.plot(x,change11,color='green')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Baseline')
plt.subplot(15,1,2)
plt.plot(x,change12,color='green')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Baseline')
plt.subplot(15,1,3)
plt.plot(x,change13,color='green')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Baseline')
plt.subplot(15,1,4)
plt.plot(x,change21,color='orange')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Growth')
plt.subplot(15,1,5)
plt.plot(x,change22,color='orange')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Growth')
plt.subplot(15,1,6)
plt.plot(x,change23,color='orange')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Growth')
plt.subplot(15,1,7)
plt.plot(x,change31,color='red')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Get it under control')
plt.subplot(15,1,8)
plt.plot(x,change32,color='red')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Get it under control')
plt.subplot(15,1,9)
plt.plot(x,change33,color='red')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Get it under control')
plt.subplot(15,1,10)
plt.plot(x,change41,color='purple')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Carbon sequestration')
plt.subplot(15,1,11)
plt.plot(x,change42,color='purple')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Carbon sequestration')
plt.subplot(15,1,12)
plt.plot(x,change43,color='purple')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-Carbon sequestration')
plt.subplot(15,1,13)
plt.plot(x,change51,color='yellow')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-My own scenario')
plt.subplot(15,1,14)
plt.plot(x,change52,color='yellow')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-My own scenario')
plt.subplot(15,1,15)
plt.plot(x,change53,color='yellow')
plt.ylabel('Sea Level(meter)')
plt.xlabel('Time')
plt.title('Sea Level-My own scenario')
plt.tight_layout()



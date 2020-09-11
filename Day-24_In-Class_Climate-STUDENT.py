#!/usr/bin/env python
# coding: utf-8

# ### <p style="text-align: right;"> &#9989; Pouria Khoushehchin.</p>
# 
# #### <p style="text-align: right;"> &#9989; Put your group member names here.</p>

# # Day 24 - The global climate cycle
# <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Carbon_cycle-cute_diagram.jpeg/500px-Carbon_cycle-cute_diagram.jpeg" width=400px>
# 
# ## Goals for today's in-class assignment
# 
# * Use the data on the global carbon cycle to create a [compartment model](https://en.wikipedia.org/wiki/Multi-compartment_model), and to make predictions about global climate change under a variety of circumstances
# 
# ## Assignment instructions
# 
# Work with your group to complete this assignment. Instructions for submitting this assignment are at the end of the notebook. The assignment is due at the end of class.  If you haven't completed all sections of the assignment, you still need to upload something!
# 
# **In today's class**, we are going to implement a [compartment model](https://en.wikipedia.org/wiki/Multi-compartment_model) describing the global carbon cycle using the data that you collected as part of the pre-class assignment, explicitly connect it to the models that you created in the last class, and to make predictions about global climate change.

# ---
# ### Step 1 - Developing a model with your group
# 
# **Before we do anything else,** spend some time discussing the pre-class assignment with your group.  In particular, ensure that you agree on all of the carbon reservoirs and fluxes.  Then, **come up with a compartment model on the whiteboard that implements**:
# 
# 1. the simplest possible model to show how the carbon reservoirs and fluxes change with time, which tracks just the major carbon reservoirs and *natural* fluxes
# 2. one that includes [anthropogenic](https://www.merriam-webster.com/dictionary/anthropogenic) (i.e., human-caused) fluxes of carbon (which should be an extension of the first model), with a function that controls the flux of human-generated carbon over time.
# 
# Think about how you will initialize the simulation, how you will evolve it in time, and how you will stop it.  Also, make sure to think about how you will keep track of the amount of carbon in each reservoir!
# 
# **Note:** This is meant to be a set of simple update equations, and should *not* be solved using odeint (you don't have quite enough information to create a model that is solvable in that manner).  As an example, if you had two carbon reservoirs, R$_A$ and R$_B$, and a flux F$_{A \rightarrow B}$ showing the amount of carbon per year that goes from reservoir A to reservoir B, the update equations would be:
# 
# $$ R_{A}^{N+1} = R_{A}^{N} - F_{A \rightarrow B} \Delta t $$
# 
# $$ R_{B}^{N+1} = R_{B}^{N} + F_{A \rightarrow B} \Delta t $$
# 
# with the times N and N+1 being separated by an amount of time $\Delta t$, and the changed signs in the flux indicating that if reservoir A gets larger, B must get smaller (and vice versa).
# 
# **Before you move forward with implementation, talk to one of the instructors to make sure you're on the right track!**

# ***Make notes about your model here!***
# Atmosphere: exchange with the ocean, exchange with the biosphere
# Oceans:exchange with atmosphere
# Earth's crust: removal to atmosphere
# biosphere: exchange with atmosphere

# ---
# ### Step 2 - Implementing the model
# 
# Now, implement your second model and, most importantly, **test it!**
# 
# **First**, run it with the anthropogenic carbon flux set to zero - do the reservoirs evolve in the way you would expect based on your model? Do they stay at constant values? What would it take for this to be true? If they don't stay constant, do they increase/decrease in a way that is consistent with your model?
# 
# **Then**, if you set the human-generated carbon flux at 9 gigatons of carbon per year entering the atmosphere, does the amount of carbon increase in a way that is consistent with your modeling from the last class?  (Make sure to check your units to ensure that you convert from gigatons of carbon to parts per million of CO$_2$!)
# 
# As a reminder, you can find flux between all of the pools/reservoirs [here](http://globecarboncycle.unh.edu/CarbonPoolsFluxes.shtml).

# In[30]:


# Put your code here
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
import pandas as pd
import numpy as np
import math
from scipy.integrate import odeint
get_ipython().run_line_magic('matplotlib', 'inline')
def imple(y0,t,a,b,c,d,e):
    atmosphere = y0[0]
    ocean = y0[1]
    crust = y0[2]
    biosphere = y0[3]
    dadt = atmosphere+b*crust+c*ocean-d*atmosphere+e*biosphere-f*biosphere
    dodt = ocean-c*ocean+d*atmosphere
    dcdt = crust-b*crust
    dbdt = biosphere- e*biosphere+f*biosphere
    
    return [dadt,dodt,dcdt,dbdt]
b= 100000000/9.3
c= 0.1
d= 0.2
e= 0.4
f= 0.1

time=np.linspace(0,50,1000)
initial_conditions=[750,38000,100000000,1500]
result = odeint(imple, initial_conditions, time, args=(b,c,d,e,f))
atmos= result[:,0]
ocean=result[:,1]
earth=result[:,2]
bios=result[:,3]
plt.subplot(4,1,1)
plt.plot(time,atmos)
plt.subplot(4,1,2)
plt.plot(time,ocean)
plt.subplot(4,1,3)
plt.plot(time,earth)
plt.subplot(4,1,4)
plt.plot(time,bios)


# ---
# ### Step 3 - Making some predictions about CO$_2$ and temperature
# 
# Next, connect your model of the carbon cycle to the simple model that you made in the last class, which relates the atmospheric carbon dioxide concentration to global temperature.  Consider a few scenarios, and show how the various carbon reservoirs and the global mean temperature evolve over time, starting in the year 2000 with 
# an atmospheric CO$_2$ concentration of 368 parts per million (ppm), an average global temperature was 15° C, and the climate sensitivity factor, S, that you estimated from data in the last class.  The scenarios that we will consider will evolve until the year 2100.  Use the following models:
# 
# 1.  **Baseline model:** A constant 9 gigatons of carbon per year is put into the atmosphere by humans
# 2.  **Growth model:** The amount of carbon put into the atmosphere actually grows: starting at 7 gigatons/year in 2000, and increasing by 0.1 gigatons/year for every additional year thereafter (to represent increased reliance on fossil fuels).
# 3.  **"Get it under control" model:** The amount of carbon put into the atmosphere starts at 7 gigatons/year in 2000, increases by 0.1 gigatons/year until 2020, and then decreases by 0.1 gigatons/year until 2100.
# 4.  **"Carbon sequestration" model:** The amount of carbon put into the atmosphere starts at 7 gigatons/year in 2000, increases by 0.1 gigatons/year until 2020, and then decreases by 0.5 gigatons/year until it reaches -5 gigatons/year (indicatin that we have developed some means of "sequestering" carbon -- in other words, removing it from the atmosphere.
# 
# Make plots of the global atmospheric CO$_2$ concentration, average global atmospheric temperature, and mass of carbon in each reservoir for each of these scenarios, plotted on the same subplot.  Create a key for the plots so we can tell which lines correspond to which scenario!

# In[34]:


# Put your code here
x=[]
co2=[]
t=[]
co2_i = 9
co2_rn= atmos[50]
for i in range (100):
    x.append(2000+i)
    co2.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t.append(T)
    co2_rn = co2_rn +co2_i/2.3
co2_gr=[]
t_gr=[]
co2_i=7
co2_rn= atmos[50]
for i in range (100):
    co2_gr.append(co2_rn)
    T = 15+3*np.log2(co2_rn/368)
    t_gr.append(T)
    co2_rn = co2_rn +co2_i/2.3
    co2_i=co2_i+0.1

co2_co=[]
t_co=[]
co2_i=7
co2_rn= atmos[50]
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


# ---
# ### Step 4 - Making a more sophisticated model
# 
# If you have time, make a more sophisticated climate model, thinking back to the [Wikipedia article on the carbon cycle](https://en.wikipedia.org/wiki/Carbon_cycle) and the [Wikipedia page on carbon sequestration](https://en.wikipedia.org/wiki/Carbon_sequestration).  What additional reservoirs might you include?  How might you create a more sophisticated or accurate representation of each reservoir or carbon flux?  (For example, do any of the carbon fluxes depend on the amount of carbon dioxide in a given carbon reservoir?)  You may want to just think this through, but not write any code - that's just fine, but make some notes in the space provided below, if that's what you choose to do!
# 

# In[ ]:


# Put code here
#We can have actual numbers and rates and more components.


# *Put your general thoughts/ideas here*

# ---

# ## Congratulations, you're done!
# 
# Submit this assignment by uploading your notebook to the course Desire2Learn web page.  Go to the "In-Class Assignments" folder, find the appropriate submission link, and upload everything there. Make sure your name is on it!

# &#169; Copyright 2018,  Michigan State University Board of Trustees

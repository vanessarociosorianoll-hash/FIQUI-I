#Papel milimetrado como cuadricula
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#usamos ax para referirnos al grafico en general, espacio de dihujo
#al usar ax.xaxis , podria ser enfocarse en x
#mientras que ax.yaxis , para solo y
#ax.spines , para los bordes del cuadro
fig, ax=plt.subplots()
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.grid(which='major', color="#2761AB", linestyle='-', linewidth=0.8, alpha=0.5)
ax.grid(which="minor",color="#2761AB",linestyle="-",linewidth=0.4,alpha=0.5)
ax.set_xlim(0,5)
ax.set_ylim(0,5)
plt.show()
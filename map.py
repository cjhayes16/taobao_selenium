import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
from matplotlib.colors import rgb2hex
plt.figure(figsize=(16,8))
m= Basemap(llcrnrlon=73, llcrnrlat=18, urcrnrlon=135, urcrnrlat=53)


m.drawcoastlines()

m.drawcountries(linewidth=1.5)

m= Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=100)
m.readshapefile('C:/Users/hp/Downloads/gadm36_CHN_shp/gadm36_CHN_1', 'states',drawbounds=True)
m.readshapefile('C:/Users/hp/Downloads/gadm36_TWN_shp/gadm36_TWN_1', 'taiwan', drawbounds=True)
df = pd.read_excel('H:/pro_sales.xls')
df.set_index('province',inplace=True)
statenames=[]
colors={}
cmap = plt.cm.PuBu
# 然后我们把每个省的数据映射到colormap上：
vmax = 1000
vmin= 300
for shapedict in m.states_info:
    statename=shapedict['NL_NAME_1']
    p=statename.split('|')
    if len(p)>1:
        s=p[1]
    else:
        s=p[0]
    s=s[:2]
    if s == '黑龍':
        s = '黑龙江'
    if s == '内蒙':
        s = '内蒙古'
    statenames.append(s)
    if df['sales'][s]:
        pop= df['sales'][s]
    else:
        POP=0
    colors[s] = cmap(np.sqrt((pop - vmin) / (vmax - vmin)))[:3]

# 最后，我们把各个省的颜色描在地图上：
ax = plt.gca()

for nshape, seg in enumerate(m.states):
    color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)
for nshape, seg in enumerate(m.taiwan):
    color = rgb2hex(colors[statenames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)

plt.show()
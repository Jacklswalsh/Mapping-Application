import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import pandas as pd
import math
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def main():
    stamen_terrain = cimgt.Stamen('terrain-background')
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([2.3, -11.5, 49.2, 60], crs=ccrs.Geodetic())
    ax.add_image(stamen_terrain, 6)
    city_list = pd.read_csv('gb.csv')
    #print(city_list)

    latlonshigh = {}
    latlonslow = {}
    City_Pop = {}
    for i, v in city_list.iterrows():
        if city_list.iloc[i, 8] > 600000:
            City_Pop[city_list.iloc[i, 0]] = city_list.iloc[i, 8]
            city = city_list.iloc[i, 0]
            long, lat = city_list.iloc[i, 1], city_list.iloc[i, 2]
            latlonshigh[city] = (long, lat)
        elif 600000 > city_list.iloc[i, 8] > 400000:
            city = city_list.iloc[i, 0]
            long, lat = city_list.iloc[i, 1], city_list.iloc[i, 2]
            latlonslow[city] = (long, lat)

    for key in latlonshigh:
        ax.plot(latlonshigh[key][1], latlonshigh[key][0], marker='.', color='k', markersize=5,
                        alpha=1, transform=ccrs.Geodetic())
        geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
        text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
        ax.text(latlonshigh[key][1], latlonshigh[key][0], u"{}".format(key),
                verticalalignment='center', horizontalalignment='right',
                transform=text_transform,
                fontsize = 6,
                bbox=dict(facecolor='sandybrown', alpha=0.6, boxstyle='round'))

    for key in latlonslow:
        ax.plot(latlonslow[key][1], latlonslow[key][0], marker='.', color='k', markersize=2,
                        alpha=1, transform=ccrs.Geodetic())
        geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
        text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
        ax.text(latlonslow[key][1], latlonslow[key][0], u"{}".format(key),
                verticalalignment='center', horizontalalignment='right',
                transform=text_transform,
                fontsize = 4,
                bbox=dict(facecolor='sandybrown', alpha=0.2, boxstyle='round'))

    #print(latlonshigh)
    #print(latlonslow)

    def Haversine(latlons1, latlons2):

        R = 6371
        dlat = math.radians(latlons2[0] - latlons1[0])
        dlon = math.radians(latlons2[1] - latlons1[1])
        lat1 = math.radians(latlons1[0])
        lat2 = math.radians(latlons2[0])

        a = (math.sin((dlat) / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin((dlon) / 2) ** 2)
        c = 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return c

    Dist_To_Liverpool_list = {}
    Dist_To_Location_list = []
    TempList = []


    Liverpool = [53.416667, -3.0]
    key_list = list(latlonshigh.keys())
    key_list2 = list(latlonslow.keys())
    i = 0

    for city in latlonshigh:
        Dist_To_Liverpool_list[key_list[i]] = round(Haversine(latlonshigh[city], Liverpool),0)
        TempList.append(key_list[i])
        TempList.append(latlonshigh[city])
        TempList.append(City_Pop[city])
        TempList.append(Dist_To_Liverpool_list[city])
        TempList.append(0)
        Dist_To_Location_list.append((TempList))
        TempList = []
        i += 1
    print(Dist_To_Location_list)

    Dist_To_Location_list.sort(key=lambda x: x[3])
    j = 1
    #Dist_To_Location_list.reverse()
    for i in Dist_To_Location_list:
        i[4] = j
        print("The distance to Liverpool from {} is {}km (Rank: {})".format(i[0], i[3], i[4]))
        j += 1
    print(Dist_To_Location_list)




## Next to do is to cut up the country into Regions and visualise

## Next to do is assign a score to the place based on distance and willingness to move/ commmute

## Next to do is to get more 6 more companies and colour by sector ===> At least try to webscrape from a jobs website

## Next to do is write a GUI in pyQT


    #plt.show()






if __name__ == '__main__':
    main()

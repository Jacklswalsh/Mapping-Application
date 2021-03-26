import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def main():
    stamen_terrain = cimgt.Stamen('terrain-background')
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([2.3, -11.5, 49.2, 60], crs=ccrs.Geodetic())
    ax.add_image(stamen_terrain, 6)
    city_list = pd.read_csv('gb.csv')
    print(city_list)

    latlonshigh = {}
    latlonslow = {}
    for i, v in city_list.iterrows():
        if city_list.iloc[i, 8] > 600000:
            city = city_list.iloc[i, 0]
            long, lat = city_list.iloc[i, 1], city_list.iloc[i, 2]
            latlonshigh[city] = (long, lat)
        elif 600000 > city_list.iloc[i, 8] > 400000:
            city = city_list.iloc[i, 0]
            long, lat = city_list.iloc[i, 1], city_list.iloc[i, 2]
            latlonslow[city] = (long, lat)

    for key in latlonshigh:
        ax.plot(latlonshigh[key][1], latlonshigh[key][0], marker='.', color='k', markersize=10,
                        alpha=1, transform=ccrs.Geodetic())
        geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
        text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
        ax.text(latlonshigh[key][1], latlonshigh[key][0], u"{}".format(key),
                verticalalignment='center', horizontalalignment='right',
                transform=text_transform,
                fontsize = 6,
                bbox=dict(facecolor='sandybrown', alpha=0.6, boxstyle='round'))

    for key in latlonslow:
        ax.plot(latlonslow[key][1], latlonslow[key][0], marker='.', color='k', markersize=10,
                        alpha=1, transform=ccrs.Geodetic())
        geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
        text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
        ax.text(latlonslow[key][1], latlonslow[key][0], u"{}".format(key),
                verticalalignment='center', horizontalalignment='right',
                transform=text_transform,
                fontsize = 4,
                bbox=dict(facecolor='sandybrown', alpha=0.2, boxstyle='round'))

    print(latlonshigh)
    print(latlonslow)

    my_url = "https://www.jaguarlandrovercareers.com/content/United-Kingdom/?locale=en_GB"
    class_item = "map-detail--info"
    loc = [3,4]

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    field_item1 = page_soup.find_all("div", {"class": class_item})

    my_url2 = "https://new.siemens.com/uk/en/company/about/siemens-uk-locations.html"
    class_item2 = "headline__base"
    loc = [3,4]

    uClient2 = uReq(my_url2)
    page_html2 = uClient2.read()
    uClient2.close()
    page_soup2 = soup(page_html2, "html.parser")
    field_item2 = page_soup2.find_all("div", {"class": class_item2})
    print(field_item2)

    def consruct_list(list, city_list, latlons):
        for city in list:
            for i, v in city_list.iterrows():
                if city == city_list.iloc[i, 1]:
                    long, lat = city_list.iloc[i, loc[0]], city_list.iloc[i, loc[1]]
                    latlons[city] = (long, lat)
        return latlons

    Jaguar_list = []
    Siemens_list = []





    def Jaguar_find(field_item, list):
        for i in range(len(field_item)):
            for h2 in field_item[i].find_all("h2"):
                list.append(h2.text.replace('\n', ' ').strip())
        return list
    print("Jaguar Find: {}".format(Jaguar_find(field_item1, Jaguar_list)))

    def Siemens_find(field_item, list):
        for i in range(len(field_item)):
            for h3 in field_item[i].find_all("h3"):
                list.append(h3.text.replace('\n', ' ').strip())
        return list


    Jag_list = Jaguar_find(field_item1, Jaguar_list)
    Sie_list = Siemens_find(field_item2, Siemens_list)


    city_list1 = pd.read_csv('UK_CITIES_300.csv')
    latlons1 = {}
    latlons2 = {}
    Jaguar_latlons = consruct_list(Jag_list, city_list1, latlons1)
    print(Jaguar_latlons)
    Siemens_latlons = consruct_list(Sie_list, city_list1, latlons2)
    print(Siemens_latlons)


    for key in Jaguar_latlons:
        ax.scatter(Jaguar_latlons[key][1], Jaguar_latlons[key][0], transform=ccrs.Geodetic(), marker=".", s=25, c="red")
    for key in Siemens_latlons:
        ax.scatter(Siemens_latlons[key][1], Siemens_latlons[key][0], transform=ccrs.Geodetic(), marker=".", s=25, c="green")

    plt.show()


if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.offsetbox import AnchoredText
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

# Make it so that for best - The program will extract the text before the comma in the string
# Score
## Make it so that this is a class and all thats needed is to feed the url and the location in the html

def main(url, class_item, file, col, mark, loc, func):

    my_url = url
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    field_item1 = page_soup.find_all("div", {"class": class_item})

    city_list = []
    #print(field_item1)
    extracted_names = func(field_item1[0], city_list)
    print(extracted_names)
    city_list1 = pd.read_csv(file)

    latlons1 = {}
    for city in extracted_names:
        for i, v in city_list1.iterrows():
            if city == city_list1.iloc[i, 0]:
                long, lat = city_list1.iloc[i, loc[0]], city_list1.iloc[i, loc[1]]
                latlons1[city] = (long, lat)

    for key in latlons1:
        ax.scatter(latlons1[key][1], latlons1[key][0], transform=ccrs.PlateCarree(), marker=mark, s=100, c=col)
    print(latlons1)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([-140, -55, 20, 75], crs=ccrs.PlateCarree())
ax.stock_img()
states_provinces = cfeature.NaturalEarthFeature(
    category="cultural",
    name="admin_1_states_provinces_lines",
    scale="50m",
    facecolor="none")
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle='-')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(states_provinces, edgecolor="gray")


def func_Jacobs(items, cities):
    for call in items.find_all("h3"):
        cities.append(call.strong.text.replace('\n', ' ').strip())
    return cities


def func_Bombardier(fitem, Bom_cities):
    for i in range(18):
        f1 = fitem[i].span.text
        Bom_cities.append(f1.replace('\n', ' ').strip())

def func_Best(items, Best_Cities):
    for item in items.find_all("td"):
        Best_Cities.append(item.text.replace('\n', ' ').strip())
    return Best_Cities












main("https://www.jacobs.com/locations/canada", "field-item", "Cities3.csv", "r", ".", [1,2], func_Jacobs)
main("https://www.jacobs.com/locations/united-states", "field-item", "US_Cites1.csv", "k",".", [8,9], func_Jacobs)
#main("https://www.bombardier.com/en/worldwide-presence/country.canada.html", "site-first", "Cities.csv", "k", ".", [1,2], func_Bombardier)
#main("https://www.canadianbusiness.com/lists-and-rankings/best-jobs/best-employers/large-employers-2018/", "single-article-text", "Cities.csv", "k", ".", [1,2], func_Best)
#main("https://www.canadianbusiness.com/lists-and-rankings/best-jobs/best-employers-2017-top-large-companies/", "single-article-text", "Cities.csv", "k", "x", [1,2], func_Best)
#main("https://www.canadianbusiness.com/lists-and-rankings/best-jobs/best-employers-ranking-2016/", "single-article-text", "Cities.csv", "k", ".", [1,2], func_Best)

plt.show()
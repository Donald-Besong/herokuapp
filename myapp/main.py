#AUTHOR: Donald O. Besong

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Select, Label
from bokeh.layouts import layout
from bokeh.plotting import figure
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians
from pytz import timezone

#create figure
f=figure(x_axis_type='datetime')

#create webscraping function
bcsite = "http://bitcoincharts.com/markets/btcnCNY.html" # I will later use https://www.bitmex.com/app/trade/XBTUSD instead, s=value_raw[3], s.text
bttrsite = "http://bitcoincharts.com/markets/btctradeCNY.html"
def extract_value(site=bcsite):
    r=requests.get(site,headers={'User-Agent':'Mozilla/5.0'})
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    value_raw=soup.find_all("p")
    value_net=float(value_raw[0].span.text)
    return value_net

#create ColumnDataSource
site = bcsite
source=ColumnDataSource(dict(x=[datetime.now(tz=timezone('Europe/Moscow'))],y=[extract_value(site)]))

#create glyphs
f.circle(x='x',y='y',color='olive',line_color='brown',source=source)
f.line(x='x',y='y',source=source)

f.xaxis.major_label_orientation=radians(90)

###begin code for plotting locally**********************************************
#from bokeh.io import output_file, show
#output_file("bitcoins.html")
#show(f)
###begin code for plotting locally**********************************************
#

###begin code for embedding static plot to html*********************************
#from bokeh.embed import components
#from bokeh.resources import CDN
#js,div=components(f)
#cdn_js=CDN.js_files[0]
#cdn_css=CDN.css_files[0]
###end code for embedding static plot to html***********************************



#begin code for dynamic plots***************************************************
#create Select widget
options=[(bcsite,"BTCN China"),(bttrsite,"bttrade CNY")]
select=Select(title="Market Name",value=bcsite,options=options)
#create periodic function
def update():
    site = select.value
    new_data=dict(x=[datetime.now(tz=timezone('Europe/Moscow'))],y=[extract_value(site)])
    source.stream(new_data,rollover=200)
    print(source.data)

def update_intermediate(attr, old, site):
    source.data=dict(x=[],y=[])
    update()
f.xaxis.formatter=DatetimeTickFormatter(
seconds=["%Y-%m-%d-%H-%m-%S"],
minsec=["%Y-%m-%d-%H-%m-%S"],
minutes=["%Y-%m-%d-%H-%m-%S"],
hourmin=["%Y-%m-%d-%H-%m-%S"],
hours=["%Y-%m-%d-%H-%m-%S"],
days=["%Y-%m-%d-%H-%m-%S"],
months=["%Y-%m-%d-%H-%m-%S"],
years=["%Y-%m-%d-%H-%m-%S"],
)

# configure visual properties on a plot's title attribute
f.title.text = "Streaming financial data - AUTHOR: Dr Donald O. Besong"
f.title.align = "right"
#f.title.text_color = "orange"
#f.title.text_font_size = "25px"
f.title.background_fill_color = "yellow"

select.on_change("value",update_intermediate)

#add figure to curdoc and configure callback
lay_out=layout([[f],[select]])
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update,2000)
#end code for dynamic plots***************************************************

#4. Displaying the document using (note Microsft edge does not work well. Use Chrome)
#on the command line, run bokeh serve --show main.py

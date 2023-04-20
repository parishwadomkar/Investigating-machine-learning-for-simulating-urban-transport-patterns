import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State,MATCH,ALL
import pandas as pd
import dash_table
from dash.exceptions import PreventUpdate
from flask import Flask
import os
import base64
import plotly.graph_objects as go
from string import digits
import Functions
import about_us
import requests
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {   'Omkar': '12345'}

server = Flask(__name__)
app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ] , external_stylesheets=[dbc.themes.BOOTSTRAP]
)

auth = dash_auth.BasicAuth( app, VALID_USERNAME_PASSWORD_PAIRS)

app.config.suppress_callback_exceptions = True

Urban_Districts = ['30101 Gamle Oslo','30102 Grünerløkka', '30103 Sagene','30104 St. Hanshaugen', '30105 Frogner','30106 Ullern', '30107 Vestre Aker','30108 Nordre Aker',
                   '30109 Bjerke','30110 Grorud', '30111 Stovner','30112 Alna', '30113 Østensjø','30114 Nordstrand',
                   '30115 Søndre Nordstrand','30116 Sentrum', '30117 Marka']

Grunnkrets = ['3012401 Tøyen Rode 1', '3012408 Tøyen Rode 8', '3012409 Tøyen Rode 9',
              '3012502 Grønland Rode 2', '3012503 Grønland Rode 3', '3012504 Grønland Rode 4', '3012505 Grønland Rode 5',
              '3012506 Grønland Rode 6','3012507 Grønland Rode 7','3012508 Grønland Rode 8','3012509 Grønland Rode 9',
              '3012601 Kampen Rode 1','3012602 Kampen Rode 2','3012603 Kampen Rode 3','3012604 Kampen Rode 4',
              '3012605 Kampen Rode 5','3012606 Kampen Rode 6','3012607 Kampen Rode 7','3012608 Kampen Rode 8',
              '3012609 Kampen Rode 9','3012610 Kampen Rode 10', '3012701 Vålerenga Rode 1', '3012702 Vålerenga Rode 2',
'3012703 Vålerenga Rode 3', '3012704 Vålerenga Rode 4', '3012705 Vålerenga Rode 5',
'3012706 Vålerenga Rode 6', '3012801 Gamlebyen Rode 1', '3012802 Gamlebyen Rode 2',
'3012803 Gamlebyen Rode 3', '3012804 Gamlebyen Rode 4', '3012805 Gamlebyen Rode 5',
'3012902 Loenga Sør', '3012903 Loenga Nord', '3013001 Grønlia', '3013513 Ryenberget',
'3013514 Nygårdskollen', '3013515 Kværner Nord', '3013516 Kværner Øst', '3013517 Kværner Sør'
, '3014202 Valle', '3014203 Etterstad', '3014204 Helsfyr', '3014210 Brynseng', '3014211 Ensjø Øst',
 '3014212 Ensjø Vest', '3014213 Ensjø Nord', '3014214 Ensjø Sør', '3015701 Øyene',
'3010207 Sentrum 2 - Rode 7', '3010210 Sentrum 2 - Rode 10', '3011305 Gamle Aker Rode 5',
'3012007 Torshov Rode 7', '3012008 Torshov Rode 8', '3012101 Sinsen Rode 1', '3012103 Sinsen Rode 3',
 '3012104 Sinsen Rode 4', '3012105 Sinsen Rode 5', '3012106 Sinsen Rode 6', '3012107 Sinsen Rode 7',
 '3012108 Sinsen Rode 8', '3012109 Sinsen Rode 9', '3012201 Rodeløkka Rode 1',
'3012202 Rodeløkka Rode 2', '3012203 Rodeløkka Rode 3', '3012204 Rodeløkka Rode 4',
'3012205 Rodeløkka Rode 5', '3012206 Rodeløkka Rode 6', '3012207 Rodeløkka Rode 7',
'3012208 Rodeløkka Rode 8', '3012209 Rodeløkka Rode 9', '3012301 Grünerløkka Rode 1',
'3012302 Grünerløkka Rode 2', '3012303 Grünerløkka Rode 3', '3012304 Grünerløkka Rode 4',
'3012305 Grünerløkka Rode 5', '3012306 Grünerløkka Rode 6', '3012307 Grünerløkka Rode 7',
'3012308 Grünerløkka Rode 8', '3012309 Grünerløkka Rode 9', '3012310 Grünerløkka Rode 10',
'3012311 Grünerløkka Rode 11', '3012312 Grünerløkka Rode 12', '3012313 Grünerløkka Rode 13',
 '3012402 Tøyen Rode 2', '3012403 Tøyen Rode 3', '3012404 Tøyen Rode 4', '3012405 Tøyen Rode 5',
 '3012406 Tøyen Rode 6', '3012407 Tøyen Rode 7', '3012410 Tøyen Rode 10', '3014304 Søndre Hovin',
 '3014306 Nordre Sinsen', '3014308 Løren Øst', '3014309 Løren Vest', '3014310 Frydenberg Øst',
 '3014311 Frydenberg Nord', '3014312 Frydenberg Vest', '3014313 Lille Tøyen Nord',
 '3014314 Lille Tøyen Vest', '3014315 Lille Tøyen Øst', '3011404 Ila Rode 4', '3011405 Ila Rode 5',
 '3011406 Ila Rode 6', '3011601 Sagene Rode 1', '3011602 Sagene Rode 2', '3011603 Sagene Rode 3',
 '3011604 Sagene Rode 4', '3011605 Sagene Rode 5', '3011606 Sagene Rode 6',
'3011607 Sagene Rode 7', '3011701 Bjølsen Rode 1', '3011702 Bjølsen Rode 2', '3011703 Bjølsen Rode 3',
 '3011704 Bjølsen Rode 4', '3011705 Bjølsen Rode 5', '3011706 Bjølsen Rode 6', '3011707 Bjølsen Rode 7', '3011708 Bjølsen Rode 8', '3011801 Sandaker Rode 1', '3011803 Sandaker Rode 3',
 '3011804 Sandaker Rode 4', '3011901 Åsen Rode 1', '3011902 Åsen Rode 2',
'3011903 Åsen Rode 3', '3011904 Åsen Rode 4', '3011906 Åsen Rode 6', '3011907 Åsen Rode 7',
'3011908 Åsen Rode 8', '3011909 Åsen Rode 9', '3011910 Åsen Rode 10', '3012001 Torshov Rode 1',
 '3012002 Torshov Rode 2', '3012003 Torshov Rode 3', '3012004 Torshov Rode 4', '3012005 Torshov Rode 5',
 '3012006 Torshov Rode 6', '3012009 Torshov Rode 9', '3012010 Torshov Rode 10',
 '3012011 Torshov Rode 11', '3012012 Torshov Rode 12', '3012102 Sinsen Rode 2', '3010201 Sentrum 2 - Rode 1',
 '3010202 Sentrum 2 - Rode 2', '3010204 Sentrum 2 - Rode 4', '3010205 Sentrum 2 - Rode 5',
 '3010206 Sentrum 2 - Rode 6', '3010208 Sentrum 2 - Rode 8', '3010209 Sentrum 2 - Rode 9'
, '3010212 Sentrum 2 - Rode 12', '3010213 Sentrum 2 - Rode 13', '3011001 Marienlyst',
 '3011101 Fagerborg Rode 1', '3011102 Fagerborg Rode 2', '3011103 Fagerborg Rode 3',
 '3011104 Fagerborg Rode 4', '3011105 Fagerborg Rode 5', '3011106 Fagerborg Rode 6',
 '3011201 St.hanshaugen Rode 1', '3011202 St.hanshaugen Rode 2', '3011203 St.hanshaugen Rode 3',
 '3011204 St.hanshaugen Rode 4', '3011205 St.hanshaugen Rode 5', '3011206 St.hanshaugen Rode 6',
 '3011207 St.hanshaugen Rode 7', '3011208 St.hanshaugen Rode 8',
'3011209 St.hanshaugen Rode 9', '3011210 St.hanshaugen Rode 10', '3011211 St.hanshaugen Rode 11',
 '3011301 Gamle Aker Rode 1', '3011302 Gamle Aker Rode 2', '3011303 Gamle Aker Rode 3',
 '3011304 Gamle Aker Rode 4', '3011401 Ila Rode 1', '3011402 Ila Rode 2”, ”3011403 Ila Rode 3',
 '3011501 Lindern Rode 1', '3011502 Lindern Rode 2', '3011503 Lindern Rode 3',
'3011504 Lindern Rode 4', '3010301 Sentrum 3 - Rode 1', '3010302 Sentrum 3 - Rode 2',
'3010303 Sentrum 3 - Rode 3', '3010304 Sentrum 3 - Rode 4', '3010308 Sentrum 3 - Rode 8',
'3010401 Filipstad', '3010501 Skillebekk Rode 1', '3010502 Skillebekk Rode 2', '3010503 Skillebekk Rode 3',
 '3010504 Skillebekk Rode 4', '3010601 Frogner Rode 1', '3010602 Frogner Rode 2',
 '3010603 Frogner Rode 3', '3010604 Frogner Rode 4', '3010605 Frogner Rode 5',
'3010606 Frogner Rode 6', '3010607 Frogner Rode 7', '3010608 Frogner Rode 8', '3010609 Frogner Rode 9',
 '3010610 Frogner Rode 10', '3010611 Frogner Rode 11', '3010612 Frogner Rode 12',
 '3010613 Frogner Rode 13', '3010614 Frogner Rode 14', '3010701 Uranienborg Rode 1',
'3010702 Uranienborg Rode 2', '3010703 Uranienborg Rode 3', '3010704 Uranienborg Rode 4',
'3010705 Uranienborg Rode 5', '3010706 Uranienborg Rode 6', '3010707 Uranienborg Rode 7',
'3010708 Uranienborg Rode 8', '3010709 Uranienborg Rode 9', '3010710 Uranienborg Rode 10',
'3010801 Homansbyen Rode 1', '3010802 Homansbyen Rode 2', '3010803 Homansbyen Rode 3',
'3010804 Homansbyen Rode 4', '3010805 Homansbyen Rode 5', '3010806 Homansbyen Rode 6',
'3010807 Homansbyen Rode 7', '3010808 Homansbyen Rode 8', '3010809 Homansbyen Rode 9',
'3010901 Majorstuen Rode 1', '3010902 Majorstuen Rode 2', '3010903 Majorstuen Rode 3',
'3010904 Majorstuen Rode 4', '3010905 Majorstuen Rode 5', '3010906 Majorstuen Rode 6',
'3010907 Majorstuen Rode 7', '3010908 Majorstuen Rode 8', '3010909 Majorstuen Rode 9',
'3010910 Majorstuen Rode 10', '3010911 Majorstuen Rode 11', '3010912 Majorstuen Rode 12',
'3010913 Majorstuen Rode 13', '3015601 Kongsgården', '3015602 Grande', '3015603 Fredriksborg',
 '3014703 Smestad', '3014706 Nordre Skøyen', '3014803 Husebybakken',
'3014804 Montebello', '3014805 Smestaddammen', '3014806 Abbedikollen', '3015206 Rolighet',
 '3015207 Ullerntoppen', '3015208 Ullernåsen', '3015210 Åsjordet', '3015301 Lysehagan',
 '3015302 Øraker', '3015303 Lysaker', '3015401 Bjørnsletta', '3015402 Furulund',
'3015403 Sollerud', '3015405 Bestum', '3015406 Vækerø', '3015407 Hoff Sør', '3015408 Hoff Nord',
 '3015501 Amalienborg', '3015502 Madserud', '3015503 Søndre Skøyen', '3015504 Sjølyst',
 '3014601 Vettakollen', '3014602 Slemdal', '3014603 Risbakken', '3014604 Vindern',
'3014611 Gråkammen', '3014701 Frøen', '3014702 Heggeli', '3014704 Volvat', '3014705 Grimelund',
'3014801 Persbråten', '3014802 Husebyskogen', '3014901 Hovseter', '3014902 Holmensletta',
 '3014903 Vestre Holmen', '3014904 Østre Holmen', '3014905 Svenstua',
'3014906 Løkkaskogen', '3014907 Lybekk', '3014908 Gressbanen', '3014909 Holmenbekken',
'3014910 Hamborg', '3014911 Jarbakken', '3014912 Arnebråten', '3015001 Lillevann',
'3015002 Østre Liaskogen', '3015003 Besserud', '3015004 Voksenåsen', '3015005 Vestre Liaskogen',
 '3015006 Bogstad', '3015007 Skogen', '3015008 Grindbakken', '3015201 Voksen',
'3015202 Sørsletta', '3015203 Røahagan', '3015204 Røa', '3015209 Myrhaugen', '3015211 Mosekollen Vest',
 '3015212 Mosekollen Øst', '3011709 Bjølsen Rode 9', '3014117 Ymers Vei',
'3014401 Frysjå', '3014402 Kjelsås', '3014403 Grefsenplatået', '3014405 Lillo Terrasse'
              ]








text_font_size='1.7vh'
navbar_font_size='1.8vh'
header_font_size='2vh'

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'kth.png')

### the part bellow is for the logo image on the header ( note that it is commented in the layout object so remove the comment to show it
encoded = base64.b64encode(open(my_file,'rb').read())

logo_img=html.Div([html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', height='70vh',
                  style=dict(marginLeft='1vh')) ],style=dict(display='inline-block'))

db_logo_img=dbc.Col([ logo_img] ,
        xs=dict(size=2,offset=0), sm=dict(size=2,offset=0),
        md=dict(size=1,offset=0), lg=dict(size=1,offset=0), xl=dict(size=1,offset=0))
###

### the part bellow is for the header text
header_text=html.Div('Transport Model For Simulating Urban Scenarios For Oslo City, Norway',style=dict(color='white',
                     fontWeight='bold',fontSize='2.5vh',paddingTop='1vh',marginLeft='',display='inline-block', paddingBottom='1vh'
                                                                                                       ))

db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=0), sm=dict(size=10,offset=0),
        md=dict(size=8,offset=0), lg=dict(size=7,offset=0), xl=dict(size=7,offset=0))
###

### the part bellow is for the navigation buttons to switch between simulations and about us pages
navigation_header=html.Div([dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Simulations", active='exact', href="/Simulations",id='Simulations', className="page-link",
                                style=dict(fontSize=navbar_font_size))),

        dbc.NavItem(dbc.NavLink("About us", href="/About_us", active='exact', id='About_us',className="page-link",
                                style=dict(fontSize=navbar_font_size)))
    ],
        pills=True,horizontal='left'
)
],style=dict(display='inline-block',marginLeft=''))

db_navigation_header=dbc.Col([navigation_header],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=4, offset=0), lg=dict(size=5, offset=0), xl=dict(size=5, offset=0)
                             )
###

### welcome msg
welcome_msg=html.Div(html.H1('Welcome Omkar Parishwad',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black',marginLeft='2vh')) ,style=dict(display=''))
###

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'Params.csv')
df=pd.read_csv(my_file)



### the part bellow is for initializing the map 1 figure ( only the layout is made but the figure data is created upon calling the related function in callback ( update_map1 ) )

fig=go.Figure()

fig.update_layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
          #      bearing=25,
                style='light',
            center=dict(
                lon=10.7658488126624,
                lat=59.93827295
            ),
          #  pitch=40,
            zoom=9.7
            ) ,margin = dict(l = 0, r = 0, t = 30, b = 0), hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell")
        )
fig.update_layout(mapbox_style="open-street-map")
###

### the part bellow is for initializing the map 2 figure ( only the layout is made but the figure data is created upon calling the related function in callback ( update_map2 ) )
fig2=go.Figure(go.Scattermapbox())
fig2.update_layout(
            uirevision= 'foo2', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
            #    bearing=25,
                style='light',
            center=dict(
                lon=10.7658488126624,
                lat=59.93827295
            ),
          #  pitch=40,
            zoom=9.7
            ),margin = dict(l = 0, r = 0, t = 0, b = 0)
        )
fig2.update_layout(mapbox_style="open-street-map")
###

### map1 header text
map_header1=html.Div(html.H1('Existing Transport Model (2019 flows)',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black')) ,style=dict(marginLeft=''))
###

### map2 header text
map_header2=html.Div(html.H1('Simulated Transport Scenario',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black')) ,style=dict(marginLeft=''))
###

### map1 division which will either contain plotly or folium map depoending on value if visualization dropdown when the callback of (update_map1) is triggered
m1_div=html.Div([
            dcc.Graph(id='map1', config={'displayModeBar': True, 'scrollZoom': True,'displaylogo': False},
                style={'height':'60vh'} ,figure=Functions.create_combined_map(df,[])
            ) ] ,id='map1_div'
        )
###

### this is the spinner component around map1 division to make the reload sigh apears while reloading the map
map_div1=dbc.Spinner([m1_div], size="lg", color="primary", type="border", fullscreen=False)
###

db_map_div1=dbc.Col([ map_header1,map_div1] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=8,offset=1), lg=dict(size=5,offset=1), xl=dict(size=5,offset=1))


### map2 division which will either contain plotly or folium map depoending on value if visualization dropdown when the callback of (update_map2) is triggered
m2_div=html.Div([
            dcc.Graph(id='map2', config={'displayModeBar': True, 'scrollZoom': True,'displaylogo': False},
                style={'height':'60vh'} ,figure=fig2
            ) ] ,id='map2_div'
        )
###


map_div2=dbc.Spinner([m2_div], size="lg", color="primary", type="border", fullscreen=False)



db_map_div2=dbc.Col([ map_header2,map_div2] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=8,offset=1), lg=dict(size=5,offset=0), xl=dict(size=5,offset=0))




simulation_type_text=html.Div(html.H1('Type of Simulation For Visualization: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))


### this is the dropdown menu that is connected to update_map1 and update_map2 callbacks that changes both divisions content when pressing okay

simulation_type_menu=  dcc.Dropdown(
        id='sim_dropdown',
        options=[
            dict(label='Node-Node(Network)', value='Network'), dict(label='Zone-Zone(Flows)', value='Flows')
        ],
        value='Flows' , style=dict(color='black',fontWeight='bold',textAlign='left',
                                     width='20vh',backgroundColor='#2358a6',border='1px solid #2358a6')
    )


simulation_type_menu_div= html.Div([simulation_type_menu],
                          style=dict(fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='',display='inline-block'))
###


model_type_text=html.Div(html.H1('Transport Model Used For Simulation:',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block',marginLeft='3vh'))

### not used now
model_type_menu=  dcc.Dropdown(
        id='model_dropdown',
        options=[
            dict(label='Gravity Model(SIM)', value='SIM'), dict(label='Machine Learning(AI)', value='AI')
        ],
        value='SIM' , style=dict(color='black',fontWeight='bold',textAlign='center'
                                 ,width='20vh',backgroundColor='#2358a6',border='1px solid #2358a6')
    )

model_type_menu_div= html.Div([model_type_menu],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='-1.5vh',display='inline-block'))
###

### not used now
city_text=html.Div(html.H1('City Subdivisons:',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block',marginLeft='3vh'))


city_menu=  dcc.Dropdown(
        id='city_dropdown',
        options=[
            dict(label='Urban Districts', value='Urban'), dict(label='Grunnkrets', value='Grunnkrets')
        ],
        value='Urban' , style=dict(color='black',fontWeight='bold',textAlign='left',
                                   width='15vh',backgroundColor='#2358a6',border='1px solid #2358a6')
    )

city_menu_div= html.Div([city_menu],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='-1.5vh',display='inline-block'))
###

### ok button that triggers update_map1 and update_map2 callbacks and responsible for updating maps when pressed depending on dropdowns values

ok_button = html.Div([dbc.Button("OK", color="primary", size='sm', n_clicks=0,
                                 id='ok_button',
                                 style=dict(fontSize='1.8vh')
                                 )], style=dict(display='inline-block', marginLeft='1vh'))
###

map_style_text=html.Div(html.H1('Maps Background Style:',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block',marginLeft='3vh'))

### dropdown menu that is also connected to update_map1 and update_map2 callbacks for changing maps background type
map_style_menu=  dcc.Dropdown(
        id='map_style_dropdown',
        options=[
            dict(label='open-street-map', value='open-street-map'), dict(label='carto-positron', value='carto-positron'),
            dict(label='carto-darkmatter', value='carto-darkmatter'), dict(label='stamen-terrain', value='stamen-terrain'),
            dict(label='stamen-toner', value='stamen-toner'), dict(label='stamen-watercolor', value='stamen-watercolor')
        ],
        value='open-street-map' , style=dict(color='black',fontWeight='bold',textAlign='center'
                                 ,width='20vh',backgroundColor='#2358a6',border='1px solid #2358a6')
    )

map_style_menu_div= html.Div([map_style_menu],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='',display='inline-block'))
###

### checklist for choosing the maps which will be affected by dropdown menus values when pressing ok ( also connected to update_map1 and update_map2 callbacks )
chosen_map=html.Div(dbc.Checklist( options=[{"label": "Map1", "value": 'Map1'},{"label": "Map2", "value": 'Map2'}],
    value=['Map1','Map2'],
    id="chosen_map", label_style=dict(fontSize='1.5vh'),inline=True
) , style=dict(display='inline-block', marginLeft='1.5vh'))
###

db_dropdowns=dbc.Col(html.Div([simulation_type_text,simulation_type_menu_div,map_style_text,map_style_menu_div,chosen_map,ok_button
                      ] , style=dict(width='100%',display= 'flex', alignItems= 'center', justifyContent= 'center')),
                             xs=dict(size=8, offset=2), sm=dict(size=8, offset=2),
                             md=dict(size=10, offset=1), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1)
                             )



scenario_header=html.H1('Oslo City Transport Simulation',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black'))


db_scenario_header=dbc.Col([scenario_header],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=8, offset=1), lg=dict(size=8, offset=1), xl=dict(size=8, offset=1)
                             )

### this is tha tabs component that responsible for changing the content of the container when a tab is pressed ( change_content callback )
navigation_header2=dbc.Tabs(
            [
                dbc.Tab(label="Scenario Selection", tab_id="Parameters",label_style={"color": "#0d6efd",'fontSize':navbar_font_size},active_tab_style={'border':'4px solid black','color':'#0d6efd'}
                        ,active_label_style={"color": 'black','fontSize':navbar_font_size,'fontWeight':'bold'},tab_style={'border':'2px solid black'}),



                dbc.Tab(label="Model Analysis", tab_id="Model Analysis",label_style={"color": "#0d6efd",'fontSize':navbar_font_size},active_tab_style={'border':'4px solid black'}
                        ,active_label_style={"color": 'black','fontSize':navbar_font_size,'fontWeight':'bold'},tab_style={'border':'2px solid black'}),


                dbc.Tab(label="Infographics", tab_id="Infographics",label_style={"color": "#0d6efd",'fontSize':navbar_font_size},active_tab_style={'border':'4px solid black'}
                        ,active_label_style={"color": 'black','fontSize':navbar_font_size,'fontWeight':'bold'},tab_style={'border':'2px solid black'})

            ],
            id="tabs",
            active_tab="Parameters",
        )






db_navigation_header2=dbc.Col([navigation_header2],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=10, offset=1), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1)
                             )


scenario_selection_text=html.Div(html.H1('Select Parameter for Simulation: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))


subdivision_text=html.Div(html.H1('Select the Subdivision: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh',marginLeft='3vh')),
                           style=dict(display='inline-block'))



### bellow is add and remove parameter buttons which are used to trigger the dynamic callback ( add_parameter ) which is different from all other callbacks
#because it create and remove dash components dynamically upon pressing on these buttons
multiple_param=html.Div([dbc.Button("Add Parameter(+)", color="primary", size='lg', n_clicks=0,id="multiple_param"
                            ,style=dict(fontSize=text_font_size,width='20vh')
                            ) ],style=dict(display='inline-block'))

remove_param=html.Div([dbc.Button("Remove Parameter(-)", color="primary", size='lg', n_clicks=0,id="remove_param"
                            ,style=dict(fontSize=text_font_size,width='20vh')
                            )],style=dict(display='inline-block',marginLeft='2vh'))

db_multiple_param=dbc.Col([html.Br(),multiple_param,remove_param],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=8, offset=1), lg=dict(size=8, offset=0), xl=dict(size=8, offset=0)
                             )
###

existing_param_text=html.Div(html.H1('Existing 2019 parameter value: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))


revised_param_text=html.Div(html.H1('Revised Parameter Value For Simulation: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block',marginLeft='2vh'))

### not used now
display_button=html.Div([ dbc.Button("Display", color="primary", size='lg', n_clicks=0,id="display_button"
                            ,style=dict(fontSize=text_font_size)
                            )  ],style=dict(display='inline-block'))
###

### this is the button that triggers analyze callback that connects to IBM model and get the results that is saved in the dcc.Store components and used in all sections of the app
analyze_button=html.Div([dbc.Button("Analyze", color="primary", size='lg', n_clicks=0,id="analyze_button"
                            ,style=dict(fontSize=text_font_size)
                            )],style=dict(display='inline-block',marginLeft=''))

### not used now
reset_map_button=html.Div([dbc.Button("Reset Map", color="primary", size='lg', n_clicks=0,id="reset_map_button"
                            ,style=dict(fontSize=text_font_size)
                            ) ],style=dict(display='inline-block',marginLeft='2vh'))
###

db_analyze_button=dbc.Col([html.Br(),analyze_button],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=10, offset=1), lg=dict(size=6, offset=0), xl=dict(size=6, offset=0)
                             )


### download buttons that download table data and they triggers download_trips_csv and download_parameters_csv callbacks
download_csv1=html.Div([dbc.Button("Download", color="primary", size='lg', n_clicks=0,id="download_csv1"
                            ,style=dict(fontSize=text_font_size)
                            )],style=dict(display='',marginLeft=''))

download_csv2=html.Div([dbc.Button("Download", color="primary", size='lg', n_clicks=0,id="download_csv2"
                            ,style=dict(fontSize=text_font_size)
                            )],style=dict(display='',marginLeft=''))
###

### bellow are 2 dash download components which are used in download_trips_csv and download_parameters_csv callbacks
csv_download_data1=html.Div([Download(id="csv_download_data1")])

csv_download_data2=html.Div([Download(id="csv_download_data2")])

### bellow is Analysis Done msg that is shown after analyze callback is executed succefully and it is wrapped around spinner component to to show loading sign
results=html.Div([''],id='results_msg',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )
results_msg=dbc.Spinner([results], size="lg", color="primary", type="border", fullscreen=False)

### parameters dropdown menu that is used with update_scatter callback to update the graph with the chosen parameter data
params_menu=  dcc.Dropdown(
        id='params_dropdown',
        options=[
            dict(label='Cost of Transport', value='Distance'), dict(label='Population', value='OPop'),
            dict(label='Employment', value='DEmpl'), dict(label='Origin Urban.', value='Ourban'),
            dict(label='Distination Urban.', value='Durban'), dict(label='Origin Income', value='OInc'),
            dict(label='Distination Income', value='DInc')
        ],
        value='OPop' , style=dict(color='black',fontWeight='bold',textAlign='center',
                                     width='20vh',backgroundColor='#2358a6',border='1px solid #2358a6')
    )

params_menu_div= html.Div([params_menu],
                          style=dict(fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='',display='inline-block'))
###

### same but with weekday data
week_day_menu=  dcc.Dropdown(
        id='week_day_dropdown',
        options=[
            dict(label='Monday', value='Monday'), dict(label='Tuesday', value='Tuesday'),
            dict(label='Wednesday', value='Wednesday'), dict(label='Thursday', value='Thursday'),
            dict(label='Friday', value='Friday'), dict(label='Saturday', value='Saturday'),
            dict(label='Sunday', value='Sunday')
        ],
        value='Monday' , style=dict(color='black',fontWeight='bold',textAlign='center',
                                     width='20vh',backgroundColor='#2358a6',border='1px solid #2358a6')
    )

week_day_menu_div= html.Div([week_day_menu],
                          style=dict(fontSize=text_font_size,
                                      marginLeft='2vh',marginBottom='',display='inline-block'))
###

### scatter division that is created and updated in infographic section
scatter_fig=go.Figure(go.Scatter())
scatter_div=html.Div([
            dcc.Graph(id='scatter', config={'displayModeBar': True, 'scrollZoom': True,'displaylogo': False},
                style={'height':'42vh'} ,figure=scatter_fig
            ) ] ,id='scatter_div'
        )


simulations_layout=  html.Div([html.Br(),dbc.Row(welcome_msg),html.Br(),dbc.Row([db_map_div1,db_map_div2]),html.Br(),
                      dbc.Row([db_dropdowns]),html.Br(),
                      dbc.Row([db_scenario_header]),html.Br(),
                      dbc.Row([db_navigation_header2]),

                      dbc.Row([dbc.Col([html.Div(
                      dbc.Container([dbc.Row(db_multiple_param),html.Div([],id='container'), # id='container' is the container div which is filled with the dynamic parameter upon adding and removing
                                     dbc.Row(db_analyze_button),html.Br(),results_msg],
                                    style=dict(border='2px solid black',maxHeight='47vh',overflow='scroll'),fluid=True
                      ),id='container_content' ) # id='container_content' is the all the content bellow the the tabs which changes upon pressing on tabs

                      ],   xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=10, offset=1), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1))
                          ]),html.Br(),html.Br(), dcc.Store(id='map1_type', data='network'),
                      dcc.Store(id='map2_type', data='flow')
                #      dbc.Row(db_2_buttons),
                      ])

app.layout=html.Div([ dbc.Row([html.Div([ #logo_img,
                                            header_text],
                                        style=dict(width='100%',display= 'flex', alignItems= 'center', justifyContent= 'center')
                                        )],style=dict(backgroundColor='#2358a6') ),
                      navigation_header,

                      html.Div(id='layout') # the current page layout is passed to this div upon pressing on dbc.NavLink() by the callback bellow ( first callback )

                      ,dcc.Location(id='url', refresh=True,pathname='/Simulations'),dcc.Store(id='trips_df'),
                        dcc.Store(id='simulated_trips',data=pd.DataFrame().to_dict('records')),
                      dcc.Store(id='parametrs_info', data=pd.DataFrame().to_dict('records')),
                      dcc.Store(id='folium_df', data=pd.DataFrame().to_dict('records')),
                      dcc.Store(id='full_trips_df', data=pd.DataFrame().to_dict('records'))



])

# this callback is responsible for changing the page layout when the current pathname ( in dcc.Location() ) changes which represent the app url
# and it changes upon pressing on ( dbc.NavLink() ) where its href value is passed to dcc.Location() pathname automatically upon pressing

@app.callback(Output('layout','children'),
              Input('url','pathname'))
def change_page(url):
    if url == '/About_us':
        return about_us.layout

    elif url == '/Simulations':
        return simulations_layout

    else:
        raise PreventUpdate


# this callback changes the container_content which is bellow the tabs upon pressing on tabs ( dbc.Tabs() )
# by checking which tab id is active then return the corresponding layout

@app.callback(Output('container_content','children'),
              Input("tabs", "active_tab") ,[State('trips_df','data'),State('parametrs_info','data')],
)
def change_content(tab,trips,parameters):

    trips_df=pd.DataFrame(trips)  # here i read the trips json ( dict ) stored data from ( analyze ) callback into a dataframe to be used in constructing the table

    parameters_df=pd.DataFrame(parameters) # here i read the parameters json ( dict ) stored data from ( analyze ) callback into a dataframe to be used in constructing the table

    if tab == 'Model Analysis':

        if (trips_df.empty or parameters_df.empty):  # return this massage if no parameters data entered yet ( dataframes are empty )

            return  dbc.Container([html.Br(),html.H1('Please Enter Parameters Data to be Analyzed ',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black')),html.Br()],
                              style=dict(border='2px solid black',maxHeight='45vh',overflow='scroll'),fluid=True )

        # parameters table
        table1 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in parameters_df.columns
            ], id='table2', page_size=20,data=parameters
            , style_cell=dict(textAlign='center', border='1px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#2358a6',color='white' ,
                              fontWeight='bold', border='1px solid 2358a6', fontSize='2vh'),
            editable=False,row_deletable=False,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )],id='table_div2')

        # trips table
        table2 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in trips_df.columns
            ], id='table', page_size=20,data=trips
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#2358a6',color='white',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=False,row_deletable=False,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'},
            style_data_conditional = [{'if': { 'filter_query': '{Simulated_Trips} != {Trips}','column_id': 'Simulated_Trips'},
                                       'backgroundColor': 'skyblue'}]
            # 'overflowY': 'auto',
        )],id='table_div')
        return (dbc.Container([html.Br(),download_csv1,html.Br(),table1,html.Br(),download_csv2,html.Br(),table2,csv_download_data1,csv_download_data2], # returning tables and csv download components
                              style=dict(border='2px solid black',maxHeight='45vh',overflow='scroll'),fluid=True)
                , False
                )

    elif tab == 'Parameters' :

        return dbc.Container([dbc.Row(db_multiple_param),html.Div([],id='container'), # returning components of parameters tab with the container div that will be filled dynamically
                              dbc.Row(db_analyze_button),html.Br(),results_msg],
                              style=dict(border='2px solid black',maxHeight='45vh',overflow='scroll'),fluid=True )


    elif tab == 'Infographics':

        if (trips_df.empty or parameters_df.empty):
            return  dbc.Container([html.Br(),html.H1('Please Enter Parameters Data to be Analyzed ',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black')),html.Br()],
                              style=dict(border='2px solid black',maxHeight='45vh',overflow='scroll'),fluid=True )

        return dbc.Container([html.Br(),params_menu_div,week_day_menu_div,html.Br(), html.Br(), # returning components of Infographics tab with the scatter plot div that will be updated with ( update_scatter callback )
                              dbc.Spinner([scatter_div], size="lg", color="primary", type="border", fullscreen=False )  ],
                              style=dict(border='2px solid black',maxHeight='45vh',overflow='scroll'),fluid=True )

    else:
        return dash.no_update

# this callback update the scatter plot depending on values of dropdowns and it calls
@app.callback(Output('scatter','figure'),
              [Input('params_dropdown','value'),Input('week_day_dropdown','value')],
              State('full_trips_df','data')
)
def update_scatter(param_value,day,full_data):
    full_df=pd.DataFrame(full_data)
    return Functions.create_params_scatter(full_df,param_value,day) # we return the output of the function that create the scatter plot in functions.py file



# before getting into this callback please watch the video in link bellow to understand the dynamic callbacks because it is hard to be illustrated in comments
# https://youtu.be/4gDwKYaA6ww
# this callback is responsible for dynamically adding and removing the components of a parameter details before analyzing

@app.callback(
    Output('container', 'children'),
    [Input('multiple_param', 'n_clicks'),Input('remove_param', 'n_clicks')],
    [State('container', 'children')]
 #   ,prevent_initial_call=True
)
def add_parameter(n_clicks,n_clicks2,container_content):

    ctx = dash.callback_context # callback_context provid advanced info about callback like which input was triggered and if the callbacks is triggered or not
                                # see more details about it here https://dash.plotly.com/advanced-callbacks

    if True: # this is not important i just replaced it with something i made before so i put if True instead of re editing all the indentations

        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   # getting the id of the input component that fired the callback

        if input_id =='remove_param':  # if the remove_param button was pressed pop the last components was in containers div

            container_content.pop()
            return container_content

        elif input_id == 'multiple_param' or True:  # if input id is multiple_param add new parameters components to the container div

            subdivisions=Urban_Districts
            parameter_menu = dcc.Dropdown(
        id={'type': 'parameter_menu','index': n_clicks},
        options=[
            dict(label='Population', value='Population'),
            dict(label='Employment (Jobs)', value='Employment'),
            dict(label='Income Levels', value='Income'),
            dict(label='Urbanisation', value='Urbanisation'),
            dict(label='Cost of Transport', value='Distance')

        ],
        value='Population', style=dict(color='black', fontWeight='bold', textAlign='left',
                                       width='20vh', backgroundColor='#2358a6', border='1px solid #2358a6')
    )

            scenario_selection_menu_div = html.Div([parameter_menu],style=dict(fontSize=text_font_size,marginLeft='1vh',
                                                                       marginBottom='-1.5vh',display='inline-block'))

            subdivision_menu = dcc.Dropdown(
        id={
            'type': 'subdivisions_dynamic_menu',
            'index': n_clicks
        },
        options=[{'label': division, 'value': division} for division in subdivisions
                 ],
        value=subdivisions[0], style=dict(color='black', fontWeight='bold', textAlign='left',
                                             width='21vh', backgroundColor='#2358a6', border='1px solid #2358a6')
    )

            subdivision_menu_div = html.Div([subdivision_menu],style=dict(fontSize=text_font_size ,marginLeft='1vh',
                                                                  marginBottom='-1.5vh',display='inline-block'))

            ok_button = html.Div([dbc.Button("OK", color="primary", size='sm', n_clicks=0,
                                      id={'type': 'ok_button_dynamic', 'index': n_clicks},
                                      style=dict(fontSize='1.8vh')
                                     )], style=dict(display='inline-block',marginLeft='2vh'))

            db_menus = dbc.Col([scenario_selection_text,scenario_selection_menu_div,
                        subdivision_text, subdivision_menu_div,ok_button ,html.Br()],
                                  xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                  md=dict(size=10, offset=0), lg=dict(size=10, offset=0), xl=dict(size=10, offset=0)
                                  )

            existing_input = dbc.Input(id={'type': 'existing_input_dynamic','index': n_clicks},
                              placeholder='Enter Value', n_submit=0,
                              type='number', size="md", autocomplete='off',value='',
                              style=dict(width='15vh', border='1px solid black')
                                     )

            existing_param_input_div = html.Div([existing_input],
                                        style=dict(fontSize='1.7vh', marginLeft='1vh', marginBottom='-2vh',display='inline-block'))


            revised_input=dbc.Input(id={'type': 'revised_input_dynamic','index': n_clicks},
                         placeholder='Enter Value', n_submit=0,
                         type='number', size="md",autocomplete='off', value='',
                         style=dict(width='15vh',border='1px solid black'))

            revised_param_input_div =html.Div([revised_input],style=dict(fontSize='1.7vh',marginLeft='1vh',marginBottom='-2vh',display='inline-block'))

            variation_text = html.Div(html.H1('',id={'type': 'dynamic_variation_text','index': n_clicks},
                                              style=dict(fontSize=text_font_size, fontWeight='bold', color='black',
                                                         marginTop='1vh')),
                                      style=dict(display='inline-block', marginLeft='2vh'))

            db_inputs = dbc.Col([existing_param_text,existing_param_input_div,revised_param_text,revised_param_input_div,
                         variation_text , html.Br(), html.Br()],
                           xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                           md=dict(size=10, offset=0), lg=dict(size=11, offset=0), xl=dict(size=11, offset=0),
                           style=dict()
                           )

            new_div=html.Div([html.Br(),dbc.Row([db_menus]),html.Br(),dbc.Row([db_inputs])])

            container_content.append(new_div)  # after creating the new_div ( new parameters components ) append it to container div

            return container_content


# update the variation text when adding a new value in modified input field

@app.callback(
    Output({'type': 'dynamic_variation_text','index': MATCH},'children'),
    Input({'type': 'revised_input_dynamic', 'index': MATCH},'value'),
    [State({'type': 'existing_input_dynamic','index': MATCH}, 'value')]
,prevent_initial_call=True
)
def update_variation(modified_input,existing_input):

    if modified_input != '' and existing_input != '' : # checking that fields are not empty
        variation=( (float(modified_input)-float(existing_input))/float(existing_input) ) *100
        return '{}% variation..'.format(str(round(variation, 2)))
    else:
        return dash.no_update

# update existing input field depending on values of parameter dropdown menus

@app.callback(
    Output({'type': 'existing_input_dynamic','index': MATCH},'value'),
    Input({'type': 'ok_button_dynamic', 'index': MATCH},'n_clicks'),
    [State({'type': 'subdivisions_dynamic_menu','index': MATCH}, 'value'),
     State({'type': 'parameter_menu','index': MATCH}, 'value')]
,prevent_initial_call=True
)
def update_existing_input(n_clicks,subdivision,parameter):

    # read Params csv
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'Params.csv')
    df=pd.read_csv(my_file)

    # remove digits from subdivision selected from dropdown menu to be the same value of one in csv column ( 30101 Gamle Oslo -> Gamle Oslo )
    remove_digits = str.maketrans('', '', digits)
    subdivision_name = subdivision.translate(remove_digits)
    subdivision_name = subdivision_name[1:]

    # return the value of the corresponding parameter for the subdivison selected
    if parameter=='Population':
        return df[df['Origin'].str.contains(subdivision_name)]['OriPop19'].values[0]

    elif parameter=='Employment':
        return df[df['Destination'].str.contains(subdivision_name)]['DestEmp19'].values[0]

    elif parameter == 'Income':
        return df[df['Origin'].str.contains(subdivision_name)]['Inc19_x'].values[0]

    elif parameter == 'Urbanisation':
        return df[df['Origin'].str.contains(subdivision_name)]['Ourban'].values[0]

    elif parameter == 'Distance':
        return 1.0

    else:
        pass



# this callback is responsible for getting the results from IBM and stire it in json data ( dcc.Store() component )
# so that it can be used as a dataframes in tables and graphs on the simulated map and the other tabs

@app.callback([Output('results_msg','children'),Output('trips_df','data'),Output('parametrs_info','data'),Output('folium_df','data'),
               Output('full_trips_df','data')],
              Input('analyze_button','n_clicks'),
              [State({'type': 'subdivisions_dynamic_menu', 'index': ALL}, 'value'),
               State({'type': 'parameter_menu', 'index': ALL}, 'value'),
               State({'type': 'existing_input_dynamic','index': ALL}, 'value'),
               State({'type': 'revised_input_dynamic','index': ALL}, 'value'),
               State({'type': 'dynamic_variation_text','index': ALL},'children')
               ]
              ,prevent_initial_call=True)

def analyze(clicks,subdivision,parameter,existing_input,revised_input,variation):

    if  ( '' in revised_input )  or  ( '' in existing_input ) : # checking that input fields have no empty values
        raise PreventUpdate

    # remove digits from all selected subdivisions from dropdowns
    remove_digits = str.maketrans('', '', digits)
    i=0
    for subdiv in subdivision:
        subdivision[i]=subdivision[i].translate(remove_digits)
        subdivision[i] = subdivision[i][1:]
        i+=1


    input_values = []  # input values to be sent to ibm
    indices=[]         # used later to prevent duplicated rows
    final_df=pd.DataFrame() # the final df that will contain simulated trips from ibm

    # reading OsloFeb.csv file
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'OsloFeb.csv')

    dff=pd.read_csv(my_file)

    # this for loop loops through all parameters, subdivisions , revised_inputs chosen and get the corresponding input values in a suitable format to be sent to IBM

    for param, division , mod_input in zip(parameter, subdivision,revised_input):

        filt_df = dff[['Unnamed: 0','Day',"OrigCode", "DestCode", "Origin", "Destination",
                       "OPop", "DEmpl", "Ourban", "Durban", "OInc", "DInc", "Distance"]]


        if param == 'Distance':
            filt_df= filt_df[(filt_df['Origin'] == division) | (filt_df['Destination'] == division) ] # filtering the dataframe based on subdivision chosen
            trips_df=dff[(dff['Origin'] == division) | (dff['Destination'] == division) ]
            dff['sim_Distance'] = dff['Distance']  # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips

            # looping through the filtered dataframe
            for index, row in filt_df.iterrows():
                if index in indices: # checking if index is not repeated
                    continue
                row['Distance'] = row['Distance']*float(mod_input) # updating the value of chosen parameters with the value of modified input field
                dff.loc[index, 'sim_Distance'] = row['Distance']    # adding that modification in the original dataframe to be used later in tables and scatter plot
                input_values.append(list(row.values))         # appending the row values to input_values to be sent to IBM
                indices.append(index)                  # appending the current index value to indices list to keep checking for duplicates

        # same

        elif param == 'Population':
            filt_df=filt_df[filt_df['Origin']==division] # filtering the dataframe based on subdivision chosen
            trips_df=dff[dff['Origin']==division]
            dff['sim_OPop'] = dff['OPop']    # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                row['OPop'] = float(mod_input)
                dff.loc[index, 'sim_OPop'] = row['OPop']
                input_values.append(list(row.values))
                indices.append(index)

        # same

        elif param=='Employment':
            filt_df=filt_df[filt_df['Destination']==division]   # filtering the dataframe based on subdivision chosen
            trips_df=dff[dff['Destination']==division]
            dff['sim_DEmpl'] = dff['DEmpl']        # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                row['DEmpl'] = float(mod_input)
                dff.loc[index, 'sim_DEmpl'] = row['DEmpl']
                input_values.append(list(row.values))
                indices.append(index)

        # same but for both origin and destination values

        elif param=='Income':
            filt_df= filt_df[(filt_df['Origin'] == division) | (filt_df['Destination'] == division) ]  # filtering the dataframe based on subdivision chosen
            trips_df=dff[(dff['Origin'] == division) | (dff['Destination'] == division) ]
            dff['sim_OInc'] = dff['OInc']     # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips
            dff['sim_DInc'] = dff['DInc']     # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                if row['Origin']==division and row['Destination']==division:
                    row['OInc'] = float(mod_input)
                    row['DInc'] = float(mod_input)
                    dff.loc[index, 'sim_OInc'] = row['OInc']
                    dff.loc[index, 'sim_DInc'] = row['DInc']

                elif row['Origin']==division:
                    row['OInc'] = float(mod_input)
                    dff.loc[index, 'sim_OInc'] = row['OInc']

                elif row['Destination']==division:
                    row['DInc'] = float(mod_input)
                    dff.loc[index, 'sim_DInc'] = row['DInc']
                input_values.append(list(row.values))
                indices.append(index)


        # same but for both origin and destination values

        elif param == 'Urbanisation':
            filt_df= filt_df[(filt_df['Origin'] == division) | (filt_df['Destination'] == division) ]  # filtering the dataframe based on subdivision chosen
            trips_df=dff[(dff['Origin'] == division) | (dff['Destination'] == division) ]
            dff['sim_Ourban'] = dff['Ourban']     # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips
            dff['sim_Durban'] = dff['Durban']     # initializing simulated parameter ( will be updated with revised inputs ) column to be used in scatter plot simulated trips
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                if row['Origin'] == division and row['Destination'] == division:
                    row['Ourban'] = float(mod_input)
                    row['Durban'] = float(mod_input)
                    dff.loc[index, 'sim_Ourban'] = row['Ourban']
                    dff.loc[index, 'sim_Durban'] = row['Durban']

                elif row['Origin'] == division:
                    row['Ourban'] = float(mod_input)
                    dff.loc[index, 'sim_Ourban'] = row['Ourban']
                elif row['Destination'] == division:
                    row['Durban'] = float(mod_input)
                    dff.loc[index, 'sim_Durban'] = row['Durban']
                input_values.append(list(row.values))
                indices.append(index)


        else:
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update)

        final_df = final_df.append(trips_df,ignore_index=False)  # filling final_df with trips dataframe before modifed parametes update

    if final_df.empty:
        return (dash.no_update, dash.no_update,dash.no_update,dash.no_update,dash.no_update)

    final_df = final_df[~final_df.index.duplicated(keep='first')] # removing duplicates

   # print('input_values',input_values)
    #print(len(input_values))


    API_KEY = '5iLReM2ZZVXnVRMaAcSA4rfGnInWte72CgK0PcCLkyKY'
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                                       data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    payload_scoring = {"input_data": [{"fields": ['Unnamed: 0','Day', "OrigCode", "DestCode", "Origin", "Destination",
                                                      "OPop", "DEmpl", "Ourban", "Durban", "OInc",
                                                    "DInc","Distance"],
                                        "values": input_values
                                       }]}
    response_scoring = requests.post(
           'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/d2b6a51e-ee5f-43dc-bb2e-aa30995a530b/predictions?version=2022-01-20',
           json=payload_scoring, headers=header)
    #print("Scoring response")
  #  print(response_scoring.json())
    results=response_scoring.json()
    results=results['predictions'][0]['values']
    final_results=[]
    for trip in results:
        final_results.append(trip[0])  # ( converting results from [ [2] , [3] ] shape to [ 2 , 3 ] ) to be used in updating final_df trips
    final_df['Simulated_Trips']=final_results # updating final_df Simulated_Trips
    mod_trips_df=dff
    mod_trips_df['Simulated_Trips']=mod_trips_df['Trips']
    mod_trips_df.loc[final_df.index,'Simulated_Trips']=final_df['Simulated_Trips'] # filling the original dataframe with updates in Simulated_Trips values
    parameters_data = {'Parameters':parameter , 'SubDivision': subdivision, 'Exisiting_Value': existing_input, # creating parameters dataframe from parameters components values
                       'Modified_Value': revised_input, 'Variation': variation }
    mod_trips_df['Simulated_Trips']=mod_trips_df['Simulated_Trips'].astype('int64')
    parameters_df = pd.DataFrame(parameters_data)
    folium_df=mod_trips_df.groupby(['Day','OrigCode','DestCode','Origin','Destination'],sort=True)['Trips','Simulated_Trips'].mean().reset_index() # creating a folium dataframe ( in the shape suitable for folium map )
    mod_trips_df2=mod_trips_df[['Day','OrigCode','DestCode',"Origin", "Destination",'Trips','Simulated_Trips']] # creating  a datafrane for tAbles that contains only the columns needed
    mod_trips_df2['Simulated_Trips']=mod_trips_df2['Simulated_Trips'].astype('int64')

    return ('Analysis Done',mod_trips_df2.to_dict('records'),parameters_df.to_dict('records'),folium_df.to_dict('records'),  # returning all thes dataframe to its relevant dcc.Store component to be used later
            mod_trips_df.to_dict('records'))




### note that the part of setting the width and spacing of maps bellow is a bit comblicated and worked after a lot of testing so it is not a concept to be illustrated its just trial and error until the right results is obtained
### the idea is in storing current maps type in dcc.Store component and updating the width and spacing according to that every time ok button is pressed


# setting the spacing of folium map when it loads depending on the second map type

@app.callback(Output('iframe_div', 'style'),
             [Input('map2_div', 'children')],
              [State('sim_dropdown','value'),State('chosen_map','value'),State('map2_type','data'),
               State('map1_type','data'),State('trips_df','data')]
    # ,prevent_initial_call=True
        )
def iframe_spacing(map2_loaded,type,chosen_map,map2_type,map1_type,map2_data):
    map2_df=pd.DataFrame(map2_data)
    if map1_type == 'network' and map2_type == 'flow':
        return dict(width='43%',height='60vh',position='absolute')

    elif map1_type == 'network' and map2_type == 'network':
        if map2_df.empty:
            return dict(width='43%',height='60vh',position='absolute')
        else:
            return dict(width='41%',height='60vh',position='absolute')

    else:
        return dash.no_update


# updating map1 depending on type of visualization ( plotly map of folium iframe )


@app.callback([Output('map1_div', 'children'),Output('map1_type','data'),Output('map2_type','data'),Output('map1_div', 'style')],
             [Input('ok_button', 'n_clicks'),Input('trips_df','data')],[State('sim_dropdown','value'),State('chosen_map','value'),State('map2_type','data'),State('map1_type','data')]
    # ,prevent_initial_call=True
        )
def update_map1(clicks,analyze_pressed,type,chosen_map,map2_type,map1_type):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'Params.csv')
    print(type,map1_type,map2_type)
    df=pd.read_csv(my_file)

    if ('Map1' not in chosen_map) and ( 'Map2' not in chosen_map ) and (input_id!='trips_df') :
        raise PreventUpdate


    if ( 'Map1' not in chosen_map ) and (input_id!='trips_df') :

        if type == 'Flows':
            if map1_type=='network':
                return (dash.no_update, dash.no_update,'flow',dash.no_update)
            else :
                return (dash.no_update, dash.no_update,'flow',{})

        elif type == 'Network':

            if map1_type=='network':

                return (dash.no_update, dash.no_update,'network',dash.no_update)
            else :

                return (dash.no_update, dash.no_update,'network',{'width':'103%'})


    if input_id =='trips_df':
        return (dash.no_update, dash.no_update,dash.no_update, dash.no_update)

    if type == 'Flows':
        if ( 'Map1' in chosen_map ) and ( 'Map2' in chosen_map ) :

            return ( dcc.Graph(id='map1', config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=Functions.create_combined_map(df,[])
              ),'flow','flow',{})

        if map2_type=='network':

            return ( dcc.Graph(id='map1', config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=Functions.create_combined_map(df,[])
              ) ,'flow',dash.no_update,{'width':'103%'})

        else:
            return (dcc.Graph(id='map1', config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=Functions.create_combined_map(df,[])
              ) ,'flow',dash.no_update,{})



    elif type == 'Network':
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'map.html')

        if ( 'Map1' in chosen_map ) and ( 'Map2' in chosen_map ) :

            return ( html.Div(html.Iframe(srcDoc = open(my_file, 'r').read()
           ,style=dict(width='100%',height='60vh',position='absolute') ,id='iframe'
            ) ,style=dict(width='41%'),id='iframe_div'),'network','network',{'width':'41%'})

        if map2_type=='network':

            return ( html.Div(html.Iframe(srcDoc = open(my_file, 'r').read()
           ,style=dict(width='100%',height='60vh',position='absolute') ,id='iframe'
            ) ,style=dict(width='41%'),id='iframe_div'),'network',dash.no_update,{'width':'41%'})

        else:

            return ( html.Div(html.Iframe(srcDoc = open(my_file, 'r').read()
           ,style=dict(width='100%',height='60vh',position='absolute') ,id='iframe'
            ),style=dict(width='43%') ,id='iframe_div'), 'network',dash.no_update,{'width':'43%'})

# updating map2 depending on type of visualization ( plotly map of folium iframe )

@app.callback(Output('map2_div', 'children'),
             [Input('trips_df','data'),Input('ok_button', 'n_clicks')],
              [State('sim_dropdown','value'),State('trips_df','data'),State('folium_df','data')
              ,State('parametrs_info','data'),State('chosen_map','value')]

       #       ,prevent_initial_call=True
        )
def update_map2(analyze_pressed,clicks,type,trips,folium_data,parameters,chosen_map):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'Params.csv')
    df=pd.read_csv(my_file)
    trips_df=pd.DataFrame(trips)
    folium_df=pd.DataFrame(folium_data)

    if ('Map1' not in chosen_map) and ( 'Map2' not in chosen_map ) and (input_id!='trips_df') :
        raise PreventUpdate

    if (trips_df.empty or folium_df.empty or 'Map2' not in chosen_map) and (input_id!='trips_df'):
        return dash.no_update

    trips_df['Simulated_Trips']=trips_df['Simulated_Trips'].astype('int64')
    folium_df['Simulated_Trips'] = folium_df['Simulated_Trips'].astype('int64')
    df['Trips']=trips_df['Simulated_Trips']

    if type == 'Flows':
        param_df=pd.DataFrame(parameters)
        divsions=param_df['SubDivision'].to_list()
        return  html.Div( dcc.Graph(id='map2', config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=Functions.create_combined_map(df,divsions)
              )
              )

    elif type == 'Network':
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'map.html')

        return html.Iframe(srcDoc=open(my_file, 'r').read()
                       , style=dict(width='77vh', height='60vh')
                       )

    else:
        return dash.no_update






# updating map1 background style

@app.callback(Output('map1', 'figure'),
             Input('ok_button', 'n_clicks'),
             [State('map1', 'figure'),State('chosen_map','value'),State('map_style_dropdown', 'value')]
        )
def map1_style(clicks,fig1,chosen_map,style):
    if 'Map1' not in chosen_map:
        return dash.no_update
    fig1['layout']['mapbox']['style'] = style
    return fig1

# updating map2 background style

@app.callback(Output('map2', 'figure'),
             Input('ok_button', 'n_clicks'),
             [State('map2', 'figure'),State('chosen_map','value'),State('map_style_dropdown', 'value')]
        )
def map2_style(clicks,fig2,chosen_map,style):
    if 'Map2' not in chosen_map:
        return dash.no_update
    fig2['layout']['mapbox']['style']=style
    return fig2

# download the table data to csv upon pressing on download_csv button by using dash Download component

@app.callback(Output('csv_download_data2', 'data'),
              Input('download_csv2', 'n_clicks'),State('trips_df','data')

    ,prevent_initial_call=True)
def download_trips_csv(clicks,data):
    trips_df=pd.DataFrame(data)
    return send_data_frame(trips_df.to_csv, "Trips.csv")

@app.callback(Output('csv_download_data1', 'data'),
              Input('download_csv1', 'n_clicks'),State('parametrs_info','data')

    ,prevent_initial_call=True)
def download_parameters_csv(clicks,data):
    parameters_df=pd.DataFrame(data)
    return send_data_frame(parameters_df.to_csv, "Parameters.csv")


if __name__ == '__main__':
    app.run_server(host='localhost',port=8500,debug=False)
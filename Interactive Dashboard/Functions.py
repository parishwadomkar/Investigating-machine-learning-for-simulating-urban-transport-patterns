import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

def create_line_map1(df):
    hov_text = []
    for ind in df.index:
        hov_text.append('Origin : {}<br>Destination : {}<br>Trips : {}<br>Population : {}'.format(df['Origin'][ind],
                                                                                                  df['Destination'][
                                                                                                      ind],
                                                                                                  df['Trips'][ind],
                                                                                                  df['OriPop19'][ind]))
    df['hover'] = hov_text

    fig = go.Figure()

    name_arr = []
    for i in range(len(df)):
        if df['Origin'][i] == df['Destination'][i]:
            continue

        current_dist = df['Destination'][i]
        current_origin = df['Origin'][i]
        trips = df['Trips'][i]
        trips_reversed = df[(df['Origin'] == current_dist) & (df['Destination'] == current_origin)]['Trips'].values[0]
        total_trips = trips + trips_reversed

        if total_trips > 15000:
            color = 'red'
            name = '> 15000 Trips'

        elif total_trips <= 15000:
            color = 'black'
            name = '<= 15000 Trips'

        legend = True
        if name in name_arr:
            legend = False
        else:
            legend = True

        fig.add_trace(go.Scattermapbox(name=name, showlegend=legend,
                                       lon=[df['lon-origin'][i], df['lon-dist'][i]],
                                       lat=[df['lat-origin'][i], df['lat-dist'][i]],
                                       mode='lines',
                                       marker={'color': color, 'size': 10, 'allowoverlap': True, 'opacity': 0.1},
                                       # unselected={'marker': {'opacity': 1}},
                                       # selected={'marker': {'opacity': 0.5, 'size': 15}},
                                       hoverinfo='text',
                                       hovertext=['Subdivision : {}<br>Population : {}'.format(df['Origin'][i],
                                                                                               df['OriPop19'][i]),
                                                  'Subdivision : {}<br>Population : {}'.format(df['Destination'][i],
                                                                                               df['OriPop19'][i])],
                                       customdata=[df['Origin'][i], df['Destination'][i]]
                                       )
                      )
        name_arr.append(name)

    fig.update_layout(
        uirevision='foo',  # preserves state of figure/map after callback activated
        clickmode='event+select',
        hovermode='closest',
        hoverdistance=2,
        mapbox=dict(
            #      bearing=25,
            style='light',
            center=dict(
                lon=10.7347673396536,
                lat=59.8992367
            ),
            #   pitch=40,
            zoom=10
        ), margin=dict(l=0, r=0, t=30, b=0), hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell")
    )
    fig.update_layout(mapbox_style='open-street-map')
    return fig

def create_size_map1(df):
    dist_df = df.groupby(['Destination', 'lon-dist', 'lat-dist'])['Trips'].sum()
    dist_df = dist_df.reset_index()
    org_df = df.groupby(['Origin', 'lon-origin', 'lat-origin'])['Trips'].sum()
    org_df = org_df.reset_index()
    inter_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['Origin'] == row['Destination']:
            inter_df = inter_df.append(row[['Origin', 'Destination', 'Trips']], ignore_index=True)

    inter_df = inter_df.sort_values('Origin', ignore_index=True)
    dist_df['dest._Trips'] = dist_df['Trips'] - inter_df['Trips']
    dist_df['orig._Trips'] = org_df['Trips'] - inter_df['Trips']
    dist_df['inter._Trips'] = inter_df['Trips']
    dist_df['Trips_Total'] = dist_df['dest._Trips'] + dist_df['orig._Trips'] + dist_df['inter._Trips']
    dist_df = dist_df.astype({"dest._Trips": int, "orig._Trips": int, "inter._Trips": int, "Trips_Total": int})

    hov_text = []
    for ind in dist_df.index:
        hov_text.append(
            'Subdivision : {}<br>Incoming Trips : {}<br>Outgoing Trips : {}<br>Intra.Trips : {}<br>Total Trips : {}'.format(
                dist_df['Destination'][ind], dist_df['orig._Trips'][ind],
                dist_df['dest._Trips'][ind], dist_df['inter._Trips'][ind], dist_df['Trips_Total'][ind]))

    dist_df['hover'] = hov_text

    fig2 = go.Figure(go.Scattermapbox(lat=dist_df['lat-dist'], lon=dist_df['lon-dist'],below="\"\"\"",
                                      marker=dict(
                                          size=dist_df['Trips_Total'] / 1000,
                                          color='rgb(0,0,255)',
                                          sizemode='area'
                                      ),
                                      hoverinfo='text', hovertemplate=dist_df['hover'], customdata=dist_df['hover']))

    fig2.update_layout(mapbox_style='open-street-map', mapbox_center_lon=10.7347673396536, mapbox_center_lat=59.8992367,
                       mapbox_zoom=10)
    fig2.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, hoverdistance=2, uirevision='foo',
                       clickmode='event+select', hovermode='closest')
    return fig2

def create_combined_map(df,divisions):
    lons = []
    lats = []
    df2=df[df['Origin']!=df['Destination']]
    lons = np.empty(3 * len(df2))
    lons[::3] = df2['lon-origin']
    lons[1::3] = df2['lon-dist']
    lons[2::3] = None
    lats = np.empty(3 * len(df2))
    lats[::3] = df2['lat-origin']
    lats[1::3] = df2['lat-dist']
    lats[2::3] = None
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
            lon=lons,
            lat=lats,
            mode='lines',
            marker={'color': 'rgb(0,0,255)', 'size': 10, 'allowoverlap': True,'opacity':0.1,},
           # unselected={'marker': {'opacity': 1}},
           # selected={'marker': {'opacity': 0.5, 'size': 15}},
            hoverinfo='skip',
         #   hovertext=['Subdivision : {}<br>Population : {}'.format(df['Origin'][i], df['OriPop19'][i]),
              #         'Subdivision : {}<br>Population : {}'.format(df['Destination'][i], df['OriPop19'][i])],
         #   customdata=[df['Origin'][i], df['Destination'][i]]
        )
        )

    fig.update_layout(
        uirevision='foo',  # preserves state of figure/map after callback activated
        clickmode='event+select',
        hovermode='closest',
        hoverdistance=2,
        mapbox=dict(
         #   bearing=25,
            style='light',
            center=dict(
                lon=10.7658488126624,
                lat=59.93827295
            ),
          #  pitch=40,
            zoom=9.7
        ), showlegend=False, margin=dict(l=0, r=0, t=0, b=0) ,hoverlabel=dict(
        font_size=16,
        font_family="Rockwell")
    )
    fig.update_layout(mapbox_style='open-street-map')

    dist_df = df.groupby(['Destination', 'lon-dist', 'lat-dist','color'])['Trips'].sum()
    dist_df = dist_df.reset_index()
    org_df = df.groupby(['Origin', 'lon-origin', 'lat-origin'])['Trips'].sum()
    org_df = org_df.reset_index()
    inter_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['Origin'] == row['Destination']:
            inter_df = inter_df.append(row[['Origin', 'Destination', 'Trips']], ignore_index=True)

    inter_df = inter_df.sort_values('Origin', ignore_index=True)
    dist_df['dest._Trips'] = dist_df['Trips'] - inter_df['Trips']
    dist_df['orig._Trips'] = org_df['Trips'] - inter_df['Trips']
    dist_df['inter._Trips'] = inter_df['Trips']
    dist_df['Trips_Total'] = dist_df['dest._Trips'] + dist_df['orig._Trips'] + dist_df['inter._Trips']
    dist_df = dist_df.astype({"dest._Trips": int, "orig._Trips": int, "inter._Trips": int, "Trips_Total": int})

    hov_text = []
    for ind in dist_df.index:
        hov_text.append(
            'Subdivision : {}<br>Incoming Trips : {}<br>Outgoing Trips : {}<br>Intra.Trips : {}<br>Total Trips : {}'.format(
                dist_df['Destination'][ind], dist_df['orig._Trips'][ind],
                dist_df['dest._Trips'][ind], dist_df['inter._Trips'][ind], dist_df['Trips_Total'][ind]))

    dist_df['hover2'] = hov_text

    if divisions != []:
        indices = dist_df[dist_df['Destination'].isin(divisions)]['color'].index
        dist_df['color'].loc[indices] = 'lightsalmon'

    fig.add_trace(go.Scattermapbox(lat=dist_df['lat-dist'], lon=dist_df['lon-dist'],name='Info' ,
                                      marker=dict(
                                          size=dist_df['Trips_Total'] / 500,
                                          color=dist_df['color'],
                                          sizemode='area',opacity=1
                                      ),
                                      hoverinfo='text', hovertemplate=dist_df['hover2'], customdata=dist_df['hover2']))


    return fig

def create_params_scatter(df,param,day):
    df['Simulated_Trips'] = df['Simulated_Trips'].astype('int64')
    df=df[ df['Day']==day ]
    hov_text = []
    for ind in df.index:
        hov_text.append(
            'Origin : {}<br>Destination : {}<br>Parameter Value : {}<br>Trips : {}<br>Simulated Trips : {}'.format(
                df['Origin'][ind], df['Destination'][ind],
                df[param][ind], df['Trips'][ind], df['Simulated_Trips'][ind]))
    df['hover'] = hov_text
    xaxis=df['{}'.format(param)]
    text=df['hover']
    if 'sim_{}'.format(param ) in df.columns:
        xaxis=df['sim_{}'.format(param ) ]
        hov_text2=[]
        for ind in df.index:
            hov_text2.append(
            'Origin : {}<br>Destination : {}<br>Exis.Parameter Value : {}<br>Mod.Parameter Value : {}<br>Trips : {}<br>Simulated Trips : {}'.format(
                df['Origin'][ind], df['Destination'][ind],df[param][ind],
                df['sim_{}'.format(param )][ind], df['Trips'][ind], df['Simulated_Trips'][ind]))
        text=hov_text2

    x1 = df[param].values.reshape(-1, 1)
    y1 = df['Trips']
    poly_f1 = PolynomialFeatures(1)
    x_poly1 = poly_f1.fit_transform(x1)
    lin_reg1 = LinearRegression()
    lin_reg1.fit(x_poly1, y1)
    df['model1'] = lin_reg1.predict(x_poly1)

    x2 = xaxis.values.reshape(-1, 1)
    y2 = df['Simulated_Trips']
    poly_f2 = PolynomialFeatures(1)
    x_poly2 = poly_f2.fit_transform(x2)
    lin_reg2 = LinearRegression()
    lin_reg2.fit(x_poly2, y2)
    df['model2'] = lin_reg2.predict(x_poly2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xaxis, y=df['Simulated_Trips'], mode='markers', name='Simulated Trips',
                             marker_color='lightsalmon',
                             hoverinfo='text', hovertext=text))

    fig.add_trace(go.Scatter(x=df[param], y=df['Trips'], mode='markers', name='Actual Trips', marker_color='#0097A9',
                             hoverinfo='text', hovertext=df['hover']))

    fig.add_trace(go.Scatter(x=xaxis, y=df['model2'], mode='lines', showlegend=False, marker_color='lightsalmon'))
    fig.add_trace(go.Scatter(x=df[param], y=df['model1'], mode='lines', showlegend=False, marker_color='#0097A9'))

    fig.update_layout(
        go.Layout(title='Parameter vs actual and simulated trips of {}'.format(day), xaxis_title='Parameter', yaxis_title='Number of Trips',
                  font=dict(size=14, family='bold'), template='ggplot2', hoverlabel=dict(
                font_size=16, font_family="Rockwell"
            )))
    return fig
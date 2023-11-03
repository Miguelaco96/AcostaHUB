# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 12:05:36 2023

@author: MIGUEL ACOSTA PERDOMO
"""

import dash
from dash import dcc, html,callback, Output, Input
import pandas as pd
import plotly.express as px
from items_disponibles import items_abalible
import plotly.graph_objs as go
from funcions import divs_data,search_cik,search_ticker,cash_flow_data, earn_data, ebit_data, history_data, ticker_selector
import dash_bootstrap_components as dbc
from css_py import style_Border_divs


df_names = pd.read_csv('SPNasdaq.csv')


headers = {"User-Agent": "FinhubAcosta@gmail.com"}

period =["1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]
interval =["1d","5d","1wk","1mo","3mo"]
# Crear la aplicación Dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Diseño del formulario
app.layout = html.Div([
    
    html.Div(html.Img(src="/assets/img3.png", style={"justify-items": "center", 'height': '300px'}), style={'display': 'flex', "justify-content": 'center'}),
           
    
    dcc.Dropdown(df_names["Name"],"Apple Inc",id="name", className="p-3 m-3",style={
        
        "color": "299eff", "font-family":"Georgia","left-padding":"1rem"}),
    
   
    
    html.Div([
      
        html.Div([
                  
                dcc.Dropdown(
                id='period_item',
                options= period,
                value="1y", className="p-2"
                ),
                 
                
                dcc.Dropdown(
                id='interval_item',
                options= interval,
                value="1d", className="p-2"
                )
                ]
            
        ,className="d-flex  p-2"),  
        
        
        
             
        dcc.Graph(id='Hist-chart', className="3-p"),
        
        
                 
                
        ],style = style_Border_divs ,className="p-3 m-3"),
    
    
    
    html.Div(html.Div(
       
         html.Div([
                   
         html.Div(dcc.Graph(id='Cash-bar'),className="col-md-5 col-ms-12",style = style_Border_divs),
         html.Div(dcc.Graph(id='earn-bar'),className="col-md-5 col-ms-12",style = style_Border_divs),
         html.Div(dcc.Graph(id="ebit-bar"),className="col-md-5 col-ms-12",style = style_Border_divs),
         html.Div(dcc.Graph(id="divs-bar"),className="col-md-5 col-ms-12",style = style_Border_divs)
         
         
         ],className="row", style={"grid-gap": "10px", "justify-content": "center","margin-top":"1rem"}         
                 
         )
        )
        ),
    
    #div general de graficos
    html.Div([
        
      #Primera fila  
     
            
        html.Div([
          dcc.Dropdown(
           id='item_selector1',
           options= items_abalible,
           value="Assets",
           className="p-1"),dcc.Graph(id='bar-chart')], style=style_Border_divs,className="col-md-5 col-sm-12 p-3"),           
   
        html.Div([
           dcc.Dropdown(
           id='item_selector2',
           options=items_abalible,
    
           value="Revenues",className="p-1"), dcc.Graph(id='bar-chart2')], style=style_Border_divs,className="col-md-5 col-sm-12 p-3"),
       
                        
    
         html.Div([ 
          dcc.Dropdown(
             id='item_selector3',
             options=items_abalible,
             value="GrossProfit",
             className="p-1"),
         dcc.Graph(id='bar-chart3')], style=style_Border_divs,className="col-md-5 col-sm-12 p-3"),
     
     
     
         html.Div([
         dcc.Dropdown(
             id='item_selector4',
             options=items_abalible,  
             value="EarningsPerShareDiluted",            
             className="p-1"),dcc.Graph(id='bar-chart4')],style=style_Border_divs,className="col-md-5 col-sm-12 p-3")
     
     
     ],className = "row" ,style={"grid-gap": "10px", "justify-content": "center","margin-top":"1rem"})  ,    
     
    html.Footer(" MIGUEL ACOSTA PERDOMO © 2023. Todos los derechos reservados.", className="footer", style = {"background":"grey", "padding":"1rem", "text-align": "center","margin-top":"1rem"})
    ],style={"background": "linear-gradient(90deg, rgba(255,255,238,0.9164040616246498) 0%, rgba(220,239,249,1) 90%, rgba(220,239,249,1) 90%)"})


@callback(
    Output('Hist-chart', 'figure'),
    Input("name","value"),
    Input("period_item", "value"),
    Input("interval_item", "value"))
    
def update_historial(name,period_item,interval_item):
                
    try:
                
        # Generar el DataFrame con los datos financieros
        
        df = history_data(ticker_selector(name,df_names),period_item, interval_item)
                     
        # Crear el gráfico de barras
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])
                      ])
        fig.update_layout(
           title='Price History Charts',
           yaxis_title=name)
                
        return fig
    
    except:
       
        return go.Figure()

@callback(
    Output('Cash-bar', 'figure'),
    Input("name","value"))
    
 
def cash_flow_update(name):
    
        try:
            
           dft = cash_flow_data(ticker_selector(name,df_names))
            
           x_axis=dft.index.tolist()
           
           fig = go.Figure()


           fig.add_trace(go.Bar(
               x=x_axis,
               
               
               y=dft["Operating Cash Flow"].tolist(),
               name="Operating Cash Flow",
               marker_color='#ADD8E6',
               text= dft["Operating Cash Flow"].tolist()
           ))


           fig.add_trace(go.Bar(
               x=x_axis,
               y=dft["Financing Cash Flow"].tolist(),
               name='Financing Cash Flow',
               marker_color='#4682B4',
               text= dft["Financing Cash Flow"].tolist()
           ))
           
           fig.add_trace(go.Bar(
               x=x_axis,
               y=dft["Free Cash Flow"].tolist(),
               name="Free Cash Flow",
               marker_color='#000080',
               text= dft["Free Cash Flow"].tolist()
           ))
           
           fig.add_trace(go.Bar(
               x=x_axis,
               y=dft["Investing Cash Flow"].tolist(),
               name="Investing Cash Flow",
               marker_color='#000033',
               text= dft["Investing Cash Flow"].tolist()
           ))
           fig.update_layout(title='Cash Flow',barmode='group', xaxis_tickangle=-45)
          


           
           return fig
        except:
            # Manejar la excepción si el DataFrame está vacío
           
            return go.Figure() 
        


@callback(
    Output('earn-bar', 'figure'),
    Input("name","value"))
    
 
def earn_update(name):
    
        try:
            
           earn = earn_data(ticker_selector(name,df_names))
           
           x_axis =earn.index.tolist()
           
           fig = go.Figure()

           fig.add_trace(go.Bar(
               x=x_axis,                            
               y=earn["EPS Estimate"].tolist(),
               name="EPS Estimate",
               marker_color='#90EE90',
               text= earn["EPS Estimate"].tolist()
           ))


           fig.add_trace(go.Bar(
               x=x_axis,
               y=earn["Reported EPS"].tolist(),
               name='Reported EPS',
               marker_color='#008000',
               text= earn["Reported EPS"].tolist()
           ))
           
          
           fig.update_layout(title='Earnings per share',barmode='group')
               
           return fig
        except:
            # Manejar la excepción si el DataFrame está vacío
           
            return go.Figure() 


@callback(
    Output('divs-bar', 'figure'),
    Input("name","value"))
    
 
def div_update(name):
                  
        
           try:
               
              div = divs_data(ticker_selector(name,df_names))
             
              x_axis = div.index.tolist()
                         
              fig = go.Figure()

              fig.add_trace(go.Bar(
                  x=x_axis,                            
                  y=div.tolist(),
                  name="Dividendos",
                  text=div.tolist(),
                  marker_color='#F2E351',
                  
              ))
             
              fig.update_layout(title='Dividends')
   
              return fig
           except:
               # Manejar la excepción si el DataFrame está vacío
              
               return go.Figure() 

                
@callback(
    
    Output('ebit-bar', 'figure'),
    Input("name","value"))
    
 
def ebit_update(name):
    
        try:
            
           ebit = ebit_data(ticker_selector(name,df_names))
          
           x_axis = ebit.index.tolist()
                      
           fig = go.Figure()

           fig.add_trace(go.Bar(
               x=x_axis,                            
               y=ebit["EBITDA"],
               name="EBITDA",
               marker_color='#D8BFD8',
               text= ebit["EBITDA"].tolist()
           ))


           fig.add_trace(go.Bar(
               x=x_axis,
               y=ebit["EBIT"],
               name="EBIT",
               marker_color='#9370DB',
               text= ebit["EBIT"].tolist()
           ))
           fig.add_trace(go.Bar(
               x=x_axis,
               y=ebit["Normalized EBITDA"],
               name="Normalized EBITDA",
               marker_color='#6A5ACD',
               text= ebit["Normalized EBITDA"].tolist()
           ))
          
           fig.update_layout(title='EBITDA',barmode='group')
          


           
           return fig
        except:
            # Manejar la excepción si el DataFrame está vacío
           
            return go.Figure() 


@callback(
    Output('bar-chart', 'figure'),
    Input("name","value"),
    Input('item_selector1', 'value'))
    
def update_bar_chart_1(name,item_selector1):
                
    try:
        # Generar el DataFrame con los datos financieros
        df = search_ticker(search_cik(name, df_names), item_selector1, headers)
                     
        # Crear el gráfico de barras
        fig = px.bar(df, x='frame', y='val')
        
        fig.update_layout(
           title='',
           xaxis_title="",
           yaxis_title="")
       
        return fig
    
    except ValueError:
       
        return go.Figure()

@callback(
    Output('bar-chart2', 'figure'),
    Input("name","value"),
    Input('item_selector2', 'value'))    

def update_bar_chart_2(name, item_selector2):
    
        try:
            # Generar el DataFrame con los datos financieros
            df = search_ticker(search_cik(name, df_names), item_selector2, headers)
                            
            # Crear el gráfico de barras
            fig = px.bar(df, x='frame', y='val')
            fig.update_layout(
               title='',
               xaxis_title="",
               yaxis_title="")
            
            return fig
        
        except ValueError:
            # Manejar la excepción si el DataFrame está vacío
           
            return go.Figure()
 
@callback(
    Output('bar-chart3', 'figure'),
    Input("name","value"),
    Input('item_selector3', 'value'))
    
    
def update_bar_chart_3(name,item_selector3):
                
    try:
        # Generar el DataFrame con los datos financieros
        df = search_ticker(search_cik(name, df_names), item_selector3, headers)
      
        # Crear el gráfico de barras
        fig = px.bar(df, x='frame', y='val')
        fig.update_layout(
           title='',
           xaxis_title="",
           yaxis_title="")
     
        return fig
    
    except ValueError:
      
        return go.Figure()

@callback(
    Output('bar-chart4', 'figure'),
    Input("name","value"),
    Input('item_selector4', 'value'))
 
def update_bar_chart_4(name, item_selector4):
    
        try:
            # Generar el DataFrame con los datos financieros
            df = search_ticker(search_cik(name, df_names), item_selector4, headers)
               
            # Crear el gráfico de barras
            fig = px.bar(df, x='frame', y='val')
            fig.update_layout(
               title='',
               xaxis_title="",
               yaxis_title="")
           
            return fig
        except ValueError:
            # Manejar la excepción si el DataFrame está vacío
           
            return go.Figure()   

if __name__ == '__main__':
    app.run_server(debug=True)
    
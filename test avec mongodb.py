import dash
from dash import Dash,html, dcc, Input, Output , State , dash_table
import pandas as pd
import plotly.express as px
import pymongo
from bson.objectid import ObjectId
import dash_bootstrap_components as dbc

#incorporate data into app
client = pymongo.MongoClient("mongodb+srv://sam:rfid@cluster0.dt27d.mongodb.net/?retryWrites=true&w=majority")
df = client["GestionDeProjet"]
collection = df["acquisition"]
df = pd.DataFrame(list(collection.find()))
df['_id']= df['_id'].astype(str)
print(df.head())
#Component build
app =Dash(__name__,external_stylesheets=[dbc.themes.COSMO])
app.title='Stats project v2 '
mytitle = dcc.Markdown(children='')
mygraph=dcc.Graph(figure={})
dropdown=dcc.Dropdown(options=df.columns.values[2:],
                        value='temperaure',
                        clearable=False)



#layout
app.layout=dbc.Container([
    dbc.Row([ dbc.Col([mytitle],width=6)] ,justify='center'),
    dbc.Row([dbc.Col([mygraph],width=12)]),
    dbc.Row([ dbc.Col([dropdown],width=6) ],justify='center'),    
    ],
    fluid=True)

#callback for interactivity
@app.callback(
    Output(mygraph, component_property='figure'),
    Output(mytitle,component_property='children'),
    Input(dropdown, component_property='value')
)

def update_graph(column_name):
    print(column_name)
    print(type(column_name))
    if column_name == 'temperaure':
        fig = px.bar(df, x='aquisition', y='temperaure')
        return fig , '# '+column_name
    else:
        fig = px.bar(df, x='aquisition', y='résistivité')
        return fig , '# '+column_name

    #fig=px.pie(data_frame=df,values='temperaure',names='résistivité')
    # return fig , '# '+column_name


#run app
if __name__ == '__main__':
    app.run_server(debug=True,port=8051)
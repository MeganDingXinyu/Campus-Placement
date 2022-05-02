from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('Placement_Data_Full_Class.csv')
df['id'] = df['sl_no']
df = df.fillna(0)

df.set_index('id', inplace=True, drop=False)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Campus Placement Dashboard', style={'textAlign': 'center','color': 'blue','fontSize': 30}),
    html.Div('Individual MA705 Project  Xinyu Ding ', style={'color': 'black', 'fontSize': 25, 'marginBottom': 50,
                             'marginTop': 25, 'margin-right': 800}),
    html.P('what is this dashboard about?', className='my-class', id='my-p-element'),
    html.Div([
       dcc.Markdown("""
                   
The dashboard summarizes the information of Campus placement or campus recruiting. 
This dataset consists of placement data of students in a certain campus. 
It includes secondary and higher secondary school percentage and specialization.
Users can query the ratio of male and female students by education, work experience and salary.

       """),
   ]),
    dash_table.DataTable(
        id='datatable-row-ids',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-row-ids-container')
])

@app.callback(
    Output('datatable-row-ids-container', 'children'),
    Input('datatable-row-ids', 'derived_virtual_row_ids'),
    Input('datatable-row-ids', 'selected_row_ids'),
    Input('datatable-row-ids', 'active_cell'))
def update_graphs(row_ids, selected_row_ids, active_cell):
    selected_id_set = set(selected_row_ids or [])

    if row_ids is None:
        dff = df
        row_ids = df['id']
    else:
        dff = df.loc[row_ids]

    active_row_id = active_cell['row_id'] if active_cell else None

    colors = ['#FF69B4' if id == active_row_id
              else '#7FDBFF' if id in selected_id_set
              else '#0074D9'
              for id in row_ids]

    return [
        dcc.Graph(
                id=column + '--row-ids',
                figure={
                    'data': [
                        {
                            'x': ['M', 'F'],
                            'y': dff[column].value_counts(),
                            'type': 'bar',
                            'marker': {'color': colors},
                        }
                    ],
                    'layout': {
                        'xaxis': {'automargin': True},
                        'yaxis': {
                            'automargin': True,
                            'title': {'text': column}
                        },
                        'height': 250,
                        'margin': {'t': 10, 'l': 10, 'r': 10},
                    },
                },
        ) for column in ['gender'] if column in dff]

if __name__ == '__main__':
    app.run_server(debug=True)
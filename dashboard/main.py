"""Run with: bokeh serve dashboard --show"""
import csv
from datetime import datetime
from pathlib import Path
from math import nan
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Div, HoverTool, Select
from bokeh.plotting import figure

summary = Path(__file__).resolve().parents[1] / 'data/monthly_response_times.csv'
if not summary.exists():
    raise RuntimeError('Run preprocess_response_times.py first; see README.md.')
with summary.open(newline='') as f:
    rows = list(csv.DictReader(f))
months = sorted({r['month'] for r in rows})
zipcodes = sorted({r['zipcode'] for r in rows} - {'ALL'})
if not zipcodes:
    raise RuntimeError('No eligible ZIP codes in the summary.')
lookup = {(r['zipcode'], r['month']): r for r in rows}
dates = [datetime.strptime(m, '%Y-%m') for m in months]


def series(area):
    return dict(date=dates, month=months,
                hours=[float(lookup[(area, m)]['average_hours']) if (area, m) in lookup else nan for m in months],
                count=[int(lookup[(area, m)]['count']) if (area, m) in lookup else 0 for m in months],
                area=[area] * len(months))


first = '10001' if '10001' in zipcodes else zipcodes[0]
second = '10472' if '10472' in zipcodes else zipcodes[min(1, len(zipcodes)-1)]
select1 = Select(title='ZIP code 1', value=first, options=zipcodes)
select2 = Select(title='ZIP code 2', value=second, options=zipcodes)
city_source = ColumnDataSource(series('ALL'))
source1 = ColumnDataSource(series(first))
source2 = ColumnDataSource(series(second))
plot = figure(title='Average time from complaint creation to closure', x_axis_type='datetime',
              height=460, sizing_mode='stretch_width', tools='pan,wheel_zoom,box_zoom,reset,save',
              x_axis_label='Closure month', y_axis_label='Average closure time (hours)')
plot.y_range.start = 0
cityline = plot.line('date', 'hours', source=city_source, color='#64748b', line_width=3, legend_label='Citywide')
line1 = plot.line('date', 'hours', source=source1, color='#087f8c', line_width=3, legend_label=f'ZIP {first}')
line2 = plot.line('date', 'hours', source=source2, color='#d97706', line_width=3, legend_label=f'ZIP {second}')
plot.add_tools(HoverTool(renderers=[cityline, line1, line2], tooltips=[('Area', '@area'), ('Closure month', '@month'), ('Average hours', '@hours{0,0.0}'), ('Complaints', '@count{0,0}')], mode='vline'))
plot.legend.location = 'top_left'
plot.legend.click_policy = 'hide'


def update(attr, old, new):
    source1.data = series(select1.value)
    source2.data = series(select2.value)
    plot.legend[0].items[1].label = {'value': f'ZIP {select1.value}'}
    plot.legend[0].items[2].label = {'value': f'ZIP {select2.value}'}


if not globals().get('STANDALONE', False):
    select1.on_change('value', update)
    select2.on_change('value', update)
intro = Div(text='<h1>NYC 311 closure times</h1><p>Compare two ZIP codes with the citywide average. Includes all complaint types opened in 2024, with a ZIP code and valid closure date.</p>')
notes = Div(text='<p><b>How to read this:</b> Months are based on when complaints closed, including closures after 2024. Gaps mean no eligible closures that month. Hover for counts and averages.</p><p>Later months only represent late closures of complaints opened in 2024, not all complaints opened in those months. Differences can reflect complaint types and extreme durations; they do not establish service quality or its causes. “Closure time” measures the recorded close date, not the first response.</p>')
curdoc().add_root(column(intro, select1, select2, plot, notes, sizing_mode='stretch_width', max_width=1100))
curdoc().title = 'NYC 311 ZIP-code comparison'

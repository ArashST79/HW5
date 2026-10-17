"""Create a standalone interactive Bokeh page from precomputed summaries."""
import runpy
from pathlib import Path
from bokeh.embed import file_html
from bokeh.models import CustomJS
from bokeh.resources import INLINE

app = runpy.run_path(str(Path(__file__).parent / 'dashboard/main.py'), init_globals={'STANDALONE': True})
callback = CustomJS(args=dict(
    select1=app['select1'], select2=app['select2'],
    source1=app['source1'], source2=app['source2'],
    legend=app['plot'].legend[0],
    summaries={z: app['series'](z) for z in app['zipcodes']}
), code="""
source1.data = summaries[select1.value];
source2.data = summaries[select2.value];
legend.items[1].label = {value: 'ZIP ' + select1.value};
legend.items[2].label = {value: 'ZIP ' + select2.value};
source1.change.emit();
source2.change.emit();
""")
app['select1'].js_on_change('value', callback)
app['select2'].js_on_change('value', callback)
output = Path(__file__).parent / 'dashboard.html'
output.write_text(file_html(app['curdoc'](), INLINE, 'NYC 311 ZIP-code comparison'))
print(output)

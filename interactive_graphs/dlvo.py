import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models import FuncTickFormatter

x = np.linspace(0.2, 100, 500)
'''
These equations specify the opening plot. Following movement of slider
the equation displayed is specified in the CustomJS callback
'''
#Electrostatic
prefactor = (4*6E24*(1.6E-19*0.04)**2)/(1.38E-23 * 300)
kappa = 1/((80*8.854E-12*1.38E-23*300)/(2*6E24*(1.6E-19)**2))**0.5
elec = prefactor*np.exp(-(1/8)*x)
print(1/kappa)
#VdW
vdw=-1*1e-19*(1/(x*1E-9)**3)

#Combined
combo = elec + vdw

#Add data to source datastructure
source = ColumnDataSource(data=dict(x=x, y=elec, a=vdw, b=combo))

#Create plot
plot = figure(x_axis_label='Separation (nm)', y_axis_label='Pressure',y_range=(-20000,50000), plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, line_color='green')
plot.line('x', 'a', source=source, line_width=3, line_alpha=0.6, line_color='blue')
plot.line('x', 'b', source=source, line_width=3, line_alpha=0.6, line_color='red')

#Add sliders to adjust parameters
hamaker_slider = Slider(start=0.01, end=10, value=1, step=0.01, title="Hamaker (*1e-19)")
kappa_slider = Slider(start=0.01, end=20, value=8, step=0.01, title="1/Kappa (*1e-9)")


callback = CustomJS(args=dict(source=source, amp=hamaker_slider, freq=kappa_slider),
                    code="""
    const data = source.data;
    const A = amp.value * 1e-19;
    const kappa = freq.value * 0.000000001;
    const x = data['x']
    const y = data['y']
    const a = data['a']
    const b = data['b']
    const prefactor =  (24*1e24*Math.pow((1.6*1e-19*0.04),2))/(1.38*1e-23 * 300)
    
    for (var i = 0; i < x.length; i++) {
        y[i] = prefactor * Math.exp(-x[i]*1e-9/kappa);
        a[i] = -A / Math.pow((x[i]*1E-9),3);
        b[i] =a[i] + y[i];
    }
    source.change.emit();
""")

hamaker_slider.js_on_change('value', callback)
kappa_slider.js_on_change('value', callback)
callback

layout = row(
    plot,
    column(hamaker_slider, kappa_slider),
)

output_file("dlvo.html", title="dlvo.py")

show(layout)
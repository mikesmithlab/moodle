import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models import FuncTickFormatter

x = np.linspace(0.2, 50, 500)
'''
These equations specify the opening plot. Following movement of slider
the equation displayed is specified in the CustomJS callback
'''
#Membrane_fluctuations
#prefactor = (4*6E24*(1.6E-19*0.04)**2)/(1.38E-23 * 300)
kappa = 80E-24
temperature = 300
membrane_flucs = (1/(x*1e-9)**3)*(1.38E-23*temperature)**2/(kappa*3.14**2)

#VdW
vdw=-(3/18)*1e-19*(1/(x*1E-9)**3)

#Combined
combo = membrane_flucs + vdw

#Add data to source datastructure
source = ColumnDataSource(data=dict(x=x, y=membrane_flucs, a=vdw, b=combo))

#Create plot
plot = figure(x_axis_label='Separation (nm)', y_axis_label='Pressure',y_range=(-20000,50000), plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, line_color='green')
plot.line('x', 'a', source=source, line_width=3, line_alpha=0.6, line_color='blue')
plot.line('x', 'b', source=source, line_width=3, line_alpha=0.6, line_color='red')

#Add sliders to adjust parameters
hamaker_slider = Slider(start=0.01, end=10, value=3, step=0.01, title="Hamaker (*1e-19)")
kappa_slider = Slider(start=1, end=200, value=80, step=1, title="Stiffness (*1e-24)")
temperature_slider = Slider(start=273, end=373, value=300, step=1, title="Temperature (K)")


callback = CustomJS(args=dict(source=source, amp=hamaker_slider, freq=kappa_slider, temp=temperature_slider),
                    code="""
    const data = source.data;
    const A = amp.value * 1e-19 / 18;
    const kappa = freq.value * 1e-24;
    const T = temp.value;
    const x = data['x']
    const y = data['y']
    const a = data['a']
    const b = data['b']
    
    
    for (var i = 0; i < x.length; i++) {
        y[i] = Math.pow(x[i]*1e-9,-3)*(1.38E-23*T)**2/(kappa*3.14**2);
        a[i] = -A / Math.pow((x[i]*1E-9),3);
        b[i] =a[i] + y[i];
    }
    source.change.emit();
""")

hamaker_slider.js_on_change('value', callback)
kappa_slider.js_on_change('value', callback)
temperature_slider.js_on_change('value', callback)
callback

layout = row(
    plot,
    column(hamaker_slider, kappa_slider, temperature_slider),
)

output_file("membranes.html", title="membrane.py")

show(layout)
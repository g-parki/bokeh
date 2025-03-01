'''This example shows how to plot multiple lines with the `multi_line` call.

.. bokeh-example-metadata::
    :apis: bokeh.plotting.figure.multi_line, bokeh.models.HoverTool, bokeh.models.TapTool
    :refs: :ref:`userguide_plotting` > :ref:`userguide_plotting_line_glyphs_multi`
    :keywords: multi_line, HoverTool, TapTool

'''

from collections import defaultdict

import numpy as np
from scipy.stats import norm

from bokeh.layouts import gridplot
from bokeh.models import HoverTool, TapTool
from bokeh.palettes import Viridis6
from bokeh.plotting import figure, output_file, show

mass_spec = defaultdict(list)

RT_x = np.linspace(118, 123, num=50)
norm_dist = norm(loc=120.4).pdf(RT_x)

# Generate several gaussian distributions and spectral lines
for scale, mz in [(1.0, 83), (0.9, 55), (0.6, 98), (0.4, 43), (0.2, 39), (0.12, 29)]:
    mass_spec["RT"].append(RT_x)
    mass_spec["RT_intensity"].append(norm_dist * scale)
    mass_spec["MZ"].append([mz, mz])
    mass_spec["MZ_intensity"].append([0, scale])
    mass_spec['MZ_tip'].append(mz)
    mass_spec['Intensity_tip'].append(scale)

mass_spec['color'] = Viridis6

figure_opts = dict(width=450, height=300)
hover_opts = dict(
    tooltips=[('MZ', '@MZ_tip'), ('Rel Intensity', '@Intensity_tip')],
    show_arrow=False,
    line_policy='next'
)
line_opts = dict(
    line_width=5, line_color='color', line_alpha=0.6,
    hover_line_color='color', hover_line_alpha=1.0,
    source=mass_spec
)

rt_plot = figure(tools=[HoverTool(**hover_opts), TapTool()], **figure_opts)
rt_plot.multi_line(xs='RT', ys='RT_intensity', legend_field="Intensity_tip", **line_opts)
rt_plot.xaxis.axis_label = "Retention Time (sec)"
rt_plot.yaxis.axis_label = "Intensity"

mz_plot = figure(tools=[HoverTool(**hover_opts), TapTool()], **figure_opts)
mz_plot.multi_line(xs='MZ', ys='MZ_intensity', legend_field="Intensity_tip", **line_opts)
mz_plot.legend.location = "top_center"
mz_plot.xaxis.axis_label = "MZ"
mz_plot.yaxis.axis_label = "Intensity"

output_file("multi_line.html", title="multi_line.py example")

show(gridplot([[rt_plot, mz_plot]]))

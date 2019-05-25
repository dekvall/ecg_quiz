from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
from plotly import tools

import pandas as pd
import numpy as np
import json

import wfdb

app = Flask(__name__)

@app.route('/')
def index():
	p = create_ecg_plot_from_local(patient_num='001', case='s0010_re')
	return render_template('index.html', plot=p)


def create_ecg_plot_from_local(patient_num, case, from_sample=10000, to_sample=14000):
	fig = tools.make_subplots(rows=3, cols=4, shared_xaxes=False, shared_yaxes=False)
	signals, fields = wfdb.rdsamp('data/patient{}/{}'.format(patient_num, case),
									sampfrom=from_sample,
									sampto=to_sample, 
									channels=[0,1,2,3,4,5,6,7,8,9,10,11])
	x = np.linspace(0,fields['sig_len']/fields['fs'],fields['sig_len'])
	for idx, name in enumerate(fields['sig_name']):
		trace = go.Scatter(
				x = x,
				y = signals[:,idx],
				mode = 'lines',
				name = name.upper()
				)
		row = idx%3+1
		col = idx//3+1
		fig.append_trace(trace, row, col)

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

@app.route('/answer', methods=['GET', 'POST'])
def change_features():
	feature = request.args['selected']
	print(feature)
	graphJSON = create_plot(feature)
	return graphJSON

if __name__ == '__main__':
	app.run()
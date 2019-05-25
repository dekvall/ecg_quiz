from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
from plotly import tools

import pandas as pd
import numpy as np
import json
import random
import wfdb

from records import records

app = Flask(__name__)
curr_info = None
swedish_plot_positions = ['AVL',
							'I',
							'-AVR',
							'II',
							'AVF',
							'III',
							'V1',
							'V2',
							'V3',
							'V4',
							'V5',
							'V6',]
swedish_plot_positions_col_wise = ['AVL',
									'V1',
									'I',
									'V2',
									'-AVR',
									'V3',
									'II',
									'V4',
									'AVF',
									'V5',
									'III',
									'V6']
swedish_plot_positions_num = [1,2,3,4,5,6,1,2,3,4,5,6]

@app.route('/')
def index():
	case = random.choice(records)
	p = create_swedish_ecg_plot_from_local(case)
	return render_template('index.html', plot=p)


def create_ecg_plot_from_local(case, from_sample=10000, to_sample=14000):
	global curr_info
	fig = tools.make_subplots(rows=3, cols=4, shared_xaxes=False, shared_yaxes=False)
	signals, fields = wfdb.rdsamp('data/{}'.format(case),
									sampfrom=from_sample,
									sampto=to_sample, 
									channels=[0,1,2,3,4,5,6,7,8,9,10,11])
	x = np.linspace(0,fields['sig_len']/fields['fs'],fields['sig_len'])
	curr_info = fields['comments']
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

def create_swedish_ecg_plot_from_local(case, from_sample=10000, to_sample=14000):
	global curr_info
	fig = tools.make_subplots(rows=6, cols=2, shared_xaxes=False, shared_yaxes=False, subplot_titles=swedish_plot_positions_col_wise)
	signals, fields = wfdb.rdsamp('data/{}'.format(case),
									sampfrom=from_sample,
									sampto=to_sample, 
									channels=[0,1,2,3,4,5,6,7,8,9,10,11])
	x = np.linspace(0,fields['sig_len']/fields['fs'],fields['sig_len'])
	curr_info = fields['comments']
	row_pos = dict(zip(swedish_plot_positions,swedish_plot_positions_num))
	for idx, name in enumerate(fields['sig_name']):
		if name.upper() == 'AVR':
			y = -signals[:,idx] 
			nm = '-{}'.format(name.upper())
		else:
			y = -signals[:,idx] 
			nm = name.upper()
		trace = go.Scatter(
				x = x,
				y = y,
				mode = 'lines',
				name = nm
				)
		row = row_pos[nm]
		col = idx//6+1
		fig.append_trace(trace, row, col)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def create_ecg_plot_from_online_storage(case, from_sample=10000, to_sample=14000):
	global curr_info
	fig = tools.make_subplots(rows=3, cols=4, shared_xaxes=False, shared_yaxes=False)
	signals, fields = wfdb.rdsamp('{}'.format(case),
									pb_dir = 'ptbdb/{}'.format(case[:10]),
									sampfrom=from_sample,
									sampto=to_sample, 
									channels=[0,1,2,3,4,5,6,7,8,9,10,11])
	x = np.linspace(0,fields['sig_len']/fields['fs'],fields['sig_len'])
	curr_info = fields['comments']
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
def submit_answer():
	answer = request.args['selected']
	return json.dumps(eval_answer(answer))

def eval_answer(ans):
	result = ""
	if ans in curr_info[4].lower():
		result += "<h2>CORRECT!</h2></br>More information:"
	else:
		result += "<h2>INCORRECT!</h2></br>More information:"
	return result + "</br>".join(curr_info)

if __name__ == '__main__':
	app.run()
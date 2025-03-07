from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def load_schedule_data(hub=None):
    df = pd.read_excel('grafik.xlsx', sheet_name='April')
    df.columns = df.columns.astype(str)

    if hub:
        df = df[df['Hub'] == hub]

    shift_counts = df['2025-04-01 00:00:00'].value_counts().to_dict()
    
    return df, shift_counts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shift_stats')
def shift_stats():
    hub = request.args.get('hub')
    df, shift_counts = load_schedule_data(hub)
    
    selected_shift = request.args.get('shift')
    agents = []

    if selected_shift:
        agents = df[df['2025-04-01 00:00:00'] == selected_shift]['Agent Name'].tolist()

    return render_template('shift_stats.html', shift_counts=shift_counts, hub=hub, agents=agents, selected_shift=selected_shift)

if __name__ == "__main__":
    app.run(debug=True)

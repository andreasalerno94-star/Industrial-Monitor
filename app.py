import os
import random
from datetime import datetime
from flask import Flask, jsonify, render_template, request

import database as db

app = Flask(__name__)
db.init_db()

_call_count = 0


def _spike(normal, spike, prob=0.02):
    return spike() if random.random() < prob else normal()


def _gen(i):
    ptype = random.choice(('vacuum', 'overpressure'))
    temp = _spike(
        lambda: round(random.uniform(380, 439), 1),
        lambda: round(random.uniform(441, 460), 1),
    )
    vib = _spike(
        lambda: round(random.uniform(0.05, 1.48), 2),
        lambda: round(random.uniform(1.52, 2.0), 2),
    )
    if ptype == 'vacuum':
        pressure = _spike(
            lambda: round(random.uniform(5e-6, 9e-5), 8),
            lambda: round(random.uniform(1.1e-4, 2e-4), 8),
        )
    else:
        pressure = _spike(
            lambda: round(random.uniform(1.1, 3.4), 2),
            lambda: round(random.uniform(3.6, 4.5) if random.random() < 0.5 else random.uniform(0.3, 0.9), 2),
        )
    return {
        'id': i,
        'name': f'Bonder {i}',
        'temperature': temp,
        'vibration': vib,
        'pressure': pressure,
        'pressure_type': ptype,
        'timestamp': datetime.now().isoformat(),
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def sensor_data():
    global _call_count
    _call_count += 1
    if _call_count % 100 == 0:
        db.cleanup_old()
    return jsonify([_gen(i) for i in range(1, 9)])


@app.route('/api/alarms')
def get_alarms():
    days = int(request.args.get('days', 7))
    return jsonify(db.get_alarms(days))


@app.route('/api/alarms/save', methods=['POST'])
def save_alarm():
    d = request.get_json(force=True)
    db.save_alarm(
        d['machine_id'], d['machine_name'], d['sensor'],
        d['value'], d['threshold_min'], d['threshold_max'],
    )
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

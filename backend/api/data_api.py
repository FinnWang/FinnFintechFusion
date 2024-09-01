# backend/api/data_api.py
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import date, datetime
import logging
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.INFO)

# 数据库连接
# 请确保替换为您的实际数据库连接信息
DB_CONNECTION = 'postgresql://postgres:5432@localhost:5432/NewDB'
engine = create_engine(DB_CONNECTION)

def custom_json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the TAIFEX Data API",
        "endpoints": {
            "/api/compare_latest": "Get comparison of latest two trading days",
            "/api/data": "Get data for a specific date range"
        }
    })

@app.route('/api/compare_latest', methods=['GET'])
def compare_latest():
    try:
        query = """
        WITH latest_dates AS (
            SELECT DISTINCT date
            FROM taifex_data_3total
            ORDER BY date DESC
            LIMIT 2
        )
        SELECT *
        FROM taifex_data_3total
        WHERE date IN (SELECT date FROM latest_dates)
        ORDER BY date DESC, identity
        """
        df = pd.read_sql(query, engine)
        
        if df.empty:
            return jsonify({"error": "No data available"}), 404

        latest_date = df['date'].iloc[0]
        previous_date = df['date'].iloc[-1]

        latest_data = df[df['date'] == latest_date]
        previous_data = df[df['date'] == previous_date]

        def calculate_totals(data):
            return {
                'total_long_position': int(data['long_position'].sum()),
                'total_short_position': int(data['short_position'].sum()),
                'total_net_position': int(data['net_position'].sum()),
            }

        latest_totals = calculate_totals(latest_data)
        previous_totals = calculate_totals(previous_data)

        changes = {
            'long_position_change': latest_totals['total_long_position'] - previous_totals['total_long_position'],
            'short_position_change': latest_totals['total_short_position'] - previous_totals['total_short_position'],
            'net_position_change': latest_totals['total_net_position'] - previous_totals['total_net_position'],
        }

        response = {
            'latest_date': latest_date,
            'previous_date': previous_date,
            'latest_data': latest_data.to_dict(orient='records'),
            'previous_data': previous_data.to_dict(orient='records'),
            'latest_totals': latest_totals,
            'previous_totals': previous_totals,
            'changes': changes
        }

        return app.response_class(
            response=json.dumps(response, default=custom_json_serializer),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        app.logger.exception(f"An error occurred in compare_latest: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        start_date = request.args.get('start_date', default=(datetime.now() - pd.Timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', default=datetime.now().strftime('%Y-%m-%d'))

        query = f"""
        SELECT *
        FROM taifex_data_3total
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date DESC, identity
        """
        df = pd.read_sql(query, engine)

        if df.empty:
            return jsonify({"error": "No data available for the specified date range"}), 404

        response = {
            'start_date': start_date,
            'end_date': end_date,
            'data': df.to_dict(orient='records')
        }

        return app.response_class(
            response=json.dumps(response, default=custom_json_serializer),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        app.logger.exception(f"An error occurred in get_data: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
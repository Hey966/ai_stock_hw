from __future__ import annotations

from flask import Blueprint, jsonify, request

from services.market_scan import load_market_scan, run_market_scan
from services.strategy import generate_daily_strategy, load_daily_strategy

api_scan = Blueprint("api_scan", __name__)


@api_scan.route("/api/market-scan", methods=["GET"])
def get_market_scan():
    return jsonify(load_market_scan())


@api_scan.route("/api/market-scan/run", methods=["POST"])
def run_scan_now():
    limit = request.args.get("limit", type=int)
    data = run_market_scan(limit=limit)
    return jsonify({"status": "ok", "data": data})


@api_scan.route("/api/daily-strategy", methods=["GET"])
def get_daily_strategy():
    return jsonify(load_daily_strategy())


@api_scan.route("/api/daily-strategy/run", methods=["POST"])
def run_daily_strategy_now():
    data = generate_daily_strategy()
    return jsonify({"status": "ok", "data": data})
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config import IS_LOCAL, Config, DevelopmentConfig
from core.controller.mask import MaskController
from core.utils.logger import logger

load_dotenv()

cfg = DevelopmentConfig if IS_LOCAL else Config

app = Flask(__name__)
app.config.from_object(cfg)

controller = MaskController(logger)


@app.route("/v1/chat", methods=["POST"])
def mask():
    try:
        request_data = request.get_json()
        return controller.mask(request_data)
    except Exception as e:
        return jsonify({"error": "Failed to decode JSON object: " + str(e)}), 400@app.route("/v1/api/chat", methods=["POST"])

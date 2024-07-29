from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from config import IS_LOCAL, Config, DevelopmentConfig
from core.controller.chat import CloneClientController
from core.service.masker import MaskerService
from core.service.searcher import OpenSearchService
from core.usecase.chat import CloneClientUsecase
from core.utils.logger import logger

load_dotenv()

cfg = DevelopmentConfig if IS_LOCAL else Config

app = Flask(__name__)
app.config.from_object(cfg)
CORS(app)

masker_service = MaskerService(
    cfg.OPENAI_API_KEY,
    logger,
)
open_service = OpenSearchService(
    cfg.VECTOR_SEARCH_URL,
    logger,
)
usecase = CloneClientUsecase(masker_service, open_service, logger)
controller = CloneClientController(usecase, logger)


@app.route("/v1/chat", methods=["POST"])
async def chat():
    try:
        request_data = request.get_json()
        return await controller.chat(request_data)
    except Exception as e:
        return jsonify({"error": "Failed to decode JSON object: " + str(e)}), 400


if __name__ == "__main__":
    app.run()

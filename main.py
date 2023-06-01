import secrets
from typing import Any, List, Dict

from flask import Flask, Response, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

computadores: List[Dict[str, Any]] = [
    {"id": 1, "cliente":"Ronaldo", "placa_mae": "Asus", "processador": "Intel", "memoria_ram": "8GB", "hd": "1TB", "ssd": "256GB", "fonte": "Corsair", "gabinete": "Corsair", "placa_de_video": "Nvidia", "preco": "R$ 5.000,00", "imagem": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.kabum.com.br%2Fproduto%2F101010%2Fplaca-de-video-gigabyte-nvidia-geforce-gtx-1660-super-oc-6gb-gddr6-gv-n166soc-6gd&psig=AOvVaw0QZ3Z3Z2Z2Z2Z2Z2Z2Z2Z2&ust=1629789845654000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCJjQ4ZqHgvICFQAAAAAdAAAAABAD"},
]


@app.route("/auth", methods=["POST"])
def auth() -> Response:
    """
    Perform authentication
    """
    data: Any = request.get_json()
    if (
        {"username", "password"}.issubset(data)
        and data["username"] == "admin"
        and data["password"] == "admin"
    ):
        access_token: str = secrets.token_urlsafe()
        refresh_token: str = secrets.token_urlsafe()
        print(access_token)
        return jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "status": "success",
            }
        )
    return jsonify({"status": "login failed"}), 401


@app.route("/computadores", methods=["GET"])
def get_computadores() -> Response:
    """
    Get all computadores
    """
    return jsonify(computadores)

@app.route("/computadores", methods=["POST"])
def create_computador() -> Response:
    """
    Create a new computador
    """
    data: Any = request.get_json()
    computador = {
        "id": len(computadores) + 1,
        "cliente": data.get("cliente"),
        "placa_mae": data.get("placa_mae"),
        "placa_de_video": data.get("placa_de_video"),
        "processador": data.get("processador"),
        "memoria_ram": data.get("memoria_ram"),
        "hd": data.get("hd"),
        "ssd": data.get("ssd"),
        "fonte": data.get("fonte"),
        "gabinete": data.get("gabinete"),
        "preco": data.get("preco"),
        "imagem": data.get("imagem"),
    }
    computadores.append(computador)
    return jsonify({"status": "success", "computador": computador}), 201

@app.route("/computadores/<int:computador_id>", methods=["DELETE"])
def delete_computador(computador_id: int) -> Response:
    """
    Delete a computador by ID
    """
    index = None
    for i, computador in enumerate(computadores):
        if computador["id"] == computador_id:
            index = i
            break

    if index is not None:
        deleted_computador = computadores.pop(index)
        return jsonify({"status": "success", "computador": deleted_computador}), 200
    else:
        return jsonify({"status": "failure", "message": "Computador not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=19003)

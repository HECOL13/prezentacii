from flask import Flask, request, jsonify
import requests
import time
import os

app = Flask(__name__)

API_TOKEN = os.getenv("r8_cuWUgDMRDihgFKC4JhUee1JFQfVdheu39mu4x")

@app.route("/")
def home():
    return "Server is working"

@app.route("/remove", methods=["POST"])
def remove():
    image = request.json.get("image")
    mask = request.json.get("mask")

    res = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers={
            "Authorization": f"Token {API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "version": "stability-ai/stable-diffusion-inpainting",
            "input": {
                "image": image,
                "mask": mask,
                "prompt": "remove watermark, clean background"
            }
        }
    ).json()

    get_url = res["urls"]["get"]

    while True:
        r = requests.get(get_url, headers={
            "Authorization": f"Token {API_TOKEN}"
        }).json()

        if r["status"] == "succeeded":
            return jsonify({"result": r["output"][0]})

        if r["status"] == "failed":
            return jsonify({"error": "AI error"})

        time.sleep(2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

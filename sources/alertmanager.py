"""
alertmanager.py

An ansible-events event source module for receiving events via a webhook from alertmanager.

Arguments:
    host: The hostname to listen to. Set to 0.0.0.0 to listen on all interfaces. Defaults to 127.0.0.1
    port: The TCP port to listen to.  Defaults to 5000

"""

from flask import Flask, request
from gevent.pywsgi import WSGIServer


def main(queue, args):

    app = Flask(__name__)

    @app.route("/<path:endpoint>", methods=["POST", "PUT", "DELETE", "PATCH"])
    def webhook(endpoint):
        payload = (request.json,)
        queue.put(
            dict(
                payload=payload,
                meta=dict(endpoint=endpoint, headers=dict(request.headers)),
            )
        )
        for alert in payload.get("alerts"):
            queue.put(
                dict(
                    alert=alert,
                    meta=dict(endpoint=endpoint, headers=dict(request.headers)),
                )
            )
        return "Received", 202

    http_server = WSGIServer(
        (args.get("host") or "127.0.0.1", args.get("port") or 5000), app
    )
    http_server.serve_forever()

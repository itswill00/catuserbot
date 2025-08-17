def register_status_route(app):
    @app.route("/status", methods=["GET"])
    def status():
        return {"status": "running"}

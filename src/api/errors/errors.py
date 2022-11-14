from src.api import app


@app.errorhandler(500)
def internal_error_code_500(error):
    return "500 error", 500


@app.errorhandler(400)
def internal_error_code_400(error):
    return "400 error", 400


@app.errorhandler(404)
def internal_error_code_400(error):
    return "Page doen't exists", 404

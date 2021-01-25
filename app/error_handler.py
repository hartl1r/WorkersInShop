from app import appfrom flask import render_template, request
@app.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html")

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {e}. route: {request.url}")
    email_admin(message="Server error", error=e, url=request.url)
    
    print(e)
    return render_template("500.html")
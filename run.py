from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', False)
    if debug:
        app.logger.warning("Running in development mode. Set FLASK_ENV to production for deployment.")
    else:
        app.logger.info("Running in production mode. Use Gunicorn or similar WSGI server for deployment.")
    app.run(host='0.0.0.0', port=port, debug=debug)

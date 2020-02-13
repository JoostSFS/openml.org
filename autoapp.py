from server.app import *

# Create flask app and routing
app = Flask(__name__, static_url_path='', static_folder='server/src/client/app/build',
            instance_relative_config=True)
app.config.from_object(Config)

app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
CORS(app)
register_extensions(app)
register_blueprints(app)
app.secret_key = 'change key here'


@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def serve_static(path):
    """ Never ever reached! """
    print("static folder serve")
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def page_not_found(e):
    # This seems to catch all routes! Refer link:
    # https://stackoverflow.com/questions/14023864/flask-url-route-route-all-other-urls-to-some-function
    print("error handler reached!")
    print(request.url)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), debug=True, ssl_context='adhoc')

# TODO Unit testing
# TODO Config management
# TODO replace to production server
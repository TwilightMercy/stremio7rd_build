from flask import Flask, jsonify, redirect, render_template

app = Flask(__name__)
app.json.sort_keys = False
################################################################
# Constants
LATEST_VERSION = "2.1.0"
STREMIO7RD_URL = "https://i.imgur.com/CRpsxpE.jpeg"
RED_THUMBS_DOWN_URL = "https://i.imgur.com/gY4MWuf.png"
GREEN_THUMBS_UP_URL = "https://i.imgur.com/ntwsGcb.png"
NEW_UPDATE_URL = "https://i.imgur.com/RZcmX2e.png"
BUILD_QR_URL = "https://i.imgur.com/wbnhJUp.png"
################################################################

# Define a base manifest template
def generate_manifest(version):
    return {
        "id": "org.stremio7rd.com",
        "version": version,
        "name": f"Stremio + Real Debrid Israel Build",
        "description": f"Stremio + Real Debrid Israel Build Version Check.",
        "logo": STREMIO7RD_URL,
        "resources": ["catalog"],
        "types": ["other"],
        "catalogs": [
            {
                "type": "other",
                "id": "info_catalog",
                "name": "Stremio + Real Debrid Israel ברוכים הבאים לבילד של"
            }
        ],
        "behaviorHints": {
            "configurable": True
        }
    }
    
def parse_params(params):
    
    # Default values
    defaults = {
        "current_version": LATEST_VERSION,
        "show_catalog_even_if_updated": True
    }
    
    """Parse params and return a dictionary with values."""
    parsed_params = {}
    if params:
        for part in params.split(","):
            if "=" in part:
                key, value = part.split("=", 1)
                # Get value or set to True/False if boolean.
                parsed_params[key] = value.lower() == "true" if value.lower() in ["true", "false"] else value
    
    # Apply defaults for missing parameters
    for key, default_value in defaults.items():
        parsed_params.setdefault(key, default_value)
        
    print(f"[DEBUG] parse_params | parsed_params={str(parsed_params)}")
    return parsed_params


@app.route("/")
def root_redirect():
    return redirect('/configure')

@app.route("/<path:params>/configure")
@app.route("/configure")
def configure_page(params=None):
    
    # Parse params into a dictionary using the helper function
    parsed_params = parse_params(params)
    
    # Boolean variable to check if current version is the latest
    is_latest_version = parsed_params["current_version"] == LATEST_VERSION
    current_version = None if is_latest_version else parsed_params["current_version"]
    
    # show_catalog_even_if_updated = true if parsed_params["show_catalog_even_if_updated"] else "false"
    show_catalog_even_if_updated = parsed_params["show_catalog_even_if_updated"]
    
    return render_template("configure.html", 
                           CURRENT_VERSION=current_version,
                           LATEST_VERSION=LATEST_VERSION,
                           SHOW_CATALOG_EVEN_IF_UPDATED=show_catalog_even_if_updated)

@app.route("/manifest.json")
def default_manifest():
    """Redirect root URL to default version manifest."""
    """If the manifest URL is accessed without a version, redirect to the versioned URL."""
    params = f'current_version={LATEST_VERSION},show_catalog_even_if_updated=true'
    return redirect(f'/{params}/manifest.json')

@app.route("/<path:params>/manifest.json")
def manifest(params):
    """Return the manifest for a specific version."""
    # Generate the manifest for the specific version
    
    # Parse params into a dictionary using the helper function
    parsed_params = parse_params(params)
    current_version = parsed_params["current_version"]
    
    manifest_data = generate_manifest(current_version)
    return respond_with(manifest_data)

@app.route("/<path:params>/catalog/other/info_catalog.json")
@app.route("/catalog/other/info_catalog.json")
def catalog(params=None):
    """Return the catalog with text fetched from an external URL."""
    print("[DEBUG] /catalog/other/info_catalog.json endpoint was called.")
    
    # Parse params into a dictionary using the helper function
    parsed_params = parse_params(params)
    
    current_version = parsed_params["current_version"]
    show_catalog_even_if_updated = parsed_params["show_catalog_even_if_updated"]
    print(f"[DEBUG] catalog | current_version={current_version} | show_catalog_even_if_updated={show_catalog_even_if_updated}")
    
    # Boolean variable to check if current version is the latest
    is_latest_version = current_version == LATEST_VERSION
    
    # Handle case where show_catalog_even_if_updated is False and current_version is the latest
    if is_latest_version and not show_catalog_even_if_updated:
        return respond_with({"metas": []})
    
    catalog_entry = [
        {
            "id": "latest_version",
            "name": f"גרסה אחרונה: {LATEST_VERSION}",
            "type": "other",
            "poster": STREMIO7RD_URL,
            "posterShape": "square"
        },
        {
            "id": "current_version",
            "name": f"גרסה נוכחית: {current_version}",
            "type": "other",
            "poster": GREEN_THUMBS_UP_URL if is_latest_version else RED_THUMBS_DOWN_URL,
            "posterShape": "square"
        }
    ]
    
    if not is_latest_version:
        catalog_entry.extend([
        {
            "id": "build_qr",
            "name": "סרוק להתקנה",
            "type": "other",
            "poster": BUILD_QR_URL,
            "posterShape": "square"
        },
        {
            "id": "update_addon",
            "name": "!יש לעדכן את הבילד",
            "type": "other",
            "poster": NEW_UPDATE_URL,
            "posterShape": "square"
        }
    ])
        
    return respond_with({"metas": catalog_entry})

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

if __name__ == "__main__":
    print("[DEBUG] Starting the Flask application on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

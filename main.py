from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

def get_zip_url(repo_url):
    parsed = urlparse(repo_url)
    domain = parsed.netloc.lower()
    path_parts = parsed.path.strip('/').split('/')

    if len(path_parts) < 2:
        return None, "Invalid repository URL"

    user, repo = path_parts[0], path_parts[1].replace('.git', '')

    if 'github.com' in domain:
        zip_url = f"https://github.com/{user}/{repo}/archive/refs/heads/master.zip"
        return zip_url, None
    elif 'gitlab.com' in domain:
        zip_url = f"https://gitlab.com/{user}/{repo}/-/archive/master/{repo}-master.zip"
        return zip_url, None
    else:
        return None, "Unsupported domain"

@app.route('/')
def api_info():
    return jsonify({
        "message": "Welcome to the Repo ZIP URL API!",
        "usage": {
            "GET": "/get-zip-url?repo_url=REPO_LINK",
            "POST": {
                "endpoint": "/get-zip-url",
                "body": {"repo_url": "REPO_LINK"}
            },
            "supported_domains": ["github.com", "gitlab.com"]
        }
    })

@app.route('/get-zip-url', methods=['GET', 'POST'])
def get_repo_zip():
    if request.method == 'POST':
        data = request.json
        repo_url = data.get('repo_url')
    else:  # GET
        repo_url = request.args.get('repo_url')

    if not repo_url:
        return jsonify({'error': 'repo_url is required'}), 400

    zip_url, error = get_zip_url(repo_url)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'zip_url': zip_url})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

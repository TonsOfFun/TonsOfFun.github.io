from flask import Flask, redirect, request, Response
import requests
import json
import yaml

app = Flask(__name__)

# Replace with your LinkedIn App's Client ID and Secret
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:5000/auth/linkedin/callback'

@app.route('/auth/linkedin', methods=['GET'])
def linkedin_auth():
    linkedin_auth_url = f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=123456&scope=profile%20email'
    return redirect(linkedin_auth_url)

@app.route('/auth/linkedin/callback', methods=['GET'])
def linkedin_callback():
    code = request.args.get('code')
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_response = requests.post(access_token_url, data=payload, headers=headers).json()
    access_token = token_response['access_token']

    # Fetch profile data
    profile_url = 'https://api.linkedin.com/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(profile_url, headers=headers)
    profile_data = response.json()

    # Convert to YAML
    yaml_data = yaml.dump(profile_data)

    return Response(
        yaml_data,
        mimetype="text/yaml",
        headers={"Content-disposition": "attachment; filename=linkedin_data.yaml"}
    )

if __name__ == '__main__':
    app.run(debug=True)

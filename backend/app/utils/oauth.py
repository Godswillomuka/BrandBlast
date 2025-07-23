# Placeholder for Google/Facebook OAuth integration

def oauth_login(provider, token):
    """
    Mock function. Replace with real OAuth library logic like Authlib or Flask-Dance.
    """
    if provider == "google":
        # validate token, get email/name from Google
        return {"email": "googleuser@example.com", "name": "Google User"}
    elif provider == "facebook":
        # validate token, get email/name from Facebook
        return {"email": "fbuser@example.com", "name": "Facebook User"}
    else:
        return None

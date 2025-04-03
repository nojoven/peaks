# authentication.py
import os
import httpx
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from functools import wraps
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize router
router = APIRouter()
# Initialize OAuth
oauth = OAuth()
# Use HTTP Bearer scheme for API Key authentication.
api_key_scheme = HTTPBearer()

def retrieve_manager_api_key():
    if not os.getenv("MANAGER_API_KEY"):
        raise ValueError("MANAGER_API_KEY is not set in the environment variables.")
    return os.getenv("MANAGER_API_KEY")

USERS_API_KEYS: Dict[str, str] = {
    retrieve_manager_api_key(): "manager",
}




def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(api_key_scheme)) -> str:
    """
    Validate the API key sent in the Authorization header.
    Returns the associated user if valid.
    """
    api_key = credentials.credentials
    if api_key not in USERS_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    # Return the username associated with the API key.
    return USERS_API_KEYS[api_key]

@router.get("/profile", tags=["profile"])
async def get_user_profile(user: str = Depends(get_api_key)):
    """
    Endpoint that returns the user's profile. Useful for testing authentication.
    Accessible only if a valid API key is provided.
    The present router is prefixed with "auth/" so the endpoint is only accessible at "auth/profile".
    """
    return {"user": user, "message": "This is your profile!"}

def retrieve_peak_api_secret_key():
    """
    Retrieve the PEAK_API_SECRET_KEY from environment variables.
    """
    if not os.getenv("PEAK_API_SECRET_KEY"):
        raise ValueError("PEAK_API_SECRET_KEY is not set in the environment variables.")
    return os.getenv("PEAK_API_SECRET_KEY")

# Configure GitHub OAuth
def configure_oauth():
    """
    Retrieve OAuth environment variables.
    """
    required_vars = (
        os.getenv('OAUTH_GITHUB_CLIENT_ID'),
        os.getenv('OAUTH_GITHUB_CLIENT_SECRET'),
        os.getenv('OAUTH_GITHUB_ACCESS_TOKEN_URL'),
        os.getenv('OAUTH_GITHUB_AUTHORIZE_URL'),
        os.getenv('OAUTH_GITHUB_API_BASE_URL')
    )
    if not all(required_vars):
        raise ValueError("Missing Valid GitHub OAuth Secret Values. Please check environment variables and secrets.")

    # Configure GitHub OAuth
    oauth.register(
        name='github',
        client_id=os.getenv('OAUTH_GITHUB_CLIENT_ID'),        # Set in environment
        client_secret=os.getenv('OAUTH_GITHUB_CLIENT_SECRET'),  # Set in environment
        access_token_url=os.getenv('OAUTH_GITHUB_ACCESS_TOKEN_URL'),
        access_token_params=None,
        authorize_url=os.getenv('OAUTH_GITHUB_AUTHORIZE_URL'),
        authorize_params=None,
        api_base_url=os.getenv('OAUTH_GITHUB_API_BASE_URL'),
        client_kwargs={'scope': 'user:email'},
    )

# Call configuration once during module initialization
configure_oauth()

@router.get('/login')
async def login(request: Request, force: bool = False):
    """
    Redirect the user to GitHub for authentication.
    """
    if "token" not in request.session:
        redirect_uri = request.url_for('auth:auth')
        return await oauth.github.authorize_redirect(
            request, 
            redirect_uri,
            prompt="consent"  # Make GitHub ask for credentials
    )
    if force:
        return RedirectResponse(url="/peaks", status_code=303)

async def revoke_github_token(access_token: str):
    """Revoke GitHub OAuth token."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"https://api.github.com/applications/{os.getenv('OAUTH_GITHUB_CLIENT_ID')}/token",
            auth=(os.getenv('OAUTH_GITHUB_CLIENT_ID'), os.getenv('OAUTH_GITHUB_CLIENT_SECRET')),
            json={"access_token": access_token},
        )
    return response.status_code == 204

@router.get('/auth', name="auth:auth")
async def auth(request: Request):
    """
    Process the GitHub callback and retrieve user information.
    """

    # Check if the user has canceled the authentication

    if "error" in request.query_params:
        # User denied access → redirect to error page
        # return RedirectResponse(url="/error?msg=Access%20Denied")
        return RedirectResponse(url="/")
    try:
        token = await oauth.github.authorize_access_token(request)
    except Exception as e:
        # Log l'erreur pour comprendre ce qui se passe
        print("Error obtaining access token:", e)
        raise HTTPException(status_code=400, detail="Failed to obtain access token")
    
    # Log le token obtenu
    print("Access token obtained:", token)
    
    if not token or "access_token" not in token:
        raise HTTPException(status_code=400, detail="Access token missing in response")
    
    # Récupérer les infos utilisateur
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token['access_token']}"}
        )
    if response.status_code != 200:
        print("Error fetching user info:", response.text)
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user info from GitHub")
    
    user = response.json()
    print("User info obtained:", user)

    request.session["user"] = user
    return RedirectResponse(url='/peaks')


def require_login(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Check if the user is logged in
        if 'user' not in request.session:
            return RedirectResponse(url='/auth/login')
        return await func(request, *args, **kwargs)
    return wrapper


@router.get("/logout", name="auth:logout")
async def logout(request: Request):
    """Logout the user by revoking GitHub token and clearing session."""
    print(f"Session avant clear: {request.session}")
    token = request.session.get("token")

    # Revoke GitHub token if present
    if token:
        await revoke_github_token(token["access_token"])

    # Clear local session
    request.session.clear()
    print(f"Session après clear: {request.session}") 
    # Redirect properly to "/"
    return RedirectResponse(url="/", status_code=303)


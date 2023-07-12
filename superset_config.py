# Superset specific config
ROW_LIMIT = 5000

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = "pk.eyJ1IjoiYWJvdXRwaGlsaXBwZSIsImEiOiJjbGswY2t4M3YwMTg2M2RubXh3aWlmcHZwIn0.go2pBHdsUa0ljydvUTm0Eg"

# Enable public access to the Port Congestion Public dashboard
PUBLIC_ROLE_LIKE_GAMMA = True
AUTH_ROLE_PUBLIC = 'Public'

# Configure Superset to allow embedding the dashboard within an iframe
ENABLE_IFRAME = True
ALLOWED_HOSTS = ['your-website-domain']  # Replace with your domain
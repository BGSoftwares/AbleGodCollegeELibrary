import os
import secrets

WSGI_PATH = "/var/www/bgdevopps_pythonanywhere_com_wsgi.py"
ENV_PATH = "/home/BGDevopps/.ablegod.env"
PROJECT_PATH = "/home/BGDevopps/AbleGodCollegeELibrary"

def fix_wsgi():
    print(f"🔧 Fixing WSGI configuration at {WSGI_PATH}...")
    wsgi_content = f"""import os
import sys

# Add your project directory to the sys.path
path = '{PROJECT_PATH}'
if path not in sys.path:
    sys.path.append(path)

# Set the correct settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
    try:
        with open(WSGI_PATH, "w") as f:
            f.write(wsgi_content)
        print("✅ Successfully updated WSGI file.")
    except PermissionError:
        print(f"❌ Permission denied writing to {WSGI_PATH}. Ensure you are running this on PythonAnywhere.")
    except FileNotFoundError:
        print(f"⚠️ Warning: Could not find WSGI file at {WSGI_PATH}. Is the path correct?")

def fix_env():
    print(f"🔧 Setting up environment variables at {ENV_PATH}...")
    if not os.path.exists(ENV_PATH):
        try:
            secret_key = secrets.token_urlsafe(50)
            env_content = f"""SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS=bgdevopps.pythonanywhere.com
"""
            with open(ENV_PATH, "w") as f:
                f.write(env_content)
            print("✅ Successfully created secure .env file.")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
    else:
        print("✅ .env file already exists. Skipping creation to preserve your existing secrets.")

if __name__ == "__main__":
    print("\n🚀 Starting PythonAnywhere automated fixes...\n")
    fix_wsgi()
    print()
    fix_env()
    
    print("\n" + "=" * 60)
    print("🎉 Configuration fixes applied!")
    print("\nTo finish the deployment, run these commands in your PythonAnywhere bash console:")
    print(f"  cd {PROJECT_PATH}")
    print("  # If you use a virtual environment, activate it first (e.g., workon myenv)")
    print("  pip install -r requirements.txt")
    print("  python manage.py migrate")
    print("  python manage.py collectstatic --noinput")
    print("\nFinally, go to your PythonAnywhere Web tab and click the big green Reload button!")
    print("=" * 60 + "\n")

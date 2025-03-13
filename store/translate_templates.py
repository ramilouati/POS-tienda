import os
from googletrans import Translator
from django.conf import settings

# Initialize Django settings (required to access settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
import django
django.setup()

# Initialize translator
translator = Translator()

# Define the source and target languages
SOURCE_LANG = 'pt'  # Spanish (or 'pt' for Portuguese)
TARGET_LANG = 'fr'  # French

def translate_text(text):
    try:
        translated = translator.translate(text, src=SOURCE_LANG, dest=TARGET_LANG)
        return translated.text
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def process_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace hardcoded text with translated text
    translated_content = translate_text(content)

    # Write the translated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_content)

def get_all_template_dirs():
    # Get the project-wide templates directory from TEMPLATES['DIRS']
    template_dirs = settings.TEMPLATES[0]['DIRS']

    # Add app-specific templates directories (if APP_DIRS is True)
    if settings.TEMPLATES[0].get('APP_DIRS', False):
        for app in settings.INSTALLED_APPS:
            try:
                # Get the app module
                app_module = __import__(app)
                # Get the app's directory
                app_path = os.path.dirname(app_module.__file__)
                # Add the app's templates directory
                app_template_dir = os.path.join(app_path, 'templates')
                if os.path.exists(app_template_dir):
                    template_dirs.append(app_template_dir)
            except ImportError:
                print(f"Could not import app: {app}")

    return template_dirs

def main():
    template_dirs = get_all_template_dirs()
    for template_dir in template_dirs:
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    print(f"Translating {file_path}...")
                    process_template(file_path)

if __name__ == "__main__":
    main()
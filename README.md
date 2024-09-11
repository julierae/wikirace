# Django Application Setup with Pyenv and venv for WikiRace Project

## Prerequisites
- pyenv (Python version management)
- pip (Python package installer)

## Setup Instructions

1. Install pyenv (if not already installed):
   For macOS/Linux:
   ```
   curl https://pyenv.run | bash
   ```
   For Windows, use pyenv-win:
   ```
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```

2. Add pyenv to your PATH and initialize it (add to your shell configuration file):
   ```
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

3. Install the desired Python version:
   ```
   pyenv install 3.11.8  # or your preferred version
   ```

4. Navigate to the folder where you want to clone the WikiRace project:
   ```
   git clone https://github.com/julierae/wikirace.git
   ```

5. Set the local Python version for your project:
   ```
   pyenv local 3.11.8  # or your installed version
   ```

6. Create a new virtual environment:
   ```
   python -m venv venv
   ```

7. Activate the virtual environment:
   On macOS/Linux:
   ```
   source venv/bin/activate
   ```
   On Windows:
   ```
   .\venv\Scripts\activate
   ```

8. Install Requirements:
   ```
   pip install -r requirements.txt
   ```

9. Run migrations:
    ```
    python manage.py migrate
    ```

10. Create a superuser (optional):
    You can use the super user to access the admin site at http://localhost:8000/admin/
    ```
    python manage.py createsuperuser
    ```

11. Start the development server:
    ```
    python manage.py runserver
    ```

12. Access the application at http://localhost:8000/


13. Here's a preview of the running WikiRace application:

   ![WikiRace Application](https://raw.githubusercontent.com/julierae/wikirace/develop/static/images/wikirace_preview.png)



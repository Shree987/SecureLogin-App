# SecureLogin
An Authentication system with additional layer of security using Password Expiration 

### Author
Shreeraksha (181CO149)

## Installation Setup:
1. Clone the repository<br/>
```
git clone https://github.com/Shree987/SecureLogin-App.git
```

2. Setup your virtual environment and activate it (Windows).
```
mkdir djangoenv  
python -m venv djangoenv
```
You can also use the existing virtual environment in this code. By using this, you can skip Step 3.
```
cd djangoenv\Scripts
activate
cd ..\..
```

3. Install Django and Django Crispy-forms with pip<br/>
```
python -m pip install Django
python -m pip install Django-crispy-forms
```

4. Open the SecureLogin folder and migrate all files
```
cd "SecureLogin App\securelogin"
python manage.py makemigrations
python manage.py migrate
```

6. Run the server<br/>
```
python manage.py runserver
```

7. Start the app at [http://127.0.0.1:8000](http://127.0.0.1:8000)
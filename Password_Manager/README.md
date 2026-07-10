# Password Manager

A production-quality password manager web application built with Flask, SQLAlchemy, Flask-Login, Bootstrap, and Fernet encryption.

## Features

- User registration and login
- Secure password hashing with Werkzeug
- Encrypted password storage with Fernet
- CRUD for saved passwords
- Search by website and username
- Password generator with uppercase, lowercase, numbers, and symbols
- Responsive Bootstrap dashboard
- CSRF protection and flash messaging

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser at:
   ```text
   http://127.0.0.1:5000/
   ```

## Requirements

- Python 3.13
- Flask
- Flask-Login
- SQLAlchemy
- Flask-WTF
- cryptography
- Werkzeug

## Folder Structure

```text
Password_Manager/
├── app.py
├── config.py
├── models.py
├── routes.py
├── forms.py
├── utils.py
├── requirements.txt
├── README.md
├── instance/
│   └── passwords.db
├── templates/
├── static/
└── screenshots/
```

## Screenshots

Screenshots can be placed in the screenshots folder after running the app.

## Future Enhancements

- Two-factor authentication
- Password strength analyzer
- Import/export of credentials
- Dark mode toggle
- Mobile app support

## License

This project is licensed under the MIT License.


---

# My Portfolio Website

Welcome to my portfolio website! This user-friendly website allows anyone to create their own portfolio by managing content through the UI. It showcases projects, provides information about the creator, and allows visitors to get in touch.

## Features

- **User Authentication**: Users can register, log in, and log out securely using password hashing and Flask-Login.

- **Project Showcase**: A section dedicated to showcasing projects with details such as project name, technologies used, GitHub link, website link (if applicable), and project images. Projects can be added, edited, and deleted through the admin panel.

- **Admin Panel**: An admin panel allows administrators to manage the website's content without changing the code. This includes adding, editing, and deleting projects, as well as managing the website's configuration.

- **Contact Form**: A contact form allows visitors to send messages directly to the website owner through the UI.

## Technologies Used

- **Python**: The backend logic is written in Python using the Flask framework.

- **Flask Extensions**: Various Flask extensions are used, including Flask-Bootstrap for frontend styling, Flask-SQLAlchemy for database management, Flask-Login for user authentication, Flask-Mail for email functionality, and Flask-WTF for form handling.

- **Database**: The website uses an SQL database managed by SQLAlchemy to store user data, project information, and website configuration.

- **Frontend**: HTML, CSS, and JavaScript are used for the frontend, with templates rendered using the Jinja2 templating engine.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/dheerajark/portfolio.git
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   - Create a `.env` file in the project root directory.
   - Add the following environment variables to the `.env` file:

     ```
     FLASK_APP=app.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key
     DB_URI=your_database_uri
     MY_EMAIL=your_email_address
     PASSWORD=your_email_password
     ```

4. Run the application:

   ```
   flask run
   ```

5. Access the website:

   Open your web browser and go to `http://localhost:5000` to view the website locally.

6. Manual Registration and Login:

   - Navigate to the registration page by adding /register to the website URL 'http://localhost:5000/register'.
   - After registering, navigate to the login page by adding /login to the website 'http://localhost:5000/login'.

## Contribution

Contributions are welcome! If you have any suggestions, improvements, or feature requests, feel free to open an issue or create a pull request.



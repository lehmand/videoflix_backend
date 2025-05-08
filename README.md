# Videoflix

Videoflix is a streaming platform that allows users to watch videos. The project consists of a Django backend and an Angular frontend.

## Project Structure

The project is divided into two main components:

1. **Backend**: Developed with Django and Django REST Framework
   - User authentication and management
   - Video storage and management
   - REST API for frontend communication

2. **Frontend**: Developed with Angular
   - Responsive user interface
   - Video player with different quality options
   - User registration and login

## Technologies

### Backend
- Python 3.x
- Django 5.2
- Django REST Framework
- PostgreSQL
- Redis (for caching and task queues)
- Django RQ (for background tasks like video conversion)

### Frontend
- Angular
- TypeScript
- SCSS
- Video.js (for video player)

## Installation

### Prerequisites
- Python 3.x
- Node.js and npm
- PostgreSQL
- Redis
- FFmpeg (for video conversion)

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/lehmand/videoflix_backend.git
   cd videoflix_backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   "venv/Scripts/activate"  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory (see `dotenv_template` as a template)

5. Migrate the database:
   ```
   python manage.py migrate
   ```

6. Create an admin user:
   ```
   python manage.py createsuperuser
   ```

7. Start the server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

git clone https://github.com/lehmand/videoflix_frontend.git
cd videoflix_frontend

1. Navigate to the frontend directory:
   ```
   cd src
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   ng serve
   ```

4. The frontend is accessible at: `http://localhost:4200`

## Features

- User registration and login
- Email confirmation for new accounts
- Password reset functionality
- Video upload (admin)
- Automatic video conversion to different quality levels
- Video catalog with categories
- Responsive design for mobile and desktop devices
- Privacy and imprint pages

## Development on Windows

This project was developed on Windows. Some notes for Windows developers:

- Make sure Python, Node.js, and npm are properly installed and available in your PATH
- Redis for Windows can be installed from [https://github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases)
- FFmpeg for Windows can be downloaded from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Ensure FFmpeg is available in your PATH

## Background Processes

The system uses Django RQ for video conversion. To start the workers:

```
python manage.py rqworker default
```
Probably only works under Linux

## Deployment

The application is configured for deployment on a Linux server with Nginx. 

## Environment Variables

A `.env` file is needed to define configuration variables. A template is available in `dotenv_template`.

## Authors

- Daniel Lehmann

## License

All rights reserved.

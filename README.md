# EnChat - Secure Chatting App

## Overview
EnChat is a secure, real-time chatting application built with Django for the backend and React for the frontend. It supports live notifications, disappearing messages, and various user-friendly features.

## Features
- **Authentication**: User registration and login with JWT authentication.
- **One-on-One Chatting**: Secure real-time messaging.
- **End-to-End Encryption**: Ensuring secure communication.
- **Typing Indicators**: Show when the other user is typing.
- **Message Read Status**: See when a message is read.
- **Live Messages**: Instant message updates with WebSockets.
- **Message History**: Store and retrieve past messages.
- **Last Seen Status**: View when a user was last online.
- **Message Deletion**: Remove messages from chat.
- **Predefined Profile Pictures**: Users can select from a set of pre-made avatars.

## Tech Stack
- **Backend**: Django, Django REST Framework, WebSockets
- **Frontend**: React, @chatscope/chat-ui-kit
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Real-time Communication**: Django Channels & WebSockets

## Installation & Setup

### Prerequisites
- Python 3.x


### Backend Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/sr1v47s4n/EnChat-API.git
   cd EnChat/backend
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the Django server:
   ```sh
   python manage.py runserver
   ```


## API Endpoints
### Authentication (`/auth/`)
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `POST /auth/refresh` - Token Refresh

### User Management (`/user/`)
- `GET /user/profile/` - Fetch user profile


### Chat (`/chat/`)
- `GET /chat/users/` - Get all user chats
- `GET /chat/messages/<chat_id>/` - Fetch messages from a chat
- `POST /chat/send/` - Send a message


### Real-Time WebSocket URLs
- `ws://127.0.0.1:8000/ws/chat/<chat_id>/` - Live chat communication
- `ws://127.0.0.1:8000/ws/typing/` - Typing indicator updates

## Usage
1. Register or log in to the application.
2. Select a chat from the available list.
3. Send and receive messages in real time.
4. See when messages are read and when the user is typing.
5. Log out when done.

## Contributing
Feel free to fork the repository, create a branch, and submit pull requests.

## License
This project is licensed under the MIT License.




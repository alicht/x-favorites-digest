# X Favorites Digest

An automated tool that sends you a daily email digest of posts you've liked on X (formerly Twitter).

## Features

- Monitors your liked posts throughout the day
- Sends a daily email digest at 11:30 PM
- Includes post text and links to original posts
- Runs in the background using launchd (macOS)

## Setup

1. Install required packages:
```bash
python3 -m pip install -r requirements.txt
```

2. Create a `.env` file with your credentials:
```
X_API_KEY=your-api-key
X_API_SECRET=your-api-secret
X_ACCESS_TOKEN=your-access-token
X_ACCESS_TOKEN_SECRET=your-access-token-secret
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

### Getting the Credentials

#### X API Keys
1. Go to https://developer.twitter.com/
2. Create a project and app
3. Generate API keys and tokens
4. Enable OAuth 1.0a

#### Gmail App Password
1. Go to your Google Account settings
2. Enable 2-Step Verification if not already enabled
3. Go to Security → App Passwords
4. Generate new app password for "Mail"

## Running the Script

```bash
python3 x_favorites_digest.py
```

The script will check for liked posts every hour and send a digest email at 11:30 PM.

## Project Structure

- `x_favorites_digest.py`: Main script
- `requirements.txt`: Python dependencies
- `.env`: Configuration file (not included in repo)
- `.gitignore`: Git ignore rules

## Note

Make sure not to commit your `.env` file as it contains sensitive credentials.

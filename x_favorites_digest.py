# File: x_favorites_digest.py
import tweepy
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, time
from time import sleep
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class XFavoritesDigest:
    def __init__(self, x_auth, email_config):
        # X API credentials (using OAuth 1.0a User Context)
        auth = tweepy.OAuthHandler(
            x_auth['api_key'],
            x_auth['api_secret']
        )
        auth.set_access_token(
            x_auth['access_token'],
            x_auth['access_token_secret']
        )
        
        # Initialize API v2 client with auth
        self.client = tweepy.Client(
            consumer_key=x_auth['api_key'],
            consumer_secret=x_auth['api_secret'],
            access_token=x_auth['access_token'],
            access_token_secret=x_auth['access_token_secret']
        )
        
        # Email configuration
        self.email_config = email_config
        
        # Store favorites for the day
        self.daily_favorites = []
        
    def get_todays_favorites(self):
        """Fetch today's favorites for the authenticated user"""
        try:
            # Get authenticated user's ID
            me = self.client.get_me()
            if not me[0]:
                raise Exception("Could not get user ID")
            
            user_id = me[0].id
            
            # Get user's liked posts from today
            likes = self.client.get_liked_tweets(
                user_id,
                tweet_fields=['created_at', 'text', 'author_id'],
                max_results=100  # Adjust as needed
            )
            
            if not likes.data:
                print("No likes found")
                return
            
            # Filter for today's likes and store them
            today = datetime.now().date()
            for post in likes.data:
                if post.created_at.date() == today:
                    self.daily_favorites.append({
                        'text': post.text,
                        'author': post.author_id,
                        'post_id': post.id
                    })
                    print(f"Found favorite: {post.text[:50]}...")
                    
        except Exception as e:
            print(f"Error fetching favorites: {str(e)}")
            raise
    
    def send_digest_email(self):
        """Send email digest of today's favorites"""
        if not self.daily_favorites:
            print("No favorites to send")
            return
            
        # Create email content
        email_body = "Your X favorites for today:\n\n"
        for i, post in enumerate(self.daily_favorites, 1):
            email_body += f"{i}. {post['text']}\n"
            email_body += f"   Link: https://x.com/x/status/{post['post_id']}\n\n"
            
        # Create email message
        msg = MIMEText(email_body)
        msg['Subject'] = f"X Favorites Digest - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = self.email_config['from_email']
        msg['To'] = self.email_config['to_email']
        
        # Send email
        try:
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
            print("Digest email sent successfully")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    def run_daily(self):
        """Main loop to run the digest service"""
        print("Starting X Favorites Digest service...")
        while True:
            now = datetime.now()
            print(f"Current time: {now.strftime('%H:%M:%S')}")
            
            # Check if it's time to send digest (default: 11:30 PM)
            if now.time() >= time(23, 30):
                print("Time to send digest...")
                try:
                    self.get_todays_favorites()
                    self.send_digest_email()
                except Exception as e:
                    print(f"Error in daily run: {str(e)}")
                self.daily_favorites = []  # Reset for next day
                
                # Sleep until next day
                sleep_until = datetime.combine(now.date(), time(0, 0))
                sleep_seconds = (sleep_until - now).seconds + 86400  # Add 24 hours
                print(f"Sleeping until tomorrow...")
                sleep(sleep_seconds)
            else:
                # Check every hour
                print("Not time for digest yet, checking again in an hour...")
                sleep(3600)

if __name__ == "__main__":
    # Load configuration from environment variables
    x_auth = {
        'api_key': os.getenv('X_API_KEY'),
        'api_secret': os.getenv('X_API_SECRET'),
        'access_token': os.getenv('X_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('X_ACCESS_TOKEN_SECRET')
    }
    
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': os.getenv('EMAIL_USERNAME'),
        'password': os.getenv('EMAIL_PASSWORD'),
        'from_email': os.getenv('EMAIL_USERNAME'),
        'to_email': os.getenv('EMAIL_USERNAME')
    }
    
    # Add some basic validation
    missing_keys = [k for k, v in x_auth.items() if not v]
    if missing_keys:
        print(f"Missing X API credentials: {', '.join(missing_keys)}")
        exit(1)
    
    missing_email = [k for k, v in email_config.items() if not v and k in ['username', 'password']]
    if missing_email:
        print(f"Missing email configuration: {', '.join(missing_email)}")
        exit(1)
        
    print("Starting service with configured credentials...")
    digest = XFavoritesDigest(x_auth, email_config)
    digest.run_daily()
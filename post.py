import tweepy
import os
import json

# Get API keys from GitHub Secrets (environment variables)
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def post_to_twitter(post_content):
    try:
        api.update_status(post_content)
        print(f"Successfully posted to Twitter: {post_content}")
        return True
    except tweepy.TweepyException as e:  #Catch the specific exception.
        print(f"Error posting to Twitter: {e}")
        return False

def read_and_post():
    try:
        with open("post_content.json", "r") as f:
            posts = json.load(f)

        if not posts:
            print("No posts to schedule.")
            return
        
        # We will take the first post.
        post = posts.pop(0)

        if post['platform'] == 'twitter':
          success = post_to_twitter(post['content'])
          if success:
            # Write the remaining posts back to file, removing the one we just posted.
            with open("post_content.json", "w") as f:
              json.dump(posts, f, indent=4)  #Nicely formatted JSON.
          else:
            print("Posting Failed.  Post will be re-attempted next run.")

        else:
            print("No supported platform")

    except FileNotFoundError:
        print("post_content.json not found.  No posts to send.")
    except json.JSONDecodeError:
        print("post_content.json is not valid JSON.  No posts to send.")

if __name__ == "__main__":
    read_and_post()

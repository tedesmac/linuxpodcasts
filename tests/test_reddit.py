import os
from podcast_bot import is_repost
import praw


# Used by TestIsRePost
reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    password=os.environ['REDDIT_PASSWORD'],
    user_agent=os.environ['REDDIT_USER_AGENT'],
    username=os.environ['REDDIT_USERNAME'],
)
subreddit = reddit.subreddit('linuxpodcasts')


# This class tests that if cetain links already exist in r/linuxpodcasts (reposts)
# Make sure that the content actually exists
class TestIsRepost:

    def test_no_repost(self):
        url = 'http://example.org'
        title = 'Example Domain'
        assert is_repost(subreddit, url, title) == False

    def test_repost(self):
        url = 'https://latenightlinux.com/late-night-linux-episode-54/'
        title = 'Late Night Linux - Episode 54'
        assert is_repost(subreddit, url, title) == True

    def test_google_repost(self):
        url = 'http://feedproxy.google.com/~r/thirdworldlinuxogg/~3/Y9NktOiaiMU/third-world-linux-happy-holidays-and.html'
        title = 'Happy Holidays and Some Songs 2017'
        assert is_repost(subreddit, url, title)

    def test_google_no_repost(self):
        url = 'https://books.google.com.mx/books?id=ZBKsMYz1Q4kC&printsec=frontcover&dq=linux&hl=en&sa=X&ved=0ahUKEwi6yqrYxvLfAhU1NX0KHTKsARQQ6AEIKjAA#v=onepage&q=linux&f=false'
        title = 'Happy Holidays and Some Songs 2017'
        assert is_repost(subreddit, url, title)

    def test_souncloud_no_repost(self):
        url = 'https://soundcloud.com/noms-tunes/missing-you'
        title = 'Missing You'
        assert is_repost(subreddit, url, title) == False

    def test_souncloud_repost(self):
        url = 'https://soundcloud.com/fingersflynn/blgp-ep-220-2018-stats'
        title = 'BLGP EP 220: 2018 Stats'
        assert is_repost(subreddit, url, title) == True

    def test_youtube_no_repost(self):
        url = 'https://www.youtube.com/watch?v=E-6xk4W6N20'
        title = 'Fan.tasia'
        assert is_repost(subreddit, url, title) == False

    def test_youtube_repost(self):
        url = 'https://www.youtube.com/watch?v=FZLwKinoxmA'
        title = 'Linux Thursday - Jan 13, 2019 - Lingering Cough Edition'
        assert is_repost(subreddit, url, title) == True

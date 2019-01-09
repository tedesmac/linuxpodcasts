#! /usr/bin/python3

"""
MIT License

Copyright (c) 2019 Kremor Pärt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the Software), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from datetime import datetime
import json
import feedparser
import praw
import time

from podcasts import podcasts as linux_podcasts


def login() -> praw.Reddit:
    with open('credentials.json', 'r') as file:
        credentials = json.loads(file.read())
        reddit = praw.Reddit(
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            password=credentials['password'],
            user_agent='r/linuxpodcasts\'s bot',
            username=credentials['user']
        )
    return reddit


def submit_post(podcast: str, title: str, link: str):
    pass


def main():
    reddit = login()
    subreddit = reddit.subreddit('linuxpodcasts')

    last_updated_all = {}

    while True:
        now = datetime.now()

        try:
            with open('last_loop.json') as file:
                last_loop = datetime(*json.loads(file.read()))
        except (FileNotFoundError, TypeError):
            last_loop = datetime.now()

        for podcast in linux_podcasts:
            name, href = podcast

            last_updated = last_updated_all.get(name, now)
            delta = now - last_updated

            # Only updates feeds after a day
            if delta.total_seconds() > 60*60*24:
                feed = feedparser.parse(href)
                for entry in feed.entries:
                    published = datetime(*entry.published_parsed[:6])
                    delta = last_loop - published
                    if delta.total_seconds() < 0:
                        title = entry.title
                        link = entry.link
                        # pulish to reddit
                        # subreddit.submit('{} - {}'.format(name, title), url=link)
                        print(name, title, published)
                        # sleeps 16 minutes before posting anything else
                        time.sleep(16 * 60)
                    else:
                        break

            last_updated_all[name] = now

        with open('last_updated.json', 'w') as file:
            file.write('[{}, {}, {}, {}, {}, {}, {}]'.format(
                now.year,
                now.month,
                now.day,
                now.hour,
                now.minute,
                now.second,
                now.microsecond
            ))

        # sleeps for 1 hour
        time.sleep(60*60)


if __name__ == '__main__':
    main()

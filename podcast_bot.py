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

import click
from datetime import datetime
import json
import feedparser
import logging
from logging.handlers import RotatingFileHandler
import praw
import time

from podcasts import podcasts as linux_podcasts


FILE_NAME = 'last_loop.json'


@click.option(
    '--client-id',
    envvar='REDDIT_CLIENT_ID',
    help='reddit client id.'
)
@click.option(
    '--client-secret',
    envvar='REDDIT_CLIENT_SECRET',
    help='reddit client secret.'
)
@click.command()
@click.option(
    '--debug',
    is_flag=True,
    help='Run bot in debug mode.'
)
@click.option(
    '--password',
    '-p',
    envvar='REDDIT_PASSWORD',
    help='reddit user password.'
)
@click.option(
    '--user-agent',
    envvar='REDDIT_USER_AGENT',
    help='reddit user agent.'
)
@click.option(
    '--username',
    '-u',
    envvar='REDDIT_USERNAME',
    help='reddit user.'
)
@click.argument('subreddit', nargs=1)
def main(client_id, client_secret, debug, password, subreddit, user_agent, username):
    """
    Simple bot that submits podcasts to reddit.

    Usage:\tpython3 bot.py askreddit
    """
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        user_agent=user_agent,
        username=username
    )
    subreddit = reddit.subreddit(subreddit)

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    now = datetime.now()

    try:
        with open(FILE_NAME) as file:
            last_loop = datetime(*json.loads(file.read()))
            logging.info('{} readed with date {}'.format(
                FILE_NAME, last_loop
            ))
    except (FileNotFoundError, TypeError):
        last_loop = datetime.now()
        logging.info(
            'Could not read {}, last_loop variable will be set to {}'.format(
                FILE_NAME,
                now
            )
        )

    for podcast in linux_podcasts:
        name, href = podcast
        feed = feedparser.parse(href)
        if len(feed.entries) == 0:
            logging.warning(
                'Podcast \'{}\' doesn\'t have a feed'.format(name)
            )
        for entry in feed.entries:
            published = datetime(*entry.published_parsed[:6])
            delta = last_loop - published
            if delta.total_seconds() < 0:
                title = entry.title
                link = entry.link
                if not debug:
                    subreddit.submit(
                        '{} - {}'.format(name, title), url=link)
                logging.info(
                    'Entry submitted.\n\tPodcast: {}\n\tTitle: {}\n\tLink: {}'.format(
                        name, title, link
                    )
                )
                # sleeps 20 minutes before posting anything else
                logging.info('Script will halt for 20 minutes.')
                time.sleep(20*60)
                logging.info('Script resumed.')
            else:
                break

    with open(FILE_NAME, 'w') as file:
        file.write('[{}, {}, {}, {}, {}, {}, {}]'.format(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
            now.microsecond
        ))
        logging.info('{} writted'.format(FILE_NAME))

    logging.info('Script execution finished at {}'.format(datetime.now()))


if __name__ == '__main__':
    main()

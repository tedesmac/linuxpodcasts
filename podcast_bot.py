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
import feedparser
import json
import html
import logging
from markdownify import markdownify
import praw
import re
import time


FILE_NAME = 'last_loop.json'
RE_HTML_TAG = re.compile(r'<.*?>')
RE_HTTP = re.compile(r'^https?://')
RE_POPULAR_SITE = re.compile(r'youtube\.com|youtu\.be|soundcloud\.com')


def get_summary(entry: feedparser.FeedParserDict) -> str:
    try:
        summary = entry.summary
        if entry.summary_detail.type in ('text/html', 'text/xml'):
            summary = remove_html_tags(markdownify(summary))
        return summary
    except AttributeError:
        return ''


def get_title(name: str, title: str) -> str:
    """
    Adds podcast's name to title if it is not in it
    """
    name_lower = name.lower()
    title_lower = title.lower()
    return title if name_lower in title_lower else '{} - {}'.format(name, title)


def format_comment(title: str, summary: str, link: str, rss_link: str) -> str:
    comment = '# [{}]({})\n---\n'.format(title, link)
    comment += '{}\n\n---\n'.format(summary) if summary else ''
    comment += '+ [RSS feed]({})'.format(rss_link)
    return comment


def is_popular_site(url: str) -> bool:
    match = RE_POPULAR_SITE.search(url)
    return match != None


def is_repost(subreddit: praw.models.Subreddit, url: str, title: str) -> bool:
    # Reddit's search doesn't work as expected if the url comes from a popular site.
    if is_popular_site(url):
        query = 'title:"{}"'.format(title)
    else:
        url = remove_http_protocol(url)
        query = 'url:{}'.format(url)
    search = subreddit.search(query)
    for _ in search:
        return True
    return False


def remove_html_tags(string: str) -> str:
    return html.unescape(re.sub(RE_HTML_TAG, '', string))


def remove_http_protocol(url: str) -> str:
    match = RE_HTTP.search(url)
    if match:
        end = match.end(0)
        return url[end:]
    return url


def submit_post(reddit: praw.Reddit, subreddit: praw.models.Subreddit, name, rss_link, title, summary, link):
    title = get_title(name, title)

    submission_id = subreddit.submit(title, url=link)
    submission = reddit.submission(id=submission_id)
    comment = format_comment(title, summary, link, rss_link)
    submission.reply(comment)

    logging.info(
        'New entry submitted:'
        '\n\tTitle: {}'
        '\n\tSummary: {}'
        '\n\tLink: {}\n'.format(title, summary, link)
    )
    logging.info(
        'Commented on entry for {}:'
        '\nComment: {}\n'.format(title, comment)
    )


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
@click.option(
    '--sleep',
    default=60,
    type=click.INT,
    help='Sleep time in minutes.'
)
@click.argument(
    'podcasts',
    nargs=1,
    type=click.Path(exists=True, resolve_path=True)
)
@click.argument(
    'subreddit',
    nargs=1,
    type=click.STRING
)
def main(client_id, client_secret, debug, password, podcasts, subreddit, user_agent, username, sleep):
    """
    Simple bot that submits podcasts to reddit

    Arguments:

    \tPODCASTS: JSON file with a list of RSS feeds.\n
    \tSUBREDDIT: Subreddit's name.

    Usage:

    \tpython3 podcast_bot.py podcasts.json linuxpodcasts

    See README.md for more information.
    """

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG if debug else logging.INFO
    )

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        user_agent=user_agent,
        username=username
    )

    if reddit.read_only:
        raise 'Login error: Reddit instance is read only, can not submit posts'

    subreddit = reddit.subreddit(subreddit)

    with open(podcasts) as file:
        podcasts = json.loads(file.read())

    while True:

        for podcast in podcasts:
            href = podcast['href']
            name = podcast['name']
            feed = feedparser.parse(href)

            logging.debug('Fetching {} feed\n'.format(name))

            # Prevents the script from crashing if the feed wasn't correctly fetched
            try:
                # Only checks the first entry
                entry = feed.entries[0]
            except IndexError:
                continue

            title = entry.title
            link = entry.link
            summary = get_summary(entry)

            repost = is_repost(subreddit, link, title)

            if repost and not debug:
                submit_post(reddit, subreddit, name,
                            href, title, summary, link)

                # sleeps 20 minutes before posting anything else
                time.sleep(20*60)

            elif debug and repost:
                logging.debug(
                    'Repost for {}:'
                    '\n\tTitle: {}'
                    '\n\tSummary: {}'
                    '\n\tLink: {}\n'.format(name, title, summary, link)
                )
                time.sleep(10)
            elif debug:
                logging.debug(
                    'New entry for {}:'
                    '\n\tTitle: {}'
                    '\n\tSummary: {}'
                    '\n\tLink: {}\n'.format(name, title, summary, link)
                )
                time.sleep(10)

        # Sleeps for 1 hour before repeating the process
        time.sleep(60*sleep)


if __name__ == '__main__':
    main()


from feedparser import FeedParserDict
import os
from podcast_bot import (
    format_comment,
    get_summary,
    get_title,
    is_popular_site,
    is_repost,
    remove_html_tags,
    remove_http_protocol
)
import praw


class TestFormatComment:

    def test_with_summary(self):
        title = 'Linux Podcast - A title'
        summary = 'A brief summary.'
        link = 'http://example.org'
        rss_link = 'http://example.org'
        comment = '# [Linux Podcast - A title](http://example.org)\n---\n' + \
            'A brief summary.\n\n---\n' + \
            '+ [RSS feed](http://example.org)'
        result = format_comment(title, summary, link, rss_link)
        assert result == comment

    def test_without_summary(self):
        title = 'Linux Podcast - A title'
        summary = ''
        link = 'http://example.org'
        rss_link = 'http://example.org'
        comment = '# [Linux Podcast - A title](http://example.org)\n---\n' + \
            '+ [RSS feed](http://example.org)'
        result = format_comment(title, summary, link, rss_link)
        assert result == comment


class TestGetSummary:

    def test_html(self):
        entry = FeedParserDict(
            summary='<html>A brief summary.</html>',
            summary_detail=FeedParserDict(type='text/html')
        )
        assert 'A brief summary.' == get_summary(entry)

    def test_markdown(self):
        entry = FeedParserDict(
            summary='**A brief summary.**',
            summary_detail=FeedParserDict(type='text/markdown')
        )
        assert '**A brief summary.**' == get_summary(entry)

    def test_no_key(self):
        entry = FeedParserDict()
        assert '' == get_summary(entry)

    def test_xml(self):
        entry = FeedParserDict(
            summary='<summary>A brief summary.</summary>',
            summary_detail=FeedParserDict(type='text/xml')
        )
        assert 'A brief summary.' == get_summary(entry)


class TestGetTitle:

    def test_name_at_start(self):
        name = 'Going Linux'
        title = 'Going Linux #360 · Run your business on Linux - Part 2'
        new_title = get_title(name, title)
        assert new_title == title

    def test_name_at_end(self):
        name = 'BSD Now'
        title = 'FOSS Clothing | BSD Now 280'
        new_title = get_title(name, title)
        assert new_title == title

    def text_no_name(self):
        name = '.XPenguin'
        title = 'No News Is No News'
        new_title = get_title(name, title)
        assert new_title == '{} - {}'.format(name, title)


class TestIsPopularSite:

    def test_other(self):
        url = 'https://latenightlinux.com/late-night-linux-episode-54/'
        assert is_popular_site(url) == False

    def test_soundcloud(self):
        url = 'https://soundcloud.com/noms-tunes/missing-you'
        assert is_popular_site(url) == True

    def test_youtu_be(self):
        url = 'https://youtu.be/E-6xk4W6N20'
        assert is_popular_site(url) == True

    def test_youtube(self):
        url = 'https://www.youtube.com/watch?v=E-6xk4W6N20'
        assert is_popular_site(url) == True


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


class TestRemoveHtml:

    def test_simple(self):
        html = '<b>Hello world!</b>'
        assert remove_html_tags(html) == 'Hello world!'

    def test_nested(self):
        html = '<p>Tantalus mortalem cornibus' + \
               ' <a href="http://precarilaboribus.io/in-simul.php">datae prohibent</a>,' + \
               ' duxit se contentus pavido Invidiae. Mi partem gerat iungere' + \
               ' quoniam dicentem tenues <a href="http://manerem.org/vestro.php">tereti</a>,' + \
               ' hoc habuit, quanta et Phrygum <em>tua</em> memorabile.' + \
               ' <strong>Iacit iacens</strong> natam meum, pietas maternos procorum' + \
               ' <a href="http://tereus-adapertaque.org/huc-erysicthonis">festisque vocat</a>' + \
               ' nemorisque negarunt secum in nervo plebi plena.</p>'
        result = 'Tantalus mortalem cornibus datae prohibent, duxit se contentus pavido' + \
                 ' Invidiae. Mi partem gerat iungere quoniam dicentem tenues tereti, hoc' + \
                 ' habuit, quanta et Phrygum tua memorabile. Iacit iacens natam meum,' + \
                 ' pietas maternos procorum festisque vocat nemorisque negarunt secum in' + \
                 ' nervo plebi plena.'
        assert remove_html_tags(html) == result


class TestRemoveProtocol:

    def test_https(self):
        url = 'https://fake-domain.com'
        assert remove_http_protocol(url) == remove_http_protocol(url)

    def test_http(self):
        url = 'http://fake-domain.com'
        assert 'fake-domain.com' == remove_http_protocol(url)

    def test_bad_protocol(self):
        url = 'htps:fake-domain.com'
        new_url = remove_http_protocol(url)
        assert url == new_url


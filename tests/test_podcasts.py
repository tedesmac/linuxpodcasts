import feedparser

from podcasts import podcasts as linux_podcasts


def test_podcasts():
    """
    Verifies that all the podcasts return a feed.
    """
    for podcast in linux_podcasts:
        name_, href = podcast
        feed = feedparser.parse(href)
        assert len(feed.entries) != 0

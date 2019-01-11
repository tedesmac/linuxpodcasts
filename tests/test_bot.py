from feedparser import FeedParserDict

from podcast_bot import (
    get_summary,
    format_comment,
    remove_html_tags,
    remove_http_protocol
)


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


class TestFormatComment:

    def test_with_summary(self):
        name = 'Linux Podcast'
        title = 'A title'
        summary = 'A brief summary.'
        link = 'http://example.org'
        rss_link = 'http://example.org'
        comment = '# [Linux Podcast - A title](http://example.org)\n---\n' + \
                  'A brief summary.\n\n---\n+ [RSS feed](http://example.org)'
        result = format_comment(name, title, summary, link, rss_link)
        assert result == comment

    def test_without_summary(self):
        name = 'Linux Podcast'
        title = 'A title'
        summary = ''
        link = 'http://example.org'
        rss_link = 'http://example.org'
        comment = '# [Linux Podcast - A title](http://example.org)\n---\n' + \
                  '+ [RSS feed](http://example.org)'
        result = format_comment(name, title, summary, link, rss_link)
        assert result == comment


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

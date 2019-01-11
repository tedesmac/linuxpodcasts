from feedparser import FeedParserDict

from podcast_bot import (
    get_summary,
    get_title,
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

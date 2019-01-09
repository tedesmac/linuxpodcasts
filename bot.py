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
import time


if __name__ == '__main__':
    with open('podcasts.json') as file:
        file_content = file.read()
        try:
            data = json.loads(file_content)
        except json.decoder.JSONDecodeError:
            print('Error: Unable to decode JSON file')

    try:
        now = datetime.now()
        last_updated = datetime(*data.get('last_updated', [2000, 1, 1]))
        podcasts = data.get('podcasts', [])
        for i, p in enumerate(podcasts):
            feed = feedparser.parse(p['href'])
            # Updates name and href
            podcasts[i]['name'] = feed.feed.title
            podcasts[i]['href'] = feed.href
            entries = feed.entries
            for entry in entries:
                title = entry.title
                link = entry.link
                published = datetime(*entry.published_parsed[:6])
                delta = last_updated - published
                if delta.total_seconds() < 0:
                    # pulish to reddit
                    print(title, link)
                else:
                    break
        # TODO - Uncomment the following code in the production section
        # data = {
        #    'last_updated': [now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond],
        #    'podcasts': podcasts
        # }
        # content = json.dumps(data, sort_keys=True)
        # with open('podcasts.json', 'w') as file:
        #    file.write(content)
    except Exception as e:
        print(e)

# Usage

To run the script Python 3 is required.

```bash
$ python3 podcast_bot.py PODCASTS SUBREDDIT
```

Where:

+ `PODCASTS` - A JSON file with an array of objects, where each object must
   contain the fields `name` and `href`. The `href` field is the url to the
   podcasts' feed:

```json
[
  {
    'name': 'A podcast',
    'href': 'https://a-podcast.com/feed/'
  },
  {
    'name': 'Another podcast',
    'href': 'https://another-podcast.com/feed.xml
  }
]
```

+ `SUBREDDIT` - Subreddit's name to which submit the content.
   E.g `linuxpodcasts`.

# Command line arguments

The bot supports multiple arguments:

- `--debug` - If passed the bot won't submit content to reddit and will only print to stdout.
- `--sleep` - Time that the bot will sleep between updates (in minutes). E.g. `--sleep 300` will update the bot every 5 hours.

The following parameters are required or need to be set as environment variables:

- `--client-id` - e.v. `REDDIT_CLIENT_ID` - Reddit client id<a href="#footnote-1"><sup>1</sup></a>.

- `--client-secret` - e.v. `REDDIT_CLIENT_SECRET` - Reddit client secret<a href="#footnote-1"><sup>1</sup></a>.

- `-p`, `--password` - e.v. `REDDIT_CLIENT_PASSWORD` - Reddit user password.

- `--user-agent` - e.v. `REDDIT_USER_AGENT` - Bot user agent. Can be any string. E.g. `r/linuxpodcasts`

- `-u`, `--username` - e.v. `REDDIT_USERNAME` - Reddit username.

---

1. <a name="footnote-1"></a>To get this credential go to
   http://www.reddit.com/prefs/apps/ and create a script app.

# License

MIT License

Copyright (c) 2019 Kremor Pärt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


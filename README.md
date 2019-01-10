# Usage

To run the script Python 3 is required.

```bash
$ python3 podcast_bot.py SUBREDDIT
```

Where SUBBREDDIT is the subreddit's name (without the `r/`) where you want to
submit content.

E.G.:

```bash
$ python3 podcast_bot.py linuxpodcasts
```

# Command line arguments

The bot supports the following optional arguments:

- `--client-id` - Reddit client id<a href="footnote-1"><sup>1</sup></a>.
  E.V. `REDDIT_CLIENT_ID`<a href="footnote-1"><sup>2</sup></a>
- `--client-secret` - Reddit client secret<a href="footnote-1"><sup>1</sup></a>.
  E.V. `REDDIT_CLIENT_SECRET`<a href="footnote-1"><sup>2</sup></a>
- `--debug` - The bot won't submit content to reddit.
- `--log` - Path to the log file.
- `-p`, `password` - Reddit user password.
  E.V. `REDDIT_CLIENT_PASSWORD`<a href="footnote-1"><sup>2</sup></a>
- `--user-agent` - Bot user agent. Can be any string.
  E.V. `REDDIT_USER_AGENT`<a href="footnote-1"><sup>2</sup></a>
- `-u`, `--username` - Reddit username.
  E.V. `REDDIT_USERNAME`<a href="footnote-1"><sup>2</sup></a>

---

1. <a name="footnote-1"></a>To get this credential go to
   http://www.reddit.com/prefs/apps/ and create a script app.
2. <a name="footnote-2"></a>If parameter isn't passed it will be read as an
   environment variable instead.

# Adding more podcasts

To add or change the podcasts simply modify the array in `podcasts.py`. Each
element in the array must be tuple, where the first element of the tuple is
the name of the podcast, and the second element is the RSS feed's URL.

```python
    ('Late Night Linux', 'https://latenightlinux.com/feed/all'),
```

# License

This program is licensed under the MIT license.

# Usage

To run the script Python 3 is required.

```bash
$ python3 podcast_bot.py
```

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

# Adding more podcasts

To add or change the podcasts simply modify the list inside `podcasts.py`. Each
element in the list must be a tuple, where the first element of the tuple is
the name of the podcast, and the second element is the RSS feed's URL.

```python
    ('Late Night Linux', 'https://latenightlinux.com/feed/all'),
```

# License

This program is licensed under the MIT license.

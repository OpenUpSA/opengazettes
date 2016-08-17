# Gazette listing

This is a simple Jekyll website listing South African Gazettes that [Code for South Africa](http://codes4sa.org)
has scraped and [indexed and stored in S3](http://code4sa-gazettes.s3.amazonaws.com/archive/index/gazette-index-latest.jsonlines) as part
of our [gazette liberation project](https://github.com/Code4SA/gazettescrape).

The structure is simple. Each jurisdiction (province) and year has an entry in the ``_gazettes`` directory, which
Jekyll treats as a collection. All the gazette info is taken from ``_data/gazettes.json`` which is grouped
by jurisdiction and year. Jekyll then does the hard work of generating the listings for each jurisdiction and year.

# Running locally

1. Clone the repo
2. Run ``bundle install``
3. Run ``jekyll server --watch``

# Updating

To update this list from the production index:

    curl http://code4sa-gazettes.s3.amazonaws.com/archive/index/gazette-index-latest.jsonlines -O
    python build-index.py

# Build process

The website is built by GitHub pages based on the Gazette information already in the repository.

[Travis](https://travis-ci.org/Code4SA/opengazettes) can also run a build, which downloads the latest
Gazette index from S3 and then pushes that to GitHub (which produces an updated website).

# License

MIT License.

#!/bin/env python
import json
import os
from collections import defaultdict


# jurisdiction -> year -> [gazettes]
gazettes = {}
jurisdictions = json.load(open('_data/jurisdictions.json'))


def write_year(juri, year, gazettes):
    provincial = juri != "ZA"
    title = jurisdictions[juri]
    if provincial:
        title = title + " Provincial"
    title = title + " Gazettes"

    with open('_gazettes/%s/%s.md' % (juri.lower(), year), 'w') as f:
        f.write("---\n")
        f.write("layout: year\n")
        f.write("title: %s %s\n" % (title, year))
        f.write("jurisdiction: %s\n" % juri)
        f.write("jurisdiction_name: %s\n" % jurisdictions[juri])
        f.write("provincial: %s\n" % str(juri != "ZA").lower())
        f.write("year: \"%s\"\n" % year)
        f.write("---\n")


def write_jurisdiction(juri, years):
    path = '_gazettes/%s' % juri.lower()
    try:
        os.makedirs(path)
    except OSError:
        pass

    with open('%s/index.md' % path, 'w') as f:
        provincial = juri != "ZA"
        title = jurisdictions[juri]
        if provincial:
            title = title + " Provincial"
        title = title + " Gazettes"

        f.write("---\n")
        f.write("layout: jurisdiction\n")
        f.write("title: %s\n" % title)
        f.write("jurisdiction: %s\n" % juri)
        f.write("jurisdiction_name: %s\n" % jurisdictions[juri])
        f.write("provincial: %s\n" % str(juri != "ZA").lower())
        f.write("---\n")

    for year in years.iterkeys():
        write_year(juri, year, years[year])


def build_index():
    for juri in jurisdictions.iterkeys():
        gazettes[juri] = defaultdict(list)

    for line in open('gazette-index-latest.jsonlines'):
        gazette = json.loads(line)
        juri = gazette['jurisdiction_code']
        year = gazette['publication_date'].split('-')[0]
        if 'archive_url' not in gazette:
            gazette['archive_url'] = 'http://code4sa-gazettes.s3.amazonaws.com/archive/' + gazette['archive_path']
        gazettes[juri][year].append(gazette)

    for juri in gazettes.iterkeys():
        write_jurisdiction(juri, gazettes[juri])

    # sort gazettes by date
    for juris in gazettes.itervalues():
        for items in juris.itervalues():
            items.sort(key=lambda g: g['publication_date'])

    with open('_data/gazettes.json', 'w') as f:
        json.dump(gazettes, f)


if __name__ == '__main__':
    build_index()

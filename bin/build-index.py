#!/bin/env python
import json
import os
from collections import defaultdict, Counter
from itertools import chain


# jurisdiction -> year -> [gazettes]
gazettes = {}
jurisdictions = json.load(open('_data/jurisdictions.json'))


def write_year(juri, year, gazettes):
    provincial = juri != "ZA"
    juri_info = jurisdictions[juri]
    title = juri_info["name"]
    if provincial:
        title = title + " Provincial"
    title = title + " Gazettes"

    with open('_gazettes/%s/%s.md' % (juri, year), 'w') as f:
        f.write("---\n")
        f.write("layout: year\n")
        f.write("title: %s %s\n" % (title, year))
        f.write("jurisdiction: %s\n" % juri)
        f.write("jurisdiction_name: %s\n" % juri_info["name"])
        f.write("provincial: %s\n" % str(provincial).lower())
        f.write('year: "%s"\n' % year)
        f.write("---\n")


def write_jurisdiction(juri, years):
    path = '_gazettes/%s' % juri
    try:
        os.makedirs(path)
    except OSError:
        pass

    with open('%s/index.md' % path, 'w') as f:
        provincial = juri != "ZA"
        juri_info = jurisdictions[juri]
        title = juri_info["name"]
        if provincial:
            title = title + " Provincial"
        title = title + " Gazettes"

        f.write("---\n")
        f.write("layout: jurisdiction\n")
        f.write("title: %s\n" % title)
        f.write("jurisdiction: %s\n" % juri)
        f.write("jurisdiction_name: %s\n" % juri_info["name"])
        f.write("provincial: %s\n" % str(provincial).lower())
        f.write("---\n")

    for year in years.iterkeys():
        write_year(juri, year, years[year])


def build_index():
    for juri, info in jurisdictions.iteritems():
        name = info["name"]
        gazettes[juri] = {
            'name': name,
            'years': set(),
            'gazettes': defaultdict(list),
            'search_collection': info["search_collection"],
        }

    stats = {
        'count': 0,
        'earliest_year': 9999,
        'latest_year': 0,
        'years': defaultdict(int),
        'counts': {},
    }

    for line in open('gazette-index-latest.jsonlines'):
        gazette = json.loads(line)
        juri = gazette['jurisdiction_code']
        year = gazette['publication_date'].split('-')[0]
        iyear = int(year)
        if 'archive_url' not in gazette:
            gazette['archive_url'] = 'https://archive.opengazettes.org.za/archive/' + gazette['archive_path']

        gazettes[juri]['gazettes'][year].append(gazette)
        gazettes[juri]['years'].add(year)

        stats['count'] += 1
        stats['earliest_year'] = min([stats['earliest_year'], iyear])
        stats['latest_year'] = max([stats['latest_year'], iyear])
        # for jekyll, years in keys should be strings
        stats['years'][year] += 1

    for juri in gazettes.iterkeys():
        write_jurisdiction(juri, gazettes[juri]['gazettes'])

    # sort gazettes by date, then title
    for code, juris in gazettes.iteritems():
        juris['years'] = sorted(list(juris['years']))
        for items in juris['gazettes'].itervalues():
            items.sort(key=lambda g: [g['publication_date'][:7], g['volume_number'], g['issue_number'], g['issue_title']])

        items = list(chain(*juris['gazettes'].itervalues()))

        # count by year
        years = Counter(g['publication_date'].split("-")[0] for g in items)
        if not years:
            continue

        # ensure values for all years
        min_year = min(int(i) for i in years.iterkeys())
        max_year = max(int(i) for i in years.iterkeys())
        for year in xrange(min_year, max_year + 1):
            years.update({str(year): 0})

        # count by year and month
        year_months = Counter(tuple(g['publication_date'].split("-")[0:2]) for g in items)

        # ensure values for contiguous years and months
        for year in xrange(min_year, max_year + 1):
            for m in xrange(1, 13):
                year_months.update({(str(year), '%02d' % m): 0})

        # make year_months nested
        year_months_nested = {}
        for (y, m), v in year_months.iteritems():
            year_months_nested.setdefault(y, {})[m] = v

        stats['counts'][code] = {
            'available': {
                'year': years,
                'year_month': year_months_nested,
            }
        }

    gazettes['stats'] = stats

    with open('_data/gazettes.json', 'w') as f:
        json.dump(gazettes, f, sort_keys=True)


if __name__ == '__main__':
    build_index()

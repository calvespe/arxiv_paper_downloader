"""
python_arXiv_parsing_example.py

This sample script illustrates a basic arXiv api call
followed by parsing of the results using the 
feedparser python module.

Please see the documentation at 
http://export.arxiv.org/api_help/docs/user-manual.html
for more information, or email the arXiv api 
mailing list at arxiv-api@googlegroups.com.

urllib is included in the standard python library.
feedparser can be downloaded from http://feedparser.org/ .

Author: Julius B. Lucks

This is free software.  Feel free to do what you want
with it, but please play nice with the arXiv API!

Editted By Carlos Alves Pereira

"""

import urllib
import urllib2
import feedparser

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = 'all' # search for electron in all fields
start = 0                     # retreive the first 5 results
max_results = 3

query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                     start,
                                                     max_results)

# Opensearch metadata such as totalResults, startIndex, 
# and itemsPerPage live in the opensearch namespase.
# Some entry metadata lives in the arXiv namespace.
# This is a hack to expose both of these namespaces in
# feedparser v4.1
feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

# perform a GET request using the base_url and query
response = urllib.urlopen(base_url+query).read()

# parse the response using feedparser
feed = feedparser.parse(response)

# Run through each entry, and print out information
for entry in feed.entries:
    # print('e-print metadata')
    # print('arxiv-id: %s' % entry.id.split('/abs/')[-1])
    # print('Published: %s' % entry.published)
    # print('Title:  %s' % entry.title)
    
    # feedparser v4.1 only grabs the first author
    author_string = entry.author

    # get the links to the abs page and pdf for this e-print
    for link in entry.links:
        if link.rel == 'alternate':
            print('abs page link: %s' % link.href)
        elif link.title == 'pdf':
            print('pdf link: %s' % link.href)
            download_url = link.href
            response = urllib2.urlopen(download_url)
            file = open(entry.title + ".pdf", 'wb')
            file.write(response.read())
            file.close()
            print("Completed")


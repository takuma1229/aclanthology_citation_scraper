from scholarly import scholarly

# Retrieve the author's data, fill-in, and print
# Get an iterator for the author results
search_query = scholarly.search_author('Steven A Cholewiak')
# Retrieve the first result from the iterator
first_author_result = next(search_query)
scholarly.pprint(first_author_result)

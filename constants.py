# define some useful constants

# below is the APIKey to query on the AlphaVantage website
key = ""
# define the name for the file that saves all symbols
symbols_filename = "symbols"
# define the name for the folder that contains all .csv files
output_directory = "datasets"
# the total threads number for querying should not be too large, which is meaningless
query_thread_number = 4
# maximum retry time when accessing one symbol
maximum_retry_times = 20
# the url below allows us to query for all symbols
query_symbols_url = (
    "https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo"
)

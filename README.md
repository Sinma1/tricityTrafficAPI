# tricityTrafficAPI  [![Build Status](https://travis-ci.com/Sinma1/tricityTrafficAPI.svg?branch=master)](https://travis-ci.com/Sinma1/tricityTrafficAPI)
Data agregator and API back-end related with traffics in tricity.

# Subpages
/cron - accessing this site will trigger fetcher to fetch all data from sources

/api - a entry point for API requests

/ - root of the host will display *Usage* API documentation

# Usage
All API request should go to [host]/api/

for example: *localhost/api/?last=5*

_API is executing addictional parameters in order from URL_

| Parametr |	Description |
|----------|--------------|
| last\=\<int\> |	Fetch last n results <br>e.g. last=5 |
| reverse	| Reverse order of data |
| source=\<string> |	Fetch data from specified source<br>e.g. source=trojmiasto.pl |
| since=\<YYYY-MM-DD> |	Fetch data added since specified date<br>e.g. since=2019-01-01 |
| date=\<YYYY-MM-DD> |	Fetch data from specified date<br>e.g. date=2019-01-01 |
| daterange=\<YYYY-MM-DD>:\<YYYY-MM-DD> |	Fetch data from specified range of dates<br>e.g. daterange=2019-01-01:2019-02-02 |
| intitle=\<string> |	Fetch data with specified string in title<br>e.g. intitle=example title |
| incontent=\<string> |	Fetch data with specified string in content<br>e.g. incontent=example content |
| contains=\<string> |	Fetch data with specified string in content or title<br>e.g. contains=example content or title |

# Live
Website is live and accessible on https://tricity-traffic-api.herokuapp.com

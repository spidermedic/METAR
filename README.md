## METAR
A program that decodes METAR data that a wrote as a practice exercise.

`Usage: python metar.py [-d] ICAO Code(s)`

The program requires one or more ICAO codes separated by spaces.
The `-d` option is for a more easily read output. The default is to provide a standard METAR report.

You will need to create a (free) account at [https://account.avwx.rest/](https://account.avwx.rest/) in order to get a authorization token so that you can download the json data.

Once you have the token, create a file called **my_token.py** and add the variable `MY_TOKEN=''` with your authorization token between the quotes. 
I chose to store the token in a separate file so as not to expose it on github, but you can easily forego using **my_token.py** and just paste the token to the end of the url in `get_metar()`. The file has lots of comments, so it should be easy to figure out where to do that. 

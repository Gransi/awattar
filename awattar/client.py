import requests
import datetime

from awattar.marketitem import MarketItem

class AwattarClient(object):
    def __init__(self,
                 country='AT'
                 ):
        """Construct a new AwattarClient object."""

        self._country = country 

    def request(self,
                start_time = None,
                end_time = None
                ):
        """
        Get Market data between start time and end time

        Parameters
        ----------
        start_time : datetime
            Start time
        end_time : datetime
            End time            

        Returns
        -------
        MarketItem
            Returns list of MarketItem

        """                   

        #set params
        params = ''
        if start_time != None:
            params = '?start=' + str(int(start_time.timestamp())) + '000'

            if end_time != None:
                #set end timestamp
                params = params + '&end=' + str(int(end_time.timestamp())) + '000'

        #build url
        if self._country == 'AT':
            url = 'https://api.awattar.com/v1/marketdata' + params
        elif self._country == 'DE':
            url = 'https://api.awattar.de/v1/marketdata' + params

        #send request
        req = requests.get(url)

        if req.status_code != requests.codes.ok: return None

        jsondata = req.json()
        data = [MarketItem(**k) for k in jsondata["data"]]

        return data

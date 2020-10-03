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
        MarketItem:
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
        self._data = [MarketItem.by_timestamp(**k) for k in jsondata["data"]]

        return self._data

    def min(self):
        """
        Get Market item with lowest price
        
        Returns
        -------
        MarketItem:
            Returns MarketItem with lowest price 

        """  

        if not hasattr(self,'_data'):
            self.request()

        min_item = self._data[0]

        for item in self._data:
            if item.marketprice < min_item.marketprice:
                min_item=item

        return min_item

    def max(self):
        """
        Get Market item with highest price
        
        Returns
        -------
        MarketItem:
            Returns MarketItem with highest price 

        """          
        if not hasattr(self,'_data'):
            self.request()

        max_item = self._data[0]

        for item in self._data:
            if item.marketprice > max_item.marketprice:
                max_item=item

        return max_item        

    def mean(self):
        """
        Get mean price of market 
        
        Returns
        -------
        float:    Returns mean price of market 

        """         
        if not hasattr(self,'_data'):
            self.request()

        return float((sum(a.marketprice for a in self._data))/len(self._data))

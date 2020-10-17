import requests
import datetime
import math

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
        Get Market item with lowest price from last request
        
        Returns
        -------
        MarketItem:
            Returns MarketItem with lowest price 

        """  

        min_item = self._data[0]

        for item in self._data:
            if item.marketprice < min_item.marketprice:
                min_item=item

        return min_item

    def max(self):
        """
        Get Market item with highest price from last request
        
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
        Get mean price of market of the last request
        
        Returns
        -------
        MarketItem:    Returns mean price of market 

        """         

        mean_value = float((sum(a.marketprice for a in self._data))/len(self._data))
        item = MarketItem(self._data[0].start_datetime,self._data[len(self._data)-1].end_datetime,mean_value, self._data[0].unit)

        return item

    def best_slot(self, 
                duration,
                start_datetime = None,
                end_datetime = None
                ):
        """
        Get the best slot.

        Parameters
        ----------
        duration : int
            Duration of usage[hour]
        start_datetime : datetime
            Start time
        end_datetime : datetime
            End time    

        Returns
        -------
        int
            Returns the best starting point

        """
        durationround = math.ceil(duration)
        best_slot = None
        start_index = None
        start_mean_market_price = None
        start_mean_datetime = None

        #clean up start_datetime
        if start_datetime is not None:
            start_datetime = start_datetime.replace(minute=0, second=0,microsecond=0)
            start_datetime = start_datetime.replace(tzinfo=datetime.timezone.utc)

        #clean up end_datetime
        if end_datetime is not None:
            end_datetime = end_datetime.replace(minute=0, second=0,microsecond=0)
            end_datetime = end_datetime.replace(tzinfo=datetime.timezone.utc)

        datalenght = len(self._data) - (durationround - 1)

        for i in range(0,datalenght):

            item = self._data[i]

            if start_datetime is None or item.start_datetime >= start_datetime:

                #get end
                if i < datalenght-1 and end_datetime is not None and self._data[i+durationround].end_datetime >= end_datetime:            
                    break

                sum_slot = 0
                for x in range(0, durationround):
                    sum_slot += self._data[i+x].marketprice

                mean_slot_price = sum_slot / durationround

                if best_slot is None or best_slot.marketprice > (mean_slot_price):
                    best_slot = MarketItem(item.start_datetime, item.start_datetime + datetime .timedelta(hours=durationround),mean_slot_price, item.unit)

        return best_slot        

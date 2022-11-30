import requests
from urllib.error import URLError

class request():
    def __init__self():
        ""
    @staticmethod
    def fetchdata(_url,  header= {}, _data = {} ):
         session = requests.Session()
         try:
            if _data:
                    result = session.get(url = _url, headers = header, data = _data)
            if header:
                ""
            else:           
                result = session.get(url = _url)

              

            return result

    

         except Exception as e:

                return e

    @staticmethod
    def postdata(_url,  header= {}, _data = {} ):
         session = requests.Session()
         try:
            if _data:
                    result = session.get(url = _url, headers = header, data = _data)
            else:           
                result = session.get(url = _url, headers = header)

              

            return result

    

         except Exception as e:

                return e

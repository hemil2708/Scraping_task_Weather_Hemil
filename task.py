import pymongo
import re
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
import requests

class task():
    host = 'localhost'
    port = '27017'
    db = 'Task_13_01_2022'

    def lol(self):
        con = pymongo.MongoClient(f'mongodb://{self.host}:{self.port}/')
        mydb = con[self.db]
        conn = mydb['Data']
        try:
            city = ["Mumbai","Hyderabad","Delhi","Bangalore"]
            code = ["03343c09f067e51a168a3b28e5a26f73d9592bf6e527ea139c4651e7c33d5429","d7f5a4af529e40b0a82d339e5467e89458e5ad5e2cf0ffdd05c853ed3e98fd38","7eece8ea75e09132257779f0aabd74ccf33ee6b6556bdd9ddc9753220cbe9845","072e7110ccda5a2b786e1b942f4946d382bdd6ff315f63682bfc14827786c271"]
            for i,j in zip(city,code):
                url = f"https://weather.com/en-IN/weather/today/l/{j}"
                payload = {}
                headers = {
                    'Cookie': 'ci=TWC-Connection-Speed=4G&TWC-Locale-Group=GLS+&TWC-Device-Class=desktop&X-Origin-Hint=PROD-IBM-Daybreak-today&TWC-Network-Type=wifi&TWC-GeoIP-Country=IN&TWC-GeoIP-Lat=23.03&TWC-GeoIP-Long=72.62&Akamai-Connection-Speed=1000+&TWC-Privacy=exempt&TWC-GeoIP-DMA=&TWC-GeoIP-City=AHMEDABAD&TWC-GeoIP-Region=GJ; speedpin=4G'
                }

                res = requests.get(url, headers=headers, data=payload)
                response = HtmlResponse(url="exampple.com",body=res.content)
                try:
                    city_name = response.xpath('//*[@class="CurrentConditions--location--kyTeL"]//text()').extract_first(default="").strip()
                except:
                    city_name = ""
                try:
                    curr_wea_in_cel = response.xpath('//*[@class="CurrentConditions--primary--2SVPh"]/*[@data-testid="TemperatureValue"][1]/text()').extract_first(default="").strip()
                except:
                    curr_wea_in_cel = ""
                try:
                    weather_con = response.xpath('//*[@class="CurrentConditions--primary--2SVPh"]/*[@data-testid="wxPhrase"][1]/text()').extract_first(default="").strip()
                except:
                    weather_con = ""
                try:
                    chances_run = response.xpath('//*[contains(text()," rain ")]//text()').extract_first(default="").strip()
                except:
                    chances_run = ""
                if city_name == "Bangalore":
                    chances_run = response.xpath('//*[@class="InsightNotification--root--3wUMX InsightNotification--background--2L66j"]/p//text()').extract_first(default="").strip()
                item = {}
                item['City Name'] = city_name
                item['Current weather in Celsius'] = curr_wea_in_cel
                item['Weather condition'] = weather_con
                item['Chances of having rain'] = chances_run
                try:
                    conn.create_index("City Name", unique=True)
                    X = conn.insert(dict(item))
                    print("Data Inserted Succesfully..!!")
                except Exception as e:
                    print(e, "Please Check Your Coding")
        except Exception as e:
            print(e)

loll = task()
loll.lol()
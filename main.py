from flask import Flask, jsonify
import os
from appwrite.client import Client
from appwrite.services.databases import Databases
import requests
from appwrite.id import ID
from datetime import datetime
from appwrite.query import Query

app = Flask(__name__)


@app.route('/')
def index():
    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')
    client.set_project('6579d789e407b4fb2461')
    client.set_key('9ec90038ea00bcacc48de00a4fcabceeb9a092dc0050106ac3409cd930023a08098985fb16c8f757bb40920b859585115944c6cd7caa7534bc8a98c3bf0b4d3f128b9bb859f69238ac8b8059c8161d9ea1d27a8bf34df11b9e767c9d47d8398c48f7568bdfb88e22b44a224f7f0c818ab620aa5ddd60edf572cbab7a1586f453a2cae8279abb7816a0ebab0f26daaca97c95f189')


    databases = Databases(client)
    result = databases.list_documents('657b88927e9f558c584e', '657f0de77ebe41f89138', [Query.limit(200)],)
    print(result['documents'][0]['TickerSymbol'])
    numberdocs = int(result['total'])
    for i in range(numberdocs):
      ticker = result['documents'][i]['TickerSymbol']
      print(ticker)
      coi = 0
      poi = 0
      toi = 0
      cv = 0
      pv = 0
      tv = 0
      url1 = "https://justcors.com/l_m4lezpxv41/https://www.optionsprofitcalculator.com/ajax/"
      url2 = "getOptions?stock=" + ticker + "&reqId=12"
      url = url1 + url2

      print(url)
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
      results = requests.get(url, headers=headers)
      json = results.json()
      if(json['data_status'] == 1):
        keys = json['options'].keys()
        for i in keys:
          for y in json['options'][i]['c'].keys():
            coi = coi + json['options'][i]['c'][y]['oi']
            cv = cv + json['options'][i]['c'][y]['v']
          for z in json['options'][i]['p'].keys():
            poi = poi + json['options'][i]['p'][z]['oi']
            pv = pv + json['options'][i]['p'][z]['v']
        tv = cv + pv
        toi = coi + poi
        date = datetime.now()
        formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
        resulter = databases.create_document('657b88927e9f558c584e', '657b88a19a2856197f58', ID.unique(), {'TickerSymbol':ticker, 'TotalOI':toi, 'CallOI':coi, 'PutOI':poi, 'TotalVolume':tv, 'CallVolume':cv, 'PutVolume':pv, 'Date':formatted_date,'API':False })
        print(resulter)
    return '{"success" : "Updated Successfully", "status" : 200}'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))







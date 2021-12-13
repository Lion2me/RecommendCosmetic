from flask import Flask, render_template, request
from flask_restful import Resource, Api
import pandas as pd
import os
from os import path
import re
import sys

app = Flask(__name__)
cosapi = Api(app)

@app.route('/',methods=['GET'])
def index():
    return render_template('./main.html')

class getCOS(Resource):
    def __init__(self):
        self.POS=['NNG','NNP','NNB','VX','VA','VCN','MAG','XR']
        self.model = fd2v('../data/cc.ko.300.bin')
        self.item_df = pd.read_json('../data/스킨케어_변환.json')
        self.tag = tagging()
    def post(self):
        sent = request.form['keywords']
        sent = self.tag.get_pos([sent],pos=self.POS,result_type = 'str')[0]
        print(sent)
#        print(self.item_df['review'][0])
        scores = [ ( self.item_df['brand'][i] ,self.item_df['product'][i], self.model.get_similar_key_docs_score(sent[0],self.item_df['review'][i]+[' '.join(self.item_df['desc'][i][0])]+ [self.item_df['product'][i]] ) ) for i in range(len(self.item_df)) ]
        scores = sorted(scores, key=lambda x:x[2])[:15]
        
        result = {
        "brand":list(map(lambda x:x[0],scores)),
        "product":list(map(lambda x:x[1],scores))
    }
        
        print(scores)
        return result

cosapi.add_resource(getCOS, '/getCOS')

if __name__ == "__main__":
    
    sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
    from Lionlp.FDoc.fd2v import fd2v
    from Lionlp.util.tagging import tagging
    app.run(debug=True, host='0.0.0.0', port=7001)

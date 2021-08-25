from flask import Flask, jsonify ,request, render_template
from flask_restful import Resource, Api, reqparse
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from config_file import ENV_CONFIG
# import config vars solved here


app = Flask(__name__)
api=Api(app)

table_name      = ENV_CONFIG["TABLE_NAME"]
db_uri          = ENV_CONFIG["DB_URI"]
get_stats_url   = ENV_CONFIG['GET_STATS_URL']
get_home_url    = ENV_CONFIG['GET_HOME_URL']
''' Config file imported for Heroku deployment and has been gitignored. Please change the config_file.py file for respective environments'''


def get_col_counts(col_name, method, table=table_name):

    ''' initialises the SQLlite DB for data retrieval using the SQL Alchemy Engine'''

    engine = create_engine(db_uri, convert_unicode=True)
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    result = {}

    try:
        ''' Query for most common values returns values apart from 'NA'. Please disable/delete the filter clause if NA count needs to be returned '''

        if method.lower() == 'values':
            result['result'] = s.execute(f'select count(distinct({col_name})) as result from {table}').fetchone()[0]
        elif method.lower() == 'common':
            result['result'] = s.execute(
                f'select  {col_name},count({col_name}) filter (where {col_name} != "NA" ) as ct from {table} group by {col_name} order by ct desc limit 1').fetchone()[0]
        else:
            result['result'] = 'Invalid method please try with <values> or <common>'

    except:
        result['result'] = 'Invalid column name'

    finally:
        s.close()

    return jsonify(result)



class DbReqGet(Resource):
    ''' API get request '''

    def get(self, colname, method):
        return get_col_counts(colname, method)


class DbReqPost(Resource):
    ''' API post request '''

    def post(self):
        json_data = request.get_json(force=True)
        return  get_col_counts(json_data['column'], json_data['method'])


api.add_resource(DbReqGet,'/get-stats/<colname>/<method>')
api.add_resource(DbReqPost,'/get-stats/api')





@app.route('/home')
def home_page():
    ''' Home Landing Page rendering for HTML interface of the API '''

    return render_template('home.html',get_stats_url=get_stats_url)


@app.route('/get_stats_results',methods = ['GET','POST'])
def get_stats():
    ''' Result Set Page rendering for HTML interface of the API '''

    if request.method == 'POST':
      result = request.form
      #Not Subscriptable error resolved here by taking values from werkzeug immutable dict
      return render_template("result.html",
                             result = result,
                             get_home_url = get_home_url,
                             vals=get_col_counts(result.to_dict()['column'],result.to_dict()['method']).json['result'])



if __name__ == '__main__':
 app.run(debug = True)


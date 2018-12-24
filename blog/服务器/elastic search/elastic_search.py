# coding: utf-8

import os
import json

import requests

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado import gen

from settings import (
    ELASTIC_HOST,
    ELASTIC_PORT,
    ELASTIC_USERNAME,
    ELASTIC_PASSWORD
)

BASE_URL = 'http://%s:%s/' % (ELASTIC_HOST, ELASTIC_PORT)
BASE_DETAIL_URL = 'http://%s:%s/coupon/commodity/' % (ELASTIC_HOST, ELASTIC_PORT)

headers = {
    'Content-type': 'application/json'
}

auth = (ELASTIC_USERNAME, ELASTIC_PASSWORD)

client = AsyncHTTPClient()


TYPE_METHOD_GET = 1
TYPE_METHOD_POST = 2
TYPE_METHOD_PUT = 3
TYPE_METHOD_DELETE = 4


def _config_request(url, method=TYPE_METHOD_GET, data=None):
    if method == TYPE_METHOD_GET:
        return requests.get(url, headers=headers, auth=auth)
    elif method == TYPE_METHOD_POST:
        return requests.post(url, data=json.dumps(data), headers=headers, auth=auth)
    elif method == TYPE_METHOD_PUT:
        return requests.put(url, headers=headers, auth=auth)
    elif method == TYPE_METHOD_DELETE:
        return requests.delete(url, headers=headers, auth=auth)
    else:
        return


@gen.coroutine
def elastic_query_info(query='', category_id='', sort='',
                       price_start=0, price_end=9999999,
                       coupon_price_start=0, coupon_price_end=999999,
                       commission_start=0, commission_end=999999,
                       start_time='', end_time='',
                       shop_id=0, taobao_cids=[],
                       source=1, has_coupon=1,
                       start=0, limit=20):
    d = {
        'price': (price_start, price_end),
        'coupon_price': (coupon_price_start, coupon_price_end),
        'commission': (commission_start, commission_end),
        'last_selected_time': (start_time, end_time)
    }
    must = []
    for (key, value) in d.iteritems():
        must.append({
            'range': {
                key: {
                    'gte': value[0],
                    'lte': value[1]
                }
            }
        })

    query_filter = {
        'filter': {
            'bool': {
                'must': must
            }
        }
    }

    must = []
    match_dict = {
        'title': query,
        'shop_id': shop_id,
        'source': source,
        'category_ids': category_id
    }
    for (key, value) in match_dict.iteritems():
        if not value:
            continue

        if key == 'title':
            must.append({
                'bool': {
                    'must': {
                        'match': {
                            'title': {
                                'query': query,
                                'operator': 'and'
                            }
                        }
                    },
                    'should': {'match': {'content': query}}
                }
            })
        else:
            must.append({
                'match': {
                    key: value
                }
            })

    if must:
        query_filter.update({
            'must': must
        })

    qe = {
        'query': {
            'bool': query_filter
        },
        'sort': sort,
        'from': start,
        'size': limit
    }

    url = BASE_DETAIL_URL + '_search?pretty'
    try:
        req = HTTPRequest(url,
                          method='POST',
                          headers=headers,
                          body=json.dumps(qe),
                          auth_username=ELASTIC_USERNAME,
                          auth_password=ELASTIC_PASSWORD)
        res = yield client.fetch(req)
        result = json.loads(res.body)
        total = result['hits']['total']
        hits = result['hits']['hits']
        ids = [r['_id'] for r in hits]
    except Exception as e:
        total = 0
        ids = []
        print 'error: %s' % e
    raise gen.Return((total, ids))


def is_doc_exist(cid):
    url = BASE_DETAIL_URL + str(cid)
    try:
        r = requests.get(url, headers=headers, auth=auth)
        d = r.json()
        return d['found']
    except Exception:
        return False


def update_elastic_index(data):
    cid = data.get('id', 0)
    if not cid:
        return

    op = '_update' if is_doc_exist(cid) else '_create'
    url = BASE_DETAIL_URL + '%s/%s' % (cid, op)
    try:
        r = requests.post(url, headers=headers, data=json.dumps(data), auth=auth)
        return r.json()
    except Exception as e:
        print 'update elastic search error: %s' % e


def delete_elastic_index(cid):
    url = BASE_DETAIL_URL + str(cid)
    try:
        r = requests.delete(url, headers=headers, auth=auth)
        return r.json()
    except Exception:
        print 'delete error: %s' % cid


def analyze(query):
    url = BASE_URL + '_analyze'
    r = requests.post(url, headers=headers, data=json.dumps(query), auth=auth)
    return r.json()


def validate(query):
    query = {'query': query.get('query', '')}
    url = BASE_DETAIL_URL + '_validate/query?explain'
    r = requests.post(url, headers=headers, data=json.dumps(query), auth=auth)
    return r.json()


# 删除索引下所有的文档
def delete_by_query():
    url = BASE_DETAIL_URL + '_delete_by_query'
    query = {
        'query': {
            'match_all': {}
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(query), auth=auth)
    return r.json()


def get_index_info():
    url = BASE_URL + '_cat/indices/coupon?v'
    r = requests.get(url, headers=headers, auth=auth)
    try:
        r = requests.get(url, headers=headers, auth=auth)
        return r.text
    except Exception as e:
        print 'error: %s' % e

    
def cat_health():
    url = BASE_URL + '_cat/health?v&pretty'
    r = _config_request(url)
    return r.text


def cat_nodes():
    url = BASE_URL + '_cat/nodes?v&pretty'
    return _config_request(url).text


def cat_all_indices():
    url = BASE_URL + '_cat/indices?v&pretty'
    return _config_request(url).text


def create_indice(name):
    url = BASE_URL + '%s?pretty' % name
    print url
    return _config_request(url, method=TYPE_METHOD_PUT).json()


def create_doc(data, index_name, type_name, qid):
    url = BASE_URL + '%s/%s/%s?pretty&pretty' % (index_name, type_name, qid)
    return _config_request(url, method=TYPE_METHOD_POST, data=data).json()


def query_doc(qid, index_name, type_name):
    url = BASE_URL + '%s/%s/%s?pretty&pretty' % (index_name, type_name, qid)
    return _config_request(url, method=TYPE_METHOD_GET).json()


def bulk_docs(filename, index_name, type_name):
    cmd = 'curl -X POST -u elastic:%s "%s:%s/%s/%s/_bulk?pretty" --data-binary @%s -H "Content-type:application/json"' % (
        ELASTIC_PASSWORD, ELASTIC_HOST, ELASTIC_PORT, index_name, type_name, filename)
    return os.system(cmd)


def search(data, index_name, type_name):
    url = BASE_URL + '%s/%s/_search?pretty' % (index_name, type_name)
    return _config_request(url, method=TYPE_METHOD_POST, data=data)

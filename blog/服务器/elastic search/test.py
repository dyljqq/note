# coding: utf-8

import os
import sys
import random
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))))

from firebird.corelib.elastic_search import (
    cat_health, cat_nodes, cat_all_indices,
    create_doc, query_doc, create_indice,
    bulk_docs, search
)


TYPE_CAT_HEALTH = 1
TYPE_CAT_NODES = 2
TYPE_CAT_INDICES = 3
TYPE_UPDATE_DOC = 4
TYPE_CREATE_INDICE = 5
TYPE_BULK_DOCS = 6
TYPE_SEARCH = 7

TYPE_DICT = {
    # TYPE_CAT_HEALTH: '集群健康',
    # TYPE_CAT_NODES: '获取所有的节点',
    # TYPE_CAT_INDICES: '获取所有索引',
    # TYPE_UPDATE_DOC: '更新文档',
    # TYPE_CREATE_INDICE: '创建索引',
    # TYPE_BULK_DOCS: '批处理'
    TYPE_SEARCH: '搜索'
}

INDICE_NAME = 'lukou'
TYPE_NAME = 'lukou'


def handle(typ):
    if typ == TYPE_CAT_HEALTH:
        print cat_health()
    elif typ == TYPE_CAT_NODES:
        print cat_nodes()
    elif typ == TYPE_CAT_INDICES:
        print cat_all_indices()
    elif typ == TYPE_UPDATE_DOC:
        # print create_indice(INDICE_NAME)
        data = {
            'name': 'jqq_%s' % random.randint(0, 9999999)
        }
        r = create_doc(data, INDICE_NAME, TYPE_NAME, 1)
        print 'create doc: %s' % r
        _id = r['_id']
        r = query_doc(_id, INDICE_NAME, TYPE_NAME)
        print 'query doc: %s' % r
    elif typ == TYPE_BULK_DOCS:
        data = [
            {'index': {'_id': '1'}},
            {'name': 'Jerry'},
            {'index': {'_id': '2'}},
            {'name': 'DYL'},
        ]
        filename = '/tmp/elastic_search_test.json'
        with open(filename, 'w') as f:
            for d in data:
                f.write(json.dumps(d) + '\n')
        print bulk_docs(filename, INDICE_NAME, TYPE_NAME)
    elif typ == TYPE_SEARCH:
        data = {
            'query': {
                'bool': {
                    'must': {'match_all': {}},
                    'filter': {
                        'range': {
                            'price': {
                                'gte': 2000,
                                'lte': 9999
                            }
                        }
                    }
                }
            },
            '_source': ['price', 'title'],
            'sort': {'sort_score': {'order': 'desc'}},
            'size': 2
        }
        print 'search: %s' % data
        r = search(data, 'coupon', 'commodity')
        print r.json()


def main():
    for (key, value) in TYPE_DICT.iteritems():
        print value + ':'
        handle(key)


if __name__ == '__main__':
    main()

Title: MongoDB Index
Tags: MongoDB, Index, B-Tree
Date: 2014-02-19 13:47


本文我们讨论一下一些特殊查询对索引的使用情况。

Test data:

    rs0:PRIMARY> db.foo.find()
    { "_id" : ObjectId("52fda635720bcc4ea4bb961c"), "name" : "test_name" }
    { "_id" : ObjectId("5304412b720bcc4ea4bb9627"), "b" : 1 }
    { "_id" : ObjectId("5304430b720bcc4ea4bb9628"), "name" : null }

    rs0:PRIMARY> db.foo.ensureIndex({'name': 1})
    rs0:PRIMARY> db.foo.ensureIndex({'b': 1})

## $exists, null

    // not use index {name: 1}
    rs0:PRIMARY> db.foo.find({'name': {$exists: true}})
    { "_id" : ObjectId("52fda635720bcc4ea4bb961c"), "name" : "test_name" }
    { "_id" : ObjectId("5304430b720bcc4ea4bb9628"), "name" : null }

`{$exists: true}` will not use index `{name: 1}`.

    // use index {name: 1}
    rs0:PRIMARY> db.foo.find({'name': {$exists: false}}, {'name': 1})
    { "_id" : ObjectId("5304412b720bcc4ea4bb9627"), "b" : 1 }

`{$exists: false}` can use the index `{name: 1}`.

    // use index {name: 1}
    rs0:PRIMARY> db.foo.find({'name': null}, {'name': 1})
    { "_id" : ObjectId("5304412b720bcc4ea4bb9627"), "b" : 1 }
    { "_id" : ObjectId("5304430b720bcc4ea4bb9628"), "name" : null }

The doucment without `name` filed also show up. So when create an index on a field without `sparse` option, if an document without the filed, it will also be indexed in the index with the filed value as `null`.

Use `explain()` on the two query, the `indexBounds` of the output are the same. They both use index `{name: 1}`, and have the same time complexity, only the outputs are different.

    "nscannedObjects" : 2,
    "nscanned" : 2,
    "indexBounds" : {
            "name" : [
                    [
                            null,
                            null
                    ]
            ]
    },




## $ne

    // use index {b: 1}
    rs0:PRIMARY> db.foo.find({'b': {$ne: 1}})
    { "_id" : ObjectId("52fda635720bcc4ea4bb961c"), "name" : "test_name" }
    { "_id" : ObjectId("5304430b720bcc4ea4bb9628"), "name" : null }


explain():

    "indexBounds" : {
            "b" : [
                    [
                            {
                                    "$minElement" : 1
                            },
                            1
                    ],
                    [
                            1,
                            {
                                    "$maxElement" : 1
                            }
                    ]
            ]
    }


**NOTE:** `_id` is output by default for any query, so if you want an query to be indexOnly, you need to specify `_id: 0` on return fields.

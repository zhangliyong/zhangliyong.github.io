Title: MongoDB Index Internals
Tags: MongoDB, Index, B-Tree
Date: 2014-02-19 16:58
Modified: 2014-02-22 10:29

[TOC]

As we all know MongoDB use B-tree to create indexes, here I'll show the deep view of MongoDB indexes.

## B-tree

First, an overview of B-tree.

From wikipedia:

> In computer science, a B-tree is a tree data structure that keeps data sorted and allows searches, sequential access, insertions, and deletions in logarithmic time. The B-tree is a generalization of a binary search tree in that a node can have more than two children (Comer 1979, p. 123). Unlike self-balancing binary search trees, the B-tree is optimized for systems that read and write large blocks of data. It is commonly used in databases and filesystems.

A B-tree of order 2 or order 5:

![btree](http://upload.wikimedia.org/wikipedia/commons/thumb/6/65/B-tree.svg/500px-B-tree.svg.png "A B-tree of order 2 or order 5.")

Internal nodes can have vary number of keys, vary between $d$ and $2d$, the factor of $2$ can guarantee that nodes can be split and combined, and still conform to the upper and lower limit.

All leaf nodes have the same depth.

Definition from wikipedia:

> According to Knuth's definition, a B-tree of order m is a tree which satisfies the following properties:

> Every node has at most m children. <br />
> Every non-leaf node (except root) has at least ⌈m⁄2⌉ children.  <br />
> The root has at least two children if it is not a leaf node.  <br />
> A non-leaf node with k children contains k−1 keys.  <br />
> All leaves appear in the same level, and internal vertices carry no information.

## MongoDB Index B-tree

In this section, I will show you mongo index btree.

From [btree.h][]:

> The nodes of our btree are referred to as buckets below.  These buckets are of size BucketSize and their body is an ordered array of <bson key, disk loc> pairs, where disk loc is the disk location of a document and bson key is a projection of this document into the schema of the index for this btree.  Ordering is determined on the basis of bson key first and then disk loc in case of a tie.  All bson keys for a btree have identical schemas with empty string field names and may not have an objsize() exceeding KeyMax.  The btree's buckets are themselves organized into an ordered tree.

This is what btree looks like:

![index btree](https://www.evernote.com/shard/s30/sh/58663d76-cf6f-4944-943b-fb850f3084b1/3bc5e37b28b267f8cd2e374e99d0d59c/deep/0/Btree.jpg)

When the btree is serialized on the disk, every bucket is stored as a record, like a document in a collection. Each bucket has a fixed size 8192, but with 16 byte to store record header. See [mongo storage]({filename}./mongodb-storage.md).


Bucket store keynode and keydata, this is what bucket looks like:

![index bucket](https://www.evernote.com/shard/s30/sh/3a7cb4c5-d387-4335-b1b4-920d7510091e/33b58b26c816e9621cd556325ceeb8d2/deep/0/From-Skitch.jpg)

`prevChildBucket` is a pointer, point to the left child bucket of this key. `kdo` points to the key data of this key. `recordLoc` points to the location of the key's doucment.

keynode is a struct, and has a fixed size.

    template< class Loc >
    struct __KeyNode {
        /**
         * The 'left' child bucket of this key.  If this is the i-th key, it
         * points to the i index child bucket.
         */
        Loc prevChildBucket;
        /** The location of the record associated with this key. */
        Loc recordLoc;
        /** Offset within current bucket of the variable width bson key for this _KeyNode. */
        unsigned short _kdo;
    }

The size of keydata varies, with upper limit 1024 bytes.

When insert a new key to a bucket, keynode is inserted from left, and keydata is insert from right.

Bucket format:

     |hhhh|kkkkkkk————bbbbbbbbbbbuuubbbuubbb|
     h = header data
     k = KeyNode data
     - = empty space
     b = bson key data
     u = unused (old) bson key data, that may be garbage collected

So how many keys can be stored in a bucket depends on keydata size. MongoDB allows to store 1024 keys at most. When the bucket is full, or has 1024 keys, it will be splited.

keydata is a projection of a document into the schema of the index. For an index, the schema is fixed, so keydata does not need to contain fieldNames. If a document does not have a field, then the fileValue will be null in keydata.

**Sparse:**
When create a sparse index, only when the document does not have all the fields of the index, it will be ignore, if one of the fields exists, it will be indexed.

**Example:**

index:

    {name: 1, age: 1}

documents:

    d1: {name: 'Tom', age: 23}          keydata: Tom,23
    d2: {name: null,  age: 40}          keydata: null,40
    d3: {name: 'Jerry', address: CA}    keydata: Jerry,null
    d4: {weight: 70,  address: CA}      keydata: null,null

If create the index with sparse as true, the document `d4` will not be indexed.


### IndexStats

MongoDB 2.4 ships with a `indexStats` command, the command can be run only on a mongod instance that uses the `--enableExperimentalIndexStatsCmd` option.

To aggregate statistics, issue the command like so:

    db.runCommand( { indexStats: "<collection>", index: "<index name>" } )

## Reference

<http://en.wikipedia.org/wiki/B-tree>
<https://github.com/mongodb/mongo/blob/master/src/mongo/db/structure/btree/btree.h>
<https://github.com/mongodb/mongo/blob/master/src/mongo/db/structure/btree/btree.cpp>


[btree.h]: https://github.com/mongodb/mongo/blob/master/src/mongo/db/structure/btree/btree.h

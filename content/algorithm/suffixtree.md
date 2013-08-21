Title: Generalized Suffix Tree


本文提供了另一种构造generalized suffix tree的方法，不需要为每个字符串添加惟一的字符，所以可以为任意数量的字符串构造后缀树。
构造原理依然采用Ukkonen提出的算法。下面我们由简入深分别介绍此种方式应对的问题。

## 前言
后缀树可以用来快速的对字符串进行搜索，详细信息推荐阅读：http://en.wikipedia.org/wiki/Suffix_tree，

后缀树的搜索非常快，但是构造后缀树比较复杂， Ukkonen提出的构造后缀树的算法时间复杂度为O(nlogn), 构造原理阅读
http://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english，本文也是在此链接
的基础上进行说明的。 **所以在继续阅读前确保你已经阅读了此链接的内容。**

suffix tree是一个字符串的所有后缀组成的一棵树。
在很多情况下我们有多个字符串，需要为这些字符串构造同一棵后缀树，即是generalized suffix tree，例如查询包含'abc'的所有字符串。

如需要为n个字符串（如s1, s2, s3, ..., sn）构造后缀树，目前通用的做法是找到n个不同的字符, 如u1, u2,..., un，
这n个字符是惟一的，且不会出现在所有的字符串中，然后将每个字符加到一个字符串后，并将它们合并，组成一个字符串：
s=s1u1s2u2.....snun，并为s构造后缀树。

例如为"ab", "abc"构造后缀树，找到两个字符"#", "$"，我们得到字符中abc#abcde$"，然后为其构造后缀树，如图:

![](static/images/suffix_tree/ab_abc.png)

当有少量字符串的时候，这种方式比较实用，我们可以很轻易找到n个不同的字符，当字符串比较多时，
我们很难找到这么多不同的字符。目前unicode的码点是从0到0x10ffff，也就是unicode最多能表示1114111个字符，仅仅是百万级。
所以假如我们有千万级的字符串时，我们就找不到如此多的字符了。

我们提供了另一种解决方案。

##准备
我们在原有的基础上进行了改进。

1. 为每个字符串设置一个惟一的索引(index)，用于标识此字符串，根据索引可找到原来的字符串。
2. 除根结点以外的所有结点都有suffix link。说明为什么加suffix link
3. 每条边有三个属性index, start, length，根据这三个属性可找到此边代表的字符串。
4. 叶结点会存储索引值（有些结点即为叶结点也为中间结点）。 //TODO 说明为什么加索引

第3条很容易理解，第1条是为第3、4条准备的，是为降低空间复杂度。下面我们对2、3进行说明。

从根结点到每个叶结点的路径代表一个字符或多个字符串的后缀，叶结点上的索引即是这些字符串的索引。

##基本

以字符串"ab"为例，其后缀树为：

![](static/images/suffix_tree/ab.png)

设置"ab"的索引为0，将索引加到叶结点中为:

![](static/images/suffix_tree/ab_index.png)

##扩展一
字符串末尾字符为重复字符，为"aba"为例，
为其构造后缀树并将索引加到叶结点后：

![](static/images/suffix_tree/aba_index_1.png)

此时active point为(root, 'a', 1), remainder为1，即我们还有一个后缀，隐含在后缀树中，
而此时字符串中所有的字符都已加到后缀树中，我们需要为此后缀创建一个叶结点，并将索引0加到叶结点中。

如图：

![](static/images/suffix_tree/aba_index_2.png)

红色的结点即是我们创建的，这个结点即是叶结点也是中间结点，对于后缀'a'来说是叶结点，
对于后缀'aba'来说是中间结点。

对于叶结点在创建的时候我们即可将索引加到叶结点中。

当字符串的所有字符都加入到后缀树之后，remainder的值即是隐式后缀的数量，我们需要为这些后缀指定索引。

如果active length为0，不需要创建结点，只需要将索引加入到active node中即可。

如字符串"abcabdab"，将所以字符加到后缀树后：

![](static/images/suffix_tree/abcabdab_index_1.png)

此时active point为(blue node, \0, 0), remainder为2。

后缀"ab", "a"为隐式，此时active length为0，将索引加到active node中后，如图：

![](static/images/suffix_tree/abcabdab_index_2.png)


## 扩展二
在后缀树中加入一个新的字符串。

在加入新的字符串之前，需要重置active point为(root, '\0', 0)。

以字符串"ab", "abc"为例, "ab"的索引为0, "abc"的索引为1，

"ab"的后缀树：

![](static/images/suffix_tree/ab_index_1.png)

我们需要向此后缀树中加入字符串"abc"，

在我们加入字符'ab'之后，后缀并没有发生变化，此时active point为(blue node, '\0', 0)，remainder为2.

我们继续加入字符"c"，在active node下加入一条边，如图：

![](static/images/suffix_tree/ab_abc_index_1.png)

此时remainder变为2，active node指向红色结点，由于我们之前为叶结点创建了suffix link，更新active node的时间复杂度依然为O(1)。

最终结果如图：

![](static/images/suffix_tree/ab_abc_index_2.png)


下面给出程序的伪代码：

    for char in text:
        remainder ++
        while remainder > 0:
            canonize // make sure the active_length is no longer than active_edge

            if active_length is 0
                edge = get edge whose label starts with char from active node
                if edge is none:
                    insert a edge whose label starts with char
                    insert index to the leaf node of the edge

                    update suffix link
                else:
                    update active point
                    break

            else:
                if active_edge[active_length] == char:
                    update active point

                    if char is the last char:
                        add index to all the remainder suffix
                    break
                else:
                    split current active_edge at active_length with an internal node
                    insert an new edge starts with char at the internal node
                    insert index to the leaf node of the new edge

                    update suffix link

            update active point

## 搜索

搜索与普通的后缀树搜索类似，根据要搜索的字符串在树中依次匹配即可。

当模式最终匹配到某一条边后，后到这条边的目标结点，则以这个结点为根结点的子树中的所有索引就是此次的搜索结果。
再根据索引可得到原来的字符串。

例如在后缀树

![](static/images/suffix_tree/ab_abc_index_2.png)

中查找'b'时，可找到索引0，1，再根据索引找到原来的字符串。

## 复杂度

### 时间
由于构造后缀树和搜索的原理与之前的一样，

假定所有字符串的长度之和为n，则构造后缀树的时间复杂度为O(nlogn)。

模式P的长度为|P|，则搜索的时间复杂度为O(|P|)

### 空间
TODO


笔者给出了一个python版本的实现。

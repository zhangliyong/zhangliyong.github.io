Title: Graphviz Tutorial
Tags: Tools, Graphviz, Tutorial
Date: 2014-02-23 15:37
Modified: 2014-02-24 11:05


When I write something, I'd like to use graphes, graph is a great way to explain ideas, it can save a lot of words, and express more clearlly.

Is there a good tool which make you drawing graphes like programming, yes there is, the great [Graphviz][graphviz]. The first time I saw it, I was shocked by its powerful, it can draw some many kinds of beautiful graphes. You can learn graphviz through its [offcial website][graphviz], the documents there are a little hard for newbies, and as a know there is no much toturials for graphviz when I'm writting this, so I want to write a tutorial for it. More people need to know this tool.


## What is Graphviz

From offcial website:

>Graphviz is open source graph visualization software. Graph visualization is a way of representing structural information as diagrams of abstract graphs and networks. It has important applications in networking, bioinformatics,  software engineering, database and web design, machine learning, and in visual interfaces for other technical domains. 

![demo](http://graphviz.org/Gallery/directed/cluster.png)

Graphviz package shiped with some programs and libs, the programs can take descriptions of graphs in a text language([The DOT Language][dot-lang])), and generate graphs in various useful formats, like png, svg, pdf, ps. Graphviz has many userful features, you can custome colors, fonts, styles.

I will introduce to you two command line programs, `dot` and `neato`. They are enough for general use, if you have special needs, look into the [documents](http://graphviz.org/Documentation.php).

## dot, neato
`dot` : a utility program for drawing directed graphs. 

`neato` : a utility program for drawing undirected graphs.

They have the same usages. Run `dot -?` for help.

    dot -Tsvg hello_world.dot -o hello_world.svg

`dot` take `hello_world.dot` as input, and generate svg file `hello_world.svg`.

`-T` option takes graph format, you can assign other formats, like png, pdf, ps.

hello_world.dot:

[gist:id=9169048,file=hello_world.dot]

hello_world.svg:

![Hello World]({filename}/images/graphviz/hello_world.svg)

`hello_world.dot` is a description in dot language.

## The DOT Language
Now I introduce [the dot language][dot-lang] to you.

Grammar defination:

[gist:id=9169048,file=dot-lang.md]

It's pretty abstract and not clear for newbies.
I'll explain to you by examples, once you understand these grammars, you can draw graphes freely.


### We start with `hello_world.dot`,

    /*
     * graph: [ strict ] (graph | digraph) [ ID ] '{' stmt_list '}'
     *
     * hello is ID, the body is the "stmt_list"
     */
    digraph hello
    {
           /* node_stmt: node_id [ attr_list ]
            * node_id: ID [ port ]
            * attr_list	:'[' [ a_list ] ']' [ attr_list ]
            * a_list: ID '=' ID [ (';' | ',') ] [ a_list ]
            * 
            * n1 is ID of a node_id
            * '[label="Hello"]' is attr_list
            * 'label="Hello"' is a_list
            */
           n1 [label="Hello"]
           n2 [label="World!"]
     
           /* edge_stmt: (node_id | subgraph) edgeRHS [ attr_list ]
            * edgeRHS: edgeop (node_id | subgraph) [ edgeRHS ]
            * 
            * 'n1' is node_id
            * '-> n2' is edgeRHS
            * '->' is edgeop
            * 'n2' is node_id
            */
           n1 -> n2
    }

An edgeop is "->" in directed graphs and "--" in undirected graphs.

### Next we add attr to graph

    attr_stmt	:	(graph | node | edge) attr_list


attr: <http://graphviz.org/content/attrs>

node-shapes: <http://graphviz.org/content/node-shapes>

arrow-shapes: <http://graphviz.org/content/arrow-shapes>

colors: <http://graphviz.org/doc/info/colors.html>


## Ref
<http://graphviz.org/>
<http://www.linuxjournal.com/article/7275?page=0,0>

[graphviz]: http://graphviz.org/
[dot-lang]: http://graphviz.org/content/dot-language

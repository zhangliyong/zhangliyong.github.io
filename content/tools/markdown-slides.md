Title: Use markdown to create presentation
Slug: markdown-to-slides
Date: 2014-04-27 16:20
Tags: markdown, pandoc, tools

Sometimes I need to prepare a presentation, there are a lot of tools I can use, like keynotes, powerpoint, latex. I used to use latex beamer, it can generate very beautiful slides, and there are a lot of themes to choos. But the latex source code is not easy to write and clear.

I love markdown, which is very popular now, I want to write source code using markdown, and generate a pdf file as beautiful as beamer. There is a powerful tool can do this, it's pandoc(<http://johnmacfarlane.net/pandoc/>), it can convert one markup format to another, and support most of formats.

Here I use pandoc to convert markdown to beamer

    pandoc -V theme:Warsaw -t beamer -o slides.pdf slides.md

I specify theme `Warsaw` to use with `-V` option.

pandoc official website show how to wite markdown to producing slides:
<http://johnmacfarlane.net/pandoc/demo/example9/producing-slide-shows-with-pandoc.html>

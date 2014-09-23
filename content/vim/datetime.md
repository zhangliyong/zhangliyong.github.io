Title: Insert datetime in vim
Date: 2014-05-05 10:29


    ## insert current date
    "map F3 to insert current date
    nnoremap <F3> "=strftime("%Y-%m-%d (%a)")<CR>P
    inoremap <F3> <C-R>=strftime("%Y-%m-%d (%a)")<CR>

<http://vim.wikia.com/wiki/Insert_current_date_or_time>

<http://vim.wikia.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_1)>

<http://stackoverflow.com/questions/1218390/what-is-your-most-productive-shortcut-with-vim/1220118#1220118>

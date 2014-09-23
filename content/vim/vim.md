Title: vim

TODO: wrap my plugins

## auto reload .vimrc

    augroup reload_vimrc " {
        autocmd!
        autocmd BufWritePost $MYVIMRC source $MYVIMRC
    augroup END " }

http://www.bestofvim.com/tip/auto-reload-your-vimrc/


Title: Problems I encouter with emacs

emacs with zsh

when I first open zsh in emacs using:

    M-x term

It always print strange characters like "4m", that's because I don't have eterm-color terminfo,
I solve this problem by running:

    # If you use Cocoa Emacs or Carbon Emacs
    tic -o ~/.terminfo /Applications/Emacs.app/Contents/Resources/etc/e/eterm-color.ti

in terminal.

ref: http://stackoverflow.com/questions/8918910/weird-character-zsh-in-emacs-terminal

-smart-case
--sort-files
--color
--type-set=rst:ext:rst,txt
--type-set=md:ext:mkd,md,markdown


ACKRC LOCATION SEMANTICS
       Ack can load its configuration from many sources.  This list specifies the sources Ack looks for configuration; each one that is
       found is loaded in the order specified here, and each one overrides options set in any of the sources preceding it.  (For example,
       if I set --sort-files in my user ackrc, and --nosort-files on the command line, the command line takes precedence)

       ·   Defaults are loaded from App::Ack::ConfigDefaults.  This can be omitted using "--ignore-ack-defaults".

       ·   Global ackrc

           Options are then loaded from the global ackrc.  This is located at "/etc/ackrc" on Unix-like systems, and "C:\Documents and
           Settings\All Users\Application Data" on Windows.  This can be omitted using "--noenv".

       ·   User ackrc

           Options are then loaded from the user's ackrc.  This is located at "$HOME/.ackrc" on Unix-like systems, and "C:\Documents and
           Settings\$USER\Application Data".  If a different ackrc is desired, it may be overridden with the $ACKRC environment variable.
           This can be omitted using "--noenv".

       ·   Project ackrc

           Options are then loaded from the project ackrc.  The project ackrc is the first ackrc file with the name ".ackrc" or "_ackrc",
           first searching in the current directory, then the parent directory, then the grandparent directory, etc.  This can be omitted
           using "--noenv".

       ·   ACK_OPTIONS

           Options are then loaded from the environment variable "ACK_OPTIONS".  This can be omitted using "--noenv".

       ·   Command line

           Options are then loaded from the command line.

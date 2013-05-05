Title: Pythonbrew

home page: https://github.com/utahta/pythonbrew

##install packages over pythonbrew

pythonbrew can install multiple python versions on the same machine,
if you want to install packages over a specified python version, a
recommand way is to install pip first.

### install pip

home page: http://www.pip-installer.org/en/latest/

pip is just a python pacakge

first use pythonbrew switch to the desired python version, then

    $ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    $ [sudo] python get-pip.py

after that you can use pip to install whatever pacakges over the python version.


If you want to install package on a different python version, re-do "install pip" section.

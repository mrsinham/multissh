# Qi (parallel request)

Qi is a simple tool based on Paramiko framework to execute a parallel query on multiple servers.


## Basic usage

Qi use its configuration file, `~/.qi`, see the configuration section. Copy qi.example to `~/.qi` to start a new conf file

    usage: main.py [-h] [-e EXECUTE] [-s SERVERALIAS] [-c COMMAND]
                   [-a [ARGS [ARGS ...]]]

    Execute multiple commands in qi on server

    optional arguments:
      -h, --help            show this help message and exit
      -e EXECUTE, --execute EXECUTE
                            Command to execute
      -s SERVERALIAS, --serveralias SERVERALIAS
                            Servers alias as specified in configuration file
      -c COMMAND, --command COMMAND
                            prefilled command in the cmd section
      -a [ARGS [ARGS ...]], --args [ARGS [ARGS ...]]


## Executing a simple command on multiple servers based on the list of configuration file

    $ qi -s myserverlist -e 'ls /tmp/ | wc -l'

This will execute the command on each server contained in the `[server]` section in the ~/.qi config file (see qi.example)


## Executing a precorded command on multiple servers

    $ qi -s myserverlist -c mycommand

This will execute the command "mycommand" recorded in the `[cmd]` section on the server list myserverlist. If the command
is declared like this :

    displaylogservers=servers, ls -lht /var/log/

You won't need to run the command with a -s serverlist, the displaylogservers will run automatically on the "servers" list :

    $ qi -c displaylogservers
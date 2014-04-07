Adium Shell
==========

.. image:: https://pypip.in/v/adium-sh/badge.png
        :target: https://pypi.python.org/pypi/adium-sh

Adium Shell (adium-sh) is a command-line Python wrapper for Adium.

Description
-----------
adium-sh is based on the Python wrapper that utilized `AppleScript support <https://trac.adium.im/wiki/AppleScript_Support_1.2>`_ of Adium.

Feature
-------

The current features are:

* Set default service and account
* Send messages using exact account name or alias
* Receive and reply to messages using patterns or external API (SimSimi currently supported)
* React to events

Installation
------------
::

    $ pip install adium-sh

Usage
-----
You must specify the account and service to associate with the current use, either as command-line arguments or in the config file. When specifying them as arguments, you must put them before the sub-commands.

Send messages
~~~~~~~~~~~~~
Send a message using account name:
::

    $ adiumsh -s GTalk -t yourname@gmail send -b buddy@gmail.com
    Hello, there
    <<EOF

Send a message using alias:
::

    $ adiumsh -s GTalk -t yourname@gmail.com send -a 'John Smith'
    Hello, there
    <<EOF

Set default configuration file at ``~/.adiumsh``:
::

    [default]
    service = GTalk
    account = yourname@gmail.com

Then you can send messages without specifying ``-s/--service`` and ``-t/--account``:
::

    $ adiumsh send -a 'John Smith'

You can also pass as argument your message:
::

    $ adiumsh send -a 'John Smith' -m 'Hello, there'

Receive messages
~~~~~~~~~~~~~~~~
You must specify a chat method to receive messages. By default, adium-sh uses "Simple Chat", which basically replies to received messages according to the patterns you set. You must set the patterns in the config file, possibly like the following settings::

    [default]
    service = GTalk
    account = yourname@gmail.com

    [chat-default]
    type = wildcard
    patterns = 
        *hello*: hi
        *what*: sorry	
        *: I'm not available now

Then, you can invoke the "receive" sub-command with the ``-c/--chat`` arguments::

    $ adiumsh receive -c default 

The patterns is a list of string pairs where each pair is separated by a colon. The string to the left of the colon is the pattern against which the received text will be matched, and the right one is the corresponding reply text. There is also a "type" option in the chat section, which defaults to "wildcard" that uses globbing pattern matching; another value to it is "regex", which uses regular expression.

You can also use "SimSimi Chat" which hits the SimSimi API with the messages received. You have to set the API key in the config file and the key type ("trial", which is default, or "paid")::

    [chat-simi]
    simi-key = some-really-long-key
    simi-key-type = trial

Then, invoke "receive" with this chat from command line::

    $ adiumsh receive -c simi

Set the default chat in the default settings::

    [default]
    service = GTalk
    account = yourname@gmail.com
    chat = default

    [chat-default]
    patterns = 
        *hello*: hi
        *what*: sorry	
        *: I'm not available now

    [chat-another]
    patterns =
        *: not here

Now you can also switch between chats from the command line other than the default::

    $ adiumsh receive -c another

TODO
----
* Complete Python wrapper API to AppleScript support
* Exhaustive commands based on the wrapper

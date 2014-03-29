adium-sh
==========

.. image:: https://pypip.in/v/adium-sh/badge.png
        :target: https://pypi.python.org/pypi/adium-sh

adium-sh is a command-line Python wrapper for Adium.

Description
-----------
adium-sh is based on the Python wrapper that utilized `AppleScript support <https://trac.adium.im/wiki/AppleScript_Support_1.2>`_ of Adium.

Feature
-------

The current features are:

* Send messages using exact account name or alias
* Set default service and account for alias

Installation
------------
::

    $ pip install adium-sh

Usage
-----


Examples
~~~~~~~~
Send a message using account name:
::

    $ adiumsh send -b buddy@gmail.com
    Hello, there
    <<EOF

Send a message using alias:
::

    $ adiumsh send -a 'John Smith' -s GTalk -t yourname@gmail.com
    Hello, there
    <<EOF

Set default configuration file at ``~/.adiumsh``:
::

    [default]
    service = GTalk
    account = yourname@gmail.com

And you can send to alias without specifying ``-s/--service`` and ``-t/--account``:
::

    $ adiumsh send -a 'John Smith'

You can also pass as argument your message:
::

    $ adiumsh send -a 'John Smith' -m 'Hello, there'

TODO
----
* Complete Python wrapper API to AppleScript support
* Exhaustive commands based on the wrapper

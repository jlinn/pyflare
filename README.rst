pyflare
=======

.. image:: https://secure.travis-ci.org/jlinn/pyflare.png?branch=master
        :target: http://travis-ci.org/jlinn/pyflare

About
-----

Pyflare is a Python adapter for `CloudFlare's Client API <http://www.cloudflare.com/docs/client-api.html>`_.

Installation
------------

.. code-block:: bash

    $ pip install pyflare

Usage
-----

.. code-block:: python

    from pyflare import Pyflare
    cf = Pyflare('address@example.com', 'your_api_key')
    # Create a new A record
    response = cf.rec_new('example.com', 'A', 'sub', '1.2.3.4')
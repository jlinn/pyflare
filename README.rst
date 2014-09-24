pyflare
=======

.. image:: https://secure.travis-ci.org/jlinn/pyflare.png?branch=master
        :target: http://travis-ci.org/jlinn/pyflare

About
-----

Pyflare is a Python adapter for `CloudFlare's Client API <http://www.cloudflare.com/docs/client-api.html>`_ and `CloudFlare's Hosting provider API <http://www.cloudflare.com/docs/host-api.html>`_.

Installation
------------

.. code-block:: bash

    $ pip install pyflare

Usage
-----

.. code-block:: python

    from pyflare import PyflareClient
    cf = PyflareClient('address@example.com', 'your_api_key')
    # Create a new A record
    response = cf.rec_new('example.com', 'A', 'sub', '1.2.3.4')


    from pyflare import PyflareHosting
    hf = PyflareHosting('your_host_api_key')
    # Authenticate a user
    response = hf.user_auth('one@example.com', 'user_password')

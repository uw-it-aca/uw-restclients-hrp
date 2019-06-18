# REST client for the UW HRP Web Service
# UW-RestClients-HRP

[![Build Status](https://api.travis-ci.org/uw-it-aca/uw-restclients-hrp.svg?branch=master)](https://travis-ci.org/uw-it-aca/uw-restclients-hrp)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/uw-restclients-hrp/badge.png?branch=master)](https://coveralls.io/r/uw-it-aca/uw-restclients-hrp?branch=master)

Installation:

    pip install UW-RestClients-HRP

To use this client, you'll need these settings in your application or script:

   RESTCLIENTS_HRPWS_HOST='https://...'

Optional settings:

    # Customizable parameters for urllib3
    RESTCLIENTS_HRPWS_TIMEOUT=60
    RESTCLIENTS_HRPWS_POOL_SIZE=10

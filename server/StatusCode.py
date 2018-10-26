#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class StatusCode:
    success = {
        200:'200:OK'
    }

    failure = {
        400:'400:Not enough money',
        401:'401:First argument must be an int',
        402:'402:Not enough shares owned',
        403:'403:Bad request',
        404:'404:Marketplace not found',
        405:'405:Negative shares value',
        501:'501:No value for this marketplace'
    }

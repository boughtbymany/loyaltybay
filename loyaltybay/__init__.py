"""
Wrapper for Loyalty Bay API
"""

# Reference: https://www.loyaltybay.co.uk/documentation/api

import json
from requests import request, ConnectionError


class LoyaltyBayError(Exception):
    pass


class LoyaltyBayAPI():

    ENDPOINT = 'https://api.loyaltybay.co.uk/api/v1'

    def __init__(self, token, endpoint=None):
        self._api_token = token
        self._api_endpoint = endpoint or self.ENDPOINT

    def _call(self, method, url, params=None, data=None):
        headers = {
            'Content-Type': 'application/json',
            'apikey': self._api_token,
        }

        try:
            response = request(
                method, 
                '%s%s' % (self._api_endpoint, url),
                params=params,
                data=json.dumps(data),
                headers=headers
            )
        except ConnectionError as err:
            raise LoyaltyBayError('Unable to connect to Loyalty Bay!')

        return response

    def _process(self, response):
        try:
            response_data = response.json()
        except ValueError as err:
            raise LoyaltyBayError('Unprocessable response! %s' % err)

        data = {}

        if response.status_code == 401:
            raise LoyaltyBayError('Invalid API details!')

        elif response.status_code == 400 or response.status_code == 500:
            message = ''

            if 'message' in response_data:
                message = response_data['message']

            raise LoyaltyBayError('Error! %s %s' % (
                response.status_code,
                message,
            ))

        elif response.status_code == 200:

            if 'data' in response_data:
                data = response_data['data']
            else:
                data = response_data

        return data

    # API Methods



    def publisher_campaign(self, campaign, uuid):
        response = self._call('GET', '/publisher_campaigns/%s' % campaign, params={
            'uuid': uuid,
        })
        result = self._process(response)

        if 'publisher_campaign' in result:
            return result['publisher_campaign']

        return result

    def create_choice(self, uuid, publisher_campaign_identifier, 
        advertiser_campaign_identifier):
        response = self._call('POST', '/choices', data={
            'uuid': uuid,
            'publisher_campaign_identifier': publisher_campaign_identifier,
            'advertiser_campaign_identifier': advertiser_campaign_identifier,
        })
        result = self._process(response)

        if 'status' in result and result['status'] == 'success':
            return True

        return False

    def create_conversion(self, uuid, publisher_campaign_identifier, email, name, 
        postcode=None, advertiser_campaign_identifier=None):
        response = self._call('POST', '/conversions', data={
            'uuid': uuid,
            'publisher_campaign_identifier': publisher_campaign_identifier,
            'email': email,
            'name': name,
            'postcode': postcode or '',
            'advertiser_campaign_identifier': advertiser_campaign_identifier or '',
        })
        result = self._process(response)

        if 'status' in result and result['status'] == 'success':
            return True

        return False

    def defer_conversion(self, uuid, publisher_campaign_identifier, reconciliation_id):
        response = self._call('POST', '/conversions/defer', data={
            'uuid': uuid,
            'publisher_campaign_identifier': publisher_campaign_identifier,
            'reconciliation_id': reconciliation_id,
        })
        result = self._process(response)

        if 'status' in result and result['status'] == 'success':
            return True

        return False

    def complete_defered_conversion(self, reconciliation_id, email, name, postcode=None):
        response = self._call('POST', '/conversions/complete_deferred', data={
            'reconciliation_id': reconciliation_id,
            'email': email,
            'name': name,
            'postcode': postcode or '',
        })
        result = self._process(response)

        if 'status' in result and result['status'] == 'success':
            return True

        return False

if __name__ == '__main__':
    lb = LoyaltyBay(
        '<some API token>'
    )

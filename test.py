"""
Simple test of functionality...
"""

import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import loyaltybay


def main():

    lb = loyaltybay.LoyaltyBayAPI(
        'YOUR_API_KEY'
    )

    publisher_campaigns = lb.publisher_campaigns()

    for campaign in publisher_campaigns:
        print(campaign['identifier'])

    if len(publisher_campaigns) == 0:
        return 

    identifier = publisher_campaigns[0]['identifier']

    campaign = lb.publisher_campaign(identifier, '12345')

    if not 'identifier' in campaign:
        return 

    print('')
    print(campaign['name'])
    print('-' * len(campaign['name']))

    for ad in campaign['advertiser_campaigns']:
        print(ad['name'])
        print(ad['description'])
        print(ad['details'])
        print('')


if __name__ == '__main__':
    main()
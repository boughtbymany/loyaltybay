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

    # AF Hi nick, I set this to none because you would need to specify this from e.g. env
    identifier = None

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
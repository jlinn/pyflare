__author__ = 'Vanc Levstik'

import requests
from pyflare import APIError


class PyflareHosting(object):

    CLOUDFLARE_URL = 'https://api.cloudflare.com/host-gw.html'

    def __init__(self, host_key):
        """
        Instantiate a Pyflare client object
        :param email: The host_key associated with your Cloudflare account
        :type email: str
        :param email: The user_key associated with user for which you are
        changing settings.
        :type email: str
        """
        self._host_key = host_key

    def host_key_regen(self):
        """
        Regenerate your host key

        :returns:
        :rtype:   dict
        """
        return self._request({'act': 'host_key_regen'})

    def user_create(self, cloudflare_email, cloudflare_pass, unique_id=None):
        """
        Create new cloudflare user with selected email and id. Optionally also
        select unique_id which can be then used to get user information.

        :param    cloudflare_email: new user cloudflare email
        :type     cloudflare_email: str
        :param    cloudflare_pass:  new user cloudflare password
        :type     cloudflare_pass:  str
        :param    unique_id:        new user unique id
        :type     unique_id:        str (optional)

        :returns:
        :rtype:   dict
        """
        params = {
            'act': 'user_create',
            'cloudflare_email': cloudflare_email,
            'cloudflare_pass': cloudflare_pass
        }
        if unique_id:
            params['unique_id'] = unique_id
        return self._request(params)

    def zone_set(self, user_key, zone_name, resolve_to, subdomains):
        """
        Create new zone for user associated with this user_key.

        :param    user_key:   The unique 3auth string,identifying the user's
        CloudFlare Account. Generated from a user_create or user_auth
        :type     user_key:   str
        :param    zone_name:  The zone you'd like to run CNAMES through CloudFlare for, e.g. "example.com".
        :type     zone_name:  str
        :param    resolve_to: The CNAME that CloudFlare should ultimately
        resolve web connections to after they have been filtered
        :type     resolve_to: str
        :param    subdomains: A comma-separated string of subdomain(s) that
        CloudFlare should host, e.g. "www,blog,forums"
        :type     subdomains: str

        :returns:
        :rtype:   dict
        """
        params = {
            'act': 'zone_set',
            'user_key': user_key,
            'zone_name': zone_name,
            'resolve_to': resolve_to,
            'subdomains': subdomains,
        }
        return self._request(params)

    def full_zone_set(self, user_key, zone_name):
        """
        Create new zone and all subdomains for user associated with this
        user_key.

        :param    user_key:   The unique 3auth string,identifying the user's
        CloudFlare Account. Generated from a user_create or user_auth
        :type     user_key:   str
        :param    zone_name:  The zone you'd like to run CNAMES through CloudFlare for, e.g. "example.com".
        :type     zone_name:  str

        :returns:
        :rtype:   dict
        """
        params = {
            'act': 'full_zone_set',
            'user_key': user_key,
            'zone_name': zone_name,
        }
        return self._request(params)

    def user_lookup(self, cloudflare_email=None, unique_id=None):
        """
        Lookup user data based on either his cloudflare_email or his
        unique_id.

        :param    cloudflare_email: email associated with user
        :type     cloudflare_email: str
        :param    unique_id:        unique id associated with user
        :type     unique_id:        str

        :returns:
        :rtype:   dict
        """
        if not cloudflare_email and not unique_id:
            raise KeyError(
                'Either cloudflare_email or unique_id must be present')

        params = {'act': 'user_lookup'}
        if cloudflare_email:
            params['cloudflare_email'] = cloudflare_email
        else:
            params['unique_id'] = unique_id

        return self._request(params)

    def user_auth(
        self,
        cloudflare_email=None,
        cloudflare_pass=None,
        unique_id=None
            ):
        """
        Get user_key based on either his email and password or unique_id.

        :param    cloudflare_email: email associated with user
        :type     cloudflare_email: str
        :param    cloudflare_pass: pass associated with user
        :type     cloudflare_pass: str
        :param    unique_id:        unique id associated with user
        :type     unique_id:        str

        :returns:
        :rtype:   dict
        """
        if not (cloudflare_email and cloudflare_pass) and not unique_id:
            raise KeyError(
                'Either cloudflare_email and cloudflare_pass or unique_id must be present')
        params = {'act': 'user_auth'}
        if cloudflare_email and cloudflare_pass:
            params['cloudflare_email'] = cloudflare_email
            params['cloudflare_pass'] = cloudflare_pass
        else:
            params['unique_id'] = unique_id

        return self._request(params)

    def zone_lookup(self, user_key, zone_name):
        """
        Lookup selected zone for a user.

        :param    user_key:  key for authentication of user
        :type     user_key:  str
        :param    zone_name: name of zone to lookup
        :type     zone_name: str

        :returns:
        :rtype:   dict
        """
        return self._request({
            'act': 'zone_lookup',
            'user_key': user_key,
            'zone_name': zone_name
        })

    def zone_delete(self, user_key, zone_name):
        """
        Delete selected zone for a user.

        :param    user_key:  key for authentication of user
        :type     user_key:  str
        :param    zone_name: name of zone to lookup
        :type     zone_name: str

        :returns:
        :rtype:   dict
        """
        return self._request({
            'act': 'zone_delete',
            'user_key': user_key,
            'zone_name': zone_name
        })

    def zone_list(
        self,
        user_key,
        limit=100,
        offset=0,
        zone_name=None,
        sub_id=None,
        zone_status='ALL',
        sub_status='ALL',
            ):
        """
        List zones for a user.

        :param    user_key:  key for authentication of user
        :type     user_key:  str
        :param    limit: limit of zones shown
        :type     limit: int
        :param    offset: offset of zones to be shown
        :type     offset: int
        :param    zone_name: name of zone to lookup
        :type     zone_name: str
        :param    sub_id: subscription id of reseller (only for use by resellers)
        :type     sub_id: str
        :param    zone_status: status of zones to be shown
        :type     zone_status: str (one of: V(active), D(deleted), ALL)
        :param    sub_status: status of subscription of zones to be shown
        :type     zone_name: str (one of: V(active), CNL(cancelled), ALL )

        :returns:
        :rtype:   dict
        """
        if zone_status not in ['V', 'D', 'ALL']:
            raise ValueError('zone_status has to be V, D or ALL')
        if sub_status not in ['V', 'CNL', 'ALL']:
            raise ValueError('sub_status has to be V, CNL or ALL')
        params = {
            'act': 'zone_list',
            'user_key': user_key,
            'limit': limit,
            'offset': offset,
            'zone_status': zone_status,
            'sub_status': sub_status
        }
        if zone_name:
            params['zone_name'] = zone_name
        if sub_id:
            params['sub_id'] = sub_id

        return self._request(params)

    def _request(self, data):
        """

        :param data: Request body to be sent to Cloudflare
        :type data: dict
        :return: Response from Cloudflare
        :rtype: dict
        """
        data['host_key'] = self._host_key
        response = requests.post(self.CLOUDFLARE_URL, data=data, verify=True).json()
        if response['result'] == 'error':
            raise APIError(response['msg'], response.get('err_code'))
        return response

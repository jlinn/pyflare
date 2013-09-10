__author__ = 'Joe Linn'

import requests


class Pyflare(object):
    class APIError(Exception):
        pass

    CLOUDFLARE_URL = 'https://www.cloudflare.com/api_json.html'

    def __init__(self, email, token):
        """
        Instantiate a Pyflare client object
        :param email: The email address associated with your Cloudflare account
        :type email: str
        :param token: The API key associated with your Cloudflare account
        :type token: str
        """
        self._email = email
        self._token = token

    def stats(self, zone, interval):
        """
        Retrive the current stats and settings for a particular website.
        :param zone:  The domain for which statistics are being retrieved.
        :type zone: str
        :param interval: The time interval for the statistics denoted by the following values:
            20 = Past 30 days
            30 = Past 7 days
            40 = Past day

            The values are for Pro accounts
            100 = 24 hours ago
            110 = 12 hours ago
            120 = 6 hours ago
        :type interval: int
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'stats',
            'z': zone,
            'interval': interval
        })

    def zone_load_multi(self):
        """
        Lists all domains in a CloudFlare account, along with other data.
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'zone_load_multi'
        })

    def rec_load_all(self, zone):
        """
        Lists all DNS records for the given domain
        :param zone: the domain for which records are being retrieved
        :type zone: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'rec_load_all',
            'z': zone
        })

    def zone_check(self, zones):
        """
        Checks for active zones and returns their corresponding zids
        :param zones: List of zones
        :type zones: list of str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'zone_check',
            'zones': ','.join(zones)
        })

    def zone_ips(self, zone, hours=24, ip_class=None, geo=False):
        """
        Retrieve IP addresses of recent visitors
        :param zone: the target domain
        :type zone: str
        :param hours: Past number of hours to query. Defaults to 24, maximum is 48.
        :type hours: int
        :param ip_class: Optional. Restrict the result set to a given class as given by:
            "r" -- regular
            "s" -- crawler
            "t" -- threat
        :type ip_class: str
        :param geo: Optional. Set to True to add longitude and latitude information to response
        :type geo: bool
        :return:
        :rtype: dict
        """
        params = {
            'a': 'zone_ips',
            'z': zone,
            'hours': hours,
            'class': ip_class,
        }
        if geo:
            params['geo'] = geo
        return self._request(params)

    def ip_lkup(self, ip):
        """
        Find the current threat score for a given IP. Note that scores are on a logarithmic scale, where a higher score
        indicates a higher threat.
        :param ip: the target IP
        :type ip: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'ip_lkup',
            'ip': ip
        })

    def zone_settings(self, zone):
        """
        Retrieves all current settings for a given domain.
        :param zone: the target domain
        :type zone: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'zone_settings',
            'z': zone
        })

    def sec_lvl(self, zone, level):
        """
        Set the security level for the given zone
        :param zone: domain name
        :type zone: str
        :param level: security level:
            "help" -- I'm under attack!
            "high" -- High
            "med" -- Medium
            "low" -- Low
            "eoff" -- Essentially Off
        :type level: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'sec_lvl',
            'z': zone,
            'v': level
        })

    def cache_lvl(self, zone, level):
        """
        Set the caching level for the given zone
        :param zone: domain name
        :type zone: str
        :param level: cache level:
            "agg" -- Aggressive
            "basic" -- Basic
        :type level: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'cache_lvl',
            'z': zone,
            'v': level
        })

    def devmode(self, zone, enabled):
        """
        This function allows you to toggle Development Mode on or off for a particular domain.
        When Development Mode is on the cache is bypassed. Development mode remains on for 3 hours or
        until when it is toggled back off.
        :param zone: domain name
        :type zone: str
        :param enabled: True to turn dev mode on, False to turn dev mode off.
        :type enabled: bool
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'devmode',
            'z': zone,
            'v': int(enabled)
        })

    def fpurge_ts(self, zone):
        """
        This function will purge CloudFlare of any cached files. It may take up to 48 hours for the cache to
        rebuild and optimum performance to be achieved so this function should be used sparingly.
        :param zone: domain name
        :type zone: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'fpurge_ts',
            'z': zone,
            'v': 1      # Value can only be "1."
        })

    def zone_file_purge(self, zone, url):
        """
        This function will purge a single file from CloudFlare's cache.
        :param zone: domain name
        :type zone: str
        :param url: The full URL of the file that needs to be purged from Cloudflare's cache. Keep in mind
            that if an HTTP and an HTTPS version of the file exists, then both versions will need to be purged
            independently.
        :type url: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'zone_file_purge',
            'z': zone,
            'url': url
        })

    def zone_grab(self, zone_id):
        """
        Update the snapshot of site for CloudFlare's challenge page
        :param zone_id: ID of zone, found in zone_check
        :type zone_id: int
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'zone_grab',
            'zid': zone_id
        })

    def wl(self, ip):
        """
        Whitelist an ip address
        :param ip: The IP address you want to whitelist
        :type ip: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'wl',
            'key': ip
        })

    def ban(self, ip):
        """
        Blacklist an ip address
        :param ip: The IP address you want to ban
        :type ip: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'ban',
            'key': ip
        })

    def nul(self, ip):
        """
        Remove an IP address from the whitelist or blacklist
        :param ip: The IP address to remove
        :type ip: str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'nul',
            'key': ip
        })

    def ipv46(self, zone, enable):
        """
        Toggles IPv6 support
        :param zone: domain name
        :type zone: str
        :param enable: True to enable, False to disable.
        :type enable: bool
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'ipv46',
            'z': zone,
            'v': int(enable)
        })

    def async(self, zone, setting):
        """
        Changes Rocket Loader setting
        :param zone: domain name
        :type zone: str
        :param setting: [0 = off, a = automatic, m = manual]
        :type setting: int or str
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'async',
            'z': zone,
            'v': setting
        })

    def minify(self, zone, setting):
        """
        Changes minification settings
        :param zone: domain name
        :type zone: str
        :param setting:
            0 = off
            1 = JavaScript only
            2 = CSS only
            3 = JavaScript and CSS
            4 = HTML only
            5 = JavaScript and HTML
            6 = CSS and HTML
            7 = CSS, JavaScript, and HTML
        :type setting: int
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'minify',
            'z': zone,
            'v': setting
        })

    def mirage2(self, zone, enable):
        """
        Toggles mirage2 support
        :param zone: domain name
        :type zone: str
        :param enable: True to enable, False to disable.
        :type enable: bool
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'mirage2',
            'z': zone,
            'v': int(enable)
        })

    def rec_new(self, zone, record_type, name, content, ttl=1, priority=None, service=None, service_name=None,
                protocol=None, weight=None, port=None, target=None):
        """
        Create a DNS record for the given zone
        :param zone: domain name
        :type zone: str
        :param record_type: Type of DNS record. Valid values are [A/CNAME/MX/TXT/SPF/AAAA/NS/SRV/LOC]
        :type record_type: str
        :param name: name of the DNS record
        :type name: str
        :param content: content of the DNS record
        :type content: str
        :param ttl: TTL of the DNS record in seconds. 1 = Automatic, otherwise, value must in between 120 and
            4,294,967,295 seconds.
        :type ttl: int
        :param priority: [applies to MX/SRV] MX record priority.
        :type priority: int
        :param service: Service for SRV record
        :type service: str
        :param service_name: Service Name for SRV record
        :type service_name: str
        :param protocol: Protocol for SRV record. Values are [_tcp/_udp/_tls].
        :type protocol: str
        :param weight: Weight for SRV record.
        :type weight: int
        :param port: Port for SRV record
        :type port: int
        :param target: Target for SRV record
        :type target: str
        :return:
        :rtype: dict
        """
        params = {
            'a': 'rec_new',
            'z': zone,
            'type': record_type,
            'name': name,
            'content': content,
            'ttl': ttl
        }
        if priority is not None:
            params['prio'] = priority
        if service is not None:
            params['service'] = service
        if service_name is not None:
            params['srvname'] = service_name
        if protocol is not None:
            params['protocol'] = protocol
        if weight is not None:
            params['weight'] = weight
        if port is not None:
            params['port'] = port
        if target is not None:
            params['target'] = target
        return self._request(params)

    def rec_edit(self, zone, record_type, record_id, name, content, ttl=1, service_mode=None, priority=None,
                 service=None, service_name=None, protocol=None, weight=None, port=None, target=None):
        """
        Edit a DNS record for the given zone.
        :param zone: domain name
        :type zone: str
        :param record_type: Type of DNS record. Valid values are [A/CNAME/MX/TXT/SPF/AAAA/NS/SRV/LOC]
        :type record_type: str
        :param record_id: DNS Record ID. Available by using the rec_load_all call.
        :type record_id: int
        :param name: Name of the DNS record
        :type name: str
        :param content: The content of the DNS record, will depend on the the type of record being added
        :type content: str
        :param ttl: TTL of record in seconds. 1 = Automatic, otherwise, value must in between 120 and 4,294,967,295
            seconds.
        :type ttl: int
        :param service_mode: [applies to A/AAAA/CNAME] Status of CloudFlare Proxy, 1 = orange cloud, 0 = grey cloud.
        :type service_mode: int
        :param priority: [applies to MX/SRV] MX record priority.
        :type priority: int
        :param service: Service for SRV record
        :type service: str
        :param service_name: Service Name for SRV record
        :type service_name: str
        :param protocol: Protocol for SRV record. Values are [_tcp/_udp/_tls].
        :type protocol: str
        :param weight: Weight for SRV record.
        :type weight: int
        :param port: Port for SRV record
        :type port: int
        :param target: Target for SRV record
        :type target: str
        :return:
        :rtype: dict
        """
        params = {
            'a': 'rec_edit',
            'z': zone,
            'type': record_type,
            'id': record_id,
            'name': name,
            'content': content,
            'ttl': ttl
        }
        if service_mode is not None:
            params['service_mode'] = service_mode
        if priority is not None:
            params['prio'] = priority
        if service is not None:
            params['service'] = service
        if service_name is not None:
            params['srvname'] = service_name
        if protocol is not None:
            params['protocol'] = protocol
        if weight is not None:
            params['weight'] = weight
        if port is not None:
            params['port'] = port
        if target is not None:
            params['target'] = target
        return self._request(params)

    def rec_delete(self, zone, record_id):
        """
        Delete a record for the given domain.
        :param zone: domain name
        :type zone: str
        :param record_id: DNS Record ID. Available by using the rec_load_all call.
        :type record_id: int
        :return:
        :rtype: dict
        """
        return self._request({
            'a': 'rec_delete',
            'z': zone,
            'id': record_id
        })

    def _request(self, data):
        """

        :param data: Request body to be sent to Cloudflare
        :type data: dict
        :return: Response from Cloudflare
        :rtype: dict
        """
        data['tkn'] = self._token
        data['email'] = self._email
        response = requests.post(self.CLOUDFLARE_URL, data=data).json()
        if response['result'] == 'error':
            raise self.APIError("%s - %s" % (response['err_code'], response['msg']))
        return response
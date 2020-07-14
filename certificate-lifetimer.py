#!/usr/bin/env python3
#
#   certificate-lifetimer
#

__version__ = '0.0.1'
__author__ = 'Kenichi Terashita'

import ssl
import socket
import argparse
import textwrap
import certifi
import os
import datetime
from dateutil.parser import parse


# Set the path of local certificates
os.environ['SSL_CERT_FILE'] = certifi.where()


def get_argparse():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''\
                        '''
                                    ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-d', '--domain', type=str, required=True,
                        help=textwrap.dedent('''\
                        Domain name to check
                        '''
                                             ))
    return parser.parse_args()


def get_certificate(args):
    fqdn = args.domain
    context = ssl.create_default_context()
    connection = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=fqdn,
    )

    try:
        connection.settimeout(1.0)
        connection.connect((fqdn, 443))
        certificate_info = connection.getpeercert()
        not_before = parse(certificate_info['notBefore'])
        not_after = parse(certificate_info['notAfter'])
        print(fqdn + ',', not_after - not_before)
    except:
        print(fqdn)

    # print(certificate_info['subject'][5][0][1])
    # print(parse(certificate_info['notBefore']))
    # print(parse(certificate_info['notAfter']))


    # print(certificate_info['subject'][5][0][1] + ',', not_after - not_before)





def main():
    # Predefined Config an Options
    args = get_argparse()

    get_certificate(args)


if __name__ == '__main__':
    main()

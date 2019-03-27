"""
Script which can check remote machines for availability
"""
import ipaddress
import re
from subprocess import PIPE, run

TARGETS = ('192.168.1.1', 'yandex.ru', 'skdfaasf', '1&3219#^#@*')


def is_hostname_or_ip(value: str) -> bool:
    """Check string is valid hostname or IP"""
    try:
        # check for valida IP address
        ipaddress.ip_address(value)
        return True
    except ValueError:
        # Check for valid hostname
        if len(value) > 255:
            return False
        value_ = value
        if value_[-1] == '.':
            value_ = value_[:-1]  # strip exactly one dot from the right, if present
        allowed = re.compile(r'(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)
        return all(allowed.match(x) for x in value_.split('.'))


class InvalidTarget(Exception):
    """Raised then target not an IP or a valida hostname"""


def ping(target: str):
    """Ping target"""
    if not is_hostname_or_ip(target):
        raise InvalidTarget(target)
    # wait 100 ms, one ICMP request
    return run(['ping', target, '-w', '100', '-n', '1'], stdout=PIPE, stderr=PIPE).returncode == 0


def main():
    """Main function, usage example"""
    for target in TARGETS:
        try:
            print(f'{target}:', ping(target))
        except InvalidTarget as exception:
            print(f'{exception}: Invalid hostname or IP')


if __name__ == '__main__':
    main()

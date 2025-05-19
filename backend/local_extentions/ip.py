from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
import os


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def get_country(ip):
    try:
        g = GeoIP2()
        country = g.country_code(ip)
    except AddressNotFoundError:
        print("country not found ip: ", ip)
        return "US"

    return country

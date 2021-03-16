[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/netletic/netinfo/master.svg)](https://results.pre-commit.ci/badge/github/netletic/netinfo/master.svg)
# netinfo

## Supported lookups

netinfo currently supports the following requests:

- [ip.netletic.com](https://ip.netletic.com) - returns your IP address
- [ptr.netletic.com](https://ptr.netletic.com) - returns the reverse DNS record for your IP if it exists; else returns HTTP 204 No Content
- [test.netletic.com](https://test.netletic.com) - returns one of the [RFC-1925](https://tools.ietf.org/html/rfc1925) fundamental networking truths
- [epoch.netletic.com](https://epoch.netletic.com) - returns the Epoch time (also known as [Unix time](https://en.wikipedia.org/wiki/Unix_time))
- [headers.netletic.com](https://headers.netletic.com) - returns HTTP request headers
- [proxy.netletic.com](https://proxy.netletic.com) - returns any known proxy headers found in your request; else returns HTTP 204 No Content


## Example usage

```bash
curl https://ip.netletic.com
198.51.100.84

curl https://ptr.netletic.com
ip-198.51.100.84.example.test

curl https://test.netletic.com
In protocol design, perfection has been reached not when there is nothing left to add, but when there is nothing left to take away.

curl https://epoch.netletic.com
1615854627

curl https://headers.netletic.com
{"host": "headers.netletic.com", "x-client-ip": "198.51.100.84", "x-client-port": "65078", "connection": "Keep-Alive", "accept": "*/*", "max-forwards": "10", "user-agent": "curl/7.69.1", "x-waws-unencoded-url": "/", "client-ip": "198.51.100.84:65078" , "disguised-host": "headers.netletic.com", "x-site-deployment-id": "azwebapp-netinfo-prod-1", "was-default-hostname": "azwebapp-netinfo-prod-1.azurewebsites.net", "x-original-url": "/", "x-forwarded-for": "198.51.100.84:65078", "x-arr-ssl": "2048|256|C=US, O=DigiCert Inc, CN=GeoTrust TLS DV RSA Mixed SHA256 2020 CA-1|CN=headers.netletic.com", "x-forwarded-proto": "https", "x-appservice-proto": "https", "x-forwarded-tlsversion": "1.2"}%

curl https://proxy.netletic.com
{"client-ip": "198.51.100.84:65078"}
```

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
### IP address
```console
curl https://ip.netletic.com
198.51.100.84
```
### PTR
```console
curl https://ptr.netletic.com
ip-198.51.100.84.example.test
```
### Test
```console
curl https://test.netletic.com
It Has To Work.
```
### Epoch time
```console
curl https://epoch.netletic.com
1615854627
```
### GET headers
```console
curl https://headers.netletic.com
{"host": "headers.netletic.com", "x-client-ip": "198.51.100.84", "...": "..."}
```
### Known proxy headers
```console
curl https://proxy.netletic.com
{"client-ip": "198.51.100.84:65078"}
```

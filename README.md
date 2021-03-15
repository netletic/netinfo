# netinfo

## Supported lookups

netinfo currently supports the following requests:

- [ip.netletic.com](https://ip.netletic.com) - returns your IP address
- [epoch.netletic.com](https://epoch.netletic.com) - return the epoch time
- [headers.netletic.com](https://headers.netletic.com) - returns your headers
- [ptr.netletic.com](https://ptr.netletic.com) - returns the reverse DNS record for your IP if it exists. Else it returns code 204.
- [proxy.netletic.com](https://proxy.netletic.com) - returns any known proxy headers found in your request. Else it returns code 204.
- [test.netletic.com](https://test.netletic.com) - returns *bumblebee*

## Example usage

```bash
curl https://ip.netletic.com
198.51. 100.84

curl https://proxy.netletic.com
{"client-ip": "198.51. 100.84:65078"}
```
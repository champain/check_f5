check_f5
=========
###Overview
A simple nagios plugin designed to gather the vserver and pool status on an F5 running BIGIP v11.x

This script uses the iControl API to gather information you already know and disperse it to nagios with proper exit codes.

Example:

```
python check_f5.py -o lb.hamer.ur.domain -u admin -p super_secret -P /Common/http_whois_v4
```

###Dependencies 
Besides the obvious,
[bigsuds](https://devcentral.f5.com/d/bigsuds-python-icontrol-library).

License - MIT

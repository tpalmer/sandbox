import ntplib
import time

NIST = ['nist1-macon.macon.ga.us', 'time.apple.com', 'time.windows.com']

ntp = ntplib.NTPClient()

for ntpServer in NIST:
    ntpResponse = None
    try:
        ntpResponse = ntp.request(ntpServer)
    except Exception as e:
        print str(e) + "\n"
        continue

    now = time.time()
    diff = now-ntpResponse.tx_time
    print 'Response from ' + ntpServer + ': '
    print 'Difference: ' + str(diff) + ' seconds'
    print 'Network Delay: ' + str(ntpResponse.delay)

    nistTime = time.strftime(
        "%a, %d %b %Y %H:%M:%S +0000",
        time.gmtime(int(ntpResponse.tx_time))
    )
    systemTime = time.strftime(
        "%a, %d %b %Y %H:%M:%S +0000",
        time.gmtime(int(now))
    )
    print 'UTC NIST: ' + nistTime
    print 'UTC SYSTEM: ' + systemTime + "\n"

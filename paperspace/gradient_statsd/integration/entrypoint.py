from gradient_statsd import Client
from datetime import datetime, timedelta
from random import randint
import time

METRIC1 = "testMetric1"
METRIC2 = "testMetric2"

if __name__ ==  '__main__':
    client = Client()

    print("Beginning gradient-statsd integration test.")
    endAt = datetime.now() + timedelta(hours=1)

    while datetime.now() <= endAt:
        print("sending {} with counter at {}".format(METRIC1, datetime.now().isoformat()))
        client.increment(METRIC1, 1)

        randNum = randint(1, 100)
        print("sending {} with gauge {} at {}".format(METRIC2, randNum, datetime.now().isoformat()))
        client.gauge(METRIC2, randNum)

        time.sleep(2)


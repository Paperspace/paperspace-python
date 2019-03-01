import os
from datadog.dogstatsd import DogStatsd


class Client(object):
    """
    Client is a wrapper around the DogStatsd client. We use this wrapper to bootstrap custom metrics ingestion on the gradient platform
    """

    def __init__(self, host=None, port=8125, max_buffer_size=1):
        self.host = host
        self.port = port
        self._initialized = True
        self._client = None
        self._max_buffer_size = max_buffer_size

        # find job handle for environment
        job_handle = os.getenv("PS_JOB_ID")
        if not job_handle:
            print("Gradient-Statsd: could not find job handle from environment. logger is not initialized and will not send metrics to statsd")
            self._initialized = False

        # if we are not initialized return no-op client
        if not self._initialized:
            self.increment = lambda *args, **kwargs: None
            self.gauge = lambda *args, **kwargs: None
            return

        # init dogstatsd client
        job_handle_tag = "{}:{}".format("container_name", job_handle)

        # configure DogStatsD client with host if override is present
        if host is not None:
            print("Gradient-Statsd: starting gradient-statsd with host:{} port:{} and job_handle:{}".format(host, port, job_handle))
            self._client = DogStatsd(host=host, port=port, max_buffer_size=self._max_buffer_size, constant_tags=[job_handle_tag])
            self._client.open_buffer(self._max_buffer_size)
            return

        # if no host override use default gateway discovery
        print("Gradient-Statsd: starting gradient-statsd job_handle:{}".format(job_handle))
        self._client = DogStatsd(max_buffer_size=self._max_buffer_size, use_default_route=True, constant_tags=[job_handle_tag])
        self._client.open_buffer(self._max_buffer_size)

    def __del__(self):
        if self._client is not None:
            self._client.close_buffer()

    def increment(self, metric, value):
        self._client.increment(metric=metric, value=value, sample_rate=1)

    def gauge(self, metric, value):
        self._client.gauge(metric=metric, value=value, sample_rate=1)

    def decrement(self, metric, value):
        self._client.decrement(metric=metric, value=value, sample_rate=1)





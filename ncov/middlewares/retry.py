from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in request.meta.get('dont_retry_status', []):
            return response
        if response.status in self.retry_http_codes or \
                response.status in request.meta.get('retry_status', []):
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

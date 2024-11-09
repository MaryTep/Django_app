from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest) -> HttpResponse:
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response
    return middleware


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.current_time_list = []
        self.request_times = {}
        self.time_delta = 60    # Разрешено делать не больше 20 запросов за 60 секунд
        self.count_requests = 20

    def __call__(self, request: HttpRequest):
        ip = request.META.get('REMOTE_ADDR')
        print("Проверка на частоту запросов от пользователя", ip)
        current_time = datetime.now()
        self.current_time_list = self.request_times.get(ip, list())

        if self.current_time_list != []:
            for elem in self.current_time_list:
                if current_time - elem > timedelta(seconds=self.time_delta):
                    self.current_time_list.remove(elem)

            if ip in self.request_times and len(self.current_time_list) > self.count_requests - 1:
                print(f"Слишком часто: за миинуту было сделано больше {self.count_requests} запросов!")
                return render(request, 'requestdataapp/spam-page.html', status=429)

        self.current_time_list.append(current_time)
        self.request_times[ip] = self.current_time_list
        response = self.get_response(request)
        return response


class CountRequestsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests_count =", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses_count =", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exception so far")


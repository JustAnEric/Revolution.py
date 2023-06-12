import os, re, json, urllib, aiohttp, requests, asyncio

class RequestType():
    GET = "GET"
    POST = "POST"

class Request():
    def __init__(self, request_url, request_method=RequestType.GET, headers=None):
        self.request_ = {
            "url": request_url,
            "method": request_method,
            "headers": headers
        }
    
    def request(self):
        if str(self.request_.get("method")).upper() == "GET":
            resp = requests.get(self.request_.get("url"), headers=self.request_.get("headers"))
        if str(self.request_.get("method")).upper() == "POST":
            resp = requests.post(self.request_.get("url"), headers=self.request_.get("headers"))
        if str(self.request_.get("method")).upper() == "PUT":
            resp = requests.put(self.request_.get("url"), headers=self.request_.get("headers"))
        if str(self.request_.get("method")).upper() == "DELETE":
            resp = requests.delete(self.request_.get("url"), headers=self.request_.get("headers"))

        return resp if resp is not None else 0
    
class RequestHandler(Request):
    global RequestType
    def __init__(self, request:requests.Response, type:RequestType, retrieve):
        self.request_type = type
        self.request_retrieve = retrieve
        self.request_ = request
        
    def c(self):
        if self.request_type == RequestType.GET:
            if self.request_retrieve == "json": return self.request_.json()
            if self.request_retrieve == "headers": return self.request_.headers
            if self.request_retrieve == "body": return self.request_.content
            if self.request_retrieve == "encoding": return self.request_.encoding
            if self.request_retrieve == "cookies": return self.request_.cookies
        if type == RequestType.POST:
            if self.request_retrieve == "json": return self.request_.json()
            if self.request_retrieve == "headers": return self.request_.headers
            if self.request_retrieve == "body": return self.request_.content
            if self.request_retrieve == "encoding": return self.request_.encoding
            if self.request_retrieve == "cookies": return self.request_.cookies
        return 0
    
class PingRequest():
    def __init__(self, request_url, request_method=RequestType.GET):
        self.request_ = {
            "url": request_url,
            "method": request_method
        }
    
    async def request(self, time=0, afterEach=None):
        while True:
            if str(self.request_.get("method")).upper() == "GET":
                resp = requests.get(self.request_.get("url"))
            if str(self.request_.get("method")).upper() == "POST":
                resp = requests.post(self.request_.get("url"))
            if str(self.request_.get("method")).upper() == "PUT":
                resp = requests.put(self.request_.get("url"))
            if str(self.request_.get("method")).upper() == "DELETE":
                resp = requests.delete(self.request_.get("url"))
            await afterEach()
            await asyncio.sleep(time)

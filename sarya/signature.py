import base64
import datetime
import hmac
from hashlib import sha256
import httpx
import asyncio
import fastapi

class HMAS:
    SIGNATURE_DELIM = '\n'
    SIGNATURE_HEADER = "x-auth-signature"
    TIMESTAMP_HEADER = "x-auth-timestamp"

    @classmethod
    def _get_current_timestamp(cls):
        return datetime.datetime.now().isoformat()
    
    @classmethod
    def _httpx_request(cls, request:httpx.Request)->tuple[str, str, str, str]:
        method = request.method
        path = request.url.path
        params = str(request.url.params) 
        content = request.content.decode('utf-8')
        return method, path, params, content 
    
    @classmethod
    async def _fastapi_request(cls, request:fastapi.Request):
        method = request.method
        path = request.url.path
        params = str(request.url.query) 
        content = await request.body()
        content = content.decode('utf-8') if content else ''
        return method, path, params, content

    @classmethod
    async def _signature(cls, request:fastapi.Request|httpx.Request, timestamp, secret_key:str)->str:
        if isinstance(request, fastapi.Request):
            method, path, params, content = await cls._fastapi_request(request=request)
        elif isinstance(request, httpx.Request):
            method, path, params, content =  cls._httpx_request(request=request)

        signature = cls._sign(method, timestamp, path,params, content, secret_key)
        return signature.decode('utf-8')
            
    @classmethod
    def _sign(cls, method:str, timestamp, path, params, content, secret_key):
        message = bytearray(method, 'utf-8') + \
                bytearray(cls.SIGNATURE_DELIM, 'utf-8') + \
                bytearray(timestamp, 'utf-8') + \
                bytearray(cls.SIGNATURE_DELIM, 'utf-8') + \
                bytearray(path, 'utf-8') + \
                bytearray(cls.SIGNATURE_DELIM, 'utf-8') + \
                bytearray(params, 'utf-8') 

        if content:
            message += bytearray(cls.SIGNATURE_DELIM, 'utf-8') + bytearray(content, 'utf-8')

        # Create the signature
        digest = hmac.new(key=bytearray(secret_key, 'utf-8'), msg=message, digestmod=sha256).digest()
        return base64.urlsafe_b64encode(digest).strip()

    @classmethod
    def decode(cls, secret_key:str):
        async def fun(request:httpx.Request) -> None:
            timestamp = cls._get_current_timestamp()
            request.headers[cls.TIMESTAMP_HEADER] = timestamp
            request.headers[cls.SIGNATURE_HEADER] = await cls._signature(request, timestamp, secret_key)
        return fun
    
    @classmethod
    async def verify(cls, secret_key, request:fastapi.Request)->bool:
        timestamp = request.headers.get(cls.TIMESTAMP_HEADER, "")
        signature = await cls._signature(request=request, timestamp=timestamp, secret_key=secret_key)
        return signature == request.headers.get(cls.SIGNATURE_HEADER, "")

        
if __name__ == "__main__":
    async def test(url="https://www.google.com", method="GET", json=None):
        async with httpx.AsyncClient(event_hooks={"request":[HMAS.decode("test")]}) as client:
            if method == "GET":
                r = await client.get(url)
            elif method == "POST":
                r = await client.post(url, json=json)
        return r 
    r = asyncio.run(test())
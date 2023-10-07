import os
import requests
from typing import List
from dacite import from_dict
from llmrails.utils import raise_for_status, finfo
from llmrails.models import ModelChoices, Datastore, Embeddings, SearchResults, ChatResult


class Client:
    """LLMRails Client

    Args:
        api_key (str): Your API key.
        max_retries (int): maximal number of retries for requests.
        timeout (int): request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str = None,
        timeout: int = 120,
    ) -> None:
        self.api_key = api_key or os.getenv("LLMRAILS_API_KEY")
        self.timeout = timeout
        self.api_url = 'https://api.llmrails.com/v1'
        self.session = requests.Session()
        self.session.headers = {'X-API-KEY':self.api_key}
    

    def _request(self, endpoint: str, method: str, body=None, files=None):
        response = self.session.request(
            method,
            f"{self.api_url}{endpoint}",
            json=body,
            files=files,
            timeout=self.timeout
        )

        raise_for_status(response)
        return response.json()


    def create_datastore(self, name: str, model: ModelChoices) -> int:
        response = self._request('/datastores', 'POST', body={
            "name": name,
            "model": model
        })

        return response['id']
    

    def delete_datastore(self, datastore_id: int) -> bool:
        self._request(f'/datastores/{datastore_id}', 'DELETE')
        return True
    
    
    def get_datastore(self, datastore_id: int) -> Datastore:
        response = self._request(f'/datastores/{datastore_id}', 'GET')
        return from_dict(data_class=Datastore, data=response)


    def embed(self, texts: List[str], model: ModelChoices) -> Embeddings:
        response = self._request('/embeddings', 'POST', body={
            'input': texts,
            'model': model
        })

        return from_dict(data_class=Embeddings, data=response)


    def upload_text(self, datastore_id: int, name: str, text: str):
        self._request(f'/datastores/{datastore_id}/text', 'POST', body={
            "name":name,
            "text":text
        })

        return True
    
    
    def upload_file(self, datastore_id, files: List[str]):
        request_files = []

        for file_name in files:
            file = open(file_name, 'rb')
            request_files.append(('file', (os.path.basename(file_name), file, finfo(file_name))))
  
        self._request(f'/datastores/{datastore_id}/file', 'POST', files=request_files)
        return True
        

    def search(self, datastore_id: int, text: str, hybrid: bool = True, summarize: bool =  False):
        response = self._request(f'/datastores/{datastore_id}/search', 'POST', body={
            "text": text,
            "hybrid":hybrid,
            "summarize": summarize
        })

        return from_dict(data_class=SearchResults, data=response)
    

    def chat(self, app_id: str, query: str, session_id: str = None):
        response = self._request(f'/chat/{app_id}', 'POST', body={
            "stream":False,
            "text":query,
            "session_id": session_id
        })

        
        return from_dict(data_class=ChatResult, data=response)


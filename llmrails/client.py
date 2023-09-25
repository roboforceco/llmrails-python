import os
import requests
from typing import List
from dacite import from_dict
from llmrails.utils import raise_for_status
from llmrails.models import ModelChoices, Datastore, Embeddings


class Client:
    """Cohere Client

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
        self.api_key = api_key or os.getenv("LLM_RAILS_API_KEY")
        self.timeout = timeout
        self.api_url = 'http://0.0.0.0:5500/v1'
        self.session = requests.Session()
        self.session.headers = {'X-API-KEY':self.api_key}
    

    def _request(self, endpoint: str, method: str, body=None):
        response = self.session.request(
            method,
            f"{self.api_url}{endpoint}",
            json=body,
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

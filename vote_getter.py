import requests
from helpers import Votes

class VoteGetter:
    def __init__(self):
        self.api_url = "http://84.215.98.118:8080"

    def _get_poll(self, id):
        req_json = requests.get(f'{self.api_url}/polls/{id}').json()
        return req_json

    def _get_poll_distro(self, id):
        req_json = requests.get(f'{self.api_url}/polls/{id}/distribution').json()
        return req_json

    def get_votes_from_poll(self, id):
        print(f"Fetching votes from {self.api_url}...")
        poll_distro = self._get_poll_distro(id)
        return Votes(poll_distro['yes'], poll_distro['no'])


# t = VoteGetter()
# print(t.get_votes_from_poll(1))
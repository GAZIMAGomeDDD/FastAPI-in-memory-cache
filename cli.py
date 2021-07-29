from cmd import Cmd
from pprint import pprint
import requests


class CLI(Cmd):
    intro = 'Welcome to the MemoryCache shell.\nType help or ? to list commands.\n'
    prompt = '>>> '
    do_exit = lambda self, _: exit()

    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()
        
    def do_get(self, key: str) -> None:
        response = self.session.post(
            url='http://127.0.0.1:8000/GET', 
            json={'key': key}
        )
        
        pprint(response.json())
    
    def do_keys(self, pattern: str) -> None:
        response = self.session.post(
            url='http://127.0.0.1:8000/KEYS', 
            json={'pattern': pattern}
        )

        pprint(response.json())

    def do_set(self, args) -> None:
        try:
            key, value, ex = args.split()
            payload = {'key': key, 'value': value, 'ex': int(ex)}
        
        except ValueError:
            key, value = args.split()
            payload = {'key': key, 'value': value}
       
        response = self.session.post(
            url='http://127.0.0.1:8000/SET', 
            json=payload
        )

        pprint(response.json())

    def do_ttl(self, key: str) -> None:
        response = self.session.post(
            url='http://127.0.0.1:8000/TTL', 
            json={'key': key}
        )
        
        pprint(response.json())
    
    def do_save(self, _) -> None:
        response = self.session.post(url='http://127.0.0.1:8000/SAVE')
        
        pprint(response.json())
    
    def do_del(self, key) -> None:
        response = self.session.post(
            url='http://127.0.0.1:8000/DEL', 
            json={'key': key}
        )
        
        pprint(response.json())


if __name__ == '__main__':
    try:
        CLI().cmdloop()
    except KeyboardInterrupt:
        pass

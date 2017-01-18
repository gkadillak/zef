import json
import os
import requests

BASE_URL = 'https://sprint.ly/api'


class File(object):
    """
    Use a file object to catch errors
    """
    
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        

def main():
    """
    Retrieving items:

    make a request to get all the stories with a given tag

    Write the results to document.

    TEMPLATE:
    
    Accomplishments:
    
    [# of points]

    [[t-shirt size]] ([bug, feature, task]) [link to sprintly item] [[description of sprintly item]]
    [include interrupt tag if it exists]

    Points in progress:
    
    [points for unfinished stories (would be nice to have size breakdown, links here)]
    """

    request_url = BASE_URL + '/items/search.json?q=tag:spirit-112'
    # store your sprintly token in an environmental variable
    response = requests.get(request_url, auth=requests.auth.HTTPBasicAuth('<your email here>', os.environ['SPRINTLY_TOKEN']))
    datum = json.loads(response.text)
    completed_items = [item for item in datum['items'] if item['status'] == 'completed']

    with File('planning.txt', 'w') as file:
        for item in completed_items:
            title = item['title']
            size = item.get('size', '')
            type = item['type']
            link = item['short_url']
            description = item['description']

            message = '{title}\n{size} ({type}) [{link}]\n{description}\n'.format(
                title=title, size=size, type=type, link=link, description=description
            )
            file.write(message)
        
        

    """
    Metrics:
    
    Get the metrics for all of the stories and also need to 
    know how long each story took (do we care about tasks, bugs?)
    """



    
    
main()

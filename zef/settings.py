import os


GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REPO_ID_CACHE = PROJECT_ROOT + '/caches/repo_ids.txt'

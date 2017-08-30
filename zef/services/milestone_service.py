MILESTONE_ATTRIBUTES = [
    'description', 'title', 'url', 'labels_url', 'created_at',
    'creator', 'number', 'html_url', 'updated_at', 'due_on',
    'state', 'closed_issues', 'open_issues', 'closed_at', 'id'
]
Milestone = collections.namedtuple('Milestone', MILESTONE_ATTRIBUTES)


def get_milestones():
    """
    Fetch all of the milestones for a given repository

    @rtype [Milestone]
    @return all milestones pertaining to repo
    """
    milestones = json.loads(github_facade.fetch_milestones().text)

    if not milestones:
        return

    return [Milestone(**milestone) for milestone in milestones]

def get_issues(milestone_id):
    """
    Fetch all of the issues for a given milestone

    @param int milestone_id: Identifier given by Github for milestone
    
    @rtype list
    @return all issues
    """
    # TODO: if no milestone_id is passed in, return all issues for the repo
    issues = json.loads(github_facade.fetch_issues_for_milestone(milestone_id).text)

    if not issues:
        return

    return [Issue(**issue) for issue in issues]

def display_milestones(milestones):
    display = ['%s %s' % (idx, milestone.title)
            for idx, milestone in enumerate(milestones, start=1)]
    return '\n'.join(display)

def ordered_milestones():
    milestones = get_milestones()
    milestones.sort(key=lambda m: m.title, reverse=True)
    return milestones

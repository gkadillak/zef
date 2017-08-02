from ..services import github_service

def ordered():
    milestones = github_service.get_milestones()
    milestones.sort(key=lambda m: m.title, reverse=True)
    return milestones


def display(milestones):
    display = ['%s %s' % (idx, milestone.title)
            for idx, milestone in enumerate(milestones, start=1)]
    return '\n'.join(display)

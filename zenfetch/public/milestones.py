from .. import services

def ordered():
    milestones = services.get_milestones()
    milestones.sort(key=lambda m: m.title, reverse=True)
    return milestones


def display(milestones):
    display = ['%s %s' % (idx, milestone.title)
            for idx, milestone in enumerate(milestones, start=1)]
    return '\n'.join(display)

from django.http import HttpResponse, HttpResponseRedirect
from .models import Songs, Votes
from django.template import loader
from django.utils import timezone

def index(request):
    songs_lists = Songs.objects.all()
    template = loader.get_template('music/index.html')
    context = {
        'songs_lists' : songs_lists
    }
    return HttpResponse(template.render(context, request))

def detail(request, song_id):
    template = loader.get_template('music/detail.html')
    singer = Songs.objects.get(pk=song_id)
    try:
        vote = Votes.objects.get(song_id=song_id)
    except Votes.DoesNotExist:
        context = {
            'singer': singer,
            'vote': 0
        }
        return HttpResponse(template.render(context, request))

    context = {
        'singer': singer,
        'vote': vote
    }
    return HttpResponse(template.render(context, request))


def vote(request, song_id):
    try:
        votes = Votes.objects.get(song_id=song_id)
    except Votes.DoesNotExist:
       votes = Votes(num_votes=1, voted_date= timezone.now(), song_id=song_id)
       votes.save()
       return HttpResponse('saved')

    votes.num_votes = votes.num_votes + 1
    votes.save()
    template = loader.get_template('music/detail.html')
    context = {
        'singer': Songs.objects.get(pk=song_id),
        'vote': votes
    }
    return HttpResponse(template.render(context, request))


class NotFoundException(Exception):
    pass

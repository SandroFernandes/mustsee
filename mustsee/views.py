import uuid
from django.shortcuts import (
    get_object_or_404, redirect, render_to_response)
from .models import Attraction, UserRank

def get_uuid(request):
    return request.session.setdefault(
        'session_uuid', uuid.uuid4().hex)

def attraction_list(request):
    attractions = Attraction.objects.prefetch_related('ranks')

    max_rank = len(attractions)
    for attraction in attractions:
        attraction.user_rank = None
        attraction.score = 0
        for user_rank in attraction.ranks.all():
            attraction.score += (max_rank - user_rank.rank)
            if user_rank.session_uuid == get_uuid(request):
                attraction.user_rank = user_rank.rank

    scores = sorted(
        map(lambda a: a.score, attractions), reverse=True
    )

    for attraction in attractions:
        attraction.overall_rank = scores.index(
            attraction.score
        )

    attractions = sorted(
        attractions, key=lambda a: (
            a.name if a.user_rank is None else a.user_rank
        )
    )

    return render_to_response(
        'mustsee/list.html',
        {'attractions': attractions}
    )

def promote(request, attraction_id):
    attraction = get_object_or_404(
        Attraction, id=attraction_id
    )
    user_rank, created = attraction.ranks.get_or_create(
        session_uuid=get_uuid(request)
    )
    if not created:
        user_rank.rank = max(user_rank.rank-1, 0)
        user_rank.save()
    return redirect('list')


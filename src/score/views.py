import io
import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse

from score.models import Criteria, Website

applicable_states = ['conforme', 'en cours de déploiement', 'non conforme']


def get_criteria_by_thematic(criterias, thematic):
    return [criteria for criteria in criterias.values() if criteria['thematic'] == thematic]


@api_view(['POST', 'PUT', 'PATCH'])
def add_website(request):
    website = Website.objects.create(url=request.data['url'])
    website.save()

    for criteria in request.data['criterias']:
        new_criteria = Criteria.objects.create(**criteria, website_id=website.pk)
        new_criteria.save()

    conform = website.criteria_set.filter(state='conforme').count()
    total = website.criteria_set.filter(state__in=applicable_states).count()
    website.score = conform / total
    website.save()

    return JsonResponse(data={"url": website.url, "score": website.score}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_pdf(request, url):
    with open("score/criterias.json", 'r') as f:
        criterias = json.load(f)



    try:
        website = Website.objects.filter(url=url).last()
    except ObjectDoesNotExist:
        content = {"message": "Nous n'avons pas encore analyser ce site internet."}
        return JsonResponse(data=content, status=status.HTTP_400_BAD_REQUEST)

    website_criterias = website.criteria_set.all()
    criterias_map = {}
    for criteria in website_criterias:
        criterias_map[criteria.number] = {
            "number": criteria.number,
            "state": criteria.state,
            "thematic": criterias.get(criteria.number)["thematique"],
            "critere": criterias.get(criteria.number)["critere"],
        }
    context = {
        'website': website,
        'criterias': criterias_map,
        'strategy': get_criteria_by_thematic(criterias_map, "Stratégie"),
        'specifications': get_criteria_by_thematic(criterias_map, "Spécifications"),
        'architecture': get_criteria_by_thematic(criterias_map, "Architecture"),
        'ui': get_criteria_by_thematic(criterias_map, "UX/UI"),
        'contents': get_criteria_by_thematic(criterias_map, "Contenus"),
        'frontend': get_criteria_by_thematic(criterias_map, "Frontend"),
        'backend': get_criteria_by_thematic(criterias_map, "Backend"),
        'hosting': get_criteria_by_thematic(criterias_map, "Hébergement"),
    }

    # return FileResponse(buffer, as_attachment=True, filename="Test.pdf")
    return render(request, 'pdf-report.html', context=context)

# Home/views.py
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RssUrls, RssData, RssSkills
from .serializers import RssUrlsSerializer, RssDataSerializer, RssSkillsSerializer
from Script import fetch_and_parse_rss


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_rss_urls(request):
    urls = RssUrls.objects.all()
    serializer = RssUrlsSerializer(urls, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_rss_data(request):
    data = RssData.objects.all()
    serializer = RssDataSerializer(data, many=True)
    return Response(serializer.data)


# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def add_rss_url(request):
#     # Parse title and link from the request
#     title = request.data.get('title')
#     link = request.data.get('link')
#
#     if not title or not link:
#         return Response({'error': 'Title and link are required fields.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     # Save the new RssUrls entry
#     rss_url = RssUrls(title=title, link=link)
#     rss_url.save()
#
#     # Fetch the latest RssUrls entry (the one just saved)
#     latest_rss_url = RssUrls.objects.latest('id')
#
#     # Scrape the URL from the latest entry
#     fetch_and_parse_rss([latest_rss_url.link])
#
#     # Serialize the latest RssUrls entry
#     serializer = RssUrlsSerializer(latest_rss_url)
#
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

############ 3RD User addtition ################
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_rss_url(request):
    title = request.data.get('title')
    link = request.data.get('link')

    if not title or not link:
        return Response({'error': 'Title and link are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

    rss_url = RssUrls.objects.create(
        title=title,
        link=link,
        user=request.user
    )
    rss_url.save()

    latest_rss_url = RssUrls.objects.latest('id')
    fetch_and_parse_rss([latest_rss_url.link])

    serializer = RssUrlsSerializer(rss_url)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def skills_view(request):
    skills = RssSkills.objects.all()
    serializer = RssSkillsSerializer(skills, many=True)
    return Response(serializer.data)

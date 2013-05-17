from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.api.deployment_networks import add_deployment_network, delete_deployment_network, get_deployment_networks
from core.serializers import DeploymentNetworkSerializer
from util.request import parse_request


class DeploymentNetworkListCreate(APIView):
    """ 
    List all deployment networks or create a new role.
    """

    def post(self, request, format = None):
        data = parse_request(request.DATA)  
        if 'auth' not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)        
        elif 'deploymentNetwork' in data:
        
            deployment = add_deployment_network(data['auth'], data['deploymentNetwork'].get('name'))
            serializer = DeploymentNetworkSerializer(deployment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            deployment_networks = get_deployment_networks(data['auth'])
            serializer = DeploymentNetworkSerializer(deployment_networks, many=True)
            return Response(serializer.data)
        
            
class DeploymentNetworkRetrieveUpdateDestroy(APIView):
    """
    Retrieve, update or delete a deployment network 
    """

    def post(self, request, pk, format=None):
        """Retrieve a deployment network"""
        data = parse_request(request.DATA)
        if 'auth' not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        deployment_networks = get_deployment_networks(data['auth'], pk)
        if not deployment_networks:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeploymentNetworkSerializer(deployment_networks[0])
        return Response(serializer.data)                  

    def put(self, request, pk, format=None):
        """deployment network update not implemnted""" 
        return Response(status=status.HTTP_404_NOT_FOUND) 

    def delete(self, request, pk, format=None):
        data = parse_request(request.DATA) 
        if 'auth' not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        delete_deployment_network(data['auth'], pk)
        return Response(status=status.HTTP_204_NO_CONTENT) 
            
            
        
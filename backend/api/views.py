from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Movie, Ticket, Customer
from .serializers import MovieSerializer, TicketSerializer, CustomerSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Check if password and confirm_password fields match
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)
        if password != confirm_password:
            return Response(
                {'error': 'Passwords do not match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Create a corresponding Customer instance
        user = serializer.instance
        Customer.objects.create(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        # Check if the credentials are valid
        if user is None:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        # Retrieve the corresponding Customer instance
        try:
            customer = Customer.objects.get(user=user)
        except customer.DoesNotExist:
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        # Create a dictionary with the relevant user data
        user_data = {
            # 'id': user.id,
            'username': user.username,
            # Add any other desired user data
        }

        return Response(
            {'user': user_data},
            status=status.HTTP_200_OK
        )
        # # Check if the customer is activated
        # if not customer.is_active:
        #     logout(request)
        #     return Response(
        #         {'error': 'Account is not activated'},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )

        serializer = UserSerializer(user)
        return Response(
            {'user': serializer.data},
            status=status.HTTP_200_OK
        )
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

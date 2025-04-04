from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from .serializers import RegistrationSerializer


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            # Validate and save user
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Catch validation errors and return details
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            # Handle database-level errors (e.g., duplicate email)
            return Response(
                {"errors": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"errors": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

"""
Authentication views for login/logout functionality.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    tags=['Authentication'],
    summary='User login',
    description='Authenticate with email and password',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'object',
                    'properties': {
                        'user': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'email': {'type': 'string'},
                                'role': {'type': 'string'},
                                'organization': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'domain_type': {'type': 'string'},
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        401: {
            'type': 'object',
            'properties': {
                'errors': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    },
    examples=[
        OpenApiExample(
            'Successful login',
            value={'email': 'user@example.com', 'password': 'secure_password'},
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user with email and password.

    Request body:
        email: User's email address
        password: User's password

    Returns:
        User data including role and organization on success
        Error message on authentication failure
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'errors': [{'message': 'Email and password are required'}]
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)

    if user is not None and user.is_active:
        login(request, user)

        # Update last login time
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])

        return Response({
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'organization': {
                        'id': user.organization.id,
                        'name': user.organization.name,
                        'domain_type': user.organization.domain_type,
                    }
                }
            }
        })

    return Response({
        'errors': [{'message': 'Invalid credentials'}]
    }, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    tags=['Authentication'],
    summary='User logout',
    description='End the current user session',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'object',
                    'properties': {
                        'success': {'type': 'boolean'}
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout the current user and invalidate their session.

    Returns:
        Success confirmation
    """
    logout(request)
    return Response({'data': {'success': True}})


@extend_schema(
    tags=['Authentication'],
    summary='Get current user',
    description='Get information about the currently authenticated user',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'object',
                    'properties': {
                        'user': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'email': {'type': 'string'},
                                'role': {'type': 'string'},
                                'organization': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'domain_type': {'type': 'string'},
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Get information about the currently authenticated user.

    Returns:
        User data including role and organization
    """
    return Response({
        'data': {
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'role': request.user.role,
                'organization': {
                    'id': request.user.organization.id,
                    'name': request.user.organization.name,
                    'domain_type': request.user.organization.domain_type,
                }
            }
        }
    })

from rest_framework.authentication import get_authorization_header , BaseAuthentication
from rest_framework import exceptions
import jwt 
from django.conf import settings
from authentication.models import User

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        print("auth_header " ,auth_header)
        
        auth_data = auth_header.decode('utf-8')
        print("\nauth_data " ,auth_data)
        
        auth_token = auth_data.split(" ")
        print("\nauth_token " ,auth_token)
        if len(auth_token)!=2:
            raise exceptions.AuthenticationFailed('Token  invalid!')
        
        token = auth_token[1]
        print("\ntoken" , token)
        try:
            payload = jwt.decode(token,settings.SECRET_KEY , algorithms='HS256' )
            print("\npayload" , payload)
            username = payload['username']
            
            user = User.objects.get(username=username)
            
            return(user , token)
            
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token Expired. Login again')
        
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Tokensss is Invalid')
        
        except User.DoesNotExist as ex:
            raise exceptions.AuthenticationFailed('No Such as User')
        

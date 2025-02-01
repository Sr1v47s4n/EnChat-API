from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import AnonymousUser
from user.models import User
from urllib.parse import parse_qs
import traceback


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        print("Query string:", query_string)

        token = query_string.get("token", [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]  # Extract user_id from token

                # Fetch the user from the database
                user = await self.get_user(user_id)
                scope["user"] = user
                print("User authenticated:", user)

            except TokenError as e:
                print("Authentication failed:", str(e))
                print(traceback.format_exc())  # Debugging
                scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    async def get_user(self, user_id):
        """Fetch user asynchronously from the database"""
        try:
            return await User.objects.aget(id=user_id)  # Use async ORM query
        except User.DoesNotExist:
            print(f"User with ID {user_id} does not exist.")
            return AnonymousUser()

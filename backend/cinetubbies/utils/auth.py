def jwt_response_payload_handler(token, user=None, request=None):
  return {
    'token': token,
    'user': { 'username': 'Hardcoded', 'name': 'Very', 'id': 1 }
    # 'user': UserSerializer(user, context={'request': request}).data
  }

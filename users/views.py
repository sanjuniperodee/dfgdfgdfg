import random
from datetime import datetime, timedelta

import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.forms import CreateUserRequestForm
from users.models import User, Document, UserCreateRequest, Type
from users.serializers import UserSerializer, DocumentSerializer


class CheckUserView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        email = request.data['email']

        if len(User.objects.filter(phone_number=phone_number)) + len(User.objects.filter(email=email)) == 0:
            return Response({}, status=200)
        return Response({}, status=400)


class UploadDocumentView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        title = request.data.get('title')
        document_id = request.data.get('id')
        print(document_id)
        if document_id != 'undefined':
            document = Document.objects.filter(pk=document_id).first()
            if document:
                document.file = file
                document.status = 'pending'
                document.save()
                print('DOCUMENT HAS BEEN CHANGED')
                return Response({'message': 'Document updated successfully'}, status=200)
            else:
                return Response({'error': 'Document not found'}, status=404)
        else:
            token = request.data.get('jwt')
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
            user = User.objects.filter(id=payload['id']).first()
            if not user:
                return Response({'error': 'User not found'}, status=404)
            document_type = Type.objects.filter(title=title).first()
            if not document_type:
                return Response({'error': 'Document type not found'}, status=404)
            document = Document.objects.create(title=document_type, file=file, status='pending')
            user.user_documents.add(document)
            return Response({'message': 'Document updated successfully'}, status=200)


class ApplicationView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        chance = 0
        for document in user.user_documents.all():
            print(document.title.score)
            if document.status == 'approved':
                chance += document.title.score
        if not user.apply_approved:
            chance = -1
        return Response({'chance': chance}, status=200)


class ApproveApplicationView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        user.apply_approved = True
        user.save()
        return Response({}, status=200)


class RegisterRequestView(APIView):
    def post(self, request):
        form = CreateUserRequestForm(data=request.data)
        if form.is_valid():
            try:
                userCreateRequest = form.save()
            except:
                return Response({'message': 'Пользователь с такой почтой или номером уже существует!'})
            sms_code = str(random.randint(100000, 999999))
            userCreateRequest.sms_code = sms_code
            userCreateRequest.save()
            print(sms_code)
            return Response({'message': 'SMS code sent. Please verify to complete registration.', 'sms_code': sms_code},
                            status=200)

        return Response(form.errors, status=400)


class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        if len(UserCreateRequest.objects.filter(sms_code=request.data['sms_code'])) == 0:
            return Response({'message': 'Wrong sms code'}, status=400)

        userCreateRequest = UserCreateRequest.objects.filter(sms_code=request.data['sms_code']).first()

        user = User(
            first_name=userCreateRequest.first_name,
            last_name=userCreateRequest.last_name,
            email=userCreateRequest.email,
            phone_number=userCreateRequest.phone_number,
            username=userCreateRequest.username,
            password=userCreateRequest.password,
        )
        user.save()

        token = jwt.encode(
            {'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24), 'iat': datetime.utcnow()}, 'sercet',
            algorithm='HS256').encode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'token': token}

        return response


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(email, password)
        user = User.objects.filter(email=email, password=password).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        token = jwt.encode(
            {'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24), 'iat': datetime.utcnow()}, 'sercet',
            algorithm='HS256').encode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'token': token}

        return response


class UserView(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed("Failed to authorize")
        try:
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authorization is expired")
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDocuments(APIView):
    def post(self, request):
        token = request.data.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed("Failed to authorize")
        try:
            payload = jwt.decode(token, 'sercet', algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authorization is expired")
        user = User.objects.filter(id=payload['id']).first()
        data = []
        for i in user.user_documents.all():
            item = {
                'id': i.pk,
                'title': i.title.title,
                'score': i.title.score,
                'status': i.status,
                'file' : i.file.name
            }
            data.append(item)
        print(data)
        return Response(data)

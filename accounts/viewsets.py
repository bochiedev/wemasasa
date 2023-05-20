from rest_framework import viewsets, status
from rest_framework.decorators import action
from accounts.serializers import UserProfileSerializer
from accounts.models import User
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated



# Create your views here.

@action(detail=False, methods=["POST"], url_path="edit-profile")
class UserProfileViewset(viewsets.ViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    @action(
        methods=['POST'],
        detail=False,
        url_path='edit',
        permission_classes=[AllowAny],
    )
    def edit_profile(self,request):
        user = self.request.user

        data = request.data
        member_no = data.pop("member_no")
        type = data.pop("type")


        try:
            user = User.objects.get(user=user)
            user.member_no = member_no
            user.type = type
            user.save()

        except Exception as e:
            print(e)

    @action(
        methods=['GET'],
        detail=False,
        url_path='cloud_user',
        permission_classes=[AllowAny],
    )
    def get_hcloud_user(self,request):
        # user = self.request.user

        url = 'https://accounts.multitenant.slade360.co.ke/oauth2/token/'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            "grant_type": "password",
            "client_id": settings.H_CLOUD_KEY,
            "client_secret": settings.H_CLOUD_SECRET,
            "username": settings.H_CLOUD_EMAIL,
            "password": settings.H_CLOUD_PASSWORD,
        }
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        data = response.json()


        print(data)

        access_token = data.get('access_token')
        member_number = '1234567'
        payer_slade_code = '457'
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        url = (
        'https://provider-edi-api.multitenant.slade360.co.ke/v1/beneficiaries/'
        'member_eligibility/?member_number={}&payer_slade_code={}'.format(
            member_number, payer_slade_code
        )
        )

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        user_data = response.json()


        return Response(
            {
                "success": True,
                "data": data,
                "user_data": user_data
            },
            status=status.HTTP_200_OK,
        )



from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django_rpx.models import RpxData
from django_rpx.views import permute_name
from django.conf import settings
TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS', []))

class RpxBackend:
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
    def get_user_by_rpx_id(self, rpx_id):
        try:
            return User.objects.get(rpxdata__identifier=rpx_id)
        except User.DoesNotExist:
            return None
            
    def authenticate(self, token=''):
        """
        TODO: pass in a message array here which can be filled with an error
        message with failure response
        """
        from django.utils import simplejson
        import urllib
        import urllib2

        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'token': token
        }
        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        json = simplejson.load(r)
        if json['stat'] <> 'ok':
            return None
        profile = json['profile']
        rpx_id = profile['identifier']
        nickname = profile.get('displayName') or \
          profile.get('preferredUsername')
        email = profile.get('email', '')
        profile_pic_url = profile.get('photo')
        info_page_url = profile.get('url')
        provider=profile.get("providerName")

        # get user from DB by this rpx
        user = self.get_user_by_rpx_id(rpx_id)
        if user:
            # we have rpx and associated user
            # so, just return that user
            return user

        # if there is not user associated with this rpx
        # try to match user by email
        if email and provider in TRUSTED_PROVIDERS:
            # beware - this would allow account theft, so we only allow it
            # for trusted providers
            user_candidates=User.objects.all().filter(email=email)
            # if unambiguous, do it. otherwise, don't.
            if user_candidates.count() == 1:
                [user] = user_candidates
                return user
            elif user_candidates.count() > 1:
                return None

        # still no single user.
        # we didn't find any user with such an email (if was given)
        if not user:
            # create a new user - but there may be duplicate user names.
            username = nickname
            user = None
            try:
                i=0
                while True:
                    User.objects.get(username=username)
                    username = permute_name(nickname, i)
                    i += 1
            except User.DoesNotExist:
                # available name!
                # create new user
                if 'Facebook' == provider:
                    # without initial email
                    # because email provided by facebook is not correct
                    user = User.objects.create_user(username, '')
                else:
                    user = User.objects.create_user(username, email)
                user.is_new = True
                user.save()

        # create new rpx record and link it to the user
        rpxdata = RpxData(identifier=rpx_id)
        if profile_pic_url:
            rpxdata.profile_pic_url=profile_pic_url
        if info_page_url:
            rpxdata.info_page_url=info_page_url
        if provider:
            rpxdata.provider=provider
        rpxdata.user = user
        rpxdata.save()
        return user
            

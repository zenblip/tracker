# -*- coding: utf-8 -*-
'''
Created on 2015/1/21

@author: sushih-wen
'''
import json
import logging
from datetime import datetime, timedelta
from uuid import uuid4
from google.appengine.ext import testbed
from ferrisnose import AppEngineTest, AppEngineWebTest, FerrisAppTest
from app.models.user_info import UserInfo
from app.models.signal import Signal


class TestBase(AppEngineWebTest):

    """
    test
    """

    def setUp(self):
        AppEngineWebTest.setUp(self)

    def create_user(self,
                    sender='sender@asdf.com',
                    name='KJ Chang',
                    given_name='KJ',
                    family_name='Change',
                    picture='https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg',
                    gender='male',
                    locale='en',
                    orgs=['test'],
                    role=0,
                    tz_offset=9,
                    last_seen=datetime.utcnow() - timedelta(days=1),
                    domain='asdf.com',
                    google_id='1234567890123456789',
                    ):

        user = UserInfo.create_user(
            email=sender,
            name=name,
            given_name=given_name,
            family_name=family_name,
            picture=picture,
            gender=gender,
            locale=locale,
            orgs=orgs,
            role=role,
            tz_offset=tz_offset,
            last_seen=last_seen,
            domain=domain,
            google_id=google_id
        )
        user.put()
        return user

    def create_legit_user(self):
        return self.create_user(role=1)

    def request_create_signal(self, sender='sender@asdf.com', subject='Mail to Su', to='', cc='', bcc='', client='gmail'):
        r = self.testapp.post('/signals/add?sync=1',
                              {'sender': sender,
                               'subject': subject,
                               'token': str(uuid4()).replace('-', '')[:12],
                               'to': to,
                               'cc': cc,
                               'bcc': bcc,
                               'client': client},
                              xhr=True)
        return r

    def create_signal(self, sender='sender@asdf.com', subject='Mail to Su', to='蘇 <to1@asdf.com>'):

        r = self.request_create_signal(sender, subject, to=to)
        logging.debug(r.status)
        logging.debug(r.body)
        #signal = json.loads(r.body)['signal']
        signal = Signal.find_by_properties(token=json.loads(r.body)['signal']['token'])
        return signal


class TestBaseWithMail(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        self.mail_stub = self.testbed.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

#          █  █ █▄ █ █▄ █ █▀▀ ▀▄▀ █▀█ █▄ █
#          ▀▄▄▀ █ ▀█ █ ▀█ ██▄  █  █▄█ █ ▀█ ▄
#                © Copyright 2024
#            ✈ https://t.me/unneyon

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit this file without direct permission from the author.
# You can redistribute this file without any changes.

import time
from datetime import date, timedelta
from hashlib import md5
from io import BytesIO
from typing import Optional, Dict, List, Union

import httpx
from httpx import AsyncClient, Response

from .errors import (
    AuthError, SchoolNotFoundError
)
from . import types

__all__ = ['NetSchoolAPI']

from netschoolapi.async_client_wrapper import AsyncClientWrapper, Requester


async def _die_on_bad_status(response: Response):
    if not response.is_redirect:
        response.raise_for_status()


class NetSchoolAPI:
    def __init__(self, url: str, default_requests_timeout: int = None):
        url = url.rstrip('/')
        self._wrapped_client = AsyncClientWrapper(
            async_client=AsyncClient(
                base_url=f'{url}',
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                  "Chrome/114.0.0.0 YaBrowser/23.7.5.739 Yowser/2.5 Safari/537.36 NetSchoolAPI/5.0.3",
                    "Referer": url,
                    "Accept": "application/json, text/plain, */*"
                },
                event_hooks={'response': [_die_on_bad_status]},
            ),
            default_requests_timeout=default_requests_timeout,
        )

        self._student_id = -1
        self._year_id = -1
        self._school_id = -1

        self._assignment_types: Dict[int, str] = {}
        self._login_data = ()
        self._access_token = None

    async def __aenter__(self) -> 'NetSchoolAPI':
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        await self.logout()


    async def request(
        self,
        method: str,
        path: str,
        requests_timeout: int = None,
        need_json: bool = True,
        need_prefix: bool = True,
        **kwargs
    ):
        path = path[1:] if path.startswith("/") else path
        if need_prefix:
            path = f"webapi/{path}"
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method=method, url=path,
                **kwargs
            )
        )
        return (resp.json() if need_json else resp)


    async def _request_with_optional_relogin(
            self, requests_timeout: Optional[int], request: httpx.Request,
            follow_redirects=False):
        try:
            response = await self._wrapped_client.request(
                requests_timeout, request, follow_redirects
            )
        except httpx.HTTPStatusError as http_status_error:
            if (
                http_status_error.response.status_code
                == httpx.codes.UNAUTHORIZED
            ):
                if self._login_data:
                    await self.login(*self._login_data)
                    return await self._request_with_optional_relogin(
                        requests_timeout, request, follow_redirects
                    )
                else:
                    raise AuthError(
                        ".login() before making requests that need "
                        "authorization"
                    )
            else:
                raise http_status_error
        else:
            return response


    async def login(
            self, user_name: str, password: str,
            school_name_or_id: Union[int, str],
            requests_timeout: int = None):
        requester = self._wrapped_client.make_requester(requests_timeout)
        # Getting the `NSSESSIONID` cookie for `auth/getdata`
        await requester(self._wrapped_client.client.build_request(
            method="GET", url="webapi/logindata"
        ))

        # Getting the `NSSESSIONID` cookie for `login`
        response = await requester(self._wrapped_client.client.build_request(
            method="POST", url='webapi/auth/getdata'
        ))
        login_meta = response.json()
        salt = login_meta.pop('salt')
        self.ver = login_meta['ver']

        encoded_password = md5(
            password.encode('windows-1251')
        ).hexdigest().encode()
        pw2 = md5(salt.encode() + encoded_password).hexdigest()
        pw = pw2[: len(password)]

        self._school_id = (
            await self._get_school_id(school_name_or_id, requester)
        ) if isinstance(school_name_or_id, str) else school_name_or_id

        try:
            response = await requester(
                self._wrapped_client.client.build_request(
                    method="POST",
                    url='webapi/login',
                    data={
                        'loginType': 1,
                        'scid': (
                            (await self._get_school_id(
                                school_name_or_id, requester,
                            ))
                            if isinstance(school_name_or_id, str) else
                            school_name_or_id
                        ),
                        'un': user_name,
                        'pw': pw,
                        'pw2': pw2,
                        **login_meta,
                    },
                )
            )
        except httpx.HTTPStatusError as http_status_error:
            if http_status_error.response.status_code == httpx.codes.CONFLICT:
                try:
                    response_json = http_status_error.response.json()
                except httpx.ResponseNotRead:
                    pass
                else:
                    if 'message' in response_json:
                        raise AuthError(
                            http_status_error.response.json()['message'], http_status_error.response.json()
                        )
                raise AuthError(
                    resp=http_status_error.response.json()
                )
            else:
                raise http_status_error
        auth_result = response.json()

        if 'at' not in auth_result:
            raise AuthError(auth_result['message'], auth_result)

        self._access_token = auth_result["at"]
        self._wrapped_client.client.headers['at'] = auth_result['at']

        response = await requester(self._wrapped_client.client.build_request(
            method="GET", url='webapi/student/diary/init',
        ))
        diary_info = response.json()
        student = diary_info['students'][diary_info['currentStudentId']]
        self._student_id = student['studentId']

        response = await requester(self._wrapped_client.client.build_request(
            method="GET", url='webapi/years/current'
        ))
        year_reference = response.json()
        self._year_id = year_reference['id']

        response = await requester(self._wrapped_client.client.build_request(
            method="GET", url="webapi/grade/assignment/types", params={"all": False},
        ))
        assignment_reference = response.json()
        self._assignment_types = {
            assignment['id']: assignment['name']
            for assignment in assignment_reference
        }
        self._login_data = (user_name, password, school_name_or_id)


    async def download_attachment(
            self, attachment_id: int, buffer: BytesIO,
            requests_timeout: int = None):
        content = (await self._request_with_optional_relogin(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="GET", url=f"webapi/attachments/{attachment_id}",
                )
        )).content
        import logging
        logging.error(buffer)
        buffer.write(content)


    async def diary(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None,
        requests_timeout: int = None,
    ) -> types.DiarySchema:
        if not start:
            monday = date.today() - timedelta(days=date.today().weekday())
            start = monday
        if not end:
            end = start + timedelta(days=5)

        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url="webapi/student/diary",
                params={
                    'schoolId': self._school_id,
                    'studentId': self._student_id,
                    'vers': self.ver,
                    'weekEnd': end.isoformat(),
                    'weekStart': start.isoformat(),
                    'withLaAssigns': True,
                    'yearId': self._year_id
                },
            )
        )
        diary_schema = types.Diary()
        diary_schema.context['assignment_types'] = self._assignment_types
        diary = diary_schema.load(response.json())
        return diary  # type: ignore


    async def mysettings(
        self,
        requests_timeout: int = None
    ) -> types.StudentSchema:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url="webapi/mysettings"
            )
        )
        student_schema = types.Student()
        student_schema.context['year_id'] = self._year_id
        student = student_schema.load(response.json())
        return student  # type: ignore


    async def overdue(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None,
        requests_timeout: int = None,
    ) -> List[types.AssignmentSchema]:
        if not start:
            monday = date.today() - timedelta(days=date.today().weekday())
            start = monday
        if not end:
            end = start + timedelta(days=5)

        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url='webapi/student/diary/pastMandatory',
                params={
                    'studentId': self._student_id,
                    'yearId': self._year_id,
                    'weekStart': start.isoformat(),
                    'weekEnd': end.isoformat(),
                },
            )
        )
        assignments_schema = types.Assignment()
        assignments_schema.context['assignment_types'] = self._assignment_types
        assignments = assignments_schema.load(response.json(), many=True)
        return assignments  # type: ignore


    async def announcements(
            self, take: Optional[int] = -1,
            requests_timeout: int = None) -> List[types.AnnouncementSchema]:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url="webapi/announcements",
                params={"take": take},
            )
        )
        announcements = types.Announcement().load(response.json(), many=True)
        return announcements  # type: ignore


    async def attachments(
            self, assignment_id: int,
            requests_timeout: int = None) -> List[types.AttachmentSchema]:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="POST",
                url='webapi/student/diary/get-attachments',
                params={'studentId': self._student_id},
                json={'assignId': [assignment_id]},
            ),
        )
        response = response.json()
        if not response:
            return []
        attachments_json = response[0]['attachments']
        attachments = types.Attachment().load(attachments_json, many=True)
        return attachments  # type: ignore


    async def get_mail(
        self, mail_type: str, # `inbox` or `sent`
        page: int = 1, count: int = 999, requests_timeout: int = None
    ) -> types.MessagesSchema:
        mail_filters = {
            "inbox": {
                "filterContext": {
                    "selectedData": [{
                        "filterId": "MailBox",
                        "filterValue": "Inbox",
                        "filterText": "Входящие"
                    }],
                    "params": None
                },
                "fields": ["author", "subject", "sent"],
                "page": page, "pageSize": count,
                "search": None,
                "order": {"fieldId": "sent", "ascending": False}
            },
            "sent": {
                "filterContext": {
                    "selectedData": [{
                        "filterId": "MailBox",
                        "filterValue": "Sent",
                        "filterText": "Отправленные"
                    }],
                    "params": None
                },
                "fields": ["toNames", "subject", "sent"],
                "page": page, "pageSize": count,
                "search": None,
                "order": {"fieldId": "sent", "ascending": False}
            }
        }
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="POST",
                url="webapi/mail/registry",
                json=mail_filters[mail_type]
            )
        )
        msgs = types.Messages().load(response.json())
        return msgs  # type: ignore


    async def get_message(
        self, message_id: int,
        requests_timeout: int = None
    ) -> types.MessageSchema:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url=f"webapi/mail/messages/{message_id}/read",
                params={
                    "userId": self._student_id
                }
            )
        )
        import logging; logging.error(response.json())
        message = types.Message().load(response.json())
        return message  # type: ignore


    async def school(self, sid: int, requests_timeout: int = None) -> types.SchoolSchema:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url='webapi/schools/{0}/card'.format(self._school_id if self._school_id != -1 else sid),
            )
        )
        school = types.School().load(response.json())
        return school  # type: ignore


    async def logout(self, requests_timeout: int = None):
        try:
            await self._wrapped_client.request(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="POST",
                    url='webapi/auth/logout',
                )
            )
        except httpx.HTTPStatusError as http_status_error:
            if (
                http_status_error.response.status_code
                == httpx.codes.UNAUTHORIZED
            ):
                # Session is dead => we are logged out already
                # OR
                # We are logged out already
                pass
            else:
                raise http_status_error


    async def full_logout(self, requests_timeout: int = None):
        await self.logout(requests_timeout)
        await self._wrapped_client.client.aclose()


    async def close(self):
        await self._wrapped_client.client.aclose()


    async def getCountries(self, requests_timeout: int = None):
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url='webapi/prepareloginform'
            )
        )
        c = resp.json()['countries']
        return c


    async def getProvinces(self, countryId, requests_timeout: int = None):
        params = {
            "cid": countryId
        }
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url='webapi/prepareloginform',
                params=params
            )
        )
        return resp.json()['provinces']


    async def getCities(self, countryId, provincesId, requests_timeout: int = None):
        params = {
            "cid": countryId,
            "pid": provincesId
        }

        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url='webapi/prepareloginform',
                params=params
            )
        )
        return resp.json()['cities']


    async def getSchools(
        self, countryId, provinceId, cityId, requests_timeout: int = None
    ):
        params = {
            "cid": countryId,
            "pid": provinceId,
            "cn": cityId
        }
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url='webapi/prepareloginform',
                params=params
            )
        )
        return resp.json()['schools']


    async def schools(
            self, requests_timeout: int = None) -> List[types.ShortSchoolSchema]:
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url="webapi/schools/search",
            )
        )
        schools = types.ShortSchool().load(resp.json(), many=True)
        return schools  # type: ignore


    async def getCurrentStudentId(self, requests_timeout: int = None):
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url="webapi/student/diary/init",
            )
        )
        diary_info = resp.json()
        student = diary_info['students'][0]
        studentId = student['studentId']
        return studentId


    async def _get_school_id(
            self, school_name: str,
            requester: Requester) -> Dict[str, int]:
        schools = (await requester(
            self._wrapped_client.client.build_request(
                method="GET",
                url="webapi/schools/search?name={school_name}",
            )
        )).json()

        for school in schools:
            if school["shortName"] == school_name:
                self._school_id = school['id']
                return school["id"]
        raise SchoolNotFoundError(school_name)


    async def download_profile_picture(
            self, user_id: int, buffer: BytesIO,
            requests_timeout: int = None):
        buffer.write((
            await self._request_with_optional_relogin(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="GET",
                    url="webapi/users/photo",
                    params={"at": self._access_token, "userId": user_id},
                ),
                follow_redirects=True,
            )
        ).content)
        return buffer
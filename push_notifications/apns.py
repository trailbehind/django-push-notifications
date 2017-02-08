"""
Apple Push Notification Service
Documentation is available on the iOS Developer Library:
https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html
"""

from django.core.exceptions import ImproperlyConfigured
from . import NotificationError
from .settings import PUSH_NOTIFICATIONS_SETTINGS as SETTINGS

from gobiko.apns import APNsClient

class APNSError(NotificationError):
	pass


class APNSServerError(APNSError):
	def __init__(self, status, identifier):
		super(APNSServerError, self).__init__(status, identifier)
		self.status = status
		self.identifier = identifier


class APNSDataOverflow(APNSError):
	pass


def _get_client(kwargs):
	certfile = kwargs.get("certfile", SETTINGS.get("APNS_CERTIFICATE"))
	key_file = kwargs.get("keyfile", SETTINGS.get("APNS_KEY_FILE"))
	key = kwargs.get("key", SETTINGS.get("APNS_KEY"))
	team_id = kwargs.get("teamid", SETTINGS.get("APNS_TEAM_ID"))
	key_id = kwargs.get("keyid", SETTINGS.get("APNS_KEY_ID"))
	bundle_id = kwargs.get("bundleid", SETTINGS.get("APNS_BUNDLE_ID"))


	if key_file:
		client = APNsClient(
			team_id=team_id,
			bundle_id=bundle_id,
			auth_key_id=key_id,
			auth_key_filepath=key_file,
			use_sandbox=True
		)
	elif key:
		client = APNsClient(
			team_id=team_id,
			bundle_id=bundle_id,
			auth_key_id=key_id,
			auth_key=key,
			use_sandbox=True
		)
	elif certfile:
		pass
	else:
		raise ImproperlyConfigured(
			'You need to set PUSH_NOTIFICATIONS_SETTINGS["APNS_CERTIFICATE"],' +
			' PUSH_NOTIFICATIONS_SETTINGS["APNS_KEY_FILE"], or PUSH_NOTIFICATIONS_SETTINGS["APNS_KEY"]' +
			' to send messages through APNS.'
		)


def apns_send_message(registration_id, alert, **kwargs):
	"""
	Sends an APNS notification to a single registration_id.
	This will send the notification as form data.
	If sending multiple notifications, it is more efficient to use
	apns_send_bulk_message()

	Note that if set alert should always be a string. If it is not set,
	it won't be included in the notification. You will need to pass None
	to this for silent notifications.
	"""

	client = _get_client(kwargs)
	try:
		client.send_message(
			registration_id, 
			alert,
			badge=kwargs.get("badge", None),
			sound=kwargs.get("source", None),
			category=kwargs.get("category", None),
			content_available=kwargs.get("content_available", False),
			action_loc_key=kwargs.get("action_loc_key", None),
			loc_key=kwargs.get("loc_key", None),
			loc_args=kwargs.get("loc_args", []),
			extra=kwargs.get("extra", {}),
			identifier=kwargs.get("identifier", None),
			expiration=kwargs.get("expiration", None),
			priority=kwargs.get("priority", 10),
			topic=kwargs.get("topic", None)
		)
	except:
		pass


def apns_send_bulk_message(registration_ids, alert, **kwargs):
	"""
	Sends an APNS notification to one or more registration_ids.
	The registration_ids argument needs to be a list.

	Note that if set alert should always be a string. If it is not set,
	it won't be included in the notification. You will need to pass None
	to this for silent notifications.
	"""
	client = _get_client(kwargs)
	try:
		client.send_bulk_message(
			registration_ids,
			alert,
			badge=kwargs.get("badge", None),
			sound=kwargs.get("source", None),
			category=kwargs.get("category", None),
			content_available=kwargs.get("content_available", False),
			action_loc_key=kwargs.get("action_loc_key", None),
			loc_key=kwargs.get("loc_key", None),
			loc_args=kwargs.get("loc_args", []),
			extra=kwargs.get("extra", {}),
			identifier=kwargs.get("identifier", None),
			expiration=kwargs.get("expiration", None),
			priority=kwargs.get("priority", 10),
			topic=kwargs.get("topic", None)
		)
	except:
		pass

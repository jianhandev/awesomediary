from google.cloud import dialogflow
from google.oauth2 import service_account

from constants import GOOGLE_SERVICE_ACCOUNT_FILE_PATH, DEFAULT_DIALOGFLOW_LANGUAGE_CODE, DIALOGFLOW_PROJECT_ID

credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE_PATH)
session_client = dialogflow.SessionsClient(credentials=credentials)


# Attempts to match an intent with given free text input
def detect_intent_via_text(session_id, text):
    text_input = dialogflow.TextInput(text=text, language_code=DEFAULT_DIALOGFLOW_LANGUAGE_CODE)

    return __detect_intent(session_id, dialogflow.QueryInput(text=text_input))


# Attempts to match an intent with given event input
def detect_intent_via_event(session_id, event):
    event_input = dialogflow.EventInput(name=event, language_code=DEFAULT_DIALOGFLOW_LANGUAGE_CODE)

    return __detect_intent(session_id, dialogflow.QueryInput(event=event_input))


def __detect_intent(session_id, query_input):
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    return response.query_result

import json
from ast import literal_eval
from typing import List, Union
from .Entity import Entity
from . import PlatformEnum, ImageDisplayOptions, ResponseMediaType
from .BasicCard import BasicCard
from .BrowseCarouselCard import BrowseCarouselCard
from .BrowseCarouselCardItem import BrowseCarouselCardItem
from .Button import Button
from .Card import Card
from .CarouselItem import CarouselItem
from .CarouselSelect import CarouselSelect
from .ColumnProperties import ColumnProperties
from .Context import Context
from .EventInput import EventInput
from .GooglePayload import GooglePayload
from .Image import Image
from .LinkOutSuggestion import LinkOutSuggestion
from .ListItem import ListItem
from .ListSelect import ListSelect
from .MediaContent import MediaContent
from .MediaObject import MediaObject
from .Message import Message
from .Payload import Payload
from .QuickReplies import QuickReplies
from .SimpleResponse import SimpleResponse
from .SimpleResponses import SimpleResponses
from .Suggestion import Suggestion
from .Suggestions import Suggestions
from .TableCard import TableCard
from .TableCardRow import TableCardRow
from .Text import Text
from GoogleActions import ImageDisplayOptions as GoogleImageDisplayOptions
from google.auth import jwt
from .SessionEntityType import SessionEntityType, EntityOverrideMode


class DialogFlow(dict):
    """

    Main class to handle interface with google actions
    Dialogflow Request:
    {
  'responseId': 'c4b863dd-aafe-41ad-a115-91736b665cb9',
  'queryResult': {
    'queryText': 'GOOGLE_ASSISTANT_WELCOME',
    'action': 'input.welcome',
    'parameters': {},
    'allRequiredParamsPresent': true,
    'fulfillmentText': '',
    'fulfillmentMessages': [],
    'outputContexts': [
      {
        'name': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/google_assistant_welcome'
      },
      {
        'name': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_screen_output'
      },
      {
        'name': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/google_assistant_input_type_voice'
      },
      {
        'name': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_audio_output'
      },
      {
        'name': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_web_browser'
      },
      {
        'name': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_media_response_audio'
      }
    ],
    'intent': {
      'name': 'projects/${PROJECTID}/agent/intents/8b006880-0af7-4ec9-a4c3-1cc503ea8260',
      'displayName': 'Default Welcome Intent'
    },
    'intentDetectionConfidence': 1,
    'diagnosticInfo': {},
    'languageCode': 'en-us'
  },
  'originalDetectIntentRequest': {
    'source': 'google',
    'version': '2',
    'payload': {
      'isInSandbox': true,
      'surface': {
        'capabilities': [
          {
            'name': 'actions.capability.SCREEN_OUTPUT'
          },
          {
            'name': 'actions.capability.AUDIO_OUTPUT'
          },
          {
            'name': 'actions.capability.WEB_BROWSER'
          },
          {
            'name': 'actions.capability.MEDIA_RESPONSE_AUDIO'
          }
        ]
      },
      'inputs': [
        {
          'rawInputs': [
            {
              'query': 'query from the user',
              'inputType': 'KEYBOARD'
            }
          ],
          'arguments': [
            {
              'rawText': 'query from the user',
              'textValue': 'query from the user',
              'name': 'text'
            }
          ],
          'intent': 'actions.intent.TEXT'
        }
      ],
      'user': {
        'lastSeen': '2018-03-16T22:08:48Z',
        'permissions': [
          'UPDATE'
        ],
        'locale': 'en-US',
        'userId': 'ABwppHEvwoXs18xBNzumk18p5h02bhRDp_riW0kTZKYdxB6-LfP3BJRjgPjHf1xqy1lxqS2uL8Z36gT6JLXSrSCZ'
      },
      'conversation': {
        'conversationId': '${SESSIONID}',
        'type': 'NEW'
      },
      'availableSurfaces': [
        {
          'capabilities': [
            {
              'name': 'actions.capability.SCREEN_OUTPUT'
            },
            {
              'name': 'actions.capability.AUDIO_OUTPUT'
            }
          ]
        }
      ]
    }
  },
  'session': 'projects/${PROJECTID}/agent/sessions/${SESSIONID}'
}

    Dialogflow response:
    {
      'fulfillmentText': string,
      'fulfillmentMessages': [
        {
          object(Message)
        }
      ],
      'source': string,
      'payload': {
        object
      },
      'outputContexts': [
        {
          object(Context)
        }
      ],
      'followupEventInput': {
        object(EventInput)
      },
      'session_entity_types': [
        {
            object(SessionEntityType)
        }
      ]
    }
    """

    def __init__(self, request_data_json: dict, version: str = 'v1', create_payload_object: bool = False,
                 client_key: str = None):
        super().__init__()

        self._source = ''
        self._session_id = ''
        self._result = {}
        self._parameters = {}
        self._action = ''

        self.create_payload_object = create_payload_object
        self._max_msg_length = 550
        self['fulfillmentMessages']: List[Message] = list()
        self['source'] = None
        self['followupEventInput'] = None
        self['fulfillmentText'] = ''
        self['session_entity_types'] = list()
        self._user_given_name = ''
        self._user_family_name = ''
        self._user_email = ''
        self._user_verification_status = ''
        self._user_storage = dict()

        if self.create_payload_object:
            self['payload'] = Payload('google', GooglePayload())

        self.load_request_data(request_data_json=request_data_json, version=version, client_key=client_key)

    def load_request_data(self, request_data_json: dict, version: str = 'v1', client_key: str = None):

        print('initializing Dialogflow with: ', version, request_data_json)
        assert isinstance(request_data_json, dict)
        super(DialogFlow, self).__init__()

        self._session_id = request_data_json.get('session')
        print('session_id : ', self._session_id)

        self._result = request_data_json.get('queryResult') or request_data_json.get('result')
        print('result: ', self._result)

        self._parameters = self._result.get('parameters')
        print('parameters: ', self._parameters)

        self._action = self._result.get('action')
        if self._action == 'input.welcome':
            self._action = 'welcome'
        print('action: ', self._action)

        self._source = None

        if request_data_json.get('originalDetectIntentRequest') is not None:
            self._source = request_data_json.get('originalDetectIntentRequest').get('source')

        self['outputContexts']: List[Context] = []
        # contexts = self._result.get('outputContexts') or self._result.get('contexts')
        # for context in contexts:
        #    self['outputContexts'].append(Context(context.get('name')))
        print('outputContexts: ', self['outputContexts'])

        if request_data_json.get('originalDetectIntentRequest'):
            if request_data_json.get('originalDetectIntentRequest').get('payload'):
                if request_data_json.get('originalDetectIntentRequest').get('payload').get('user'):

                    self._user_verification_status = request_data_json.get('originalDetectIntentRequest').get(
                        'payload').get('user').get('userVerificationStatus')

                    self._user_storage = request_data_json.get('originalDetectIntentRequest').get(
                        'payload').get('user').get('userStorage')

                    if isinstance(self._user_storage, str):
                        # converting user storage to string since its in
                        self._user_storage = self._user_storage.replace('null', '""')
                        self._user_storage = literal_eval(self._user_storage)

                    if request_data_json.get('originalDetectIntentRequest').get('payload').get('user').get('idToken'):
                        import http.client
                        conn = http.client.HTTPSConnection("www.googleapis.com")
                        conn.request("GET", "/oauth2/v1/certs")
                        r1 = conn.getresponse()
                        print(r1.status, r1.reason)
                        certs = json.loads(r1.read().decode('utf-8'))  # This will return entire content.
                        print(type(certs), certs)

                        encoded_user_token = request_data_json.get('originalDetectIntentRequest').get('payload').get(
                            'user').get('idToken')
                        print('encoded_token: ', encoded_user_token)
                        decoded_user_token = jwt.decode(encoded_user_token, certs=certs, verify=True,
                                                        audience=client_key)
                        print('decoded_token: ', decoded_user_token)
                        self._user_given_name = decoded_user_token.get('given_name')
                        self._user_family_name = decoded_user_token.get('family_name')
                        self._user_email = decoded_user_token.get('email')

    @property
    def user_given_name(self):
        return self._user_given_name

    @property
    def user_family_name(self):
        return self._user_family_name

    @property
    def user_email(self):
        return self._user_email

    @property
    def session_id(self):
        return self._session_id

    @property
    def action(self):
        return self._action

    @property
    def parameters(self):
        return self._parameters

    def get_parameter(self, parameter_name: str):
        return self._parameters.get(parameter_name)

    @property
    def user_storage(self):
        return self._user_storage

    @property
    def user_verification_status(self):
        return self._user_verification_status

    # Source functions
    @property
    def source(self) -> str:
        return self['source']

    @source.setter
    def source(self, source: str):
        assert isinstance(source, str)
        self['source'] = source

    def add_source(self, source: str):
        self.source = source
        return self['source']

    # Context functions
    @property
    def contexts(self) -> List[Context]:
        return self['outputContexts']

    @contexts.setter
    def contexts(self, context_name: str, lifespan: int = 0, **parameters):
        assert isinstance(context_name, str)
        assert isinstance(lifespan, int)

        for context in self['outputContexts']:
            if context.name == context_name:
                context.lifespan_count = lifespan
                context.update_parameters(**parameters)

    def add_context(self, context_name: str, lifespan: int = 0, **parameters) -> List[Context]:
        assert isinstance(context_name, str)
        assert isinstance(lifespan, int)

        for context in self['outputContexts']:
            if context.name == context_name:
                context.update_parameters(**parameters)
                context.lifespan = lifespan
                return self['outputContexts']

        self['outputContexts'].append(Context(name=context_name, lifespan_count=lifespan, **parameters))
        print('context: ', self['outputContexts'])
        return self['outputContexts']

    def delete_context(self, context_names) -> bool:

        if len(context_names) == 0:
            self['outputContexts'] = list()

        else:
            for context_name in context_names:
                assert isinstance(context_name, str)

                for context in self['outputContexts']:
                    if context.name == context_name:
                        self['outputContexts'].remove(context)

        return True

    @property
    def session_entity_types(self):
        return self['session_entity_types']

    @session_entity_types.setter
    def session_entity_types(self, session_entity_types: List[SessionEntityType]):
        self['session_entity_types'] = session_entity_types

    def add_session_entity(self, entity_name: str, entity_overide_mode: EntityOverrideMode, entities: List[Entity]):
        self['session_entity_types'].append(SessionEntityType(name=self._session_id + '/entityTypes/' + entity_name,
                                                              entity_overide_mode=entity_overide_mode,
                                                              entities=entities))

    # Followup_event_input functions
    @property
    def followup_event_input(self):
        return self['followupEventInput']

    def add_followup_event_input(self, name, language_code, **parameters):
        self['followupEventInput'] = EventInput(name=name, language_code=language_code, **parameters)

    # Fulfillment_messages functions
    @property
    def fulfillment_messages(self) -> List[Message]:
        return self['fulfillmentMessages']

    @fulfillment_messages.setter
    def fulfillment_messages(self, message_list: List[Message]):
        for message in message_list:
            self.add_fulfillment_messages(message)

    def add_fulfillment_messages(self, message: Message) -> List[Message]:

        print('adding fulfillment_message: ', type(message), message)
        assert isinstance(message, Message)

        # only add the message if its simple responses or if not then theres already a simple response in the
        # fulfillment messages
        if self.has_fulfillment_message_type(message.platform,
                                             'simple_responses') or message.message_type == 'simple_responses':
            # check if the same type of message object already exists in the list,if yes then modify it or add a new one
            if self.has_fulfillment_message_type(message.platform,
                                                 message.message_type) and message.message_type == 'payload':
                self.get_fulfillment_message(message.platform, message.message_type).message_object = \
                    message.message_object
            else:
                self.fulfillment_messages.append(message)

        return self['fulfillmentMessages']

    def delete_messages(self):
        self['fulfillmentMessages'] = []
        return self

    def has_fulfillment_message_type(self, platform, message_type) -> bool:
        for message in self.fulfillment_messages:
            if message_type == message.message_type and message.platform == platform:
                return True

        return False

    def get_fulfillment_message(self, platform, message_type):
        print('looking for fulfillment message for', platform, message_type)
        for message in self.fulfillment_messages:
            print('in message ', message.message_type, message.platform)
            if message_type == message.message_type and message.platform == platform:
                print('found it: ', message)
                return message

        return KeyError()

    # Payload functions
    @property
    def payload(self):
        return self.get('payload')

    @payload.setter
    def payload(self, payload):
        assert isinstance(payload, Payload)
        self['payload'] = payload

    def add_payload(self, payload: Union[GooglePayload, Payload]) -> Payload:
        if isinstance(payload, Payload):
            self.payload = payload
        elif isinstance(payload, GooglePayload):
            self.payload = Payload(payload_type='google', payload=payload)
        return self.payload

    # Fulfillment_text functions
    @property
    def fulfillment_text(self):
        """This function returns the text which is set for Dialogflow to show in response"""
        return self.get('fulfillmentText')

    @fulfillment_text.setter
    def fulfillment_text(self, display_text: str):
        """This function sets the dialogflow text response"""
        self['fulfillmentText'] = display_text

    # Helper functions for Message
    def add_text_message(self, platform: PlatformEnum, text_to_speech: str, ssml: str = '', display_text: str = ''):
        self.fulfillment_text = display_text if display_text else text_to_speech

        self.add_fulfillment_messages(Message(platform=platform, message_object=Text(text_to_speech)))

        if platform == PlatformEnum.ACTIONS_ON_GOOGLE:
            simple_responses: SimpleResponses = SimpleResponses(
                [SimpleResponse(text_to_speech=text_to_speech, ssml=ssml,
                                display_text=display_text)])
            print('simple_responses: ', simple_responses)
            self.add_fulfillment_messages(Message(platform=platform, message_object=simple_responses))

        if self.create_payload_object:

            if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
                self.add_fulfillment_messages(Message(platform=platform,
                                                      message_object=self.payload))
            fulfillment_message = self.get_fulfillment_message(platform=platform, message_type='payload')
            print('fulfillment_message: ', type(fulfillment_message), fulfillment_message)
            message_object = fulfillment_message.message_object
            print('message_object: ', type(message_object), message_object)
            payload_object = message_object.payload
            print('payload_object', type(payload_object), payload_object)
            payload_object.add_simple_response(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text)

        return self

    def add_image(self, platform: PlatformEnum, uri: str = '', accessibility_text: str = ''):
        print('adding image: ', platform, uri, accessibility_text)
        image = Image(image_uri=uri, accessibility_text=accessibility_text)
        self.add_fulfillment_messages(Message(platform=platform, message_object=image))
        return self

    def add_quick_replies(self, platform: PlatformEnum, title: str, quick_replies):
        print('adding quick_replies: ', platform, title, quick_replies)
        print('adding quick replies')
        print('platform:', platform)
        print('title:', title)
        print('quick_replies: ', quick_replies)
        quick_reply: QuickReplies = QuickReplies(title, quick_replies)
        self.add_fulfillment_messages(Message(platform=platform, message_object=quick_reply))

        if platform == PlatformEnum.ACTIONS_ON_GOOGLE:
            suggestions_list: List[Suggestion] = [Suggestion(title=item) for item in quick_replies]
            suggestions: Suggestions = Suggestions(suggestions=suggestions_list)
            self.add_fulfillment_messages(Message(platform=platform, message_object=suggestions))

        if self.create_payload_object:

            if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
                self.add_fulfillment_messages(Message(platform=platform,
                                                      message_object=self.payload))
            fulfillment_message = self.get_fulfillment_message(platform=platform, message_type='payload')
            print('fulfillment_message: ', type(fulfillment_message), fulfillment_message)
            message_object = fulfillment_message.message_object
            print('message_object: ', type(message_object), message_object)
            payload_object = message_object.payload
            print('payload_object', type(payload_object), payload_object)
            payload_object.add_suggestions(quick_replies)
            return self

    def add_card(self, platform: PlatformEnum, title: str, subtitle: str, image_uri: str, formatted_text: str = '',
                 image_text: str = '', buttons: List[Button] = None):
        print('adding card: ', platform, title, subtitle, image_uri, formatted_text, image_text, buttons)
        if buttons is None:
            buttons = []

        card: Card = Card(title=title, subtitle=subtitle, image_uri=image_uri, buttons=buttons)
        self.add_fulfillment_messages(Message(platform=platform, message_object=card))

        if platform == PlatformEnum.ACTIONS_ON_GOOGLE:
            basic_card: BasicCard = BasicCard(title=title, formatted_text=formatted_text, subtitle=subtitle,
                                              image=Image(image_uri=image_uri, accessibility_text=image_text),
                                              buttons=buttons)
            self.add_fulfillment_messages(Message(platform=platform, message_object=basic_card))

        if self.create_payload_object:
            if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
                self.add_fulfillment_messages(Message(platform=platform,
                                                      message_object=self.payload))
            self.get_fulfillment_message(platform=platform, message_type='payload').message_object.payload. \
                add_basic_card(title=title, formatted_text=formatted_text, subtitle=subtitle, image_uri=image_uri,
                               image_text=image_text, image_height=None, image_width=None, image_display_options=None,
                               buttons=buttons)

        return self

    # Google Actions Functions      
    def add_link_out_suggestion(self, platform: PlatformEnum, uri: str, destination_name: str):
        print('adding link_out_suggestion: ', platform, uri, destination_name)
        link_out_suggestion = LinkOutSuggestion(uri=uri, destination_name=destination_name)
        self.add_fulfillment_messages(Message(platform=platform, message_object=link_out_suggestion))

        if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
            self.add_fulfillment_messages(Message(platform=platform,
                                                  message_object=self.payload))

        if self.create_payload_object:
            self.get_fulfillment_message(platform=platform, message_type='payload').message_object.payload. \
                add_link_out_suggestions(url=uri, destination_name=destination_name)

        return link_out_suggestion

    def add_list_select(self, platform: PlatformEnum, title: str, subtitle: str, list_items: List[ListItem]):
        print('adding list_select: ', platform, title, subtitle, list_items)
        list_select = ListSelect(title=title, subtitle=subtitle, list_items=list_items)
        self.add_fulfillment_messages(Message(platform=platform, message_object=list_select))
        return list_select

    def add_carousel_select(self, platform: PlatformEnum, carousel_items: List[CarouselItem]):
        print('adding carousel_select: ', platform, carousel_items)
        carousel_select = CarouselSelect(carousel_items)
        self.add_fulfillment_messages(Message(platform=platform, message_object=carousel_select))
        return carousel_select

    def add_carousel_browse_card(self, platform: PlatformEnum, image_display_options: ImageDisplayOptions,
                                 browse_carousel_card_items: List[BrowseCarouselCardItem]):
        print('adding carousel_browse_card: ', platform, image_display_options, browse_carousel_card_items)
        carousel_browse = BrowseCarouselCard(image_display_options=image_display_options,
                                             browse_carousel_card_items=browse_carousel_card_items)
        self.add_fulfillment_messages(Message(platform=platform, message_object=carousel_browse))

        if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
            self.add_fulfillment_messages(Message(platform=platform,
                                                  message_object=self.payload))

        if self.create_payload_object:
            fulfillment_message = self.get_fulfillment_message(platform=platform, message_type='payload')
            print('fulfillment_message: ', type(fulfillment_message), fulfillment_message)
            message_object = fulfillment_message.message_object
            print('message_object: ', type(message_object), message_object)
            payload_object = message_object.payload
            print('payload_object', type(payload_object), payload_object)
            assert image_display_options in (ImageDisplayOptions.WHITE, ImageDisplayOptions.CROPPED,
                                             ImageDisplayOptions.IMAGE_DISPLAY_OPTIONS_UNSPECIFIED)
            if image_display_options == ImageDisplayOptions.IMAGE_DISPLAY_OPTIONS_UNSPECIFIED:
                image_display_options = GoogleImageDisplayOptions.DEFAULT
            payload_object.add_carousel_browse(image_display_options=image_display_options,
                                               browse_carousel_card_items=browse_carousel_card_items)
        return self

    def add_table_card(self, platform: PlatformEnum, title: str, subtitle: str, image_uri: str, accessibility_text: str,
                       image_height: int, image_width: int, column_properties: List[ColumnProperties],
                       rows: List[TableCardRow], buttons: List[Button]):
        print('adding table_card: ', platform, title, subtitle, image_uri, accessibility_text, image_height,
              image_width, column_properties, rows, buttons)
        table_card = TableCard(title=title, subtitle=subtitle, image=Image(image_uri=image_uri,
                                                                           accessibility_text=accessibility_text),
                               column_properties=column_properties, rows=rows, buttons=buttons)
        self.add_fulfillment_messages(Message(platform=platform, message_object=table_card))

        if self.create_payload_object:
            if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
                self.add_fulfillment_messages(Message(platform=platform,
                                                      message_object=self.payload))
            self.get_fulfillment_message(platform=platform, message_type='payload').message_object.payload. \
                add_table_card(self, title=title, subtitle=subtitle, image_uri=image_uri,
                               accessibility_text=accessibility_text, image_height=image_height,
                               image_width=image_width, column_properties=column_properties, rows=rows, buttons=buttons)
        return self

    def add_media(self, platform: PlatformEnum, media_type: ResponseMediaType, media_objects: List[MediaObject]):
        print('adding media: ', platform, media_type, media_objects)
        media_content = MediaContent(media_type=media_type, media_objects=media_objects)
        self.add_fulfillment_messages(Message(platform=platform, message_object=media_content))

        if self.create_payload_object:
            if not self.has_fulfillment_message_type(platform=platform, message_type='payload'):
                self.add_fulfillment_messages(Message(platform=platform,
                                                      message_object=self.payload))
            self.get_fulfillment_message(platform=platform, message_type='payload').message_object.payload. \
                add_media_response(media_type=media_type, media_objects=media_objects)
        return self

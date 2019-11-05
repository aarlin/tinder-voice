# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from fb_auth import get_auth_token
from phone_auth import send_phone_code, get_token_through_phone
from tinder_api import set_location

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "Welcome to the Tinder Lite! "
            "Would you like to authenicate with phone or authenticate through email?")

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False).response

class PhoneAuthIntentHandler(AbstractRequestHandler):
    """Handler for Phone Auth Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PhoneAuthIntent")(handler_input)
        
    def handle(self, handler_input):
        """Handler for Skill Launch."""
        # type: (HandlerInput) -> Response
        speech_text = "To access Tinder, we will send a request code to you. What is your phone number?"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
            False).response

class FacebookAuthIntentHandler(AbstractRequestHandler):
    """Handler for Facebook Auth Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FacebookAuthIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Skill Launch."""
        # type: (HandlerInput) -> Response
        speech_text_invalid_acc_link = "To access Tinder, you need to link your Facebook account"
        speech_text_valid_acc_link = "We have you authenticated. Where do you want to set your location to?"
        
        current_user = handler_input.request_envelope.context.system.user
        session_attributes = handler_input.attributes_manager.session_attributes

        print(current_user)

        if access_token not in current_user:
            return handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Facebook Authentication", speech_text)).set_should_end_session(
                False).response
        else:
            print(current_user.access_token)
            auth_token = get_auth_token(current_user.access_token)
            session_attributes['AUTH_TOKEN'] = auth_token
            return handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Facebook Authentication", speech_text)).set_should_end_session(
                False).response
            


class PhoneRequestCodeIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PhoneRequestCodeIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Phone Authentication Intent."""
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        if 'PhoneNumber' in slots:
            phone_number = slots['PhoneNumber'].value
            handler_input.attributes_manager.session_attributes['PHONE_NUMBER'] = phone_number
            request_code = send_phone_code(phone_number)
            handler_input.attributes_manager.session_attributes['REQUEST_CODE'] = request_code
        else:
            speech = "I'm not sure what your phone number is, please try again"
            reprompt = ("I'm not sure what your phone number is. "
                        "You can tell me your phone number by saying, "
                        "my phone number is ")

        speech_text = "What is the request code that was sent to your phone?"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
            True).response

class PhoneAuthenticationIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PhoneAuthenticationIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Phone Authentication Intent."""
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        session_attributes = handler_input.attributes_manager.session_attributes

        if 'SMSCode' in slots:
            sms_code = slots['SMSCode'].value
            session_attributes['SMS_CODE'] = sms_code
            auth_token = get_token_through_phone(sms_code, session_attributes['PHONE_NUMBER'], session_attributes['REQUEST_CODE'])

            session_attributes['AUTH_TOKEN'] = auth_token
        else:
            speech = "I'm not sure what your confirmation code is, please try again"
            reprompt = ("I'm not sure what your confirmation code is. "
                        "You can tell me your confirmation code by saying, "
                        "my confirmation code is ")

        speech_text = "Okay, we have you authenticated. Where do you want to set your location to?"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Phone Authentication", speech_text)).set_should_end_session(
            True).response

class SetLocationIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SetLocationIntent")(handler_input)

    def handle(self, handler_input):
        """Handler for Hello World Intent."""
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        session_attributes = handler_input.attributes_manager.session_attributes

        if 'City' in slots:
            city = slots['City'].value
            session_attributes['CITY'] = city
            response = set_location(session_attributes['AUTH_TOKEN'], city)
        else:
            speech = "I'm not sure what city you asked for, please try again"
            reprompt = ("I'm not sure what city you set your location to. "
                        "You can tell me your set city location by saying, "
                        "set my location to ")

        speech_text = "We set your location to {}".format(city)

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Location Set", speech_text)).set_should_end_session(
            True).response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PhoneAuthIntentHandler())
sb.add_request_handler(FacebookAuthIntentHandler())
sb.add_request_handler(PhoneRequestCodeIntentHandler())
sb.add_request_handler(PhoneAuthenticationIntentHandler())
sb.add_request_handler(SetLocationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

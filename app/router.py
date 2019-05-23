#!/usr/bin/env python3

import requests
from flask import Response, jsonify

from app import apartment_scraper
from app import apartment_bot

class Router:
    def __init__(self, configs):
        self.configs = configs

    def email(self, args):
        try:
            return self.__unauthorized()
        except Exception as ex:
            return self.__exception_error(ex)

    def slackbot(self, args):
        try:
            r = apartment_scraper.main(self.configs)
            return self.__handle_response(r)
        except Exception as ex:
            return self.__exception_error(ex)

    def slack_event(self, args):
        try:
            if args is None or args['type'] is None:
                return self.__bad_request('Missing `type` param')
            elif args['type'] == 'url_verification':
                return self.slack_event_verification(args['challenge'])
            elif args['type'] == 'event_callback':
                r = apartment_bot.main(self.configs, args['event'])
                return self.__handle_response(r)
            return self.__bad_request('Invalid `type` param')
        except Exception as ex:
            return self.__exception_error(ex)

    def slack_event_verification(self, challenge):
        resp = jsonify({ 'challenge': challenge })
        resp.status_code = 200
        return resp

    def __handle_response(self, response):
        if isinstance(response, requests.models.Response):
            if response:
                return self.__response_success(response.text, response.status_code)
            else:
                return self.__response_error(response.text, response.status_code)
        return self.__response_error('Could not send slack post')

    def __bad_request(self, error_message='Bad Request'):
        return self.__response_error(error_message, 400)

    def __unauthorized(self, error_message='Not Authorized'):
        return self.__response_error(error_message, 401)

    def __exception_error(self, exception):
        return self.__response_error(str(exception))

    def __response_success(self, success_message='OK', success_code=200):
        resp = jsonify({ 'message': success_message, 'success': True })
        resp.status_code = success_code
        return resp

    def __response_error(self, error_message='Internal Error', error_code=500):
        resp = jsonify({ 'error': error_message, 'success': False })
        resp.status_code = error_code
        return resp

#!/usr/bin/env python3

import gmail

def send(date, scrape_size, file_path, opts = {}):
    sender = opts['FROM'] if 'FROM' in opts else configurationEmailError('FROM')
    to = opts['TO'] if 'TO' in opts else configurationEmailError('TO')
    subject = opts['SUBJECT'].format(date) if 'SUBJECT' in opts else configurationEmailError('SUBJECT')
    body = opts['BODY'].format(date, scrape_size) if 'BODY' in opts else configurationEmailError('BODY')

    service = gmail.service()
    message = gmail.create_message(
        sender,
        to,
        subject,
        body,
        file_path
    )
    gmail.send_message(service, sender, message)

def configurationEmailError(field):
    raise ValueError('"{}" configuration missing').format(field)

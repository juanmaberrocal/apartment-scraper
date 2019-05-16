#!/usr/bin/env python3

import gmail

def send(date, scrape_size, file_path, opts = {}):
    sender = opts['FROM'] if 'FROM' in opts else configuration_email_error('FROM')
    to = opts['TO'] if 'TO' in opts else configuration_email_error('TO')
    subject = opts['SUBJECT'].format(date) if 'SUBJECT' in opts else configuration_email_error('SUBJECT')
    body = opts['BODY'].format(date, scrape_size) if 'BODY' in opts else configuration_email_error('BODY')

    service = gmail.service()
    message = gmail.create_message(
        sender,
        to,
        subject,
        body,
        file_path
    )
    gmail.send_message(service, sender, message)

def configuration_email_error(field):
    raise ValueError('"{}" configuration missing').format(field)

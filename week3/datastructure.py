#!/usr/bin/python3

results = {

    '152.157.64.5': {
        'osmatch': {}, 
        'ports': [
            {
                'protocol': 'tcp', 
                'portid':'22', 
                'state': 'open', 
                'reason': 'syn-ack', 
                'reason_ttl': '49', 
                'service': {'name': 'ssh', 'method': 'table', 'conf': '3'}, 
                'cpe': [], 
                'scripts': []
            },
            {
                'protocol':'tcp',
                'portid': '80', 
                'state': 'open', 
                'reason': 'syn-ack', 
                'reason_ttl': '49',
                'service': {'name': 'http', 'method': 'table', 'conf': '3'}, 
                'cpe': [], 
                'scripts':[]

            },
            {    
                'protocol': 'tcp', 
                'portid': '113',
                'state': 'closed',
                'reason': 'reset',
                'reason_ttl': '51',
                'service': {'name': 'ident', 'method': 'table', 'conf': '3'},
                'cpe': [],
                'scripts': []
            }, 
            {   
                'protocol': 'tcp', 
                'portid': '443', 
                'state': 'open',
                'reason': 'syn-ack',
                'reason_ttl': '49', 
                'service': {'name': 'https', 'method':'table', 'conf': '3'}, 
                'cpe': [], 
                'scripts': []
             }
                        
    ], 

        'hostname': [],
        'macaddress':None,
        'state': {'state': 'up', 'reason': 'syn-ack', 'reason_ttl': '49'}

    },

    'runtime': {
        'time': '1680459977', 
        'timestr': 'Sun Apr 2 11:26:17 2023',
        'elapsed':'15.08', 
        'summary': 'Nmap done at Sun Apr 2 11:26:17 2023; 1 IP address (1 host up) scanned in 15.08 seconds',
        'exit': 'success'
    }, 

    'stats': {
        'scanner': 'nmap',
        'args': '/usr/bin/nmap -v -oX - -sS 152.157.64.5', 
        'start': '1680459961',
        'startstr': 'Sun Apr 2 11:26:01 2023', 
        'version': '7.80', 
        'xmloutputversion':'1.04'

     },

    'task_results': [
         {'task': 'Ping Scan', 'time': '1680459962', 'extrainfo':'1 total hosts'}, 
         {'task': 'Parallel DNS resolution of 1 host.', 'time':'1680459972'}, 
         {'task': 'SYN Stealth Scan', 'time': '1680459976', 'extrainfo':'1000 total ports'}
           
        ]

    }

print(results)
















































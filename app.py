from flask import Flask, request
from pysnmp.hlapi import *
import os

app = Flask(__name__)

@app.route('/snmptrap', methods=['POST'])
def snmp_trap():
    data = request.json
    send_snmp_trap(data)
    return '', 200

def send_snmp_trap(data):
    solarwinds_ip = os.getenv('SOLARWINDS_IP')
    if not solarwinds_ip:
        raise ValueError("SOLARWINDS_IP environment variable not set")

    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public', mpModel=1),
            UdpTransportTarget((solarwinds_ip, 162)),
            ContextData(),
            'trap',
            NotificationType(
                ObjectIdentity('1.3.6.1.4.1.8072.2.3.0.1')
            ).addVarBinds(
                ('1.3.6.1.2.1.1.1.0', OctetString(str(data)))
            )
        )
    )
    if errorIndication:
        print(errorIndication)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# solarwinds-snmp

oc new-project solarwinds-snmp
oc new-build --binary --name=flask-app -l app=flask-app
oc start-build flask-app --from-dir=. --follow
oc create deployment flask-app --image=$(oc get is flask-app -o jsonpath='{.status.dockerImageRepository}')
oc set env deployment/flask-app APP_FILE=app.py SOLARWINDS_IP=10.10.10.10
oc expose deployment/flask-app --port=5000
oc expose svc/flask-app

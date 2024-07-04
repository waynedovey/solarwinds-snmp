# Build this on an OpenShift Cluster - Ensure Build services are enabled first 
```
oc new-project solarwinds-snmp
```
```
oc new-build --binary --name=flask-app -l app=flask-app
```
```
oc start-build flask-app --from-dir=. --follow
```
```
oc create deployment flask-app --image=$(oc get is flask-app -o jsonpath='{.status.dockerImageRepository}')
```
```
oc set env deployment/flask-app APP_FILE=app.py SOLARWINDS_IP=10.10.10.10
```
```
oc expose deployment/flask-app --port=5000
```

**Use with caution and only for external testing**
```
oc expose svc/flask-app
```
## Test the service Internally 

```
curl http://flask-app.solarwinds-snmp.svc:5000/snmptrap
```

## Set the Alertmanager Rule

```
receivers:
  - name: Default
    webhook_configs:
      - url: 'http://flask-app.solarwinds-snmp.svc:5000/snmptrap'
  - name: 'null'
  - name: snmp-webhook
    webhook_configs:
      - url: 'http://flask-app.solarwinds-snmp.svc:5000/snmptrap'
  - name: Watchdog
```


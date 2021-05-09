from kubernetes import client, config
import json
import csv
import pprint
import time
import subprocess
import datetime
 
count = 0
 
config.load_kube_config()
api = client.CustomObjectsApi()
resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="default", plural="pods")
 
 
value = input("load-test value? ")
 
cpu_data =  value+'_metrics-cpu.csv'
memory_data = value+'_metrics-memory.csv'
 
db_cpu_data =  value+'_db_metrics-cpu.csv'
db_memory_data = value+'_db_metrics-memory.csv'
 
#Pod name取得
subprocess.run("kubectl get pod | grep -v 'maria' | grep -v 'lb' | grep 'wordpress' | awk '{print $1}' > Pod_name.txt", shell=True)
with open("Pod_name.txt") as f:
  Pod_name = f.read()
Pod_name = Pod_name.replace('\n','')
 
##kubectl get pod | grep -v "maria" | grep -v "lb" | grep wordpress | awk '{print $1}'
 
#svcを取得
subprocess.run("kubectl get svc | grep -v 'maria' | grep wordpress | awk '{print $5}' > svc.txt", shell=True)
with open("svc.txt") as f:
  svc_port = f.read()
svc_port = svc_port[3:8]
#kubectl get svc | grep -v "maria" | grep wordpress | awk '{print $5}'
 
subprocess.Popen(['locust', '-f', './locustfile.py', '--host=http://ito-k3s-worker2:'+svc_port, '--headless', '-u', value, '-r', value, '--csv='+value, '-t', '60s'])

while count < 75:
  config.load_kube_config()
  api = client.CustomObjectsApi()
  resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="default", plural="pods")
  for pod in resource["items"]:
    
    if True == (Pod_name in pod["metadata"]["name"]):

      with open(cpu_data,'a') as file:
        print(pod['containers'][0]['usage']['cpu'], file=file)
 
      with open(memory_data,'a') as file:
        print(pod['containers'][0]['usage']['memory'], file=file)
 
  time.sleep(1)
  count+=1



# kube-cert-validity-check
## HELP kube_cert_validity_period cert validity period

## TYPE kube_cert_validity_period gauge

kube_cert_validity_period{filename="apiserver-kubelet-client.crt"} 1.755742141e+09

kube_cert_validity_period{filename="apiserver.crt"} 1.755742141e+09

kube_cert_validity_period{filename="ca.crt"} 2.039566141e+09

kube_cert_validity_period{filename="front-proxy-ca.crt"} 2.039566141e+09

kube_cert_validity_period{filename="front-proxy-client.crt"} 1.755742141e+09

![image](https://github.com/user-attachments/assets/9040068b-cb6c-42a4-bfff-98f17997649c)



## alert config
```yaml
  - alert: KubeCertValidityPeriod
    expr: kube_cert_validity_period{} - time() <= 5184000
    for: 5m
    labels:
      type: 'Cert'
      severity: 1
    annotations:
      summary: "Kube Cert Validity Period < 60 days"
```

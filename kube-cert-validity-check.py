#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
# -*- coding: utf-8 -*-
Time    : 2024/9/23 14:41:37
project name: kube-cert-validity-check.py
file    : kube-cert-validity-check.py.py
"""

import os
import logging  # 导入 logging 模块
from datetime import datetime

import prometheus_client
from OpenSSL import crypto
from flask import Flask, Response
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST
from prometheus_client import Gauge

app = Flask(__name__)

# 定义一个仓库
REGISTRY = CollectorRegistry(auto_describe=False)


class CertValidity():
    kube_cert_validity_period = Gauge(
        'kube_cert_validity_period', 'cert validity period', ['filename'], registry=REGISTRY)

    def get_certificate_expiry_date(self, cert_path):
        with open(cert_path, 'rt') as f:
            cert_data = f.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        expiry_date = cert.get_notAfter().decode('utf-8')
        dt = datetime.strptime(expiry_date, "%Y%m%d%H%M%SZ")
        timestamp = dt.timestamp()
        return timestamp

    def filter(self):
        for filename in os.listdir(kube_pki_path):
            if filename.endswith('.crt'):
                self.kube_cert_validity_period.labels(filename).set(
                    self.get_certificate_expiry_date(cert_path="{}/{}".format(kube_pki_path, filename)))


@app.route("/metrics")
@app.route("/")
def cert_validity_period():
    CertValidity().filter()
    return Response(prometheus_client.generate_latest(registry=REGISTRY), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    # 获取环境变量中的 pki 路径
    kube_pki_path = os.getenv('kube_pki_path', "/etc/kubernetes/pki")

    # 设置 Werkzeug 日志级别
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    # 启动 Flask 应用
    app.run(host="0.0.0.0", port=11601, debug=False)

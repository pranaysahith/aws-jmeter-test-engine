# How to install and run InfluxDB and Grafana on Amazon Linux

## OS update
```bash
 sudo yum update -y
```
## Install InfluxDB and start service 

InfluxDB runs on port 8086

```bash
sudo wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.2.x86_64.rpm
sudo yum localinstall influxdb-1.8.2.x86_64.rpm -y
sudo service influxdb start
```
## Install Grafana and start service

Grafana runs on port 3000 
```bash
cat <<EOF | sudo tee /etc/yum.repos.d/grafana.repo
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF
```
```bash
sudo yum -y install grafana
sudo service grafana-server start
sudo chkconfig grafana-server on
```
# Verify that both are running

```bash
netstat -tulpn
```

```bash
[ec2-user@ip-172-31-83-255 ~]$ netstat -tulpn
(No info could be read for "-p": geteuid()=500 but you should be root.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name   
tcp        0      0 0.0.0.0:111                 0.0.0.0:*                   LISTEN      -                   
tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      -                   
tcp        0      0 127.0.0.1:8088              0.0.0.0:*                   LISTEN      -                   
tcp        0      0 127.0.0.1:25                0.0.0.0:*                   LISTEN      -                   
tcp        0      0 0.0.0.0:34971               0.0.0.0:*                   LISTEN      -                   
tcp        0      0 :::58345                    :::*                        LISTEN      -                   
tcp        0      0 :::111                      :::*                        LISTEN      -                   
tcp        0      0 :::22                       :::*                        LISTEN      -                   
tcp        0      0 :::8086                     :::*                        LISTEN      -                   
tcp        0      0 :::3000                     :::*                        LISTEN      -     
```
In above results, server is listening on ports 8086 (influxdb) and 3000(grafana)



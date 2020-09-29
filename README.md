**aws-jmeter-test-engine-v1**

**Project brief**

**Objective:** A AWS cloud test orchestration solution to generate up to 100000 concurrent requests directly to the ICAP server using the c-icap client on AWS platform.

**Requirements:**

- A Configured AWS Cloud Formation stack able to generate large amounts of traffic
- Implemented input mechanism to retrieve required file for processing from S3/MinIO.
- Implemented assertion mechanism that validates the response code returned
- Implemented assertion mechanism that validates the response code returned
- Implemented Influx DB logging solution to log the performance metrics
- A automatic Intelligent Analyzer to automatically detect & flag performance issues for AWS implementation

**Metrics to monitor:**

- **Running Servers Statistics**

- Children number:
- Free Servers:
- Used Servers:
- Started Processes:
- Closed Processes:
- Crashed Processes:
- Closing Processes:

- **Service gw\_rebuild Statistics**

- Service gw\_rebuild REQMODS:
- Service gw\_rebuild RESPMODS:
- Service gw\_rebuild REQUESTS SCANNED:
- Service gw\_rebuild REBUILD FAILURES:
- Service gw\_rebuild REBUILD ERRORS:
- Service gw\_rebuild SCAN REBUILT:
- Service gw\_rebuild UNPROCESSED:
- Service gw\_rebuild UNPROCESSABLE:
- Service gw\_rebuild BYTES IN:
- Service gw\_rebuild BYTES OUT:
- Service gw\_rebuild HTTP BYTES IN:
- Service gw\_rebuild HTTP BYTES OUT:
- Service gw\_rebuild BODY BYTES IN:
- Service gw\_rebuild BODY BYTES OUT:
- Service gw\_rebuild BODY BYTES SCANNED:

**Other metrics:**

- CPU &amp; Memory utilisation of the running pods
- Number of files processed
- Number of concurrent requests processed

**AWS Infrastructure**

- The stack picks up files & generates EC2 instances to execute all the instructions in the scenario file
- JMeter results response times, throughput and error metrics etc. are sent to Influx DB
- The metrics are sent to & displayed on Grafana dashboard
- Automatic Intelligent Analyzer tool automatically detects performance anomalies between builds.

**Success Criteria:**

- The solution setup details are clearly documented with required step by step information and scripts to run
- The solution satisfies all the above defined requirements
- Use of GitHub Actions CI/CD
- The test engine can be started with minimal configuration and run tests with 1 command
- The test engine can run up to 4 million requests to generate up to 100k concurrent requests with use of few files
- Ability to run a continuous heartbeat test successfully with a continuous view of the performance dashboard

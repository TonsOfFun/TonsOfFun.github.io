
# Puma configrations
## Minimum recommended configuration
### Processes
> I recommend that all Ruby webapps run at least 3 processes per server or container - Nate Berkopec https://www.speedshop.co/2017/10/12/appserver.html


### RAM per process considerations
> (TOTAL_RAM / (RAM_PER_PROCESS * 1.2))
We want our application's memory consumption to be stable, but application code that creates a large number of Ruby objects is going to cause memory bloat where the resources of our container exceed their allocation our system resources become saturated and our application becomes unresponsive.

Depending on our application's runtime profile, we may need to increase headroom beyond 1.2x. For example, if our application is memory intensive, we may need to increase headroom to 1.5x or 2x, that is until we can refactor our application to reduce memory consumption and increase performance.

### Calculating RAM per process
## Heroku or similar shared hosting platforms
https://devcenter.heroku.com/articles/deploying-rails-applications-with-the-puma-web-server#recommended-default-puma-process-and-thread-configuration


## Kubernetes deployments
https://github.com/puma/puma/blob/master/docs/kubernetes.md#workers-per-pod-and-other-config-issues
With containerization, you will have to make a decision about how "big" to make each pod. Should you run 2 pods with 50 workers each? 25 pods, each with 4 workers? 100 pods, with each Puma running in single mode? Each scenario represents the same total amount of capacity (100 Puma processes that can respond to requests), but there are tradeoffs to make.

Worker counts should be somewhere between 4 and 32 in most cases. You want more than 4 in order to minimize time spent in request queueing for a free Puma worker, but probably less than ~32 because otherwise autoscaling is working in too large of an increment or they probably won't fit very well into your nodes. In any queueing system, queue time is proportional to 1/n, where n is the number of things pulling from the queue. Each pod will have its own request queue (i.e., the socket backlog). If you have 4 pods with 1 worker each (4 request queues), wait times are, proportionally, about 4 times higher than if you had 1 pod with 4 workers (1 request queue).
Unless you have a very I/O-heavy application (50%+ time spent waiting on IO), use the default thread count (5 for MRI). Using higher numbers of threads with low I/O wait (<50%) will lead to additional request queueing time (latency!) and additional memory usage.
More processes per pod reduces memory usage per process, because of copy-on-write memory and because the cost of the single master process is "amortized" over more child processes.
Don't run less than 4 processes per pod if you can. Low numbers of processes per pod will lead to high request queueing, which means you will have to run more pods.
If multithreaded, allocate 1 CPU per worker. If single threaded, allocate 0.75 cpus per worker. Most web applications spend about 25% of their time in I/O - but when you're running multi-threaded, your Puma process will have higher CPU usage and should be able to fully saturate a CPU core.
Most Puma processes will use about ~512MB-1GB per worker, and about 1GB for the master process. However, you probably shouldn't bother with setting memory limits lower than around 2GB per process, because most places you are deploying will have 2GB of RAM per CPU. A sensible memory limit for a Puma configuration of 4 child workers might be something like 8 GB (1 GB for the master, 7GB for the 4 children).
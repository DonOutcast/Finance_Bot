FROM redis/redis-stack:latest
COPY redis.conf /usr/local/etc/redis/redis.conf
EXPOSE 6379:6379
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]

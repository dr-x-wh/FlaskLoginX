FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN mkdir -p logs
RUN chmod +x /app/bin/run.sh

EXPOSE 9009
CMD ["/app/bin/run.sh"]

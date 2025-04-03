FROM alpine:3.18

RUN apk add --no-cache bash git

COPY . /action
WORKDIR /action

ENTRYPOINT ["/bin/bash", "-c", "echo 'Running release operations composite action'"]
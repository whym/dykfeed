build:
  podman build -t dykfeed .
test: build
  podman run -it dykfeed pytest

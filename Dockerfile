FROM golang:1.21.1-bullseye as base

WORKDIR /src

COPY . .

RUN go mod download
RUN go mod verify

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /app



FROM gcr.io/distroless/static-debian11

WORKDIR /data

COPY --from=base /app /usr/bin

CMD ["app"]

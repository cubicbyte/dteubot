package data

import (
	gocache "github.com/patrickmn/go-cache"
	"time"
)

const TTL = time.Minute * 5

var chatCache *gocache.Cache
var userCache *gocache.Cache

func SetupCache() {
	chatCache = gocache.New(TTL, TTL)
	userCache = gocache.New(TTL, TTL)
}

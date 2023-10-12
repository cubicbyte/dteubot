package data

import (
	gocache "github.com/patrickmn/go-cache"
	"time"
)

const TTL = time.Minute

var chatCache *gocache.Cache
var userCache *gocache.Cache

// SetupCache initializes the database records cache.
// Needed to reduce database load.
func SetupCache() {
	chatCache = gocache.New(TTL, TTL)
	userCache = gocache.New(TTL, TTL)
}

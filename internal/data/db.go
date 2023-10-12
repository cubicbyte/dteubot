package data

import (
	_ "embed"
	"fmt"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/op/go-logging"
)

// TODO: Use pgx

var log = logging.MustGetLogger("database")

// Load SQL queries from files
var (
	//go:embed sql/create_chat.sql
	CreateChatQuery string
	//go:embed sql/create_user.sql
	CreateUserQuery string
	//go:embed sql/get_chat.sql
	GetChatQuery string
	//go:embed sql/get_user.sql
	GetUserQuery string
	//go:embed sql/is_chat_exists.sql
	IsChatExistsQuery string
	//go:embed sql/is_user_exists.sql
	IsUserExistsQuery string
	//go:embed sql/update_chat.sql
	UpdateChatQuery string
	//go:embed sql/update_user.sql
	UpdateUserQuery string
)

var DbInstance *Database

// Database is a PostgreSQL database connection manager.
type Database struct {
	Host     string
	Port     int
	User     string
	Password string
	Database string
	// Should we use SSL to connect to the database?
	Ssl bool
	Db  *sqlx.DB
}

// Connect connects to the database.
func (db *Database) Connect() error {
	log.Info("Connecting to database")

	// Create credentials string
	var sslmode string
	if db.Ssl {
		sslmode = "enable"
	} else {
		sslmode = "disable"
	}

	credentials := fmt.Sprintf(
		"user=%s password=%s host=%s port=%d dbname=%s sslmode=%s",
		db.User, db.Password, db.Host, db.Port, db.Database, sslmode,
	)

	// Connect to the database
	dbConn, err := sqlx.Connect("postgres", credentials)
	if err != nil {
		return err
	}
	db.Db = dbConn

	return nil
}

// Close closes the database connection.
func (db *Database) Close() error {
	log.Info("Closing database connection")

	err := db.Db.Close()
	if err != nil {
		return err
	}

	return nil
}

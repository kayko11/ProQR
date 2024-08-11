const mysql = require('mysql2');

// Create a connection pool
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'admin',
  database: 'mydb',
  port: 3306 // Default MariaDB port
});

// Export the pool with promise support
module.exports = pool.promise();

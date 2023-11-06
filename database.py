from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://sjtbncuj5j4ph3541i3z:pscale_pw_u1xe9tlXfAgkcXffL6aBr5QsQDs4xcKrIYPrNawuzcV@aws.connect.psdb.cloud/baseballstatistics?charset=utf8mb4"

engine = create_engine(
  db_connection_string, 
  connect_args={
    "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem",
    }
  })


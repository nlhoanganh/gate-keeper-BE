class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'xifintest@gmail.com'
    MAIL_PASSWORD = 'rlsjfmivvxckucye'
    MAIL_USE_TLS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/terrathon'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
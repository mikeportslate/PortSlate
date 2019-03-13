# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mikelam:12345678@awssample1.cji0zdy5khnh.us-west-2.rds.amazonaws.com:3306/PortSlate'

SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_ECHO=True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'CTaUlI2kbIe9GFA9jI2Hz9krZRZzF0wEW0Tw7kqf'

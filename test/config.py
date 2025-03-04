import os

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5000)
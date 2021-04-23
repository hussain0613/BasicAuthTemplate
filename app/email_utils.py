import smtplib


#tls port 587

class EmailClient():
    def __init__(self, host='localhost', port=465, username=None, password=None, use_tls=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        
        if(use_tls == '0'): use_tls = False
        self.use_tls = use_tls
        
    def send_message(self, msgobj):
        with smtplib.SMTP(self.host, self.port) as server:
            if(self.use_tls):
                server.starttls()
            if(self.username and self.password):
                server.login(self.username, self.password)
            server.send_message(msgobj)
        
if __name__ == "__main__":
    import email
    from email.message import MIMEPart, EmailMessage
    from email.mime.text import MIMEText
    from dotenv import load_dotenv
    import os
    #with smtplib.SMTP('localhost', 465) as server:
    #    server.starttls()
    #    msg = email.message.EmailMessage()
    #    msg['From'] = "hussain"
    #    msg['To'] = "matha"
    #    msg['Subject'] = 'test'
    #    msg.set_content("yo")
    #    server.send_message(msg)

    #msg = email.message.EmailMessage()
    
    msg = EmailMessage()# MIMEPart()
    msg['From'] = "ibuykhai@gmail.com"
    msg['To'] = "omanush0@gmail.com"
    msg['Subject'] = 'Testing'
    
    
    text= "Hello World Texts"
    html = "<html><body><h1>Hello World</h1></body></html>"
    html_mime = MIMEText("<html><body><h1>Hello World</h1></body></html>", 'html')
    
    #msg.set_type(type = html_mime.get_content_type())

    #msg.set_content()
    msg.set_content(text)
    
    
    load_dotenv(".env")
    SERVER_TYPE = os.getenv('ENVIRONMENT_TYPE')
    if(SERVER_TYPE): load_dotenv(SERVER_TYPE+".env")
    def get_env_vars():
        config = {
            "SECRET_KEY" : os.getenv("SECRET_KEY"),
            "DATABASE_URI" : os.getenv("DATABASE_URI"),
            "MAIL_SERVER" : os.getenv("MAIL_SERVER"),
            "MAIL_PORT" : os.getenv("MAIL_PORT"),
            "MAIL_USERNAME" : os.getenv("MAIL_USERNAME"),
            "MAIL_PASSWORD" : os.getenv("MAIL_PASSWORD"),
            'MAIL_USE_TLS' : os.getenv('MAIL_USE_TLS')
        }
        return config
    env = get_env_vars()
    
    server = EmailClient(env['MAIL_SERVER'], env['MAIL_PORT'], env['MAIL_USERNAME'], env['MAIL_PASSWORD'], env['MAIL_USE_TLS'])
    #server = EmailServer()
    
    server.send_message(msg)
    
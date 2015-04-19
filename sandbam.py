from sandman import app
from sandman.model import activate

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/accounts.db'
app.config['SANDMAN_SHOW_PKS'] = True
app.config['SERVER_HOST'] = '0.0.0.0'
app.config['SERVER_PORT'] = 8080

activate(browser=False)
app.run(host='0.0.0.0', port=8080)

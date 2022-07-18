__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os
from app import app
from layouts import layout_authentication

app.title = "Retail Simulator"
app.layout = layout_authentication.layout

if __name__ == '__main__':
    app.run_server()
    # if os.environ["ENV"] == "deployment":
    #     app.run_server(host="0.0.0.0", port=8050)
    # else:
    #     app.run_server(debug=True, port=8052)
# Xbox Price Tracker

This is a simple Python script that scrapes the Xbox consoles page on the Microsoft Store and stores the prices of each console in a SQLite database. It then checks if the price of a console has changed since the last time the script ran and sends a message to a Telegram chat if there has been a change.

## Installation
Clone the repository:
```bash
git clone https://github.com/baumfaust/xbox-price-tracker.git
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory of the project with the following variables:
```dotenv
BOT_TOKEN=<your Telegram bot token>
CHAT_ID=<the chat ID of the chat you want to send messages to>
```

Run the script:
```bash
python main.py
```

## Usage
The script can be run manually or set up to run automatically at regular intervals using a scheduling tool like Cron or Task Scheduler. The script will check if the price of a console has changed since the last time it ran and send a message to the specified Telegram chat if there has been a change.

### Systemd
To run the script every 2 hours on Arch Linux using systemd, follow these steps:

Create a new systemd service file:
```bash
sudo nano /etc/systemd/system/xbox-price-tracker.service
```

Add the following configuration:
```makefile
[Unit]
Description=Xbox Price Tracker
After=network-online.target

[Service]
Type=simple
User=<your username>
WorkingDirectory=<path to the project directory>
ExecStart=/usr/bin/python main.py
Restart=always
RestartSec=120

[Install]
WantedBy=multi-user.target
```

Save the file and exit nano.

Reload the systemd daemon:
```bash
sudo systemctl daemon-reload
```

Enable the service to start on boot:
```bash
sudo systemctl enable xbox-price-tracker.service
```

Start the service:
```bash
sudo systemctl start xbox-price-tracker.service
```

The script will now run every 2 hours and send a message to your specified Telegram chat if there has been a change in the price of any Xbox console.

## Contributing
If you find any bugs or issues with the script, please feel free to submit an issue or pull request.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

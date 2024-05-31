# SMM Integrated Telegram Bot

This repository contains the source code for an integrated Telegram bot for social media marketing (SMM) purposes.

## Overview

This Telegram bot integrates with an SMM API to provide various services related to social media promotion, including ordering, checking status, and managing orders.

## Features

- **Ordering Services**: Users can place orders for various social media services.
- **Checking Status**: Users can check the status of their orders.
- **Managing Orders**: Users can manage their orders, such as cancelling or refilling them.
- **Balance Inquiry**: Users can check their account balance.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/deeorbeck/smmbot.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the bot by editing the `data/config.py` file and providing your API keys and other required parameters.

4. Run the bot:

    ```bash
    python app.py
    ```

## Usage

- Start the bot by messaging it on Telegram.
- Follow the on-screen instructions to place orders, check order status, manage orders, and inquire about your balance.

## API Integration

This bot integrates with an SMM API to provide its services. The `Api` class handles the communication with the API server. It supports various API actions such as ordering, checking status, refilling, cancelling orders, and querying account balance.

## Database Models

The bot uses a database to store user information, orders, categories, and services. The database models are defined using Django's ORM.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/deeorbeck/smmbot?tab=MIT-1-ov-file) file for details.

## Access

You can access the bot at [ismailov.uz](https://ismailov.uz)
#!/bin/bash

sudo rm /etc/systemd/coupon.service
sudo cp coupon.service /etc/systemd/coupon.service
sudo systemctl daemon-reload
sudo systemctl status coupon.service



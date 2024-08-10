#!/bin/bash

# Function to print success message in green
log_success() {
    local message="$1"
    echo -e "\033[0;32m$message\033[0m"
}

# Function to print error message in red
log_error() {
    local message="$1"
    echo -e "\033[0;31m$message\033[0m"
}
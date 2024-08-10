#!/bin/bash
reset_db() {
    echo "{}" > "$db_path"
}

# This will loop until a specific test is printed and then it will call the callback function
# if the text is not printed it will reach timeout and will return 1
wait_for_output_with_timeout() {
  local file=$1
  local search_string=$2
  local timeout=$3
  local callback=$4

  local start_time=$(date +%s)

  while true; do
    if grep -q "$search_string" "$file"; then
      if [ -n "$callback" ]; then
        eval "$callback" # Execute the callback
      fi
      return 0 # Success
    fi

    local current_time=$(date +%s)
    local elapsed_time=$((current_time - start_time))

    if [ "$elapsed_time" -ge "$timeout" ]; then
      return 1 # Timeout
    fi

    sleep 1
  done
}

start_server() {
  local callback=$1
  local output_server=$(mktemp)

  reset_db

  python3 -u ./server/src/server.py > "$output_server" 2>&1 &
  SERVER_PID=$!

  if ! wait_for_output_with_timeout "$output_server" "running server" "$server_startup_max_wait_time" "$callback"; then
    echo "Failed to start server"
    rm "$output_server"
    reset_db
    exit 1
  fi

  rm "$output_server"
}

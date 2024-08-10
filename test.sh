# Start the server script in the background and capture its output in a variable
export TEST_MODE=true

server_startup_max_wait_time=20
db_path="./tests/helpers/db.json"

# helpers to log and run server
source ./tests/helpers/logger.sh
source ./tests/helpers/run_server.sh

# Node tests
source ./tests/node.sh

reset_db

log_success "aaAll tasks completed successfully."

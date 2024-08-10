#!/bin/bash
node_tests() {
    local output_stub=$(mktemp)
    local max_wait_time=5

    create() {
        node ./client-node/index.js create --name=testchannel --type=SIMPLE > "$output_stub" 2>&1 &
        STUB_PID=$!

        if wait_for_output_with_timeout "$output_stub" "queue created successfully" "$max_wait_time"; then
            log_success "node pass: create queue"
        else
            cat $output_server
            cat $output_stub
            rm "$output_server"
            log_error "node fail: error to create queue"
            kill $SERVER_PID
            exit 1
        fi
    }

    publish() {
        node ./client-node/index.js publish --name=testchannel --messages=abc,xyz > "$output_stub" 2>&1 &
        STUB_PID=$!

        if wait_for_output_with_timeout "$output_stub" "messages published" "$max_wait_time"; then
            log_success "node pass: publish"
        else
            cat $output_server
            cat $output_stub
            rm "$output_server"
            log_error "node fail: error to publish"
            kill $SERVER_PID
            exit 1
        fi
    }

    list() {
        node ./client-node/index.js list > "$output_stub" 2>&1 &
        STUB_PID=$!

        if wait_for_output_with_timeout "$output_stub" "list os queues" "$max_wait_time"; then
            log_success "node pass: list"
        else
            cat $output_server
            cat $output_stub
            rm "$output_server"
            log_error "node fail: error to list"
            kill $SERVER_PID
            exit 1
        fi
    }

    remove() {
        node ./client-node/index.js remove --name=testchannel > "$output_stub" 2>&1 &
        STUB_PID=$!

        if wait_for_output_with_timeout "$output_stub" "queue removed" "$max_wait_time"; then
            log_success "node pass: remove"
        else
            cat $output_server
            cat $output_stub
            rm "$output_server"
            log_error "node fail: error to remove"
            kill $SERVER_PID
            exit 1
        fi
    }

    cb () {
        create
        sleep 1

        publish
        sleep 1

        list
        sleep 1
        
        remove
        kill $SERVER_PID
    }

    start_server cb
}

node_tests

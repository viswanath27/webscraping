#!/bin/bash
start (){
    echo "Start of the rasa"
    conda activate rasa_env
    echo "Activated the env"
    cd rasa
    echo "moved to the required directory"
    rasa run actions >> action_server_log.txt 2>&1 & echo $! >> action_server.pid

    #rasa run actions & | tee -a process_1.txt
    echo "Rasa action server up"
    rasa run --enable-api --cors "*" >> core_server_log.txt 2>&1 & echo $! >> core_server.pid
    echo "Rasa main server up"
    echo "Activate ui env"
    conda activate base
    echo "Moving back to the main folder"
    cd ../ui_app
    echo "avoid stoping the background server"
    stty -tostop
    echo "Start of ui server"
    python app.py
}

stop (){
    action_server_pid="rasa/action_server.pid"
    if [ -f "rasa/action_server.pid" ]; then 
        #read line < "rasa/action_server.pid"
        pid=$(cat rasa/action_server.pid)
        kill $pid
        rm -rf rasa/action_server.pid
    fi
    core_server_pid="rasa/core_server.pid"
    if [ -f "rasa/core_server.pid" ]; then 
        #read line1 < "rasa/core_server.pid"
        pid=$(cat rasa/core_server.pid)
        kill $pid
        rm -rf rasa/core_server.pid
    fi
}

case $1 in
    start) "$@"; exit;;
    stop) "$@"; exit;;
    #     # action_server_pid="rasa/action_server.pid"
    #     if [ -f rasa/action_server.pid ]; then 
    #         #read line < "rasa/action_server.pid"
    #         pid=$(cat rasa/action_server.pid)
    #         kill $pid
    #         rm -rf rasa/action_server.pid
    #     fi
    # ;;
    *) 
        echo "Usage: $0 {start|stop}"
        exit 1
esac



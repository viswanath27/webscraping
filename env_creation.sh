rm -rf ~/webscraping
git clone https://github.com/viswanath27/webscraping.git
echo "Setting the servers"
sudo apt install software-properties-common --assume-yes
sudo add-apt-repository ppa:deadsnakes/ppa -y
echo "Installing Python 3.8"
sudo apt-get install  python3.8 --assume-yes
sudo apt-get install python3.8-dev python3.8-venv --assume-yes
echo "Installing pip"
sudo apt-get install python3-pip --assume-yes
cd ~
echo "create env dir"
mkdir rasa_env
echo "create virtual env"
python3.8 -m venv rasa_env
echo "Acticate virtual env"
source ~/rasa_env/bin/activate
echo "Installing Rasa with Transformers"
pip install rasa[transformers] --quiet
pip3 install boto3 --quiet
pip3 install flask
export AWS_SECRET_ACCESS_KEY=3oTbM1F+BENxWrhHFRub7gNfB2DtvfhvkztpdSLV
export AWS_ACCESS_KEY_ID=AKIAZ74VWP2NKSAYXVTV
export AWS_DEFAULT_REGION=ap-northeast-1
export BUCKET_NAME=ssrasafinancebot
export AWS_ENDPOINT_URL=https://ssrasafinancebot.s3.ap-northeast-1.amazonaws.com/models/20220903-172133-khaki-lion.tar.gz

echo "create rasa core dir"
#mkdir rasa_core
#cd rasa_core
cd webscraping/src/rasa
echo "Start rasa core .."
rasa run --model 20220903-172133-khaki-lion.tar.gz --remote-storage aws &
echo "Start rasa action server .."
rasa run actions &
echo "Starting the UI server .."
cd ~/webscraping/src/ui_app
python3 app.py &
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
echo "create rasa core dir"
cd webscraping/src/rasa
#mkdir rasa_core
#cd rasa_core
echo "Start rasa_init"
rasa init --no-prompt

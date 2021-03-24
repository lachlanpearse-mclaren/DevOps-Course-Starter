Vagrant.configure("2") do |config|
    config.vm.box = "hashicorp/bionic64"
    config.vm.network "forwarded_port", guest: 5000, host: 5000
    config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    SHELL
    config.vm.provision "shell", privileged: false, inline: <<-SHELL    
        git clone https://github.com/pyenv/pyenv.git ~/.pyenv
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
    SHELL
    config.vm.provision "shell", privileged: false, inline: <<-SHELL
        pyenv install 3.9.0
        pyenv global 3.9.0
        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python 
    SHELL
    config.vm.provision "shell", privileged: false, inline: <<-SHELL 
        cd /vagrant
        poetry install
        sudo cp /vagrant/gunicorn.service /etc/systemd/system
        sudo sed -i "s#VENV_PATH#$(poetry env info --path)#g" /etc/systemd/system/gunicorn.service
        sudo systemctl daemon-reload
    SHELL
    config.trigger.after :up do |trigger|
        trigger.name = "Launching App"
        trigger.info = "Running the TODO app setup script"
        trigger.run_remote = {inline: "
        systemctl start gunicorn        
        "}
    end
end
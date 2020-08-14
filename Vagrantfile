
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  
  config.vm.provision "shell", privileged: false, inline: <<-SHELL 
    sudo apt-get update
    
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
      libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
      xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    
    # sourcing ~/.bashrc doesn't seem to work...
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    echo 'eval "$(pyenv init -)"' > ~/.bashrc
    pyenv install 3.8.1 
    pyenv global 3.8.1

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
      # Install dependencies and launch
      # <your script here>
      cd /vagrant
      export PATH=\"$HOME/.pyenv/bin:$PATH\"
      eval \"$(pyenv init -)\"
      pyenv shell 3.8.1
      poetry install
      poetry run flask run --host=0.0.0.0
    "}
  end
end

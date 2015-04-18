$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-get --assume-yes update
    apt-get --assume-yes dist-upgrade
    apt-get install --assume-yes \
        python2.7 \
        python2.7-dev \
        python-pip \
        firefox \
        ca-certificates \
        xfonts-100dpi \
        xfonts-75dpi \
        xfonts-scalable \
        xfonts-cyrillic \
        xvfb --no-install-recommends
    pip install supervisor sandman
    pip install -r /vagrant/requirements.txt
    ln -s /vagrant/supervisord.conf /etc/supervisord.conf
    echo "DISPLAY=:99" >> /etc/environment
    cat /vagrant/.env >> /etc/environment
    curl "https://raw.githubusercontent.com/Supervisor/initscripts/master/ubuntu" > /etc/init.d/supervisor
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.33.18"
  config.vm.provision "shell", inline: $script
  config.vm.hostname = "dev.bam.local"
end

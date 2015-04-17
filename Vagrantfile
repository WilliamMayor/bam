$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-get --assume-yes update
    apt-get --assume-yes upgrade
    
    wget -qO- https://get.docker.com/ | sh
    usermod -aG docker vagrant
    
    wget -qO- https://raw.githubusercontent.com/WilliamMayor/vantage/master/bootstrap.sh | sh
    echo "VG_APP_DIR=/vagrant" >> /etc/environment
    echo "VG_PLUGIN_PATH=/vagrant/vantage" >> /etc/environment
    echo "VG_DEFAULT_ENV=/vagrant/.env" >> /etc/environment
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.33.18"
  config.vm.provision "shell", inline: $script
  config.vm.hostname = "dev.bam.local"
end

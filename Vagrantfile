$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-get --assume-yes update
    apt-get --assume-yes dist-upgrade
    apt-get --assume-yes install git

    usermod --home /vagrant vagrant

    wget -O- https://get.docker.com/ | sh
    usermod -aG docker vagrant
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell", inline: $script
end

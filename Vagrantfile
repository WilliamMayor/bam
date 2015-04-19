$script = <<SCRIPT
    locale-gen en_GB.UTF-8
    apt-get --assume-yes update
    apt-get --assume-yes dist-upgrade
    wget -qO- https://get.docker.com/ | sh
    usermod -aG docker vagrant
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.33.18"
  config.vm.provision "shell", inline: $script
  config.vm.hostname = "dev.bam.local"
end

$script = <<SCRIPT
    
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "deb/wheezy-amd64"
  config.vm.network "private_network", ip: "192.168.33.18"
  config.vm.provision "shell", inline: $script
  config.vm.hostname = "dev.bam.local"
end

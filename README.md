# Deprecated please try arfedora-weclome

https://github.com/yucefsourani/arfedora-welcome


# LUniversalInstaller
https://arfedora.blogspot.com

Python+Gtk  Universal Installer



# Screenshot (Terminal Supported (if Vte291 exists))

![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/0.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/1.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/2.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/3.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/4.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/5.png "Screenshot")


![Alt text](https://raw.githubusercontent.com/yucefsourani/LUniversalInstaller/master/Screenshot/6.png "Screenshot")





# Some Plugin Requires

python3-beautifulsoup4

flatpak


# Install (Require Meson)

cd && git clone https://github.com/yucefsourani/LUniversalInstaller

cd ~/LUniversalInstaller

meson setup builddir

sudo meson install -C builddir


# Install on Fedora

 sudo dnf copr enable youssefmsourani/luniversalinstaller -y
 
 sudo dnf install luniversalinstaller -y


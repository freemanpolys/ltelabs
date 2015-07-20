__author__ = 'James Kokou GAGLO'
__copyright__ = "Copyright {YEAR}, Dovealabs"
__credits__ = ["James Kokou GAGLO"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "James Kokou GAGLO"
__email__ = "freemanpolys@gmail.com"
__status__ = "Production"

from fabric.api import hosts, run,runs_once,cd

ims_core = ('vagrant@192.168.56.100')
pcscsf=('vagrant@192.168.56.100')
icscsf=('vagrant@192.168.56.100')
scscsf=('vagrant@192.168.56.100')
hss=('vagrant@192.168.56.100')

@hosts(ims_core)
def install():
    apt_update()
    run("sudo apt-get install libcurl4-gnutls-dev -y")
    run("sudo apt-get install bison -y")
    run("sudo apt-get install curl -y")
    run("sudo apt-get install debhelper cdbs lintian build-essential fakeroot devscripts pbuilder dh-make debootstrap dpatch flex libxml2-dev libmysqlclient15-dev ant docbook-to-man -y")
    run("sudo apt-get install ipsec-tools -y")
    run("sudo apt-get install subversion -y")
    # run("sudo apt-get install mysql-server-5.5 -y")
    run("sudo apt-get install libmysqlclient18 libmysqlclient-dev -y")

    # install JDK 7
    run("sudo apt-get install python-software-properties debconf-utils -y")
    run("sudo add-apt-repository ppa:webupd8team/java")
    apt_update()
    run("echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections")
    run("echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections")
    run("sudo apt-get install oracle-java7-installer -y")

    # set up the Java 7 environment variables JAVA_HOME and PATH
    run("sudo apt-get install oracle-java7-set-default -y")

    # Download openIMScore
    imscore ="/opt/OpenIMSCore"
    run("sudo mkdir -p "+imscore)
    with cd(imscore):
        run("sudo svn checkout https://svn.code.sf.net/p/openimscore/code/ser_ims/trunk/ ser_ims")
        # solve problem on ubuntu 12
        run("sudo sed -i '/include <curl\/types.h>/d' ser_ims/lib/lost/client.h")

    with cd(imscore+"/ser_ims"):
        run("sudo make install-libs all")

@runs_once
def apt_update():
    run("sudo apt-get update -y")
@hosts(hss)
def ins_hss():
    run("sudo apt-get install mysql-server-5.5 -y")
    run("sudo apt-get install libmysqlclient18 libmysqlclient-dev -y")
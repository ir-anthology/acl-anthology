srun -v --container-writable --container-image=ubuntu:20.04 "--container-mounts=/mnt/ceph/storage/data-tmp/$(date +"%Y")/$(whoami):/ceph" --container-name=ir-anthology-build --mem=20g --cpu-freq=high --cpus-per-task 8 bash -c "
set -e
apt-get update
apt-get install -y hugo python3-pip python3-venv wget git
cd /tmp
rm -rf ir-anthology
git clone https://github.com/ir-anthology/ir-anthology
cd ir-anthology
make
tar -cf build.tar build
rm -rf /ceph/ir-anthology_build
mkdir /ceph/ir-anthology_build
mv wcsp.ldjson /ceph/ir-anthology_build/
mv build.tar /ceph/ir-anthology_build/
"
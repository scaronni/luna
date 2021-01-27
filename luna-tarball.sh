#!/bin/sh -e

INSTALLER=610-000397-003_SW_Linux_Luna_Client_V10.3.0_RevA.tar
VERSION=10.3.0
NAME=luna

rm -fr $NAME-$VERSION
mkdir $NAME-$VERSION

tar -C $NAME-$VERSION/ -xvf $INSTALLER --strip-components=1

pushd $NAME-$VERSION

rm -f 64/{plink,pscp,common,*i686.rpm}

for srpm in 64/*.src.rpm; do
    kmod_src=$(rpm -qpl $srpm | grep -v spec)
    rpm2cpio $srpm | cpio -idm $kmod_src
    rm -f $srpm
done

mkdir kmod
mv *gz kmod/

mkdir scripts

for rpm in 64/*.rpm; do
    rpm2cpio $rpm | cpio -idm
    rpm -qpi $rpm > scripts/$(basename $rpm.txt)
    rpm -qpl $rpm >> scripts/$(basename $rpm.txt)
    rpm -qp --scripts $rpm >> scripts/$(basename $rpm.txt)
done

rm -fr 64

chmod -x *txt *pdf

popd

tar --remove-files -cJf $NAME-$VERSION.tar.xz $NAME-$VERSION

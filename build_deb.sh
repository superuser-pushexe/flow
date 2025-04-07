#!/bin/bash
echo "Building .deb package..."
dpkg-deb --build debian
mv debian.deb python-desktop-x11_1.0_all.deb
echo "Done! Package is: python-desktop-x11_1.0_all.deb"

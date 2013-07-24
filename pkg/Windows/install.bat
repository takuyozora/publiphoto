echo off

echo Installation des fichiers necessaires a Publi' Photo

echo Installation de Python ...
python-3.3.2.msi

echo Installation de Pillow ...
Pillow-2.1.0.win32-py3.3.exe

echo Installation de GTK ...
set pypath=C:\Python33\Lib\site-packages

cd pygobject

copy pygtk.pth %pypath%
mkdir %pypath%\gtk
xcopy gtk %pypath%\gtk /E
mkdir %pypath%\gi
xcopy gi %pypath%\gi /E
mkdir %pypath%\cairo
xcopy cairo %pypath%\cairo /E
cd ../

:locale
cd ../../
cd po

mkdir C:\locale\fr_FR\LC_MESSAGES
copy fr\LC_MESSAGES\publiphoto.mo C:\locale\fr_FR\LC_MESSAGES


echo Installation terminée

pause
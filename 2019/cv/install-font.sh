CACHE_DIR=~/.adobe-source-han-serf
FONT_DIR=~/.fonts/adobe-fonts

mkdir -p $CACHE_DIR
cd $CACHE_DIR
wget https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SourceHanSerifSC_SB-H.zip
wget https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/OTF/SourceHanSerifSC_EL-M.zip
unzip SourceHanSerifSC_SB-H.zip
unzip SourceHanSerifSC_EL-M.zip

mkdir -p $FONT_DIR
cp -r ./SourceHanSerifSC_EL-M ./SourceHanSerifSC_SB-H $FONT_DIR
fc-cache -f -v $FONT_DIR/SourceHanSerifSC_EL-M
fc-cache -f -v $FONT_DIR/SourceHanSerifSC_SB-H

rm -rf $CACHE_DIR
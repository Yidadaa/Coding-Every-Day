# 用来新建本周的周报

week=$(date +"%V")

dirname="week-$week"

template='\documentclass{article}\n\n
\input{../template/structure.tex}\n\n
\\title{CFM AI\&VR Weekly Report: Week \#'$week' of 2019}\n\n
\\author{Zhang Yifei(\\texttt{yidadaa@qq.com})}\n\n
\date{UESTC --- \\today}\n\n
\\begin{document}\n\n
\maketitle\n\n
\section{Summary}\n\n
\section{Plan}\n\n
\\end{document}'

if [ -d $dirname ]; then
    echo "你已经写过第$week 周的周报了"
else
    mkdir $dirname
    cd $dirname
    echo $template > "$dirname.tex"
    echo "模板已生成"
fi
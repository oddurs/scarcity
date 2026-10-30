# latexmk configuration: LuaLaTeX + biber, build products in paper/build/.
$pdf_mode = 4;                # 4 = lualatex
$lualatex = 'lualatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=0 %O %S';
$bibtex_use = 2;              # run biber when needed; delete .bbl on clean
$out_dir = 'build';
$aux_dir = 'build';
$max_repeat = 6;
@default_files = ('main.tex');

dir .\export_svg\*.svg /b > .\export_svg\inkscape_export_pdf_list_svg.txt
for /f "tokens=1 delims=." %%a in ( .\export_svg\inkscape_export_pdf_list_svg.txt ) do ( 
"C:\Program Files\Inkscape\\inkscape.com" -f .\export_svg\%%a.svg -A .\export_pdf\%%a.pdf
 )
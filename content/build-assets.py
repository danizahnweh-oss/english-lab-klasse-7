from pathlib import Path
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[1]/'dist/material'
regions=[(2021,2,(89,613,816,852),'listening'),(2022,4,(221,865,788,1075),'listening'),(2023,3,(162,615,757,779),'listening'),(2024,2,(128,580,829,735),'listening'),(2021,5,(89,441,860,1113),'writing'),(2022,7,(91,354,868,1176),'writing'),(2023,5,(105,346,879,1135),'writing'),(2024,6,(104,364,871,861),'writing'),(2025,6,(80,390,880,1140),'writing')]
for y,page,region,kind in regions:
 d=pdfium.PdfDocument(R/f'JA7_GY_E_{y}_Aufg.pdf')
 d[page-1].render(scale=1.6).to_pil().crop(region).save(R/f'{y}-{kind}.webp',quality=92)

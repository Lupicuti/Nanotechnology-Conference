# -*- coding: utf-8 -*-
"""
Script per generare il documento PDF riepilogativo di logistica, preventivi e contatti
da allegare alla mail per la direzione SSAS e la segreteria.
Predisposto a cura del comitato organizzatore studenti SSAS Sapienza.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def create_pdf(filename="preventivo_logistica_relatori_ssas.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#64748B'),
        alignment=1, # Center
        spaceAfter=10
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading1'],
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B')
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=body_style,
        fontSize=8.5,
        leading=11.5
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    story = []
    
    # Intestazione istituzionale
    story.append(Paragraph("SCUOLA SUPERIORE DI STUDI AVANZATI SAPIENZA (SSAS) • COMITATO ORGANIZZATORE", header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=10))
    
    # Titolo
    story.append(Paragraph("DOCUMENTO RIEPILOGATIVO LOGISTICA E PREVENTIVI", title_style))
    story.append(Spacer(1, 8))
    
    # Sezione 1
    story.append(Paragraph("1. Logistica e contatti dei relatori plenari confermati", h1_style))
    story.append(Paragraph(
        "Il presente documento riepiloga le necessità organizzative, i contatti e i costi stimati per l'accoglienza dei relatori. "
        "In questa prima sezione sono riportate le spese logistiche di base (viaggi e pernottamenti essenziali). Le opzioni per "
        "estendere il pernottamento a due notti per tutti i relatori e per invitare speaker supplementari sono dettagliate nelle sezioni successive.",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Le stime di costo fanno riferimento a hotel 4 stelle in zona Sapienza, compagnie aeree di linea e treni ad alta velocità. "
        "È stato applicato un margine prudenziale di 20-30 euro su ciascuna voce per assorbire eventuali fluttuazioni di prezzo.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Tabella Relatori Confermati
    headers = [
        Paragraph("Relatore e Afferenza", table_header),
        Paragraph("Mezzo e Tratta", table_header),
        Paragraph("Pernottamento (Base)", table_header),
        Paragraph("Stima Costo", table_header)
    ]
    
    data = [headers,
        [
            Paragraph("Carlo Beenakker<br/>Leiden University<br/>beenakker@lorentz.leidenuniv.nl", table_cell),
            Paragraph("Volo A/R<br/>Amsterdam ↔ Roma FCO", table_cell),
            Paragraph("1 notte (17 sett.)", table_cell),
            Paragraph("Volo: ~250-320 €<br/>Hotel: ~160-185 €<br/>Tot: ~410-505 €", table_cell)
        ],
        [
            Paragraph("Kazu Suenaga<br/>Osaka University / AIST<br/>suenaga@sanken.osaka-u.ac.jp", table_cell),
            Paragraph("Già in Italia<br/>(Nessun volo richiesto)", table_cell),
            Paragraph("1 notte (17 sett.)", table_cell),
            Paragraph("Volo: 0 €<br/>Hotel: ~160-185 €<br/>Tot: ~160-185 €", table_cell)
        ],
        [
            Paragraph("Maximilian Haider<br/>CEOS GmbH / KIT<br/>haider@ceos-gmbh.de", table_cell),
            Paragraph("Già in Italia<br/>(Nessun volo richiesto)", table_cell),
            Paragraph("1 notte (17 sett.)", table_cell),
            Paragraph("Volo: 0 €<br/>Hotel: ~160-185 €<br/>Tot: ~160-185 €", table_cell)
        ],
        [
            Paragraph("Francesco De Angelis<br/>IIT<br/>francesco.deangelis@iit.it", table_cell),
            Paragraph("Volo A/R<br/>Sicilia ↔ Roma FCO", table_cell),
            Paragraph("Nessun pernottamento<br/>(Alloggio a Roma)", table_cell),
            Paragraph("Volo A/R: ~120-170 €<br/>Hotel: 0 €<br/>Tot: ~120-170 €", table_cell)
        ],
        [
            Paragraph("Gabriella Di Carlo<br/>CNR-ISMN<br/>gabriella.dicarlo@cnr.it", table_cell),
            Paragraph("Sede lavorativa a Roma", table_cell),
            Paragraph("Nessun pernottamento", table_cell),
            Paragraph("Viaggio: 0 €<br/>Hotel: 0 €<br/>Tot: 0 €", table_cell)
        ],
        [
            Paragraph("Camilla Coletti<br/>IIT & CNI@NEST<br/>camilla.coletti@iit.it", table_cell),
            Paragraph("Treno AV A/R<br/>Pisa ↔ Roma Termini", table_cell),
            Paragraph("Nessun pernottamento<br/>(Rientro in giornata)", table_cell),
            Paragraph("Treno: ~80-100 €<br/>Hotel: 0 €<br/>Tot: ~80-100 €", table_cell)
        ],
        [
            Paragraph("Giulia Serrano<br/>Università di Firenze<br/>giulia.serrano@unifi.it", table_cell),
            Paragraph("Treno AV A/R<br/>Firenze ↔ Roma Termini", table_cell),
            Paragraph("Nessun pernottamento<br/>(Rientro in giornata)", table_cell),
            Paragraph("Treno: ~70-90 €<br/>Hotel: 0 €<br/>Tot: ~70-90 €", table_cell)
        ],
        [
            Paragraph("Alessandro Tredicucci<br/>Università di Pisa<br/>alessandro.tredicucci@unipi.it", table_cell),
            Paragraph("Treno AV A/R<br/>Pisa ↔ Roma Termini", table_cell),
            Paragraph("Nessun pernottamento<br/>(Rientro in giornata)", table_cell),
            Paragraph("Treno: ~80-100 €<br/>Hotel: 0 €<br/>Tot: ~80-100 €", table_cell)
        ],
        [
            Paragraph("TOTALE RELATORI (8)", table_cell_bold),
            Paragraph("2 Voli + 4 Treni AV", table_cell_bold),
            Paragraph("3 Notti Hotel tot.", table_cell_bold),
            Paragraph("~ 1.080 € - 1.335 €", table_cell_bold)
        ]
    ]
    
    t = Table(data, colWidths=[5.4*cm, 4.6*cm, 4.2*cm, 3.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 12))
    
    # Sezione 2
    story.append(Paragraph("2. Opzioni per 2 relatori plenari supplementari", h1_style))
    story.append(Paragraph(
        "Per completare il programma, abbiamo individuato 2 possibili relatori supplementari. Prima di procedere con gli inviti formali, "
        "sottoponiamo due opzioni di spesa per valutare la disponibilità del budget residuo:",
        body_style
    ))
    story.append(Spacer(1, 6))
    
    headers_extra = [
        Paragraph("Opzione Supplementare", table_header),
        Paragraph("Modalità Logistica", table_header),
        Paragraph("Impatto sul Budget ", table_header)
    ]
    data_extra = [
        headers_extra,
        [
            Paragraph("Opzione A: economica<br/>(2 relatori dall'Italia)", table_cell),
            Paragraph("Solo treno AV A/R.<br/>Nessun pernottamento (rientro in giornata).", table_cell),
            Paragraph("Treni : ~160 - 200 €<br/>Hotel: 0 €<br/>Totale: ~160 - 200 €", table_cell)
        ],
        [
            Paragraph("Opzione B: internazionale<br/>(2 relatori dall'estero)", table_cell),
            Paragraph("Volo A/R per Roma FCO e pernottamento di 1 notte per ciascun relatore.", table_cell),
            Paragraph("Voli : ~500 - 640 €<br/>Hotel (2 notti): ~320 - 370 €<br/>Totale: ~820 - 1.010 €", table_cell)
        ]
    ]
    t_extra = Table(data_extra, colWidths=[5.6*cm, 7.8*cm, 4.6*cm])
    t_extra.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_extra)
    story.append(Spacer(1, 12))
    
    # Sezione 3
    story.append(Paragraph("3. Trasporti e aule per i workshop", h1_style))
    story.append(Paragraph(
        "Per i workshop pomeridiani di venerdì 18 settembre (15:00 - 18:00) sono previste le seguenti necessità logistiche:",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "- Navetta: servizio riservato per raggiungere i laboratori di San Pietro in Vincoli dall'Aula Amaldi e ritorno (stima prudenziale: ~170 - 250 €).",
        bullet_style
    ))
    story.append(Paragraph(
        "- Aule didattiche: alcune sessioni pratiche potrebbero richiedere l'uso delle aule della Scuola. Seguiranno dettagli sul numero esatto di spazi necessari.",
        bullet_style
    ))
    story.append(Spacer(1, 12))
    
    # Sezione 4
    story.append(Paragraph("4. Materiale tipografico e catering", h1_style))
    story.append(Paragraph(
        "Di seguito le stime per i materiali di supporto e la ristorazione per entrambe le giornate:",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "- Materiale tipografico: locandine, flyer, roll-up, stampa dei poster per la sessione ricercatori e badge (stima complessiva: ~250 - 400 €).",
        bullet_style
    ))
    story.append(Paragraph(
        "- Catering (coffee e lunch break): sono previsti coffee break per entrambe le giornate. Per il pranzo a buffet, proponiamo due alternative in base ai fondi disponibili:",
        bullet_style
    ))
    story.append(Paragraph(
        "- Lunch ristretto: riservato a relatori, membri del comitato scientifico, organizzatori e staff.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=30, fontSize=8.5, leading=12)
    ))
    story.append(Paragraph(
        "- Lunch completo: esteso a tutti i partecipanti registrati alla conferenza.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=30, fontSize=8.5, leading=12)
    ))
    story.append(Spacer(1, 12))
    
    # Sezione 5
    story.append(Paragraph("5. Riepilogo scenari di preventivo", h1_style))
    story.append(Paragraph(
        "Di seguito il riepilogo degli scenari, che confrontano la copertura logistica essenziale con l'opzione estesa a 2 notti per tutti i relatori. "
        "Si precisa che Francesco De Angelis e Gabriella Di Carlo non necessitano di pernottamento. L'opzione a 2 notti copre pertanto i restanti 6 relatori (12 notti totali).",
        body_style
    ))
    story.append(Spacer(1, 6))
    
    summary_headers = [
        Paragraph("Scenario", table_header),
        Paragraph("Voci Logistiche Incluse", table_header),
        Paragraph("Stima Costo", table_header)
    ]
    summary_data = [
        summary_headers,
        [
            Paragraph("Scenario 1: Base<br/>(8 relatori confermati)", table_cell),
            Paragraph("Voli/treni per gli 8 confermati + 3 notti hotel tot. + Navetta + Materiale tipografico base.", table_cell),
            Paragraph("~ 1.500 € - 1.985 €", table_cell_bold)
        ],
        [
            Paragraph("Scenario 2: Full Conference<br/>(8 relatori confermati)", table_cell),
            Paragraph("Voli/treni per gli 8 confermati + 12 notti hotel tot. + Navetta + Materiale tipografico e catering.", table_cell),
            Paragraph("~ 2.550 € - 3.250 €", table_cell_bold)
        ],
        [
            Paragraph("Scenario 3: 2 Notti + 2 relatori extra (Italia)", table_cell),
            Paragraph("Scenario 2 + 2 relatori supplementari italiani (treno AV + 2 notti hotel).", table_cell),
            Paragraph("~ 3.030 € - 3.820 €", table_cell_bold)
        ],
        [
            Paragraph("Scenario 4: 2 Notti + 2 relatori extra (Estero)", table_cell),
            Paragraph("Scenario 2 + 2 relatori supplementari esteri (voli A/R + 2 notti hotel).", table_cell),
            Paragraph("~ 3.690 € - 4.630 €", table_cell_bold)
        ]
    ]
    
    t_summary = Table(summary_data, colWidths=[5.4*cm, 8.0*cm, 4.6*cm])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(t_summary)
    story.append(Spacer(1, 14))
    
    doc.build(story)
    print(f"PDF generato con successo: {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_pdf()